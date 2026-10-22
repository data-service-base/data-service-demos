#!/usr/bin/env python3
"""Tạo thư mục demo mới từ một file HTML.

Chạy:
  python3 scripts/new_demo.py duong/dan/file.html --slug ten-demo --title "Tên báo cáo" \
      --industry FnB --department "Kinh doanh" [--type dashboard] [--desc "..."] [--tags a,b] [--author "Tên"]
Sau đó: thêm thumb.jpg (ảnh chụp 16:10), chạy check_demo.py, rồi build_catalog.py.
"""
import argparse, datetime, json, pathlib, re, shutil, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDUSTRIES = ["General", "FnB", "Sản xuất", "Xây dựng", "BĐS - CĐT - Nhà thầu", "Vận tải", "Thời trang", "Cao su", "Bán lẻ", "Giáo dục", "Năng lượng"]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("html")
    p.add_argument("--slug", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--industry", required=True)
    p.add_argument("--department", required=True)
    p.add_argument("--type", default="dashboard", choices=["dashboard", "proposal", "deck", "tool"])
    p.add_argument("--desc", default="")
    p.add_argument("--tags", default="")
    p.add_argument("--author", default="")
    a = p.parse_args()
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", a.slug):
        sys.exit("slug chỉ gồm chữ thường không dấu, số và gạch ngang, ví dụ: sapoche-kho-thanh-pham")
    if a.industry not in INDUSTRIES:
        print(f"! ngành '{a.industry}' chưa có trong danh sách chuẩn: {', '.join(INDUSTRIES)}")
    dest = ROOT / "demos" / a.slug
    if dest.exists():
        sys.exit(f"đã có thư mục {dest}")
    dest.mkdir(parents=True)
    shutil.copy(a.html, dest / "index.html")
    meta = {"slug": a.slug, "title": a.title, "type": a.type, "industry": a.industry,
            "department": a.department, "description": a.desc, "tools": ["HTML"], "source": "",
            "source_repo": "", "author": a.author, "added": datetime.date.today().isoformat(),
            "status": "demo", "data": "demo", "tags": [t.strip() for t in a.tags.split(",") if t.strip()]}
    (dest / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✓ tạo {dest}. Còn thiếu thumb.jpg. Kiểm tra: python3 scripts/check_demo.py demos/{a.slug}")

if __name__ == "__main__":
    main()
