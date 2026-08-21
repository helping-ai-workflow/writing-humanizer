"""Ship-gate：八份 manifest 與 CHANGELOG 頂層版本必須一致。

版本號同時活在 .claude-plugin/plugin.json 與 .claude-plugin/marketplace.json
兩處。這兩處一旦不同步，marketplace 列表顯示的版本會跟實際裝到的版本不一樣，
而且沒有任何執行期錯誤會提示。
"""
import json
import pathlib
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
_CHANGELOG_TOP = re.compile(r"^##\s*(\d+\.\d+\.\d+)", re.MULTILINE)


def _changelog_top():
    m = _CHANGELOG_TOP.search((ROOT / "CHANGELOG.md").read_text(encoding="utf-8"))
    assert m, "CHANGELOG.md 沒有 '## X.Y.Z' 標題"
    return m.group(1)


def _json_version(rel, accessor):
    return accessor(json.loads((ROOT / rel).read_text(encoding="utf-8")))


# rel_path -> 取出版本號的方式。與 .version-bump.json 的 files[] 一一對應。
_MANIFESTS = {
    ".claude-plugin/plugin.json": lambda: _json_version(".claude-plugin/plugin.json", lambda d: d["version"]),
    ".claude-plugin/marketplace.json": lambda: _json_version(".claude-plugin/marketplace.json", lambda d: d["plugins"][0]["version"]),
    ".codex-plugin/plugin.json": lambda: _json_version(".codex-plugin/plugin.json", lambda d: d["version"]),
    ".cursor-plugin/plugin.json": lambda: _json_version(".cursor-plugin/plugin.json", lambda d: d["version"]),
    ".kimi-plugin/plugin.json": lambda: _json_version(".kimi-plugin/plugin.json", lambda d: d["version"]),
    "plugin.json": lambda: _json_version("plugin.json", lambda d: d["version"]),
    "package.json": lambda: _json_version("package.json", lambda d: d["version"]),
    "gemini-extension.json": lambda: _json_version("gemini-extension.json", lambda d: d["version"]),
}


@pytest.mark.parametrize("rel_path,getter", sorted(_MANIFESTS.items()))
def test_manifest_version_matches_changelog_top(rel_path, getter):
    assert (ROOT / rel_path).is_file(), f"帶版本的 manifest 不存在：{rel_path}"
    version = getter()
    top = _changelog_top()
    assert version == top, (
        f"{rel_path} 宣告 {version!r}，但 CHANGELOG 頂層是 {top!r}；"
        f"跑 `python scripts/bump_version.py {top}` 重新同步。")


def test_version_bump_config_declares_every_manifest():
    """.version-bump.json 的 files[] 必須涵蓋本檔測到的每一份 manifest。

    漏宣告一份，bump() 就永遠不會寫它，而它會靜靜停在舊版本。
    """
    cfg = json.loads((ROOT / ".version-bump.json").read_text(encoding="utf-8"))
    declared = {e["path"] for e in cfg["files"]}
    missing = set(_MANIFESTS) - declared
    assert not missing, f".version-bump.json 漏宣告：{sorted(missing)}"


def test_version_bump_config_carries_previous():
    """`previous` 一旦不見，--audit 的過期 manifest 掃描會靜默跳過。

    bump_version.py 在缺 `previous` 時只印一行 'Stale-manifest scan SKIPPED'
    就照樣回 0，整套測試仍然全綠——這個掃描等於被無聲關掉。
    """
    cfg = json.loads((ROOT / ".version-bump.json").read_text(encoding="utf-8"))
    assert "previous" in cfg, (
        ".version-bump.json 沒有 `previous` 欄位——過期 manifest 掃描被無聲跳過")
    assert re.fullmatch(r"\d+\.\d+\.\d+", cfg["previous"] or ""), (
        f"`previous` 不是純 X.Y.Z：{cfg.get('previous')!r}")
    assert cfg["previous"] != cfg["current"], (
        "`previous` 不可等於 `current`")
    assert cfg.get("current") == _changelog_top(), (
        f".version-bump.json 的 `current` 是 {cfg.get('current')!r}，"
        f"但 CHANGELOG 頂層是 {_changelog_top()!r}")
