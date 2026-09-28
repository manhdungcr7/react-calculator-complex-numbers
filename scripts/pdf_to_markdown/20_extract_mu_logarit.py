"""Trích ứng viên câu Mũ–Logarit từ DAP AN.pdf và render trang để kiểm duyệt.

Script kế thừa cách làm của scripts/pdf_to_markdown/1_find_questions.py và
2_render_pages.py, nhưng tách câu theo block thay vì chỉ xét dòng chứa "Câu".
Không gọi LLM và không tự coi kết quả lọc từ khóa là nhãn vàng.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import unicodedata
from pathlib import Path

import fitz


QUESTION_RE = re.compile(r"(?m)^\s*Câu\s*(\d+)\s*:\s*")
SOLUTION_RE = re.compile(r"(?:ý\s*)?Lời\s*giải\s*\.?", re.IGNORECASE)


def ascii_text(text: str) -> str:
    text = unicodedata.normalize("NFD", text.lower())
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text.replace("đ", "d")


def compact(text: str) -> str:
    return re.sub(r"\s+", "", ascii_text(text))


def relevance(prompt: str, full_block: str) -> list[str]:
    """Lọc rộng để ưu tiên recall; nhãn cuối vẫn cần người kiểm duyệt."""
    p = ascii_text(prompt)
    pc = compact(prompt)
    b = ascii_text(full_block)
    reasons: list[str] = []

    if "log" in p or re.search(r"(?<![a-z])ln(?![a-z])", p):
        reasons.append("log_or_ln_in_question")

    phrases = {
        "hamsomu": "ham_so_mu",
        "phuongtrinhmu": "phuong_trinh_mu",
        "batphuongtrinhmu": "bat_phuong_trinh_mu",
        "hamsohamũ": "ham_so_mu",
        "luythua": "luy_thua",
    }
    for token, label in phrases.items():
        if token in pc and label not in reasons:
            reasons.append(label)

    # Bài toán tăng trưởng/lãi kép thuộc mô hình hàm mũ dù đề có thể không ghi
    # trực tiếp từ "mũ" hoặc "logarit".
    if ("lai suat" in p and any(x in p for x in ("ngan hang", "gui", "von", "tien"))) \
            or any(x in p for x in (
                "lai kep", "tang truong", "dan so tang",
                "moi nam tiep theo deu tang", "moi nam deu tang",
            )):
        reasons.append("exponential_application")

    # Câu phương trình mũ thường chỉ hiện thành 2x/3x trong text layer. Nếu lời
    # giải dùng log và đề hỏi nghiệm/tham số thì giữ làm ứng viên để khỏi bỏ sót.
    if not reasons and "log" in b and any(x in p for x in (
        "phuong trinh", "bat phuong trinh", "tap nghiem", "nghiem cua",
        "so nghiem", "tham so", "gia tri m", "gia tri nguyen",
    )):
        reasons.append("log_in_solution_review_exponential")

    return reasons


def visual_reasons(prompt: str) -> list[str]:
    p = ascii_text(prompt)
    pc = compact(prompt)
    phrases = {
        "hinh ben": "hinh_ben",
        "hinh ve": "hinh_ve",
        "hinh duoi": "hinh_duoi",
        "tham khao hinh": "tham_khao_hinh",
        "bang bien thien": "bang_bien_thien",
        "duong cong": "duong_cong",
    }
    out = [label for phrase, label in phrases.items() if phrase in p]
    compact_phrases = {
        "hinhben": "hinh_ben",
        "hinhve": "hinh_ve",
        "hinhduoi": "hinh_duoi",
        "thamkhaohinh": "tham_khao_hinh",
        "bangbienthien": "bang_bien_thien",
        "duongcong": "duong_cong",
    }
    for phrase, label in compact_phrases.items():
        if phrase in pc and label not in out:
            out.append(label)
    if (
        "dothi" in pc
        and (
            "bondothi" in pc
            or "timdothi" in pc
            or "dothinaoduoi" in pc
            or "dothinaosau" in pc
        )
        and "do_thi_phuong_an" not in out
    ):
        out.append("do_thi_phuong_an")
    return out


def out_of_scope_reasons(prompt: str) -> list[str]:
    """Loại câu chỉ mượn log/e^x nhưng nhiệm vụ chính thuộc chuyên đề khác."""
    p = ascii_text(prompt)
    pc = compact(prompt)
    groups = {
        "nguyen_ham_tich_phan": (
            "nguyen ham", "tich phan", "dien tich hinh phang",
            "hinh thang cong", "khoi tron xoay", "the tich v cua khoi tron xoay",
        ),
        "day_so": ("day so",),
    }
    out = [label for label, phrases in groups.items() if any(x in p for x in phrases)]

    calculus_compact = (
        "nguyenham", "tichphan", "dientichhinhphang", "hinhthangcong",
        "khoitronxoay", "thetichcuakhoitronxoay", "thetichvcuakhoitronxoay",
    )
    integral_layout = "dx" in pc and bool(re.search(r"(?:^|\n)\s*(?:\d+\s*)?Z(?:\s|\d)", prompt))
    derivative_initial_value = (
        ("f′(x)=" in pc or "f'(x)=" in pc)
        and len(re.findall(r"f\([^x][^)]*\)=", pc)) >= 2
    )
    if (
        any(x in pc for x in calculus_compact)
        or integral_layout
        or derivative_initial_value
    ) and "nguyen_ham_tich_phan" not in out:
        out.append("nguyen_ham_tich_phan")
    return out


def exponential_layout_questions(doc: fitz.Document) -> set[tuple[int, int]]:
    """Tìm a^x từ layout span vì text layer làm mất ký hiệu số mũ (13^x -> 13x)."""
    found: set[tuple[int, int]] = set()
    for page_no, page in enumerate(doc, start=1):
        current: tuple[int, int] | None = None
        in_prompt = False
        blocks = sorted(page.get_text("dict").get("blocks", []), key=lambda b: (
            b.get("bbox", (0, 0, 0, 0))[1], b.get("bbox", (0, 0, 0, 0))[0]
        ))
        for block in blocks:
            lines = sorted(block.get("lines", []), key=lambda line: (
                line.get("bbox", (0, 0, 0, 0))[1], line.get("bbox", (0, 0, 0, 0))[0]
            ))
            for line in lines:
                spans = line.get("spans", [])
                text = "".join(span.get("text", "") for span in spans)
                question = re.search(r"Câu\s*(\d+)\s*:", text)
                if question:
                    current = (page_no, int(question.group(1)))
                    in_prompt = True
                if SOLUTION_RE.search(text):
                    in_prompt = False
                if not current or not in_prompt or len(spans) < 2:
                    continue

                normal_size = max(float(span.get("size", 0)) for span in spans)
                pos = 0
                while pos < len(spans):
                    if float(spans[pos].get("size", 0)) > normal_size * 0.82:
                        pos += 1
                        continue

                    run_start = pos
                    while (
                        pos < len(spans)
                        and float(spans[pos].get("size", 0)) <= normal_size * 0.82
                    ):
                        pos += 1
                    if run_start == 0:
                        continue

                    previous = spans[run_start - 1]
                    previous_text = previous.get("text", "").rstrip()
                    run_text = "".join(
                        span.get("text", "") for span in spans[run_start:pos]
                    ).strip()
                    if not run_text or not re.search(r"[xXymntkab]", run_text):
                        continue
                    if not re.search(r"(?:\d|[eab])$", previous_text, re.IGNORECASE):
                        continue
                    first = spans[run_start]
                    gap = float(first.get("bbox", (0, 0, 0, 0))[0]) - float(
                        previous.get("bbox", (0, 0, 0, 0))[2]
                    )
                    raised = float(first.get("origin", (0, 0))[1]) < float(
                        previous.get("origin", (0, 0))[1]
                    ) - 1.0
                    if -1.5 <= gap <= 3.0 and raised:
                        found.add(current)
    return found


def parse_questions(doc: fitz.Document) -> list[dict]:
    chunks: list[str] = []
    page_at_offset: list[tuple[int, int]] = []
    offset = 0
    for page_no, page in enumerate(doc, start=1):
        marker = f"\n--- PAGE {page_no} ---\n"
        text = page.get_text("text")
        chunks.extend((marker, text))
        page_at_offset.append((offset + len(marker), page_no))
        offset += len(marker) + len(text)

    full = "".join(chunks)
    matches = list(QUESTION_RE.finditer(full))

    def page_for(pos: int) -> int:
        result = 1
        for start, page_no in page_at_offset:
            if start > pos:
                break
            result = page_no
        return result

    exponential_layout = exponential_layout_questions(doc)
    rows: list[dict] = []
    for idx, match in enumerate(matches):
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(full)
        block = full[match.start():end].strip()
        solution = SOLUTION_RE.search(block)
        prompt = block[:solution.start()].strip() if solution else block
        start_page = page_for(match.start())
        end_page = page_for(max(match.start(), end - 1))
        reasons = relevance(prompt, block)
        number = int(match.group(1))
        if (start_page, number) in exponential_layout and "exponential_superscript_layout" not in reasons:
            reasons.append("exponential_superscript_layout")
        if not reasons:
            continue
        visuals = visual_reasons(prompt)
        out_of_scope = out_of_scope_reasons(prompt)
        rows.append({
            "id": f"p{start_page:03d}_q{number:02d}",
            "page_start": start_page,
            "page_end": end_page,
            "question_number": number,
            "topic": "Mũ - Logarit",
            "match_reasons": reasons,
            "needs_visual": bool(visuals),
            "visual_reasons": visuals,
            "out_of_scope": bool(out_of_scope),
            "out_of_scope_reasons": out_of_scope,
            "selected_no_visual": not visuals and not out_of_scope,
            "prompt_text_layer": prompt,
            "full_text_layer": block,
        })
    return rows


def write_outputs(rows: list[dict], output_dir: Path, doc: fitz.Document, dpi: int) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    selected = [row for row in rows if row["selected_no_visual"]]

    for name, data in (("candidates_all.jsonl", rows), ("selected_no_visual.jsonl", selected)):
        with (output_dir / name).open("w", encoding="utf-8", newline="\n") as f:
            for row in data:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")

    fields = [
        "id", "page_start", "page_end", "question_number", "topic",
        "match_reasons", "needs_visual", "visual_reasons", "selected_no_visual",
        "out_of_scope", "out_of_scope_reasons", "prompt_text_layer",
    ]
    with (output_dir / "review.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            item = dict(row)
            item["match_reasons"] = "|".join(row["match_reasons"])
            item["visual_reasons"] = "|".join(row["visual_reasons"])
            item["out_of_scope_reasons"] = "|".join(row["out_of_scope_reasons"])
            writer.writerow(item)

    pages = sorted({p for row in selected for p in range(row["page_start"], row["page_end"] + 1)})
    pages_dir = output_dir / "pages"
    pages_dir.mkdir(exist_ok=True)
    for old_page in pages_dir.glob("page_*.png"):
        old_page.unlink()
    scale = dpi / 72.0
    for page_no in pages:
        pix = doc[page_no - 1].get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
        pix.save(pages_dir / f"page_{page_no:03d}.png")

    summary = {
        "source_pdf": str(Path(doc.name).resolve()),
        "topic": "Mũ - Logarit",
        "candidate_count": len(rows),
        "excluded_visual_count": sum(row["needs_visual"] for row in rows),
        "excluded_other_topic_count": sum(row["out_of_scope"] for row in rows),
        "selected_no_visual_count": len(selected),
        "rendered_page_count": len(pages),
        "rendered_pages": pages,
        "warning": "Bộ lọc ưu tiên recall; phải duyệt review.csv và ảnh trước khi dùng làm nhãn vàng.",
    }
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", type=Path, default=Path("DAP AN.pdf"))
    parser.add_argument(
        "--output-dir", type=Path,
        default=Path("data/questions/mu_logarit_extraction"),
    )
    parser.add_argument("--dpi", type=int, default=180)
    args = parser.parse_args()

    if not args.pdf.is_file():
        raise FileNotFoundError(args.pdf)
    if args.dpi < 72:
        raise ValueError("--dpi phải >= 72")

    with fitz.open(args.pdf) as doc:
        rows = parse_questions(doc)
        write_outputs(rows, args.output_dir, doc, args.dpi)


if __name__ == "__main__":
    main()
