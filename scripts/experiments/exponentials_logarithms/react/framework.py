# -*- coding: utf-8 -*-
"""
Shared helpers for the per type modules `dang_Dxx.py` (version 2 of the ReAct +
Calculator pipeline, used for the types that Qwen3-4B zero-shot does not solve
completely).

A type module provides:
  MA_DANG, FREE_UNKNOWNS
  PART_HUONGGIAI, PART_NHIEMVU     model facing text (English)
  EXAMPLE_QUESTION, EXAMPLE_ANSWER the worked example (not one of the 90 questions)
  EXAMPLE_THOUGHTS                 one Thought per command of program(EXAMPLE_QUESTION)
  program(question_text) -> list of Calculator commands; the last one stores `answer`
  OPTION_STYLE                     "exact" (Eq) or "numeric" (tolerance)  [default "exact"]
  option_expressions(question)     optional override: {letter: calculator text of the option}

Everything the notebook does with the model is therefore also done here without
a model: the commands are replayed on the 90 questions (and on the source
question) and the matched letter must equal the stored key.
"""
import re

OPTION_LINE = re.compile(r"(?m)^([A-D])\.\s*(.*?)\s*$")


# ---------------------------------------------------------------------------
# LaTeX -> Calculator text
# ---------------------------------------------------------------------------
def _match_brace(s, i):
    """s[i] == '{' -> index of the matching '}'."""
    depth = 0
    for j in range(i, len(s)):
        if s[j] == "{":
            depth += 1
        elif s[j] == "}":
            depth -= 1
            if depth == 0:
                return j
    raise ValueError(f"unbalanced braces in {s!r}")


def latex_to_calc(s):
    """Convert the small LaTeX subset used in the options into Calculator syntax."""
    s = s.strip().strip("$").strip()
    s = s.rstrip(".").strip()
    s = s.replace("\\left", "").replace("\\right", "").replace("\\,", "").replace("\\ ", " ")
    s = s.replace("\\cdot", "*").replace("\\times", "*")
    changed = True
    while changed:
        changed = False
        for cmd in ("\\dfrac", "\\frac"):
            k = s.find(cmd)
            if k >= 0:
                i = k + len(cmd)
                j = _match_brace(s, i)
                num = s[i + 1:j]
                assert s[j + 1] == "{", s
                l = _match_brace(s, j + 1)
                den = s[j + 2:l]
                atom = r"-?\d+|[A-Za-z]|\\sqrt\{\d+\}|log\(\d+\)"
                num_t = num.strip() if re.fullmatch(atom, num.strip()) else f"({num})"
                den_t = den.strip() if re.fullmatch(atom, den.strip()) else f"({den})"
                prev = s[:k].rstrip()[-1:]
                nxt = s[l + 1:].lstrip()[:1]
                frac = f"{num_t}/{den_t}"
                if prev in ("*", "/", "^") or nxt in ("^", "/"):
                    frac = f"({frac})"
                s = s[:k] + frac + s[l + 1:]
                changed = True
                break
        if changed:
            continue
        k = s.find("\\sqrt")
        if k >= 0:
            i = k + len("\\sqrt")
            if s[i] == "[":
                e = s.index("]", i)
                root = s[i + 1:e]
                j = _match_brace(s, e + 1)
                s = s[:k] + f"(({s[e + 2:j]})**(1/({root})))" + s[j + 1:]
            else:
                j = _match_brace(s, i)
                s = s[:k] + f"sqrt({s[i + 1:j]})" + s[j + 1:]
            changed = True
    s = s.replace("\\pi", "pi").replace("\\ln", "log").replace("\\infty", "oo")
    s = re.sub(r"\^\{([^{}]*)\}", r"**(\1)", s)
    s = s.replace("^", "**").replace("{", "(").replace("}", ")")
    # implicit multiplication: 2sqrt(3), 3(…), )(, digit followed by letter
    s = re.sub(r"(\d)\s*(sqrt|\()", r"\1*\2", s)
    s = re.sub(r"\)\s*(\(|sqrt|\d|[a-zA-Z])", r")*\1", s)
    s = re.sub(r"(\d)\s*([a-zA-Z])", r"\1*\2", s)
    return re.sub(r"\s+", "", s)


def parse_options(question_text):
    """{letter: raw text of the option} (the part after 'A.' etc., '$' and final '.' removed)."""
    out = {}
    for letter, body in OPTION_LINE.findall(question_text):
        body = body.strip()
        if body.endswith("."):
            body = body[:-1].strip()
        body = body.replace("$", "").strip()
        out[letter] = body
    assert sorted(out) == list("ABCD"), (sorted(out), question_text[-200:])
    return out


SYMBOL_PREFIX = re.compile(r"^\s*[A-Za-z](?:_\{?\\?[A-Za-z]+\}?)?\s*=\s*")


def strip_symbol_prefix(body):
    """A simple symbol on the left of '=' is dropped: 'x=7/2' -> '7/2', 'P_{min}=3' -> '3'."""
    return SYMBOL_PREFIX.sub("", body, count=1)


def default_option_expressions(question_text):
    out = {}
    for k, v in parse_options(question_text).items():
        # "Vô số" (infinitely many) only appears in the source questions; it is never the key here
        out[k] = "oo" if re.search(r"V[ôo]\s*s[ốo]", v) else latex_to_calc(strip_symbol_prefix(v))
    return out


# ---------------------------------------------------------------------------
# option tests
# ---------------------------------------------------------------------------
def test_command(letter, expr, style):
    if style == "exact":
        return f"test_{letter} = Eq(answer, {expr})"
    if style == "boolean":                 # the option text already is a True/False condition on `answer`
        return f"test_{letter} = {expr}"
    return f"test_{letter} = Abs(answer - ({expr})) < 10**(-9)"


def split_top_level(text, sep=";"):
    """Split on `sep` outside braces and parentheses."""
    parts, depth, cur = [], 0, ""
    for ch in text:
        if ch in "{(":
            depth += 1
        elif ch in "})":
            depth -= 1
        if ch == sep and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    parts.append(cur)
    return parts


def parse_interval(body):
    """'\\left[\\dfrac{5}{2};3\\right)' -> ('[', '5/2', '3', ')'). Ends may be infinity."""
    s = body.replace("\\left", "").replace("\\right", "").strip()
    left, right = s[0], s[-1]
    assert left in "[(" and right in ")]", body
    lo_text, hi_text = split_top_level(s[1:-1])

    def conv(t):
        t = t.strip()
        if "infty" in t:
            return "-oo" if t.startswith("-") else "oo"
        return latex_to_calc(t)

    return left, conv(lo_text), conv(hi_text), right


def interval_condition(body, var="answer"):
    """Calculator condition: the value `var` belongs to the interval written in the option."""
    left, lo, hi, right = parse_interval(body)
    parts = []
    if lo != "-oo":
        parts.append(f"{lo} {'<=' if left == '[' else '<'} {var}")
    if hi != "oo":
        parts.append(f"{var} {'<=' if right == ']' else '<'} {hi}")
    return parts[0] if len(parts) == 1 else f"And({', '.join(parts)})"


def interval_constructor(body):
    """The option '[a;b)' as a Calculator interval: [a;b] -> Interval(a, b), (a;b) -> Interval.open(a, b),
    [a;b) -> Interval.Ropen(a, b), (a;b] -> Interval.Lopen(a, b)."""
    left, lo, hi, right = parse_interval(body)
    name = {("[", "]"): "Interval", ("(", ")"): "Interval.open",
            ("[", ")"): "Interval.Ropen", ("(", "]"): "Interval.Lopen"}[(left, right)]
    return f"{name}({lo}, {hi})"


INTERVAL_NOTE = (
    "Each option is an interval, so write it as a Calculator interval according to its brackets, left bracket first: "
    "`[a; b]` is `Interval(a, b)`, `(a; b)` is `Interval.open(a, b)`, `[a; b)` is `Interval.Ropen(a, b)` and "
    "`(a; b]` is `Interval.Lopen(a, b)`; write $+\\infty$ as `oo` and $-\\infty$ as `-oo`, and each end in Calculator syntax. "
    "For example `[-14; -13)` becomes `option_a = Interval.Ropen(-14, -13)`. ")


def full_program(dang, question_text):
    """Commands: [optional: the four options stored first] + the method + the four option tests.

    With dang.OPTION_VARIABLES the options are stored as option_a ... option_d BEFORE anything is computed
    (the model copies them while it cannot yet be influenced by the result), and each test compares the
    result with the stored option."""
    cmds = list(dang.program(question_text))
    style = getattr(dang, "OPTION_STYLE", "exact")
    getter = getattr(dang, "option_expressions", default_option_expressions)
    opts = getter(question_text)
    if getattr(dang, "OPTION_VARIABLES", False):
        stores = [f"option_{k.lower()} = {opts[k]}" for k in "ABCD"]
        tests = [test_command(k, f"option_{k.lower()}", style) for k in "ABCD"]
        return stores + cmds + tests
    return cmds + [test_command(k, opts[k], style) for k in "ABCD"]


def display_options(dang, question_text):
    """[(letter, shown as written in the problem, Calculator text)] for the worked example."""
    getter = getattr(dang, "option_expressions", default_option_expressions)
    raw = parse_options(question_text)
    calc = getter(question_text)
    return [(k, raw[k], calc[k]) for k in "ABCD"]


# ---------------------------------------------------------------------------
# standard PART_NHIEMVU
# ---------------------------------------------------------------------------
def make_nhiemvu(steps, style="exact", extra_option_note="", option_variables=False, merge_reading=False):
    """steps: list of strings, one per method step (the option steps are added here).

    option_variables=True: the first method step reads the problem; then comes a step that stores the four
    options as option_a ... option_d; the last step tests the result against them."""
    if style == "exact":
        test_form = "`test_A = Eq(answer, <option A>)`"
    elif style == "boolean":
        test_form = "`test_A = <condition that option A is correct>`"
    else:
        test_form = "`test_A = Abs(answer - (<option A>)) < 10**(-9)`"
    lines = ["", "**PART 4: YOUR TURN**", "",
             "Open a `<think>` tag as the very first thing you write, and close it with `</think>`. Think in English inside the tags. "
             "Work through the method of PART 2, and use a Calculator call for every computation; never compute anything yourself:", ""]
    if option_variables:
        store = (
            "Before computing anything, store the four options exactly as they are written in the problem, in the order A, B, C, D, "
            "one command each: `option_a = <value of option A>`, then `option_b = ...`, `option_c = ...`, `option_d = ...`. "
            "Keep the order of the problem (do not sort the options) and write each value in Calculator syntax "
            "(a fraction `\\dfrac{p}{q}` becomes `p/q`, `\\sqrt{n}` becomes `sqrt(n)`, a power `u^{k}` becomes `u**k`; "
            "a negative number keeps its minus sign). " + extra_option_note)
        if merge_reading:
            # order: the four options first, then the reading, written at the start of the Thought of the first
            # command of the method (so every Thought ends with an Action)
            read_rule = (" Write every number digit by digit as you copy it (for example 1200 is 1, 2, 0, 0), keep its sign, "
                         "and say where in the problem you found it. Put this reading at the start of the Thought of the next "
                         "command, the first command of the method.")
            steps = [store.strip(), steps[0] + read_rule] + list(steps[1:])
        else:
            read_rule = (" Write every number digit by digit as you copy it (for example 1200 is 1, 2, 0, 0), keep its sign, "
                         "and say where in the problem you found it. Do this in a Thought of its own, before the first Action.")
            steps = [steps[0] + read_rule, store.strip()] + list(steps[1:])
        for i, st in enumerate(steps, 1):
            lines.append(f"[Step {i}] {st}")
        n = len(steps) + 1
        if style == "exact":
            tests = "`test_A = Eq(answer, option_a)`, then `test_B = Eq(answer, option_b)`, `test_C`, `test_D` in the same way"
        else:
            tests = "`test_A = Abs(answer - option_a) < 10**(-9)`, then `test_B`, `test_C`, `test_D` in the same way"
        lines.append(f"[Step {n}] Test the result against every stored option: {tests}. "
                     "Exactly one of the four is `True`; its letter is the answer. Do not pick the letter by eye.")
        lines += ["", "Then, immediately after `</think>`, write exactly:", "Final Answer: \\boxed{<Letter>}", "", "Đề bài:", "{de_bai}", ""]
        return "\n".join(lines)
    for i, st in enumerate(steps, 1):
        lines.append(f"[Step {i}] {st}")
    n = len(steps) + 1
    lines.append(
        f"[Step {n}] Copy all four options side by side in one Thought, and write each one in Calculator syntax "
        "(a fraction `\\dfrac{p}{q}` becomes `p/q`, `\\sqrt{n}` becomes `sqrt(n)`, a power `u^{k}` becomes `u**k`). "
        f"{extra_option_note}Then test every option in order with {test_form}, then `test_B`, `test_C`, `test_D` in the same way. "
        "Finally line up each copied option next to its stored result; exactly one of them is `True`. Do not pick the letter by eye.")
    lines += ["", "Then, immediately after `</think>`, write exactly:", "Final Answer: \\boxed{<Letter>}", "", "Đề bài:", "{de_bai}", ""]
    return "\n".join(lines)


def spaced(expr):
    """'x+5' -> 'x + 5', 'x-2' -> 'x - 2' (binary operators get spaces; a leading minus stays)."""
    out = re.sub(r"(?<=[\w)])\s*([+\-])\s*(?=[\w(])", r" \1 ", expr.strip())
    return out
