from __future__ import annotations

import importlib.util
import hashlib
import json
import re
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / ".claude" / "skills" / "career-planning"
EXAMPLE = ROOT / "examples" / "职业决策报告示例.html"
RENDERER_PATH = SKILL / "scripts" / "render_report.py"
BUILDER_PATH = ROOT / "scripts" / "build_release.py"

spec = importlib.util.spec_from_file_location("career_report_renderer", RENDERER_PATH)
renderer = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(renderer)

builder_spec = importlib.util.spec_from_file_location("career_release_builder", BUILDER_PATH)
builder = importlib.util.module_from_spec(builder_spec)
assert builder_spec and builder_spec.loader
builder_spec.loader.exec_module(builder)


def complete_fields() -> dict[str, str]:
    fields = {field: "待确认" for field in renderer.ALL_FIELDS}
    fields.update(
        {
            "NAME": "测试用户 <script>alert(1)</script>",
            "DATE": "2026-07-22",
            "TITLE": "职业方向验证",
            "SUMMARY": "基于真实经历形成的暂定判断。",
            "CONCLUSION": (
                '<p>先验证方向。</p><script>alert(1)</script>'
                '<img src="https://tracker.example/x">'
                '<svg viewBox="0 0 10 10"><g fill="url(https://tracker.example/pixel.svg#x)">'
                '<circle cx="5" cy="5" r="4"></circle></g></svg>'
            ),
            "EVIDENCE": '<div class="summary-grid"><p onclick="bad()">已有项目证据</p></div>',
            "ROLE_COMPARISON": "<table><tr><th>方向</th></tr><tr><td>内容策略</td></tr></table>",
            "INTEREST_NEXT_CHECKS": "<ul><li>完成一次访谈</li></ul>",
            "MOAT": '<div class="moat-layer">研究与表达</div>',
            "MASTER_LENS": "<p>框架来源待核实。</p>",
            "CAREER_PATH": '<ol><li>1 年</li><li>3 年</li><li>5 年</li></ol>',
            "ANTIFRAGILITY": "<p>A 主路径，B 备选，Z 安全底座。</p>",
            "ACTIONS": '<ol class="actions"><li class="roadmap-p1">14 天验证</li></ol>',
            "OPEN_QUESTIONS": "<ul><li>哪类任务愿意长期重复？</li></ul>",
            "USER_NOTES": "<p>暂无补充。</p>",
            "DECISION_HISTORY": "<p>2026-07-22 建档。</p>",
        }
    )
    return fields


class ReleaseTests(unittest.TestCase):
    def test_required_skill_files_exist(self) -> None:
        required = [
            SKILL / "SKILL.md",
            SKILL / "references" / "行业与岗位地图.md",
            SKILL / "references" / "决策协议与质量门槛.md",
            SKILL / "assets" / "报告模板.html",
            SKILL / "assets" / "报告数据示例.json",
            RENDERER_PATH,
            SKILL / "scripts" / "validate_report.py",
        ]
        self.assertEqual([], [str(path) for path in required if not path.is_file()])

    def test_cursor_adapter_reference_resolves(self) -> None:
        adapter = (ROOT / "adapters" / "cursor" / "career-planning.mdc").read_text(encoding="utf-8")
        for relative in re.findall(r"`(\.claude/skills/career-planning/[^`]+)`", adapter):
            self.assertTrue((ROOT / relative).exists(), relative)

    def test_example_is_complete_and_safe(self) -> None:
        document = EXAMPLE.read_text(encoding="utf-8")
        self.assertEqual([], renderer.validate_report(document))
        self.assertNotRegex(document, r"\{\{[A-Z0-9_]+\}\}")
        self.assertNotRegex(document, r"--w\s*:\s*\d+(?:\.\d+)?%")
        self.assertIn("1 YEAR", document)
        self.assertIn("3 YEARS", document)
        self.assertIn("5 YEARS", document)
        self.assertIn("15–30 天", document)
        self.assertIn("31–90 天", document)

    def test_renderer_escapes_text_and_sanitizes_fragments(self) -> None:
        template = (SKILL / "assets" / "报告模板.html").read_text(encoding="utf-8")
        document = renderer.render(template, complete_fields())
        self.assertEqual([], renderer.validate_report(document))
        self.assertIn("测试用户 &lt;script&gt;alert(1)&lt;/script&gt;", document)
        self.assertNotIn("<script", document.lower())
        self.assertNotIn("onclick=", document.lower())
        self.assertNotIn("tracker.example", document)

    def test_svg_attributes_use_semantic_allowlists(self) -> None:
        safe = renderer.sanitize_fragment(
            '<svg viewBox="0 0 10 10" width="10" height="10">'
            '<g transform="translate(1 2)" fill="#245947">'
            '<path d="M0 0 L5 5 Z" stroke="currentColor"></path></g></svg>'
        )
        self.assertIn('fill="#245947"', safe)
        self.assertIn('transform="translate(1 2)"', safe)
        self.assertNotIn("url(", safe)

        unsafe = (
            '<svg viewBox="0 0 10 10"><g fill="url(https://tracker.example/x)">'
            '<circle cx="5" cy="5" r="4"></circle></g></svg>'
        )
        self.assertNotIn("tracker.example", renderer.sanitize_fragment(unsafe))
        self.assertIn("Disallowed external resource", renderer.validate_report(unsafe))

    def test_renderer_cli_writes_valid_report(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            data_path = temp / "data.json"
            output_path = temp / "report.html"
            data_path.write_text(json.dumps(complete_fields(), ensure_ascii=False), encoding="utf-8")
            subprocess.run(
                ["python3", str(RENDERER_PATH), "--data", str(data_path), "--output", str(output_path)],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual([], renderer.validate_report(output_path.read_text(encoding="utf-8")))

    def test_bundled_sample_data_renders(self) -> None:
        fields = renderer.load_data(SKILL / "assets" / "报告数据示例.json")
        template = (SKILL / "assets" / "报告模板.html").read_text(encoding="utf-8")
        document = renderer.render(template, fields)
        self.assertEqual([], renderer.validate_report(document))

    def test_report_template_has_one_responsive_design_system(self) -> None:
        template = (SKILL / "assets" / "报告模板.html").read_text(encoding="utf-8")
        self.assertEqual(1, len(re.findall(r"<style\b", template, re.IGNORECASE)))
        self.assertIn('font-family: "Career Futura"', template)
        self.assertRegex(template, r'--cn:\s*"PingFang SC"')
        self.assertIn('"Microsoft YaHei"', template)
        self.assertIn("overflow-wrap: anywhere", template)
        title_rule = re.search(r"\.report-header h1\s*\{(?P<body>.*?)\}", template, re.DOTALL)
        self.assertIsNotNone(title_rule)
        self.assertIn("overflow-wrap: anywhere", title_rule.group("body"))
        self.assertIn("word-break: break-word", title_rule.group("body"))
        mobile_title_rules = re.findall(
            r"\.report-header h1\s*\{(?P<body>.*?)\}", template, re.DOTALL
        )
        self.assertGreaterEqual(len(mobile_title_rules), 2)
        mobile_title_rule = mobile_title_rules[-1]
        for phrase in [
            "width: 100%",
            "max-width: 100%",
            "min-width: 0",
            "font-size: clamp(31px, 9vw, 39px)",
            "white-space: normal",
            "word-break: break-all",
        ]:
            self.assertIn(phrase, mobile_title_rule)
        self.assertIn("white-space: pre-line", template)
        self.assertIn("@media (max-width: 680px)", template)
        self.assertIn("@media (prefers-reduced-motion: reduce)", template)
        self.assertIn("@media print", template)
        self.assertIn("Content-Security-Policy", template)
        self.assertIn("connect-src 'none'", template)
        self.assertNotIn("LIVING EDITION", template)
        self.assertNotIn("writing-mode: vertical", template)
        self.assertIn('class="depth-block ecosystem-panel"', template)
        self.assertIn('class="depth-block ability-panel"', template)

    def test_sample_data_demonstrates_long_text_wrapping(self) -> None:
        fields = renderer.load_data(SKILL / "assets" / "报告数据示例.json")
        point_fields = ["LEADING_SIGNALS", "INTEREST_TASKS", "ABILITY_EVIDENCE", "ROLE_MATCH"]
        self.assertTrue(any("\n•" in fields[field] for field in point_fields))

    def test_method_requires_ecosystem_and_ability_depth(self) -> None:
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        roles = (SKILL / "references" / "行业与岗位地图.md").read_text(encoding="utf-8")
        abilities = (SKILL / "references" / "能力点挖掘.md").read_text(encoding="utf-8")
        quality = (SKILL / "references" / "决策协议与质量门槛.md").read_text(encoding="utf-8")
        for phrase in ["上游输入", "核心判断", "负责结果", "能力账户", "岗位重要性"]:
            self.assertIn(phrase, skill + roles + abilities)
        for phrase in ["行业价值链", "当前组织", "个人长期发展", "缺位后果", "未来 3 年变化"]:
            self.assertIn(phrase, skill + roles + quality)
        for phrase in ["AI 应用产品", "模型评测、质量与安全", "下一份证据", "准入能力", "可复用系统", "放大杠杆"]:
            self.assertIn(phrase, roles + abilities)

    def test_trigger_description_has_positive_and_negative_scope(self) -> None:
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        frontmatter = skill.split("---", 2)[1]
        for signal in ["职业", "事业发展", "擅长能力", "离职", "入职", "长期道路"]:
            self.assertIn(signal, frontmatter)
        for exclusion in ["周报", "润色文案", "技术任务", "通用管理知识"]:
            self.assertIn(exclusion, frontmatter)

    def test_public_readme_excludes_maintainer_notes(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        maintainer_only = [
            "发布前检查",
            "build_release.py",
            "source_dirty",
            "host-validation",
            "公开发布前的独立测试",
            "不会要求用户提交邮箱",
        ]
        for phrase in maintainer_only:
            self.assertNotIn(phrase, readme)
        self.assertIn("请开启一个新会话", readme)

    def test_packaged_references_exclude_release_process_notes(self) -> None:
        quality = (SKILL / "references" / "决策协议与质量门槛.md").read_text(encoding="utf-8")
        self.assertNotIn("公开发布前的独立测试", quality)
        self.assertNotIn("大改 Skill 后", quality)

    def test_long_references_have_a_table_of_contents(self) -> None:
        for path in sorted((SKILL / "references").glob("*.md")):
            document = path.read_text(encoding="utf-8")
            if len(document.splitlines()) > 100:
                self.assertIn("## 目录", "\n".join(document.splitlines()[:30]), path.name)

    def test_cross_host_records_are_explicitly_optional(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "release-check.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("Validate optional cross-host result schema", workflow)
        self.assertNotIn("--require-all", workflow)

    def test_public_install_docs_cover_shared_multi_host_install(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for phrase in [
            "npx skills add",
            "https://github.com/yutongcai0628/career-planning-skill",
            "--skill career-planning",
            "-a claude-code -a codex -a cursor -a kimi-code-cli",
            "~/.claude/skills/career-planning/",
            "~/.codex/skills/career-planning/",
            "~/.cursor/skills/career-planning/",
            "~/.kimi-code/skills/career-planning/",
        ]:
            self.assertIn(phrase, readme)

    def test_github_actions_are_pinned_to_full_commit_shas(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "release-check.yml").read_text(
            encoding="utf-8"
        )
        uses = re.findall(r"^\s*-\s+uses:\s+([^\s#]+)", workflow, re.MULTILINE)
        self.assertTrue(uses)
        for action in uses:
            self.assertRegex(action, r"^[^@]+@[0-9a-f]{40}$")

    def test_state_updates_preserve_notes_and_append_history(self) -> None:
        original = complete_fields()
        original["USER_NOTES"] = "<p>用户原文：不要删除。</p>"
        original["DECISION_HISTORY"] = "<p>第一次建档。</p>"
        merged = renderer.merge_update(
            original,
            {"CURRENT_RECOMMENDATION": "更新后的建议"},
            {"DECISION_HISTORY": "<p>完成一次访谈。</p>"},
        )
        self.assertEqual("<p>用户原文：不要删除。</p>", merged["USER_NOTES"])
        self.assertEqual("更新后的建议", merged["CURRENT_RECOMMENDATION"])
        self.assertIn("第一次建档", merged["DECISION_HISTORY"])
        self.assertTrue(merged["DECISION_HISTORY"].endswith("<p>完成一次访谈。</p>"))
        with self.assertRaises(ValueError):
            renderer.merge_update(original, {"USER_NOTES": "<p>覆盖</p>"}, {})

    def test_renderer_cli_merges_partial_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            full = temp / "full.json"
            patch = temp / "patch.json"
            state = temp / "career.state.json"
            output = temp / "career.html"
            full.write_text(json.dumps(complete_fields(), ensure_ascii=False), encoding="utf-8")
            subprocess.run(
                [
                    "python3",
                    str(RENDERER_PATH),
                    "--data",
                    str(full),
                    "--state",
                    str(state),
                    "--output",
                    str(output),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            patch.write_text(
                json.dumps(
                    {
                        "fields": {"CURRENT_RECOMMENDATION": "保留旧字段，只更新这一项。"},
                        "append": {"DECISION_HISTORY": "<p>追加记录。</p>"},
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            subprocess.run(
                [
                    "python3",
                    str(RENDERER_PATH),
                    "--data",
                    str(patch),
                    "--state",
                    str(state),
                    "--output",
                    str(output),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            state_fields = json.loads(state.read_text(encoding="utf-8"))["fields"]
            self.assertEqual("保留旧字段，只更新这一项。", state_fields["CURRENT_RECOMMENDATION"])
            self.assertIn("追加记录", state_fields["DECISION_HISTORY"])
            self.assertEqual("测试用户 <script>alert(1)</script>", state_fields["NAME"])
            self.assertEqual([], renderer.validate_report(output.read_text(encoding="utf-8")))

    def test_release_source_is_exactly_allowlisted(self) -> None:
        public_files = builder.validate_source()
        builder.scan_public_files(public_files)
        self.assertEqual(set(builder.PUBLIC_FILES), {str(path.relative_to(SKILL)) for path in public_files})

        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            for relative in builder.PUBLIC_FILES:
                path = source / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("placeholder", encoding="utf-8")
            private_report = source / "职业档案" / "真实用户.html"
            private_report.parent.mkdir()
            private_report.write_text("private", encoding="utf-8")
            with self.assertRaises(SystemExit):
                builder.validate_source(source)

    def test_release_zip_is_reproducible_and_has_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            release = Path(directory)
            _, archive, _, _ = builder.build_release(
                release,
                version="test",
                commit="0123456789abcdef",
                dirty=True,
                archive_old=False,
            )
            first_hash = hashlib.sha256(archive.read_bytes()).hexdigest()
            _, archive, _, _ = builder.build_release(
                release,
                version="test",
                commit="0123456789abcdef",
                dirty=True,
                archive_old=False,
            )
            second_hash = hashlib.sha256(archive.read_bytes()).hexdigest()
            self.assertEqual(first_hash, second_hash)
            with zipfile.ZipFile(archive) as package:
                names = package.namelist()
                self.assertIn("career-planning/SKILL.md", names)
                self.assertIn("career-planning/LICENSE", names)
                self.assertIn("career-planning/MANIFEST.json", names)
                manifest = json.loads(package.read("career-planning/MANIFEST.json"))
                self.assertEqual("0123456789abcdef", manifest["source_commit"])
                self.assertTrue(manifest["source_dirty"])

    def test_master_lens_preserves_verified_web_search(self) -> None:
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        lens = (SKILL / "references" / "标杆与思维透镜.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        adapter = (ROOT / "adapters" / "cursor" / "career-planning.mdc").read_text(
            encoding="utf-8"
        )
        combined = "\n".join([skill, lens, readme, adapter])
        for phrase in [
            "Web Search",
            "一手材料",
            "访问日期",
            "本次未完成联网核验",
            "去身份化",
            "完整简历",
            "私人职业档案",
            "未公开雇主",
        ]:
            self.assertIn(phrase, combined)
        self.assertIn("报告保持离线", skill)
        self.assertNotIn("全网搜索", combined)

    def test_full_plan_auto_generates_html_and_feishu_choice_is_gated(self) -> None:
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        archive = (SKILL / "references" / "持续档案.md").read_text(encoding="utf-8")
        interaction = (SKILL / "references" / "交互与可视化.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        adapter = (ROOT / "adapters" / "cursor" / "career-planning.mdc").read_text(encoding="utf-8")
        combined = "\n".join([skill, archive, interaction, readme, adapter])
        for phrase in [
            "文档能力可调用且授权有效",
            "A 本地 HTML B 飞书文档",
            "默认生成本地 HTML",
            "信息不足时先问 1–3",
            "回答后自动生成",
            "飞书不可用时不询问格式",
            "用户明确拒绝保存",
            "不要未经同意自动改换存储位置",
            "用户明确要求“两种都要”",
        ]:
            self.assertIn(phrase, combined)
        self.assertNotIn("A 本地 HTML B 飞书文档 C 只做本次", combined)
        self.assertNotIn("A 本地 HTML B 只做本次", combined)
        self.assertNotIn("HTML + 飞书同步", combined)

    def test_blind_eval_suite_has_trigger_and_non_trigger_cases(self) -> None:
        suite = json.loads((ROOT / "tests" / "blind-eval-cases.json").read_text(encoding="utf-8"))
        cases = suite["cases"]
        self.assertGreaterEqual(len(cases), 10)
        self.assertTrue(any(case["should_trigger"] for case in cases))
        self.assertTrue(any(not case["should_trigger"] for case in cases))
        self.assertEqual(len(cases), len({case["id"] for case in cases}))
        depth_checks = " ".join(
            check
            for case in cases
            if case["id"].startswith("depth-")
            for check in case["checks"]
        )
        for phrase in ["行业价值", "关键判断", "护城河层级", "3–5 年"]:
            self.assertIn(phrase, depth_checks)

    def test_banned_style_phrases_are_absent(self) -> None:
        files = [SKILL / "SKILL.md", *sorted((SKILL / "references").glob("*.md"))]
        combined = "\n".join(path.read_text(encoding="utf-8") for path in files)
        banned = [
            r"不是.{0,60}而是",
            r"稳稳地接住你",
            r"最来劲",
            r"上瘾",
            r"螺丝钉",
            r"骑驴找马",
            r"填坑救火",
            r"和稀泥",
            r"know-how",
        ]
        for pattern in banned:
            self.assertIsNone(re.search(pattern, combined), pattern)


if __name__ == "__main__":
    unittest.main()
