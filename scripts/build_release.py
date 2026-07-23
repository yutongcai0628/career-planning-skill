#!/usr/bin/env python3
"""Build a deterministic, allowlisted RedSkill upload package."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / ".claude" / "skills" / "career-planning"
DEFAULT_RELEASE = ROOT / "release"
PACKAGE_NAME = "career-planning"
MAX_FILE_BYTES = 10 * 1024 * 1024
MAX_TOTAL_BYTES = 30 * 1024 * 1024

# A public package is assembled from this exact list. New files fail the build
# until a maintainer explicitly reviews and adds them here.
PUBLIC_FILES = (
    "SKILL.md",
    "agents/openai.yaml",
    "assets/报告数据示例.json",
    "assets/报告模板.html",
    "assets/报告设计哲学.md",
    "references/中期规划.md",
    "references/交互与可视化.md",
    "references/决策协议与质量门槛.md",
    "references/导出报告.md",
    "references/岗位分析.md",
    "references/持续档案.md",
    "references/标杆与思维透镜.md",
    "references/职业反脆弱.md",
    "references/能力点挖掘.md",
    "references/行业与岗位地图.md",
    "scripts/render_report.py",
    "scripts/validate_report.py",
)

SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "credential assignment": re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\b"
        r"\s*[:=]\s*[\"'][A-Za-z0-9_./+=-]{12,}[\"']"
    ),
    "mainland phone number": re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"),
    "mainland ID number": re.compile(r"(?<!\d)\d{17}[0-9Xx](?!\d)"),
}


def run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def source_state() -> tuple[str, str, bool]:
    try:
        commit = run_git("rev-parse", "HEAD")
        commit_date = run_git("show", "-s", "--format=%cs", "HEAD").replace("-", "")
        dirty = bool(run_git("status", "--porcelain", "--untracked-files=all"))
    except (OSError, subprocess.CalledProcessError) as error:
        raise SystemExit("Release builds require a Git checkout") from error
    return commit, commit_date, dirty


def validate_source(source: Path = SOURCE) -> list[Path]:
    expected = {Path(relative) for relative in PUBLIC_FILES}
    actual: set[Path] = set()
    unsafe_nodes: list[str] = []

    for path in source.rglob("*"):
        relative = path.relative_to(source)
        if path.is_symlink():
            unsafe_nodes.append(f"symbolic link: {relative}")
        elif path.is_file():
            actual.add(relative)
        elif not path.is_dir():
            unsafe_nodes.append(f"unsupported filesystem node: {relative}")

    missing = sorted(expected - actual)
    unexpected = sorted(actual - expected)
    if missing or unexpected or unsafe_nodes:
        problems = []
        if missing:
            problems.append("missing: " + ", ".join(path.as_posix() for path in missing))
        if unexpected:
            problems.append(
                "not reviewed for public release: "
                + ", ".join(path.as_posix() for path in unexpected)
            )
        problems.extend(unsafe_nodes)
        raise SystemExit("Unsafe release source (" + "; ".join(problems) + ")")
    return [source / relative for relative in sorted(expected)]


def scan_public_files(paths: list[Path]) -> None:
    findings: list[str] = []
    for path in paths:
        if path.stat().st_size > MAX_FILE_BYTES:
            findings.append(f"{path.name}: exceeds 10 MB")
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(f"{path.name}: public files must be UTF-8 text")
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(content):
                findings.append(f"{path.relative_to(SOURCE)}: possible {label}")
    if findings:
        raise SystemExit("Sensitive or invalid public content: " + "; ".join(findings))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stable_zip_timestamp() -> tuple[int, int, int, int, int, int]:
    raw_epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if raw_epoch is None:
        return (1980, 1, 1, 0, 0, 0)
    try:
        epoch = max(int(raw_epoch), 315532800)
    except ValueError as error:
        raise SystemExit("SOURCE_DATE_EPOCH must be an integer") from error
    value = datetime.fromtimestamp(epoch, timezone.utc)
    return (value.year, value.month, value.day, value.hour, value.minute, value.second)


def write_deterministic_zip(source: Path, destination: Path) -> None:
    timestamp = stable_zip_timestamp()
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(item for item in source.rglob("*") if item.is_file()):
            relative = Path(PACKAGE_NAME) / path.relative_to(source)
            info = zipfile.ZipInfo(relative.as_posix(), date_time=timestamp)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def archive_previous_packages(release: Path, current_archive: Path) -> None:
    previous = [
        path
        for path in release.glob(f"{PACKAGE_NAME}-redskill-*.zip")
        if path != current_archive
    ]
    if not previous:
        return
    archive_dir = release / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    for path in previous:
        destination = archive_dir / path.name
        if destination.exists():
            destination.unlink()
        path.replace(destination)


def build_release(
    release: Path,
    version: str,
    commit: str,
    dirty: bool,
    archive_old: bool,
) -> tuple[Path, Path, int, int]:
    source_files = validate_source()
    scan_public_files(source_files)
    license_path = ROOT / "LICENSE"
    if not license_path.is_file() or license_path.is_symlink():
        raise SystemExit(f"Missing or unsafe license: {license_path}")

    release.mkdir(parents=True, exist_ok=True)
    temporary_root = Path(tempfile.mkdtemp(prefix=".career-planning-", dir=release))
    temporary_package = temporary_root / PACKAGE_NAME
    temporary_package.mkdir()
    try:
        for source_path in source_files:
            relative = source_path.relative_to(SOURCE)
            destination = temporary_package / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_path, destination)
            destination.chmod(0o644)
        shutil.copyfile(license_path, temporary_package / "LICENSE")
        (temporary_package / "LICENSE").chmod(0o644)

        packaged_files = sorted(path for path in temporary_package.rglob("*") if path.is_file())
        records = [
            {
                "path": path.relative_to(temporary_package).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in packaged_files
        ]
        manifest = {
            "format": 1,
            "package": PACKAGE_NAME,
            "version": version,
            "source_commit": commit,
            "source_dirty": dirty,
            "files": records,
        }
        manifest_path = temporary_package / "MANIFEST.json"
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        manifest_path.chmod(0o644)

        final_files = sorted(path for path in temporary_package.rglob("*") if path.is_file())
        oversized = [path for path in final_files if path.stat().st_size > MAX_FILE_BYTES]
        total_size = sum(path.stat().st_size for path in final_files)
        if oversized:
            raise SystemExit(
                "Files exceed RedSkill's 10 MB limit: "
                + ", ".join(path.name for path in oversized)
            )
        if total_size > MAX_TOTAL_BYTES:
            raise SystemExit("Skill exceeds RedSkill's 30 MB total limit")

        target = release / PACKAGE_NAME
        if target.exists():
            shutil.rmtree(target)
        temporary_package.replace(target)

        archive = release / f"{PACKAGE_NAME}-redskill-{version}.zip"
        temporary_archive = temporary_root / archive.name
        write_deterministic_zip(target, temporary_archive)
        os.replace(temporary_archive, archive)
        if archive_old:
            archive_previous_packages(release, archive)

        latest = {
            "archive": archive.name,
            "bytes": archive.stat().st_size,
            "sha256": sha256(archive),
            "source_commit": commit,
            "source_dirty": dirty,
            "version": version,
        }
        (release / "LATEST.json").write_text(
            json.dumps(latest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return target, archive, len(final_files), total_size
    finally:
        shutil.rmtree(temporary_root, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a deterministic, allowlisted RedSkill folder and zip archive."
    )
    parser.add_argument("--release-dir", type=Path, default=DEFAULT_RELEASE)
    parser.add_argument("--version", help="Archive version; defaults to the HEAD commit date")
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Allow a development build from uncommitted files; public releases must omit this flag",
    )
    parser.add_argument(
        "--keep-old",
        action="store_true",
        help="Keep older release zips beside the latest zip instead of moving them to release/archive/",
    )
    args = parser.parse_args()

    commit, commit_date, dirty = source_state()
    if dirty and not args.allow_dirty:
        raise SystemExit(
            "Working tree is not clean. Commit the reviewed files before a public build, "
            "or use --allow-dirty only for local verification."
        )
    version = args.version or os.environ.get("RELEASE_VERSION") or commit_date
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}", version):
        raise SystemExit("Version may contain only letters, digits, dots, underscores, and hyphens")

    target, archive, file_count, total_size = build_release(
        args.release_dir.resolve(),
        version,
        commit,
        dirty,
        archive_old=not args.keep_old,
    )
    print(f"Folder: {target}")
    print(f"Zip:    {archive}")
    print(f"SHA256: {sha256(archive)}")
    print(f"Files:  {file_count}")
    print(f"Size:   {total_size / 1024:.1f} KiB source, {archive.stat().st_size / 1024:.1f} KiB zip")
    if dirty:
        print("WARNING: development build from a dirty working tree; do not upload publicly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
