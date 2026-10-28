# -*- coding: utf-8 -*-
"""
Sua loi mojibake nghiem trong o batch_round2.json va D01_bien_the.json bang
cach SINH LAI TU DAU tu code nguon SACH (khoi phuc tu commit truoc khi bi
Codex vo tinh lam hong encoding), thay vi co gang va sua chuoi da hong.
Dong thoi mo rong len 90 bien the/dang giong quy uoc chung cua du an.
"""
import json
import random
import re
import sys
from importlib import import_module

sys.path.insert(0, "scripts/generate_questions")
utils = import_module("10_common_utils")

r2 = import_module("23_generate_round2")
d01 = import_module("11_generate_D01")

import math
import sympy as sp


def fast_gen_D67(B, k, c):
    """Ban goc gen_D67 dung 3 lan sp.solve_univariate_inequality de tim
    KHOANG roi lam tron -> cham. Vi cau hoi chi can DEM SO NGUYEN m thoa 3
    dieu kien (disc>0, tong>0, tich>0), quet TRUC TIEP tung so nguyen m
    bang float la du va nhanh hon nhieu, khong can tim khoang lien tuc."""
    Bi, ki, ci = int(B), int(k), int(c)
    if ki != Bi:
        raise AssertionError("The source question ties the coefficient to the base: k = B.")
    if 4 * ci <= Bi ** 2:
        raise AssertionError("A finite integer range requires 4c > B^2.")
    int_vals = []
    for m in range(-60, 61):
        disc = (ki * m) ** 2 - 4 * (ci * m ** 2 - ci)
        if disc > 0 and ki * m > 0 and ci * m ** 2 - ci > 0:
            int_vals.append(m)
    if not (1 <= len(int_vals) <= 6):
        raise AssertionError("so luong phan tu ngoai [1,6]")
    count = len(int_vals)
    upper = sp.sqrt(sp.Rational(4 * ci, 4 * ci - Bi ** 2))
    exact_vals = [m for m in range(2, int(sp.floor(upper)) + 1) if m ** 2 < upper ** 2]
    if sorted(int_vals) != exact_vals:
        raise AssertionError("Direct enumeration disagrees with the derived integer interval.")
    de_bai = (
        f"Gọi $S$ là tập hợp tất cả các giá trị nguyên của tham số $m$ sao cho phương trình "
        f"${Bi**2}^x-m\\cdot{Bi}^{{x+1}}+{ci}m^2-{ci}=0$ có hai nghiệm phân biệt. Hỏi $S$ có bao nhiêu phần tử?\n\n"
    )
    utils_mod = import_module("10_common_utils")
    vals = utils_mod.bump_until_distinct([count, count + 1, max(count - 1, 0), count + 2])
    correct, wrong1, wrong2, wrong3 = (str(v) for v in vals)
    lines, dap_an = r2.render_mc([correct, wrong1, wrong2, wrong3], 0)
    de_bai += "\n".join(lines)
    loi_giai = (
        f"Đặt $t={Bi}^x>0$: $t^2-{ki}mt+{ci}m^2-{ci}=0$. YCBT $\\Leftrightarrow$ PT có 2 nghiệm dương phân biệt "
        f"$\\Leftrightarrow \\Delta>0,\\ {ki}m>0,\\ {ci}m^2-{ci}>0$. "
        f"Do $4\\cdot{ci}>{Bi**2}$, điều kiện $\\Delta>0$ tương đương "
        f"$|m|<{utils.latex(upper)}$. Kết hợp hai điều kiện còn lại, ta được "
        f"$1<m<{utils.latex(upper)}$. Do đó các giá trị nguyên là "
        f"$S=\\{{{','.join(str(v) for v in sorted(int_vals))}\\}}$, có ${count}$ phần tử."
    )
    return de_bai, dap_an, loi_giai, dict(B=str(Bi), k=str(ki), c=str(ci))


def fast_verify_D67(params, expected_count):
    """Ban goc dung sp.solve 100 lan/candidate -> qua cham khi mo rong len
    90/dang. Thay bang cong thuc nghiem bac hai true tiep (math.sqrt, khong
    qua sympy), van la giai lai phuong trinh (khong dua vao nguong dong dang
    da suy trong gen_D67) nhung nhanh hon nhieu bac."""
    B, k, c = (float(params[key]) for key in ("B", "k", "c"))
    if B != k:
        return False
    count = 0
    for mv in range(-80, 80):
        a_coef, b_coef, c_coef = 1.0, -k * mv, c * mv ** 2 - c
        disc = b_coef ** 2 - 4 * a_coef * c_coef
        if disc <= 0:
            continue
        sq = math.sqrt(disc)
        t1 = (-b_coef + sq) / (2 * a_coef)
        t2 = (-b_coef - sq) / (2 * a_coef)
        if t1 > 1e-9 and t2 > 1e-9 and abs(t1 - t2) > 1e-9:
            count += 1
    return count == expected_count


def fast_verify_D69(params, expected_count):
    # Delegate to exact verifier; a floating grid can miss a narrow minimum.
    return r2.verify_D69_full(params, expected_count)


def fast_verify_D51(params, expected_count):
    # Check the logarithm domain with integers, avoiding floating-point logs.
    F, D, lo_x, hi_x, dk_hi = (int(params[k]) for k in ("F", "D", "lo_x", "hi_x", "dk_hi"))
    count = 0
    for xv in range(1, dk_hi + 1):
        if F * xv <= 10 ** D and 4 ** xv - 20 * 2 ** xv + 64 >= 0:
            count += 1
    return count == expected_count


TARGET = 90
MAX_TRIES = 20000


def expand(ma_dang, ten_dang, id_goc, gen_fn, verify_fn, sampler,
           expects_count=False, target=TARGET, max_tries=MAX_TRIES, seed=0):
    rnd = random.Random(seed)
    seen_params, seen_de_bai = set(), set()
    rows = []
    tries = 0
    while len(rows) < target and tries < max_tries:
        tries += 1
        args = sampler(rnd)
        if args in seen_params:
            continue
        try:
            de_bai, dap_an, loi_giai, params = gen_fn(*args)
        except AssertionError:
            continue
        if de_bai in seen_de_bai:
            continue
        key = tuple(sorted(params.items()))
        if key in seen_params:
            continue
        try:
            if expects_count:
                expected = int(dap_an.split("$")[1])
                ok = verify_fn(params, expected)
            else:
                ok = verify_fn(params)
        except Exception:
            ok = False
        if not ok:
            continue
        lines = [l for l in de_bai.split("\n") if re.match(r"^[A-D]\.", l.strip())]
        opts = [re.sub(r"^[A-D]\.\s*", "", l).strip() for l in lines]
        if len(opts) != 4 or len(set(opts)) != 4:
            continue
        seen_params.add(args)
        seen_params.add(key)
        seen_de_bai.add(de_bai)
        rows.append({
            "id_goc": id_goc, "ma_dang": ma_dang, "ten_dang": ten_dang,
            "nguon": "Nhân bản", "loai_bien_the": "chuan",
            "de_bai": de_bai, "dap_an": dap_an, "loi_giai": loi_giai, "params": params,
        })
    print(f"{ma_dang}: {len(rows)}/{target} (tries={tries})", flush=True)
    with open("scripts/generate_questions/.tmp_progress.txt", "a", encoding="utf-8") as pf:
        pf.write(f"{ma_dang}: {len(rows)}/{target} (tries={tries})\n")
    return rows


ROUND2_PATH = "data/questions/mu_logarit_extraction/bien_the/batch_round2.json"


def save_round2(all_rows):
    with open(ROUND2_PATH, "w", encoding="utf-8") as f:
        json.dump(all_rows, f, ensure_ascii=False, indent=2)


DONE_DANG = {"D15", "D05", "D45", "D40", "D16", "D35", "D69", "D67", "D51"}  # da luu du 90, khong lam lai


def main():
    try:
        with open(ROUND2_PATH, encoding="utf-8") as f:
            all_rows = json.load(f)
        all_rows = [r for r in all_rows if r["ma_dang"] in DONE_DANG]
        print(f"Resumed with {len(all_rows)} existing rows from {DONE_DANG}", flush=True)
    except FileNotFoundError:
        all_rows = []

    if "D15" not in DONE_DANG:
        all_rows += expand("D15", "Đạo hàm hàm hợp chứa lôgarit tự nhiên", "p021_q18",
                            r2.gen_D15, r2.verify_D15,
                            lambda r: (r.randint(0, 500),), seed=1501)
        save_round2(all_rows)

    if "D05" not in DONE_DANG:
        all_rows += expand("D05", "Nhận biết mệnh đề đúng/sai về biến đổi lôgarit của tích lũy thừa", "p006_q16",
                            r2.gen_D05, r2.verify_D05,
                            lambda r: (r.randint(2, 40), r.randint(2, 60)), seed=501)
        save_round2(all_rows)

    if "D45" not in DONE_DANG:
        all_rows += expand("D45", "Giải bất phương trình mũ bằng đặt ẩn phụ t=a^x", "p099_q31",
                            r2.gen_D45, r2.verify_D45,
                            lambda r: (r.randint(2, 15), r.randint(1, 60), -r.randint(1, 60)), seed=4501)
        save_round2(all_rows)

    if "D40" not in DONE_DANG:
        all_rows += expand("D40", "Tìm tham số để phương trình lôgarit bậc hai (đặt ẩn phụ) có hai nghiệm phân biệt thỏa điều kiện",
                            "p088_q43", lambda a, p, q: r2.gen_D40(a, a, p, q), r2.verify_D40_full,
                            lambda r: (r.randint(2, 15), r.randint(-40, 40), r.randint(-40, 40)), seed=4001)
        save_round2(all_rows)

    if "D16" not in DONE_DANG:
        all_rows += expand("D16", "Tìm tham số để phương trình mũ có nghiệm thuộc một khoảng (đặt ẩn phụ, xét hàm)",
                            "p021_q20", r2.gen_D16, r2.verify_D16,
                            lambda r: (r.randint(4, 200), r.randint(2, 20), r.randint(1, 40)), seed=1601)
        save_round2(all_rows)

    if "D35" not in DONE_DANG:
        all_rows += expand("D35", "Giải phương trình lôgarit bằng đặt ẩn phụ t=a^x, tính tổng nghiệm", "p070_q31",
                            r2.gen_D35, r2.verify_D35,
                            lambda r: (r.randint(2, 15), r.randint(5, 200), r.randint(1, 30)), seed=3501)
        save_round2(all_rows)

    if "D67" not in DONE_DANG:
        all_rows += expand("D67", "Tìm tham số nguyên để phương trình mũ đặt ẩn phụ có hai nghiệm ẩn phụ phân biệt",
                            "p161_q35", fast_gen_D67, fast_verify_D67,
                            lambda r: (lambda B: (B, B, r.randint(1, 100)))(r.randint(4, 20)),
                            expects_count=True, seed=6704, max_tries=30000)
        save_round2(all_rows)

    if "D69" not in DONE_DANG:
        all_rows += expand("D69", "Đếm giá trị nguyên tham số để phương trình mũ-lôgarit lồng nhau có nghiệm",
                            "p166_q45", r2.gen_D69, fast_verify_D69,
                            lambda r: (r.randint(2, 15), -r.randint(5, 100), r.randint(5, 100)),
                            expects_count=True, seed=6901)
        save_round2(all_rows)

    def gen_D51_capped(F, D):
        de_bai, dap_an, loi_giai, params = r2.gen_D51(2, 2, F, D)
        if int(params["dk_hi"]) > 5000:  # tranh vong lap verify qua lon
            raise AssertionError("dk_hi qua lon")
        return de_bai, dap_an, loi_giai, params

    if "D51" not in DONE_DANG:
        all_rows += expand("D51", "Đếm số nguyên thỏa bất phương trình mũ-lôgarit-căn phức hợp", "p115_q39",
                            gen_D51_capped, fast_verify_D51,
                            lambda r: (r.randint(2, 500), r.randint(2, 4)), expects_count=True, seed=5104, max_tries=8000)
        save_round2(all_rows)

    with open("data/questions/mu_logarit_extraction/bien_the/batch_round2.json", "w", encoding="utf-8") as f:
        json.dump(all_rows, f, ensure_ascii=False, indent=2)

    # ---- D01: verify doc lap bang giai lai phuong trinh (khong dung cong
    # thuc dong dang cua mau_D01), giong dung phong cach pilot ban dau ----
    import sympy as sp
    x_sym = sp.Symbol("x")

    def verify_D01_independent(params):
        a, m, c, k = (sp.sympify(params[key]) for key in ("a", "m", "c", "k"))
        sols = sp.solve(sp.Eq(a ** k, m * x_sym + c), x_sym)
        if not sols:
            return False
        dung = sols[0]
        target_latex = sp.latex(sp.nsimplify(dung)).replace(r"\frac", r"\dfrac")
        return target_latex.replace(" ", "") in params.get("_dap_an_check", "").replace(" ", "")

    def gen_D01_wrapped(a, m, c, k):
        de_bai, dap_an, loi_giai, params = d01.mau_D01(a, m, c, k)
        params["_dap_an_check"] = dap_an
        return de_bai, dap_an, loi_giai, params

    def verify_D01_final(params):
        return verify_D01_independent(params)

    d01_rows = expand("D01", "Giải phương trình lôgarit cơ bản dạng log_a(f(x))=k, f(x) bậc nhất",
                       "p006_q12", gen_D01_wrapped, verify_D01_final,
                       lambda r: (r.choice([2, 3, 4, 5, 6, 7]), r.choice([1, 2, 3]),
                                  r.randint(-15, 15), r.choice([1, 2, 3, 4])),
                       seed=101)
    for row in d01_rows:
        row["params"].pop("_dap_an_check", None)

    with open("data/questions/mu_logarit_extraction/bien_the/D01_bien_the.json", "w", encoding="utf-8") as f:
        json.dump(d01_rows, f, ensure_ascii=False, indent=2)

    with open("scripts/generate_questions/.tmp_expand_output.txt", "w", encoding="utf-8") as f:
        f.write(f"batch_round2.json: {len(all_rows)} rows\n")
        f.write(f"D01_bien_the.json: {len(d01_rows)} rows\n")


if __name__ == "__main__":
    main()
