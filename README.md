# Writing Humanizer

Remove AI writing patterns from text, making it sound more natural and human. Focused on Traditional Chinese (Taiwan).

> Forked from [shyuan/writing-humanizer](https://github.com/shyuan/writing-humanizer), maintained by [helping-ai-workflow](https://github.com/helping-ai-workflow).

One skill, eight hosts. The same `skills/writing-humanizer` skill runs in Claude Code, OpenAI Codex, Cursor, Google Antigravity CLI, OpenCode, Kimi CLI, pi, and Gemini CLI — only the per-host manifest differs.

## Installation

### Claude Code

```bash
claude plugin marketplace add git@github.com:helping-ai-workflow/writing-humanizer.git
claude plugin install writing-humanizer
```

Reopen a Claude Code session and the skill is available.

To update:

```bash
claude plugin marketplace update writing-humanizer && claude plugin install writing-humanizer
```

<details>
<summary>Other AI agents (Cursor / Codex / Kimi / Gemini / Antigravity / OpenCode / pi)</summary>

| Agent | Install |
|---|---|
| Cursor / Codex / Kimi | Add `git@github.com:helping-ai-workflow/writing-humanizer.git` through the host's own plugin marketplace, then install `writing-humanizer` |
| Gemini CLI | `gemini extensions install https://github.com/helping-ai-workflow/writing-humanizer` |
| Antigravity CLI | Reads `plugin.json` at the repo root — clone the repo into the host's plugins location |
| OpenCode | Add `"writing-humanizer@git+https://github.com/helping-ai-workflow/writing-humanizer.git"` to the `plugin` array in `opencode.json` (see [`.opencode/INSTALL.md`](.opencode/INSTALL.md)) |
| pi | `pi install git:github.com/helping-ai-workflow/writing-humanizer` |

| Host | Manifest the host reads |
|------|--------------------------|
| Claude Code | `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` |
| OpenAI Codex | `.codex-plugin/plugin.json` |
| Cursor | `.cursor-plugin/plugin.json` |
| Google Antigravity CLI | `plugin.json` (repo root) |
| Kimi CLI | `.kimi-plugin/plugin.json` |
| Gemini CLI | `gemini-extension.json` + `GEMINI.md` |
| OpenCode / pi | `package.json` |

</details>

## What You Get

### Skill: `writing-humanizer`

A comprehensive skill that detects and rewrites 31 categories of AI writing patterns:

**Content Patterns (1-6)**
- Significance inflation, notability name-dropping, superficial analysis
- Promotional language, vague attributions, formulaic "challenges & outlook"

**Language Patterns (7-12)**
- AI vocabulary overuse, copula avoidance, negative parallelisms
- Rule of three, synonym cycling, false ranges

**Style Patterns (13-17)**
- Em dash overuse, boldface overuse, inline-header lists
- Emoji decoration, quotation mark issues

**Communication Patterns (18-24)**
- Chatbot artifacts, knowledge-cutoff disclaimers, sycophantic tone
- Filler phrases, excessive hedging, generic conclusions, throat-clearing openers

**Structure & Rhetoric Patterns (25-31)** — Chinese-essay-specific
- Outline-as-essay, bold 4-char-label lists, significance-stamping endings
- In-sentence keyword bolding, meta-discourse/roadmap announcements, sublimating moralizing conclusions
- Reifying an abstract process into "a line/route" and pointing back to it repeatedly

### Key Features

- AI vocabulary watchlist with suggested replacements for Traditional Chinese (Taiwan)
- Common AI sentence templates specific to Chinese writing
- Two-pass rewriting process with self-audit
- Quality scoring system (50 points across 5 dimensions)

## Quick Start

After installation, invoke the skill (slash-command syntax varies by host — this is the Claude Code form):

```
/writing-humanizer:writing-humanizer <paste your text here>
```

Or simply ask your agent to humanize text — the skill is discovered from its description and loaded on demand.

## References

- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [Wikipedia: AI 生成文的特徵](https://zh.wikipedia.org/wiki/Wikipedia:AI%E7%94%9F%E6%88%90%E6%96%87%E7%9A%84%E7%89%B9%E5%BE%B5)
- [stop-slop](https://github.com/hardikpandya/stop-slop)
- [humanizer](https://github.com/blader/humanizer) / [Humanizer-zh](https://github.com/op7418/Humanizer-zh)

## License

MIT

---

# Writing Humanizer（中文說明）

> Fork 自 [shyuan/writing-humanizer](https://github.com/shyuan/writing-humanizer)，由 [helping-ai-workflow](https://github.com/helping-ai-workflow) 維護。

去除文章中的 AI 寫作痕跡，使文字更自然、更有人味。以台灣正體中文為主。

一份 skill，八個 host。同一個 `skills/writing-humanizer` skill 可在 Claude Code、OpenAI Codex、Cursor、Google Antigravity CLI、OpenCode、Kimi CLI、pi、Gemini CLI 上運作——差別只在各 host 的 manifest。

## 安裝方式

### Claude Code

```bash
claude plugin marketplace add git@github.com:helping-ai-workflow/writing-humanizer.git
claude plugin install writing-humanizer
```

裝好後重開一個 Claude Code 對話即可使用。

更新：

```bash
claude plugin marketplace update writing-humanizer && claude plugin install writing-humanizer
```

<details>
<summary>其他 AI agent 安裝（Cursor / Codex / Kimi / Gemini / Antigravity / OpenCode / pi）</summary>

| Agent | 安裝 |
|---|---|
| Cursor / Codex / Kimi | 用各自的 plugin marketplace 加 `git@github.com:helping-ai-workflow/writing-humanizer.git`，再 install `writing-humanizer` |
| Gemini CLI | `gemini extensions install https://github.com/helping-ai-workflow/writing-humanizer` |
| Antigravity CLI | 讀 repo 根的 `plugin.json`——把 repo clone 進該 host 的 plugin 目錄 |
| OpenCode | `opencode.json` 的 `plugin` 陣列加 `"writing-humanizer@git+https://github.com/helping-ai-workflow/writing-humanizer.git"`（見 [`.opencode/INSTALL.md`](.opencode/INSTALL.md)） |
| pi | `pi install git:github.com/helping-ai-workflow/writing-humanizer` |

| Host | 該 host 讀的 manifest |
|------|--------------------------|
| Claude Code | `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` |
| OpenAI Codex | `.codex-plugin/plugin.json` |
| Cursor | `.cursor-plugin/plugin.json` |
| Google Antigravity CLI | `plugin.json`（repo 根） |
| Kimi CLI | `.kimi-plugin/plugin.json` |
| Gemini CLI | `gemini-extension.json` + `GEMINI.md` |
| OpenCode / pi | `package.json` |

</details>

## 安裝後你會得到

### Skill：`writing-humanizer`

一個完整的 skill，可偵測並改寫 31 類 AI 寫作模式：

**內容模式（1-6）**
- 誇大象徵意義、過度強調知名度、膚淺分析
- 宣傳性語言、模糊歸因、公式化的「挑戰與展望」

**語言模式（7-12）**
- AI 詞彙過度使用、繫動詞迴避、否定式排比
- 三段式法則、同義詞循環、虛假範圍

**風格模式（13-17）**
- 破折號過度使用、粗體過度使用、內嵌標題列表
- 表情符號裝飾、引號問題

**交流模式（18-24）**
- 聊天機器人痕跡、知識截止免責聲明、諂媚語氣
- 填充短語、過度限定、通用積極結論、開場白贅詞

**結構與修辭模式（25-31）** — 中文論說文專屬
- 大綱骨架代替文章、四字標籤排比清單、意義蓋章式收尾
- 句內關鍵詞粗體、元論述導讀宣告、升華訓誡式結尾
- 抽象事物具象成「一條線／路線」並反覆回指

### 主要特色

- 台灣正體中文 AI 詞彙警示列表與替代建議
- 中文常見 AI 句式模板辨識
- 兩輪改寫流程（初稿 + 自我審查再修改）
- 質量評分系統（5 個維度，滿分 50 分）

## 快速入門

安裝完成後，呼叫 skill（slash 指令語法因 host 而異，以下為 Claude Code 形式）：

```
/writing-humanizer:writing-humanizer <貼上你要處理的文字>
```

或直接請你的 agent 幫你去除 AI 痕跡——skill 會依其 description 被探索並按需載入。

## 參考資料

- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [Wikipedia: AI 生成文的特徵](https://zh.wikipedia.org/wiki/Wikipedia:AI%E7%94%9F%E6%88%90%E6%96%87%E7%9A%84%E7%89%B9%E5%BE%B5)
- [stop-slop](https://github.com/hardikpandya/stop-slop)
- [humanizer](https://github.com/blader/humanizer) / [Humanizer-zh](https://github.com/op7418/Humanizer-zh)

## 授權條款

MIT
