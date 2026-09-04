# Data Dictionary — Giải pháp Merchant Peye-Haiti (từ điển dữ liệu từng trường)

| Trường | Nội dung |
|---|---|
| Mã tài liệu | **Peye-Haiti-DD-001 · v4.4** — 24/08/2026 · **«v3.7» (đồng bộ API Spec v3.7 — chỉ đổi LỜI MÔ TẢ, không đổi cột/giá trị):** `idem_key` ca đang-xử-lý (`response` nullable — trùng key khi NULL → 409 `details.state="processing"`); +mô tả `addenda.payment_ref` (khóa khớp ĐÍCH DANH B.5 — ưu tiên trước bill_id); liên kết NGUỒN TRẢ (funding) thuộc CÁ NHÂN — MỌI vai, kể cả chủ gian hàng (hết gắn riêng «người mua») · **«v3.6» TẠO LÀ ACTIVE:** đổi NGHĨA (không đổi giá trị) enum `merchant.status.pending` + `application.status` (pending_review = cờ HẬU KIỂM, không chặn active; SLA ≤24h thay «duyệt ≤8h»; flags +`e2_deferred`) · **20/08 (v3.5 — hai bậc xác thực):** `payment` +4 cột `sca_*` (18→22 trường; tổng 306→310) · `payment.status` +`sca_required` (110 giá trị) · `failure_reason` +`sca_failed` · §2.23: `PAY_MAX_PILOT`→`PAY_SCA_THRESHOLD` (ngưỡng OTP định chế), `PAY_DAY_MAX` chỉ bậc-PIN · person = mọi VAI (chọn vai CH-00, nút nâng cấp lên người bán) · **19/08 (AuthOB v3.4):** hạn mức pilot `PAY_MAX_PILOT` = 5.000 HTG/GD, PIN-only + trần ngày `PAY_DAY_MAX` (§2.23 **+2 key** — bảng `payment` KHÔNG đổi cột; xác thực = PIN app trước khi gửi, không cột SCA) · **15/08 (Peye-Haiti — app chung, mô hình BiMPay):** **15/08 (Peye-Haiti — app chung, mô hình BiMPay):** đổi tên dự án PINASSI→HaitiPay (file `PeyeHaiti_*.md`; prefix kỹ thuật `PIN-` GIỮ nguyên tránh vỡ code/hợp đồng); thêm module NGƯỜI MUA (nguồn: BRH «Application client» 15/08): +bảng 2.31 `payment` (18 trường — lệnh trả người mua khởi tạo, tiền vẫn ngoài Peye-Haiti), `account_link` mở cho person (+`person_id`, `merchant_id` nullable, scope token +`payment`), `person` +`kyc_level` (KYC1 người mua · KYC2 merchant — đảo một phần quyết định 25/07 «1 bậc»), `merchant` +`public_phone` (trang công khai xác minh) — **28 bảng · 306 trường · 28 enum/109 giá trị · 45 quan hệ (25 vật lý · 17 logic · 3 đa hình)** · **15/08 (CR BRH)**: `merchant` +3 cột (`mcc` CR-1 · `alias` chờ CR-4 · `national_merchant_id` chờ CR-2) · `person` +2 cột (`nif_no` CR-5 · `rni_person_id` chờ CR-6) · `credit_event` +2 cột chờ (`payer_person_id` · `payer_operator` CR-7) · phụ lục §6 «bản đồ khai báo nhật ký quốc gia + 3 KHÔNG» (CR-8) — theo `BRH/PeyeHaiti_CR_BRH_LuuTru_NhatKy.md` (đối chiếu văn bản BRH 12/08) · **04/08**: ghi chú `param` — màn BRH-09 bỏ, quản trị qua E.13.x (vận hành Natcom, 4 mắt) · **02/08 (CANON2)**: bỏ M7/M4b/qr_intent/report_schedule/buyer_profile, gộp device→auth_session, matching 2 mức (bỏ HIST) — **27 bảng nghiệp vụ**; nền 24/07 v3.3: đồng bộ tên ví Natcash→wallet2 (NatTransfer), mã ví dụ NATC→NTRF · **4 dịch vụ · mỗi dịch vụ một schema (5 schema)** · event bus **Apache Kafka**; các mục v1.1 giữ nhãn «bổ sung chuẩn v1.1»; v3.3: bỏ M5 + gộp còn 1 bậc KYC |
| Loại tài liệu | Data Dictionary — mô tả từng bảng/từng trường của CSDL nghiệp vụ MMS Peye-Haiti (PostgreSQL 15) — **5 schema: 4 dịch vụ + `shared`** (TSD §5) |
| Nguồn chuẩn | `PeyeHaiti_TSD.md` **§5 (DDL — nguồn gốc, bám 100%)**, §13.3 (tham số), §4 (schema sự kiện Kafka) · `PeyeHaiti_SSD.md` **v5.1c** §4 (sở hữu dữ liệu — 4 dịch vụ), §6 (ERD) · `PeyeHaiti_PRD.md` (nghiệp vụ) |
| Phạm vi | 28 bảng nghiệp vụ (+ bảng hạ tầng `outbox`, mỗi schema một bảng) phục vụ footprint go-live 01/10/2026 — 601 merchant · 3 thành phố (Pétion-Ville · Les Cayes · Cap-Haïtien) · BRH chủ trì, Natcom đầu mối, VDS xây dựng. Hạ tầng sizing cho **5.000 merchant** (TSD §9) |
| Đối tượng đọc | Dev backend/DBA/QA/đối soát — dùng song song với migration tại `/db/migrations` |

---

## 1. Quy ước chung

### 1.1. Kiểu dữ liệu chuẩn

| Kiểu | Dùng cho | Quy ước |
|---|---|---|
| `UUID` | Khóa chính, khóa ngoại, `client_uuid` | **PK/FK: server sinh UUID v7** (sắp theo thời gian, thân thiện index; default DB `gen_random_uuid()` chỉ là lưới đỡ khi chèn ngoài ứng dụng) · **`client_uuid` & `Idempotency-Key`: client sinh UUID v4** (khớp API_Spec A.5) |
| `TEXT` | Mọi chuỗi | Không dùng `VARCHAR(n)`; ràng buộc giá trị bằng `CHECK` |
| `BIGINT` | Tiền — cột hậu tố `_ct` | **Centime (ct)**: 1 gourde (G) = 100 ct; ví dụ 150.000 ct = 1.500 G; không bao giờ dùng số thập phân cho tiền |
| `NUMERIC` | Điểm số 0..1 (eKYC) · tọa độ `lat`/`lng` `NUMERIC(9,6)` «v1.1» | So sánh với ngưỡng trong bảng `param`; tọa độ theo WGS84 |
| `BOOL` | Cờ | Mặc định tường minh trong DDL |
| `DATE` | `biz_date`, `dob`, `effective_from` | `biz_date` = ngày nghiệp vụ theo **giờ Haiti (America/Port-au-Prince)** |
| `timestamptz` | Mọi mốc thời gian | Lưu **UTC**, trao đổi RFC3339 |
| `JSONB` | Payload mở rộng (`addenda`, `params`, `value`, `payload`) | Không đánh index trừ khi có nhu cầu truy vấn |
| `BYTEA` | Dữ liệu mã hóa (`*_enc`) & hash | Mã hóa **envelope Vault** (AES-256-GCM + KEK trong Vault, xoay KEK 12 tháng); hash chain của audit |
| `TEXT[]` | Mảng (`scope`, `channel`) | — |

### 1.2. Quy tắc đặt tên & cột chuẩn

- **snake_case** cho mọi bảng/cột; tên bảng số ít (`merchant`, `bill`); bảng `case` là từ khóa SQL — luôn viết `"case"` khi truy vấn.
- **Khóa chính**: `id UUID` cho mọi bảng, **ngoại lệ**: `param` (PK = `key TEXT`), `idem_key` (PK = `key UUID` — chính là Idempotency-Key), `audit_log` (PK = `seq BIGSERIAL` — bảo toàn thứ tự chuỗi hash).
- **`created_at` / `updated_at` `timestamptz` mặc định mọi bảng** (default `now()`). DDL TSD §5 là bản rút gọn — bảng nào không ghi 2 cột này thì tài liệu bổ sung và đánh dấu **«bổ sung chuẩn»**. Ngoại lệ không bổ sung: `audit_log` (append-only, mốc thời gian là `at`), `idem_key` (bản ghi bất biến, chỉ `created_at`, purge 48h).
- **Soft-delete: KHÔNG dùng** toàn hệ thống — ngoại lệ duy nhất theo DDL: `product.deleted_at`.
- **`client_uuid`**: UUID **v4** do app client sinh (offline-first) — chống trùng khi đồng bộ, luôn `UNIQUE`.
- **`version INT`**: khóa lạc quan (optimistic lock) — **chỉ dùng cho đồng bộ offline** (TSD §7: client gửi `version` đang giữ, server từ chối nếu đã cũ). **KHÔNG dùng cho khớp tiền**: khớp tiền nay là **transaction nội bộ dịch vụ Commerce** (`SELECT … FOR UPDATE`), không còn lệnh nội bộ xuyên dịch vụ.
- **Enum** = `TEXT` + `CHECK` (không dùng kiểu ENUM của Postgres); giá trị chữ thường, riêng `match_result.level` viết HOA. Toàn bộ enum tập trung tại **§3**.
- **🔒 = PII/bí mật**: mã hóa at-rest (AES-256), che khi hiển thị, không ghi log rõ, kiểm soát truy cập theo RBAC; chi tiết §5.
- **Cột «Bắt buộc»**: `Có` = NOT NULL theo DDL hoặc theo nghiệp vụ khi bản ghi hoàn tất luồng; `Có*` = bắt buộc về nghiệp vụ nhưng điền ở bước sau của luồng (chú thích ngay dưới bảng); `Không` = cho phép NULL.

### 1.3. Mã định danh nghiệp vụ

| Mã | Định dạng · Ví dụ | Ghi chú |
|---|---|---|
| Mã merchant | `PIN-M-000241` | `merchant.code`, in trên standee |
| RefID | `PIN-2026-000123` | Do **Switch BRH (ACI)** sinh; `credit_event.ref_id`; **NULL với giao dịch on-us** (nội bộ bank, không qua Switch) |
| Mã bill | `B-<ddMM>-<seq>` · `B-1007-17` | Client sinh, `seq` reset theo ngày; `UNIQUE(merchant_id, biz_date, code)` |
| Mã nhân viên hiện trường (`agent_code`) | `NAT-xxx` · `NAT-014` | Nhân viên field Natcom, danh mục trong `param` |
| Tiền tệ | `HTG` (ISO 4217, mã số **332**) | QR tag 53 = `332`; bút toán 100% gourde |

### 1.4. Nguyên tắc kiến trúc phản chiếu vào dữ liệu

- **Mỗi dịch vụ đúng một schema** (TSD §5): `merchant_identity` · `commerce` · `backoffice` · `notification` + `shared` (hạ tầng tầng API — `idem_key`). Mỗi dịch vụ một DB role, chỉ được `GRANT` trên schema của mình; **không dịch vụ nào đọc/ghi thẳng bảng của schema dịch vụ khác**. Ranh giới miền nghiệp vụ giữ ở tầng module trong code.
- **FK vật lý chỉ trong CÙNG schema.** Tham chiếu XUYÊN schema là **tham chiếu LOGIC** (cột UUID, KHÔNG có `REFERENCES`) — dữ liệu lấy qua REST nội bộ hoặc sự kiện Kafka. §4 đánh dấu rõ từng quan hệ là FK vật lý hay ref logic.
- **Bảng `outbox` (mỗi schema một bảng)**: ghi trong CÙNG transaction nghiệp vụ, tiến trình relay publish sang **Kafka** sau commit (mẫu transactional outbox — TSD §4/§5) → chi tiết §2.32.
- **Khớp tiền là transaction nội bộ Commerce**: ghi `match_result` (kiêm luôn dữ liệu biên lai) + đổi `bill.status` → `paid` / ghi `ledger_entry(repay,auto)` + set cờ `credit_event.late_auto` khi khớp-muộn xảy ra trong **một transaction ACID** cùng database (khóa hàng `SELECT … FOR UPDATE`). Invariant «1 credit_event ↔ ≤1 đích» do `UNIQUE(match_result.credit_event_id)` bảo đảm — **không còn lệnh nội bộ xuyên dịch vụ, không saga, không khóa lạc quan xuyên dịch vụ**.
- **QR/standee in SỐ TÀI KHOẢN THẬT đã liên kết** (mô hình VietQR): đích tiền luôn là TK thật tại bank/ví nhận qua `account_link` — **không tồn tại bảng tài khoản ảo** trong schema.
- MMS **ngoài đường tiền**: `credit_event` là bản ghi thông tin báo Có (nguồn «ting ting»), không phải bút toán tiền.
- Đổi TK nhận: 2 dòng `account_link` song song cùng bank (TK mới `active` + TK cũ `grace` 30 ngày) — ràng buộc `UNIQUE(merchant_id, bank_code, ext_link_id)` cho phép điều này.
- Retention tóm tắt: `audit_log` 10 năm · ảnh eKYC 5 năm sau đóng gian (MinIO, DB chỉ giữ key) · `credit_event`/`match_result` 5 năm · `notification` 12 tháng · `idem_key` 48h — chi tiết §5.

---

## 2. Từ điển bảng (28 bảng nghiệp vụ + `outbox`)

Sở hữu dữ liệu theo **SSD §4 (4 dịch vụ)** và **TSD §5 (5 schema)** — dịch vụ sở hữu là **nơi duy nhất ghi** bảng của schema mình; dịch vụ khác đọc qua REST nội bộ (`/internal/*`) hoặc sự kiện **Kafka**, không truy cập chéo schema:

| # | Dịch vụ | Schema PostgreSQL | Bảng sở hữu |
|---|---|---|---|
| 1 | **Merchant & Identity** | `merchant_identity` | `merchant` · `standee` · `application`² · `person` · `ekyc_result` · `auth_session` · `account_link` · `token` |
| 2 | **Commerce** | `commerce` | `credit_event` (module Ingest) · `match_result` (kiêm biên lai) · `product` · `bill` · `bill_item` · `debtor` · `ledger_entry` |
| 3 | **Back-office** | `backoffice` | `case` (kèm chứng cứ JSONB) · `adjustment` · `aml_alert` · `recon_run` · `discrepancy` · `param` · `market` · `app_user` · `audit_log` · `report` |
| 4 | **Notification** | `notification` | `notification` |
| — | *(hạ tầng tầng API — không thuộc dịch vụ nào)* | `shared` | `idem_key` |
| — | *(hạ tầng — mỗi schema một bảng)* | mọi schema | `outbox` (§2.32) |

² Bảng «bổ sung chuẩn v1.1» (review vòng 1): `application` (Merchant & Identity — hồ sơ onboarding).

> **Hệ quả của việc gom về 4 dịch vụ (SSD §4 · A10)**: `match_result` (kiêm biên lai) ↔ `bill` ↔ `ledger_entry` nay **cùng schema `commerce`, cùng một database**, trong cùng schema `commerce` với `credit_event` → khớp tiền → đánh dấu đơn «đã thu» / gạch nợ → sinh biên lai là **MỘT transaction ACID nội bộ**, **không còn lệnh ghi xuyên dịch vụ và không còn khóa lạc quan xuyên dịch vụ** (§1.4). Tương tự, bút toán điều chỉnh sinh từ khiếu nại và từ đối soát nay dùng chung một bảng `adjustment` trong schema `backoffice`.

### 2.1. `merchant` — dịch vụ **Merchant & Identity** · schema `merchant_identity` *(module Gian hàng)*

Hồ sơ gian hàng tiểu thương — thực thể trung tâm của vòng đời onboarding → hoạt động → đóng (F1, BRH-03/04).

| Trường | Kiểu | Bắt buộc | Mô tả | Ràng buộc / Ví dụ |
|---|---|---|---|---|
| `id` | UUID | Có | Khóa chính | PK |
| `code` | TEXT | Có | Mã merchant nghiệp vụ, in trên standee, tra cứu portal | `UNIQUE` · vd `PIN-M-000241` |
| `shop_name` | TEXT | Có | Tên gian hàng hiển thị (QR tag 59, danh bạ người mua) | vd `MARIE DELVA` |
| `mcc` | CHAR(4) | Có | Mã ngành hàng ISO 18245 — vào QR tag 52 (HTQRPAY) & hồ sơ merchant BRH (§3.2 bắt buộc); tiểu thương KHÔNG tự chọn — default `MCC_DEFAULT`, suy từ `business_type` (E.2.2 «v3.6» — business_type KHÔNG lưu cột riêng, chỉ dùng ánh xạ → mcc), BRH sửa được khi hậu kiểm (BRH-03 «v3.6») «CR-1 15/08» | default `5411` (param §13.3 TSD) |
| `alias` | TEXT | Không | Tên ngắn merchant (BRH §3.2) — **CỘT CHỜ, CHƯA DÙNG**: không hiển thị, không vào QR (alias thuộc HTQR v1.1, sống ở RNI) «CR-4 15/08» | NULL toàn pilot |
| `public_phone` | TEXT | Không | SĐT hiện trên TRANG CÔNG KHAI xác minh merchant (P.1 — yêu cầu C-CLIENTS của BRH); merchant tự khai & đồng ý công khai, KHÔNG mặc định lấy `person.msisdn` «Peye-Haiti 15/08» | NULL = không hiện SĐT |
| `national_merchant_id` | TEXT | Không | **MerchantID QUỐC GIA** do BRH/RNI cấp — CỘT CHỜ: NULL ở pilot, cơ chế điền chốt khi module RNI có hợp đồng API (nhập tay qua portal cũng được); mapping ngôn ngữ BRH: `code` = OperatorMerchantID · `shop_name` = MerchantName · `market.city` = City «CR-2 15/08» | `UNIQUE` khi không NULL |
| `market_id` | UUID | Có | Chợ nơi đặt gian hàng | FK → `market.id` (REFERENCES trong DDL) |
| `status` | TEXT | Có | Trạng thái vòng đời hồ sơ/gian hàng | CHECK: `draft` · `pending` · `need_more` · `rejected` · `active` · `suspended` · `closed` (nghĩa tại §3) |
| `person_id` | UUID | Có | Chủ gian hàng (quan hệ 1–1 theo ERD) | FK → `person.id` |
| `agent_code` | TEXT | Không | Mã nhân viên hiện trường Natcom đăng ký hộ (US-06) — «v3.6»: nhận ở E.1.1, GHI khi nộp E.2.2 (app truyền lại); danh mục agent quản trong `param` (không còn bảng riêng) | vd `NAT-014` · NULL nếu tự đăng ký |
| `activated_at` | timestamptz | Không | Thời điểm kích hoạt (auto C10 hoặc BRH duyệt tay) | NULL khi chưa kích hoạt |
| `lat` | NUMERIC(9,6) | Không | Vĩ độ vị trí gian hàng — hiển thị bản đồ portal (danh bạ người mua hoãn — S5) «bổ sung chuẩn v1.1» | NULL khi chưa định vị |
| `lng` | NUMERIC(9,6) | Không | Kinh độ vị trí gian hàng «bổ sung chuẩn v1.1» | NULL khi chưa định vị |
| `created_at` | timestamptz | Có | Thời điểm tạo bản ghi «bổ sung chuẩn» | default `now()` |
| `updated_at` | timestamptz | Có | Lần cập nhật cuối «bổ sung chuẩn» | default `now()` |

- Chuyển trạng thái phát sự kiện `merchant.activated / merchant.suspended / merchant.closed`; `suspended` → rớt nhãn «Đã xác thực» trên danh bạ ≤5 phút (cache TTL).
- Kích hoạt (C10 «v3.6» — TẠO LÀ ACTIVE): `ekyc.matched (PASS) + đủ hồ sơ gian hàng + TK nhận` → `active` NGAY; `score < AUTO_ACTIVATE_SCORE(0.85)` HOẶC `e2.hit` HOẶC E2 5xx (`e2_deferred`) → VẪN active + cờ `post_review` (hậu kiểm ≤24h); hồ sơ sạch → mẫu 10%.

### 2.2. `person` — dịch vụ **Merchant & Identity** · schema `merchant_identity` *(module Định danh)*

Danh tính cá nhân của chủ gian hàng **và người dùng cá nhân (profile Client — kyc_level 1)** — «v3.7»: liên kết NGUỒN TRẢ (funding) luôn thuộc CÁ NHÂN, mọi vai — tách khỏi `merchant` để dùng lại eKYC giữa các lần nộp hồ sơ. Mã đục gửi định chế khi liên kết nguồn trả («v3.4»): `person_ref = "prn_" + HMAC-SHA256(person.id, khóa nội bộ)[:22]` — phát sinh deterministic, KHÔNG cột mới (API Spec C.1).

| Trường | Kiểu | Bắt buộc | Mô tả | Ràng buộc / Ví dụ |
|---|---|---|---|---|
| `id` | UUID | Có | Khóa chính | PK |
| `full_name` 🔒 | TEXT | Có* | Họ tên theo thẻ CIN | vd `Marie Delva` |
| `dob` 🔒 | DATE | Có* | Ngày sinh (KYC C1) | — |
| `cin_no` 🔒 | TEXT | Có* | Số căn cước CIN (ONI) — chống trùng hồ sơ | `UNIQUE` |
| `nif_no` 🔒 | TEXT | Không | Số định danh thuế NIF — BRH III.1.A chấp nhận CIN **hoặc** NIF; nghiệp vụ CIN-first (E1 đối chiếu ONI theo CIN), NIF là bổ sung khi có «CR-5 15/08» | `UNIQUE` khi không NULL |
| `rni_person_id` | TEXT | Không | **PersonID quốc gia** (RNI, III.1.F) — CỘT CHỜ, chưa dùng; MMS KHÔNG gửi CIN/NIF sang RNI, chỉ nhận mã đục về «CR-6 15/08» | `UNIQUE` khi không NULL |
| `msisdn` 🔒 | TEXT | Có | SĐT chính chủ — đăng nhập, OTP, khóa khẩn | `UNIQUE` · E.164, vd `+50937xxxxxx` |
| `kyc_level` | SMALLINT | Có | Bậc KYC theo khung hài hòa BRH III.1.E — `1` người mua (OTP, giao dịch nhỏ) · `2` merchant (eKYC E1 đầy đủ); đảo một phần quyết định 25/07 «1 bậc» vì mô hình BiMPay thêm profile người mua «Peye-Haiti 15/08» | default `1`; lên `2` khi eKYC pass |
| `pin_hash` 🔒 | TEXT | Có | Băm PIN 6 số — Argon2id (m=64MB, t=3, p=1); khóa 60′ sau 5 lần sai (C2) | Không bao giờ lưu PIN rõ |
| `lang` | TEXT | Có | Ngôn ngữ app | default `'ht'` (Kreyòl) · `'fr'` (Pháp) |
| `created_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |
| `updated_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |

\* `full_name`, `dob`, `cin_no` điền ở bước eKYC (NB-2A); NULL khi hồ sơ mới tạo bằng SĐT.

### 2.4. `auth_session` — dịch vụ **Merchant & Identity** · schema `merchant_identity` *(module Định danh)*

Phiên đăng nhập (refresh token) của app người bán/người mua và portal; khóa khẩn = revoke mọi phiên theo `person`.

| Trường | Kiểu | Bắt buộc | Mô tả | Ràng buộc / Ví dụ |
|---|---|---|---|---|
| `id` | UUID | Có | Khóa chính | PK |
| `person_id` | UUID | Không | Chủ phiên app (người bán/mua) — đúng 1 trong 2 với `user_id` | FK → `person.id` |
| `user_id` | UUID | Không | Chủ phiên portal BRH/vận hành | FK → `app_user.id` |
| `device_id` | UUID | Không | Định danh thiết bị của phiên (client sinh) | — (opaque, không FK) |
| `fingerprint` 🔒 | TEXT | Không | Định danh thiết bị/trình duyệt PWA (gắn vào JWT) — gộp từ bảng thiết bị cũ (S7) | — |
| `is_agent_session` | BOOL | Có | Phiên hỗ trợ trên máy nhân viên hiện trường — đánh dấu riêng để truy vết (AC-1.5), gộp từ bảng thiết bị cũ (S7) | default `false` |
| `refresh_hash` 🔒 | TEXT | Có | Băm refresh token (JWT refresh 30 ngày app; access 15′) | Không lưu token rõ |
| `expires_at` | timestamptz | Có | Hết hạn phiên | — |
| `revoked` | BOOL | Có | Đã thu hồi — khóa khẩn hotline 8686 thu hồi mọi phiên ≤60s (AC-10.1) | default `false` |
| `created_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |
| `updated_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |

### 2.5. `ekyc_result` — dịch vụ **Merchant & Identity** · schema `merchant_identity` *(module Định danh)*

Kết quả từng lần đối chiếu danh tính E1 (ảnh CIN 2 mặt + selfie ↔ dữ liệu ONI); tham chiếu `ref` dùng cho liên kết M1.

| Trường | Kiểu | Bắt buộc | Mô tả | Ràng buộc / Ví dụ |
|---|---|---|---|---|
| `id` | UUID | Có | Khóa chính | PK |
| `person_id` | UUID | Có | Người được đối chiếu | FK → `person.id` |
| `provider` | TEXT | Có | Nhà cung cấp eKYC | default `'BRH-E1'` |
| `ref` | TEXT | Có | Mã tham chiếu phiên E1 — truyền vào M1 (`kyc_evidence_ref`) khi liên kết TK | — |
| `matched` | BOOL | Có | Kết quả khớp/không khớp | E1 chỉ trả khớp + điểm (C3), không trả ảnh gốc |
| `score` | NUMERIC | Có | Điểm tin cậy 0..1 — «v3.6»: dưới `AUTO_ACTIVATE_SCORE (0.85)` = gắn cờ `post_review` hậu kiểm (VẪN active) | vd `0.91` |
| `created_at` | timestamptz | Có | Thời điểm có kết quả (có sẵn trong DDL) | — |
| `front_key` 🔒 | TEXT | Có* | Khóa MinIO ảnh CIN mặt trước (cột thêm bằng ALTER trong DDL) | Ảnh nén ≤200KB; retention 5 năm sau đóng gian |
| `back_key` 🔒 | TEXT | Có* | Khóa MinIO ảnh CIN mặt sau | như trên |
| `selfie_key` 🔒 | TEXT | Có* | Khóa MinIO ảnh selfie (chống giả mạo) | như trên |
| `updated_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |

\* 3 khóa ảnh bắt buộc trong luồng E1 chuẩn (upload trước khi gọi verify); DDL khai báo qua ALTER không kèm NOT NULL.

### 2.6. `account_link` — dịch vụ **Merchant & Identity** · schema `merchant_identity` *(module Tài khoản & Token)*

Liên kết tài khoản tại bank/ví (M1 liên kết TK có sẵn) — hai vai theo chủ sở hữu «Peye-Haiti 15/08»: (a) **TK NHẬN của merchant** — nguồn số TK thật cho QR/standee, nguồn đăng ký danh mục TK với Switch (E3-reg); (b) **TK NGUỒN TRẢ của CÁ NHÂN** (funding — MỌI vai, kể cả chủ gian hàng «v3.7») — consent scope `payment` để khởi tạo M-PAY.

| Trường | Kiểu | Bắt buộc | Mô tả | Ràng buộc / Ví dụ |
|---|---|---|---|---|
| `id` | UUID | Có | Khóa chính | PK |
| `merchant_id` | UUID | Không* | Merchant sở hữu liên kết (1..2 bank theo ERD) — TK NHẬN của người bán | FK → `merchant.id` |
| `person_id` | UUID | Không* | Cá nhân sở hữu liên kết — TK NGUỒN TRẢ (funding — mọi vai «v3.7», mô hình BiMPay). \* CHECK: đúng MỘT trong hai (`merchant_id`, `person_id`) khác NULL | FK → `person.id` |
| `bank_code` | TEXT | Có | Mã bank/ví nhận | vd `NTRF` (wallet2) |
| `ext_link_id` | TEXT | Có | `link_id` do bank cấp qua M1 — khóa map `M4.link_id` → merchant | `UNIQUE` toàn cục · vd `lnk_01H...` |
| `account_no_masked` 🔒 | TEXT | Có | Số TK che, hiển thị trên app/biên lai | vd `…7709` |
| `account_no_enc` 🔒 | BYTEA | Có | **Số TK đầy đủ MÃ HÓA** (envelope Vault) — nguồn cho E3-reg & so khớp `account_no` trong bảng kê E3 | Chỉ giải mã trong luồng nghiệp vụ |
| `account_no_hmac` 🔒 | BYTEA | Không | HMAC-SHA256 số TK (khóa riêng trong Vault ≠ khóa envelope) — cột TRA CỨU cho resolve E.16.1 (không đảo ngược được, thỏa «3 KHÔNG»); ghi khi liên kết (C.2/E.3.3) «Peye-Haiti 15/08 vòng 2» | index partial (bank_code, hmac) WHERE active·grace |
| `holder_name` 🔒 | TEXT | Có | Tên chủ TK do bank trả về khi liên kết (M1) — hiển thị xác nhận | — |
| `status` | TEXT | Có | Trạng thái liên kết | CHECK: `active` · `grace` · `revoked` (nghĩa tại §3) |
| `created_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |
| `updated_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |

- Ràng buộc: `UNIQUE(ext_link_id)` (bank cấp, toàn cục) **và** `UNIQUE(merchant_id, bank_code, ext_link_id)` — cho phép 2 liên kết song song cùng bank trong giai đoạn grace (TK mới `active` + TK cũ `grace` 30 ngày `OLD_LINK_GRACE`, S4).
- Đổi TK/đóng gian → cập nhật E3-reg với Switch; thu hồi bằng M1b → `revoked`.
- Không có khái niệm tài khoản ảo: mọi dòng trỏ tới TK thật tại bank/ví — của merchant (TK nhận) hoặc của cá nhân — mọi vai (TK nguồn trả «v3.7») (Q4).

### 2.7. `token` — dịch vụ **Merchant & Identity** · schema `merchant_identity` *(module Tài khoản & Token)*

Token consent OAuth2 theo từng liên kết (1–1 với `account_link`) — dùng gọi M3 lịch sử, nhận M4.

| Trường | Kiểu | Bắt buộc | Mô tả | Ràng buộc / Ví dụ |
|---|---|---|---|---|
| `id` | UUID | Có | Khóa chính | PK |
| `link_id` | UUID | Có | Liên kết sở hữu token | `UNIQUE` (1–1) · FK → `account_link.id` |
| `access_enc` 🔒 | BYTEA | Có | Access token mã hóa envelope — hiệu lực 90 ngày (C4) | Vault AES-256-GCM |
| `refresh_enc` 🔒 | BYTEA | Có | Refresh token mã hóa — hiệu lực 12 tháng (C4) | như trên |
| `scope` | TEXT[] | Có | Phạm vi consent — liên kết người mua thêm `payment` (khởi tạo trả M-PAY) «Peye-Haiti 15/08» | `{balance, history, credit-notify}` · người mua: `{payment, history}` |
| `expires_at` | timestamptz | Có | Hết hạn access token — job `token-renewal` gia hạn trước D-7 (`TOKEN_RENEW_BEFORE`) | — |
| `status` | TEXT | Có | Trạng thái token | CHECK: `active` · `expiring` · `revoked` (nghĩa tại §3) |
| `created_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |
| `updated_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |

- Chuyển trạng thái phát sự kiện `token.expiring` / `token.revoked` (nhắc D-7, cảnh báo AQ-00).

### 2.8. `standee` — dịch vụ **Merchant & Identity** · schema `merchant_identity` *(module Gian hàng)*

Bảng QR mica tại quầy — in **số TK thật đã liên kết** + tên gian hàng + mã merchant (mẫu chuẩn BRH, D4); payload QR theo **HTQR 1.0** (TSD §13.4 — có tag 52 MCC, CR-3); tracking vòng đời in → giao → dán (BRH-04, S8).

| Trường | Kiểu | Bắt buộc | Mô tả | Ràng buộc / Ví dụ |
|---|---|---|---|---|
| `id` | UUID | Có | Khóa chính | PK |
| `merchant_id` | UUID | Có | Gian hàng gắn standee | FK → `merchant.id` |
| `account_link_id` | UUID | Có | TK liên kết là nguồn payload QR in trên standee | FK → `account_link.id` (REFERENCES trong DDL) |
| `qr_ver` | INT | Có | Phiên bản QR — **tăng khi đổi TK nhận** (in lại standee) | default `1` |
| `market_id` | UUID | Có | Chợ giao/lắp standee | FK → `market.id` |
| `status` | TEXT | Có | Trạng thái vòng đời standee | CHECK: `ordered` · `printed` · `delivered` · `mounted` · `replacing` · `recalled` (nghĩa tại §3) |
| `mounted_at` | timestamptz | Không | Thời điểm merchant xác nhận «đã dán» — điều kiện bước ⑤ thu hồi token cũ (M1b) trong cutover S4 | NULL khi chưa dán |
| `created_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |
| `updated_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |

- In theo đợt kích hoạt; trong lúc chờ, app tự in QR giấy A5 (không tracking trong bảng này).

### 2.9. `credit_event` — dịch vụ **Commerce** · schema `commerce` *(module Ingest)*

Sự kiện **báo Có** tiền vào TK liên kết — nguồn của «ting ting»; hợp nhất 2 nguồn (webhook M4, quét M3-poll) sau dedup 2 tầng. MMS ngoài đường tiền: đây là bản ghi thông tin, không phải bút toán.

| Trường | Kiểu | Bắt buộc | Mô tả | Ràng buộc / Ví dụ |
|---|---|---|---|---|
| `id` | UUID | Có | Khóa chính nội bộ | PK |
| `event_id` | TEXT | Có | Định danh sự kiện **do bank sinh** — dedup tầng 1; bản ghi từ quét M3-poll sinh `poll:`+ref_id/txn_id | `NOT NULL` · **`UNIQUE` toàn cục** |
| `ref_id` | TEXT | Không | RefID do Switch sinh — dedup tầng 2 xuyên nguồn; bắt buộc với GD qua Switch, **NULL với GD on-us** (nội bộ bank; E3 bỏ qua on-us) | Partial `UNIQUE` (`ce_refid_uq WHERE ref_id IS NOT NULL`) · vd `PIN-2026-000123` |
| `merchant_id` | UUID | Có | Merchant nhận tiền — xác định từ `link_id` (mức ①); **partition key** của topic Kafka `credit.received` | ref logic → `merchant_identity.merchant.id` (xuyên schema — không FK vật lý) |
| `account_no_masked` 🔒 | TEXT | Không | Số TK nhận che — chỉ để hiển thị | vd `…7709` |
| `amount_ct` | BIGINT | Có | Số tiền ghi Có (centime) | vd `150000` = 1.500 G |
| `currency` | TEXT | Có | Tiền tệ | default `'HTG'` (ISO 332) |
| `payer_msisdn` 🔒 | TEXT | Không | SĐT người trả (M4 `payer`) — nuôi biên lai (gửi SMS) & gạch bill | vd `+50937xxxxxx` |
| `payer_name` 🔒 | TEXT | Không | Tên người trả | vd `J. PIERRE` |
| `payer_person_id` | TEXT | Không | PersonID quốc gia (mã đục RNI) của người trả — CỘT CHỜ: chỉ có khi định chế bên trả gửi kèm trong M4 (trường optional hợp đồng D2); về lâu dài thay vai PII của `payer_msisdn` «CR-7 15/08» | NULL toàn pilot |
| `payer_operator` | TEXT | Không | Mã định chế bên trả dải 9332xx (chuẩn HTQR) — CỘT CHỜ như trên; phục vụ khai báo nhật ký quốc gia nhóm A «CR-7 15/08» | vd `933201` |
| `narrative` 🔒 | TEXT | Không | Nội dung chuyển khoản — **không tin cậy để khớp** (A5), chỉ tham khảo/hiển thị | — |
| `addenda` | JSONB | Không | Dữ liệu kèm theo chuẩn QR; `addenda.payment_ref` («16/08» — mã tra cứu B.5, TTL 15′) → khớp ĐÍCH DANH ưu tiên số 1; `addenda.bill_id` (nếu D1/D2 bảo toàn) → khớp `LINK` trực tiếp | vd `{"bill_id":"B-1007-17"}` |
| `link_id` | UUID | Không\*\* | Liên kết TK nhận — map về merchant (mức ①) | ref logic → `merchant_identity.account_link.id` (xuyên schema) |
| `late_auto` | BOOL | Có | Cờ khớp-muộn: báo có tự động về **sau** khi merchant đã xác nhận tay → giữ kết quả tay, chỉ bật cờ | default `false` |
| `is_revenue` | BOOL | Có | Cờ doanh thu — `false` = «không phải doanh thu» (US-40, E.5.6): loại khỏi doanh số & KPI matching, VẪN tính giám sát AML «bổ sung chuẩn v1.1» | default `true` |
| `non_revenue_reason` | TEXT | Không | Lý do «không phải doanh thu» (quy ước E.5.6: `personal` · `family` · `other`); NULL khi `is_revenue=true` «bổ sung chuẩn v1.1» | — |
| `source` | TEXT | Có | Nguồn bản ghi | CHECK: `m4` · `m3poll` (nghĩa tại §3) |
| `booked_at` | timestamptz | Có | **T0** — thời điểm bank ghi Có (mốc đo SLA báo có ≤5s P95) | RFC3339 UTC |
| `received_at` | timestamptz | Có | Thời điểm MMS nhận/chuẩn hóa sự kiện | — |
| `created_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |
| `updated_at` | timestamptz | Có | «bổ sung chuẩn» (cập nhật khi set `late_auto`) | default `now()` |

\*\* Hợp đồng M4 (D2) quy định `link_id` **BẮT BUỘC** trong mọi webhook (mọi TK nhận đều qua liên kết M1); cột cho phép NULL cho bản ghi nguồn `m3poll`/webhook thiếu chi tiết — khi đó chờ xác nhận tay.

- Chỉ mục: `UNIQUE(event_id)` · partial unique `ce_refid_uq(ref_id) WHERE ref_id IS NOT NULL` · `INDEX(merchant_id, booked_at DESC)`.
- **Partition**: pilot chưa bật; DDL thiết kế sẵn **RANGE theo tháng** cho `credit_event` khi >5.000 merchant (TSD §5).
- Retention 5 năm. Quan hệ 1–1 với `match_result` (bản ghi khớp kiêm biên lai).

### 2.11. `match_result` — dịch vụ **Commerce** · schema `commerce` *(module Khớp tiền)*

Kết quả gạch (khớp) của từng `credit_event` — 1–1. `UNIQUE(credit_event_id)` **chính là** invariant «1 credit_event ↔ ≤1 đích». Bảng này **kiêm luôn dữ liệu biên lai** (1–1 với `credit_event` nên không cần bảng riêng). Việc ghi bản ghi này + đổi `bill.status` → `paid` (hoặc ghi `ledger_entry` gạch nợ) + điền thông tin biên lai + set cờ `credit_event.late_auto` khi khớp-muộn nằm trong **CÙNG MỘT transaction** (khóa hàng `SELECT … FOR UPDATE`, tất cả cùng schema `commerce`) — **không còn lệnh ghi nội bộ xuyên dịch vụ, không saga**. Sự kiện `match.completed` chỉ phát ra Kafka SAU COMMIT (qua `outbox`) cho Notification + Back-office (KPI) tiêu thụ.

| Trường | Kiểu | Bắt buộc | Mô tả | Ràng buộc / Ví dụ |
|---|---|---|---|---|
| `id` | UUID | Có | Khóa chính | PK |
| `credit_event_id` | UUID | Có | Sự kiện tiền về được khớp | **`UNIQUE` (1–1) = invariant** · FK vật lý → `commerce.credit_event.id` (cùng schema) |
| `level` | TEXT | Có | Mức khớp — tạo `PENDING` **ngay khi nhận** (mẫu số KPI tính từ đây) | CHECK: `PENDING` · `LINK` · `MANUAL` · `STRAY` (nghĩa tại §3) |
| `target_type` | TEXT | Không | Loại đích khớp | CHECK: `bill` · `ledger` · `stray` · NULL khi `PENDING` |
| `target_id` | UUID | Không | Id đích (đa hình theo `target_type`): `commerce.bill.id` hoặc `commerce.ledger_entry.id` — **cùng schema**; NULL với `stray` | Đa hình — không FK vật lý |
| `matched_by` | UUID | Không | Chủ thể xác nhận tay mức ② (`person` của merchant hoặc `app_user` portal); NULL khi khớp tự động | — |
| `matched_at` | timestamptz | Không | Thời điểm chốt khớp | — |
| `sent_msisdn` 🔒 | TEXT | Không | *(biên lai)* SĐT merchant chủ động gửi biên lai qua SMS (khách không có app — US-24) | — |
| `receipt_channel` | TEXT[] | Có | *(biên lai)* Các kênh đã phát biên lai | default `{}` · vd `{app}`, `{app,sms}` |
| `created_at` | timestamptz | Có | «bổ sung chuẩn» — mốc vào trạng thái `PENDING` | default `now()` |
| `updated_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |

- KPI gạch tự động = `count(level = LINK) / count(level NOT IN (STRAY, PENDING))`; khoản gắn cờ «không phải doanh thu» (US-40) loại khỏi cả tử số lẫn mẫu số — job `kpi-matching` ghi vào `report`.
- `PENDING` quá `STRAY_AFTER` (72h) không ai xử lý → `STRAY` (đóng, vẫn tính doanh thu vãng lai).
- Retention 5 năm (cùng `credit_event`).

### 2.12. `product` — dịch vụ **Commerce** · schema `commerce` *(module Đơn hàng)*

Danh mục món + giá của merchant — hậu kiểm C9: hiển thị ngay khi tạo, nhãn «chờ kiểm duyệt» chỉ nội bộ, gỡ khi vi phạm/báo cáo.

| Trường | Kiểu | Bắt buộc | Mô tả | Ràng buộc / Ví dụ |
|---|---|---|---|---|
| `id` | UUID | Có | Khóa chính | PK |
| `merchant_id` | UUID | Có | Gian hàng sở hữu món | FK → `merchant.id` |
| `name` | TEXT | Có | Tên món | vd `Diri (gạo) 1kg` |
| `price_ct` | BIGINT | Có | Đơn giá (centime) | vd `25000` = 250 G |
| `photo_key` | TEXT | Không | Khóa MinIO ảnh món (nén ≤200KB, upload qua `POST /media`) | NULL nếu không ảnh |
| `moderation` | TEXT | Có | Trạng thái hậu kiểm | default `'pending'` · CHECK: `pending` · `ok` · `removed` (nghĩa tại §3) |
| `removed_reason` | TEXT | Không | Lý do gỡ món khi `moderation='removed'` — hiển thị cho merchant (E.7.1) «bổ sung chuẩn v1.1» | NULL khi chưa gỡ |
| `deleted_at` | timestamptz | Không | **Soft-delete — ngoại lệ duy nhất toàn hệ thống** (TSD §5) | NULL = còn hiệu lực |
| `version` | INT | Có | Khóa lạc quan cho PATCH danh mục (E.7.3, sync E.9.1) «bổ sung chuẩn v1.1» | default `1` |
| `created_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |
| `updated_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |

### 2.13. `bill` — dịch vụ **Commerce** · schema `commerce` *(module Đơn hàng)*

Đơn tính tiền (F3) — 6 trạng thái; `paid` **chỉ do server đặt** qua matching (client không bao giờ set); đồng bộ offline theo ma trận transition (TSD §7).

| Trường | Kiểu | Bắt buộc | Mô tả | Ràng buộc / Ví dụ |
|---|---|---|---|---|
| `id` | UUID | Có | Khóa chính | PK |
| `code` | TEXT | Có | Mã bill hiển thị `B-<ddMM>-<seq>` — `seq` do client sinh, reset theo ngày | `UNIQUE(merchant_id, biz_date, code)` · vd `B-1007-17` |
| `merchant_id` | UUID | Có | Gian hàng tạo bill | FK → `merchant.id` |
| `total_ct` | BIGINT | Có | Tổng tiền bill — matching so khớp **tuyệt đối** (`AMOUNT_TOLERANCE = 0 ct`) | vd `214000` = 2.140 G |
| `note` | TEXT | Không | Ghi chú bill (≤140 — E.4.3) «bổ sung chuẩn v1.1» | — |
| `status` | TEXT | Có | Trạng thái bill | CHECK: `open` · `paid` · `cash` · `cancelled` · `expired` · `credit` (nghĩa tại §3) |
| `qr_expires_at` | timestamptz | Không | Hết hạn QR động với **người quét** (`QR_DYNAMIC_TTL` 15′, app tự xoay mã); tiền đã chuyển trong hạn vẫn về sau được | — |
| `expires_at` | timestamptz | Có | Hết đời bill = 24h (`BILL_TTL`) — cửa sổ khớp mở **toàn đời bill**, không giới hạn 15′ | — |
| `biz_date` | DATE | Có | Ngày nghiệp vụ = `created_at_client` quy về múi giờ Haiti (America/Port-au-Prince) — chốt v1.1, khớp API E.4.3 | thành phần khóa `UNIQUE` |
| `client_uuid` | UUID | Có | UUID app sinh (offline-first, idempotent sync) | `UNIQUE` |
| `version` | INT | Có | Khóa lạc quan — **chỉ dùng cho đồng bộ offline** (TSD §7); khớp tiền không dùng `version` (đã là transaction nội bộ Commerce, khóa hàng `SELECT … FOR UPDATE`) | default `0` |
| `paid_by_credit_event_id` | UUID | Không | Khoản tiền về đã thanh toán bill này — ghi trong CÙNG transaction khớp (bước 6b) | FK → `credit_event.id` · NULL khi chưa thu |
| `created_at` | timestamptz | Có | «bổ sung chuẩn» — **dùng cho tie-break**: bill duy nhất tạo trong ±`MATCH_LOOKBACK` (15′) quanh `booked_at` | default `now()` |
| `updated_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |

- Chỉ mục: `UNIQUE(merchant_id, biz_date, code)` · `UNIQUE(client_uuid)` · `INDEX(merchant_id, status, total_ct)` — phục vụ tìm ứng viên matching.
- Client chỉ được chuyển `open → cash/cancelled/credit`; mọi vi phạm trả `conflict{server_state}`; `paid`/`expired` chỉ đọc.

### 2.14. `bill_item` — dịch vụ **Commerce** · schema `commerce` *(module Đơn hàng)*

Dòng món trong đơn tính tiền — snapshot tên/giá tại thời điểm bán (không đổi khi sửa `product` sau này).

| Trường | Kiểu | Bắt buộc | Mô tả | Ràng buộc / Ví dụ |
|---|---|---|---|---|
| `id` | UUID | Có | Khóa chính | PK |
| `bill_id` | UUID | Có | Bill chứa dòng | FK → `bill.id` |
| `product_id` | UUID | Không | Món trong danh mục; NULL = món nhập tự do | FK → `product.id` |
| `name` | TEXT | Có | Tên món (snapshot) | — |
| `qty` | INT | Có | Số lượng (chỉnh −/+ trên NB-07) | ≥1 |
| `price_ct` | BIGINT | Có | Đơn giá snapshot (centime) | — |
| `created_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |
| `updated_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |

### 2.15. `debtor` — dịch vụ **Commerce** · schema `commerce` *(module Sổ nợ)*

Khách nợ trong sổ nợ của merchant — chạy offline 100% (F5); dữ liệu thuộc merchant, chỉ dùng chấm điểm khi có consent (C7).

| Trường | Kiểu | Bắt buộc | Mô tả | Ràng buộc / Ví dụ |
|---|---|---|---|---|
| `id` | UUID | Có | Khóa chính | PK |
| `merchant_id` | UUID | Có | Chủ sổ nợ | FK → `merchant.id` |
| `name` 🔒 | TEXT | Có | Tên khách nợ (merchant tự đặt) | vd `Jean` |
| `msisdn` 🔒 | TEXT | Không | SĐT khách — để nhắc nợ SMS (tối đa 1 tin/khách/ngày, AC-4.4) | NULL nếu không có |
| `client_uuid` | UUID | Có | UUID app sinh (offline-first) | `UNIQUE` |
| `created_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |
| `updated_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |

### 2.16. `ledger_entry` — dịch vụ **Commerce** · schema `commerce` *(module Sổ nợ)*

Bút ghi sổ nợ (ghi nợ/ghi trả) — **không sửa entry đã có**, chỉ thêm bút ghi đảo; chống trừ nợ 2 lần bằng `client_uuid` + tham chiếu `credit_event_id`.

| Trường | Kiểu | Bắt buộc | Mô tả | Ràng buộc / Ví dụ |
|---|---|---|---|---|
| `id` | UUID | Có | Khóa chính | PK |
| `debtor_id` | UUID | Có | Khách nợ | FK → `debtor.id` |
| `type` | TEXT | Có | Loại bút ghi | CHECK: `debt` · `repay` (nghĩa tại §3) |
| `amount_ct` | BIGINT | Có | Số tiền (centime) | vd `90000` = 900 G |
| `origin` | TEXT | Có | Nguồn bút ghi: client tạo `debt/repay(manual)`; server tạo `repay(auto)` khi gạch nợ | CHECK: `manual` · `auto` (nghĩa tại §3) |
| `credit_event_id` | UUID | Không | Khoản tiền về đã gạch vào nợ này (S7) — khớp-tay-trước thì credit tham chiếu vào entry, không trừ 2 lần (AC-4.3) | ref logic → `commerce.credit_event.id` (xuyên schema) |
| `bill_id` | UUID | Không | Bill nguồn khi «Bán chịu» (bill → `credit`, E.6.3) «bổ sung chuẩn v1.1» | FK → `bill.id` |
| `due_at` | timestamptz | Không | Hẹn trả (nếu có) | — |
| `note` | TEXT | Không | Ghi chú bút ghi (≤140 — E.6.3) «bổ sung chuẩn v1.1» | — |
| `reversed_by_entry_id` | UUID | Không | Bút ghi đảo tham chiếu ngược — entry không sửa, chỉ thêm bút ghi đảo (E.6.4) «bổ sung chuẩn v1.1» | FK → `ledger_entry.id` (self) |
| `client_uuid` | UUID | Có | UUID sinh phía tạo (app/server) — trùng `client_uuid` = idempotent | `UNIQUE` |
| `version` | INT | Có | Khóa lạc quan — **chỉ dùng cho đồng bộ offline** (TSD §7); gạch nợ tự động chạy trong transaction nội bộ Commerce | default `0` |
| `created_at` | timestamptz | Có | «bổ sung chuẩn» — thời điểm ghi nợ/trả (thao tác ≤10 giây, AC-4.1) | default `now()` |
| `updated_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |

### 2.18. `case` — dịch vụ **Back-office** · schema `backoffice` *(module Khiếu nại)*

Hồ sơ tra soát/khiếu nại bám RefID (F7) — hoàn tiền = merchant chuyển trả + **xác minh bút toán** (M3/chứng từ) + case chốt; tên bảng là từ khóa SQL, luôn truy vấn `"case"`.

| Trường | Kiểu | Bắt buộc | Mô tả | Ràng buộc / Ví dụ |
|---|---|---|---|---|
| `id` | UUID | Có | Khóa chính | PK |
| `code` | TEXT | Có | Mã case nghiệp vụ (tra cứu/hiển thị hàng đợi BRH-06) | `UNIQUE` |
| `ref_id` | TEXT | Không | RefID giao dịch gốc mà case bám theo — **NULL với GD on-us, khi đó bắt buộc `credit_event_id`** (khớp API E.12.3) | vd `PIN-2026-000123` (tham chiếu logic, không FK) |
| `credit_event_id` | UUID | Không* | Khoản báo Có của case — bắt buộc khi `ref_id` NULL (GD on-us) «bổ sung chuẩn v1.1» | FK → `credit_event.id` |
| `payment_id` | UUID | Không* | Lệnh trả của case NGƯỜI MUA (source=`buyer_app`) — khi đó `merchant_id` được NULL nếu payment chưa resolve «Peye-Haiti 15/08 vòng 2» | ref logic → `commerce.payment.id` |
| `merchant_id` | UUID | Có | Merchant liên quan | FK → `merchant.id` |
| `type` | TEXT | Có | Loại khiếu nại | CHECK: `wrong_amount` · `not_received` · `duplicate` · `fraud_suspect` · `other` (nghĩa tại §3) |
| `description` | TEXT | Có | Lời khai/mô tả khiếu nại (≤1000 — E.12.3; ≤500 từ app E.5.4) «bổ sung chuẩn v1.1» | — |
| `source` | TEXT | Có | Kênh mở case «bổ sung chuẩn v1.1» | CHECK: `merchant_app` · `portal` · `hotline` · `recon` · `buyer_app` «Peye-Haiti 15/08» (nghĩa tại §3) |
| `assigned_to` | UUID | Không | Cán bộ nhận ca xử lý (E.12.4) «bổ sung chuẩn v1.1» | FK → `app_user.id` · NULL khi chưa phân |
| `status` | TEXT | Có | Trạng thái xử lý | CHECK: `open` · `awaiting_merchant` · `investigating` · `concluded_refund` · `concluded_reject` · `closed` (nghĩa tại §3) |
| `sla_due_at` | timestamptz | Có | Hạn SLA đếm ngược — phản hồi đầu 24h (`CASE_SLA_FIRST`), đóng 5 ngày làm việc (`CASE_SLA_CLOSE`); quá hạn nổi đỏ BRH-02 (AC-7.2) | — |
| `refund_verified` | BOOL | Có | Đã xác minh bút toán chuyển trả — **chặn chốt «Đã hoàn» khi false** (AC-7.1) | default `false` |
| `evidence` | JSONB | Có | Chứng cứ 2 phía (không còn bảng riêng): mảng phần tử `{kind, side, object_key, uploaded_by, note, at}` — file lưu MinIO, DB chỉ giữ khóa; `side` ∈ `merchant` · `buyer` · `brh`; `uploaded_by` = `person` hoặc `app_user` | default `[]` |
| `created_at` | timestamptz | Có | «bổ sung chuẩn» — mốc mở case | default `now()` |
| `updated_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |

\* Một trong BA `ref_id` / `credit_event_id` / `payment_id` bắt buộc: GD qua Switch → `ref_id`; GD on-us → `credit_event_id`; khiếu nại người mua (E.16.5) → `payment_id` «Peye-Haiti 15/08 vòng 2».

- Sự kiện `case.opened` / `case.concluded` phát lên **Kafka** (Notification + Merchant & Identity khóa/mở gian hàng). Cờ refund dùng **nội bộ Back-office** — module Đối soát cùng dịch vụ đọc thẳng, để E3 không đếm khoản chuyển trả thành GD bán mới.

### 2.19. `adjustment` — dịch vụ **Back-office** · schema `backoffice` *(bút toán điều chỉnh — dùng chung 2 module)*

Bút toán điều chỉnh doanh số — **một luồng phê duyệt duy nhất** `draft → approved (4 mắt) → posted`, nay **nằm gọn trong module Compliance của Back-office**: cả module Khiếu nại lẫn module Đối soát đều tạo nháp trên cùng bảng này (mẫu C19: bút toán đảo có tham chiếu gốc, khóa sổ ngày).

| Trường | Kiểu | Bắt buộc | Mô tả | Ràng buộc / Ví dụ |
|---|---|---|---|---|
| `id` | UUID | Có | Khóa chính | PK |
| `source` | TEXT | Có | Nguồn phát sinh | CHECK: `case` · `recon` (nghĩa tại §3) |
| `case_id` | UUID | Không | Case gốc — bắt buộc khi `source='case'` | FK → `case.id` |
| `recon_run_id` | UUID | Không | Phiên đối soát gốc — bắt buộc khi `source='recon'` | FK → `recon_run.id` |
| `merchant_id` | UUID | Có | Merchant bị điều chỉnh doanh số | FK → `merchant.id` |
| `amount_ct` | BIGINT | Có | Số tiền điều chỉnh (centime) | — |
| `direction` | TEXT | Có | Chiều điều chỉnh | CHECK: `debit` · `credit` (nghĩa tại §3) |
| `status` | TEXT | Có | Trạng thái luồng phê duyệt | CHECK: `draft` · `approved` · `posted` (nghĩa tại §3) |
| `maker` | UUID | Có | Người lập (đề xuất) | FK → `app_user.id` |
| `checker` | UUID | Không | Người phê duyệt 4 mắt — **phải khác maker**; NULL khi còn `draft` | FK → `app_user.id` |
| `created_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |
| `updated_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |

- Quy tắc nghiệp vụ: điền đúng một trong `case_id`/`recon_run_id` khớp với `source`.

### 2.20. `aml_alert` — dịch vụ **Back-office** · schema `backoffice` *(module Rửa tiền)*

Cảnh báo phòng chống rửa tiền — từ sàng lọc E2, luật ngưỡng/hành vi C14, hoặc hậu kiểm hạn mức (sự kiện Kafka `limit.breached` do Commerce phát); **module Compliance (Back-office) là nơi duy nhất ra quyết định về rửa tiền**, mọi quyết định bắt buộc lý do.

| Trường | Kiểu | Bắt buộc | Mô tả | Ràng buộc / Ví dụ |
|---|---|---|---|---|
| `id` | UUID | Có | Khóa chính | PK |
| `merchant_id` | UUID | Có | Merchant bị cảnh báo | FK → `merchant.id` |
| `source` | TEXT | Có | Nguồn cảnh báo | CHECK: `e2` · `rule` · `limit` (nghĩa tại §3) |
| `rule_code` | TEXT | Có | Mã luật kích hoạt | vd `AML_TX_FLAG` (≥10.000.000 ct/GD) · `AML_DAY_FLAG` (≥50.000.000 ct/ngày) · `AML_SMURF` (≥5 GD 80–100% ngưỡng/24h) · mã danh sách E2 |
| `status` | TEXT | Có | Trạng thái xử lý | CHECK: `open` · `awaiting_reply` · `investigating` · `dismissed` · `escalated` (nghĩa tại §3) |
| `reason` | TEXT | Không | Lý do quyết định — **bắt buộc nhập khi ra quyết định** (AC-8.3), NULL khi chưa quyết | — |
| `created_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |
| `updated_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |

- Cảnh báo vượt hạn mức (`limit.breached`) → gắn cờ hạn chế gian hàng + mở case AML tới khi xử lý (AC-8.1).

### 2.21. `recon_run` — dịch vụ **Back-office** · schema `backoffice` *(module Đối soát)*

Một phiên đối soát với bảng kê EOD của Switch (E3) — khởi điểm 3 phiên/ngày (C18), quyết toán T+1; file JSONL ký số, đã lọc theo danh mục TK nhận đăng ký (E3-reg).

| Trường | Kiểu | Bắt buộc | Mô tả | Ràng buộc / Ví dụ |
|---|---|---|---|---|
| `id` | UUID | Có | Khóa chính | PK |
| `session_no` | INT | Có | Số phiên trong ngày | 1..3 |
| `biz_date` | DATE | Có | Ngày đối soát (giờ Haiti) | — |
| `e3_file_key` | TEXT | Có | Khóa MinIO file bảng kê E3 (JSONL + chữ ký số) | vd key của `/eod/20261001_S1.jsonl.sig` |
| `status` | TEXT | Có | Trạng thái phiên | CHECK: `ingesting` · `matched` · `discrepancy` · `closed` (nghĩa tại §3) |
| `total_e3` | INT | Không | Tổng bản ghi E3 sau lọc registry — điền khi nạp xong | — |
| `total_matched` | INT | Không | Số bản ghi khớp với `credit_event` | — |
| `created_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |
| `updated_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |

- So khớp theo RefID / số TK / số tiền; **E3 không chứa giao dịch on-us** (`ref_id` NULL được loại khỏi đối soát E3).

### 2.22. `discrepancy` — dịch vụ **Back-office** · schema `backoffice` *(module Đối soát)*

Khoản chênh lệch phát hiện trong một phiên đối soát — xử lý bằng quét M3-poll lấp khoảng / bút toán điều chỉnh 4 mắt / chuyển case; SLA đóng ≤2 ngày làm việc.

| Trường | Kiểu | Bắt buộc | Mô tả | Ràng buộc / Ví dụ |
|---|---|---|---|---|
| `id` | UUID | Có | Khóa chính | PK |
| `run_id` | UUID | Có | Phiên đối soát phát hiện | FK → `recon_run.id` |
| `ref_id` | TEXT | Không | RefID khoản lệch (nếu xác định được) | vd `PIN-2026-000123` |
| `account_no` 🔒 | TEXT | Không | Số TK nhận trong bảng kê E3 (so với `account_no_enc` giải mã) | — |
| `dtype` | TEXT | Có | Loại lệch | CHECK: `missing_in_mms` · `missing_in_e3` · `amount_diff` (nghĩa tại §3) |
| `status` | TEXT | Có | Trạng thái xử lý | CHECK: `open` · `replaying` · `adjusting` · `case` · `closed` (nghĩa tại §3) |
| `sla_due_at` | timestamptz | Có | Hạn xử lý = `DISCREPANCY_SLA` (2 ngày làm việc); backlog >50 → cảnh báo AQ-04 | — |
| `created_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |
| `updated_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |

- Phát sự kiện `recon.discrepancy` vào hàng đợi AQ-04; vết xử lý đầy đủ nguyên nhân → hành động (AC-9.2).

### 2.23. `param` — dịch vụ **Back-office** · schema `backoffice`

Tham số cấu hình hệ thống (quản trị qua E.13.x bởi vận hành Natcom — màn BRH-09 đã bỏ 04/08) — cơ chế 4 mắt maker/checker, hiệu lực theo ngày; thay đổi phát `param.changed` lên **Kafka** (mỗi dịch vụ một consumer group) để mọi dịch vụ cache-bust.

| Trường | Kiểu | Bắt buộc | Mô tả | Ràng buộc / Ví dụ |
|---|---|---|---|---|
| `key` | TEXT | Có | Tên tham số — **PK** (ngoại lệ: không dùng `id` UUID) | vd `QR_DYNAMIC_TTL` |
| `value` | JSONB | Có | Giá trị tham số ĐANG hiệu lực | vd `{"minutes": 15}` |
| `value_pending` | TEXT | Không | Giá trị đề xuất đang CHỜ DUYỆT (chuỗi JSON — E.13.2/E.13.3); NULL khi không có đề xuất «bổ sung chuẩn v1.1» | — |
| `effective_from` | DATE | Có | Ngày hiệu lực | — |
| `status` | TEXT | Có | Trạng thái luồng 4 mắt «bổ sung chuẩn v1.1» | CHECK: `active` · `pending_approval` (nghĩa tại §3) |
| `maker` | UUID | Có | Người đề xuất | FK → `app_user.id` |
| `checker` | UUID | Không | Người phê duyệt (≠ maker — chặn tự duyệt, AC-6.2); NULL khi chờ duyệt | FK → `app_user.id` |
| `proposed_by` | UUID | Không | Người đề xuất `value_pending` của lần đề xuất ĐANG chờ (E.13.3) «bổ sung chuẩn v1.1» | FK → `app_user.id` |
| `approved_by` | UUID | Không | Người phê duyệt lần thay đổi gần nhất (≠ `proposed_by` — 4 mắt, E.13.4) «bổ sung chuẩn v1.1» | FK → `app_user.id` |
| `created_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |
| `updated_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |

Danh mục key chuẩn (TSD §13.3 — giá trị mặc định):

| Key | Mặc định | Key | Mặc định |
|---|---|---|---|
| `QR_DYNAMIC_TTL` | 15 phút | `CASE_SLA_FIRST` / `CASE_SLA_CLOSE` | 24h / 5 ngày làm việc |
| `BILL_TTL` | 24 giờ | `DISCREPANCY_SLA` | 2 ngày làm việc |
| `MATCH_LOOKBACK` | 15 phút | `OLD_LINK_GRACE` | 30 ngày |
| `AMOUNT_TOLERANCE` | 0 ct | `FEE_PILOT` | 0 (đến 31/12/2026) |
| `AML_DAY_FLAG` | 50.000.000 ct/ngày (= 500.000 G) | `STRAY_AFTER` | 72 giờ |
| `TOKEN_RENEW_BEFORE` | 7 ngày | `AML_TX_FLAG` | 10.000.000 ct/GD (= 100.000 G) |
| `OTP_TTL` / `OTP_MAX_PER_DAY` | 120s / 5 | `AML_SMURF` | ≥5 GD ∈ [80–100%] ngưỡng/24h |
| `SMS_RATE_LIMIT` | 5/giờ/merchant | `AUTO_ACTIVATE_SCORE` | 0.85 · hậu kiểm mẫu 10% |
| `MCC_DEFAULT` «CR-1» | `5411` | `PAY_CONFIRM_SLA` «Peye-Haiti 15/08» | 3 giây (P95) |
| `PAY_TIMEOUT` «Peye-Haiti 15/08» | 60 giây | `PAY_CREATE_TTL` «vòng 2» | 15 phút |
| `PAY_SCA_THRESHOLD` «v3.5» (thay PAY_MAX_PILOT) | 500.000 ct = 5.000 HTG — ngưỡng hai bậc: ≤ chỉ PIN · > thêm SMS OTP định chế | `PAY_DAY_MAX` «v3.5» | 2.500.000 ct & ≤20 lệnh/ngày — CHỈ đếm lệnh bậc-PIN |
| `OPERATOR_DIRECTORY` «vòng 2» | JSONB 9332xx↔bank_code (seed cùng D1) | — | — |

### 2.24. `market` — dịch vụ **Back-office** · schema `backoffice`

Danh mục chợ — seed 3 thành phố · 9 chợ (`/db/migrations/0002_seed_market.sql`, danh sách chốt với BRH trước T8/2026).

| Trường | Kiểu | Bắt buộc | Mô tả | Ràng buộc / Ví dụ |
|---|---|---|---|---|
| `id` | UUID | Có | Khóa chính | PK |
| `city` | TEXT | Có | Thành phố | `Pétion-Ville` · `Les Cayes` · `Cap-Haïtien` |
| `name` | TEXT | Có | Tên chợ | — |
| `active` | BOOL | Có | Còn hoạt động (hiện trong dropdown chọn chợ NB-2B «v3.6») | — |
| `created_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |
| `updated_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |

### 2.25. `app_user` — dịch vụ **Back-office** · schema `backoffice`

Người dùng portal BRH & console vận hành — 2FA TOTP bắt buộc (BRH-01), RBAC 5 vai trò (C11), nguyên tắc không vai trò nào vừa tạo vừa duyệt (`/docs/rbac.csv`).

| Trường | Kiểu | Bắt buộc | Mô tả | Ràng buộc / Ví dụ |
|---|---|---|---|---|
| `id` | UUID | Có | Khóa chính | PK |
| `email` 🔒 | TEXT | Có | Email đăng nhập portal | `UNIQUE` |
| `role` | TEXT | Có | Vai trò RBAC | CHECK: `admin` · `approver` · `supervisor_aml` · `ops_read` · `inspector_read` (nghĩa tại §3) |
| `org` | TEXT | Có | Tổ chức | `BRH` · `VDS` · `Natcom` |
| `status` | TEXT | Có | Trạng thái tài khoản — vòng đời mời → hoạt động → khóa (E.13.6–E.13.8); CHECK bổ sung v1.1 | CHECK: `invited` · `active` · `disabled` (nghĩa tại §3) |
| `totp_secret_enc` 🔒 | BYTEA | Có* | Bí mật TOTP mã hóa envelope (2FA) | \* thiết lập ở lần đăng nhập đầu |
| `created_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |
| `updated_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |

### 2.26. `audit_log` — dịch vụ **Back-office** · schema `backoffice`

Nhật ký bất biến append-only với **hash chain** — chỉ ghi sự kiện CÓ actor (thao tác người dùng/quyết định); sự kiện kỹ thuật thuần đi vào observability, không vào audit; job `audit-verify` kiểm chuỗi hằng đêm (AC-6.5); phục vụ thanh tra (US-31).

| Trường | Kiểu | Bắt buộc | Mô tả | Ràng buộc / Ví dụ |
|---|---|---|---|---|
| `seq` | BIGSERIAL | Có | Số thứ tự tăng đơn điệu — **PK** (ngoại lệ: không dùng `id` UUID để bảo toàn thứ tự chuỗi hash) | PK |
| `actor` | UUID | Có | Chủ thể thao tác (`app_user` portal; hoặc `person` với thao tác có tính quyết định từ app) — đa hình, không FK vật lý | — |
| `action` | TEXT | Có | Hành động (duyệt hồ sơ, đổi tham số, khóa merchant, kết luận case…) — chuẩn hóa theo API portal | vd duyệt hồ sơ tại `POST /admin/applications/{id}/approve` |
| `target` | TEXT | Có | Đối tượng tác động | vd `merchant:<uuid>` |
| `payload` | JSONB | Có | Chi tiết thao tác (có thể chứa PII 🔒 — truy cập theo RBAC) | — |
| `at` | timestamptz | Có | Thời điểm thao tác | — |
| `prev_hash` | BYTEA | Không | Hash bản ghi liền trước — NULL ở bản ghi đầu chuỗi | — |
| `hash` | BYTEA | Có | `SHA256(prev_hash ‖ canonical_json)` — đứt gãy = có can thiệp | — |

- **Không bổ sung** `id`/`created_at`/`updated_at` — bảng append-only, mốc thời gian là `at`, cấm UPDATE/DELETE.
- Retention **10 năm** (C17); thiết kế sẵn partition RANGE theo tháng khi >5.000 merchant.

### 2.27. `notification` — dịch vụ **Notification** · schema `notification`

Thông báo đa kênh (I5): ưu tiên push (FCM/WebPush) → chờ ack 60s → SMS N1 brandname «PEYE-HAITI» (đổi từ PINASSI — cần đăng ký lại template với Natcom); template FR/Creole đăng ký trước (D6).

| Trường | Kiểu | Bắt buộc | Mô tả | Ràng buộc / Ví dụ |
|---|---|---|---|---|
| `id` | UUID | Có | Khóa chính | PK |
| `target_kind` | TEXT | Có | Loại đích nhận (DDL không CHECK — quy ước: `merchant` · `buyer` · `user`) | — |
| `target_id` | UUID | Có | Id đích theo `target_kind` — đa hình, không FK vật lý | — |
| `kind` | TEXT | Có | Nhóm nội dung: báo có, nhắc token D-7, case, nhắc nợ, trạng thái hồ sơ… | — |
| `template_id` | TEXT | Có | Mẫu tin FR/Creole (`/i18n/notif/*.po`; template SMS đăng ký trước với Natcom) | — |
| `params` | JSONB | Không | Biến điền vào template | vd `{"amount":"1.500 G"}` |
| `channel` | TEXT | Có | Kênh gửi của bản ghi (DDL không CHECK — quy ước `push` · `sms` · `inapp`; v1.1 thêm `inapp` khớp E.8.2) | — |
| `status` | TEXT | Có | Trạng thái gửi | CHECK: `queued` · `sent` · `acked` · `failed` (nghĩa tại §3) |
| `acked_at` | timestamptz | Không | Thời điểm app ack — không ack trong 60s → fallback SMS (AC-2.2) | — |
| `created_at` | timestamptz | Có | «bổ sung chuẩn» — thời điểm vào hàng đợi | default `now()` |
| `updated_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |

- Rate limit 5 SMS/merchant/giờ (`SMS_RATE_LIMIT`, trừ OTP). Retention **12 tháng**; thiết kế sẵn partition RANGE theo tháng.

### 2.28. `report` — dịch vụ **Back-office** · schema `backoffice`

Báo cáo/KPI tổng hợp chốt theo ngày (BRH-08; chế độ ngày/tuần/tháng — C15) — sinh bởi các job `kpi-*`; số liệu chốt theo ngày đối soát.

| Trường | Kiểu | Bắt buộc | Mô tả | Ràng buộc / Ví dụ |
|---|---|---|---|---|
| `id` | UUID | Có | Khóa chính | PK |
| `kind` | TEXT | Có | Loại báo cáo | vd `kpi-matching` (job §6 TSD), KPI ngày/tuần/tháng |
| `biz_date` | DATE | Có | Ngày số liệu (giờ Haiti) | — |
| `payload` | JSONB | Có | Số liệu tổng hợp (xuất CSV/PDF, email định kỳ từ đây) | — |
| `generated_at` | timestamptz | Có | Thời điểm sinh báo cáo (có sẵn trong DDL) | — |
| `created_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |
| `updated_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |

### 2.29. `idem_key` — hạ tầng tầng API · schema `shared` *(không thuộc dịch vụ nào)*

Kho Idempotency-Key của mọi POST ghi (TSD §1): bản ghi tạo NGAY khi bắt đầu xử lý; trùng key + cùng body đã có response → replay kèm `Idempotency-Replayed: true`; `response` còn NULL (đang xử lý) → `409` `details.state="processing"` + `Retry-After: 1` — client giữ key retry («v3.7»); TTL 48h, cron purge.

| Trường | Kiểu | Bắt buộc | Mô tả | Ràng buộc / Ví dụ |
|---|---|---|---|---|
| `key` | UUID | Có | Giá trị header `Idempotency-Key` (UUIDv4 client sinh) — **PK** (ngoại lệ: không dùng `id`) | PK |
| `endpoint` | TEXT | Có | Endpoint đã gọi (chống dùng lại key cho endpoint khác) | vd `POST /bills` |
| `response` | JSONB | Không («v3.7» — NULL khi đang xử lý) | Response đã trả — phát lại nguyên văn khi trùng key; NULL + trùng key → 409 processing; trùng key khác body → `PIN-409-IDEM` | — |
| `created_at` | timestamptz | Có | Mốc tính TTL 48h (có sẵn trong DDL) | — |

- **Không bổ sung** `updated_at` — bản ghi bất biến, ghi một lần rồi purge.

### 2.30. `application` — dịch vụ **Merchant & Identity** · schema `merchant_identity` *(module Gian hàng)* «bổ sung chuẩn v1.1»

Hồ sơ đăng ký (application) từng lần nộp onboarding — bảng nguồn cho trạng thái NB-1C (`GET /applications/me`, E.2.3) và danh sách HẬU KIỂM BRH-03 (`GET /admin/applications`, E.11.1 «v3.6»); tách khỏi `merchant.status` để giữ vết từng lần nộp + kết luận hậu kiểm (đóng cờ E.11.2 / tạm khóa).

| Trường | Kiểu | Bắt buộc | Mô tả | Ràng buộc / Ví dụ |
|---|---|---|---|---|
| `id` | UUID | Có | Khóa chính — chính là `application_id` trong API | PK |
| `merchant_id` | UUID | Có | Merchant của hồ sơ | FK → `merchant.id` |
| `status` | TEXT | Có | Trạng thái hồ sơ | CHECK: `submitted` · `auto_approved` · `pending_review` · `approved` · `need_more` · `rejected` (nghĩa tại §3) |
| `ekyc_result_id` | UUID | Có* | Kết quả E1 gắn với lần nộp | FK → `ekyc_result.id` |
| `aml_status` | TEXT | Có* | Kết quả sàng lọc E2 (không CHECK — quy ước `pending` · `clear` · `review`) | — |
| `flags` | JSONB | Không | Cờ HẬU KIỂM («v3.6» — E.11.1): `ekyc_low_score` · `aml_hit` · `e2_deferred` (E2 bù sau) · `name_mismatch` · `e1_manual` · `sampled` (mẫu 10%) | vd `["sampled"]` |
| `submitted_at` | timestamptz | Có | Thời điểm nộp — mốc SLA HẬU KIỂM hồ sơ có cờ ≤24h («v3.6») | — |
| `decided_at` | timestamptz | Không | Thời điểm ra quyết định; NULL khi đang xử lý | — |
| `decided_by` | UUID | Không | Cán bộ quyết định (duyệt tay E.11.2–E.11.4); NULL khi auto-activate (C10) | FK → `app_user.id` |
| `reject_reason` | TEXT | Không | Lý do từ chối — bắt buộc nghiệp vụ khi `rejected` (AC-6.1) | — |
| `created_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |
| `updated_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |

\* Điền khi pipeline E1/E2 trả kết quả (bản ghi tạo ở `submitted` ngay khi `POST /ekyc/submit`).

- Map hiển thị API (E.2.3/E.11.1): `processing` ⇔ `submitted`; `approved` (API) ⇔ `auto_approved` (tự động C10) HOẶC `approved` (duyệt tay đồng ý — E.11.2, ghi `decided_by`/`decided_at`).

### 2.31. `payment` — dịch vụ **Commerce** · schema `commerce` *(module Payment — profile người mua)* «Peye-Haiti 15/08»

Lệnh trả do NGƯỜI DÙNG (mọi vai «v3.7») khởi tạo trên app Peye-Haiti (quét QR HTQR → xác nhận tên merchant → trả một chạm). **Tiền KHÔNG chạm Peye-Haiti**: server chuyển lệnh sang định chế TRẢ qua M-PAY (consent token scope `payment`), định chế thực hiện chuyển tiền (Switch/on-us) rồi báo kết quả về webhook; bên NHẬN vẫn nhận M4 và khớp bill như luồng S2 — hai phía độc lập, đối chiếu qua `ref_id`. Số TK đích (từ QR) chỉ đi QUA server tới định chế trả — KHÔNG lưu bản đầy đủ.

| Trường | Kiểu | Bắt buộc | Mô tả | Ràng buộc / Ví dụ |
|---|---|---|---|---|
| `id` | UUID | Có | Khóa chính | PK |
| `client_uuid` | UUID | Có | App sinh — idempotent (bấm trả 2 lần = 1 lệnh) | `UNIQUE` |
| `person_id` | UUID | Có | Người trả | ref logic → `merchant_identity.person.id` (xuyên schema) |
| `funding_link_id` | UUID | Có | TK nguồn trả (liên kết funding của cá nhân — mọi vai) | ref logic → `merchant_identity.account_link.id` |
| `merchant_id` | UUID | Không | Merchant đích (từ resolve QR) — NULL nếu đích ngoài danh bạ Peye-Haiti | ref logic → `merchant_identity.merchant.id` |
| `target_operator` | TEXT | Có | Mã định chế NHẬN từ QR tag 38-01 (dải 9332xx) | vd `933201` |
| `target_account_masked` 🔒 | TEXT | Có | Số TK đích — CHỈ lưu bản che; bản đầy đủ chỉ relay sang M-PAY, không ghi đĩa | vd `…7709` |
| `bill_code` | TEXT | Không | Mã bill từ QR động tag 62-01 — bên nhận gạch mức ① | vd `B-1007-17` |
| `amount_ct` | BIGINT | Có | Số tiền (centime) | > 0 |
| `currency` | TEXT | Có | Tiền tệ | default `'HTG'` |
| `status` | TEXT | Có | Vòng đời lệnh — state machine TSD §6b (`succeeded`/`failed` = cuối bất biến; `timeout` = tạm; «v3.5»: +`sca_required` khi lệnh > `PAY_SCA_THRESHOLD` chờ OTP định chế) | CHECK: `created` · `submitted` · `sca_required` · `succeeded` · `failed` · `timeout` (nghĩa tại §3) |
| `sca_challenge_id` | TEXT | Không | «v3.5» Mã challenge OTP do định chế cấp (C.7 nhánh `sca_required`) — ghép khi nộp OTP (E.16.6 → C.9) | NULL khi lệnh ≤ ngưỡng |
| `sca_expires_at` | timestamptz | Không | «v3.5» Hạn OTP phía định chế — quá hạn chưa xác nhận → định chế chốt `failed`/`sca_failed`; sweeper hỏi C.8 sau hạn + 5′ | — |
| `sca_msisdn_masked` | TEXT | Không | «v3.5» SĐT nhận OTP (che) — app hiển thị cho người dùng biết mã về số nào; phục vụ resume E.16.3 | vd `+509****3456` |
| `sca_attempts_left` | SMALLINT | Không | «v3.5» Số lần nhập còn lại (định chế trả về, cập nhật sau mỗi lần sai) | — |
| `failure_reason` | TEXT | Không | Lý do thất bại — MÃ DỮ LIỆU, không phải mã lỗi API (từ định chế: `insufficient_funds` · `declined` · `limit` · `other`; nội bộ: `expired` — job sweeper quá `PAY_CREATE_TTL`) | NULL khi thành công |
| `ext_payment_id` | TEXT | Không | Mã lệnh tại định chế trả (M-PAY trả về) | `UNIQUE` khi không NULL |
| `ref_id` | TEXT | Không | RefID Switch — khớp chéo với `credit_event.ref_id` bên nhận | — |
| `submitted_at` | timestamptz | Không | Thời điểm gửi sang M-PAY | — |
| `finished_at` | timestamptz | Không | Thời điểm có kết quả cuối — SLA xác nhận ≤3s P95 (`PAY_CONFIRM_SLA`) | — |
| `created_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |
| `updated_at` | timestamptz | Có | «bổ sung chuẩn» | default `now()` |

- Chỉ mục: `UNIQUE(client_uuid)` · partial `UNIQUE(ext_payment_id)` · `INDEX(person_id, created_at DESC)`.
- Khiếu nại: người mua tạo case từ NM-04 → `case.source='buyer_app'`, tham chiếu bằng cột `case.payment_id` (ref logic xuyên schema); người mua theo dõi qua trường `dispute` của E.16.3.
- Quá `PAY_TIMEOUT` không có kết quả → `timeout` + job hỏi lại M-PAY.2; retention 5 năm.

### 2.32. `outbox` — hạ tầng **mỗi schema một bảng** (mẫu transactional outbox)

Bảng phát sự kiện tin cậy: dịch vụ ghi bản ghi nghiệp vụ **và** dòng `outbox` trong **CÙNG một transaction**; tiến trình relay đọc bảng này rồi publish sang **Kafka SAU COMMIT** → không bao giờ có chuyện «đã đổi DB nhưng mất sự kiện» (TSD §4, §5). Có mặt trong **cả 4 schema dịch vụ** (`merchant_identity` · `commerce` · `backoffice` · `notification`).

| Trường | Kiểu | Bắt buộc | Mô tả | Ràng buộc / Ví dụ |
|---|---|---|---|---|
| `id` | BIGSERIAL | Có | Khóa chính — **ngoại lệ**: dùng BIGSERIAL để relay đọc theo thứ tự ghi | PK |
| `topic` | TEXT | Có | Topic Kafka đích | vd `credit.received` · `match.completed` |
| `key` | TEXT | Có | Khóa phân vùng Kafka — quy ước **`merchant_id`** (giữ thứ tự nhân-quả theo merchant) | vd `9f3c…` |
| `payload` | JSONB | Có | Nội dung sự kiện đúng schema TSD §4 (luôn chứa `event_id` để bên nhận idempotent) | — |
| `created_at` | timestamptz | Có | Thời điểm ghi (trong transaction nghiệp vụ) | default `now()` |
| `published_at` | timestamptz | Không | Thời điểm relay publish thành công; **NULL = chưa gửi** (relay quét NULL) | NULL khi còn hàng đợi |

- Relay retry cho tới khi Kafka nhận; consumer chống trùng theo `event_id` (at-least-once). Mất broker → **phát lại từ `outbox`** (TSD §9.4: Kafka không sao lưu, nguồn sự thật là PostgreSQL + `outbox`).
- **Không bổ sung** `updated_at` — bản ghi chỉ đổi một lần khi set `published_at`; purge dòng đã publish sau 7 ngày (cùng retention Kafka).


---

## 3. Bảng enum tập trung

Toàn bộ 28 enum (`TEXT` + `CHECK`) trong schema — giá trị đúng theo DDL TSD §5 (gồm «bổ sung chuẩn v1.1»), nghĩa tiếng Việt:

| Bảng.Cột | Giá trị | Nghĩa tiếng Việt |
|---|---|---|
| `merchant.status` | `draft` | Nháp — hồ sơ đang tự khai, chưa nộp đủ |
| `merchant.status` | `pending` | «v3.6» Hồ sơ vai bán đang khai dở / eKYC chưa PASS — KHÔNG còn nghĩa «chờ duyệt» (tạo xong là `active` ngay) |
| `merchant.status` | `need_more` | Cần bổ sung — yêu cầu chụp lại/thêm thông tin (NB-1C) |
| `merchant.status` | `rejected` | Từ chối — kèm lý do bắt buộc |
| `merchant.status` | `active` | Hoạt động — được nhận tiền |
| `merchant.status` | `suspended` | Tạm khóa — BRH khóa; gắn cờ hạn chế, app bị chặn thao tác ghi |
| `merchant.status` | `closed` | Đóng — chấm dứt; thu hồi standee + thu hồi token (M1b) |
| `application.status` | `submitted` | Đã nộp — pipeline E1/E2 đang chạy (API hiển thị `processing`) |
| `application.status` | `auto_approved` | «v3.6» Kích hoạt tức thời khi tạo xong (eKYC PASS) — nghĩa mặc định của mọi hồ sơ; mẫu 10% gắn `sampled` hậu kiểm |
| `application.status` | `pending_review` | «v3.6» Cờ HẬU KIỂM (điểm thấp/AML hit/E2 bù) — gian hàng VẪN active; BRH xem ≤24h, kết luận ghi `decided_by`/`decided_at`, xấu thì suspend |
| `application.status` | `approved` | «v3.6»: ĐÓNG hậu kiểm (E.11.2, từ `pending_review` — gian hàng vốn đã active); ghi `decided_by`/`decided_at` |
| `application.status` | `need_more` | Cần bổ sung — yêu cầu chụp lại/thêm thông tin (NB-1C, E.11.4) |
| `application.status` | `rejected` | Từ chối — `reject_reason` bắt buộc (AC-6.1) |
| `account_link.status` | `active` | Liên kết đang hiệu lực |
| `account_link.status` | `grace` | Ân hạn — TK cũ giữ liên kết 30 ngày sau đổi TK (`OLD_LINK_GRACE`); vẫn nhận báo có, vẫn gạch bill |
| `account_link.status` | `revoked` | Đã thu hồi liên kết/token (M1b) |
| `token.status` | `active` | Token hiệu lực |
| `token.status` | `expiring` | Sắp hết hạn — vào diện gia hạn trước D-7 (`TOKEN_RENEW_BEFORE`) |
| `token.status` | `revoked` | Đã thu hồi — mọi call sau đó bị bank từ chối |
| `standee.status` | `ordered` | Đã đặt in (theo đợt kích hoạt) |
| `standee.status` | `printed` | Đã in xong |
| `standee.status` | `delivered` | Đã giao tới chợ |
| `standee.status` | `mounted` | Đã dán tại quầy (merchant xác nhận) |
| `standee.status` | `replacing` | Chờ thay — đổi TK nhận → QR mới, `qr_ver` tăng, in lại |
| `standee.status` | `recalled` | Đã thu hồi — merchant đóng gian hàng |
| `credit_event.source` | `m4` | Webhook báo có realtime từ bank nhận |
| `credit_event.source` | `m3poll` | Sinh từ quét lịch sử M3 (M3-poll) khi webhook gián đoạn — `event_id` tiền tố `poll:`, cờ `replayed` |
| `match_result.level` | `PENDING` | Mới nhận/chờ xử lý — tạo ngay khi nhận credit; mẫu số KPI tính từ đây |
| `match_result.level` | `LINK` | Khớp mức ① qua TK liên kết — ưu tiên `addenda.payment_ref` (đích danh B.5); sau đó `addenda.bill_id` hợp lệ hoặc duy nhất 1 bill trùng tiền trong cửa sổ |
| `match_result.level` | `MANUAL` | Khớp mức ② — merchant xác nhận tay (bill/nợ/vãng lai) |
| `match_result.level` | `STRAY` | Vãng lai đóng — `PENDING` quá 72h (`STRAY_AFTER`); vẫn tính doanh thu vãng lai theo ngày |
| `match_result.target_type` | `bill` | Đích khớp là đơn tính tiền |
| `match_result.target_type` | `ledger` | Đích khớp là bút ghi sổ nợ (`ledger_entry`) |
| `match_result.target_type` | `stray` | Không gắn đích — tiền vãng lai |
| `product.moderation` | `pending` | Chờ hậu kiểm — vẫn hiển thị ngay (C9), nhãn chỉ nội bộ |
| `product.moderation` | `ok` | Đã kiểm, hợp lệ |
| `product.moderation` | `removed` | Đã gỡ — vi phạm/bị báo cáo |
| `bill.status` | `open` | Chờ thu |
| `bill.status` | `paid` | Đã thu qua QR — **chỉ server đặt** qua matching |
| `bill.status` | `cash` | Đã thu tiền mặt — ngoài dòng tiền QR/đối soát bank |
| `bill.status` | `cancelled` | Đã hủy (ghi log) |
| `bill.status` | `expired` | Hết hạn 24h — có nút tạo lại |
| `bill.status` | `credit` | Bán chịu — chuyển sang sổ nợ (NB-15) |
| `ledger_entry.type` | `debt` | Bút ghi nợ |
| `ledger_entry.type` | `repay` | Bút ghi trả nợ |
| `ledger_entry.origin` | `manual` | Merchant tự ghi (client tạo) |
| `ledger_entry.origin` | `auto` | Server sinh khi gạch nợ từ tiền về (S7 — sau khi merchant xác nhận) |
| `case.type` | `wrong_amount` | Sai số tiền |
| `case.type` | `not_received` | Báo không nhận được (tiền/hàng) |
| `case.type` | `duplicate` | Giao dịch trùng lặp |
| `case.type` | `fraud_suspect` | Nghi gian lận |
| `case.type` | `other` | Loại khác |
| `case.status` | `open` | Mới mở — SLA phản hồi đầu 24h |
| `case.status` | `awaiting_merchant` | Chờ merchant giải trình/nộp chứng cứ |
| `case.status` | `investigating` | Đang điều tra |
| `case.status` | `concluded_refund` | Kết luận hoàn — chỉ khi `refund_verified = true` (xác minh bút toán chuyển trả) |
| `case.status` | `concluded_reject` | Kết luận bác khiếu nại |
| `case.status` | `closed` | Đã đóng |
| `case.source` | `merchant_app` | Mở từ app người bán (E.5.4) |
| `case.source` | `portal` | Mở tại portal BRH (E.12.3) |
| `case.source` | `hotline` | Tiếp nhận qua hotline — cán bộ nhập tại portal (E.12.3) |
| `case.source` | `recon` | Chuyển từ chênh lệch đối soát (E.14.7 `to_case`) |
| `case.source` | `buyer_app` | Người mua khiếu nại khoản đã trả từ NM-04 (E.16.5) «Peye-Haiti 15/08» |
| `adjustment.source` | `case` | Phát sinh từ kết luận case |
| `adjustment.source` | `recon` | Phát sinh từ chênh lệch đối soát (module Đối soát của Back-office tạo nháp) |
| `adjustment.direction` | `debit` | Điều chỉnh giảm doanh số |
| `adjustment.direction` | `credit` | Điều chỉnh tăng doanh số |
| `adjustment.status` | `draft` | Nháp — chờ phê duyệt |
| `adjustment.status` | `approved` | Đã duyệt 4 mắt (checker ≠ maker) |
| `adjustment.status` | `posted` | Đã ghi sổ — khóa, không sửa |
| `aml_alert.source` | `e2` | Trúng danh sách sàng lọc E2 (BRH-System) |
| `aml_alert.source` | `rule` | Luật ngưỡng/hành vi — `AML_TX_FLAG` · `AML_DAY_FLAG` · `AML_SMURF` |
| `aml_alert.source` | `limit` | Vượt ngưỡng ngày AML (`AML_DAY_FLAG`) (sự kiện `limit.breached`) |
| `aml_alert.status` | `open` | Mở — chưa xử lý |
| `aml_alert.status` | `awaiting_reply` | Chờ merchant giải trình |
| `aml_alert.status` | `investigating` | Đang xử lý |
| `aml_alert.status` | `dismissed` | Bỏ qua — bắt buộc ghi lý do |
| `aml_alert.status` | `escalated` | Leo thang (tạm khóa/chuyển cấp) |
| `recon_run.status` | `ingesting` | Đang nạp file E3 |
| `recon_run.status` | `matched` | Khớp xong — không lệch |
| `recon_run.status` | `discrepancy` | Có chênh lệch — sinh bản ghi `discrepancy` |
| `recon_run.status` | `closed` | Đóng phiên |
| `discrepancy.dtype` | `missing_in_mms` | Switch có — MMS không thấy (thường do rơi webhook → phục hồi M3-poll) |
| `discrepancy.dtype` | `missing_in_e3` | MMS có — bảng kê E3 không có |
| `discrepancy.dtype` | `amount_diff` | Lệch số tiền giữa hai nguồn |
| `discrepancy.status` | `open` | Mở |
| `discrepancy.status` | `replaying` | Đang quét M3-poll lấp khoảng (phục hồi) |
| `discrepancy.status` | `adjusting` | Đang lập bút toán điều chỉnh (4 mắt) |
| `discrepancy.status` | `case` | Đã chuyển thành case tra soát |
| `discrepancy.status` | `closed` | Đóng — ≤2 ngày làm việc, có vết nguyên nhân → hành động |
| `param.status` | `active` | Giá trị `value` đang hiệu lực — không có đề xuất chờ |
| `param.status` | `pending_approval` | Có `value_pending` chờ phê duyệt 4 mắt (E.13.3/E.13.4) |
| `app_user.role` | `admin` | Quản trị hệ thống — không xem dữ liệu giao dịch |
| `app_user.role` | `approver` | Duyệt hồ sơ + phê duyệt 4 mắt |
| `app_user.role` | `supervisor_aml` | Giám sát giao dịch/case/AML |
| `app_user.role` | `ops_read` | Vận hành — chỉ đọc |
| `app_user.role` | `inspector_read` | Thanh tra — chỉ đọc |
| `app_user.status` | `invited` | Đã mời — chờ đặt mật khẩu + enroll TOTP (link 24h, E.13.7) |
| `app_user.status` | `active` | Đang hoạt động |
| `app_user.status` | `disabled` | Đã khóa — thu hồi phiên ngay (E.13.8) |
| `notification.status` | `queued` | Xếp hàng chờ gửi |
| `notification.status` | `sent` | Đã gửi |
| `notification.status` | `acked` | App xác nhận đã nhận (trong 60 giây — quyết định có fallback SMS hay không) |
| `notification.status` | `failed` | Gửi lỗi |
| `payment.status` | `created` | Đã tạo từ lần quét — CHỜ người mua xác nhận (TTL `PAY_CREATE_TTL` 15′, quá hạn → failed('expired') bởi job payment-sweeper) «Peye-Haiti 15/08» |
| `payment.status` | `submitted` | Đã gửi M-PAY, chờ định chế trả xử lý |
| `payment.status` | `sca_required` | «v3.5» Lệnh > `PAY_SCA_THRESHOLD` — định chế đã gửi SMS OTP cho chủ TK, chờ người dùng nhập (E.16.6 → C.9); quá `sca_expires_at` → failed('sca_failed') |
| `payment.status` | `succeeded` | Định chế trả xác nhận đã chuyển — có biên lai số |
| `payment.status` | `failed` | Định chế trả từ chối — xem `failure_reason` |
| `payment.status` | `timeout` | Quá `PAY_TIMEOUT` không có kết quả — job hỏi lại M-PAY.2 |

Giá trị quy ước không có CHECK trong DDL (tham khảo): `case.evidence[].side` (`merchant` · `buyer` · `brh` — chứng cứ phía nào, E.12.5) · `person.lang` (`ht` Kreyòl · `fr` Pháp) · `application.aml_status` (`pending`/`clear`/`review`) · `credit_event.non_revenue_reason` (`personal`/`family`/`other` — E.5.6) · `notification.target_kind` (`merchant`/`buyer`/`user`) · `notification.channel` (`push`/`sms`/`inapp`) · `match_result.receipt_channel` (`app`/`sms`) · `payment.failure_reason` (`insufficient_funds`/`declined`/`limit`/`sca_failed` «v3.5»/`other` từ định chế + `expired` nội bộ).

---

## 4. Quan hệ khóa ngoại (FK) & tham chiếu logic xuyên schema

**Quy tắc chốt (TSD §5)**: **FK vật lý (`REFERENCES`) CHỈ trong cùng schema**. Quan hệ **xuyên schema** = **tham chiếu LOGIC** — cột UUID trần, **không có ràng buộc `REFERENCES`**, không cascade, không join trực tiếp; dữ liệu lấy qua REST nội bộ hoặc sự kiện Kafka (bên nhận snapshot lại field cần dùng). Cột «Loại» dưới đây phân biệt hai nhóm — đây là **thay đổi so với v1.0/v1.1** (trước khi tách schema, mọi quan hệ đều là FK vật lý trong một schema `mms` duy nhất).

| Bảng con.Cột | Trỏ tới | Loại | Bản số | Ghi chú |
|---|---|---|---|---|
| `merchant.market_id` | `backoffice.market.id` | **ref logic** | N–1 | Xuyên schema (`merchant_identity`→`admin`) — đọc qua REST nội bộ / cache tham số |
| `merchant.person_id` | `merchant_identity.person.id` | FK vật lý | 1–1 | Chủ gian hàng — cùng schema |
| `ekyc_result.person_id` | `merchant_identity.person.id` | FK vật lý | N–1 | Nhiều lần eKYC (chụp lại) |
| `application.merchant_id` | `merchant_identity.merchant.id` | FK vật lý | N–1 | «bổ sung v1.1» — mỗi lần nộp một bản ghi |
| `account_link.person_id` | `merchant_identity.person.id` | FK vật lý | N–1 | «Peye-Haiti 15/08» — TK nguồn trả của cá nhân (mọi vai «v3.7»); CHECK đúng một trong (merchant_id, person_id) |
| `payment.person_id` | `merchant_identity.person.id` | **ref logic** | N–1 | «Peye-Haiti 15/08» — xuyên schema (`commerce`→`merchant_identity`) |
| `payment.funding_link_id` | `merchant_identity.account_link.id` | **ref logic** | N–1 | «Peye-Haiti 15/08» — xuyên schema |
| `payment.merchant_id` | `merchant_identity.merchant.id` | **ref logic** | N–1 | «Peye-Haiti 15/08» — đích trả (NULL nếu ngoài danh bạ) |
| `application.ekyc_result_id` | `merchant_identity.ekyc_result.id` | FK vật lý | N–1 | «bổ sung v1.1» — kết quả E1 của lần nộp |
| `application.decided_by` | `backoffice.app_user.id` | **ref logic** | N–0..1 | Xuyên schema — NULL khi auto-activate (C10) |
| `auth_session.person_id` | `merchant_identity.person.id` | FK vật lý | N–0..1 | Đúng 1 trong 2 với `user_id` |
| `auth_session.user_id` | `backoffice.app_user.id` | **ref logic** | N–0..1 | Phiên portal — xuyên schema |
| `account_link.merchant_id` | `merchant_identity.merchant.id` | FK vật lý | N–1 | 1..2 bank; +1 dòng `grace` khi đổi TK |
| `token.link_id` | `merchant_identity.account_link.id` | FK vật lý | 1–1 | `UNIQUE(link_id)` — REFERENCES tường minh |
| `standee.merchant_id` | `merchant_identity.merchant.id` | FK vật lý | N–1 | ERD: merchant có 0..1 standee hiệu lực |
| `standee.account_link_id` | `merchant_identity.account_link.id` | FK vật lý | N–1 | REFERENCES tường minh — nguồn payload QR |
| `standee.market_id` | `backoffice.market.id` | **ref logic** | N–1 | Xuyên schema |
| `credit_event.merchant_id` | `merchant_identity.merchant.id` | **ref logic** | N–1 | Xuyên schema (`commerce`→`merchant_identity`) · partition key Kafka |
| `credit_event.link_id` | `merchant_identity.account_link.id` | **ref logic** | N–0..1 | Xuyên schema — NULL khi nguồn thiếu chi tiết (mức ②) |
| `match_result.credit_event_id` | `commerce.credit_event.id` | FK vật lý | 1–1 | Cùng schema `commerce` · **`UNIQUE` = invariant «1 credit ↔ ≤1 đích»** (thay cho saga) |
| `match_result.target_id` | `commerce.bill.id` \| `commerce.ledger_entry.id` | đa hình | N–0..1 | Cùng schema `commerce` (cùng transaction khớp) — không FK vì đa hình |
| `product.merchant_id` | `merchant_identity.merchant.id` | **ref logic** | N–1 | Xuyên schema |
| `bill.merchant_id` | `merchant_identity.merchant.id` | **ref logic** | N–1 | Xuyên schema |
| `bill_item.bill_id` | `commerce.bill.id` | FK vật lý | N–1 | Cùng schema |
| `bill_item.product_id` | `commerce.product.id` | FK vật lý | N–0..1 | NULL = món tự do |
| `debtor.merchant_id` | `merchant_identity.merchant.id` | **ref logic** | N–1 | Xuyên schema |
| `ledger_entry.debtor_id` | `commerce.debtor.id` | FK vật lý | N–1 | Cùng schema |
| `ledger_entry.credit_event_id` | `commerce.credit_event.id` | FK vật lý | N–0..1 | Cùng schema `commerce` — gạch nợ từ tiền về (S7) |
| `bill.paid_by_credit_event_id` | `commerce.credit_event.id` | FK vật lý | N–0..1 | Cùng schema `commerce` — ghi trong CÙNG transaction khớp |
| `ledger_entry.bill_id` | `commerce.bill.id` | FK vật lý | N–0..1 | «bổ sung v1.1» — bán chịu từ bill (E.6.3) |
| `ledger_entry.reversed_by_entry_id` | `commerce.ledger_entry.id` | FK vật lý | N–0..1 | «bổ sung v1.1» — bút ghi đảo (self-FK) |
| `case.merchant_id` | `merchant_identity.merchant.id` | **ref logic** | N–1 | Xuyên schema · `case.ref_id` cũng là tham chiếu logic RefID |
| `case.credit_event_id` | `commerce.credit_event.id` | **ref logic** | N–0..1 | Xuyên schema — bắt buộc khi `ref_id` NULL (GD on-us) |
| `case.payment_id` | `commerce.payment.id` | **ref logic** | N–0..1 | «Peye-Haiti 15/08 vòng 2» — case người mua (source=buyer_app) |
| `case.assigned_to` | `backoffice.app_user.id` | FK vật lý | N–0..1 | Cùng schema `backoffice` — cán bộ nhận ca |
| `adjustment.case_id` | `backoffice."case".id` | FK vật lý | N–0..1 | Bắt buộc khi `source='case'` |
| `adjustment.recon_run_id` | `backoffice.recon_run.id` | FK vật lý | N–0..1 | **Cùng schema** (khiếu nại + đối soát nay chung module Compliance của Back-office) — bắt buộc khi `source='recon'` |
| `adjustment.merchant_id` | `merchant_identity.merchant.id` | **ref logic** | N–1 | Xuyên schema |
| `adjustment.maker` / `.checker` | `backoffice.app_user.id` | FK vật lý | N–1 / N–0..1 | Cùng schema `backoffice` — 4 mắt: checker ≠ maker |
| `aml_alert.merchant_id` | `merchant_identity.merchant.id` | **ref logic** | N–1 | Xuyên schema |
| `discrepancy.run_id` | `backoffice.recon_run.id` | FK vật lý | N–1 | Cùng schema |
| `param.maker` / `.checker` | `backoffice.app_user.id` | FK vật lý | N–1 / N–0..1 | Cùng schema `backoffice` — 4 mắt |
| `param.proposed_by` / `.approved_by` | `backoffice.app_user.id` | FK vật lý | N–0..1 / N–0..1 | «bổ sung v1.1» — đề xuất đang chờ / lần duyệt gần nhất |
| `audit_log.actor` | `backoffice.app_user.id` \| `merchant_identity.person.id` | đa hình | N–1 | Đa hình + xuyên schema — không FK |
| `notification.target_id` | theo `target_kind` (merchant/buyer/user) | đa hình | N–1 | Đa hình + xuyên schema — không FK |
| `outbox` (mọi schema) | — | — | — | Không FK — bảng hạ tầng phát sự kiện (§2.32) |

---

## 5. Retention & dữ liệu cá nhân (PII)

### 5.1. Thời hạn lưu trữ (TSD §5)

| Dữ liệu | Thời hạn | Ghi chú |
|---|---|---|
| `audit_log` | **10 năm** (C17) | Append-only + hash chain; xuất bằng chứng theo yêu cầu thanh tra; partition tháng khi scale |
| Ảnh eKYC (object MinIO của `front_key`/`back_key`/`selfie_key`) | **5 năm sau khi đóng gian hàng** | DB chỉ giữ **khóa MinIO**, không lưu ảnh; truy cập bằng presigned URL có TTL; bucket mã hóa |
| `credit_event` · `match_result` | 5 năm | Partition RANGE theo tháng thiết kế sẵn (bật khi >5.000 merchant) |
| `notification` | 12 tháng | Partition tháng thiết kế sẵn |
| `idem_key` | 48 giờ | Cron purge |
| Các bảng còn lại | Theo đời hệ thống | TSD không quy định thời hạn riêng |

### 5.2. Bản đồ trường PII/bí mật (đánh dấu 🔒 trong §2)

| Nhóm | Trường | Biện pháp |
|---|---|---|
| Danh tính merchant | `person.full_name` · `dob` · `cin_no` · `nif_no` · `msisdn` | AES-256 at rest; hiển thị tối thiểu theo màn; không ghi log rõ |
| Bí mật xác thực | `person.pin_hash` · `auth_session.refresh_hash` · `app_user.totp_secret_enc` | Chỉ lưu băm (Argon2id)/mã hóa envelope; so sánh constant-time |
| Thiết bị | `auth_session.fingerprint` | Gắn phiên đăng nhập với thiết bị, truy vết phiên hỗ trợ |
| Ảnh eKYC | `ekyc_result.front_key` · `back_key` · `selfie_key` | Key MinIO — object mã hóa, TTL truy cập |
| Tài khoản nhận | `account_link.account_no_enc` (envelope Vault) · `account_no_hmac` (tra cứu, không đảo ngược) · `account_no_masked` · `holder_name` · `credit_event.account_no_masked` · `discrepancy.account_no` | Số TK đầy đủ **chỉ** tồn tại dạng mã hóa; mọi hiển thị dùng bản che `…7709` |
| Token Open Banking | `token.access_enc` · `refresh_enc` | Mã hóa envelope Vault (AES-256-GCM), xoay KEK 12 tháng |
| Người trả (M4) | `credit_event.payer_msisdn` · `payer_name` · `narrative` | Theo chuẩn OB do BRH ban hành; chỉ nuôi biên lai & gạch bill |
| Sổ nợ (thuộc merchant — consent C7) | `debtor.name` · `msisdn` | Thuộc sở hữu merchant; client lưu IndexedDB mã hóa AES-GCM (khóa từ PIN); chỉ dùng chấm điểm khi opt-in |
| Người mua | `match_result.sent_msisdn` (SĐT nhận biên lai SMS) | — |
| Người mua (payment) «Peye-Haiti 15/08» | `payment.target_account_masked` | CHỈ bản che; số TK đích đầy đủ relay sang M-PAY qua mTLS, KHÔNG ghi đĩa; TK nguồn = `account_link` (đã envelope) |
| Portal | `app_user.email` | — |
| Gián tiếp | `audit_log.payload` · `case.evidence[].object_key` (+object) | Có thể chứa PII — truy cập theo RBAC (inspector_read/supervisor_aml) |

### 5.3. Ghi chú tuân thủ

- **Không có bảng tài khoản ảo**: kiến trúc chốt là QR/standee in **số TK thật đã liên kết** (Q4) — mọi truy vết dòng tiền dựa trên `account_link` + `credit_event`; MMS ngoài đường tiền, không giữ số dư.
- Trường tiền (`*_ct`) không phải PII nhưng là dữ liệu tài chính nhạy cảm — vai trò `admin` không xem dữ liệu giao dịch (C11).
- Mọi thao tác đọc/ghi dữ liệu 🔒 từ portal đều để vết trong `audit_log` (hash chain, 10 năm).
- Xóa dữ liệu: hệ thống không dùng soft-delete (trừ `product.deleted_at`); yêu cầu xóa/ẩn dữ liệu cá nhân xử lý theo chính sách BRH ở tầng nghiệp vụ, không xóa vật lý bản ghi tài chính trong thời hạn lưu trữ.

---

*Tài liệu sinh từ DDL TSD §5 (Peye-Haiti-TSD-001) — mọi sai khác giữa tài liệu này và migration thực tế tại `/db/migrations` phải được cập nhật ngược về cả hai phía. Tổng hợp: **28 bảng nghiệp vụ · 310 trường (20/08: +4 cột sca_* «v3.5»)** (15/08 Peye-Haiti: +bảng `payment` 18 trường, +`kyc_level`/`public_phone`/`account_link.person_id`; vòng 2: +`account_no_hmac`/`case.payment_id`; trước đó +7 trường CR-1/2/4/5/6/7) **+ bảng hạ tầng `outbox` 6 trường** (mỗi schema một bảng) · 28 enum/110 giá trị · **45 quan hệ: 25 FK vật lý (cùng schema) · 17 tham chiếu logic (xuyên schema) · 3 đa hình**. (v3.4 (CANON2): bỏ M7/M4b/qr_intent/report_schedule/buyer_profile, gộp device→auth_session (di 2 cột `fingerprint`/`is_agent_session`), matching 2 mức [bỏ `HIST`] — −4 bảng, −32 trường, −2 enum/−7 giá trị, −6 quan hệ; v3.3: bỏ API M5 + gộp còn 1 bậc KYC — bỏ 1 cột phân hạng định danh (−1 trường), 1 enum tương ứng (−1 enum/−2 giá trị), 2 tham số liên quan; v3.1: **mỗi dịch vụ một schema** — gộp `ingest`→`commerce`, `compliance`+`admin`→`backoffice`; bỏ cơ chế cửa sổ an toàn thiết bị (2 cột `device`), 4 quan hệ nâng lên FK vật lý; v3.0: **4 dịch vụ** — gộp biên lai vào `match_result`, chứng cứ vào `case.evidence` JSONB, danh mục agent vào `param` (bỏ 3 bảng `receipt`/`evidence`/`field_agent`); cờ khớp-muộn `late_auto` ghi trong chính transaction khớp; v2.0: event bus **Kafka**, bỏ mọi lệnh ghi nội bộ và khóa lạc quan xuyên dịch vụ, thêm bảng `outbox`; v1.1: +2 bảng `application`/`report_schedule` — bỏ cột hash PIN kênh USSD dự phòng của `person`.)*

## 6. Phụ lục — Bản đồ khai báo nhật ký giao dịch quốc gia (CR-8 · 15/08)

Văn bản BRH 12/08 (Phần III.3) định nghĩa bản ghi nhật ký quốc gia gồm 7 nhóm trường A–G. MMS **ngoài đường tiền**, chỉ nhìn thấy PHÍA NHẬN — bảng dưới chứng minh MMS khai báo được góc nhìn merchant-system từ dữ liệu sẵn có, **không thêm bảng mới, không xây pipeline** (JNT trong dự án này là module nhỏ; hợp đồng dữ liệu bàn khi có thật).

| Nhóm BRH | Trường MMS | Ghi chú |
|---|---|---|
| A · Định danh | `credit_event.ref_id` (RefID Switch; on-us dùng `event_id`) · `merchant.national_merchant_id` (khi có, tạm thời `merchant.code`) · `credit_event.payer_operator` · `payer_person_id` (cột chờ CR-7); khi người mua trả bằng app Peye-Haiti: `payment.person_id`/`funding_link` đã có sẵn phía trả «Peye-Haiti 15/08» · InstitutionID: không áp dụng (MMS không thu hộ tổ chức công) | — |
| B · Số tiền | `credit_event.amount_ct` · `currency` | Phí pilot = 0 (`FEE_PILOT`) |
| C · QR | Loại QR suy ra: `addenda.bill_id` có → động, không → tĩnh; phiên bản = `standee.qr_ver` | **KHÔNG gửi chuỗi QR thô** (chứa số TK thật) |
| D · API | `booked_at` (T0 bank ghi Có) · `received_at` (MMS nhận) | **KHÔNG gửi token OAuth / chữ ký HMAC thô** — chỉ mã khóa/băm (lập trường ④, 12/08) |
| E · Quyết toán | Trạng thái khớp (`match_result.level`) + tham chiếu đối soát E3 (`recon_run`) | Quyết toán thật do Switch/BRH khai — ngoài MMS |
| F · An ninh | Không chấm điểm quốc gia; cờ AML nội bộ (`aml_alert`) chỉ cung cấp khi BRH yêu cầu bằng văn bản | — |
| G · Metadata | `channel` = `qr_static` / `qr_dynamic` | Với người trả dùng app Peye-Haiti (profile Client): thiết bị = `auth_session` phía người mua, khai được khi BRH yêu cầu; người trả dùng app ví khác: thuộc app đó «Peye-Haiti 15/08» |

**Quy định 3 KHÔNG (dữ liệu MMS gửi ra mọi hệ thống quốc gia):** ① không chuỗi QR thô · ② không bí mật sống (token OAuth, HMAC — chỉ mã khóa/băm) · ③ không số tài khoản đầy đủ (chỉ bản che `…7709`). Nguyên tắc cứng, ghi tại API Spec (đầu mục B) và SSD §8.
