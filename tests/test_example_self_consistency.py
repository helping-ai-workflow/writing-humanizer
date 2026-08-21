"""Ship-gate：skill 自己的「改寫後」範例不得違反 skill 自己的絕對禁令。

「改寫後」區塊是這份 skill 對「正確輸出」的示範。示範一旦牴觸規則，模型讀到的就是
互相矛盾的指令——而這種矛盾不會有任何錯誤訊息，只會讓輸出默默變差。v1.4.0 的審查
就抓到過這一類：模式 13 當時禁止一切破折號，卻有三個「改寫後」範例自己在用。

刻意不檢查破折號：模式 13 的判準已改成密度（同一段落 2 個以上才觸發），單一破折號
是道地中文，列進來會誤殺——那正是這一版要修掉的毛病，不該用測試把它固化回來。
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
REFS = ROOT / "skills" / "writing-humanizer" / "references"

_AFTER = "**改寫後：**"

# 絕對禁令：skill 對這些沒有任何例外條款，出現在「正確示範」裡就是自相矛盾。
_BANNED = [
    (re.compile(r"[\U0001F300-\U0001FAFF☀-➿⬀-⯿]"),
     "裝飾性 emoji（模式 16）"),
    (re.compile(r"不僅.{0,20}?(更是|而且|還是)"),
     "「不僅……更是……」否定式排比（鐵律／模式 9）"),
    (re.compile(r"\*\*[^*\n]+\*\*"),
     "散文內粗體（模式 14／28）"),
    (re.compile(r"此外"), "AI 高頻詞「此外」（模式 7）"),
    (re.compile(r"值得注意的是"), "AI 句式「值得注意的是」（模式 24）"),
    (re.compile(r"在當今"), "AI 句式「在當今……的時代」（zh-tw-slop-list）"),
]


def _rewrite_blocks():
    """回傳 [(檔名, 該檔第幾個「改寫後」, 區塊文字)]。

    區塊 = 「改寫後：」之後、跳過空行、連續以 `>` 開頭的引用行。
    """
    out = []
    for path in sorted(REFS.glob("*.md")):
        lines = path.read_text(encoding="utf-8").splitlines()
        count = 0
        for i, line in enumerate(lines):
            if line.strip() != _AFTER:
                continue
            count += 1
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            block = []
            while j < len(lines) and lines[j].startswith(">"):
                block.append(lines[j].lstrip("> "))
                j += 1
            out.append((path.name, count, "\n".join(block)))
    return out


def test_rewrite_examples_are_discovered():
    """先確認掃描器真的抓到東西。

    抓到 0 個會讓下面的檢查空轉成假綠。用下限而不是精確數字：新增模式是正常演進，
    不該每加一條就改測試；但數量掉到 25 以下代表解析壞了，不是有人刪了範例。
    """
    blocks = _rewrite_blocks()
    assert len(blocks) >= 25, f"只掃到 {len(blocks)} 個「改寫後」區塊，解析可能壞了"
    empty = [f"{n} 第 {i} 個" for n, i, t in blocks if not t.strip()]
    assert not empty, "這些「改寫後：」後面接不到引用區塊：" + "、".join(empty)


_EM_DASH = re.compile(r"——")


def test_no_rewrite_example_exceeds_the_dash_density_threshold():
    """模式 13 的門檻是「同一段落兩個以上」。正確示範不該自己超標。

    這條刻意跟 _BANNED 分開：破折號不是絕對禁令，單一個是道地中文。把它塞進
    _BANNED 會誤殺 v1.5.0 剛解禁的合法用法，等於用測試把舊 bug 固化回來。
    這裡要的是計數，不是存在性。
    """
    failures = []
    for name, idx, text in _rewrite_blocks():
        count = len(_EM_DASH.findall(text))
        if count > 1:
            failures.append(
                f"{name} 第 {idx} 個「改寫後」有 {count} 個破折號，超過模式 13 的門檻")
    assert not failures, (
        "「改寫後」範例的破折號密度超過模式 13 自己的門檻：\n" + "\n".join(failures))


def test_no_rewrite_example_violates_an_absolute_rule():
    failures = []
    for name, idx, text in _rewrite_blocks():
        for pattern, label in _BANNED:
            found = pattern.search(text)
            if found:
                failures.append(
                    f"{name} 第 {idx} 個「改寫後」含{label}：{found.group(0)!r}")
    assert not failures, (
        "「改寫後」範例違反 skill 自己的絕對禁令——示範與規則牴觸，"
        "模型會讀到互相矛盾的指令：\n" + "\n".join(failures))
