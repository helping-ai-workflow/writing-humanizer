# Changelog

## 1.4.0

- 新增自託管 marketplace（`.claude-plugin/marketplace.json`，`source: "./"`），
  可用 `claude plugin marketplace add` 直接指向本 repo 安裝。
- 新增第八個 host：Gemini CLI（`gemini-extension.json` + `GEMINI.md`）。
- 新增 `scripts/bump_version.py` 與 `.version-bump.json`，八份 manifest 加
  CHANGELOG 的版本一次同步，`--audit` 會抓出漏宣告的 manifest。
- 新增 pytest 與 GitHub Actions CI：鎖版本一致性、manifest 完整性、
  模式編號 1-31 在 spoke／SKILL.md／README 三處對齊。
- 署名與 repository URL 改指 `helping-ai-workflow`；LICENSE 保留上游
  `shyuan` 的原始著作權聲明並加註 fork 修改。

## 1.3.0

- 新增 Codex、Cursor、Antigravity CLI、OpenCode、Kimi CLI、pi 六個 host 的
  manifest 與 loader，README 改寫為七個 host 的安裝說明。

## 1.2.0

- 新增中文論說文專屬的結構與修辭模式 25-31（大綱骨架、四字標籤清單、
  意義蓋章收尾、句內粗體、元論述、升華結尾、抽象事物具象成路線）。
- 新增 `AGENTS.md` 記錄 repo 慣例，`CLAUDE.md` 以 `@AGENTS.md` 匯入。

## 1.1.0

- `SKILL.md` 重構為精簡 hub，模式細節下放至 `references/` spoke 檔。

## 1.0.0

- 首版：hub-and-spoke skill 架構、雙語 README、MIT LICENSE。
