#!/usr/bin/env python3
"""Kiểm tra một demo trước khi đưa vào kho.

Chạy: python3 scripts/check_demo.py demos/<slug>
Báo: thiếu file, file cục bộ bị tham chiếu nhưng không có, tên miền bên ngoài được gọi,
dung lượng, và các mẫu có thể là dữ liệu thật (email, số điện thoại) để người nộp tự soát.
"""
import pathlib, re, sys

def check(folder: pathlib.Path) -> bool:
    ok = True
    html_path = folder / "index.html"
    if not html_path.exists():
        print("✗ thiếu index.html"); return False
    html = html_path.read_text(encoding="utf-8", errors="ignore")
    size = html_path.stat().st_size / 1e6
    print(f"• index.html {size:.2f} MB" + ("  (lớn, nên tách ảnh ra file riêng)" if size > 8 else ""))
    if not (folder / "meta.json").exists():
        print("✗ thiếu meta.json (chạy scripts/new_demo.py để tạo)"); ok = False
    if not any((folder / t).exists() for t in ("thumb.jpg", "thumb.png", "thumb.webp")):
        print("! chưa có thumb.jpg (ảnh chụp 16:10 hiện ở trang kho)")
    for ref in sorted(set(re.findall(r'(?:src|href)="(?!https?:|data:|#|mailto:|tel:|javascript:|blob:)([^"?#]+)', html))):
        if ref and "${" not in ref and not (folder / ref).exists():
            print(f"✗ tham chiếu file cục bộ không có: {ref}"); ok = False
    hosts = sorted(set(re.findall(r'(?:src|href)="https?://([^/"]+)', html)))
    if hosts:
        print("• gọi tới:", ", ".join(hosts))
    emails = set(re.findall(r'[\w.+-]+@[\w-]+\.[a-z]{2,}(?:\.[a-z]{2,})?', html))
    phones = set(re.findall(r'(?<![#\w.])(?:\+84|0)\d{2,3}[ .]?\d{3}[ .]?\d{3,4}(?![\d.])', html))
    if emails or phones:
        print(f"! soát lại dữ liệu thật: {len(emails)} email, {len(phones)} số điện thoại")
        for x in sorted(emails)[:5] + sorted(phones)[:5]:
            print("   ", x)
    print("✓ đạt" if ok else "✗ cần sửa")
    return ok

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Cách dùng: python3 scripts/check_demo.py demos/<slug>")
    sys.exit(0 if check(pathlib.Path(sys.argv[1])) else 1)
