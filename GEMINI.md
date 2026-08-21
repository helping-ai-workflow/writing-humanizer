# Writing Humanizer（Gemini context）

這個 extension 提供 `writing-humanizer` skill：偵測並改寫 AI 生成文本的痕跡，
以台灣正體中文為主，共 31 類模式。

這是**按需載入**的 skill，不是每個 session 都要套用的規則。當使用者要求「去 AI 味」、
「人性化」、「改寫得更自然」、「潤稿」、「改得像人寫的」，或提供一段明顯由 AI 生成的
中文內容時，讀本 extension 目錄下的 `skills/writing-humanizer/SKILL.md`（通常位於
`~/.gemini/extensions/writing-humanizer/`）並照它執行。

SKILL.md 是 hub，只有鐵律、理性化陷阱表、兩輪流程與評分標準。實際的模式目錄在同一個
extension 目錄下的 `skills/writing-humanizer/references/`，依 SKILL.md 的指示按需載入。

## Gemini 工具對應

- 讀檔 -> `read_file`；寫檔 -> `write_file`；找檔 -> `glob`。
- skill 的 `allowed-tools`（Read / Edit / Write / Glob）在 Gemini 對應上述三個工具。
- 這個 skill 不需要網路存取。
