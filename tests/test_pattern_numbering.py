"""Ship-gate：模式編號 1-31 在 spoke／SKILL.md／README 三處必須對齊。

AGENTS.md 規定新增或重編模式要同時改三個地方。這條規則原本純靠人工遵守，
漏改一處不會有任何錯誤——只會讓使用者看到的模式清單與 skill 實際掃描的
範圍對不上。本檔把它變成 CI 會擋的機械檢查。
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
REFS = ROOT / "skills" / "writing-humanizer" / "references"
SKILL = ROOT / "skills" / "writing-humanizer" / "SKILL.md"
README = ROOT / "README.md"
KIMI = ROOT / ".kimi-plugin" / "plugin.json"
GEMINI = ROOT / "GEMINI.md"

# spoke 檔頭：# 內容模式（模式 1-6）
_SPOKE_HEADER = re.compile(r"^#\s.*（模式\s*(\d+)-(\d+)）", re.MULTILINE)
# spoke 內文：## 模式 1：過度強調意義
_SPOKE_PATTERN = re.compile(r"^##\s*模式\s*(\d+)[：:]", re.MULTILINE)
# SKILL.md：- **內容模式（模式 1-6）** — … [x](references/content-patterns.md)
_SKILL_REF = re.compile(r"（模式\s*(\d+)-(\d+)）.*\(references/([a-z0-9-]+\.md)\)")
# README 英文段：**Content Patterns (1-6)**
_README_EN = re.compile(r"\*\*[^*]+ Patterns \((\d+)-(\d+)\)\*\*")
# README 中文段：**內容模式（1-6）**
_README_ZH = re.compile(r"\*\*[^*]+（(\d+)-(\d+)）\*\*")


def _spokes():
    """{檔名: (檔頭宣告的範圍, 實際出現的模式編號 list)}，只收有宣告範圍的 spoke。"""
    out = {}
    for path in sorted(REFS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        header = _SPOKE_HEADER.search(text)
        if not header:
            continue  # zh-tw-slop-list.md 是詞彙表，沒有編號模式
        declared = (int(header.group(1)), int(header.group(2)))
        actual = [int(n) for n in _SPOKE_PATTERN.findall(text)]
        out[path.name] = (declared, actual)
    return out


def test_spokes_are_discovered():
    """先確認掃描器真的抓到東西——空 dict 會讓後面每個測試都空轉變成假綠。"""
    spokes = _spokes()
    assert len(spokes) == 5, f"預期 5 個帶編號的 spoke，實際掃到 {sorted(spokes)}"


def test_each_spoke_header_matches_its_own_headings():
    for name, (declared, actual) in _spokes().items():
        assert actual, f"{name} 檔頭宣告了範圍卻沒有任何 '## 模式 N' 標題"
        assert len(actual) == len(set(actual)), f"{name} 有重複的模式編號：{actual}"
        assert actual == sorted(actual), f"{name} 的模式編號沒有遞增：{actual}"
        assert declared == (actual[0], actual[-1]), (
            f"{name} 檔頭宣告 {declared[0]}-{declared[1]}，"
            f"實際是 {actual[0]}-{actual[-1]}")


def test_all_spokes_together_cover_one_to_max_contiguously():
    everything = [n for _, actual in _spokes().values() for n in actual]
    assert len(everything) == len(set(everything)), (
        f"跨檔重複的模式編號：{sorted(n for n in everything if everything.count(n) > 1)}")
    assert sorted(everything) == list(range(1, max(everything) + 1)), (
        f"模式編號不連續，缺號：{sorted(set(range(1, max(everything) + 1)) - set(everything))}")


def test_skill_hub_reference_list_matches_the_spokes():
    text = SKILL.read_text(encoding="utf-8")
    found = {fname: (int(lo), int(hi)) for lo, hi, fname in _SKILL_REF.findall(text)}
    for name, (declared, _) in _spokes().items():
        assert name in found, f"SKILL.md 的參考清單沒有列出 {name}"
        assert found[name] == declared, (
            f"SKILL.md 說 {name} 是 {found[name][0]}-{found[name][1]}，"
            f"但該檔實際是 {declared[0]}-{declared[1]}")


def test_readme_both_language_sections_match_the_spokes():
    text = README.read_text(encoding="utf-8")
    expected = {declared for declared, _ in _spokes().values()}
    en = {(int(lo), int(hi)) for lo, hi in _README_EN.findall(text)}
    zh = {(int(lo), int(hi)) for lo, hi in _README_ZH.findall(text)}
    assert en == expected, f"README 英文段的範圍 {sorted(en)} 對不上 spoke {sorted(expected)}"
    assert zh == expected, f"README 中文段的範圍 {sorted(zh)} 對不上 spoke {sorted(expected)}"


def test_every_declared_total_equals_the_highest_pattern_number():
    """總數宣告散在三個檔。改了模式數量卻漏改其中一處，使用者看到的數字就是錯的。"""
    highest = max(n for _, actual in _spokes().values() for n in actual)
    readme = README.read_text(encoding="utf-8")
    kimi = json.loads(KIMI.read_text(encoding="utf-8"))["interface"]["longDescription"]
    gemini = GEMINI.read_text(encoding="utf-8")

    claims = {
        "README 英文段": re.search(r"(\d+) categories of AI writing patterns", readme),
        "README 中文段": re.search(r"(\d+) 類 AI 寫作模式", readme),
        "kimi longDescription": re.search(r"(\d+) 類 AI 生成文本的破綻", kimi),
        "GEMINI.md": re.search(r"共\s*(\d+)\s*類模式", gemini),
    }
    for where, m in claims.items():
        assert m, f"{where} 找不到模式總數的宣告句"
        assert int(m.group(1)) == highest, (
            f"{where} 宣告 {m.group(1)} 類，但實際最大模式編號是 {highest}")
