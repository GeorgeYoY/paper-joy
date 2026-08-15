# PaperJoy · 学术文献深刻剖析系统（文献悦读）

[![License](https://img.shields.io/github/license/youyang9205/paper-joy?style=flat)](LICENSE)
[![Version](https://img.shields.io/github/v/release/youyang9205/paper-joy?label=version)](https://github.com/youyang9205/paper-joy/releases)
[![Build](https://img.shields.io/github/actions/workflow/status/youyang9205/paper-joy/validate.yml?branch=main&label=build)](https://github.com/youyang9205/paper-joy/actions/workflows/validate.yml)
[![Repo Size](https://img.shields.io/github/repo-size/youyang9205/paper-joy)](https://github.com/youyang9205/paper-joy)
[![Last Commit](https://img.shields.io/github/last-commit/youyang9205/paper-joy)](https://github.com/youyang9205/paper-joy/commits/main)
[![Downloads](https://img.shields.io/github/downloads/youyang9205/paper-joy/total)](https://github.com/youyang9205/paper-joy/releases/latest)
[![Stars](https://img.shields.io/github/stars/youyang9205/paper-joy?style=social)](https://github.com/youyang9205/paper-joy/stargazers)
[![Download](https://img.shields.io/badge/download-paper--joy.zip-blue)](https://github.com/youyang9205/paper-joy/releases/latest/download/paper-joy.zip)

> 一款**跨平台**的学术文献深度剖析提示词 / 技能。无论是 WorkBuddy、Claude、ChatGPT、Cursor、Gemini，还是任意支持「自定义指令 / System Prompt / Skills」的 AI 助手，都能装上它。
> 粘贴一篇论文（全文 / 摘要 / PDF 复制文本 / 段落摘录均可），自动产出结构化的七模块深度剖析报告，并额外生成**试验时间线图**与**试验时间分配表**，让你一眼看清「什么时间做了什么试验、什么时间出了什么结果」。

---

## ✨ 功能特性

| 模块 | 内容 |
| --- | --- |
| 一、文本预处理与降噪 | 内部执行：修复 PDF 复制导致的换行/断句/乱码，重构逻辑段落（不对外展示） |
| 二、一分钟速览 TL;DR | ≤200 字高密度概括 + ★1–5 星阅读推荐指数 |
| 三、核心术语表 | 提取 3–5 个核心术语/缩写，通俗降维解释 |
| 四、多维度深度剖析 | 背景动机 / 假设 / 方法 / 创新点 / 结果与结论（**强制图文映射**）/ 局限 / 批判性评价 |
| 五、技术路线重构与时间线 | `graph TD` 流程图（节点带时间窗）+ Mermaid `timeline` 时间线 + **试验时间分配表** |
| 六、可复现性评估 | 开源代码/数据、参数完备性、复现可行性判断 |
| 七、延伸探索 | 3 个基于该技术路线的延伸研究问题 |

**核心亮点**：所有结论必须标注支撑图表（`**【对应图表：Figure X】**`），缺失则如实标注「无明确支撑」，不编造；试验时间分配表把「做试验」与「出结果」对齐到同一时间节点。

---

## 🤖 模型适配建议（关于「效果取决于 AI 本身」）

PaperJoy 本质是一份**结构化提示词（System Prompt）**，不是独立程序——它不自带分析引擎，而是把能力「借」给运行它的基础模型。因此：

- **效果上界由你选用的模型决定**：模型越强（长上下文、强推理、少幻觉），剖析越深越准；弱模型可能省略细节或理解偏差。这是提示词类工具的固有属性，无法靠提示词本身消除。
- **但 PaperJoy 已内置多重护栏，把方差压到最低**：
  - **强制七模块**：无论模型强弱，结构完整、不漏模块；
  - **禁虚构约束**：明确要求「无图表支撑须写『无明确支撑』、不得编造编号/数据/链接」；
  - **图文映射硬绑定**：每条结论必须标注支撑图表；
  - **输出前自检清单**：模型交付前逐条核对模块齐备性、图表标注、零虚构、Mermaid 可渲染。
  → 即便在一般模型上，也能保证**格式规范、不胡编**，而非保证深度与强模型等同。
- **推荐模型**（实测/官方建议，按能力排序）：Claude Opus / Sonnet 系列、GPT-4o 及更高、Gemini 1.5 Pro 及更高、WorkBuddy 内置的强模型。处理长论文（>20 页）时，优先选**长上下文**模型以避免截断。
- **一句话**：把 PaperJoy 当作「严谨的论文剖析模板 + 约束器」，模型是「执行者」。想拿到最佳报告，请配强模型使用。

---

## 📦 安装方式（任选其一，全平台通用）

### 方式 A：粘贴提示词（最通用，所有 AI 都支持）
适用于**任何** AI 助手——只要它能设置「系统指令 / 自定义指令 / Custom Instructions / 系统提示词」。

1. 获取 `PROMPT.md`：从本仓库 **[Release 资产](https://github.com/youyang9205/paper-joy/releases/latest/download/paper-joy.zip)** 下载（解压即得），或克隆仓库后运行 `python tools/build_prompt.py` 本地生成。
2. 全选复制 `PROMPT.md` 全部内容，粘贴到你所用 AI 的「系统指令 / 自定义指令」设置里并保存。
3. 之后直接把论文贴给 AI，说「分析这篇文献」即可触发七模块剖析。

> `PROMPT.md` 是 `SKILL.md` 的**自动派生**文件（由 `tools/build_prompt.py` 生成），二者内容等价且**同源维护**——你只需编辑 `SKILL.md`，重跑脚本即可同步 `PROMPT.md`，不会出现两份手维护的重复体。

### 方式 B：放入技能文件夹（支持 Skills 的客户端）
把整个 `PaperJoy` 文件夹放进对应客户端的 skills 目录，重启客户端即可：

| 客户端 | 放置路径 |
| --- | --- |
| **WorkBuddy** | 用户级 `C:\Users\你的用户名\.workbuddy\skills\PaperJoy\` 或项目级 `<工作区>\.workbuddy\skills\PaperJoy\` |
| **Claude（Claude Code / 桌面端）** | `~/.claude/skills/PaperJoy/` |
| **Cursor** | 项目级 `.cursor/skills/PaperJoy/` 或用户级 skills 目录 |
| **其他兼容客户端** | 参考其文档，将本目录作为 skill / 指令集加载（目录内需含 `SKILL.md`） |

> 各客户端对 skills 的目录约定不同，上面为常见写法；若你的客户端有特殊要求，以官方文档为准。

### 方式 C：上架公共技能市场（供网友一键安装）
- **WorkBuddy 市场**：从本仓库 **[Release](https://github.com/youyang9205/paper-joy/releases/latest)** 下载 `paper-joy.zip` 提交审核，通过后网友可搜索安装。
- **其他客户端的市场 / 插件商店**：按平台要求上传 `SKILL.md` 或 `PROMPT.md`（如支持自定义技能上传，直接传 `PROMPT.md` 即可）。

---

## 🧪 使用示例

**示例 1 · 基础深度剖析**
> 用户：分析这篇文献 ——（粘贴全文）
> 系统：输出七模块完整报告，含强制图文映射。

**示例 2 · 聚焦试验时间线（特色）**
> 用户：帮我拆解这篇田间试验论文，重点看时间线
> 系统：额外生成 Mermaid 时间线图 + 「试验时间分配表」（时间节点 / 阶段 / 干了什么试验 / 对应图表 / 产出结果）。

**示例 3 · 只有摘要/片段**
> 用户：（仅粘贴摘要）
> 系统：基于已有信息剖析，对缺失部分如实标注「原文未提供」，不编造。

**示例 4 · 英文文献**
> 用户：（粘贴英文论文，要求英文报告）
> 系统：同结构输出英文版剖析。

---

## 📋 输入要求与能力边界

为拿到最稳、最准确的剖析，请这样提供文献（更完整说明见 `SKILL.md` 第六、七节）：

- **给什么最稳**：论文全文 > 摘要 + 关键段落 > PDF 复制文本 > 上传图片（需配文字）。推荐单次 **≤ 约 20 页 / 1.5 万–2 万中文字**；超长请按章节拆分或换长上下文模型。
- **复杂格式**：表格复制为文本 / Markdown / CSV；公式给 LaTeX；双栏 PDF 先转纯文本；扫描版先 OCR；图表可上传截图并指明编号。
- **输入不足时**：系统会在首条回复给出**具体补充指引**（缺什么、以何种格式补），不会含糊带过，也不会编造。
- **明确不能做**：不能自行检索 / 下载原文、不能替代文献库检索、不保证未提供文本处的准确性、不导出引文格式、不翻译整篇、效果上界受运行模型限制。

## 🚫 常见错误用法（反模式）

- ❌ 只给标题 / 一句描述就期待完整剖析 → 至少给摘要。
- ❌纯图片 PDF / 截图直接丢进来却无文字 → 先 OCR / 复制正文。
- ❌ 期望系统凭空补全原文没有的方法 / 数据 / 图表编号 → 缺失会如实标注，不会编造。
- ❌ 「一句话总结」式指令却想要深度剖析 → 明确说「用 PaperJoy 完整分析这篇文献」。
- ❌ 一次想吃下整本书 → 超长请拆分或换长上下文模型。
- ✅ 正确姿势：粘贴文本 / 上传图 + 一句触发（「分析这篇文献」），缺什么系统会告诉你。

## ❓ 常见问题 FAQ

- **只给摘要能分析吗？** 能，但相关结论按「基于片段分析，结论可能不完整」标注缺口，不编造。
- **超长论文怎么办？** 按章节拆分多次分析，或选长上下文模型，避免截断。
- **公式 / 表格 / 双栏 PDF 怎么处理？** 表格复制为文本；公式给 LaTeX；双栏先转纯文本；扫描版先 OCR。
- **能分析图片里的图吗？** 可上传截图并指明编号（如「这是 Figure 3」），图外正文仍需文字。
- **中英文都支持吗？** 都支持；默认中文，要求英文时整体英文输出，模块结构不变。
- **结果能直接引用 / 写进论文吗？** 用于辅助理解，关键数据请回看原文核对，勿把输出当已发表事实直接引用。
- **为什么不同 AI 效果不同？** 本技能是提示词，分析引擎是运行它的基础模型；强模型剖析更深（详见「🤖 模型适配建议」）。
- **需要联网 / 装插件 / 配密钥吗？** 不需要。纯提示词，离线可用，国内 AI 助手均可装载。

---

## 📁 目录结构

```
paper-joy/
├── SKILL.md                 # ★ 唯一手工维护文件（七模块剖析框架，WorkBuddy 等客户端用）
├── tools/
│   └── build_prompt.py      # 由 SKILL.md 自动生成 PROMPT.md 的脚本（单一信息源构建器）
├── PROMPT.md               # （自动生成，未跟踪）通用提示词版，见 Release 资产
├── paper-joy.zip            # （自动生成，未跟踪）可直接上架的分发包，见 Release 资产
├── manifest.yaml            # 市场发布元数据（name/触发词/分类/tags）
├── README.md                # 本文件
├── LICENSE                  # MIT 许可证
└── .gitignore
```

> **单一信息源说明**：`SKILL.md` 是唯一需要你编辑的文件；`PROMPT.md` 与 `paper-joy.zip` 均由脚本/打包流程在其基础上自动生成，已加入 `.gitignore`，不进版本跟踪，仅在 Release 中随包分发。这避免了「两份核心文件高度重复、占用不必要的空间」的问题。

---

## 🔄 更新日志

- **v1.0.4**（2026-08-15）回应 TRACE 全维测评低分项（反模式/FAQ 3.5、异常处理 4.0、能力边界 4.5）：① `SKILL.md` 新增「输入要求与最佳实践 / 能力边界与限制 / 常见错误用法（反模式）/ 常见问题 FAQ」四节；② 模块一新增「输入校验 Input Gate」，输入不足（仅标题/纯图无文/乱码）时首条回复即给具体补充指引，消除「提示含糊」；③ README 同步增补输入要求、反模式、FAQ 三节，降低新手误用率。
- **v1.0.3**（2026-08-15）回应使用反馈，消除冗余 + 明确效果边界：① **单一信息源**：`SKILL.md` 为唯一手工维护文件，`PROMPT.md` 改由 `tools/build_prompt.py` 自动生成并移出版本跟踪（gitignore），不再有两份手维护的重复核心文件、不占仓库空间；② 提示词内新增**「输出前质量自检」**强制清单（模块齐备/图文映射/零虚构/Mermaid 可渲染/语言一致），拉平不同模型产出方差；③ README 新增 **「🤖 模型适配建议」** 小节，诚实说明效果上界由基础模型决定、已内置护栏把方差压到最低，并给出推荐模型；④ 下载入口统一指向 Release 资产。
- **v1.0.2**（2026-08-15）跨平台化：新增 `PROMPT.md`（纯提示词通用版，可粘贴进任意 AI）；README 改为跨主流 AI 客户端安装（WorkBuddy / Claude / Cursor / ChatGPT / Gemini 等），去 WorkBuddy 专属表述；`manifest.yaml` 描述泛化。
- **v1.0.1**（2026-08-15）公开更名记录同步：展示名「文献悦读」→「PaperJoy」、内部标识 `literature-yuedu` → `paper-joy`（功能不变）；README 增加仓库徽章（License / Version / Build / 下载按钮等）。
- **v1.0.0**（2026-08-15）初版发布：七模块剖析框架 + 试验时间线图 + 试验时间分配表；口语化触发词 15 条；作者 youyang9205。

---

## 🤝 反馈与贡献

欢迎在 GitHub Issues / 各市场评论区提出吐槽与建议。收到反馈后我会：
改 `SKILL.md`（**唯一源文件**）→ 跑 `tools/build_prompt.py` 同步 `PROMPT.md` → 递增 `manifest.yaml` 的 `version` 并更新本文件「更新日志」→ 重新打包 `paper-joy.zip` → 发布新 Release / 重新提交市场审核 → 已安装用户自动收到更新。

如想贡献代码或示例，欢迎提交 Pull Request。

---

## ☕ 支持与交流

如果这个技能帮你省下了读文献的时间，欢迎用以下方式支持持续维护：

- **交流 / 反馈**：[youyang9205@foxmail.com]
- **公众号**：[环境科学笔记]
- 也欢迎直接开 [GitHub Issue](https://github.com/youyang9205/paper-joy/issues) 提建议或报 bug。

> 注：上方方括号内容为占位符，发布前请替换为你的真实链接；不想公开可整段删除。

---

## 📄 许可证

[MIT](LICENSE) © youyang9205
