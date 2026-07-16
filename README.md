# 职业规划导师 · Career Planning Skill

> 一个能**长期陪你**的 AI 职业规划导师。从兴趣出发挖掘你最擅长的事，用选择题和图表帮你想清楚，并把每次对话沉淀成一份越用越准、可不断迭代的职业档案——而不是聊完就忘的一次性对话。

这是一个跨 Agent 的 **SKILL.md 职业规划 skill**。它优先兼容 [Claude Code](https://claude.com/claude-code) 和 Codex，也可以给 Kimi、Cursor Agent、通用本地 Agent 当作系统化工作流使用。装上之后，你只要像聊天一样说"帮我做职业规划""这个 offer 适不适合我""我不知道自己适合做什么"，它就会自动化身一位职业规划导师，带你一步步走。

---

## 为什么不是"随便找 AI 聊两句"

普通对话聊完就散了，信息留不下来，每次都得从头说。这个 skill 的不同，在五件事上：

| 能力 | 它做了什么 |
|---|---|
| 🌱 **从兴趣出发** | 不直接问"你喜欢什么"（多数人答不上来），而是从行为线索挖出你的真实兴趣，再顺着兴趣找到能力点。兴趣是种子，擅长是长出来的。 |
| 🧩 **选择题挖掘** | 用选择题代替"写小作文"；有表单工具就点选，没有就回复编号——选 < 写，认得出 < 想得起。 |
| 📊 **图表可视化** | 兴趣×能力×价值三圈图、能力雷达图、职业路径图、JD 匹配度图……支持 widget / Mermaid / SVG / Markdown 表格降级。 |
| 🗂️ **职业笔记系统 · 可迭代** | 为你维护一份会持续生长的职业档案，每次回来先读档、接着上次聊，跑"假设→小实验→看反馈→更新"的循环。越用越懂你。可存本地，也可**同步到飞书**随时翻看、自己编辑。 |
| 🧠 **导师天团** | 内置 16 位知名企业家/CEO 的思维框架（马斯克、乔布斯、黄仁勋、奥特曼、海莉·比伯、Cursor、多邻国和 Canva 创始人……）当决策工具——借脑子，不照抄。 |

外加一份**可导出的正式报告**（HTML / PDF / 飞书文档 / Markdown），把规划变成能保存、能分享的东西。

---

## 它能帮哪些人

- **刚入职场 / 迷茫**：从兴趣出发挖掘能力点，找到值得走的方向。
- **想越走越高**：怎么打造"人无我有"的核心竞争力？感觉到顶了怎么突破天花板？怎么实现个人价值？
- **手里有机会要抉择**：两个 offer 怎么选？大厂还是创业？这个岗位适不适合我？该不该入职？该不该离职？
- **怕被裁 / 组织变化 / 行业下行**：怎么让自己反脆弱、越老越值钱？怎么找到一份能长期甚至终身做的事？

---

## 什么时候会触发

你不一定要说"使用这个 skill"。只要问题涉及职业方向、岗位选择、公司选择、入职/离职/跳槽、职业安全感，它都应该进入职业规划导师模式。

典型触发句：

```text
帮我做职业规划
我不知道自己适合做什么
我该不该离职
我要不要入职这家公司
这个 offer 要不要接
这个岗位适合我吗
我该不该转行
我怕被裁，怎么提高安全感
怎么才能变得不可替代
```

---

## 数据、格式与飞书

- **真实数据优先**：你可以直接给它 JD、简历、薪资、offer 条款、公司信息、行业判断、面试反馈。它会基于你提供的数据分析，并标注哪些是"用户提供信息"。
- **不编造实时数据**：涉及名人、公司、融资、估值、裁员、政策、股价、行业规模等会变化的信息，能联网就查公开来源；不能核实时必须说明"无法现场核实"，不能硬编数字。
- **格式自动输出**：你说 HTML 就生成 HTML；说 Markdown 就给 Markdown；说 PDF 就先生成 HTML 再转/打印；说飞书/Lark 就优先创建飞书文档。
- **飞书深度集成**：如果当前 Agent 有飞书能力或本地装了 `lark-cli`，可以把报告写到飞书文档；如果有 `lark-whiteboard`，关键图会优先做成飞书画板。

---

## 安装

你可以按自己使用的平台安装：

### Claude Code

**A. 只在某个项目里用** —— 把 `career-planning` 文件夹放到项目的 `.claude/skills/` 下：
```
你的项目/.claude/skills/career-planning/
```

**B. 在任何地方都能用（推荐）** —— 复制到全局 skills 目录：
```bash
cp -r .claude/skills/career-planning ~/.claude/skills/
```

> `.claude` 是隐藏文件夹。Mac 访达里按 `Command + Shift + .` 可显示隐藏文件。

### Codex

复制到 Codex 的 skills 目录：

```bash
mkdir -p ~/.codex/skills
cp -r .claude/skills/career-planning ~/.codex/skills/
```

然后在 Codex 里说：`用 $career-planning 帮我做职业规划`，或直接描述你的职业问题。

### Kimi / Cursor Agent / 通用 Agent

如果平台支持上传/引用 skill、知识库或规则文件，把 `.claude/skills/career-planning/` 整个文件夹作为一个 skill 导入；如果不支持文件型 skill，就把 `SKILL.md` 作为主规则，并保持 `references/` 和 `assets/` 的相对路径可访问。

这个 skill 不强依赖某个专用工具：没有选择题工具就用聊天编号，没有图表工具就用 Mermaid/SVG/Markdown 表格，没有飞书或 PDF 能力就退回 HTML/Markdown。

### Redskill / GitHub 发布

Redskill 如果要求上传 skill 目录，请选择 `.claude/skills/career-planning/`，不要上传整个本地项目目录。GitHub 可以发布整个仓库，但发布前建议确认 `git status --ignored --short` 里只有 ignored 的个人档案、系统文件和本地设置。

如果你已经安装 GitHub CLI，可以这样发布到 GitHub：

```bash
gh auth login
git status --short --ignored
git add README.md LICENSE .gitignore .claude/skills/career-planning
git commit -m "Publish career planning skill"
gh repo create career-planning-skill --public --source=. --remote=origin --push
```

如果 GitHub 上已经建好了仓库，就改用：

```bash
git remote add origin https://github.com/<你的用户名>/<仓库名>.git
git push -u origin main
```

发布前确认不要提交 `职业档案/`、`.claude/settings.local.json`、`.DS_Store`、本地 zip/tar 包或任何用户真实简历/JD。

---

## 怎么用

像找一位顾问那样跟它说话就行。试试这些：

```
帮我做一下职业规划
我不知道自己适合做什么，能帮我挖挖吗
我纠结去大厂还是创业公司
怎么才能让自己变得不可替代
（贴一段 JD）这个岗位适合我吗
我纠结要不要裸辞做内容创业，用第一性原理帮我想想
帮我把这次的规划导出成一份报告
```

它会按需问选择题、画图、给出带判断和行动清单的规划；如果当前环境能读写文件，并且你同意保存，它会把关键进展记进你的职业档案。下次再来，它会接着上次往下聊。

---

## 隐私

你的个人职业档案默认存在项目下的 `职业档案/` 文件夹里，**已被 `.gitignore` 忽略**——你 fork、clone、push 这个仓库都不会泄露任何个人数据。第一次建档或同步飞书前，skill 会先征求你的同意。Skill 本体不含任何人的信息，每个人装上后各自生成自己的档案。

发布到 Redskill / GitHub 时，请只发布被 Git 跟踪的 skill 文件，不要手动把整个本地目录打包上传；本地可能包含 `职业档案/`、`.claude/settings.local.json`、`.DS_Store` 这类隐私或系统文件。需要压缩包时，建议先从 Git 生成干净发布包，而不是直接右键压缩当前文件夹。

---

## 发布前检查清单

- `SKILL.md` 的 `description` 覆盖"职业规划 / 入职 / 离职 / offer / JD / 转行 / 被裁 / 行业下行"等触发词。
- 没有专用工具时，选择题、图表、文件保存、飞书、PDF 都能降级。
- HTML 模板不依赖外部图片或脚本，用户输入会先转义。
- 涉及实时信息时不编造；无法核实时明确说明。
- 每份完整规划和导出报告都有免责声明。
- `git status --ignored --short` 里没有要被误提交的隐私文件。
- 压缩包或 GitHub 仓库根目录能让人直接找到 `.claude/skills/career-planning/SKILL.md`。

---

## 目录结构

```
.
├── README.md                       ← 你正在看的这个
├── .gitignore                      ← 忽略个人档案，保护隐私
└── .claude/skills/career-planning/
    ├── SKILL.md                    ← 主文件：人格、流程、报告模板
    ├── README.md                   ← 给二次开发者的编辑地图
    ├── agents/openai.yaml           ← Codex/OpenAI 侧展示元数据
    ├── assets/
    │   ├── 报告模板.html             ← 导出用的精美报告模板（纯 HTML/CSS/SVG 图表）
    │   └── 报告设计哲学.md           ← 「晨刊」视觉宪法（填报告前必读）
    └── references/
        ├── 持续档案.md              ← 跨对话记忆 + 迭代循环
        ├── 能力点挖掘.md            ← 从兴趣到能力（场景①）
        ├── 中期规划.md             ← 核心竞争力 / 突破天花板 / 个人价值（场景②）
        ├── 岗位分析.md             ← 单 JD 适配 + 多 offer 抉择（场景③）
        ├── 职业反脆弱.md            ← 组织变化 / 裁员 / 行业下行 / 终身事业（场景④）
        ├── 交互与可视化.md          ← 选择题题库 + 图表模板
        ├── 标杆与思维透镜.md        ← 16 位知名导师的决策框架
        └── 导出报告.md             ← HTML/PDF/飞书/Markdown 导出
```

想二次开发、改内容，看 [`.claude/skills/career-planning/README.md`](.claude/skills/career-planning/README.md) 那份编辑地图。

---

## 一点说明（免责声明）

这个 skill 提供的是思考工具和结构，不是标准答案。所有名人框架都是**决策透镜，不是成功公式**——他们都是幸存者，路径有大量运气和时代红利。

**本工具产出的全部分析与建议仅供参考，不构成职业、法律、投资等任何方面的直接指导；使用者据此做出的任何决定及其后果由本人承担。最终决定权，始终在你自己手上。**

---

## License

MIT（可自行调整）。欢迎 fork、改造、分享。
