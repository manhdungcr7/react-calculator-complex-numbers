"""
Kiem tra DOC LAP dap an cua toan bo bien the thi diem (D01, D12, D18, D53).
Voi moi cau, dua vao "params" da luu, TINH LAI dap an dung bang mot cach
khac voi luc sinh (dung sp.solve / sp.diff thay vi cong thuc dong dang da
viet tay trong script sinh), roi so sanh voi chuoi "dap_an".
"""
import json
import re

import sympy as sp

x = sp.Symbol("x")


def P(params, key):
    return sp.sympify(params[key])


def extract_letter(dap_an):
    m = re.match(r"^([A-D])\.", dap_an.strip())
    return m.group(1) if m else None


def _contains(target, text):
    return target.replace(" ", "") in text.replace(" ", "")


def verify_D01(params, dap_an):
    a, m, c, k = P(params, "a"), P(params, "m"), P(params, "c"), P(params, "k")
    sols = sp.solve(sp.Eq(a ** k, m * x + c), x)
    if not sols:
        return False, "khong giai duoc (doc lap)"
    dung = sols[0]
    target = sp.latex(sp.nsimplify(dung)).replace(r"\frac", r"\dfrac")
    ok = _contains(f"x={target}", dap_an)
    return ok, "" if ok else f"khong khop x={target} (doc lap)"


def verify_D12(params, dap_an):
    a, m, c, k = P(params, "a"), P(params, "m"), P(params, "c"), P(params, "k")
    N = a ** k
    sols = sp.solve(sp.Eq(m * x + c, sp.log(N, a)), x)
    if not sols:
        return False, "khong giai duoc (doc lap)"
    dung = sp.nsimplify(sp.simplify(sols[0]))
    target = sp.latex(dung).replace(r"\frac", r"\dfrac")
    ok = _contains(f"x={target}", dap_an)
    return ok, "" if ok else f"khong khop x={target} (doc lap)"


def verify_D18(params, dap_an):
    a = P(params, "a")
    deriv = sp.diff(sp.log(x, a), x)
    deriv = sp.simplify(deriv)
    # deriv doc lap tinh bang sp.diff, dang 1/(x*log(a))
    target_frac = f"y'=\\dfrac{{1}}{{x\\ln {a}}}"
    ok = _contains(target_frac, dap_an)
    if not ok:
        return False, f"khong khop {target_frac} (doc lap qua sp.diff)"
    return True, ""


def verify_D53(params, dap_an):
    a, m, c, k = P(params, "a"), P(params, "m"), P(params, "c"), P(params, "k")
    sol_set = sp.solve_univariate_inequality(m * x + c > a ** k, x, relational=False)
    boundary = sol_set.start
    target = sp.latex(sp.nsimplify(boundary)).replace(r"\frac", r"\dfrac")
    target_interval = f"\\left({target};+\\infty\\right)"
    ok = _contains(target_interval, dap_an)
    return ok, "" if ok else f"khong khop {target_interval} (doc lap)"


VERIFIERS = {
    "D01": verify_D01,
    "D12": verify_D12,
    "D18": verify_D18,
    "D53": verify_D53,
}


def verify_row(row):
    fn = VERIFIERS.get(row["ma_dang"])
    if fn is None:
        return "Chưa có checker", "Không có hàm kiểm tra cho dạng này"
    try:
        ok, note = fn(row["params"], row["dap_an"])
    except Exception as e:
        return "Lỗi khi kiểm tra", f"{type(e).__name__}: {e}"
    return ("Đạt" if ok else "Cần xem lại"), note


if __name__ == "__main__":
    files = [
        "data/questions/mu_logarit_extraction/bien_the/D01_bien_the.json",
        "data/questions/mu_logarit_extraction/bien_the/D12_bien_the.json",
        "data/questions/mu_logarit_extraction/bien_the/D18_bien_the.json",
        "data/questions/mu_logarit_extraction/bien_the/D53_bien_the.json",
    ]
    stats = {}
    failures = []
    total = 0
    for path in files:
        with open(path, encoding="utf-8") as f:
            rows = json.load(f)
        for row in rows:
            total += 1
            status, note = verify_row(row)
            stats[status] = stats.get(status, 0) + 1
            if status != "Đạt":
                failures.append((row["id_goc"], row["ma_dang"], row["params"], status, note))

    lines = [f"Tong so bien the kiem tra: {total}"]
    for status, count in sorted(stats.items()):
        lines.append(f"{status}: {count}")
    if failures:
        lines.append("")
        lines.append("Chi tiet cac cau CHUA DAT:")
        for id_goc, ma_dang, params, status, note in failures:
            lines.append(f"  {ma_dang} {id_goc} params={params} -> {status}: {note}")
    with open("scripts/generate_questions/.tmp_verify_output.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
