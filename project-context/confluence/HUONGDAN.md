# Bản xuất Confluence — tài liệu Peye-Haiti

Sinh từ các file `.md` cùng thư mục cha bằng `tools/md2confluence.py`.
Định dạng: **Confluence Storage Format** (XHTML + macro Confluence).

## Nội dung thư mục

| File | Nguồn | Sơ đồ |
|---|---|---|
| `PeyeHaiti_PRD.storage.html` | `PeyeHaiti_PRD.md` | 8 |
| `PeyeHaiti_BRD.storage.html` | `PeyeHaiti_BRD.md` | 16 |
| `PeyeHaiti_SSD.storage.html` | `PeyeHaiti_SSD.md` | 13 |
| `PeyeHaiti_TSD.storage.html` | `PeyeHaiti_TSD.md` | 2 |
| `PeyeHaiti_API_Spec.storage.html` | `PeyeHaiti_API_Spec.md` | 0 |
| `PeyeHaiti_DataDict.storage.html` | `PeyeHaiti_DataDict.md` | 0 |
| `PeyeHaiti_Traceability.storage.html` | `PeyeHaiti_Traceability.md` | 0 |
| `README.storage.html` | `README.md` | 0 |

- `images/*.png` — 39 sơ đồ mermaid đã render (scale 2×, nền trắng)
- `images/*.mmd` — nguồn mermaid tương ứng, để render lại khi sửa
- `MANIFEST.txt` — trang nào cần attach những ảnh nào

## Cách insert vào Confluence (thủ công)

1. Tạo / mở trang đích → vào chế độ **Edit**.
2. **Attach ảnh trước**: kéo toàn bộ `images/<TÊN_TÀI_LIỆU>-diagram-*.png` vào trang
   (hoặc menu `···` → *Attachments*). Tên file phải giữ nguyên — HTML tham chiếu
   theo đúng tên này.
3. Bấm **`+`** (Insert) → **Markup** → chọn **Confluence Storage Format** hoặc
   *Confluence Wiki / HTML* tuỳ phiên bản → dán toàn bộ nội dung file
   `*.storage.html` → **Insert**.
4. Publish.

> Nếu menu Markup không có mục *Confluence Storage Format*: dùng **Edit contents**
> của macro *HTML* (cần admin bật), hoặc đẩy qua REST API bằng `tools/upload.sh`.

## Cách insert bằng REST API (tự động, khuyến nghị khi có 39 ảnh)

```bash
export CONF_BASE="https://<site>.atlassian.net/wiki"
export CONF_USER="vuvhh@viettel.com.vn"
export CONF_TOKEN="<API token>"
export CONF_SPACE="MMS"

cd confluence/tools
./upload.sh PeyeHaiti_PRD "PRD — Giải pháp Merchant Peye-Haiti"
./upload.sh PeyeHaiti_BRD "BRD — Giải pháp Merchant Peye-Haiti"
# ... các tài liệu còn lại
```

Script tự tạo trang mới (hoặc cập nhật trang cùng tiêu đề) rồi upload kèm
mọi ảnh sơ đồ của tài liệu đó. Tham số thứ 3 (tuỳ chọn) là `PARENT_PAGE_ID`
nếu muốn đặt trang con.

## Sinh lại bản xuất sau khi sửa `.md`

```bash
cd "$(dirname confluence)"                       # thư mục chứa các file .md
python3 confluence/tools/md2confluence.py *.md --out confluence --toc
confluence/tools/render-mermaid.sh               # cần mermaid-cli
```

Cờ hữu ích của `md2confluence.py`:

| Cờ | Tác dụng |
|---|---|
| `--toc` | chèn macro *Table of Contents* đầu trang (đang bật cho bản này) |
| `--mermaid-format svg` | xuất sơ đồ dạng SVG thay vì PNG |
| `--mermaid-source` | kèm nguồn mermaid trong macro *Expand* ngay dưới ảnh |

## Quy ước chuyển đổi

| Markdown | Confluence Storage Format |
|---|---|
| `#`…`######` | `<h1>`…`<h6>` |
| bảng GFM (kể cả `<br/>` trong ô, canh lề `:---:`) | `<table><tbody><tr><th>/<td>` + `style="text-align:…"` |
| ``` ```json ``` ``` | macro `code` + `<ac:plain-text-body><![CDATA[…]]>` |
| ``` ```http ``` ``` | macro `code` với `language=none` (Confluence không có lexer `http`) |
| ``` ```mermaid ``` ``` | `<ac:image><ri:attachment ri:filename="…png"/>` + file PNG trong `images/` |
| `> trích dẫn` | macro `info` |
| `---` | `<hr />` |
| `**đậm**` · `*nghiêng*` · `` `code` `` | `<strong>` · `<em>` · `<code>` |
| danh sách lồng nhau | `<ul>`/`<ol>` lồng, mỗi item bọc `<p>` |

## Đã kiểm chứng

- 8/8 file là XHTML well-formed (parse bằng `xml.etree`, có khai báo namespace `ac:`/`ri:`).
- Số heading, số bảng, số dòng bảng, số code block, số sơ đồ: **khớp 100%** với nguồn.
- Nội dung mọi code block và mọi sơ đồ mermaid: **khớp nguyên văn** với `.md`.
- 39/39 ảnh render thành công (tiếng Việt có dấu và emoji hiển thị đúng).

### Hai điểm cần biết

1. `&nbsp;` được xuất thành `&#160;` — `&nbsp;` là entity không định nghĩa trong
   XHTML thuần nên một số API/validator từ chối.
2. Trường hợp `*nghiêng* bao quanh **đậm**` sẽ không thành nghiêng (giữ nguyên dấu
   `*`), để bảo đảm thẻ không lệch. Trong bộ tài liệu này chỉ gặp 1 lần
   (`PeyeHaiti_DataDict.md` dòng 894, đoạn ghi chú cuối bảng) — nguyên nhân là
   `sca_*` trong câu bị GFM hiểu là dấu đóng nghiêng.
