#!/usr/bin/env python3
"""Chụp thumb.jpg (16:10, 720x450) cho demo chưa có ảnh, bằng Playwright.

Cài một lần: pip install playwright pillow && python3 -m playwright install chromium
Chạy:
  python3 scripts/make_thumb.py                  chụp mọi demo chưa có thumb
  python3 scripts/make_thumb.py demos/<slug>     chụp (hoặc chụp lại) một demo
"""
import functools, http.server, io, pathlib, sys, threading

ROOT = pathlib.Path(__file__).resolve().parent.parent
THUMBS = ("thumb.jpg", "thumb.png", "thumb.webp")

def serve():
    # chạy server tĩnh để demo tải được file cùng thư mục và thư viện CDN như trên kho thật
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
    handler.log_message = lambda *a: None
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd

def main():
    try:
        from playwright.sync_api import sync_playwright
        from PIL import Image
    except ImportError:
        sys.exit("Thiếu thư viện: pip install playwright pillow && python3 -m playwright install chromium")
    if len(sys.argv) > 1:
        folders = [pathlib.Path(a).resolve() for a in sys.argv[1:]]
    else:
        folders = [f for f in sorted((ROOT / "demos").iterdir())
                   if f.is_dir() and not any((f / t).exists() for t in THUMBS)]
    if not folders:
        print("Mọi demo đã có thumb."); return
    httpd = serve()
    base = f"http://127.0.0.1:{httpd.server_address[1]}"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        for folder in folders:
            url = f"{base}/{folder.relative_to(ROOT).as_posix()}/"
            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
            except Exception as e:
                print(f"! {folder.name}: tải chưa xong ({e.__class__.__name__}), vẫn chụp")
            page.wait_for_timeout(1500)  # chờ biểu đồ chạy xong hiệu ứng
            img = Image.open(io.BytesIO(page.screenshot())).convert("RGB").resize((720, 450), Image.LANCZOS)
            img.save(folder / "thumb.jpg", quality=82, optimize=True)
            print(f"✓ {folder.name}/thumb.jpg")
        browser.close()
    httpd.shutdown()

if __name__ == "__main__":
    main()
