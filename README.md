# Writing Humanizer

Remove AI writing patterns from text, making it sound more natural and human. Focused on Traditional Chinese (Taiwan).

One skill, seven hosts. The same `skills/writing-humanizer` skill runs in Claude Code, OpenAI Codex, Cursor, Google Antigravity CLI, OpenCode, Kimi CLI, and pi — only the per-host manifest differs.

## Installation

### Claude Code

Via marketplace (recommended):

```bash
/plugin marketplace add shyuan/shyuan-marketplace
/plugin install writing-humanizer@shyuan-marketplace
```

Or direct:

```bash
/plugin install shyuan/writing-humanizer
```

### OpenCode

Add to the `plugin` array in your `opencode.json` (global or project-level), then restart OpenCode:

```json
{
  "plugin": ["writing-humanizer@git+https://github.com/shyuan/writing-humanizer.git"]
}
```

See [`.opencode/INSTALL.md`](.opencode/INSTALL.md) for version pinning and troubleshooting.

### Codex / Cursor / Antigravity CLI / Kimi CLI

Each of these hosts reads its own manifest bundled in this repo. Install with the host's own plugin/marketplace command pointing at this repo, or clone it into the host's plugins location and let the host discover the manifest:

```bash
git clone https://github.com/shyuan/writing-humanizer.git
```

| Host | Manifest the host reads |
|------|--------------------------|
| OpenAI Codex | `.codex-plugin/plugin.json` |
| Cursor | `.cursor-plugin/plugin.json` |
| Google Antigravity CLI | `plugin.json` (repo root) |
| Kimi CLI | `.kimi-plugin/plugin.json` |

### pi

pi loads the skill through the `"pi"` field in `package.json` (extension at `.pi/extensions/writing-humanizer.ts`). Install the package into your pi setup so pi discovers the bundled `skills/`.

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

去除文章中的 AI 寫作痕跡，使文字更自然、更有人味。以台灣正體中文為主。

一份 skill，七個 host。同一個 `skills/writing-humanizer` skill 可在 Claude Code、OpenAI Codex、Cursor、Google Antigravity CLI、OpenCode、Kimi CLI、pi 上運作——差別只在各 host 的 manifest。

## 安裝方式

### Claude Code

透過 Marketplace（推薦）：

```bash
/plugin marketplace add shyuan/shyuan-marketplace
/plugin install writing-humanizer@shyuan-marketplace
```

或直接安裝：

```bash
/plugin install shyuan/writing-humanizer
```

### OpenCode

在你的 `opencode.json`（全域或專案層級）的 `plugin` 陣列加入以下設定，然後重啟 OpenCode：

```json
{
  "plugin": ["writing-humanizer@git+https://github.com/shyuan/writing-humanizer.git"]
}
```

版本鎖定與排錯請見 [`.opencode/INSTALL.md`](.opencode/INSTALL.md)。

### Codex / Cursor / Antigravity CLI / Kimi CLI

這幾個 host 各自讀取 repo 內附的 manifest。用該 host 自己的 plugin／marketplace 安裝指令指向本 repo，或將 repo clone 到該 host 的 plugins 位置，讓它探索對應 manifest：

```bash
git clone https://github.com/shyuan/writing-humanizer.git
```

| Host | 讀取的 manifest |
|------|------|
| OpenAI Codex | `.codex-plugin/plugin.json` |
| Cursor | `.cursor-plugin/plugin.json` |
| Google Antigravity CLI | `plugin.json`（repo 根目錄） |
| Kimi CLI | `.kimi-plugin/plugin.json` |

### pi

pi 透過 `package.json` 的 `"pi"` 欄位載入 skill（extension 在 `.pi/extensions/writing-humanizer.ts`）。將此套件安裝進你的 pi 環境，pi 便會探索到內附的 `skills/`。

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
