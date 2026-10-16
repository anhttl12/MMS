# Ma trận truy vết — Giải pháp Merchant Peye-Haiti (footprint go-live 01/10/2026)

| Trường | Nội dung |
|---|---|
| Mã tài liệu | **Peye-Haiti-TRC-001 · v4.2** — 20/08/2026 tối · **«v3.6»:** CH-00 trước eKYC · TẠO LÀ ACTIVE (US-07/AC-1.4/BRH-03/US-26 đổi ngữ nghĩa hậu kiểm — không đổi mã/số đếm) · **20/08 (v3.5):** một app CHỌN VAI (+US-46/AC-1.8 — 42 US·46 AC; +màn CH-00 — 42 màn); hai bậc xác thực (khôi phục C.9/E.16.6 → 109 mục/110 HTTP · OB 12 API); PAY_SCA_THRESHOLD thay PAY_MAX_PILOT · nền v4.0 — 15/08/2026 · **15/08 (Peye-Haiti — app chung, mô hình BiMPay):** đổi tên PINASSI→HaitiPay (file `PeyeHaiti_*.md`; prefix `PIN-` giữ); +EP-11 người mua US-41..45 · AC-11.1..11.5; +bảng `payment` (28); +M-PAY/M-PAY-hook (tích hợp 14); +E.16 (5) · P.1 · C.7/C.8 · B.4 → 106 mục/107 HTTP; +5 màn NM (wireframes đợt sau) → 41 màn; +luồng S9 · **15/08 (CR BRH)**: áp CR-1/2/3/4/5/6/7/8/12 (`BRH/PeyeHaiti_CR_BRH_LuuTru_NhatKy.md`) — merchant +mcc/alias/national_merchant_id · person +nif_no/rni_person_id · credit_event +payer_person_id/payer_operator · QR theo HTQR 1.0 · KYC=KYC2; số bảng/màn/US/AC/endpoint KHÔNG đổi · **04/08**: hoán đúng vai AQ-00 (đầu nối/kho token) ↔ AQ-01 (tổng quan sức khỏe/trực ban) theo wireframes + thân API Spec; sửa số mục C của M1a/M1b/M3 (C.3/C.4/C.6); bỏ màn BRH-09 «Cấu hình» — màn 37→36 (BRH 10), tham số chuyển vận hành Natcom qua E.13.x · **02/08 (CANON2)**: 8 rút gọn — bỏ M7/M4b/qr_intent/report_schedule/buyer_profile, hoãn app người mua NM + danh bạ V1, gộp device→auth_session, matching 2 mức; US 40→36 · AC 44→39 · màn 43→37 · bảng 31→27 · tích hợp 15→12 · mã lỗi 44→41 · **25/07**: bỏ API M5 (đối chiếu tên — bank tự xác thực qua OTP) + gộp còn 1 bậc KYC · sắp xếp mục C theo luồng onboarding · tích hợp 17→15, mã lỗi 48→44 · đồng bộ tên ví Natcash→wallet2 (NatTransfer), mã ví dụ NATC→NTRF (đồng bộ quyết định chốt: **4 dịch vụ** · event bus **Apache Kafka** · sizing **5.000 merchant** UAT+PROD; nền v1.1: vá 3 điểm hở AC + 1 lệch mapping màn + 6 mâu thuẫn số liệu — xem §8) |
| Loại | Ma trận truy vết (traceability matrix) — artifact DÙNG CHUNG cho DEV & TESTER |
| Nguồn (5 tài liệu, không có nội dung mới) | `PeyeHaiti_PRD.md` **v4.2** · `PeyeHaiti_SSD.md` **v5.0** · `PeyeHaiti_TSD.md` **v4.4** · `PeyeHaiti_API_Spec.md` **v3.4** · `PeyeHaiti_DataDict.md` **v4.1** |
| Phạm vi phủ | **11 Epic** · **42 user story** (US-01…US-46; +US-46 chọn vai «v3.5») · **46 acceptance criteria** (AC-1.1…AC-11.6, +AC-1.8) · 9 luồng F1–F9 / **9 luồng S1–S9** · **42 màn** (NB 17 · BRH 10 · AQ 4 · VI 5 · NM 5 · **CH 1 «v3.6» — đã có wireframe**) · **4 dịch vụ** (Merchant & Identity · Commerce (Ingest + **Payment**) · Back-office · Notification) · **28 bảng** · **109 mục API** (B 5 · C 9 · D 5 · E 89 · P 1 — nhóm E: 89 mục / 90 HTTP; tổng **110 HTTP endpoint**) · **14 mục tích hợp = 12 giao diện ngoài + 2 nội bộ** · 11 phụ thuộc D1–D11 |
| Ràng buộc đã chốt (nhắc lại) | KHÔNG có tài khoản ảo · KHÔNG có USSD (ngoại lệ: enum kênh tra cứu B.5 cho GĐ2) · KHÔNG dùng mã M2/M6/M6b/N2 · MMS ngoài đường tiền · QR in SỐ TK THẬT (chuẩn HTQR 1.0, có tag 52 MCC) · M4 do BANK NHẬN cung cấp · dữ liệu ra hệ thống quốc gia theo «3 KHÔNG» (CR-8) |

**Cách đọc (2 lối vào):**

- **DEV** đi từ **§1 cột US → cột API + cột Bảng dữ liệu**: biết phải code endpoint nào (tra chi tiết trường & mã lỗi tại API_Spec mục tương ứng), ghi vào bảng nào (tra kiểu trường tại DataDict), thuộc service nào (SSD §4). Cần đi ngược (đang sửa 1 màn / 1 bảng thì ảnh hưởng US nào) → **§2** và **§3**.
- **TESTER** đi từ **§5 cột AC → loại test + tiền điều kiện + cách đo**: mỗi dòng AC là một kịch bản UAT/SIT có số liệu nghiệm thu cụ thể. Kịch bản phụ thuộc đối tác → tra **§4** (interface nào phải sống) và **§7** (phụ thuộc D-x nào phải xong trước).
- Ô trong ma trận dùng **mã**, không diễn giải: `E.4.3` = mục trong API_Spec · `C.1` = Open Banking M1 · `S2` = luồng SSD §5 · `AC-2.1` = tiêu chí PRD §7.

---

## §1. Ma trận CHÍNH — theo user story (41 hàng)

| US | Epic | Tên rút gọn | Luồng | Màn | Service (SSD §4) | API chính (API_Spec) | Bảng dữ liệu chính | AC | Ưu tiên |
|---|---|---|---|---|---|---|---|---|---|
| US-01 | EP-1 | Tự đăng ký gian hàng <10 phút | F1 · S1 | NB-01/02 · CH-00 · NB-2A/2B («v3.6» — gian hàng khai ở NB-2B, nộp cùng E.2.2) | Merchant & Identity | `E.1.1 POST /auth/register` · `E.1.2` · `E.1.3` · `E.1.4 POST /auth/pin/set` (→ `D.5` N1) · `E.2.2` («v3.6» — gian hàng) | `person` · `merchant` · `application` · `market` | AC-1.1 | Bắt buộc |
| US-02 | EP-1 | Chụp CIN + selfie → eKYC | F1 · S1 | NB-2A | Merchant & Identity | `E.2.1 POST /ekyc/photos` · `E.2.2 POST /ekyc/submit` (→ `D.1` E1, `D.2` E2) | `ekyc_result` · `application` · `person` | AC-1.2 | Bắt buộc |
| US-03 | EP-1 | Liên kết TK/ví đã có làm nơi nhận | F1 · S1 | NB-2B | Merchant & Identity | `E.3.2 POST /links` · `E.3.3 POST /links/confirm` (→ `C.1/C.2` M1) | `account_link` · `token` | AC-1.3 | Bắt buộc |
| US-05 | EP-1 | Thấy hồ sơ đang ở bước nào | F1 | NB-1C | Merchant & Identity | `E.2.3 GET /applications/me` · `E.2.4 POST /applications/me/resubmit` | `application` · `ekyc_result` | AC-1.2 | Bắt buộc |
| US-06 | EP-1 | Field-agent đăng ký hộ (NAT-xxx) | F1 · S1 | NB-01 | Merchant & Identity | `E.1.1` (`agent_code` — đánh dấu phiên) · `E.1.4` (`is_agent_session=true`) · `E.2.2` («v3.6» — app truyền lại, ghi `merchant.agent_code`) | `merchant` (agent_code — danh mục trong `param`) · `auth_session` | AC-1.5 | Bắt buộc |
| US-07 «v3.6» | EP-1 | Gian hàng ACTIVE NGAY khi tạo (không cổng duyệt); hồ sơ CÓ CỜ vào hậu kiểm ưu tiên + suspend 1 chạm | F1 · S1 | BRH-03 | Merchant & Identity · Back-office (Compliance) | `E.2.2` (kích hoạt tức thời C10 «v3.6») · `E.11.1` (danh sách hậu kiểm) · `E.11.2` (đóng hậu kiểm) | `application` · `merchant` · `aml_alert` | AC-1.4 | Bắt buộc |
| US-08 | EP-2 | QR TĨNH dán quầy (số TK thật) | F2 · S3 · S8 | NB-04 | Commerce (I2 · QR) · Merchant & Identity (standee) | `E.4.1 GET /qr/static` | `standee` · `account_link` · `merchant` | AC-2.1 · AC-2.8 | Bắt buộc |
| US-09 | EP-2 | QR ĐỘNG kèm đúng số tiền | F2 · S3 | NB-04/07 | Commerce | `E.4.7 GET /bills/{id}/qr` (QR render offline; khớp số tiền + cửa sổ) | `bill` · `match_result` | AC-2.3 · AC-2.6 · AC-2.8 | Bắt buộc |
| US-10 | EP-2 | «Ting ting» + biên lai NGAY khi tiền vào | F2 · F4 · S2 | NB-05 | Commerce (Ingest → khớp) · Notification | `B.1 POST /credit-events` (M4) · `E.5.1 GET /credit-events` · `E.8.3 POST /notifications/{id}/ack` | `credit_event` · `match_result` (kiêm biên lai) · `notification` | AC-2.1 | Bắt buộc |
| US-11 | EP-2 | SMS báo tiền về khi máy offline/hết pin | F2 · S2 | NB-05/13 | Notification | `D.5 POST /natcom/sms/v1/send` (N1) · `B.2 POST /sms-dlr` · `E.8.2` | `notification` | AC-2.2 | Bắt buộc |
| US-12 | EP-2 | Người mua quét QR & trả bằng ví của họ | F2 | VI-01→04 | (bên trả — NGOÀI MMS; đường tiền qua Switch) | — (không có endpoint MMS; nghiệm thu bằng test vectors QR TSD §12.1) | `credit_event` (hệ quả qua M4) | AC-2.5 | Bắt buộc (D9) |
| US-13 | EP-3 | Danh mục món + giá + ảnh | F3 | NB-06 | Commerce | `E.7.1` · `E.7.2 POST /products` · `E.7.3` · `E.9.2 POST /media` | `product` | AC-3.5 | Nên có |
| US-14 | EP-3 | Tick món (−/+), tổng tự cộng | F3 | NB-07 | Commerce | `E.4.3 POST /bills` | `bill` · `bill_item` · `product` | AC-3.1 · AC-3.5 | Nên có |
| US-15 | EP-3 | «Thu tiền» → QR đúng tổng bill | F3 · F4 | NB-07→04 | Commerce | `E.4.3` · `E.4.7` | `bill` · `match_result` | AC-3.1 · AC-3.2 | Nên có |
| US-16 | EP-3 | Đóng bill «tiền mặt» / hủy bill | F3 | NB-08 | Commerce | `E.4.5 POST /bills/{id}/close-cash` · `E.4.6 POST /bills/{id}/cancel` | `bill` | AC-3.4 | Nên có |
| US-17 | EP-3 | Bill trong ngày theo 3 nhóm + tổng | F3 | NB-08 | Commerce | `E.4.4 GET /bills?status&biz_date` | `bill` · `bill_item` | AC-3.1 · AC-3.3 | Nên có |
| US-18 | EP-4 | Ghi nợ khách quen ≤10 giây | F5 | NB-15 | Commerce | `E.6.2 POST /debtors` · `E.6.3 POST /debtors/{id}/entries` | `debtor` · `ledger_entry` | AC-4.1 | Bắt buộc |
| US-19 | EP-4 | Nhắc nợ 1 nút qua SMS | F5 | NB-15 | Commerce · Notification | `E.6.5 POST /debtors/{id}/remind` (→ `D.5` N1) | `ledger_entry` · `debtor` · `notification` | AC-4.4 | Bắt buộc |
| US-20 | EP-4 | Trả nợ bằng QR → app ĐỀ XUẤT gạch nợ | F5 · F4 · S7 | NB-15/05 | Commerce | `E.5.1` (`suggestion`) · `E.5.2 POST /credit-events/{id}/confirm-match` | `match_result` · `ledger_entry` · `credit_event` | AC-4.2 · AC-4.3 | Bắt buộc |
| US-21 | EP-4 | Sổ nợ chạy 100% không mạng | F5 | NB-15 | Commerce (qua tầng BFF Sync) | `E.9.1 POST /sync/batch` | `ledger_entry` · `debtor` | AC-4.1 | Bắt buộc |
| US-24 | EP-5 | Nhận biên lai qua SMS khi người bán gửi | F6 | NB-05/09 | Commerce · Notification | `E.5.5 POST /credit-events/{id}/send-receipt` (→ `D.5` N1) | `match_result` (biên lai) · `notification` | **AC-5.4** | Nên có |
| US-26 | EP-6 | Hàng đợi hậu kiểm hồ sơ có cờ, SLA ≤24h («v3.6») | F1 | BRH-03 | Merchant & Identity · Back-office (Admin) | `E.11.1 GET /admin/applications` · `E.11.2` · `E.11.3` · `E.11.4` | `application` · `ekyc_result` · `aml_alert` · `audit_log` | AC-6.1 | Bắt buộc |
| US-27 | EP-6 | Dashboard realtime + truy vết theo RefID | F2 · F8 | BRH-02/05 | Back-office (Admin) · Commerce · Back-office (Compliance) | `E.15.1 GET /admin/dashboard` · `E.12.1` · `E.12.2 GET /admin/transactions/{id}` | `credit_event` · `match_result` · `case` · `aml_alert` · `recon_run` | AC-6.3 | Bắt buộc |
| US-28 | EP-6 | Khóa/mở/đóng merchant + tracking standee | F1 · S8 | BRH-04 | Merchant & Identity | `E.11.5` · `E.11.6 suspend` · `E.11.7 resume` · `E.11.8 close` · `E.11.9 PATCH standee` · `E.15.2` | `merchant` · `standee` · `account_link` · `audit_log` | — (wireframe + audit) | Bắt buộc |
| US-29 | EP-6 | Báo cáo KPI pilot CSV/PDF (on-demand; email định kỳ HOÃN — S10) | — | BRH-08 | Back-office (Admin) | `E.13.1 GET /admin/reports/kpi` | `report` | AC-6.4 | Bắt buộc |
| US-30 | EP-6 | Sửa tham số theo cơ chế 4 mắt (vận hành Natcom qua API — không màn) | — | — | Back-office (Admin) | `E.13.2` · `E.13.3 PUT /admin/params/{key}` · `E.13.4 approve` | `param` · `audit_log` | AC-6.2 | Bắt buộc |
| US-31 | EP-6 | Tra cứu nhật ký bất biến (hash chain) | — | BRH-11/12 | Back-office (Admin) | `E.13.5 GET /admin/audit` (+ `E.13.6`–`E.13.8` người dùng) | `audit_log` · `app_user` | AC-6.5 | Bắt buộc |
| US-32 | EP-7 | Case khiếu nại + XÁC MINH chuyển trả trước «Đã hoàn» | F7 · S5 | BRH-06 · NB-09 | Back-office (Compliance) | `E.12.3` · `E.12.4` · `E.12.5` · `E.15.3` · `E.12.6 conclude` · `E.13.9` (4 mắt) (→ `C.5` M3) | `case` (chứng cứ JSONB) · `adjustment` · `credit_event` | AC-7.1 · AC-7.2 · AC-7.3 | Bắt buộc |
| US-33 | EP-8 | Hàng đợi cảnh báo AML kèm bối cảnh | F2 | BRH-07 | Back-office (Compliance) | `E.12.7 GET /admin/aml-alerts` (→ `D.2` E2) | `aml_alert` · `merchant` · `credit_event` | AC-8.1 · AC-8.2 | Bắt buộc |
| US-34 | EP-8 | Mọi quyết định AML bắt buộc ghi lý do | — | BRH-07 | Back-office (Compliance) | `E.12.8 POST /admin/aml-alerts/{id}/decide` | `aml_alert` · `audit_log` | AC-8.3 | Bắt buộc |
| US-35 | EP-9 | 1 màn biết bank nào trục trặc, token sắp hết hạn | F8 | AQ-00/01 | (ops — mọi connector) | `E.14.1 GET /ops/connections` · `E.14.2 GET /ops/tokens` · `E.14.4 GET /ops/health` | `token` · `account_link` · `credit_event` | AC-9.3 | Bắt buộc |
| US-36 | EP-9 | Đối soát cuối ngày + xử lệch ≤2 ngày làm việc | F8 · S6 | AQ-03/04 | Back-office (Compliance — đối soát + bút toán điều chỉnh — cùng dịch vụ) | `E.14.5` · `E.14.6` · `E.14.7 resolve` (→ `D.3` E3, `C.5` M3-poll) | `recon_run` · `discrepancy` · `adjustment` · `credit_event` | AC-9.1 · AC-9.2 | Bắt buộc |
| US-37 | EP-9 | Cảnh báo tự leo thang 5–30–60 phút | F8 | AQ-01 | Back-office (Admin — ngưỡng C12) · tầng Observability (hạ tầng, không phải dịch vụ) | `E.14.1` · `E.14.4` · `E.13.2` (ngưỡng từ `param`) | `param` · `notification` | AC-9.3 | Bắt buộc |
| US-38 | EP-10 | Quên PIN → lấy lại bằng OTP | F9 | NB-00 | Merchant & Identity | `E.1.2` · `E.1.3` · `E.1.7 POST /auth/pin/reset` | `person` · `auth_session` | **AC-10.2** | Bắt buộc |
| US-39 | EP-10 | Mất máy → khóa khẩn hotline 8686 | F9 | NB-00 | Merchant & Identity | `E.1.8 POST /auth/emergency-lock` | `auth_session` · `person` · `notification` | AC-10.1 | Bắt buộc |
| US-41 | EP-11 | Người mua quét QR & trả 1 chạm <3s «Peye-Haiti 15/08» | S9 | NM-01/02 | Commerce (Payment) | `E.16.1 POST /payments` · `E.16.2 confirm` (→ `C.7` M-PAY.1 · `B.4` kết quả) | `payment` · `account_link` · `person` | AC-11.1 | Bắt buộc (khi bật Client) |
| US-42 | EP-11 | Thấy TÊN người bán trước khi xác nhận (chống dán đè) | S9 | NM-02 | Commerce (Payment) | `E.16.1` (resolve trong response) | `payment` · `merchant` | AC-11.1 | Bắt buộc |
| US-43 | EP-11 | Thông báo kết quả + biên lai số | S9 | NM-03 | Commerce (Payment) · Notification | `E.16.3 GET /payments/{id}` · `B.4` | `payment` · `notification` | AC-11.2 · AC-11.3 | Bắt buộc |
| US-44 | EP-11 | Trang công khai xác minh merchant | — | web P.1 | Merchant & Identity | `P.1 GET /public/merchants/{code}` | `merchant` · `market` | AC-11.4 | Nên có |
| US-45 | EP-11 | Khiếu nại khoản đã trả trong app | S9 · F7 | NM-04 | Back-office (Compliance) | `E.16.5 POST /payments/{id}/dispute` | `case` · `payment` | AC-11.5 | Bắt buộc |
| US-46 «v3.5» | EP-1 | Chọn vai sau đăng ký [PILOT] + nút «Trở thành người bán» (làm nốt phần thiếu: eKYC2 · gian hàng · TK nhận) [**SAU PILOT** — user 20/08; pilot đổi vai qua kênh hỗ trợ] | F1 · S9 | CH-00 · hồ sơ | Merchant & Identity | `E.10.4 GET /me` (trạng thái vai) · E.2.x — không endpoint mới | `person` · `merchant` · `application` | AC-1.8 (sau pilot) | Chọn vai: Bắt buộc · Nâng cấp: sau pilot |
| US-40 | EP-2 | Đánh dấu «không phải doanh thu» | F2 | NB-05/09 | Commerce (module Ingest) · Back-office (KPI) | `E.5.6 POST /credit-events/{id}/revenue-flag` | `credit_event` (`is_revenue`, `non_revenue_reason`) | AC-2.7 | Nên có |

> Ghi chú US-40: theo PRD §4.3 (Q4) và AC-2.7 — khoản đánh dấu bị LOẠI khỏi doanh số NB-10/BRH-08 và khỏi KPI gạch tự động (TSD §6), nhưng **VẪN tính trong giám sát AML**.

---

## §2. Ma trận NGƯỢC — theo màn hình (42 màn — đã gồm CH-00 «v3.6»)

> «v3.5»: +**CH-00 Chọn vai** (sau OTP+PIN, trước eKYC; nâng cấp SAU pilot) → `E.10.4 GET /me` + E.2.x — đã có wireframe; NM đã có wireframe. NM-01 Quét & nhập tiền → `E.16.1` · NM-02 Xác nhận tên+nguồn → `E.16.2` · NM-03 Kết quả & biên lai → `E.16.3` · NM-04 Lịch sử & khiếu nại → `E.16.4`/`E.16.5` · NM-05 Liên kết TK trả → `E.3.x (holder=person)`. Bảng dưới liệt kê 36 màn NB/BRH/AQ/VI — CH-00 và NM tra ở ghi chú này.

Nguồn: API_Spec F.2 (endpoint × màn) · SSD §14 (màn → dịch vụ → tích hợp) · PRD §7 (US → màn).

### §2.1. App người bán — NB (17 màn)

| Màn | Nội dung | US | Endpoint (API_Spec) | Service · Tích hợp |
|---|---|---|---|---|
| NB-00 | Đăng nhập · quên PIN · khóa khẩn | US-38 · US-39 | `E.1.5` · `E.1.6` · `E.1.7` · `E.1.8` (+`E.1.2`/`E.1.3`) | Merchant & Identity · N1 |
| NB-01 | Đăng ký chung (SĐT · mã NAT-xxx — «v3.6» gian hàng khai ở NB-2B) | US-01 · US-06 | `E.1.1` (đã chốt: NB-01 là màn ĐĂNG KÝ — API_Spec F.2 đã sửa) | Merchant & Identity · N1 |
| NB-02 | OTP + tạo PIN | US-01 | `E.1.2` · `E.1.3` · `E.1.4` | Merchant & Identity · N1 |
| NB-2A | Chụp & nộp eKYC | US-02 | `E.2.1` · `E.2.2` | Merchant & Identity · E1 · E2 |
| NB-2B | Khai gian hàng («v3.6» — nộp cùng E.2.2) & liên kết TK nhận | US-01 · US-03 | `E.2.2` (phần gian hàng) · `E.3.1` · `E.3.2` · `E.3.3` | Merchant & Identity · M1 |
| NB-1C | Trạng thái hồ sơ · yêu cầu bổ sung | US-05 | `E.2.3` · `E.2.4` | Merchant & Identity · N1 |
| NB-03 | Trang chủ (tiền về hôm nay · tổng doanh số · hiển thị USD C5) | — (đặc tả bằng wireframe + UX-1..7) | `E.5.1` (tiền về hôm nay từ `credit_event`) · `E.8.1` (tổng doanh số) | Commerce (module Ingest — tiền về) · Back-office (doanh số) |
| NB-04 | QR tĩnh / QR động | US-08 · US-09 | `E.4.1` · `E.4.7` | Commerce (I2) |
| NB-05 | Két tiền — tiền về realtime · biên lai | US-10 · US-11 · US-20 · US-24 · US-40 | `E.5.1` · `E.5.2` · `E.5.5` · `E.5.6` | Commerce · Notification · **M4** · N1 |
| NB-06 | Danh mục món | US-13 | `E.7.1` · `E.7.2` · `E.7.3` · `E.9.2` | Commerce |
| NB-07 | Đơn tính tiền (tick món) → QR động | US-14 · US-15 | `E.4.3` · `E.4.7` | Commerce |
| NB-08 | Bill trong ngày (3 nhóm) | US-16 · US-17 | `E.4.4` · `E.4.5` · `E.4.6` | Commerce |
| NB-09 | Lịch sử · biên lai · báo sai · cờ doanh thu | US-24 · US-32 (xem «Đã hoàn») · US-40 | `E.5.3` · `E.5.4` · `E.5.5` · `E.5.6` | Commerce · Back-office (Compliance — báo sai) · M3 |
| NB-10 | Báo cáo bán hàng | — (wireframe + UX) | `E.8.1 GET /reports/sales` | Back-office (Admin — KPI) |
| NB-13 | Hộp thông báo | US-11 | `E.8.2` · `E.8.3` | Notification · N1 |
| NB-14 | Quản lý liên kết · đổi TK (S4) · standee · gia hạn token · ngôn ngữ | US-28 (standee) | `E.3.1` · `E.3.5` · `E.3.6` · `E.3.7` | Merchant & Identity · M1 · M1a · M1b |
| NB-15 | Sổ nợ (offline-first) | US-18 · US-19 · US-20 · US-21 | `E.6.1` · `E.6.2` · `E.6.3` · `E.6.4` · `E.6.5` | Commerce · N1 |
| (mọi màn NB) | Đồng bộ offline · upload ảnh · hồ sơ | US-21 · US-13 | `E.9.1` · `E.9.2` · `E.10.4` · `E.10.5` | tầng BFF → Commerce (đồng bộ) · Merchant & Identity (hồ sơ) |

### §2.3. Portal BRH (10 màn)

| Màn | Nội dung | US | Endpoint | Service · Tích hợp |
|---|---|---|---|---|
| BRH-01 | Đăng nhập 2FA (mật khẩu + TOTP) | US-31 (gián tiếp: quản lý user) | `E.1.9` · `E.1.10` | Back-office (Admin) |
| BRH-02 | Dashboard giám sát realtime | US-27 | `E.15.1` (drill-down → `E.11.1`, `E.12.4`, `E.12.7`, `E.14.6`) | Back-office (Admin) |
| BRH-03 | Hậu kiểm hồ sơ gian hàng | US-07 · US-26 | `E.11.1` · `E.11.2` · `E.11.3` · `E.11.4` | Merchant & Identity · E1 |
| BRH-04 | Quản lý merchant · standee · dòng hoạt động | US-28 | `E.11.5` · `E.11.6` · `E.11.7` · `E.11.8` · `E.11.9` · `E.15.2` | Merchant & Identity · **M1b** (khi đóng) |
| BRH-05 | Tra cứu & truy vết giao dịch theo RefID | US-27 | `E.12.1` · `E.12.2` | Commerce · Back-office (Compliance) |
| BRH-06 | Case: mở · hàng đợi · chứng cứ · bổ sung · kết luận | US-32 | `E.12.3` · `E.12.4` · `E.12.5` · `E.15.3` · `E.12.6` · `E.12.9` | Back-office (Compliance) · **M3** (xác minh hoàn) |
| BRH-07 | Cảnh báo AML | US-33 · US-34 | `E.12.7` · `E.12.8` | Back-office (Compliance) · E2 |
| BRH-08 | KPI & báo cáo (xuất on-demand) | US-29 | `E.13.1` | Back-office (Admin) |
| *BRH-09 — ĐÃ BỎ 04/08* | Tham số hệ thống chuyển sang vận hành Natcom qua API (4 mắt), không còn màn portal | US-30 · US-37 (ngưỡng) | `E.13.2` · `E.13.3` · `E.13.4` | Back-office (Admin) |
| BRH-11 | Audit log bất biến | US-31 | `E.13.5` | Back-office (Admin) |
| BRH-12 | Người dùng & phân quyền (RBAC 5 vai trò) | US-31 | `E.13.6` · `E.13.7` · `E.13.8` | Back-office (Admin) |

### §2.4. Console vận hành VDS — AQ (4 màn)

| Màn | Nội dung | US | Endpoint | Service · Tích hợp |
|---|---|---|---|---|
| AQ-00 | Đầu nối Open Banking · kho token · M3-poll | US-35 | `E.14.1` · `E.14.2` | Commerce (module Ingest) · Merchant & Identity (kho token) · M3 · M1a |
| AQ-01 | Tổng quan sức khỏe (nội bộ + đối tác) · cảnh báo trực ban · điểm đo T0→T1 | US-35 · US-37 | `E.14.4` · `E.14.1` | mọi connector · M-series · E · N |
| AQ-03 | Phiên đối soát E3 | US-36 | `E.14.5` | Back-office (Compliance) · **E3** · E3-reg |
| AQ-04 | Hàng đợi chênh lệch & xử lý | US-36 | `E.14.6` · `E.14.7` | Back-office (Compliance) · M3-poll |

### §2.5. Ví bên trả — VI (5 màn · tham chiếu, ngoài phạm vi xây)

| Màn | Nội dung | US | Endpoint | Ghi chú |
|---|---|---|---|---|
| VI-00 | «1 mã QR — mọi ví quét được» (lộ trình liên thông C21) | US-12 | — | Không gọi API MMS |
| VI-01 | Quét QR (SDK nhúng app wallet2 — C22) | US-12 | — | Nghiệm thu bằng test vectors QR (TSD §12.1) |
| VI-02 | Xác nhận trả (hiển thị tên gian hàng từ tag 59) | US-12 | — | D9 |
| VI-03 | Kết quả trả (phí liên ví C20 = 0 pilot) | US-12 | — | D9 |
| VI-04 | Biên lai bên trả | US-12 | — | Tiền về MMS qua **M4** (`B.1`) |

---

## §3. Ma trận NGƯỢC — theo bảng dữ liệu (28 bảng)

Quy tắc SSD §4 (4 dịch vụ) / DataDict §2 (5 schema PostgreSQL): **dịch vụ sở hữu là nơi DUY NHẤT ghi bảng của schema mình**; dịch vụ khác đọc qua REST nội bộ `/internal/*` hoặc sự kiện **Kafka**. Khớp tiền (`match_result` ↔ `bill` ↔ `ledger_entry` ↔ `match_result` (biên lai)) nay **cùng schema `commerce`** → một transaction nội bộ, **không còn lệnh ghi xuyên dịch vụ**.

| # | Bảng | Service sở hữu | US / luồng GHI vào | Endpoint chính (ghi / đọc) |
|---|---|---|---|---|
| 1 | `merchant` | Merchant & Identity | US-01, US-07, US-28 · F1/S1, S8 | Ghi: `E.2.2` («v3.6» — E.1.1 không còn tạo merchant), `E.11.2`, `E.11.6/7/8` · Đọc: `E.10.4`, `E.11.5`, `E.15.1` |
| 2 | `person` | Merchant & Identity | US-01, US-02, US-38 · F1, F9 | Ghi: `E.1.1`, `E.1.4`, `E.1.7`, `E.2.2` · Đọc: `E.1.5`, `E.10.4` |
| 4 | `auth_session` (kèm `fingerprint`, `is_agent_session`) | Merchant & Identity | US-06, US-38, US-39 · F1, F9 | Ghi: `E.1.4`, `E.1.5`, `E.1.6`, `E.1.7`, `E.1.8`, `E.13.8` · Đọc: nội bộ AuthN (gắn phiên với thiết bị, truy vết phiên hỗ trợ) |
| 5 | `ekyc_result` | Merchant & Identity | US-02 · F1/S1 | Ghi: `E.2.2` (kết quả `D.1` E1) · Đọc: `E.2.3`, `E.11.1` |
| 6 | `account_link` | Merchant & Identity | US-03, US-28 · S1, S4, S8 | Ghi: `E.3.3`, `E.3.5`, `E.11.8` (→ `C.1-C.2` M1 · `C.4` M1b) · Đọc: `E.3.1`, `E.4.1`, `E.14.2`, `D.4` E3-reg |
| 7 | `token` | Merchant & Identity | US-03 · S4 | Ghi: `E.3.3`, `E.3.7` (→ `C.2` M1 · `C.3` M1a) · Đọc: `E.14.2` |
| 8 | `standee` | Merchant & Identity | US-08, US-28 · S8, S4 | Ghi: `E.11.2` (sinh lệnh in), `E.11.9`, `E.3.6` · Đọc: `E.11.5` |
| 9 | `credit_event` | Commerce (module Ingest) | US-10, US-40 · F2/S2 (dedup 2 tầng) | Ghi: **`B.1`** (M4), `C.6` (M3-poll), `E.5.6` (`is_revenue`) · Đọc: `E.5.1`, `E.12.1`, `E.14.5` · Khớp đích danh: `B.5` cấp `payment_ref` → `B.1 addenda.payment_ref` («16/08») |
| 11 | `match_result` (kiêm biên lai) | Commerce | US-10, US-15, US-20 · F4/S2, S7 | Ghi: **transaction nội bộ Commerce** (nghe `credit.received`), `E.5.2` (MANUAL) · Đọc: `E.5.1`, `E.12.1`, KPI `E.13.1` · biên lai: Ghi trong transaction khớp + `E.5.5` (sent_msisdn) · Đọc: `E.5.3` |
| 12 | `product` | Commerce | US-13 · F3 (hậu kiểm C9) | Ghi: `E.7.2`, `E.7.3`, `E.9.1` · Đọc: `E.7.1` |
| 13 | `bill` | Commerce | US-14…US-17 · F3/S3 (`paid` CHỈ server) | Ghi: `E.4.3`, `E.4.5`, `E.4.6`, `E.9.1`, **transaction khớp nội bộ Commerce** (`status`→`paid`) · Đọc: `E.4.4`, `E.8.1` |
| 14 | `bill_item` | Commerce | US-14 · F3 | Ghi: `E.4.3`, `E.9.1` · Đọc: `E.4.4` |
| 15 | `debtor` | Commerce | US-18, US-21 · F5 | Ghi: `E.6.2`, `E.9.1` · Đọc: `E.6.1` |
| 16 | `ledger_entry` | Commerce | US-18, US-20, US-21 · F5/S7 | Ghi: `E.6.3`, `E.9.1`, **transaction khớp nội bộ Commerce** (gạch nợ `origin=auto`) · Đọc: `E.6.4` |
| 18 | `case` (kèm chứng cứ JSONB) | Back-office (Compliance) | US-32, US-36 · F7/S5 | Ghi: `E.5.4`, `E.12.3`, `E.12.6`, `E.15.3`, `E.14.7` (`to_case`) · Đọc: `E.12.4`, `E.12.9` |
| 19 | `adjustment` | Back-office (Compliance) | US-32, US-36 · S5, S6 (4 mắt) | Ghi: `E.12.6` (nháp), `E.14.7` (`action=adjust`), `E.13.9` (duyệt→posted) · Đọc: `E.13.9` |
| 20 | `aml_alert` | Back-office (Compliance) | US-07, US-33, US-34 · F2 (`limit.breached`) | Ghi: `D.2` E2 hit, Commerce phát `limit.breached` (hậu kiểm hạn mức), `E.12.8` · Đọc: `E.12.7`, `E.15.1` |
| 21 | `recon_run` | Back-office (Compliance) | US-36 · F8/S6 | Ghi: `B.3` (E3 push), `D.3` (E3 pull) · Đọc: `E.14.5` |
| 22 | `discrepancy` | Back-office (Compliance) | US-36 · F8/S6 | Ghi: Session Reconciler, `E.14.7` · Đọc: `E.14.6`, `E.15.1` |
| 23 | `param` | Back-office (Admin) | US-30, US-37 · vận hành Natcom 4 mắt (màn BRH-09 đã bỏ) | Ghi: `E.13.3` (maker), `E.13.4` (checker) · Đọc: `E.13.2` + mọi service (cache `param.changed`) · kiêm danh mục agent hiện trường NAT-xxx (`E.1.1` validate) |
| 24 | `market` | Back-office (Admin) | — (seed 3 TP · 9 chợ) | Ghi: migration `0002_seed_market.sql` · Đọc: `E.2.2` (validate `market_id` «v3.6»), `E.11.1` |
| 25 | `app_user` | Back-office (Admin) | US-31 · BRH-12 | Ghi: `E.13.7`, `E.13.8` · Đọc: `E.13.6`, `E.1.9`/`E.1.10` |
| 26 | `audit_log` | Back-office (Admin) | US-31 · mọi sự kiện CÓ actor | Ghi: Audit Writer (append-only, hash chain) · Đọc: `E.13.5` |
| 27 | `notification` | Notification | US-10, US-11, US-19 · I5 | Ghi: Notification (`match.completed`, `token.*`, `case.*`), `B.2` (DLR) · Đọc: `E.8.2`, `E.8.3` |
| 28 | `report` | Back-office (Admin) | US-29 · job `kpi-*` | Ghi: job KPI (chốt theo ngày đối soát) · Đọc: `E.13.1`, `E.8.1` |
| 29 | `idem_key` | shared (hạ tầng API) | — (mọi POST ghi) | Ghi/Đọc: middleware Idempotency (TTL 48h) |
| 30 | `application` | Merchant & Identity «v1.1» | US-02, US-05, US-07, US-26 · F1/S1 | Ghi: `E.2.2`, `E.2.4`, `E.11.2/3/4` · Đọc: `E.2.3`, `E.11.1` |
| 31 | `payment` «Peye-Haiti 15/08» | Commerce (module Payment) | US-41, US-42, US-43, US-45 · S9 | Ghi: `E.16.1`, `E.16.2`, `B.4`, job `PAY_TIMEOUT` · Đọc: `E.16.3`, `E.16.4` |

---

## §4. Ma trận TÍCH HỢP (12 giao diện ngoài)

Nhóm **M** = bank/ví NHẬN cung cấp · **E** = BRH/Switch · **N** = Natcom. (I2/I5 = năng lực nội bộ MMS, không phải giao diện ngoài. M2/M6/M6b/N2 = **không sử dụng** — TSD §2.)

| Mã | Tên | US / luồng dùng | Endpoint (API_Spec) | Phụ thuộc | Degrade nếu interface CHẾT |
|---|---|---|---|---|---|
| **M1** | Liên kết TK → token (2 bước + OTP chủ TK) | US-03 · F1/S1, S4 | `C.1 POST /ob/v1/links` · `C.2 .../confirm` (BFF: `E.3.2`, `E.3.3`) | **D2** | Không onboard được merchant mới (chặn F1 bước 7); merchant đã liên kết KHÔNG ảnh hưởng — tiền vẫn về, vẫn «ting ting». `PIN-503-DEP`, circuit breaker |
| **M1a** | Gia hạn token (job D-7) | US-03 · S4 · AQ-01 | `C.3 POST /ob/v1/tokens/refresh` (BFF: `E.3.7`) | D2 | Token hết hạn → mất M3/M4 theo link; cảnh báo `token_expiring_7d` >20 tại AQ-00; buộc re-link (`E.3.2`) |
| **M1b** | Thu hồi token (đổi TK/đóng/gian lận) | US-28 · S4 ⑤, S8 | `C.4 POST /ob/v1/tokens/revoke` (BFF: `E.11.8`) | D2 | TK cũ tiếp tục nhận M4 quá hạn grace (rác dữ liệu); đóng merchant không sạch → xử tay + ghi case |
| **M3** | Lịch sử giao dịch (bằng token) | US-32 (xác minh hoàn) · US-36 · NB-03/09 | `C.6 GET .../transactions` | D2 | Mất fallback M3-poll; **không xác minh được hoàn tiền qua `m3`** → `E.12.6` buộc `method=document`; đối soát phải dựa hoàn toàn E3 |
| **M4** | **Webhook báo có realtime (kèm NGƯỜI TRẢ)** — ĐƯỜNG GĂNG | US-10, US-11, US-20, US-40 · F2/S2, F4 | `B.1 POST /credit-events` (MMS expose) | **D2** (SLA P95 ≤5s) | **Mất «ting ting»** → chuyển **M3-poll 5 phút/lần** (trễ báo có, phá AC-2.1) + **đối soát E3** bù; tiền VẪN về (MMS ngoài đường tiền) |
| **E1** | eKYC CIN+selfie ↔ ONI | US-02, US-05, US-07 · F1/S1 | `D.1 POST /brh/ekyc/v1/verify` | **D3** | Runbook: hồ sơ vào hàng đợi + **duyệt tay ảnh CIN** tại BRH-03; `e1_error_rate>5%/15'` → cảnh báo trực ban ≤5 phút (AC-9.3) |
| **E2** | Sàng lọc AML | US-07, US-33 · F1, giám sát | `D.2 POST /brh/aml/v1/screen` | — (BRH có sẵn) | 5xx lúc onboarding «v3.6»: KHÔNG chặn kích hoạt — gian hàng vẫn active + cờ `e2_deferred`, sàng lọc BÙ khi E2 về; monitoring: retry job sau |
| **E3** | Bảng kê EOD từ Switch (3 phiên/ngày) | US-36 · F8/S6 | `D.3 GET /switch/v1/eod` (pull) · `B.3 POST /eod-notifications` (push) | **D10** | Thiếu file >2h → cảnh báo AQ-01, **đối soát dời phiên**; chuyển **SFTP dự phòng**; số liệu KPI `settled_through` lùi lại |
| **E3-reg** | Đăng ký danh mục TK NHẬN để Switch lọc EOD | US-03, US-28 · S4, S6 | `D.4 PUT /switch/v1/account-registry` | D10 | Switch gửi file **chưa lọc** → MMS tự lọc, hủy phần thừa (chế độ quá độ); rủi ro lộ dữ liệu TK ngoài phạm vi |
| **N1** | SMS liên mạng (OTP · báo có · nhắc nợ) | US-01, US-11, US-19, US-24, US-26, US-39 | `D.5 POST /natcom/sms/v1/send` · DLR `B.2` | **D6** | Runbook: **OTP thoại** (thủ tục Natcom); báo có **chỉ còn push** (AC-2.2 FAIL với máy offline); nhắc nợ US-19 dừng |
| **M-PAY** «v3.5» | Khởi tạo lệnh trả + trạng thái + xác nhận OTP (định chế TRẢ) | US-41, US-42, US-43 · S9 | `C.7 POST /ob/v1/payments` · `C.8 GET /ob/v1/payments/{id}` · `C.9 POST /ob/v1/payments/{id}/sca` | D2 (phụ lục M-PAY; định chế có SMS GW gửi OTP — F.4 điều 6) | Chưa ký phụ lục → profile Client KHÔNG bật; người mua vẫn trả bằng app ví (VI-01→04), người bán không ảnh hưởng |
| **M-PAY-hook** «Peye-Haiti 15/08» | Webhook kết quả trả (định chế TRẢ → MMS) | US-43 · S9 | `B.4 POST /payment-results` | D2 (phụ lục M-PAY) | Webhook sót → job hỏi lại `C.8` sau `PAY_TIMEOUT`; không bao giờ tự tạo lệnh mới |
| **B.5 /qr-inquiry** «16/08» | App định chế TRẢ tra cứu xác minh QR vào nền tảng (tên/trạng thái merchant + bill + `payment_ref`) | US-41, US-42 · S2/S9 | `B.5 POST /qr-inquiry` | D2 | Không gọi được → app định chế vẫn trả như cũ (offline-first A9); khớp rơi về mức số tiền + cửa sổ |

---

## §5. Ma trận KIỂM THỬ — theo acceptance criteria (45 hàng, cơ sở kịch bản UAT)

Loại test: **U** unit · **CT** contract (sandbox đối tác) · **SIT** tích hợp · **UAT** BRH nghiệm thu · **PERF** tải/soak · **DR** diễn tập sự cố.

| AC | US | Loại | Tiền điều kiện | Cách đo (số liệu từ AC) |
|---|---|---|---|---|
| AC-1.1 | US-01 | UAT · PERF | Người mới, CIN hợp lệ; E1 sandbox (D3); M1 sandbox (D2) | Đo funnel `onb.step` (TSD §13.2) bước 1→8: **tổng thao tác ≤10 phút**; kết thúc ở trạng thái «KÍCH HOẠT» ngay khi hoàn tất («v3.6» — không còn «chờ duyệt») |
| AC-1.2 | US-02, US-05 | CT · SIT | E1 sandbox trả `E1-422-QUALITY` cho ảnh mờ | NB-1C (`E.2.3`) chuyển `need_more` + SMS; `E.2.4 resubmit` chỉ gửi ảnh cần sửa — **KHÔNG nhập lại thông tin** |
| AC-1.3 | US-03 | CT · SIT | Người bán nhập số TK KHÔNG thuộc mình; bấm liên kết (`E.3.2`) | Bank gửi OTP tới SĐT chủ TK thật → người bán không có OTP → `E.3.3` thất bại, **KHÔNG cấp token** (kiểm bảng `token` rỗng) |
| AC-1.4 «v3.6» | US-07 | SIT · UAT | Hoàn tất tạo gian hàng (eKYC PASS + TK nhận) | `active` NGAY ≤5s, QR + lệnh standee sinh tức thời, KHÔNG hàng đợi duyệt; hồ sơ cờ (điểm thấp/AML hit/E2 bù) → hậu kiểm ≤24h, suspend 1 chạm; mẫu 10% hồ sơ sạch |
| AC-1.5 | US-06 | SIT · UAT | Phiên đăng ký hộ với `agent_code=NAT-014` | `merchant.agent_code` = NAT-014; `auth_session.is_agent_session=true` — phiên hỗ trợ đánh dấu riêng, tách bạch với phiên của merchant |
| AC-2.1 | US-08, US-10 | PERF (soak 72h) | Merchant đã kích hoạt; M4 sandbox/prod; đo tại AQ-00 | **95% giao dịch** có «ting ting»/biên lai trong **≤5 giây** kể từ T0 (bank ghi Có) → T1 (app ack); `credit_notify_latency_p95 ≤ 5s` |
| AC-2.2 | US-11 | SIT | App merchant offline (không ack); N1 sandbox | Không ack trong **60 giây** → gửi SMS; SMS tới máy trong **≤60 giây tiếp theo** (đối chiếu DLR `B.2`) |
| AC-2.3 | US-09 | U · SIT | QR động 1.500 G; khách sửa số tiền khác | Tiền vẫn vào `credit_event` nhưng **KHÔNG tự gạch bill** (`AMOUNT_TOLERANCE=0`) → rơi `PENDING`/xác nhận tay |
| AC-2.4 | US-08 | SIT (quy trình đổi TK S4) | Merchant đổi TK nhận qua `E.3.5` | QR mới (`qr_version`+1) + lệnh in standee mới; TK cũ `status=grace` **≥30 ngày** (`OLD_LINK_GRACE`) — tiền QR cũ vẫn về + ting ting + gạch bill; app nhắc thay standee tới khi `E.3.6` |
| AC-2.5 | US-12 | CT (D9) | Ví wallet2 bản go-live; bộ test vectors QR (TSD §12.1) | Quét **3 vector hợp lệ** (tĩnh / động có tiền / động + addenda bill_id): hiển thị đúng tên gian hàng, **trả thành công cả 3**; từ chối vector sai chuẩn |
| AC-2.6 | US-09 | U | QR động quá `QR_DYNAMIC_TTL` (15 phút) | App bên trả báo **mã hết hạn**; merchant tạo lại bằng **2 chạm** |
| AC-2.7 | US-40 | U · SIT | Khoản tiền về không phải bán hàng | `E.5.6 revenue-flag` → loại khỏi doanh số `E.8.1`/`E.13.1` và KPI matching; **VẪN vào giám sát AML** (kiểm `aml_alert` vẫn cộng) |
| AC-2.8 | US-08, US-09 | SIT (offline) | Máy mất mạng hoàn toàn (airplane mode) | QR động hiển thị **ngay** (render offline); khách quét trả bình thường; tiền về vẫn có thông báo khi app online lại / qua SMS |
| AC-3.1 | US-14, US-15, US-17 | U · SIT | Bill 2 món tổng **2.140 G**; tiền về đúng 2.140 G trong đời bill | Bill tự `paid`; tổng ngày khớp ở **NB-08 (`E.4.4 summary`) = NB-09 = NB-10 (`E.8.1`)** — một nguồn số liệu |
| AC-3.2 | US-15 | U (matching) | 2 bill cùng mở, cùng số tiền | Hệ thống **KHÔNG tự đoán** → `PENDING` chờ merchant chọn; ngoại lệ: chỉ 1 bill tạo trong **±15 phút** (`MATCH_LOOKBACK`) quanh `booked_at` |
| AC-3.3 | US-17 | U (job) | Bill `open` quá **24 giờ** (`BILL_TTL`) | NB-08 hiện `expired` + nút tạo lại (job server, giờ server) |
| AC-3.4 | US-16 | SIT | Khách trả tiền mặt | `E.4.5 close-cash` → `status=cash`; **KHÔNG lẫn** vào dòng tiền QR/đối soát bank (kiểm `E.14.5` không đếm) |
| AC-3.5 | US-13, US-14 | SIT (offline) | Máy offline; tạo bill/danh mục | Thao tác hoàn tất **ngay trên máy**; tự đồng bộ `E.9.1` khi có mạng; **không mất dữ liệu khi tắt app** |
| AC-4.1 | US-18, US-21 | UAT (bấm giờ) | Máy đang offline | Ghi nợ/ghi trả xong **≤10 giây**; dữ liệu còn nguyên sau tắt-mở app (IndexedDB mã hóa) |
| AC-4.2 | US-20 | U (S7) | Nợ **900 G** của Jean; tiền về 900 G không khớp bill nào | App đề xuất «gạch nợ Jean?» (`E.5.1 suggestion`) — **chỉ gạch khi merchant xác nhận** (`E.5.2`) |
| AC-4.3 | US-20 | U (idempotency) | Merchant đã gạch tay khoản nợ lúc offline; báo có tự động về sau | **KHÔNG trừ nợ lần hai** — đối chiếu `ledger_entry.client_uuid` + `credit_event_id` |
| AC-4.4 | US-19 | SIT (N1) | Bấm nút nhắc nợ; debtor có `msisdn` | SMS mẫu (Creole/FR) tới khách **≤10 giây**; tối đa **1 tin/khách/ngày** (`BIZ-REMIND-LIMIT`) |
| **AC-5.4** | US-24 | SIT (N1) | Merchant bấm «gửi biên lai cho khách» tại NB-05/09; N1 sandbox; nhập SĐT người mua | SMS biên lai (mã GD · số tiền · tên gian hàng · giờ) tới **≤30 giây** (đối chiếu DLR `B.2`); vượt **5 SMS/giờ/merchant** (`SMS_RATE_LIMIT`) → `PIN-429-RATE`; gọi `E.5.5` lần 2 cho **cùng `credit_event`** KHÔNG sinh SMS trùng (idempotent) |
| AC-6.1 | US-26 | SIT · UAT | Ca hồ sơ cờ vàng; cán bộ từ chối | Bắt buộc `reason` (`BIZ-REASON-REQUIRED`); merchant nhận SMS + NB-1C đổi trạng thái; **audit ghi vết** |
| AC-6.2 | US-30 | U | Người đề xuất tự phê duyệt tham số «phí pilot» | Hệ thống **chặn** — `BIZ-FOUR-EYES` (bắt buộc người thứ hai) |
| AC-6.3 | US-27 | UAT | Một giao dịch bất kỳ, tra theo RefID tại BRH-05 | `E.12.2 timeline[]` hiện **chuỗi đầy đủ trong 1 màn**: `booked → received → deduped → matched → notified → receipt_created → case_*` |
| AC-6.4 | US-29 | SIT | Cán bộ bấm xuất báo cáo tuần (`E.13.1`) | Tải CSV/PDF; số liệu **CHỐT theo `settled_through`** (không lệch BRH-02 quá số GD chưa chốt) |
| AC-6.5 | US-31 | SIT (job đêm) | Mọi bản ghi `audit_log` | Job `audit-verify` kiểm chuỗi hash hằng đêm → **không đứt gãy**; `E.13.5 chain.verified=true` |
| AC-7.1 | US-32 | U · SIT | Kết luận «hoàn» chưa có xác minh chuyển trả | `E.12.6` trả `BIZ-REFUND-UNVERIFIED` — **không thể đánh «Đã hoàn» tay không** |
| AC-7.2 | US-32 | SIT | Case quá `CASE_SLA_FIRST` (24h) / `CASE_SLA_CLOSE` | Case **nổi đỏ** trên BRH-02 (`E.15.1 alerts[]`, `overdue=true`) + email nhắc người phụ trách |
| AC-7.3 | US-32 | SIT | Case chốt `concluded_refund` | NB-09 (`E.5.3`) hiện `status=refunded` + `refund_case_code`; **doanh số ngày đã trừ đúng** (`E.8.1 totals.refunded_ct`) |
| AC-8.1 | US-33 | SIT | Merchant nhận **>500.000 G/ngày** (`AML_DAY_FLAG` 50.000.000 ct) | Tự sinh `aml_alert(rule_code=AML_DAY_FLAG)` + **gắn cờ hạn chế gian hàng** (`merchant_flag`) + mở case AML tới khi xử lý |
| AC-8.2 | US-33 | U (rule) | **≥5 giao dịch trong dải 80–100% ngưỡng `AML_TX_FLAG` / 24h** (`AML_SMURF={count≥5, band 0.80–1.00}`) — số liệu test SINH TỪ THAM SỐ, không hard-code | Sinh cảnh báo «nghi chia nhỏ» **đúng ca này** (không false-negative, không sinh với 4 GD, không sinh khi GD ngoài dải) |
| AC-8.3 | US-34 | U | Quyết định «bỏ qua» (`dismiss`) thiếu lý do | `E.12.8` **từ chối lưu** — `BIZ-REASON-REQUIRED` |
| AC-9.1 | US-36 | DR (diễn tập) | Webhook bank ngừng **30 phút** rồi phục hồi | **M3-poll lấp khoảng** lấy về đủ sự kiện + **E3 đối soát bù**, **không tạo trùng** (dedup `event_id`/`ref_id`) — không backfill bằng bank |
| AC-9.2 | US-36 | SIT · UAT | 1 khoản lệch `missing_in_mms` (Switch có – MMS không thấy) | Đóng **≤2 ngày làm việc** (`DISCREPANCY_SLA`) + `resolution` có **vết đầy đủ** (nguyên nhân → hành động) |
| AC-9.3 | US-35, US-37 | DR · SIT | Dịch vụ E1 lỗi **>5%/15 phút** (`e1_error_rate`) | Trực ban nhận cảnh báo **≤5 phút**; luồng đăng ký tự chuyển chế độ **«chờ đối chiếu tay»** |
| AC-10.1 | US-39 | SIT | Lệnh khóa khẩn qua hotline 8686 (OTP về SIM đăng ký) | Mọi phiên đăng nhập thu hồi **≤60 giây**; **QR vẫn nhận tiền**; SMS xác nhận gửi về |
| **AC-10.2** | US-38 | SIT · UAT (bảo mật) | Người dùng quên PIN, yêu cầu đặt lại | Bắt buộc OTP gửi về SIM đăng ký; đặt lại xong mọi phiên cũ thu hồi (kiểm bằng refresh cũ → 401) |
| AC-11.1 «v3.5» | US-41 · US-42 | SIT · PERF (sandbox M-PAY) | Quét QR HTQR hợp lệ ở NM-01 | App hiện TÊN người bán + số tiền; HAI BẬC: ≤5.000 chỉ PIN · >5.000 +OTP định chế (`PAY_SCA_THRESHOLD`); trần ngày chỉ bậc-PIN; kết quả cuối **≤3s P95** (`PAY_CONFIRM_SLA` — nhánh OTP tính lại từ lúc nộp OTP); định chế chậm → «đang xử lý», không treo |
| AC-11.2 | US-43 | SIT | Định chế trả từ chối (thiếu số dư/hạn mức/`sca_failed` sai OTP quá lần «v3.5») | Lý do bản địa hóa từ `failure_reason`; KHÔNG sinh biên lai; lịch sử hiện «thất bại» |
| AC-11.3 | US-43 | SIT · UAT | Thanh toán thành công | Người mua nhận thông báo + biên lai số; người bán vẫn nhận «ting ting» qua M4 và gạch bill như S2 |
| AC-11.4 | US-44 | SIT | Mở trang công khai P.1 | Tên, ngành, chợ/TP, SĐT công khai (nếu opt-in) + nhãn «Đã xác thực»; KHÔNG lộ số TK/doanh số; `suspended` hiện cảnh báo |
| AC-11.5 | US-45 | SIT · UAT | Khiếu nại khoản đã trả ở NM-04 | Sinh case nguồn `buyer_app` (kèm `case.payment_id`), SLA phản hồi đầu `CASE_SLA_FIRST` (24h); người mua theo dõi được trạng thái |
| AC-11.6 «vòng 2» | US-41 | SIT (chaos mạng) | Mất mạng giữa confirm và kết quả | Online lại: app chỉ poll E.16.3, không sinh lệnh mới (nhánh OTP: mở lại trạng thái nhập OTP nếu còn hạn «v3.5»); lệnh trùng đích khi lệnh cũ chưa chốt bị chặn `PIN-409-STATE` (TSD §6b) |
| AC-1.8 «v3.5 — SAU PILOT» | US-46 | SIT · UAT (giai đoạn sau pilot) | Người mua bấm «Trở thành người bán», hoàn tất phần vai bán còn thiếu | App chuyển giao diện vai bán ≤5s sau merchant `active`, không đăng nhập lại; chức năng thanh toán giữ nguyên |

> **Cổng go-live (PRD §13)** — kịch bản tổng hợp cần chạy: 100% F1–F9 pass UAT · gạch tự động **≥95%** · báo có **≤5s P95 đo 72h liên tục** · diễn tập rơi webhook (phục hồi M3-poll + E3) / E1 gián đoạn / hàng đợi lệch · pentest OWASP ASVS L2 không còn lỗi nghiêm trọng · **≥90% standee đã dán** · Go/No-Go trước 25/9/2026 với D1–D11 hoàn thành.

---

## §6. Ma trận NFR & tham số

| NFR (PRD §9) | Cơ chế (SSD §10 · TSD §10) | Ngưỡng đo | Param liên quan (TSD §13.3) |
|---|---|---|---|
| Báo có ≤5s P95 | T0 = `booked_at` (bank) trong M4; T1 = app ack (`E.8.3`) hoặc N1 nhận gửi SMS; P95 trượt 24h tại AQ-00 | `credit_notify_latency_p95 > 5s trong 5'` → page trực ban | — (đo, không cấu hình) · liên quan `SMS_RATE_LIMIT` |
| Xác nhận trả người mua ≤3s P95 «Peye-Haiti 15/08» | Đo T0 = bấm xác nhận (E.16.2) → T1 = kết quả cuối tới app; webhook B.4 + fallback hỏi C.8 | `pay_confirm_p95 > 3s trong 15'` → xem SLA định chế trả | `PAY_CONFIRM_SLA=3s` · `PAY_TIMEOUT=60s` |
| Khả dụng 99,5% | Synthetic 1 phút/lần, **5 hành trình vàng** (login · qr · credit_notify · sync · report) tại `E.14.4`; downtime = phút có ≥1 fail | fail ≥1 hành trình → tính downtime + page | — |
| Hiệu năng **50 TPS nhận tiền về** (= 3.000 GD/phút) + **300 rps API** · quy mô **5.000 merchant** | Ingest stateless + HPA, phân vùng Kafka theo `merchant_id`; load test k6 30' vào `B.1` | P95 accept **<2s**, không mất sự kiện (đối chiếu count) | — |
| Quy mô **5.000 merchant** | Sizing TSD §9 (PROD 24 VM · UAT 8 VM · sao lưu thay DR); partition RANGE thiết kế sẵn; read-replica | Headroom ≥2× đỉnh burst; **vượt 5.000** → thêm replica/broker, >20.000 → tách cụm PG Ingest/Commerce (TSD §9.5) | — |
| Gạch bill tự động ≥95% | Khớp tiền 2 mức (module Khớp tiền của Commerce — TSD §6); KPI = `LINK / (không tính STRAY, PENDING, non-revenue)` | `match_auto_rate < 95%/ngày` → xem backlog PendingManual | `AMOUNT_TOLERANCE=0` · `MATCH_LOOKBACK=15'` · `BILL_TTL=24h` · `STRAY_AFTER=72h` |
| Offline-first | IndexedDB mã hóa AES-GCM (khóa từ PIN/PBKDF2); `E.9.1 sync/batch`; ma trận transition bill (client KHÔNG set `paid`) | Batch ≤200 entries/500KB; hàng đợi client ≤2.000 (cảnh báo NB-14); ảnh ≤200KB | `QR_DYNAMIC_TTL=15'` · `BILL_TTL=24h` |
| Funnel <10 phút · kích hoạt tức thời «v3.6» · hậu kiểm cờ ≤24h | Instrument `onb.step{step,ms}` từng bước NB-01→CH-00→2B; `onb.submit→activate` (≈0) | Báo cáo BRH-08 (`E.13.1 kpis.onboarding`) | `AUTO_ACTIVATE_SCORE=0.85` (ngưỡng GẮN CỜ — hậu kiểm; mẫu 10%) |
| Bảo mật — PIN/OTP | PIN 6 số Argon2id (m=64MB,t=3,p=1), khóa 60' sau 5 lần sai; OTP constant-time | `BIZ-PIN-LOCKED` · `BIZ-OTP-LIMIT` | `OTP_TTL=120s` · `OTP_MAX_PER_DAY=5` |
| Bảo mật — kênh & khóa | mTLS TLS1.2+; thẻ hệ thống tự ký A.1b kèm `body_sha256` (hash body — Bearer mọi chiều, «v3.4»); thẻ RESPONSE tài chính F.3 (`x-jws-signature`); JWKS không `kid`, xoay khóa chồng lấp 7 ngày, cache 1h; Vault envelope AES-256-GCM, xoay KEK 12 tháng | `PIN-401-JWS`; kid rotation 90 ngày | `TOKEN_RENEW_BEFORE=7 ngày` |
| Bảo mật — RBAC & 4 mắt | 5 vai trò (C11), không vai trò nào vừa tạo vừa duyệt; 4 mắt cho phí/hạn mức/bút toán | `BIZ-FOUR-EYES` (AC-6.2) | — (`/docs/rbac.csv`) |
| Bảo mật — audit | Append-only + hash chain `SHA256(prev_hash ‖ canonical_json)`; job `audit-verify` đêm | Không đứt gãy chuỗi (AC-6.5) | — (retention 10 năm — C17) |
| Giám sát hạn mức (hậu kiểm AML) | Tổng nhận ngày chạm `AML_DAY_FLAG` → MMS phát `limit.breached`; mọi merchant eKYC đầy đủ — không còn chặn cứng theo bậc ở bank | Vượt → `aml_alert` + gắn cờ hạn chế (AC-8.1) | `AML_DAY_FLAG=50.000.000 ct/ngày` |
| AML ngưỡng | Rule Engine: E2 + ngưỡng C14 + chống chia nhỏ | Cảnh báo BRH-07 | `AML_TX_FLAG=10.000.000 ct/GD` · `AML_DAY_FLAG=50.000.000 ct/ngày` · `AML_SMURF={count≥5, band 0.80–1.00}` |
| SLA case & đối soát | Đồng hồ SLA đếm ngược; đóng lệch theo phiên | Case quá hạn nổi đỏ (AC-7.2); lệch đóng ≤2 ngày (AC-9.2) | `CASE_SLA_FIRST=24h` · `CASE_SLA_CLOSE=5 ngày làm việc` · `DISCREPANCY_SLA=2 ngày làm việc` |
| Cutover TK nhận | Trình tự S4 (5 bước, trong Merchant & Identity); TK cũ giữ liên kết & nhận M4 | Grace ≥30 ngày (AC-2.4) | `OLD_LINK_GRACE=30 ngày` |
| Phí pilot | Tham số 4 mắt (vận hành Natcom, E.13.x) | 0% đến 31/12/2026 | `FEE_PILOT=0` |
| Riêng tư | Thông tin người trả theo chuẩn OB BRH; sổ nợ thuộc merchant (consent C7); ảnh eKYC MinIO mã hóa, TTL truy cập | PII 🔒 che khi hiển thị, không log rõ | — (retention: eKYC 5 năm sau đóng gian) |
| Ngôn ngữ | App FR + Creole (`.po`); chọn ngay màn đầu (UX-4), đổi tại NB-14 | `Accept-Language: fr\|ht` | — (C8) |

---

## §7. Bảng phụ thuộc & rủi ro chặn (D1–D11)

| # | Phụ thuộc | Hạn · Chủ trì | Ảnh hưởng tới US / luồng | Hệ quả nếu TRỄ | Phương án degrade |
|---|---|---|---|---|---|
| D1 | Chuẩn QR quốc gia (copy bộ Napas) ban hành | 31/7/2026 · BRH (VDS tư vấn) | US-08, US-09, US-12 · F2/S3 · AC-2.5, AC-2.6 | Payload QR chưa chuẩn hóa (tag 38 AID, danh mục bank); ví bên trả không nghiệm thu được | §13.4 đã theo **HTQR 1.0 dự thảo v0.9.1** (trình G3 15/08 — CR-3); nếu BRH chỉnh khi ban hành chính thức, chỉ thay GUID/sub-tag, **không đổi kiến trúc**; pilot nội bộ wallet2 trước |
| D2 | Bộ API Open Banking + SLA (M1/M1a/M1b/M3/M4), **M4 kèm người trả** | Ký T7/2026 · Natcom/VDS | US-03, US-10, US-11, US-20, US-32, US-36 · F1, F2, F4, F8 | **Chặn cứng toàn bộ đường báo có** — không có «ting ting», không gạch bill, không onboarding TK | Sandbox mock connector (`/connectors/ob-*`) dùng trên UAT trước khi ký; **không có degrade thật cho PROD** — đây là rủi ro «Cao» số 1 (PRD §11) |
| D3 | Specs + sandbox eKYC E1 | T7/2026 · BRH | US-02, US-05, US-07 · F1/S1 · AC-1.2, AC-1.4, AC-9.3 | Không tự động hóa xác minh danh tính; onboarding nghẽn | **Duyệt tay ảnh CIN** tại BRH-03 + hàng đợi (`pending_review`); mock contract-first; tự động hóa sau |
| D4 | Chốt mẫu standee + quy trình in theo đợt | Trước T9/2026 · BRH·VDS | US-08, US-28 · S8 · gate «≥90% standee đã dán» | Merchant không có QR tại quầy → mất kênh nhận tiền chính | App tự **in QR giấy A5** dùng tạm (S8); standee bù theo đợt sau |
| D5 | Phê phí pilot = 0 + chốt ngưỡng giám sát AML ngày (`AML_DAY_FLAG`) — mọi merchant eKYC đầy đủ, không đặt hạn mức nhận theo bậc | Trước 31/7/2026 · BRH | US-07, US-33 · S2 (giám sát hậu kiểm) · AC-8.1 | Chưa chốt ngưỡng → giám sát AML hậu kiểm thiếu mốc mặc định | MMS **hậu kiểm** `limit.breached` khi tổng nhận ngày chạm `AML_DAY_FLAG` (hậu kiểm, không chặn ghi Có) |
| D6 | Brandname SMS Peye-Haiti + bộ template đăng ký trước | T8/2026 · Natcom | US-01, US-11, US-19, US-24, US-26, US-39 · N1 | SMS bị chặn/không đúng brandname → mất OTP, mất báo có offline | `N1-400-TPL` alert; **OTP thoại** theo runbook Natcom; báo có chỉ push (AC-2.2 FAIL) |
| D7 | Hotline 8686 + đội field đào tạo theo chợ | T9/2026 · Natcom | US-06, US-39 · F1, F9 · AC-1.5, AC-10.1 | Không khóa khẩn được khi mất máy; phủ 601 merchant chậm | Khóa khẩn vẫn gọi được `E.1.8` từ máy bất kỳ (OTP về SIM); đăng ký tự phục vụ (chậm hơn) |
| D8 | Danh bạ trực ban 3 bên + số leo thang | Trước go-live · 3 bên | US-37 · F8 · AC-9.3 | Sự cố trôi, không leo thang 5–30–60 phút | Alertmanager gửi kênh nội bộ VDS; DLQ bank không có người xử → tồn lệch |
| D9 | **wallet2 (bên trả) quét & trả QR chuẩn QG trên môi trường thật** | Trước go-live · Natcom | US-12 · VI-00→04 · F2 · **AC-2.5** | **Không ai trả được tiền** → toàn bộ footprint vô nghĩa | Không có degrade — điều kiện Go/No-Go bắt buộc; lộ trình C21 (wallet2 → MonCash T12 → bank 2027) |
| D10 | Đặc tả + lịch báo cáo EOD từ Switch (E3) | T8/2026 · BRH/ACI | US-36 · F8/S6 · AC-9.1, AC-9.2 | Không đối soát được; không phát hiện `missing_in_mms` | **SFTP dự phòng**; đối soát dời phiên; dựa M3 (lịch sử TK) làm nguồn đối chiếu tạm |
| **D11** | **Chốt danh sách chợ & phân bổ 601 merchant** (PRD C23) | T8/2026 · BRH·Natcom | US-01, US-06, US-29 · bảng `market` (seed `0002_seed_market.sql`) · KPI theo chợ BRH-08 | Không seed được danh mục chợ → NB-2B («v3.6») không có ô «chọn chợ»; đội field không có chỉ tiêu phân bổ; KPI theo chợ không cắt được | Seed **9 chợ / 3 TP** theo đề xuất kỹ thuật (Port-au-Prince·Pétion-Ville, Les Cayes, Cap-Haïtien); sửa danh mục qua API tham số E.13.x (vận hành Natcom, 4 mắt) khi BRH chốt — **không đổi schema** |

---

## §8. Điểm hở (gap register)

Phát hiện khi lập ma trận: **6 điểm hở + 6 mâu thuẫn số liệu**. Bản v1.1 này **đã VÁ**: G2/G3 (bổ sung 2 AC — AC-5.4, AC-10.1 — vào PRD §7) · G6 (sửa preamble API_Spec F.2) · X1–X6 (chốt số liệu ở cả 5 tài liệu). **Còn lại 2 điểm hở — cả hai đều CÓ CHỦ Ý, chấp nhận được**, không có điểm hở nghiêm trọng (mọi US đều có AC + API + bảng; mọi bảng đều có người ghi).

| # | Loại | Nội dung | Ảnh hưởng | Xử lý |
|---|---|---|---|---|
| **G4** | Màn thiếu US | **NB-10** (báo cáo bán hàng, `E.8.1`), **NB-03** (trang chủ), **BRH-01** — PRD §7 ghi rõ «đặc tả trực tiếp bằng wireframe + UX-1..7, không lập US riêng» | Có chủ ý, không phải lỗi — nhưng **`E.8.1 GET /reports/sales` là endpoint không map US nào** | **CHẤP NHẬN**; tester dùng wireframe + AC-3.1 (một nguồn số liệu) làm tiêu chí cho NB-10 |
| **G5** | Endpoint không map US | `E.12.9 GET /admin/cases/{id}` · `E.15.2 GET /admin/merchants/{id}/activity` · `E.13.9 adjustments approve/reject` · `E.10.4/E.10.5 GET/PATCH /me` — bổ khuyết portal v1.1, không gắn US nào trong PRD §7 | Dev có endpoint nhưng PRD không có yêu cầu tương ứng → rủi ro cắt scope nhầm | **CHẤP NHẬN**: ghi nhận là **enabler** của US-32 (E.12.9, E.13.9) và US-28 (E.15.2); không cần thêm US |

**Điểm hở ĐÃ VÁ (nhật ký v1.1):**

| # | Điểm hở | Cách vá | Vết |
|---|---|---|---|
| **G2** | US-24 (biên lai SMS qua `E.5.5`) không có AC | Thêm **AC-5.4** (SMS ≤30 giây · `SMS_RATE_LIMIT` 5/giờ/merchant · không gửi trùng cùng `credit_event`) | PRD §7/EP-5 · §1 (US-24) · §5 |
| **G3** | US-38 (quên PIN qua `E.1.7`) không có AC — bề mặt tấn công | Thêm **AC-10.1** (OTP về SIM đăng ký; reset xong thu hồi mọi phiên cũ) | Đã vá |
| **G6** | API_Spec F.2 preamble xếp NB-01/NB-03 là «màn tĩnh không gọi API», lệch với PRD §7 | Sửa preamble F.2: **NB-01 = màn ĐĂNG KÝ** (gọi `E.1.1`); **NB-03 = trang chủ động** (gọi `E.5.1` + `E.8.1`). Thêm hàng NB-03 vào bảng F.2.1; §2.1 ma trận này đồng bộ | API_Spec §F.2/F.2.1 · §2.1 |

**Bảng không ai ghi:** không có. 28/28 bảng đều có ít nhất 1 endpoint hoặc job ghi (xem §3; `payment`: ghi `E.16.1/2` + `B.4`, đọc `E.16.3/4`). `market` chỉ ghi bằng migration seed, danh mục agent hiện trường nằm trong `param` (không có endpoint CRUD riêng trong API_Spec) — **có chủ ý** với pilot, nhưng dev cần công cụ nội bộ để seed danh mục chợ + danh sách NAT-xxx trước go-live (**D11**).

**Nhật ký chốt số liệu X1–X6 — ĐÃ ĐỒNG BỘ trên cả 5 tài liệu** (điều kiện in bản ký):

| # | Hạng mục | Giá trị CHỐT (kiểm đếm thực tế) | Đã sửa tại |
|---|---|---|---|
| **X1** | User story · acceptance criteria | **42 US** (US-01…US-46; +US-46 «v3.5») · **46 AC** (AC-1.1…AC-11.6 +AC-1.8) = 6+8+5+4+1+5+3+3+3+2+6 | PRD §7 intro · ma trận này (header, §1, §5) |
| **X2** | Số màn wireframe | **42 màn** = NB 17 + BRH 10 + AQ 4 + VI 5 + NM 5 + **CH 1 (CH-00 chọn vai «v3.6» — đã có wireframe)** (BRH-09 bỏ 04/08) | PRD header + §4.1 · SSD header · TSD header · ma trận này §2 |
| **X3** | Quy mô tích hợp | **14 mục · 12 giao diện ngoài + 2 nội bộ** (I2/I5). Ngoài = M1, M1a, M1b, M3, M4, **M-PAY, M-PAY-hook «Peye-Haiti 15/08»**, E1, E2, E3, E3-reg, N1. **M2 không tính** (ngữ cảnh đường tiền, không phải API tích hợp) | PRD §8 (tiêu đề + ghi chú kiểm đếm) · SSD §7 (tiêu đề + ghi chú) · ma trận này §4 |
| **X4** | Quy mô API | Nhóm E: **89 mục đánh số**. Tổng **B 5 · C 9 · D 5 · E 89 · P 1 = 109 mục / 110 HTTP endpoint** «v3.5» | TSD §2c · API_Spec §F.2 · ma trận này (header) |
| **X5** | Ngưỡng AML chống chia nhỏ | AC-8.2 viết **theo tham số**: ≥5 GD trong dải **80–100% `AML_TX_FLAG`** / 24h (`AML_SMURF={count≥5, band 0.80–1.00}`) — **bỏ hard-code khoảng tiền tuyệt đối**; test sinh số liệu từ param | PRD AC-8.2 · ma trận này §5 (hàng AC-8.2) · TSD §13.3 (không đổi) |
| **X6** | Danh mục chợ pilot | Chưa được BRH chốt → nâng thành **điểm quyết C23** + **phụ thuộc D11** (hạn T8/2026). Đề xuất kỹ thuật giữ nguyên: **9 chợ / 3 TP** (seed `0002_seed_market.sql`) | PRD §16 (C23) · PRD §10 (D11) · ma trận này §7 (D11) |

**Dấu vết USSD / tài khoản ảo / M2·M6·M6b·N2:** đã rà toàn bộ 5 tài liệu — **chỉ tồn tại dưới dạng câu loại trừ tường minh** (API_Spec header «KHÔNG có VA/M2/M6/M6b/USSD/N2»; TSD §2 «Mã M2, M6, M6b, N2 để trống — không sử dụng»; TSD §5 comment «BỎ cột hash PIN kênh USSD»; DataDict §1.4/§5.3 «không tồn tại bảng tài khoản ảo»). **Không có đặc tả sống nào** cho USSD/USS-01, tài khoản ảo, M6/M6b/N2 — NGOẠI LỆ duy nhất («16/08»): B.5 /qr-inquiry có giá trị enum kênh `"app"|"ussd"` cho GĐ2 (chỉ là kênh TRA CỨU của app định chế, KHÔNG có luồng USSD nào của Peye-Haiti trong pilot). Sạch.

---

## §9. Chỉ mục nhanh — hỏi gì, tra ở đâu

| Câu hỏi | Tài liệu · Mục |
|---|---|
| «Trường X kiểu gì, NULL được không, ràng buộc gì?» | **DataDict** §2 (28 bảng, từng trường) · §3 (enum tập trung) · §4 (FK) |
| «Endpoint này trả mã lỗi nào?» | **API_Spec** §F.1 (41 mã đóng: 11 PIN + 14 OB + 16 BIZ) · bảng «Lỗi riêng» dưới từng endpoint |
| «Request/response endpoint này có trường gì?» | **API_Spec** mục E (BFF app/portal) · B (đối tác gọi vào) · C (Open Banking) · D (E1/E2/E3/N1) |
| «Màn này gọi API nào?» | **API_Spec** §F.2 (ma trận endpoint × màn) · ma trận này **§2** |
| «Bảng này ai được ghi?» | **SSD** §4 (4 dịch vụ + ownership) · **DataDict** §2 (28 bảng · 5 schema) · ma trận này **§3** |
| «Luồng nghiệp vụ đầu-cuối chạy thế nào?» | **PRD** §6 (F1–F9) · **SSD** §5 (S1–S9, chi tiết kỹ thuật) |
| «Component bên trong 1 dịch vụ?» | **SSD** §4.1 (C4-L3 — 7 sơ đồ: BFF + 4 dịch vụ theo module) |
| «Thuật toán gạch bill?» | **TSD** §6 (state machine + pseudo-code + invariant «1 credit ↔ ≤1 đích») |
| «Giá trị mặc định của tham số / đổi ở đâu?» | **TSD** §13.3 (25 param — +MCC_DEFAULT · PAY_CONFIRM_SLA · PAY_TIMEOUT · PAY_CREATE_TTL · OPERATOR_DIRECTORY) → sửa qua `E.13.2`–`E.13.4` bởi vận hành Natcom (4 mắt — không còn màn portal) |
| «Contract M4 (webhook báo có)?» | **TSD** §3 · **API_Spec** §B.1 (đầy đủ từng trường + hành vi retry của bank) |
| «Xác thực đối tác & chống replay?» | **API_Spec** §A.1b (thẻ tự ký kèm hash body, ≤5′, không kid/jti) + §F.3 (thẻ response tài chính) + §F.5 (ví dụ bản tin) |
| «Yêu cầu RNI/KYC/nhật ký quốc gia của BRH ảnh hưởng gì?» | Văn bản BRH 12/08: `BRH/BRH_RNI_QuyetToan_BaoMat_Dich_VI.md` · quyết định áp dụng: `BRH/PeyeHaiti_CR_BRH_LuuTru_NhatKy.md` (CR-1…12) · bản đồ khai báo A–G: **DataDict** §6 · KYC=KYC2: **PRD** §4 / **SSD** §8 |
| «Payload QR gồm tag nào?» | **TSD** §13.4 (HTQR 1.0 dự thảo v0.9.1 — CR-3) · test vectors §12.1 |
| «Đồng bộ offline & xung đột?» | **TSD** §7 (ma trận transition bill) · **API_Spec** §E.9.1 |
| «Tiêu chí nghiệm thu US này?» | **PRD** §7 (AC-x.y) · ma trận này **§5** (kèm loại test + cách đo) |
| «Sizing hạ tầng UAT/PROD?» | **TSD** §9 — 5.000 merchant (PROD 24 VM · UAT 8 VM · sao lưu thay DR) |
| «Điểm nào BRH còn phải quyết?» | **PRD** §16 (C1–C23 kèm đề xuất chốt theo tham chiếu VN) |
| «Cái gì chặn go-live?» | **PRD** §10 (D1–D11) · §13 (gate) · ma trận này **§7** |
| «Ngưỡng cảnh báo vận hành?» | **TSD** §10 (bảng metric + hành động) · PRD C12 |
| «RBAC ai làm được gì?» | **TSD** §8 (5 vai trò) · `/docs/rbac.csv` · cột «Quyền» từng endpoint mục E |

---

*Ma trận này là ARTIFACT DẪN XUẤT — mọi ô đều trích từ 5 tài liệu nguồn, không bổ sung yêu cầu mới. Khi 5 tài liệu nguồn thay đổi, cập nhật ma trận trong cùng lần review. **Mâu thuẫn X1–X6 và điểm hở G1/G2/G3/G6 đã được xử lý ở bản v1.1** (xem §8) — 5 tài liệu đã đồng bộ số liệu, đủ điều kiện in bản ký nghiệm thu; còn G4/G5 là hai điểm hở CÓ CHỦ Ý, đã chấp nhận.*
