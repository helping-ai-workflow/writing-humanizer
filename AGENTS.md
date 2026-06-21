# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A cross-tool **plugin** (not an application). It ships a single user-invocable skill, `writing-humanizer`, that detects and rewrites AI-generated writing patterns, focused on Traditional Chinese (Taiwan). There is no build, lint, test, or runtime — the "code" is Markdown prompt content that the host (Claude Code, OpenAI Codex, Cursor, Google Antigravity CLI, OpenCode, Kimi CLI, or pi) loads as a skill. Changes are validated by reading them and by exercising the skill, not by a toolchain.

The same `skills/` directory and `SKILL.md` format are shared by all hosts (Claude Code, OpenAI Codex, Cursor, Google Antigravity CLI, OpenCode, Kimi CLI, pi); only the manifest/loader differs per host.

## Repository layout

- `.claude-plugin/plugin.json` — Claude Code plugin manifest. Distributed via the `shyuan-marketplace`.
- `.codex-plugin/plugin.json` — OpenAI Codex plugin manifest. Points at the shared skills dir via `"skills": "./skills/"`.
- `.cursor-plugin/plugin.json` — Cursor plugin manifest (Cursor 2.5+). Points at the shared skills dir via `"skills": "skills/"`.
- `plugin.json` (repo root) — Google Antigravity CLI plugin manifest. Antigravity expects this at the plugin root (not in a namespaced dir); `"skills"` is an array pointing at each skill dir (`["skills/writing-humanizer"]`).
- `package.json` + `.opencode/plugins/writing-humanizer.js` + `.opencode/INSTALL.md` — OpenCode loader. OpenCode does **not** read the top-level `skills/` dir; instead it installs this repo as a JS plugin (via the `plugin` array in the user's `opencode.json`, resolved through `package.json`'s `"main"`), and the plugin's `config` hook injects `skills/` into `config.skills.paths` so the skill is auto-discovered — no symlinks. See `.opencode/INSTALL.md`.
- `.kimi-plugin/plugin.json` — Kimi CLI plugin manifest. Points at the shared skills dir via `"skills": "./skills/"`, plus a Kimi-specific `interface` block for display metadata. (We omit Kimi's optional `sessionStart` so the skill loads on demand, and `skillInstructions` since the skill references no host-specific tools.)
- `.pi/extensions/writing-humanizer.ts` + the `"pi"` field in `package.json` — pi loader. Like OpenCode, pi does not read the top-level `skills/` dir on its own; the TS extension's `resources_discover` hook returns `skillPaths: [skillsDir]` to register the shared `skills/` dir. `package.json`'s `"pi"` field lists the extension and skills paths.
- `skills/writing-humanizer/SKILL.md` — the skill entry point (hub), used by all seven hosts. Its YAML frontmatter (`name`, `description`) drives triggering on all of them; Claude-specific keys (`user-invocable`, `argument-hint`, `allowed-tools`) are ignored by the others.
- `skills/writing-humanizer/references/` — spoke files loaded on demand by the hub.
- `README.md` — bilingual (English + 中文) user-facing docs, kept in sync with the pattern catalog.

## Architecture: hub-and-spoke skill

`SKILL.md` is a deliberately concise **hub**. It holds the always-loaded essentials — iron rules (鐵律), the rationalization-trap table (理性化陷阱), red-flag self-checks, the two-pass process, the final checklist, and the scoring rubric — then links out to detailed pattern catalogs. Keep the hub short; push detail into spokes.

The spokes catalog AI patterns in **numbered categories (1–31)**, partitioned by file. The numbering is contiguous across files and must stay consistent with both `SKILL.md`'s reference section and `README.md`:

- `content-patterns.md` — patterns 1–6 (significance inflation, promotional language, vague attribution…)
- `language-patterns.md` — patterns 7–12 (AI vocabulary, copula avoidance, negative parallelism, rule of three…)
- `style-patterns.md` — patterns 13–17 (em dash overuse, boldface, emoji, quotation marks…)
- `communication-patterns.md` — patterns 18–24 (filler phrases, hedging, sycophancy, throat-clearing…)
- `structure-rhetoric-patterns.md` — patterns 25–31, Chinese-essay-specific (outline-as-essay, 4-char-label lists, significance-stamping endings, sublimating/moralizing conclusions…)
- `zh-tw-slop-list.md` — the AI vocabulary watchlist with Traditional Chinese replacements.

## Conventions when editing

- **Adding or renumbering a pattern** touches three places that must agree: the relevant `references/*.md` spoke, the reference list in `SKILL.md`, and the pattern summary in `README.md` (both language sections). Patterns are append-only at the end of their category range to avoid renumbering churn.
- Keep `SKILL.md` lean. New rules go in spokes; only promote something to the hub if it must be active on every invocation.
- All prose, examples, comments, and commit messages are written in **台灣正體中文** with full orthographic correctness, matching the skill's own domain.
- The skill's philosophy is prescriptive and absolute by design (the 鐵律 / "no exceptions" framing). When editing rule text, preserve that uncompromising tone — softening it weakens the skill.

## Publishing changes

After editing skill content: bump the `version` in **all six** manifests — `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `.cursor-plugin/plugin.json`, `plugin.json`, `package.json`, and `.kimi-plugin/plugin.json` (keep them in sync) — then update `README.md` if the pattern catalog or feature list changed.
