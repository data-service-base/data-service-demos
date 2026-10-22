# Kho demo Data Service

Kho lưu toàn bộ demo HTML của team Data Service (Base.vn). Mỗi demo có một link riêng, trang chủ là trang kho để tìm theo ngành, phòng ban, tên.

- Trang kho: `https://<ten-du-an>.pages.dev/` (sau này: `https://dataservice.base.vn/`)
- Link một demo: `https://<ten-du-an>.pages.dev/demos/<slug>/` (link ngắn `/<slug>` cũng chạy)

## Cấu trúc

```
demos/<slug>/
  index.html      file demo, chạy độc lập (thư viện từ CDN, ảnh nhúng sẵn hoặc để cùng thư mục)
  meta.json       thẻ mô tả, dùng cho trang kho và cho Claude dò tìm
  thumb.jpg       ảnh chụp 16:10 (khoảng 720x450)
scripts/
  new_demo.py     tạo thư mục demo mới từ một file HTML
  check_demo.py   kiểm tra demo trước khi đưa lên
  make_thumb.py   chụp thumb.jpg tự động (Playwright) cho demo chưa có ảnh
  build_catalog.py  gom meta.json thành catalog.json và _redirects (Cloudflare chạy mỗi lần build)
.github/workflows/check-demo.yml  tự chạy check_demo.py cho demo đổi trong mỗi pull request
kho.config.json   tên kho, link repo (để hiện nút "Xem code")
index.html        trang kho
catalog.json      sinh tự động, không sửa tay
```

## Quy ước

**slug**: chữ thường không dấu, số, gạch ngang. Đặt theo `ngành-hoặc-khách-nội-dung`, ví dụ `cao-su-ton-kho`, `fnb-doanh-thu-chuoi`. Slug là một phần của link nên không đổi sau khi đã gửi link cho ai.

**meta.json**

| Trường | Bắt buộc | Ý nghĩa |
|---|---|---|
| slug | có | trùng tên thư mục |
| title | có | tên báo cáo |
| type | có | `dashboard`, `proposal`, `deck`, `tool` |
| industry | có | một trong: General, FnB, Sản xuất, Xây dựng, BĐS - CĐT - Nhà thầu, Vận tải, Thời trang, Cao su |
| department | có | ví dụ HR, Kinh doanh, Tài chính, Vận hành, MKT, Supply Chain, Chuỗi cung ứng, Chăm sóc khách hàng, All |
| description | nên có | 1 đến 2 câu: báo cáo trả lời câu hỏi gì |
| tools | nên có | HTML, Chart.js, ECharts, D3, Power BI… |
| tags | tuỳ chọn | từ khoá thêm để tìm: `tồn kho`, `lương`, `EUDR`… |
| author | nên có | người làm |
| added | có | ngày đưa vào kho, YYYY-MM-DD |
| data | có | `demo` (số liệu giả). Kho này **không nhận dữ liệu thật của khách** |
| source, source_repo | tuỳ chọn | link gốc nếu demo chuyển từ nơi khác về |

## Thêm demo mới

```
python3 scripts/new_demo.py ~/Downloads/bao-cao.html --slug fnb-doanh-thu-chuoi \
  --title "Doanh thu chuỗi cửa hàng" --industry FnB --department "Kinh doanh" \
  --desc "Doanh thu theo cửa hàng, ngày, nhóm món" --tags "chuỗi,cửa hàng" --author "Tên"
python3 scripts/make_thumb.py demos/fnb-doanh-thu-chuoi   # hoặc tự thêm thumb.jpg
python3 scripts/check_demo.py demos/fnb-doanh-thu-chuoi
python3 scripts/build_catalog.py
git add . && git commit -m "Thêm demo fnb-doanh-thu-chuoi" && git push
```

Khoảng 1 phút sau link mới chạy, trang kho tự hiện demo.

## Sửa demo

Sửa `demos/<slug>/index.html`, commit, push. GitHub giữ lịch sử mọi lần sửa; muốn xem hay lấy lại bản cũ thì vào tab History của file trên GitHub.

## Xem thử trên máy

```
python3 scripts/build_catalog.py
python3 -m http.server 8000
# mở http://localhost:8000
```
(Mở trực tiếp file index.html bằng trình duyệt sẽ không đọc được catalog.json, cần chạy lệnh trên.)
