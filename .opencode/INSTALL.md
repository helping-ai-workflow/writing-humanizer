# Installing Writing Humanizer for OpenCode

## Prerequisites

- [OpenCode.ai](https://opencode.ai) installed

## Installation

Add the plugin to the `plugin` array in your `opencode.json` (global or project-level):

```json
{
  "plugin": ["writing-humanizer@git+https://github.com/shyuan/writing-humanizer.git"]
}
```

Restart OpenCode. The plugin installs through OpenCode's plugin manager and
registers the shared `skills/` directory, so the `writing-humanizer` skill is
discovered without any symlinks or manual `skills.paths` edits.

To pin a specific version:

```json
{
  "plugin": ["writing-humanizer@git+https://github.com/shyuan/writing-humanizer.git#v1.2.0"]
}
```

OpenCode uses its own plugin install. If you also use Claude Code, Codex,
Cursor, or Antigravity, install the plugin separately for each one.

## Usage

Use OpenCode's native `skill` tool:

```
use skill tool to list skills
use skill tool to load writing-humanizer
```

Or simply ask OpenCode to humanize a piece of text — the skill is discovered
from its `description` and loaded on demand.

## Troubleshooting

### Plugin not loading

1. Check logs: `opencode run --print-logs "hello" 2>&1 | grep -i writing-humanizer`
2. Verify the plugin line in your `opencode.json`
3. Make sure you're running a recent version of OpenCode

### Skill not found

1. Use the `skill` tool to list what's discovered
2. Confirm the plugin is loading (see above) — it injects this repo's `skills/`
   directory into `config.skills.paths`
