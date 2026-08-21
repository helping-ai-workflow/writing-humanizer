"""Ship-gate：每個 host 的 manifest 都在、可解析、名稱一致。

八個 host 各自只讀自己的 manifest。少一份、名稱打錯，或 marketplace 宣告的
plugin 名稱與 plugin.json 對不上，使用者會在安裝當下才撞到，而且沒有任何
執行期錯誤會提示。
"""
import json
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent

# rel_path -> 從解析後的 dict 取出 plugin 名稱的方式
_NAME_MANIFESTS = {
    ".claude-plugin/plugin.json": lambda d: d["name"],
    ".claude-plugin/marketplace.json": lambda d: d["plugins"][0]["name"],
    ".codex-plugin/plugin.json": lambda d: d["name"],
    ".cursor-plugin/plugin.json": lambda d: d["name"],
    ".kimi-plugin/plugin.json": lambda d: d["name"],
    "gemini-extension.json": lambda d: d["name"],
    "plugin.json": lambda d: d["name"],
    "package.json": lambda d: d["name"],
}


def _load(rel):
    path = ROOT / rel
    assert path.is_file(), f"manifest 不存在：{rel}"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("rel", sorted(_NAME_MANIFESTS))
def test_manifest_parses_and_names_writing_humanizer(rel):
    data = _load(rel)
    assert _NAME_MANIFESTS[rel](data) == "writing-humanizer", (
        f"{rel} 宣告的名稱不是 writing-humanizer")


def test_marketplace_is_self_hosted_single_plugin():
    mp = _load(".claude-plugin/marketplace.json")
    assert mp["name"] == "writing-humanizer"
    assert len(mp["plugins"]) == 1, "本 marketplace 只託管這一個 plugin"
    assert mp["plugins"][0]["source"] == "./", (
        "source 必須是 './' — 自託管 marketplace 與 plugin 同一個 repo")


def test_every_host_manifest_wires_the_shared_skills_dir():
    assert _load(".codex-plugin/plugin.json")["skills"] == "./skills/"
    assert _load(".cursor-plugin/plugin.json")["skills"] == "skills/"
    assert _load(".kimi-plugin/plugin.json")["skills"] == "./skills/"
    assert _load("plugin.json")["skills"] == ["skills/writing-humanizer"]
    pkg = _load("package.json")
    assert pkg["main"] == ".opencode/plugins/writing-humanizer.js"
    assert pkg["pi"]["extensions"] == ["./.pi/extensions/writing-humanizer.ts"]
    assert pkg["pi"]["skills"] == ["./skills"]


def test_gemini_extension_points_at_an_existing_context_file():
    gem = _load("gemini-extension.json")
    assert gem["contextFileName"] == "GEMINI.md"
    assert (ROOT / "GEMINI.md").is_file(), (
        "gemini-extension.json 宣告了 GEMINI.md，但檔案不存在")
