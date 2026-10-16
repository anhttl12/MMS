# Review chéo SRS — conflict giữa các tài liệu

- **Ngày:** 16/10/2026
- **Phạm vi:** `common/COMMON-01` · `Phu-luc/CFG-01..04`, `PL-01`, `PL-02` · `srs/CN-01` → `CN-08`
- **Đối chiếu thêm:** `project-context/PeyeHaiti_API_Spec.md` — mục D.4 (E3-reg)
- **Trạng thái:** Nhóm A, B và E3-reg **đã chốt và đã sửa** vào tài liệu. Nhóm C, D **chờ BA trả lời**.

Ký hiệu: ✅ đã sửa · ⏳ chờ quyết định · **(*)** mã/tham số mới phát sinh, chưa có trong danh mục

---

## A. Conflict nghiệp vụ — đã chốt

| # | Vấn đề | Quyết định | File đã sửa |
|---|---|---|---|
| A1 | Nhập sai OTP Peye-Haiti: giữ mã hay hủy ngay | **Theo COMMON-01**: sai còn lượt thì giữ mã, trả `tries_left`; hết `OTP_MAX_ATTEMPTS` thì hủy mã (`PIN-422-OTPLOCKED`). SRS **refer COMMON-01 Luồng 2/3 theo cách viết của CN-01**, không mô tả lại | ✅ CFG-03 · CN-01 · CN-02 · CN-03 · CN-06 (15a) |
| A2 | Sai PIN đủ số lần có thu hồi phiên không | **Thu hồi mọi phiên** (COMMON-01 Luồng 1 · Bước 8). Người dùng vào lại thì chọn Quên PIN, đặt lại PIN theo CN-03 (hoặc chờ hết giờ) | ✅ CN-02 · CN-05 · CN-07 |
| A3 | Cách xác thực PIN cho hành động nhạy cảm | **Theo COMMON-01 Luồng 1**: PIN nhập ở NB-0F, gửi trong body API nghiệp vụ, không có API kiểm PIN riêng, không `verify_token` | ✅ CN-07 · CN-08 (đã đúng). **CN-05 là ngoại lệ có chủ đích**: giữ NB-14B, kiểm PIN hiện tại riêng trước khi nhập PIN mới — đã ghi chú ở CN-05 và COMMON-01 |
| A4 | Đổi tài khoản nhận có cần OTP | **Chỉ cần PIN.** Bước 7 CN-07 ghi rõ: liên kết mới **dùng lại token đang có**; token liên kết cũ **chưa bị thu hồi ngay** | ✅ CFG-01 (`STEPUP_AMOUNT_THRESHOLD`) · COMMON-01 mục 5 · CN-07 |
| A5 | Hủy liên kết đang `grace` | **Không cho hủy trực tiếp.** `grace` → `revoked` **chỉ qua JOB** của CN-07 khi hết `OLD_LINK_GRACE` **và** `standee_order.status = mounted`. NB-16A ẩn **Remove this account** khi `grace`; server trả `PIN-422-LINKGRACE` **(*)** | ✅ CN-06 · CN-08 |
| A6 | Hủy liên kết đang `expired` | **Bỏ qua lời gọi thu hồi** token tại định chế | ✅ CN-08 |
| A7 | Liên kết có phân loại nhận/trả không | **Không phân loại** trên giao diện lẫn hệ thống: tài khoản nhận tiền đồng thời là nguồn trả. Một trần chung `LINK_MAX_PER_PERSON` **(*)**; sở hữu theo `account_link.person_id` | ✅ CN-06 · CN-08 |
| A8 | Liên kết `revoked` có hiện trên NB-16 | **Không hiện** — theo CN-06 mục 2.2.2.1 | ✅ CN-06 · CN-07 |
| A9 | `PIN-000-OFFLINE` và `PIN-500-SYS` | **Theo COMMON-01 Mục 4**: OFFLINE = app phát hiện **không có mạng**; có mạng mà không nhận được phản hồi / server lỗi = `PIN-500-SYS` | ✅ CFG-03 · CN-03 · CN-04 · CN-05 · CN-06 · CN-07 · CN-08 |
| A10 | Khóa khẩn | **Chỉ qua hotline 8686 và thao tác trên portal BRH.** Bỏ `purpose = emergency_lock` | ✅ COMMON-01 · CN-02 |

### Lệch nhỏ — đã chốt

| # | Vấn đề | Quyết định | File đã sửa |
|---|---|---|---|
| N1 | Số `Terminated` đăng ký lại | CN-01 kiểm trùng `msisdn` **trừ các `person` đã `Terminated`** — tạo `person` mới | ✅ CN-01 |
| N2 | Đồng hồ gửi lại OTP | Đếm từ **`OTP_RESEND_AFTER`**, không phải `OTP_TTL` | ✅ CFG-01 · PL-01 · CN-03 |
| N3 | Liên kết `confirming` khi onboarding | CN-06 tự thử lại; **thành công thì server tự chạy tiếp CN-01 Luồng 7 từ Bước 2** để kích hoạt gian hàng | ✅ CN-01 · CN-06 |
| N4 | `merchant.status` trong CN-07 dùng `draft/pending/need_more/rejected/closed`, CN-01 chỉ có `draft/active/suspended` | ⏳ Đã phản biện DataDict + soạn **CR-STATUS-01** — xem mục **N4** bên dưới | — |

---

## N4. `merchant.status` — tình trạng hiện tại và đề xuất đồng bộ

### Tình trạng hiện tại

**Nguồn chuẩn** (DataDict v4.4 · DDL TSD §5) khai **7 giá trị**:

| Giá trị | Nghĩa theo DataDict | Ghi chú |
|---|---|---|
| `draft` | Nháp — hồ sơ đang tự khai, chưa nộp đủ | |
| `pending` | «v3.6» Hồ sơ vai bán đang khai dở / eKYC chưa PASS | **Trùng nghĩa với `draft`** từ khi chuyển sang mô hình "tạo là active" |
| `need_more` | Cần bổ sung — chụp lại / thêm thông tin | **Trùng** `application.status = need_more` |
| `rejected` | Từ chối — kèm lý do bắt buộc | Pilot **không còn** duyệt tay; hậu kiểm xấu thì `suspended` |
| `active` | Hoạt động — được nhận tiền | |
| `suspended` | Tạm khóa — BRH khóa, chặn thao tác ghi | |
| `closed` | Đóng — thu hồi standee + token (M1b) | Chưa có SRS đóng gian hàng |

**Cách các tài liệu đang dùng:**

| Tài liệu | Giá trị dùng | Lệch |
|---|---|---|
| **CN-01** | `draft` → `active` → `suspended` | Tiến độ hồ sơ theo dõi ở `application.status` (`draft` · `submitted` · `need_more` · `auto_approved`), **không** ở `merchant.status`. Luồng 6 · Bước 9 viết nhầm **"Pending"** trong khi sơ đồ trạng thái ghi giữ `draft`. Không nhắc `closed` |
| **CN-02** | `suspended` · `closed` _(chỉ đọc)_ | Khớp |
| **CN-06** | Không đổi `merchant.status` | Khớp |
| **CN-07** | Cả 7 giá trị | Bước 6: `suspended` / `closed` → `PIN-422-SHOPHOLD`; `draft` / `pending` / `need_more` / `rejected` → `PIN-422-PROFILE`. Dùng nguyên danh sách DataDict, nên lệch với CN-01 |
| **CFG-03** | `PIN-422-SHOPHOLD` = tạm khóa hoặc đã đóng · `PIN-422-PROFILE` = hồ sơ dở dang | Khớp ý nghĩa, không liệt kê giá trị |

**Bản chất:** từ v3.6 ("tạo là active"), `pending`, `need_more`, `rejected` của `merchant` không còn đường nào dẫn tới trong luồng pilot. Trạng thái **tiến độ hồ sơ** đã chuyển hẳn sang `application.status` + `next_step`, còn `merchant.status` chỉ trả lời câu hỏi **"gian hàng có nhận tiền được không"**.

### Phản biện DataDict (đối chiếu DataDict §2–§3 · DDL TSD §5 · API E.2.2–E.2.4, E.11.1–E.11.5)

**Gốc vấn đề:** v3.6 chuyển sang "tạo là active" nhưng DataDict chọn **"đổi NGHĨA, không đổi giá trị"**. Kết quả: `merchant.status` gánh cả tiến độ hồ sơ; `application.status` gánh ba chiều cùng lúc — tiến độ khai, kết quả kích hoạt, kết quả hậu kiểm.

**`merchant.status`**
- **M1** `draft` và `pending` trùng nghĩa — không có chuyển đổi giữa hai giá trị, không SRS nào đặt `pending`
- **M2** `need_more` không có đường vào — trùng `application.need_more`; từ v3.6 gian hàng active bị yêu cầu bổ sung thì đi `suspended`
- **M3** `rejected` mâu thuẫn với API — E.11.3 không nói merchant đổi gì, ghi chú v3.6 lại nói reject = suspend
- **M4** `activated_at` vẫn nhắc "BRH duyệt tay"

**`application.status`**
- **A1** Thiếu trạng thái "đang khai" — CN-01 tạo `application.draft` từ CH-00 nhưng enum bắt đầu từ `submitted`; đây là nguồn gốc chồng lấn
- **A2** `submitted` ba nghĩa: DataDict "E1/E2 đang chạy" · CN-01 "đã nộp, chờ liên kết TK" · API E.2.2 "nộp và kích hoạt trong một lệnh"
- **A3** Trộn hai chiều: `auto_approved` / `pending_review` / `approved` đều là gian hàng **đã active**, chỉ khác hậu kiểm
- **A4** Hai cơ chế hậu kiểm song song: mẫu 10% = `auto_approved` + cờ `sampled`; cờ rủi ro = `pending_review`
- **A5** `approved` đổi nghĩa ngược tên — nay là "đóng hậu kiểm OK"; E.2.3 còn gộp `auto_approved → approved`
- **A6** `pending_review` gần như không có đường vào ở pilot (chặn cứng điểm, AML sang `aml_alert`, bỏ cờ hậu kiểm onboarding — CR-J)
- **A7** `need_more` lẫn (a) chụp lại tự động trước khi nộp và (b) BRH yêu cầu bổ sung với gian hàng đã active — (b) không rõ còn nhận tiền không. E.2.4 cho sửa tay CIN/họ tên/ngày sinh, trái CN-01

### Đề xuất — chi tiết ở `reference/CR-STATUS-01_merchant-application-status.md`

| Trường | Trả lời câu hỏi | Giá trị |
|---|---|---|
| `merchant.status` | Gian hàng có nhận được tiền không | `draft` · `active` · `suspended` · `closed` |
| `application.status` | Hồ sơ onboarding đang ở bước nào | `draft` · `need_more` · `submitted` · `activated` |
| `application.review_status` **(mới)** | Hậu kiểm sau kích hoạt | `none` · `pending` · `ok` · `failed` |

Kích hoạt là điểm **duy nhất** hai trường đổi cùng lúc (`activated` ⇔ `active`). Hậu kiểm xấu → `review_status = failed` + `merchant = suspended`.

⏳ **Chờ BA/BRH chốt Q1–Q3 của CR-STATUS-01** — chưa sửa tài liệu:
- **Q1** Pilot có còn từ chối vĩnh viễn không — `closed` kèm lý do hay giữ `rejected`?
- **Q2** Gian hàng active bị yêu cầu bổ sung (E.11.4) có ngừng nhận tiền (`suspended`) không?
- **Q3** E.2.4 có cho sửa tay `cin_no` / `full_name` / `dob` không?

---

## B. Trùng mã — đã chốt

| Vấn đề | Quyết định | File đã sửa |
|---|---|---|
| NB-16B dùng cho 2 màn | NB-16B thuộc **CN-07**. Sheet xác nhận hủy của CN-08 đổi thành **NB-16C** (kể cả chỗ viết nhầm NB-15B) | ✅ CN-08 |
| MS00007 dùng cho 2 mẫu tin | `MS00007` = `LINK_ADDED` (CN-06). CN-08 dùng mã mới **`MS00009` · `LINK_REMOVED` (*)** | ✅ CN-08 |
| Tên MS00002 | `LOGIN_LOCK` | ✅ CN-02 |
| Tham chiếu mã chức năng sai | Đánh lại theo CN-01 → CN-08 hiện có; chức năng chưa có SRS **chỉ ghi tên** | ✅ CN-01 · CN-02 · CN-03 · CN-04 · CN-05 · CN-06 · CN-07 · CN-08 |

---

## E3-reg — đối chiếu API Spec D.4

Quy tắc: gọi lại (`PUT` trọn bộ danh mục) **mỗi khi** liên kết mới (M1) · đổi TK (S4, gồm TK cũ đang `grace`) · hết `grace`/thu hồi (M1b) · merchant đóng. Job đối chiếu đêm gửi lại toàn bộ.

| Sự kiện | Nơi đặc tả | Trạng thái |
|---|---|---|
| Liên kết mới (M1) | CN-06 Luồng 3 · Bước 20 | ✅ Sửa: gọi với **mọi** liên kết mới (trước đây chỉ khi là tài khoản nhận) |
| Kích hoạt gian hàng | CN-01 Luồng 7 · Bước 5 | Giữ nguyên — gọi thêm một lần lúc kích hoạt, an toàn vì là `PUT` trọn bộ |
| Đổi TK nhận (S4) | CN-07 Luồng 1 · Bước 9 | Đã có |
| Hết `grace` / thu hồi (M1b) | CN-07 Luồng 3 · Bước 6 | Đã có |
| Hủy liên kết (M1b) | CN-08 Luồng 1 · Bước 7 | ✅ **Bổ sung** |
| Merchant đóng | Chưa có SRS | ⏳ Ghi nhận khi viết SRS đóng gian hàng |

---

## C. Dùng nhưng chưa khai báo trong danh mục — ⏳ chờ BA

**Tham số (CFG-01):** `OTP_MAX_ATTEMPTS` · `OLD_LINK_GRACE` · `MAX_LENGTH_MSISDN` · `LENGTH_OTP`. CN-06 gọi `TOKEN_RENEW_BEFORE`, CFG-01 đặt tên `LINK_TOKEN_RENEW_BEFORE`.

**Mẫu tin (CFG-02):** `MS00007` `LINK_ADDED` · `MS00008` `RECV_CHANGED`. _(`MS00009` đã đăng ký 16/10 nên CFG-02 đang nhảy cóc 06 → 09 cho tới khi bổ sung 07, 08.)_ CN-06 dùng `MS00003` (mẫu `APP_STATUS` của hồ sơ) để báo liên kết thất bại, trong khi CFG-04 đã có `NOTI030002`. Biến `NOTI030001`: CN-06 dùng `{bank}`, CFG-04 dùng `{bank_name}`.

**Mã lỗi (CFG-03):**
- Mã thành công: `PIN-200-LINKADDED` · `PIN-200-RECVCHANGED` · `PIN-200-LINKREVOKED`
- Liên kết / đổi tài khoản nhận: `PIN-422-LINKLIMIT` · `PIN-409-ACCTAKEN` · `PIN-422-LINKNOTACTIVE` · `PIN-422-RECVSAME` · `PIN-409-CUTOVER` · `PIN-422-LINKPRIMARY`
- eKYC: CN-01 dùng `PIN-422-EKYCLOWSCORE` · `PIN-422-EKYCNOMATCH`; CFG-03 đặt `E1-422-LOWSCORE` · `E1-422-NOMATCH`
- CN-02 còn mã cũ `BIZ-PERSON-LOCKED` · `BIZ-PERSON-TERMINATED` · `BIZ-MERCHANT-STATE`
- Hành động lệch: `OB-422-KYC`, `OB-423-LOCK` — CFG-03 "dừng luồng, gọi 8686" vs mapping CN-01/CN-06 "inline error, cho nhập lại". `OB-429-OTPWAIT` hiện "cạnh nút Resend" nhưng NB-2D không có Resend
- Lỗi gửi SMS N1: CFG-02 / CN-02 mục 3.5 trả `PIN-503-DEP`, COMMON-01 trả `PIN-503-OTPSEND`

> Đã thêm sẵn `PIN-422-OTPLOCKED` vào CFG-03 vì quyết định A1 cần mã này.

**PL-02:** mới có trường `Amount`. Thiếu Phone Number · PIN · OTP · Account number mà mọi SRS trỏ tới.

**Khác:**
- QR: CN-01 ghi HTQR 1.0, CN-07 ghi EMVCo. Thực thể: CN-01 `standee`, CN-07 `standee_order` + `merchant_qr`
- CFG-01 `REFRESH_TOKEN_TTL` vẫn ghi "chưa có chức năng đăng xuất" (CN-04 đã có)

---

## D. Lỗi nội bộ từng tài liệu — ⏳ chờ BA

- **CN-01:** tham chiếu màn không tồn tại NB-2A9 · NB-2A11 · NB-2A13; Retake NB-2A8 trỏ về chính NB-2A8; số control NB-01 lệch (Continue tham chiếu (4)/(6) thay vì (3)/(5)); mã gian hàng lúc `Mxxxxxx` lúc `PIN-M-xxxxxx`; Luồng 6 Bước 9 ghi "Pending" thay vì `draft`; sơ đồ trạng thái ghi kích hoạt ở "Bước 15/17" (thực tế Bước 4); điểm vào 3 "NB-1C tự hiện" vs Luồng 8 "vào qua menu"; mapping `E1-400-VAL` / `E1-401-AUTH` / `E1-429-RATE` "chụp lại cả ba" trái với mục 4.1.2
- **CN-02:** NB-0D Back về NB-00 nhưng nhánh 4a ghi về NB-0C
- **CN-03:** thiếu bước gửi `MS00006` (CN-05 và CFG-02 yêu cầu); ràng buộc trỏ "PL-02 · STT 3" không tồn tại
- **CN-04:** số control NB-14 / NB-14A lệch, tham chiếu control (7) không tồn tại
- **CN-05:** mục 5 yêu cầu gỡ "control STT 7" của NB-02A và đổi mã `OUT-*` của CN-04 — cả hai đã không còn
- **CN-06:** "Liên kết lại" vừa ghi "là liên kết mới" vừa ghi "cập nhật cùng bản ghi"; Bước 20 nhắc "Bước 8 đặt `is_primary`" (đúng là Bước 19)
- **CN-07:** bảng tham số còn `LINK_SESSION_TTL`, `LINK_CONFIRM_RETRY_*` không dùng tới
- **CN-08:** Infobox ghi "3 trường hợp" nhưng chỉ có 2; ẩn Remove khi `is_agent_session` chưa có trong CN-06

---

## E. Điểm còn mở cần BA chốt

1. ~~CN-05 — màn NB-14B~~ → **Đã chốt 16/10:** giữ như hiện tại, kiểm PIN riêng trước khi nhập PIN mới. Ghi là ngoại lệ ở CN-05 (Mục đích) và COMMON-01 (Luồng 1 · Bước 4, mục 5).
2. **N4 / CR-STATUS-01** — chốt Q1, Q2, Q3 rồi duyệt CR.
3. **Nhóm C, D** ở trên.
4. ~~Đăng ký mã mới phát sinh~~ → **Đã thêm 16/10:** `LINK_MAX_PER_PERSON` vào CFG-01 §1.7 _(mặc định **5** là đề xuất — cần chốt)_ · `MS00009` · `LINK_REMOVED` vào CFG-02 · `PIN-422-LINKGRACE` vào CFG-03 §2.5. CN-08 đã bỏ đánh dấu (*).
