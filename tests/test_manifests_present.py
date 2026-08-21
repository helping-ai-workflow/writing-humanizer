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
    """不只比對字串——路徑本身也要真的存在，否則刪掉目標檔案這條測試也會維持綠燈。"""
    codex_skills = _load(".codex-plugin/plugin.json")["skills"]
    assert codex_skills == "./skills/"
    assert (ROOT / "skills").is_dir(), (
        f".codex-plugin/plugin.json 的 skills 欄位指向 {codex_skills!r}，"
        "但 skills/ 目錄不存在")

    cursor_skills = _load(".cursor-plugin/plugin.json")["skills"]
    assert cursor_skills == "skills/"
    assert (ROOT / "skills").is_dir(), (
        f".cursor-plugin/plugin.json 的 skills 欄位指向 {cursor_skills!r}，"
        "但 skills/ 目錄不存在")

    kimi_skills = _load(".kimi-plugin/plugin.json")["skills"]
    assert kimi_skills == "./skills/"
    assert (ROOT / "skills").is_dir(), (
        f".kimi-plugin/plugin.json 的 skills 欄位指向 {kimi_skills!r}，"
        "但 skills/ 目錄不存在")

    root_skills = _load("plugin.json")["skills"]
    assert root_skills == ["skills/writing-humanizer"]
    assert (ROOT / "skills/writing-humanizer").is_dir(), (
        f"plugin.json 的 skills 欄位指向 {root_skills!r}，"
        "但 skills/writing-humanizer/ 目錄不存在")

    pkg = _load("package.json")
    assert pkg["main"] == ".opencode/plugins/writing-humanizer.js"
    assert (ROOT / pkg["main"]).is_file(), (
        f"package.json 的 main 欄位指向 {pkg['main']!r}，但檔案不存在"
        "（OpenCode 靠這個檔案載入 plugin）")

    pi_extensions = pkg["pi"]["extensions"]
    assert pi_extensions == ["./.pi/extensions/writing-humanizer.ts"]
    assert (ROOT / ".pi/extensions/writing-humanizer.ts").is_file(), (
        f"package.json 的 pi.extensions 欄位指向 {pi_extensions!r}，但檔案不存在"
        "（pi 靠這個 extension 註冊 skills 目錄）")

    pi_skills = pkg["pi"]["skills"]
    assert pi_skills == ["./skills"]
    assert (ROOT / "skills").is_dir(), (
        f"package.json 的 pi.skills 欄位指向 {pi_skills!r}，但 skills/ 目錄不存在")


def test_gemini_extension_points_at_an_existing_context_file():
    gem = _load("gemini-extension.json")
    assert gem["contextFileName"] == "GEMINI.md"
    assert (ROOT / "GEMINI.md").is_file(), (
        "gemini-extension.json 宣告了 GEMINI.md，但檔案不存在")


_FORK_URL = "https://github.com/helping-ai-workflow/writing-humanizer"
_FORK_OWNER = "helping-ai-workflow"


def test_no_manifest_still_points_at_the_upstream_repo():
    """fork 自帶 marketplace 之後，manifest 再指回上游會讓使用者以為裝到的是上游版。"""
    for rel in sorted(_NAME_MANIFESTS):
        raw = (ROOT / rel).read_text(encoding="utf-8")
        assert "shyuan" not in raw, (
            f"{rel} 仍帶有上游署名或 URL；LICENSE 以外的地方都該改指 {_FORK_OWNER}")


def test_every_ownership_field_names_the_fork():
    claude = _load(".claude-plugin/plugin.json")
    assert claude["author"]["name"] == _FORK_OWNER
    assert claude["repository"] == _FORK_URL

    codex = _load(".codex-plugin/plugin.json")
    assert codex["author"] == _FORK_OWNER, ".codex-plugin 的 author 是字串不是物件"
    assert codex["repository"] == _FORK_URL

    assert _load(".cursor-plugin/plugin.json")["author"]["name"] == _FORK_OWNER
    assert _load("plugin.json")["author"]["name"] == _FORK_OWNER
    assert _load("package.json")["repository"] == _FORK_URL

    kimi = _load(".kimi-plugin/plugin.json")
    assert kimi["author"]["name"] == _FORK_OWNER
    assert kimi["homepage"] == _FORK_URL
    assert kimi["interface"]["developerName"] == _FORK_OWNER
    assert kimi["interface"]["websiteURL"] == _FORK_URL


def test_license_keeps_the_upstream_copyright_and_adds_the_fork():
    text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert "Copyright (c) 2026 shyuan" in text, (
        "MIT 要求原始著作權聲明必須隨散佈保留，不可刪除")
    assert f"Copyright (c) 2026 {_FORK_OWNER}" in text, (
        "fork 的修改部分也要有自己的著作權行")
