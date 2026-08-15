# PaperJoy · 学术文献终极剖析系统（V4.0）（曾用名：文献悦读）

[![License](https://img.shields.io/github/license/GeorgeYoY/paper-joy?style=flat)](LICENSE)
[![Version](https://img.shields.io/github/v/release/GeorgeYoY/paper-joy?label=version)](https://github.com/GeorgeYoY/paper-joy/releases)
[![Build](https://img.shields.io/github/actions/workflow/status/GeorgeYoY/paper-joy/validate.yml?branch=main&label=build)](https://github.com/GeorgeYoY/paper-joy/actions/workflows/validate.yml)
[![Repo Size](https://img.shields.io/github/repo-size/GeorgeYoY/paper-joy)](https://github.com/GeorgeYoY/paper-joy)
[![Last Commit](https://img.shields.io/github/last-commit/GeorgeYoY/paper-joy)](https://github.com/GeorgeYoY/paper-joy/commits/main)
[![Downloads](https://img.shields.io/github/downloads/GeorgeYoY/paper-joy/total)](https://github.com/GeorgeYoY/paper-joy/releases/latest)
[![Stars](https://img.shields.io/github/stars/GeorgeYoY/paper-joy?style=social)](https://github.com/GeorgeYoY/paper-joy/stargazers)
[![Download](https://img.shields.io/badge/download-paper--joy.zip-blue)](https://github.com/GeorgeYoY/paper-joy/releases/latest)

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

## 📦 安装方式（任选其一，全平台通用）

### 方式 A：粘贴提示词（最通用，所有 AI 都支持）
适用于**任何** AI 助手——只要它能设置「系统指令 / 自定义指令 / Custom Instructions / 系统提示词」。

1. 打开本仓库的 **`PROMPT.md`**，全选复制全部内容。
2. 粘贴到你所用 AI 的「系统指令 / 自定义指令」设置里并保存。
3. 之后直接把论文贴给 AI，说「分析这篇文献」即可触发七模块剖析。

> `PROMPT.md` 是去除了平台专属标记的纯提示词版，与本仓库 `SKILL.md` 内容等价，专供不支持 skills 文件夹的客户端使用。

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
- **WorkBuddy 市场**：用本仓库的 `paper-joy.zip` 提交审核，通过后网友可搜索安装。
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

## 📁 目录结构

```
paper-joy/
├── SKILL.md                 # 技能本体（七模块剖析框架，WorkBuddy 等客户端用）
├── PROMPT.md               # 通用提示词版（去平台标记，任意 AI 粘贴即用）
├── manifest.yaml            # 市场发布元数据（name/触发词/分类/tags）
├── paper-joy.zip            # 可直接上架的分发包
├── README.md                # 本文件
├── LICENSE                  # MIT 许可证
└── .gitignore
```

---

## 🔄 更新日志

- **v1.0.2**（2026-08-15）跨平台化：新增 `PROMPT.md`（纯提示词通用版，可粘贴进任意 AI）；README 改为跨主流 AI 客户端安装（WorkBuddy / Claude / Cursor / ChatGPT / Gemini 等），去 WorkBuddy 专属表述；`manifest.yaml` 描述泛化。
- **v1.0.1**（2026-08-15）公开更名记录同步：展示名「文献悦读」→「PaperJoy」、内部标识 `literature-yuedu` → `paper-joy`（功能不变）；README 增加仓库徽章（License / Version / Build / 下载按钮等）。
- **v1.0.0**（2026-08-15）初版发布：七模块剖析框架 + 试验时间线图 + 试验时间分配表；口语化触发词 15 条；作者 GeorgeYoY。

---

## 🤝 反馈与贡献

欢迎在 GitHub Issues / 各市场评论区提出吐槽与建议。收到反馈后我会：
改 `SKILL.md` / `PROMPT.md` → 递增 `manifest.yaml` 的 `version` 并更新本文件「更新日志」→ 重新打包 `paper-joy.zip` → 发布新 Release / 重新提交市场审核 → 已安装用户自动收到更新。

如想贡献代码或示例，欢迎提交 Pull Request。

---

## ☕ 支持与交流

如果这个技能帮你省下了读文献的时间，欢迎用以下方式支持持续维护：

- **请作者喝杯咖啡（捐赠）**：[在此填写你的捐赠链接，如 爱发电 / Patreon / 支付宝收款码]
- **交流群 / 反馈群**：[在此放置群链接或二维码图片地址，如 微信群 / QQ 群 / Discord]
- **公众号 / 自媒体**：[在此填写你的账号名，方便网友关注后续更新]
- 也欢迎直接开 [GitHub Issue](https://github.com/GeorgeYoY/paper-joy/issues) 提建议或报 bug。

> 注：上方方括号内容为占位符，发布前请替换为你的真实链接；不想公开可整段删除。

---

## 📄 许可证

[MIT](LICENSE) © GeorgeYoY
