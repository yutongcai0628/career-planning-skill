#!/usr/bin/env python3
"""Render a career report from JSON without allowing executable HTML."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import tempfile
from html.parser import HTMLParser
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TEMPLATE = SKILL_ROOT / "assets" / "报告模板.html"

TEXT_FIELDS = {
    "NAME",
    "DATE",
    "TITLE",
    "SUMMARY",
    "INTEREST_STATUS",
    "MOAT_STATUS",
    "NEXT_PRIORITY",
    "DECISION_TYPE",
    "DECISION_QUESTION",
    "CURRENT_RECOMMENDATION",
    "DECISIVE_QUESTION",
    "REVERSAL_CONDITION",
    "LEADING_SIGNALS",
    "REVIEW_DATE",
    "EVIDENCE_STATUS",
    "INTEREST_EXPERIENCE",
    "INTEREST_TASKS",
    "ABILITY_EVIDENCE",
    "ROLE_MATCH",
    "INTEREST_NEXT_STEP",
    "INTEREST_DIRECTION",
    "INTEREST_REASON",
}

RICH_FIELDS = {
    "CONCLUSION",
    "EVIDENCE",
    "ROLE_COMPARISON",
    "ECOSYSTEM_POSITION",
    "ABILITY_REFINEMENT",
    "INTEREST_NEXT_CHECKS",
    "MOAT",
    "MASTER_LENS",
    "CAREER_PATH",
    "ANTIFRAGILITY",
    "ACTIONS",
    "OPEN_QUESTIONS",
    "USER_NOTES",
    "DECISION_HISTORY",
}

ALL_FIELDS = TEXT_FIELDS | RICH_FIELDS
APPEND_ONLY_FIELDS = {"USER_NOTES", "DECISION_HISTORY"}
REQUIRED_SECTION_IDS = (
    "conclusion",
    "evidence",
    "interest-map",
    "moat",
    "master-lens",
    "career-path",
    "antifragility",
    "actions",
    "open-questions",
    "user-notes",
    "decision-history",
)

ALLOWED_TAGS = {
    "p",
    "div",
    "span",
    "strong",
    "b",
    "em",
    "i",
    "small",
    "ul",
    "ol",
    "li",
    "table",
    "thead",
    "tbody",
    "tr",
    "th",
    "td",
    "h3",
    "h4",
    "time",
    "blockquote",
    "dl",
    "dt",
    "dd",
    "br",
    "svg",
    "g",
    "circle",
    "line",
    "polyline",
    "polygon",
    "path",
    "text",
}
VOID_TAGS = {"br"}
BLOCKED_TAGS = {"script", "style", "iframe", "object", "embed", "link", "meta"}
GLOBAL_ATTRS = {"class", "role", "aria-label", "data-step", "data-layer"}
TAG_ATTRS = {
    "th": {"colspan", "rowspan", "scope"},
    "td": {"colspan", "rowspan"},
    "time": {"datetime"},
    "svg": {"viewbox", "width", "height", "aria-hidden", "preserveaspectratio"},
    "g": {"transform", "fill", "stroke"},
    "circle": {"cx", "cy", "r", "fill", "stroke", "stroke-width"},
    "line": {"x1", "y1", "x2", "y2", "stroke", "stroke-width", "stroke-linecap"},
    "polyline": {"points", "fill", "stroke", "stroke-width", "stroke-linecap", "stroke-linejoin"},
    "polygon": {"points", "fill", "stroke", "stroke-width"},
    "path": {"d", "fill", "stroke", "stroke-width", "stroke-linecap", "stroke-linejoin"},
    "text": {"x", "y", "dx", "dy", "fill", "text-anchor", "transform"},
}
CLASS_RE = re.compile(r"^[A-Za-z0-9_-]+(?:\s+[A-Za-z0-9_-]+)*$")
PLACEHOLDER_RE = re.compile(r"\{\{([A-Z0-9_]+)\}\}")
UNSAFE_ATTRIBUTE_VALUE_RE = re.compile(
    r"(?:url\s*\(|(?:https?|file|ftp|javascript|vbscript|data)\s*:|^\s*//)",
    re.IGNORECASE,
)
NUMBER_RE = re.compile(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?")
NUMBER_LIST_RE = re.compile(
    rf"^\s*{NUMBER_RE.pattern}(?:[\s,]+{NUMBER_RE.pattern})*\s*$"
)
COLOR_RE = re.compile(
    r"^(?:none|transparent|currentColor|#[0-9A-Fa-f]{3,8}|"
    r"(?:rgb|rgba|hsl|hsla)\(\s*[-+0-9.%\s,]+\))$"
)
PATH_RE = re.compile(r"^[MmZzLlHhVvCcSsQqTtAa0-9eE+\-.,\s]+$")
TRANSFORM_RE = re.compile(
    r"^(?:(?:matrix|translate|scale|rotate|skewX|skewY)"
    r"\(\s*[-+0-9eE.,\s]+\)\s*)+$"
)
TOKEN_RE = re.compile(r"^[A-Za-z0-9_-]{1,64}$")
DATETIME_RE = re.compile(r"^[0-9T:+\-.\sZ]{1,64}$")


def attribute_is_safe(tag: str, name: str, value: str) -> bool:
    """Validate allowed attributes by meaning, not only by name."""
    decoded = html.unescape(value).strip()
    if not decoded or len(decoded) > 500 or UNSAFE_ATTRIBUTE_VALUE_RE.search(decoded):
        return False
    if any(character in decoded for character in ("\x00", "\r", "\n")):
        return False

    if name == "class":
        return bool(CLASS_RE.fullmatch(decoded))
    if name in {"role", "data-step", "data-layer"}:
        return bool(TOKEN_RE.fullmatch(decoded))
    if name == "aria-label":
        return len(decoded) <= 200
    if name == "aria-hidden":
        return decoded in {"true", "false"}
    if name in {"colspan", "rowspan", "width", "height"}:
        return bool(re.fullmatch(r"\d{1,4}", decoded))
    if name == "scope":
        return decoded in {"row", "col", "rowgroup", "colgroup"}
    if name == "datetime":
        return bool(DATETIME_RE.fullmatch(decoded))
    if name == "viewbox":
        return len(NUMBER_RE.findall(decoded)) == 4 and bool(NUMBER_LIST_RE.fullmatch(decoded))
    if name == "preserveaspectratio":
        return bool(re.fullmatch(r"(?:none|x(?:Min|Mid|Max)Y(?:Min|Mid|Max))(?:\s+(?:meet|slice))?", decoded))
    if name in {"fill", "stroke"}:
        return bool(COLOR_RE.fullmatch(decoded))
    if name == "transform":
        return bool(TRANSFORM_RE.fullmatch(decoded))
    if name in {
        "cx",
        "cy",
        "r",
        "x",
        "y",
        "dx",
        "dy",
        "x1",
        "y1",
        "x2",
        "y2",
        "stroke-width",
    }:
        return bool(NUMBER_RE.fullmatch(decoded))
    if name == "points":
        return bool(NUMBER_LIST_RE.fullmatch(decoded))
    if name == "d":
        return bool(PATH_RE.fullmatch(decoded))
    if name == "stroke-linecap":
        return decoded in {"butt", "round", "square"}
    if name == "stroke-linejoin":
        return decoded in {"arcs", "bevel", "miter", "miter-clip", "round"}
    if name == "text-anchor":
        return decoded in {"start", "middle", "end"}
    return False


class FragmentSanitizer(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.output: list[str] = []
        self.open_tags: list[str] = []
        self.blocked_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if self.blocked_depth:
            if tag in BLOCKED_TAGS:
                self.blocked_depth += 1
            return
        if tag in BLOCKED_TAGS:
            self.blocked_depth = 1
            return
        if tag not in ALLOWED_TAGS:
            return

        safe_attrs: list[str] = []
        allowed_attrs = GLOBAL_ATTRS | TAG_ATTRS.get(tag, set())
        for raw_name, raw_value in attrs:
            name = raw_name.lower()
            if name not in allowed_attrs or raw_value is None:
                continue
            value = raw_value.strip()
            if not attribute_is_safe(tag, name, value):
                continue
            safe_attrs.append(f' {name}="{html.escape(value, quote=True)}"')

        self.output.append(f"<{tag}{''.join(safe_attrs)}>")
        if tag not in VOID_TAGS:
            self.open_tags.append(tag)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        was_blocked = self.blocked_depth
        self.handle_starttag(tag, attrs)
        tag = tag.lower()
        if tag in BLOCKED_TAGS and self.blocked_depth > was_blocked:
            self.blocked_depth -= 1
            return
        if tag not in VOID_TAGS and self.open_tags and self.open_tags[-1] == tag:
            self.open_tags.pop()
            self.output.append(f"</{tag}>")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if self.blocked_depth:
            if tag in BLOCKED_TAGS:
                self.blocked_depth -= 1
            return
        if tag not in self.open_tags:
            return
        while self.open_tags:
            current = self.open_tags.pop()
            self.output.append(f"</{current}>")
            if current == tag:
                break

    def handle_data(self, data: str) -> None:
        if not self.blocked_depth:
            self.output.append(html.escape(data))

    def handle_entityref(self, name: str) -> None:
        if not self.blocked_depth:
            self.output.append(html.escape(html.unescape(f"&{name};")))

    def handle_charref(self, name: str) -> None:
        if not self.blocked_depth:
            self.output.append(html.escape(html.unescape(f"&#{name};")))

    def result(self) -> str:
        while self.open_tags:
            self.output.append(f"</{self.open_tags.pop()}>")
        return "".join(self.output)


def sanitize_fragment(fragment: str) -> str:
    parser = FragmentSanitizer()
    parser.feed(fragment)
    parser.close()
    return parser.result()


def validate_report(document: str) -> list[str]:
    errors: list[str] = []
    unresolved = sorted(set(PLACEHOLDER_RE.findall(document)))
    if unresolved:
        errors.append("Unresolved placeholders: " + ", ".join(unresolved))

    csp_meta_count = len(
        re.findall(
            r"<meta\b[^>]*http-equiv=[\"\']Content-Security-Policy[\"\'][^>]*>",
            document,
            re.IGNORECASE,
        )
    )
    if csp_meta_count != 1:
        errors.append(f"The report must contain exactly one Content-Security-Policy meta tag; found {csp_meta_count}")
    for directive in (
        "default-src 'none'",
        "img-src 'none'",
        "object-src 'none'",
        "frame-src 'none'",
        "connect-src 'none'",
        "base-uri 'none'",
        "form-action 'none'",
    ):
        if directive not in document:
            errors.append(f"Missing CSP directive: {directive}")

    for section_id in REQUIRED_SECTION_IDS:
        count = len(re.findall(rf'\bid=["\']{re.escape(section_id)}["\']', document, re.IGNORECASE))
        if count != 1:
            errors.append(f"Section id '{section_id}' must appear once; found {count}")

    if document.count('class="decision-ticket"') != 1:
        errors.append("The report must contain exactly one decision-ticket")
    if len(re.findall(r'class=["\'][^"\']*\binterest-step\b', document, re.IGNORECASE)) != 5:
        errors.append("The interest evidence chain must contain five steps")
    if document.count('class="depth-block ecosystem-panel"') != 1:
        errors.append("The report must contain exactly one ecosystem-position panel")
    if document.count('class="depth-block ability-panel"') != 1:
        errors.append("The report must contain exactly one ability-refinement panel")

    hazardous_patterns = {
        "script tag": r"<\s*script\b",
        "iframe tag": r"<\s*iframe\b",
        "object/embed tag": r"<\s*(?:object|embed)\b",
        "event handler": r"\son[a-z0-9_-]+\s*=",
        "javascript URL": r"javascript\s*:",
        "external resource": (
            r"\b[a-z_:][-a-z0-9_:.]*\s*=\s*[\"\'][^\"\']*"
            r"(?:url\s*\(|(?:https?|file|ftp|javascript|vbscript|data)\s*:|//)"
        ),
    }
    for label, pattern in hazardous_patterns.items():
        if re.search(pattern, document, re.IGNORECASE):
            errors.append(f"Disallowed {label}")
    return errors


def validate_field_values(payload: object, require_all: bool) -> dict[str, str]:
    if not isinstance(payload, dict):
        raise ValueError("JSON fields must be an object")

    fields = dict(payload)
    missing = sorted(ALL_FIELDS - fields.keys()) if require_all else []
    unknown = sorted(fields.keys() - ALL_FIELDS)
    if missing:
        raise ValueError("Missing fields: " + ", ".join(missing))
    if unknown:
        raise ValueError("Unknown fields: " + ", ".join(unknown))
    if any(not isinstance(value, str) for value in fields.values()):
        raise ValueError("Every field value must be a string")
    return fields


def load_data(path: Path) -> dict[str, str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict) and isinstance(payload.get("fields"), dict):
        payload = payload["fields"]
    return validate_field_values(payload, require_all=True)


def load_update(path: Path) -> tuple[dict[str, str], dict[str, str]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Update JSON must be an object")

    if "fields" in payload or "append" in payload:
        unknown_top_level = sorted(payload.keys() - {"fields", "append", "format"})
        if unknown_top_level:
            raise ValueError("Unknown update keys: " + ", ".join(unknown_top_level))
        fields = validate_field_values(payload.get("fields", {}), require_all=False)
        append = payload.get("append", {})
    else:
        fields = validate_field_values(payload, require_all=False)
        append = {}

    if not isinstance(append, dict):
        raise ValueError("'append' must be an object")
    unknown_append = sorted(append.keys() - APPEND_ONLY_FIELDS)
    if unknown_append:
        raise ValueError(
            "Only USER_NOTES and DECISION_HISTORY support append operations; found: "
            + ", ".join(unknown_append)
        )
    if any(not isinstance(value, str) for value in append.values()):
        raise ValueError("Every appended value must be a string")
    return fields, dict(append)


def merge_update(
    existing: dict[str, str],
    changes: dict[str, str],
    append: dict[str, str],
    allow_protected_replace: bool = False,
) -> dict[str, str]:
    protected_changes = sorted(APPEND_ONLY_FIELDS & changes.keys())
    if protected_changes and not allow_protected_replace:
        raise ValueError(
            "Protected fields must use the append operation unless "
            "--allow-protected-replace is explicit: "
            + ", ".join(protected_changes)
        )

    merged = dict(existing)
    merged.update(changes)
    for field, addition in append.items():
        if not addition:
            continue
        separator = "\n" if merged.get(field, "").strip() else ""
        merged[field] = merged.get(field, "") + separator + addition
    return validate_field_values(merged, require_all=True)


def render(template: str, fields: dict[str, str]) -> str:
    template_fields = set(PLACEHOLDER_RE.findall(template))
    if template_fields != ALL_FIELDS:
        missing = sorted(ALL_FIELDS - template_fields)
        extra = sorted(template_fields - ALL_FIELDS)
        details = []
        if missing:
            details.append("missing in template: " + ", ".join(missing))
        if extra:
            details.append("unknown in template: " + ", ".join(extra))
        raise ValueError("Template field mismatch (" + "; ".join(details) + ")")

    rendered = template
    for field in sorted(TEXT_FIELDS):
        rendered = rendered.replace("{{" + field + "}}", html.escape(fields[field], quote=True))
    for field in sorted(RICH_FIELDS):
        rendered = rendered.replace("{{" + field + "}}", sanitize_fragment(fields[field]))
    return rendered


def write_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(content)
        temporary_path = Path(handle.name)
    os.replace(temporary_path, path)


def serialize_state(fields: dict[str, str]) -> str:
    payload = {"format": 1, "fields": fields}
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a safe career-planning HTML report from JSON.")
    parser.add_argument(
        "--data",
        required=True,
        type=Path,
        help="UTF-8 JSON containing all fields, or a partial update when --state already exists",
    )
    parser.add_argument("--output", required=True, type=Path, help="Destination HTML path")
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE, help="Optional report template")
    parser.add_argument(
        "--state",
        type=Path,
        help="Private canonical JSON state. Existing state is merged with the partial --data update.",
    )
    parser.add_argument(
        "--allow-protected-replace",
        action="store_true",
        help="Allow an explicit replacement of USER_NOTES or DECISION_HISTORY instead of append-only update",
    )
    args = parser.parse_args()

    template_path = args.template.resolve()
    output_path = args.output.resolve()
    state_path = args.state.resolve() if args.state else None
    if output_path == template_path:
        parser.error("Output must not overwrite the template")
    if state_path and state_path in {template_path, output_path}:
        parser.error("State, output, and template must use different paths")

    try:
        if state_path and state_path.exists():
            existing = load_data(state_path)
            changes, append = load_update(args.data)
            fields = merge_update(
                existing,
                changes,
                append,
                allow_protected_replace=args.allow_protected_replace,
            )
        else:
            fields = load_data(args.data)
        document = render(template_path.read_text(encoding="utf-8"), fields)
        errors = validate_report(document)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))
    if errors:
        parser.error("; ".join(errors))

    write_atomic(output_path, document)
    if state_path:
        write_atomic(state_path, serialize_state(fields))
    print(output_path)
    if state_path:
        print(state_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
