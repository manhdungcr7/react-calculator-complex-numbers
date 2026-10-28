# -*- coding: utf-8 -*-
"""Rebuild D67 variants with the coefficient tied to the base as in the source."""
import importlib.util
import json
import random
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
FIX_PATH = Path(__file__).with_name("31_fix_and_expand.py")
spec = importlib.util.spec_from_file_location("fix_and_expand", FIX_PATH)
fix = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fix)

OUT = REPO / "data/questions/mu_logarit_extraction/bien_the/batch_round2.json"
TARGET = 90
SOURCE_ID = "p161_q35"
TYPE_NAME = "Tìm tham số nguyên để phương trình mũ đặt ẩn phụ có hai nghiệm ẩn phụ phân biệt"


def main():
    candidates = []
    for B in range(4, 21):
        for c in range(1, 101):
            # B is the base and also the coefficient induced by B^(x+1).
            try:
                q, answer, solution, params = fix.fast_gen_D67(B, B, c)
            except AssertionError:
                continue
            if (B, c) == (5, 7):  # Keep the original source question out of variants.
                continue
            expected = int(re.search(r"\$(-?\d+)\$", answer).group(1))
            if not fix.fast_verify_D67(params, expected):
                raise AssertionError(f"Independent verification failed: {params}")
            choices = re.findall(r"(?m)^([A-D])\.\s*(.+)$", q)
            norm = [re.sub(r"[\s$.,]", "", value) for _, value in choices]
            if len(choices) != 4 or {letter for letter, _ in choices} != set("ABCD") or len(set(norm)) != 4:
                raise AssertionError(f"Invalid options for {params}")
            candidates.append((q, answer, solution, params))

    random.Random(6704).shuffle(candidates)
    selected = candidates[:TARGET]
    if len(selected) != TARGET:
        raise AssertionError(f"Only {len(selected)} valid D67 variants found")

    new_rows = [{
        "id_goc": SOURCE_ID,
        "ma_dang": "D67",
        "ten_dang": TYPE_NAME,
        "nguon": "Nhân bản",
        "loai_bien_the": "chuan",
        "de_bai": q,
        "dap_an": answer,
        "loi_giai": solution,
        "params": {key: str(value) for key, value in params.items()},
    } for q, answer, solution, params in selected]

    old_rows = json.loads(OUT.read_text(encoding="utf-8"))
    rows = [row for row in old_rows if row.get("ma_dang") != "D67"] + new_rows
    OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Rebuilt and independently verified {len(new_rows)} D67 variants")


if __name__ == "__main__":
    main()
