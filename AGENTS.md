# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A cross-tool **plugin** (not an application). It ships a single user-invocable skill, `writing-humanizer`, that detects and rewrites AI-generated writing patterns, focused on Traditional Chinese (Taiwan). There is no build, lint, or runtime — the "code" is Markdown prompt content that the host (Claude Code, OpenAI Codex, Cursor, Google Antigravity CLI, OpenCode, Kimi CLI, pi, or Gemini CLI) loads as a skill. There is a pytest suite, but it tests no runtime behaviour (there is none) — it mechanically gates the things that would otherwise silently drift: that every manifest is present and parseable, that the version agrees across all eight manifests plus the CHANGELOG top heading, and that the pattern numbering stays aligned across the spoke files, `SKILL.md`, and both language sections of `README.md`. The skill's actual behaviour is still validated by reading it and exercising it, not by a toolchain.

The same `skills/` directory and `SKILL.md` format are shared by all hosts (Claude Code, OpenAI Codex, Cursor, Google Antigravity CLI, OpenCode, Kimi CLI, pi, Gemini CLI); only the manifest/loader differs per host.

## Repository layout

- `.claude-plugin/plugin.json` — Claude Code plugin manifest.
- `.claude-plugin/marketplace.json` — self-hosted single-plugin marketplace (`"source": "./"`). This repo IS its own marketplace; users add it directly with `claude plugin marketplace add`. The version lives here a second time, at `plugins[0].version` — it must match `plugin.json`.
- `.codex-plugin/plugin.json` — OpenAI Codex plugin manifest. Points at the shared skills dir via `"skills": "./skills/"`.
- `.cursor-plugin/plugin.json` — Cursor plugin manifest (Cursor 2.5+). Points at the shared skills dir via `"skills": "skills/"`.
- `plugin.json` (repo root) — Google Antigravity CLI plugin manifest. Antigravity expects this at the plugin root (not in a namespaced dir); `"skills"` is an array pointing at each skill dir (`["skills/writing-humanizer"]`).
- `package.json` + `.opencode/plugins/writing-humanizer.js` + `.opencode/INSTALL.md` — OpenCode loader. OpenCode does **not** read the top-level `skills/` dir; instead it installs this repo as a JS plugin (via the `plugin` array in the user's `opencode.json`, resolved through `package.json`'s `"main"`), and the plugin's `config` hook injects `skills/` into `config.skills.paths` so the skill is auto-discovered — no symlinks. See `.opencode/INSTALL.md`.
- `.kimi-plugin/plugin.json` — Kimi CLI plugin manifest. Points at the shared skills dir via `"skills": "./skills/"`, plus a Kimi-specific `interface` block for display metadata. (We omit Kimi's optional `sessionStart` so the skill loads on demand, and `skillInstructions` since the skill references no host-specific tools.)
- `.pi/extensions/writing-humanizer.ts` + the `"pi"` field in `package.json` — pi loader. Like OpenCode, pi does not read the top-level `skills/` dir on its own; the TS extension's `resources_discover` hook returns `skillPaths: [skillsDir]` to register the shared `skills/` dir. `package.json`'s `"pi"` field lists the extension and skills paths.
- `skills/writing-humanizer/SKILL.md` — the skill entry point (hub), used by all eight hosts. Its YAML frontmatter (`name`, `description`) drives triggering on all of them; Claude-specific keys (`user-invocable`, `argument-hint`, `allowed-tools`) are ignored by the others.
- `skills/writing-humanizer/references/` — spoke files loaded on demand by the hub.
- `gemini-extension.json` + `GEMINI.md` — Gemini CLI extension manifest and its context file. `GEMINI.md` deliberately does NOT `@`-import `SKILL.md`: this is an on-demand skill, not a session-wide contract, so inlining it would cost every Gemini session a full SKILL.md of context.
- `.version-bump.json` + `scripts/bump_version.py` — version sync across all eight manifests plus the CHANGELOG top heading. `--check` reports drift; `--audit` greps the tracked repo for an undeclared file carrying the version (a manifest someone forgot to declare).
- `CHANGELOG.md` — the narrative of what changed per version. Its top `## X.Y.Z` heading is load-bearing: `bump_version.py --check` and `tests/test_version_consistency.py` both read it as the source of truth.
- `tests/` — pytest ship-gates. No runtime code is tested here (there is none); the tests lock manifest completeness, version consistency, and the pattern-numbering invariant that this file documents below.
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

After editing skill content:

1. Add the new `## X.Y.Z` entry at the top of `CHANGELOG.md`.
2. Run `python scripts/bump_version.py X.Y.Z`. It writes all eight manifests and advances `.version-bump.json`'s `previous` / `current` / `next`, then re-audits.
3. Run `python -m pytest -q`. CI runs the same gates, so a manual edit that misses a manifest fails the build instead of shipping a split version.

Never hand-edit a version in a single manifest — that is the exact drift the script exists to prevent.
