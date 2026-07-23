# 职业规划导师

从真实经历中找出能力点，选择一条可以长期发展的职业道路。

这是一个面向 Claude Code、Codex、Kimi、Cursor Agent 及其他支持文件型规则的 Agent 的职业规划 Skill。用户谈到自己的职业选择、职场处境、事业发展或长期能力积累时，可以使用它。它尤其适合帮助暂时没有方向的人，理清自己擅长什么、愿意长期做什么，以及下一步该选择哪类岗位和行业。

它会从真实经历、做成的结果和他人反馈中提取能力证据，再检查这些能力能否在未来 3–5 年持续积累。最终交付包括主路径、相邻方向、主要风险和下一步行动。用户需要持续档案时，可以选择本地可视化 HTML；当前 Agent 已连接并授权飞书 CLI 时，也可以直接选择飞书文档。

## 你可以拿它解决什么

- 「我对工作和未来很迷茫，不知道自己擅长什么。」
- 「我的事业接下来应该怎么发展？」
- 「我想找到一条能够长期积累、越做越深的职业道路。」
- 「我现在的工作还可以，但看不清三年后的方向。」
- 「我现在遇到一个问题：领导让我转到另一个业务线，我该去吗？」
- 「我该不该离职？留下和离开的代价分别是什么？」
- 「我要不要入职这家公司？这份 offer 对我下一步有没有帮助？」
- 「这是 JD 和我的简历，这个岗位适合我吗？」
- 「我不知道自己适合做什么，怎么从已有经历里找到方向？」
- 「我工作三年了，下一步该积累什么能力？」
- 「公司在调整、行业在下行，我该怎样降低职业风险？」
- 「继续我的职业档案：我这周遇到了一个新问题。」

你不需要一次性交代完整背景。可以先说问题，也可以直接贴 JD、简历片段、offer 条款、薪资结构、面试反馈或你自己整理的数据。Skill 会补问那些会改变结论的问题。

## 它和普通聊天有什么不同

普通聊天可以给建议，但常常缺少决策过程。这套 Skill 对每次完整咨询有几项固定要求：

| 环节 | Skill 的做法 |
|---|---|
| 明确问题 | 先确认这次到底要决定什么，再给针对性的职业建议。 |
| 收集证据 | 把用户经历、现实约束、公开事实和推断分开；缺信息时只追问关键问题。 |
| 找出能力点 | 从具体任务、做成的结果和他人反馈中找出已经证明的能力，不用性格标签代替证据。 |
| 判断岗位重要性 | 分开分析岗位在行业价值链、当前组织和个人长期发展中的位置；说明它为何重要、缺位会发生什么、未来 3 年会怎样变化。 |
| 提炼能力账户 | 从岗位最重要的判断和结果倒推能力，把经历改写成“当前证据、能力边界、下一层、证明方式”，明确未来真正要练什么。 |
| 确认长期兴趣 | 判断用户愿意重复哪些工作，也检查他是否能接受这些工作的日常与枯燥部分。 |
| 对应岗位 | 先判断用户愿意重复的任务，再从互联网、AI、金融、消费、文化、制造、医疗、教育、能源等行业中找到具体岗位。每个方向都说明日常任务、门槛和验证方法。 |
| 选择长期道路 | 给出一个主方向和一至两个相邻方向，说明未来 3–5 年可以积累什么，以及换公司后还能带走什么。 |
| 建设职业护城河 | 判断用户目前处于准入能力、关键判断、可复用系统、可携带资产或放大杠杆中的哪一层，再安排 90 天、1 年和 3–5 年建设顺序。 |
| 锁定决策 | 生成一张判断票据：问题类型、当前建议、最关键的问题、什么时候换方向、先看哪些变化和复盘日期。 |
| 大师透镜 | 选择 1–2 个真正相关的框架，标明它是正式框架、归纳启发式还是案例类比，并说明来源和失效边界。 |
| 反脆弱体检 | 检查组织变化、裁员、行业下行和技能折旧，给出 A/B/Z 路径。 |
| 变成行动 | 生成 90 天行动 Roadmap，按 P1/P2/P3 阶段写清时间、产物和验收信号。 |
| 留下记录 | 用户一次授权后，持续更新选定的 HTML 或飞书文档；下一次直接在已有履历、行动和新证据上继续。 |

真正的差别在诊断深度和持续复盘。Skill 不会从“行业热门”直接跳到“建议进入”，它会先分析岗位怎样创造价值、在组织里能决定什么、对什么结果负责，再从这些关键判断倒推用户要培养的能力。本轮结论会变成下一轮可检查的假设。用户回来后，先看哪些判断被现实验证或推翻，再调整主路径、能力账户和护城河建设顺序。

大师透镜还有一道准入门槛。一个观点需要有明确原始出处，或在不同公开场景中反复出现并能处理新问题，才能称为“框架”；证据较弱时只能写成“启发式”或“案例类比”。报告不会模仿名人语气，不会杜撰引语，也不会暗示某位人物本人认可这份建议。

这里使用 **ABZ**。A 是当前集中投入的主路径，B 是与 A 相邻并提前准备的备选路径，Z 是 A/B 都受挫时保护现金流和生活的安全底座。这套框架与 ABC 评分无关。报告会用圈层图和白话说明三者的关系。

它也会根据问题选择合适的图表或结构化表，例如从经历到岗位的证据链、岗位生态位置、能力账户、offer 对比、路径图、JD 匹配表和职业风险四象限。HTML 使用米色纸张与编辑部研究档案版式：封面负责建立主题，判断区是一张连续小票，正文使用证据刻度、链路、纸带和时间轴解释结论。长字段会自动拆成 2–4 个短要点，页面不会依靠缩小字号容纳长段落。页面不依赖图片或 JavaScript，手机与打印会自动调整。

## 大师透镜如何工作

大师透镜会根据用户正在解决的问题定向检索。它不会先列一份名人排行榜，也不会因为某个人有名就套用他的故事。

当前宿主具备搜索或浏览能力时，Skill 会搜索创业者、产品负责人、设计师、投资人、管理学者和行业专家的公开材料。检索顺序是：

1. 本人著作、官网、课程、公开演讲和署名文章。
2. 本人接受的正式访谈、播客或机构发布的完整记录。
3. 多个可靠来源能够相互印证的归纳。
4. 人物或公司的经历类比。案例只能帮助提出问题，不能直接证明用户应该照做。

一个候选透镜需要同时通过四项检查：

- **相关**：能处理用户当前的职业问题，不只提供鼓励。
- **可核实**：有清楚来源，知道它属于正式框架、归纳启发式还是案例类比。
- **可执行**：能够转换成一个判断、实验或行动。
- **有边界**：说明它在什么情况下不适用，以及人物经历和用户处境有哪些差别。

每份完整规划最多使用两个透镜，并写明来源状态、核心方法、对当前用户的用途和失效边界。Skill 不模仿名人语气，不拼接二手金句，也不会暗示当事人认可这份职业建议。

当前宿主没有联网能力时，Skill 会标注“未现场核实”。它只使用来源较稳定的框架，动态履历、公司数据和人物引语不会自行补全。

这里的“联网搜索”和“HTML 离线安全”是两层能力：

- **咨询阶段可以联网**：宿主有 Web Search、浏览器或网页读取工具时，Skill 会用 2–4 个定向查询寻找本人著作、官方演讲、完整访谈、股东信、论文等一手材料，并把来源、核实日期和适用边界写进透镜。
- **报告打开时不自动联网**：生成后的 HTML 不加载外部图片、脚本、字体、视频或追踪地址。报告可以用纯文本记录来源 URL，用户需要时自行打开。这能防止用户只看本地档案，也无意中向陌生网站暴露 IP 和打开时间。

这与女娲 Skill 的思路相同：网络搜索负责发现公开材料，一手来源负责证明归属，搜索工具不可用时诚实降级。职业规划只选择与本次决策相关的 1–2 个透镜，不运行人物蒸馏所需的六路重型调研。

## HTML 在不同 Agent 中会不会变化

会有一定变化。Claude、Codex、Kimi 和 Cursor 负责形成内容，最终页面由浏览器渲染。完整 Skill 包和生成脚本可以固定大部分视觉规则，但无法让所有系统、字体和浏览器产生逐像素相同的结果。

**固定的部分：**

- `assets/报告模板.html` 固定米色纸张、编辑部档案网格、判断小票、章节顺序、图表组件、移动端和打印样式。
- `scripts/render_report.py` 把结构化数据填入同一模板，转义用户文字并清理危险标签。
- `scripts/validate_report.py` 检查 11 个固定章节、五步兴趣证据链、判断票据、占位符和可执行内容。
- 完整规划统一使用兴趣路径、岗位对照、护城河纸带、ABZ 圈层和行动 Roadmap，不允许 Agent 临时发明另一套页面结构。

**仍可能变化的部分：**

- 不同 Agent 对内容长短、标题和图表数量的判断可能不同，内容密度会影响页面节奏。
- 当前部分栏目仍允许 Agent 生成受限的 HTML 片段；它如果没有沿用示例组件，局部排版会发生变化。
- Futura 和苹方采用本地字体。设备没有安装 Futura 时会退回 Futura PT 或 Century Gothic；没有苹方时会退回微软雅黑、思源黑体、Noto Sans CJK SC 或冬青黑体。公开仓库不直接打包商业字体。
- 滚动动效使用渐进增强。旧浏览器会关闭部分动效，但正文、图表和打印不会缺失。

在 Claude Code 中使用时，应导入整个 `career-planning/` 文件夹，并允许它读取 `assets/`、`references/` 和 `scripts/`。只复制 `SKILL.md` 会显著增加视觉偏差。具备 Python 和文件权限时，必须通过生成脚本输出 HTML，再运行校验器；不要让 Agent 手工重写整页 CSS。

当前架构可以稳定整体风格，局部组件仍存在中等偏差风险。进一步追求跨 Agent 一致性时，应把栏目数据改成固定 JSON 数组，由渲染器生成所有卡片、表格和图表，让 Agent 只填写文字与状态。

## 它不会怎么做

- 不用一次性性格测试或“你属于某类人”决定职业方向。
- 不用公司名、title、薪资或通用 JD 匹配百分比代替真实工作与团队判断。
- 不用 1–10 分自评、随意权重和小数总分制造客观感。
- 不扮演名人给用户下结论，也不把二手金句包装成“大师理论”。
- 不同时列十条方向让用户自己选；信息足够时会给倾向，信息不足时会给最小验证实验。
- 不声称拥有平台没有提供的长期记忆、后台监听或自动提醒能力。

## 怎么开始与继续

第一次使用，直接像下面这样说：

```text
帮我做职业规划。我现在做产品运营 2 年，想转产品经理，但担心收入下降。

我该不该离职？我在现在公司待了 18 个月，手里有一个新 offer。

这是我的简历和 JD，帮我判断是否值得投递。

帮我做职业规划，并建立一份飞书职业档案。以后我回来补充进展时，请继续更新同一篇文档。
```

以后遇到新情况，可以随时回来补充：

```text
继续我的职业档案：我现在遇到的问题是组织要调整，我可能会被转岗。

更新我的职业规划：我试了上次建议的项目，发现自己更喜欢客户研究，不喜欢纯投放。

我有一个新 offer。按我们上次的目标，帮我重新判断要不要去。
```

第一次明确要求完整职业规划、职业档案或持续咨询时，Skill 会先检查飞书文档能力是否真的可调用且已授权。飞书已连接时，用户选择本地 HTML、飞书文档或只做本次；飞书不可用时，只显示 HTML 和只做本次。轻量问答会先直接回答，不用存档询问打断。选择 HTML 后，同目录的 `.state.json` 作为私有数据源；选择飞书后，只持续更新同一篇飞书文档。只有用户明确说“两种都要”时才双写。

它不会把整段聊天保存进去，也不会在用户离开后假装仍在后台记忆、监听或弹窗。飞书通知、定时提醒和后台更新需要额外配置机器人或自动化。

## 你会拿到什么

完整规划写入用户选定的主档案：

- `HTML`：本地档案，包含判断票据、证据、兴趣假设、职业护城河、大师透镜、职业路径、反脆弱体检和行动 Roadmap；配套私有状态 JSON 用于安全增量更新。
- `飞书 / Lark`：只有当前环境具备已授权且可调用的飞书文档能力时才显示。选择后持续更新同一篇飞书文档，不额外生成 HTML。仅安装 CLI 不代表已完成授权。
- `两种都要`：不作为默认选项；用户明确提出时才同时维护 HTML 和飞书。
- `PDF`：HTML 用户可直接打印或导出。飞书用户要求 PDF 时，先确认从飞书导出还是额外生成 HTML。

本地不再创建 Markdown 职业档案。没有文件权限时，Skill 会在对话中交付完整规划；没有图表工具时退回 Mermaid、SVG 或表格，不会因为缺少某个平台能力而中断。

匿名 HTML 预览见 [职业决策报告示例](examples/职业决策报告示例.html)，其中包含兴趣到岗位的证据链、护城河分层纸带、大师透镜、组织/裁员/行业风险表、ABZ 圈层解释和行动 Roadmap。

HTML 由 Skill 内的安全生成脚本从结构化 JSON 产出。普通文字会自动转义，图表片段只保留有限的排版与 SVG 属性；脚本、事件属性、外部资源和未知属性会被移除。模板还带 CSP，浏览器会阻止报告自动访问网络。这个限制只作用于生成后的档案，不会关闭 Agent 在咨询阶段的 Web Search。匿名字段样例见 `.claude/skills/career-planning/assets/报告数据示例.json`。

## 数据与边界

- 可以基于用户提供的简历、JD、offer、薪资、公司信息和个人约束分析，并明确这些信息来自用户。
- 对公司经营、融资、裁员、薪资、法规、行业数据等动态信息：有可靠搜索能力时查公开来源；无法核实时会说明不确定性，不补造数字或新闻。
- 不要粘贴身份证号、电话、住址、公司机密、客户数据或未公开业务信息。
- 输出是职业规划与决策支持，不构成法律、劳动争议、签证、投资、税务、医疗或心理健康意见。重要决定应由用户结合完整信息作出，必要时咨询专业人士。

## 安装

本仓库的 Skill 目录是：

```text
.claude/skills/career-planning/
```

这是一个标准的 Agent Skill 目录：根部是 `SKILL.md`，同级包含 `references/`、`assets/` 和 `scripts/`。小红书 RedSkill 可直接上传该文件夹，也可上传本仓库生成的 RedSkill zip 包。

### 通用安装（发布 GitHub 后推荐）

支持 [Agent Skills](https://agentskills.io/) 和 `skills` CLI 的宿主，可以从 GitHub 自动识别并安装：

```bash
npx skills add https://github.com/yutongcai0628/career-planning-skill --skill career-planning
```

也可指定宿主，例如 `--agent claude-code`、`--agent codex` 或 `--agent cursor`。

### Claude Code

放到项目内：

```text
你的项目/.claude/skills/career-planning/
```

或复制到全局目录：

```bash
cp -r .claude/skills/career-planning ~/.claude/skills/
```

### Codex

```bash
mkdir -p ~/.codex/skills
cp -r .claude/skills/career-planning ~/.codex/skills/
```

之后可以直接说：`我对工作有点迷茫，不知道自己擅长什么，也不知道未来几年该走哪条路。`

### Cursor

Cursor 可以直接读取用户级 Skill：

```bash
mkdir -p ~/.cursor/skills
cp -r .claude/skills/career-planning ~/.cursor/skills/
```

也可以使用项目规则适配器。将适配文件复制到打开的项目中，并同时保留项目根目录下的 `.claude/skills/career-planning/`：

```bash
mkdir -p .cursor/rules
cp adapters/cursor/career-planning.mdc .cursor/rules/career-planning.mdc
```

这个规则会在相关对话中引导 Cursor Agent 读取同一份 `SKILL.md`，所以方法论只维护一处。项目需要更强的自动触发时再加 `.mdc`；常规安装优先使用 `~/.cursor/skills/`。

### Kimi Code

Kimi Code CLI 原生支持目录型 `SKILL.md`，并可根据 `description` 自动触发：

```bash
mkdir -p ~/.kimi-code/skills
cp -r .claude/skills/career-planning ~/.kimi-code/skills/
```

也可安装到项目的 `.kimi-code/skills/` 或 `.agents/skills/`。手动调用时输入 `/skill:career-planning`。安装路径和自动触发行为参考 [Kimi Code 官方 Agent Skills 文档](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/skills.html)。

### GitHub Copilot

GitHub Copilot 可以在项目中读取 `.github/skills/`、`.claude/skills/` 或 `.agents/skills/`，所以当前仓库结构可直接使用。用户级安装可复制到 `~/.copilot/skills/` 或 `~/.agents/skills/`。详见 [GitHub 官方 Agent Skills 文档](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)。

### 其他 Agent

如果平台支持导入 Skill、规则文件或知识库，导入 `.claude/skills/career-planning/` 整个目录，并保持 `references/` 与 `assets/` 的相对路径可访问。

对于 OpenClaw、Gemini CLI、OpenCode、Hermes Agent 等支持标准 Agent Skills 或通用 `skills` CLI 的宿主，优先使用前面的 `npx skills add`。女娲 Skill 也采用这种“标准目录 + 通用安装器 + 纯 Markdown 降级”方式，可参考其 [GitHub 仓库](https://github.com/alchaincyf/nuwa-skill)。

不支持自动发现 Skill 的 Agent，可以把 `SKILL.md` 加入项目规则或对话上下文。此时仍要让 Agent 能读取同级的 `references/`、`assets/` 和 `scripts/`。

不同平台对自动触发的支持并不一致。支持读取 `SKILL.md` 元数据的平台会根据描述匹配职业、职场、事业发展、工作迷茫、能力优势、长期道路、离职、入职、offer、JD 和转行等请求。其他平台需要在规则中引用 `SKILL.md`，也可以让用户明确说「使用 career-planning skill」。

安装后可以用下面三句话测试触发：

```text
我最近对事业发展很迷茫，不知道下一步应该做什么。
我想知道自己真正擅长哪些能力，未来几年应该怎样积累。
这份工作收入还可以，但我看不清长期职业道路。
```

## 目录说明

```text
.
├── README.md
├── LICENSE
├── .gitignore
├── .github/workflows/release-check.yml   GitHub 自动发布检查
├── adapters/cursor/career-planning.mdc  Cursor 项目规则适配入口
├── examples/职业决策报告示例.html         匿名报告成品，用于查看 HTML 版式
├── scripts/build_release.py             生成 RedSkill 文件夹与 zip
├── scripts/validate_host_results.py     校验真实跨宿主盲测记录
├── tests/                               静态测试、盲测题与宿主结果
└── .claude/skills/career-planning/
    ├── SKILL.md                    主流程、触发词、边界与输出要求
    ├── agents/openai.yaml          Codex 展示元数据
    ├── assets/报告模板.html         无外部图片和脚本的 HTML 报告模板
    ├── assets/报告数据示例.json     匿名结构化字段样例
    ├── assets/报告设计哲学.md       报告布局与图表规范
    ├── scripts/render_report.py    转义、清理并生成 HTML
    ├── scripts/validate_report.py  检查栏目、占位符和危险内容
    └── references/                 按场景加载的方法、行业岗位地图与质量门槛
```

发布到 RedSkill 时，上传 `.claude/skills/career-planning/` 整个文件夹，或上传仓库生成的 `career-planning-redskill-<版本>.zip`。zip 解压后的第一层必须是 `career-planning/`，其中直接包含 `SKILL.md`、`LICENSE` 和 `MANIFEST.json`。构建器只接受审核过的文件白名单，拒绝符号链接、未知文件、常见凭据、手机号和身份证号，并检查单个文件不超过 10 MB、总大小不超过 30 MB。`release/LATEST.json` 会标明唯一应上传的文件及 SHA-256；旧 ZIP 自动移入 `release/archive/`。

发布到 GitHub 时，提交整个仓库即可；请勿提交 `职业档案/`、真实简历/JD、`.DS_Store`、本地设置或本地生成的报告。

## 发布前检查

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .claude/skills/career-planning
python3 .claude/skills/career-planning/scripts/validate_report.py examples/职业决策报告示例.html
python3 scripts/build_release.py
```

公开构建要求 Git 工作区干净，并从 HEAD 的提交日期生成稳定版本名。相同源码、版本和 `SOURCE_DATE_EPOCH` 会得到相同 ZIP；本地开发中尚未提交时只能使用 `python3 scripts/build_release.py --allow-dirty --version dev`，生成的 manifest 会标记 `source_dirty: true`，不得上传。

`tests/blind-eval-cases.json` 收录了应触发、不应触发、offer 决策、联网大师检索、档案增量更新、隐私与离线数据等盲测题。需要补充跨宿主质量证据时，可交给未参与开发的 Agent 单独运行，避免它从开发记录中猜到预期答案。真实运行结果写入 `tests/host-validation-results.json`，脱敏后的原始输出保存在 `tests/host-artifacts/`。这些记录是可选验证材料，不作为 Git tag 或 RedSkill 上传的强制门槛。

## License

[MIT](LICENSE)
