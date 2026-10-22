#!/usr/bin/env python3
"""Gom mọi demos/<slug>/meta.json thành catalog.json cho trang kho.

Chạy: python3 scripts/build_catalog.py
Cloudflare Pages chạy lệnh này mỗi lần build (xem HUONG_DAN_TIEP_THEO.md).
"""
import json, pathlib, sys, unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
REQUIRED = ["slug", "title", "type", "industry", "department"]

def main():
    items, errors = [], []
    for meta_path in sorted((ROOT / "demos").glob("*/meta.json")):
        folder = meta_path.parent
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception as e:
            errors.append(f"{meta_path}: không đọc được JSON ({e})"); continue
        missing = [k for k in REQUIRED if not meta.get(k)]
        if missing:
            errors.append(f"{meta_path}: thiếu {', '.join(missing)}"); continue
        if meta["slug"] != folder.name:
            errors.append(f"{meta_path}: slug '{meta['slug']}' khác tên thư mục '{folder.name}'"); continue
        if not (folder / "index.html").exists():
            errors.append(f"{folder}: thiếu index.html"); continue
        for k in ("industry", "department", "type"):
            meta[k] = unicodedata.normalize("NFC", " ".join(str(meta[k]).split()))  # chuẩn hoá để bộ lọc không bị tách đôi
        meta["path"] = f"demos/{folder.name}/"
        thumb = next((t for t in ("thumb.jpg", "thumb.png", "thumb.webp") if (folder / t).exists()), None)
        meta["thumb"] = f"demos/{folder.name}/{thumb}" if thumb else ""
        items.append(meta)
    items.sort(key=lambda m: (m.get("added", ""), m["title"]), reverse=True)
    cfg_path = ROOT / "kho.config.json"
    config = json.loads(cfg_path.read_text(encoding="utf-8")) if cfg_path.exists() else {}
    (ROOT / "catalog.json").write_text(json.dumps({"config": config, "items": items}, ensure_ascii=False, indent=1), encoding="utf-8")
    # link ngắn /<slug> → /demos/<slug>/ (Cloudflare Pages đọc file _redirects ở gốc)
    redirects = "".join(f"/{m['slug']}  /demos/{m['slug']}/  301\n" for m in sorted(items, key=lambda m: m["slug"]))
    (ROOT / "_redirects").write_text(redirects, encoding="utf-8")
    print(f"catalog.json: {len(items)} demo")
    for e in errors:
        print("  LỖI:", e, file=sys.stderr)
    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main()
