![](http://10.254.136.32:8090/plugins/servlet/confluence/placeholder/macro?definition=e3RvY30&locale=en_US&version=2)

**Bảng ghi nhận thay đổi tài liệu**

A – Tạo mới, M – Sửa đổi, D – Xóa bỏ

|   |   |   |   |   |   |
|---|---|---|---|---|---|
|Ngày thay đổi|Vị trí thay đổi|A, M, D|Nguồn gốc|Mô tả thay đổi|Phiên bản|
|07/09/2026|Toàn bộ|A|BRD 1.0 · PRD 5.0 · TSD v4.6 · API Spec v3.7 · DataDict v4.4 · Wireframes 20/08 · AuthOB v3.7|Tạo mới tài liệu|1.0|

---

# 1. Mô tả chung

|   |   |
|---|---|
|**Mục đích**|Cho phép người dùng đã có tài khoản mở app Peye-Haiti và vào được các chức năng nghiệp vụ **mà không phải nhập PIN thường xuyên**.  <br>  <br>Cơ chế: khởi động app **chỉ kiểm tra tại máy** — refresh token còn trong `REFRESH_TOKEN_TTL`, và `auth_time` còn trong `PIN_REAUTH_INTERVAL`. Còn hạn cả hai thì vào thẳng Trang chủ, **không gọi server**, nên mở được app cả khi mất mạng.  <br>  <br>Trước khi hiện màn nhập PIN, hệ thống kiểm tra số điện thoại có tài khoản và trạng thái tài khoản hợp lệ (MSISDN precheck).  <br>  <br>Phạm vi: khởi động app · chọn ngôn ngữ lần đầu · kiểm tra số điện thoại · xác thực PIN · gia hạn phiên ngầm · xác thực lại định kỳ · xác thực thiết bị mới bằng OTP.|
|**Loại chức năng**|**Mobile app** _(React Native — Android/iOS, chạy được trên mạng 2G)_|
|**Đối tượng sử dụng**|- Người mua — vai MUA, `kyc_level = 1`  <br>- Người bán / tiểu thương — vai BÁN, `kyc_level = 2`  <br>- Nhân viên hiện trường Natcom — phiên gắn cờ `is_agent_session`|
|**Kênh áp dụng**|App Peye-Haiti _(một app dùng chung cho cả người mua và người bán)_.  <br>Ngôn ngữ giao diện: Creole `ht` **(mặc định)** · French `fr` · English `en`|
|**Đường dẫn chức năng**|Mở app _(không có điểm vào nào khác — chức năng chạy ngay khi khởi động)_|
|**Precondition**|1. Người dùng đã có `person` với `msisdn` và `pin_hash` — đã hoàn tất CN-01 tới bước đặt PIN.  <br>2. `person.status = Active`.  <br>3. Chưa vượt `OTP_MAX_PER_DAY` cho `purpose = login_new_device`.  <br>4. **Khởi động app (Luồng 1) không cần mạng.** Mọi luồng còn lại — MSISDN precheck, xác thực PIN, OTP, gia hạn phiên — đều yêu cầu kết nối tới BFF; **không** có nhánh xác thực PIN offline.  <br>  <br>_Lưu ý: `person` đang bị **khóa đăng nhập** do sai PIN vẫn thỏa Precondition — người dùng phải vào được NB-00 để thấy đồng hồ đếm ngược và đường đặt lại PIN._|
|**Post-condition**|**Khởi động với phiên còn dùng được:** app mở Trang chủ, không gọi server, không hỏi PIN; token trên máy giữ nguyên.  <br>  <br>**Gia hạn phiên ngầm thành công:** app có access token mới **mang nguyên `auth_time` cũ**.  <br>  <br>**Đăng nhập mới thành công:** ghi phiên mới gắn `device_id` + băm refresh token; app nhận cặp token; **xóa `login_lock`** của `person`; ghi số điện thoại vào Secure Storage trên máy; cập nhật `person.lang` theo ngôn ngữ app đang dùng.  <br>  <br>**Xác thực lại thành công:** `auth_time` và `last_auth_at` đặt về hiện tại; **không** tạo phiên mới, **không** xoay refresh token.  <br>  <br>**Bị khóa đăng nhập do sai PIN:** tạo `login_lock` với `locked_until`; gửi SMS `MS00002` cho chủ số; **`person.status` vẫn là `Active`**; **các phiên đang hoạt động không bị thu hồi**; người dùng vẫn vào được luồng đặt lại PIN của `SRS-CN03`.  <br>  <br>**Mất mạng giữa lúc đang dùng app:** **giữ nguyên token**, app chuyển chế độ ngoại tuyến — không bị đẩy về màn PIN.|
|**Ràng buộc**|- PIN app **tách biệt hoàn toàn** PIN ví/ngân hàng — hệ thống không bao giờ hỏi hoặc lưu PIN ví/bank.<br>- PIN băm phía server; **không bao giờ** lưu PIN rõ.<br>- Sai PIN đủ `PIN_MAX_ATTEMPTS` lần → khóa đăng nhập trong `PIN_LOCK_DURATION`, đếm theo `person`. Khóa đăng nhập **không** làm đổi `person.status`.<br>- Số điện thoại là dữ liệu PII — lưu trên thiết bị phải mã hóa qua Keychain/Keystore, không ghi log rõ, hiển thị bản che 4 số cuối.<br>- App **không hiện mã lỗi kỹ thuật** cho người dùng — chỉ hiện thông báo đã bản địa hóa kèm việc cần làm tiếp.<br>- **Server chốt mọi quyết định về chu kỳ xác thực lại.** App chỉ đọc `auth_time` trong token đã lưu để định tuyến sớm khi khởi động, **không** dùng đồng hồ máy làm lớp bảo vệ.<br>- **Khởi động app không được gọi server.** Gia hạn phiên ngầm chạy lazy: nền sau khi app đã mở, và khi API nghiệp vụ trả token hết hạn.<br>- **App không bao giờ xóa token vì lý do không gọi được server** — chỉ xóa khi server từ chối rõ ràng.<br>- Quy định chung về control: `PL-01`. Định dạng từng trường input: `PL-02`. Giá trị tham số: `CFG-01`. Nội dung SMS: `CFG-02`.<br>- Ngoài phạm vi: **quên PIN & đặt lại PIN** (`SRS-CN03`)|

**  
Bảng thuật ngữ**

|   |   |
|---|---|
|Thuật ngữ|Nghĩa trong tài liệu này|
|**access token**|Mã dùng để xác thực và cấp quyền cho mỗi lời gọi API, không phải gửi lại PIN. Hiệu lực `ACCESS_TOKEN_TTL`|
|**refresh token**|Chuỗi cấp cùng access token, dùng xin cấp lại access token mới. Hiệu lực `REFRESH_TOKEN_TTL`|
|**gia hạn phiên ngầm** _(silent refresh)_|App tự gọi API gia hạn bằng refresh token, không hỏi người dùng. **Không** làm mới `auth_time`|
|**auth_time**|Mốc người dùng nhập PIN hoặc OTP thành công **lần cuối** (chuẩn OIDC). Lưu song song ở `auth_session.last_auth_at`|
|**amr**|Đã xác thực bằng cách gì (chuẩn OIDC): `["pin"]` hoặc `["pin","otp"]`|
|**chu kỳ xác thực lại** _(re-authentication interval)_|Khoảng thời gian tối đa kể từ `auth_time` mà sau đó hệ thống bắt xác thực lại. Giá trị `PIN_REAUTH_INTERVAL`|
|**xác thực lại** _(re-authentication)_|Bắt nhập lại PIN khi hết chu kỳ trên, trong lúc phiên vẫn còn|
|**step-up token** (`verify_token`)|Mã xác thực một lần cấp sau khi xác thực nâng cấp thành công|
|**MSISDN precheck**|Bước kiểm tra số điện thoại có `person` và trạng thái hợp lệ, **trước khi** hiện màn nhập PIN|
|**login_lock**|Trạng thái khóa đăng nhập do sai PIN. Tách khỏi `person.status`|
|**chế độ ngoại tuyến**|Trạng thái app khi không gọi được BFF: giữ nguyên token, chỉ cho đọc/ghi dữ liệu cục bộ và sinh QR tại máy|

**Bảng tham chiếu tham số & quy định dùng chung**

|STT|Mã / Tham số|Tài liệu nguồn|
|---|---|---|
|**A**|**Tham số hệ thống**||
|1|`ACCESS_TOKEN_TTL`|CFG-01|
|2|`REFRESH_TOKEN_TTL`|CFG-01|
|3|`PIN_REAUTH_INTERVAL`|CFG-01|
|4|`STEPUP_TTL`|CFG-01|
|5|`PIN_MAX_ATTEMPTS`|CFG-01|
|6|`PIN_LOCK_DURATION`|CFG-01|
|7|`OTP_TTL`|CFG-01|
|8|`OTP_MAX_PER_DAY`|CFG-01|
|9|`FORMAT_MSISDN`|CFG-01|
|10|`OTP_RESEND_AFTER`|—|
|**B**|**Mẫu SMS**||
|11|`MS00001` · `OTP_GENERIC`|CFG-02|
|12|`MS00002` · `EMERGENCY_LOCK`|CFG-02|
|**D**|**Quy định control & input**||
|13|Phone Number|PL-02|
|14|PIN|PL-02|
|15|OTP|PL-02|
|16|Thời gian hiệu lực OTP|PL-02|
|17|`Label` · `Button` · `Hyperlink` · `Infobox` · `Inlineerror` · `Pin input` · `Otp input` · `Countdown timer` · `Account card` · `Radio card` · `Single line of text`|PL-01|

---

# 2. Màn hình

## 2.1. Mô phỏng màn hình

|   |   |   |   |   |
|---|---|---|---|---|
|### NB-0A — App launch|### NB-0B — Choose your language|### NB-0C — Enter your phone number|### NB-0C — Enter your phone number<br><br>- error|NB-0D — Verify device|
|![](http://10.254.136.32:8090/download/attachments/105325946/01_NB-0A_Startup.png?version=1&modificationDate=1788947632668&api=v2 "Kinh doanh quốc tế > CN-02 · Đăng nhập bằng mã PIN > 01_NB-0A_Startup.png")|![](http://10.254.136.32:8090/download/attachments/105325946/02_NB-0B_Select_language.png?version=1&modificationDate=1788947652894&api=v2 "Kinh doanh quốc tế > CN-02 · Đăng nhập bằng mã PIN > 02_NB-0B_Select_language.png")|### ![](http://10.254.136.32:8090/download/attachments/105325946/03_NB-0C_Phone_number_1-2.png?version=1&modificationDate=1788947670097&api=v2 "Kinh doanh quốc tế > CN-02 · Đăng nhập bằng mã PIN > 03_NB-0C_Phone_number_1-2.png")|![](http://10.254.136.32:8090/download/attachments/105325946/10_NB-0C_Phone_number_1-2_copy.png?version=1&modificationDate=1788947701981&api=v2 "Kinh doanh quốc tế > CN-02 · Đăng nhập bằng mã PIN > 10_NB-0C_Phone_number_1-2_copy.png")|![](http://10.254.136.32:8090/download/attachments/105325946/NB-02%20confirm.png?version=1&modificationDate=1789544874559&api=v2 "Kinh doanh quốc tế > CN-02 · Đăng nhập bằng mã PIN > NB-02 confirm.png")|
|### NB-00 — Enter PIN|### NB-00 — Enter PIN<br><br>- wrong PIN|### NB-00 — Enter PIN<br><br>- Khóa đăng nhập|### NB-00 — Enter PIN<br><br>- phiên hết hạn|### NB-00 — Enter PIN<br><br>- xác thực lại|
|![](http://10.254.136.32:8090/download/attachments/105325946/04_NB-00_Enter_PIN_2-2.png?version=1&modificationDate=1788947749621&api=v2 "Kinh doanh quốc tế > CN-02 · Đăng nhập bằng mã PIN > 04_NB-00_Enter_PIN_2-2.png")|![](http://10.254.136.32:8090/download/attachments/105325946/05_NB-00_Wrong_PIN.png?version=1&modificationDate=1788947766534&api=v2 "Kinh doanh quốc tế > CN-02 · Đăng nhập bằng mã PIN > 05_NB-00_Wrong_PIN.png")|![](http://10.254.136.32:8090/download/attachments/105325946/06_NB-00_Locked_60_min.png?version=1&modificationDate=1788947791808&api=v2 "Kinh doanh quốc tế > CN-02 · Đăng nhập bằng mã PIN > 06_NB-00_Locked_60_min.png")|![](http://10.254.136.32:8090/download/attachments/105325946/07_NB-00_Session_expired.png?version=1&modificationDate=1788947856289&api=v2 "Kinh doanh quốc tế > CN-02 · Đăng nhập bằng mã PIN > 07_NB-00_Session_expired.png")|![](http://10.254.136.32:8090/download/attachments/105325946/11_NB-00_-_x%C3%A1c_th%E1%BB%B1c_l%E1%BA%A1i.png?version=1&modificationDate=1788947904575&api=v2 "Kinh doanh quốc tế > CN-02 · Đăng nhập bằng mã PIN > 11_NB-00_-_xác_thực_lại.png")|

## 2.2. Các yếu tố trên màn hình

### 2.2.1. NB-0A — App launch

Màn này **không có control nào**. Không gọi API, không kiểm tra kết nối mạng, không gia hạn phiên. Người dùng không thao tác gì.

### 2.2.2. NB-0B — Choose your language

|   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|
|**STT**|**Tên control**|**Loại control**|**Require**|**Maxlength**|**Giá trị mặc định**|**Mô tả**|
|1|Choose your language|`Label`|Không|–|–|Tiêu đề màn|
|2|Language list|`Radiocard`|**Có**|–|`Creole`|Ba thẻ: <br><br>- `Creole` <br>- `French`<br>- `English`|
|3|Continue|`Button` _(chính)_|Không|–|Enabled|Ghi ngôn ngữ đã chọn và cờ `first_run_done` vào Secure Storage trên máy. **Không gọi API**|

**Ghi chú:** màn chỉ hiện **đúng một lần**, ở lần mở app đầu tiên sau khi cài đặt; gỡ app và cài lại thì hiện lại. NB-0B đứng **trước** NB-01 của CN-01, nên trường ngôn ngữ ở bước đăng ký phải lấy giá trị từ đây.

### 2.2.3. NB-0C — Enter your phone number

|   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|
|**STT**|**Tên control**|**Loại control**|**Require**|**Maxlength**|**Giá trị mặc định**|**Mô tả**|
|1|Sign in|`Label`|Không|–|–|Tiêu đề thanh điều hướng|
|2|Enter your phone number|`Label`|Không|–|–|Tiêu đề màn|
|3|+509|`Label`|Không|–|`+509`|Mã quốc gia, cố định ở pilot, không cho sửa|
|4|Phone number|`Singlelineoftext`|**Có**|`MAX_LENGTH_MSISDN`|Trống|Trường **Phone Number** — xem `PL-02` <br><br>Kiểm định dạng **tại máy** theo `FORMAT_MSISDN`; đạt định dạng thì bật control "Continue"|
|5|Phone number error|`Inlineerror`|Không|–|Ẩn|Nội dung theo kết quả validate định dạng/precheck|
|6|Continue|`Button` _(chính)_|Không|–|Disabled|Bật khi đạt định dạng. Gọi **MSISDN precheck** — **không** chuyển màn ngay, chờ kết quả|
|7|No account yet? Sign up|`Button`|Không|–|Enabled|Chọn sẽ mang theo số đã nhập sang màn NB-01 (luồng CN-01)|
|8|Lost your phone? Call hotline 8686 to LOCK your account.|`Infobox`|Không|–|–|Nhắc khóa khẩn, hiện ở chân màn|

**Ghi chú:** màn hiện khi trên máy **không có** số điện thoại đăng nhập thành công gần nhất — cài mới, gỡ cài lại, bấm _Change phone number_ ở NB-00, hoặc thiết bị dùng chung của nhân viên hiện trường.

### 2.2.4. NB-00 — Enter PIN

|   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|
|**STT**|**Tên control**|**Loại control**|**Require**|**Maxlength**|**Giá trị mặc định**|**Mô tả**|
|1|Back|`Button` _(điều hướng)_|Không|–|Ẩn|**Chỉ hiện khi vào từ NB-0C.** Quay lại NB-0C giữ nguyên số đã nhập|
|2|Enter PIN|`Label`|Không|–|–|Tiêu đề thanh điều hướng|
|3|Session expired banner|`Infobox`|Không|–|Ẩn|Chỉ hiện khi vào do **phiên hết hạn hoặc bị thu hồi** _(Luồng 5 · B12)_. Nội dung refer `PIN-401-SESSION`|
|4|Routine check banner|`Infobox`|Không|–|Ẩn|Chỉ hiện khi vào do **hết chu kỳ xác thực lại**: Nội dung refer `PIN-401-REAUTH`|
|5|Sign-in locked banner|`Infobox` _(đỏ)_|Không|–|Ẩn|Chỉ hiện ở trạng thái khóa đăng nhập, nội dung refer `PIN-422-PINLOCKED`, `{countdown}` tính từ `details.locked_until`|
|6|Account card|`Accountcard`|Không|–|–|Số điện thoại **bản che** 4 số cuối; dòng phụ là tên person do precheck trả về, hoặc trống nếu chưa có|
|7|Change|`Hyperlink`|Không|–|Enabled|Thay đổi số điện thoại đăng nhập → Hiện NB-0C với ô số điện thoại để trống và nút Back bật|
|8|Enter your PIN|`Label`|Không|–|–|Dòng nhắc trên ô nhập. Số ký tự lấy theo|
|9|PIN input|`Pininput`|**Có**|6|Trống|Trường **PIN** — xem `PL-02.` Nhập đủ ký tự thì **tự gửi**, không cần nút xác nhận. Ẩn ở trạng thái khóa đăng nhập|
|10|PIN error|`Inlineerror`|Không|–|Ẩn|Hiện sau mỗi lần sai PIN, Nội dung = thông điệp `PIN-401-PINWRONG`, `N` lấy từ `details.tries_left`|
|11|Try again in|`Countdowntimer`|Không|–|Ẩn|Chỉ hiện ở trạng thái khóa; đếm tới `details.locked_until`; hết giờ tự bật lại control (9)|
|12|Forgot PIN? Verify by OTP|`Hyperlink`|Không|–|Enabled|Chuyển sang luồng của `SRS-CN03`. **Vẫn bật khi đang bị khóa đăng nhập**|
|13|Reset PIN|`Button` _(chính)_|Không|–|Ẩn|**Chỉ hiện ở trạng thái khóa đăng nhập.** Cùng đích với control (12), chỉ khác dạng hiển thị|
|15|Lost your phone? Call hotline 8686 to LOCK your account.|`Label`|Không|–|–|Nhắc khóa khẩn, luôn hiện ở chân màn|

**Ghi chú:**

- NB-00 xuất hiện trong **3 trường hợp**: ① không có refresh token còn hạn trên máy; ② phiên hết hạn hoặc bị thu hồi giữa lúc đang dùng app; ③ phiên vẫn còn nhưng hết chu kỳ xác thực lại.
- **Phân biệt ② và ③ là điểm dễ làm sai nhất.** Hai trường hợp dùng hai banner khác nhau — control (3) và (4) — và app gọi **hai endpoint khác nhau**: ② nhập PIN **tạo phiên mới**; ③ nhập PIN chỉ **cập nhật `last_auth_at`**, không tạo phiên mới, không xoay refresh token.
- Ba banner (3), (4), (5) **loại trừ nhau** — không bao giờ hiện quá một cái cùng lúc.
- Màn này **luôn đi sau MSISDN precheck** — không có đường nào vào NB-00 mà chưa biết `person` tồn tại và `person.status = Active`.

### 2.2.5. NB-0D — Verify device

|   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|
|**STT**|**Tên control**|**Loại control**|**Require**|**Maxlength**|**Giá trị mặc định**|**Mô tả**|
|1|Back|`Button` _(điều hướng)_|Không|–|Enabled|**Luôn hiện.** Bấm Back **hủy mã OTP đang chờ** và quay lại NB-00; phải nhập PIN lại từ đầu|
|2|Enter the code just sent to|`Label`|Không|–|–|Tiêu đề màn + dòng phụ hiện **số điện thoại đầy đủ vừa nhập** _(người dùng cần thấy để phát hiện gõ sai số)_|
|3|OTP input|`Pininput`|**Có**|`6`|Trống|Trường **OTP** — xem `PL-02`. Nhập đủ ký tự thì **tự gửi**|
|4|Did not get the code? Resend code (mm:ss)|`Hyperlink`|Không|–|Disabled|<mm:ss> đồng hồ đếm ngược từ `OTP_RESEND_AFTER`; sau đó enable "Resend code", ẩn bộ đếm ngược  <br>**enable ngay nếu mã vừa bị hủy do nhập sai**.<br><br>Tổng số lần gửi ≤ `OTP_MAX_PER_DAY`|
|5|OTP error|`Inlineerror`|Không|–|Ẩn|Hiển thị nỗi dung lỗi khi nhập sai OTP/OTP hết hạn. Đồng thời: xóa ô nhập (3), dừng đồng hồ và bật control (4)|

**Ghi chú:** `verify_token` cấp ở màn này hiệu lực `STEPUP_TTL` và **dùng đúng một lần**. OTP tại đây là OTP của **nền tảng** (qua Natcom N1), không phải OTP của định chế.

# 3. Luồng nghiệp vụ

## 3.1. Activity diagram

### 3.1.1. Luồng 1 — Khởi động ứng dụng & định tuyến (NB-0A · NB-0B)

|   |
|---|
|@startuml<br>skinparam backgroundColor #FFFFFF<br>skinparam ActivityBorderColor #4A90E2<br>skinparam ActivityBackgroundColor #FFFFFF<br>skinparam ActivityDiamondBackgroundColor #FFF2CC<br>skinparam ArrowColor #333333<br>skinparam ActivityFontSize 12<br>skinparam swimlaneWidth same<br><br>\|#F5F5F5\|Người dùng\|<br>start<br>:[Bước 1] Cham bieu tuong de mo ung dung;<br>\|#DAE8FC\|App Peye-Haiti\|<br>:[Bước 2] Hien NB-0A va doc du lieu da luu tren may;<br>if ([Bước 3] Lan dau mo app sau khi cai dat?) then (Co)<br>\|#F5F5F5\|Người dùng\|<br>:[Bước 4] Chon ngon ngu tai NB-0B - mac dinh Creole;<br>\|#DAE8FC\|App Peye-Haiti\|<br>endif<br>if ([Bước 5] Co refresh token va con trong REFRESH_TOKEN_TTL? Kiem tai may) then (Co)<br>if ([Bước 6] Con trong PIN_REAUTH_INTERVAL tinh tu auth_time? Kiem tai may) then (Co)<br>#D5E8D4:[Bước 7] Mo NB-03 Trang chu - KHONG goi mang, KHONG hoi PIN. Ket thuc;<br>stop<br>else (Khong)<br>#FFF2CC:[Bước 8] Dat ngu canh xac thuc lai - sang Luong 2. Ket thuc;<br>stop<br>endif<br>endif<br>#FFF2CC:[Bước 9] Khong dung duoc phien nao - dang nhap moi - sang Luong 2. Ket thuc;<br>stop<br>@enduml|

### 3.1.2. Luồng 2 — Precheck kiểm tra số điện thoại trước màn PIN (NB-0C)

|   |
|---|
|@startuml<br>skinparam backgroundColor #FFFFFF<br>skinparam ActivityBorderColor #4A90E2<br>skinparam ActivityBackgroundColor #FFFFFF<br>skinparam ActivityDiamondBackgroundColor #FFF2CC<br>skinparam ArrowColor #333333<br>skinparam ActivityFontSize 12<br>skinparam swimlaneWidth same<br><br>\|#DAE8FC\|App Peye-Haiti\|<br>start<br>if ([Bước 1] Co so dien thoai da ghi nho tren may?) then (Khong)<br>\|#F5F5F5\|Người dùng\|<br>:[Bước 2] Nhap so dien thoai tai NB-0C - app kiem FORMAT_MSISDN tai may;<br>\|#DAE8FC\|App Peye-Haiti\|<br>endif<br>:[Bước 3] Goi MSISDN precheck voi msisdn va device_id;<br>\|#D5E8D4\|Merchant Identity Service\|<br>if ([Bước 4] Co person gan voi so dien thoai nay?) then (Khong)<br>#FFCCCC:[Bước 5] Tra PIN-404-PERSON - app moi dang ky. Ket thuc;<br>stop<br>endif<br>if ([Bước 6] person.status?) then (Locked)<br>#FFCCCC:[Bước 7] Tra PIN-422-ACCLOCKED - huong dan goi hotline 8686. Ket thuc;<br>stop<br>elseif (Terminated)<br>#FFCCCC:[Bước 8] Tra PIN-422-ACCCLOSED - huong dan dang ky moi. Ket thuc;<br>stop<br>else (Active)<br>endif<br>if ([Bước 9] person dang co login_lock con hieu luc?) then (Co)<br>#FFF2CC:[Bước 10] Tra PIN-422-PINLOCKED kem locked_until - app mo NB-00 trang thai khoa - KHONG gui OTP. Ket thuc;<br>stop<br>endif<br>:[Bước 11] Tra msisdn, ten person va co device_known;<br>\|#DAE8FC\|App Peye-Haiti\|<br>if ([Bước 12] device_known?) then (Chua biet)<br>#FFF2CC:Mo NB-0D - sang Luong 4 de xac thuc OTP TRUOC;<br>stop<br>else (Da biet)<br>#D5E8D4:Mo NB-00 - sang Luong 3 de nhap PIN;<br>stop<br>endif<br>@enduml|

### 3.1.3. Luồng 3 — Xác thực mã PIN (NB-00)

|   |
|---|
|@startuml<br>skinparam backgroundColor #FFFFFF<br>skinparam sequenceArrowColor #333333<br>skinparam ParticipantFontSize 12<br><br>actor "Người dùng" as USR<br>participant "App Peye-Haiti" as APP #White<br>participant "Merchant Identity Service" as MIS #DAE8FC<br><br>USR -> APP : [Bước 1] Nhap ma PIN du so ky tu tai NB-00<br>APP -> MIS : [Bước 2] Gui msisdn, PIN, device_id va verify_token neu vua qua NB-0D<br>alt Dang bi khoa dang nhap<br>  MIS --> APP : [Bước 3] PIN-422-PINLOCKED kem details.locked_until<br>  APP -> USR : Nhanh 3a - NB-00 trang thai khoa, dong ho Try again in<br>else Khong bi khoa<br>  MIS -> MIS : [Bước 4] So khop PIN voi person.pin_hash<br>  alt PIN sai<br>    MIS -> MIS : [Bước 5] Tang so lan sai cua person<br>    alt Da du PIN_MAX_ATTEMPTS lan<br>      MIS -> MIS : [Bước 6] Tao login_lock voi locked_until - person.status giu nguyen Active<br>      MIS -> MIS : [Bước 7] Goi di - gui SMS canh bao khoa dang nhap<br>      note right of MIS<br>Goi Notification Service de gui SMS qua Natcom N1 (nhom D.5)<br>Mau tin MS00002, tham so minutes<br>Gui that bai KHONG lam that bai viec khoa<br>      end note<br>      MIS --> APP : PIN-422-PINLOCKED kem details.locked_until<br>    else Con luot<br>      MIS --> APP : [Bước 8] PIN-401-PINWRONG kem details.tries_left - KHONG tieu verify_token<br>      APP -> USR : Hien PIN error, cho nhap lai ngay tai NB-00<br>    end<br>  else PIN dung<br>    MIS -> MIS : [Bước 9] Kiem tra thiet bi va verify_token<br>    alt Thiet bi moi, khong kem verify_token<br>      MIS --> APP : PIN-401-NEWDEVICE<br>      APP -> USR : Mo NB-0D - sang Luong 4<br>    else Thiet bi moi, verify_token sai hoac het STEPUP_TTL hoac da dung<br>      MIS --> APP : PIN-401-STEPUP<br>      APP -> USR : Mo lai NB-0D - sang Luong 4<br>    else Thiet bi da biet hoac verify_token hop le<br>      MIS -> MIS : [Bước 10] Mo phien moi, ghi nhan thiet bi, tieu verify_token, xoa login_lock<br>      MIS --> APP : [Bước 11] Tra cap token kem person va merchant<br>      APP -> USR : [Bước 12] Dieu huong vao NB-03 Trang chu<br>    end<br>  end<br>end<br>@enduml|

### 3.1.4. Luồng 4 — Xác thực thiết bị mới bằng OTP (NB-0D)

|   |
|---|
|@startuml<br>skinparam backgroundColor #FFFFFF<br>skinparam sequenceArrowColor #333333<br>skinparam ParticipantFontSize 12<br><br>actor "Người dùng" as USR<br>participant "App Peye-Haiti" as APP #White<br>participant "Merchant Identity Service" as MIS #DAE8FC<br><br>note over APP : Vao tu Luong 2 Buoc 12 khi device_known = false<br>APP -> MIS : [Bước 1] Yeu cau gui OTP voi purpose login_new_device<br>alt Vuot OTP_MAX_PER_DAY<br>  MIS --> APP : PIN-422-OTPLIMIT - sang nhanh 1a<br>else Trong han muc<br>  MIS -> MIS : [Bước 2] Goi di - gui SMS chua ma OTP<br>  note right of MIS<br>Goi Notification Service de gui SMS qua Natcom N1 (nhom D.5)<br>Mau tin MS00001, tham so otp va ttl_min<br>Loi gui tin tra PIN-503-OTPSEND, so khong nhan duoc SMS tra PIN-422-SMSUNREACH<br>  end note<br>  MIS --> USR : Tin SMS chua ma OTP hieu luc OTP_TTL<br>  USR -> APP : [Bước 3] Nhap ma OTP tai NB-0D<br>  APP -> MIS : [Bước 4] Gui ma OTP va ma tham chieu<br>  alt OTP dung va con hieu luc<br>    MIS --> APP : [Bước 6] Cap verify_token hieu luc STEPUP_TTL - CHUA tieu<br>    APP -> USR : [Bước 7] Mo NB-00 banner Device verified - sang Luong 3 de nhap PIN<br>  else OTP sai<br>    MIS --> APP : [Bước 5] PIN-422-OTPWRONG - ma bi huy ngay - sang nhanh 5a<br>  else Qua OTP_TTL<br>    MIS --> APP : [Bước 5] PIN-422-OTPEXPIRED - sang nhanh 5a<br>  else Ma tham chieu khong ton tai<br>    MIS --> APP : [Bước 5] PIN-404-OTP - sang nhanh 5a<br>  end<br>end<br>@enduml|

### 3.1.5. Luồng 5 — Phiên hết hạn hoặc cần xác thực lại giữa lúc đang dùng app

|   |
|---|
|@startuml<br>skinparam backgroundColor #FFFFFF<br>skinparam ActivityBorderColor #4A90E2<br>skinparam ActivityBackgroundColor #FFFFFF<br>skinparam ActivityDiamondBackgroundColor #FFF2CC<br>skinparam ArrowColor #333333<br>skinparam ActivityFontSize 12<br>skinparam swimlaneWidth same<br><br>\|#F5F5F5\|Người dùng\|<br>start<br>:[Bước 1] Vao mot chuc nang can goi API nghiep vu;<br>\|#DAE8FC\|App Peye-Haiti\|<br>:[Bước 2] Gui yeu cau kem access token va device_id;<br>\|#D5E8D4\|Merchant Identity Service\|<br>if ([Bước 3] Access token con hieu luc va con trong PIN_REAUTH_INTERVAL?) then (Co)<br>#D5E8D4:[Bước 4] Tra ket qua nghiep vu - nguoi dung dung binh thuong. Ket thuc;<br>stop<br>elseif (Con hieu luc nhung qua PIN_REAUTH_INTERVAL)<br>#FFF2CC:Nhanh 3a - Tra PIN-401-REAUTH - app di thang toi NB-00 banner Routine check. Ket thuc;<br>stop<br>else (Het han ACCESS_TOKEN_TTL)<br>endif<br>:[Bước 5] Tra PIN-401-EXPIRED;<br>\|#DAE8FC\|App Peye-Haiti\|<br>:[Bước 6] Tu dong gia han phien ngam bang refresh token - khong hoi nguoi dung;<br>if ([Bước 7] Co nhan duoc phan hoi tu server khong?) then (Khong goi duoc)<br>#FFF2CC:[Bước 8] GIU NGUYEN token - chuyen che do ngoai tuyen - lui lich thu lai. Ket thuc;<br>stop<br>endif<br>\|#D5E8D4\|Merchant Identity Service\|<br>if ([Bước 9] Refresh token con hieu luc va chua bi thu hoi?) then (Co)<br>\|#DAE8FC\|App Peye-Haiti\|<br>#D5E8D4:[Bước 10] Nhan access token moi - goi lai API nghiep vu - nguoi dung khong thay gian doan. Ket thuc;<br>stop<br>else (Server tu choi ro rang - PIN-401-SESSION)<br>\|#DAE8FC\|App Peye-Haiti\|<br>:[Bước 11] Xoa access token va refresh token khoi bo nho va khoi may;<br>#FFCCCC:[Bước 12] Dat ngu canh dang nhap moi - sang Luong 2 - NB-00 banner Session expired;<br>stop<br>endif<br>@enduml|

## 3.2. Mô tả luồng nghiệp vụ

### 3.2.1. Luồng 1 — Khởi động ứng dụng & định tuyến

|   |   |   |   |   |
|---|---|---|---|---|
|Bước|Đối tượng|Mô tả|Ghi chú|Bảng/Thực thể liên quan|
|—||**Luồng dữ liệu chính**|||
|1|**Người dùng**|**Mở ứng dụng**  <br>Chạm biểu tượng app|–|–|
|2|**App Peye-Haiti**|**Hiện màn khởi động và đọc dữ liệu trên máy**  <br>NB-0A hiển thị. Đọc từ máy:<br><br>- cờ `first_run_done`, ngôn ngữ đã chọn<br>- số điện thoại đăng nhập thành công gần nhất<br>- refresh token, mốc `auth_time`|**Không kiểm tra kết nối mạng ở bước này.** Số điện thoại và refresh token là dữ liệu PII — lưu mã hóa qua Keychain/Keystore, không ghi log rõ|–|
|3|**App Peye-Haiti**|**Kiểm tra lần mở đầu tiên**  <br>• Không có cờ `first_run_done` → **sang Bước 4**  <br>• Đã có cờ → dùng ngôn ngữ đã lưu, **sang Bước 5**|–|–|
|4|**Người dùng**|**Chọn ngôn ngữ lần đầu**  <br>NB-0B: chọn Creole_(mặc định)_ / French/ English.<br><br>App ghi ngôn ngữ và cờ `first_run_done` lên máy|–|–|
|5|**App Peye-Haiti**|**Kiểm tra refresh token**  <br>• Có refresh token và còn trong hạn `REFRESH_TOKEN_TTL` → **sang Bước 6**  <br>• Không có, hoặc đã quá hạn → **sang Bước 9**|Hạn tính theo mốc lưu cùng token trên máy, **không cần gọi server**. Tham số: xem `CFG-01`|–|
|6|**App Peye-Haiti**|**Kiểm tra chu kỳ xác thực lại**  <br>• `now − auth_time` ≤ `PIN_REAUTH_INTERVAL` → **sang Bước 7**  <br>• Vượt hạn → **sang Bước 8**|Cũng không cần gọi server|–|
|7|**App Peye-Haiti**|**Vào Trang chủ**  <br>Mở NB-03, **không gọi mạng, không hỏi PIN**. **Kết thúc**|Kho dữ liệu cục bộ đọc được ngay vì khóa nằm trong Keychain/Keystore, không cần PIN|`person` · `merchant`|
|8|**App Peye-Haiti**|**Mở màn xác thực lại**  <br>Đặt ngữ cảnh **xác thực lại**, **sang Luồng 2**. NB-00 chỉ mở **sau** precheck _(Luồng 2 · B12)_, với banner **Routine check**|**Không** xóa refresh token, **không** xóa số điện thoại đã ghi nhớ.  <br>Mất mạng ở đây là **không vào được app** — điểm chặn có chủ đích, xem nhánh 3b của Luồng 2|`auth_session`|
|9|**App Peye-Haiti**|**Không dùng được phiên nào**  <br>Đăng nhập mới**, Sang Luồng 2** để lấy `msisdn` và kiểm tra số điện thoại|Khác Bước 8: đây là **mất phiên**, nhập PIN đúng sẽ **tạo phiên mới**|–|
|—||**Luồng dữ liệu rẽ nhánh**|||
|7a|**App Peye-Haiti**|**Gia hạn phiên ngầm chạy nền**  <br>Sau khi vào Trang chủ, app gọi gia hạn phiên ở chế độ nền.<br><br>Thành công thì thay token mới; thất bại thì **không hiện gì cho người dùng** và **không đẩy ra màn PIN**|Nếu để lỗi nền đẩy người dùng ra NB-00 thì mất hoàn toàn tác dụng của việc "khởi động không gọi server".|`auth_session`|

### 3.2.2. Luồng 2 — Kiểm tra số điện thoại trước màn PIN

|   |   |   |   |   |
|---|---|---|---|---|
|Bước|Đối tượng|Mô tả|Ghi chú|Bảng/Thực thể liên quan|
|—||**Luồng dữ liệu chính**|||
|1|**App Peye-Haiti**|**Kiểm tra số điện thoại đã ghi nhớ**  <br>• Có số trên máy → **sang Bước 3**  <br>• Không có → **sang Bước 2**|Số điện thoại đọc từ Keychain/Keystore của máy|–|
|2|**Người dùng**|**Nhập số điện thoại**  <br>Nhập vào control **Phone number** tại NB-0C. App kiểm định dạng **tại máy** theo `FORMAT_MSISDN` — sai định dạng thì báo lỗi ngay, **không** gọi API|Quy tắc trường: xem **Phone Number** ở `PL-02`|–|
|3|**App Peye-Haiti**|**Gọi MSISDN precheck**  <br>Gửi `msisdn` + `device_id`|Endpoint mới — xem CR-K. Chạy cho **cả hai đường**: số nhập tay và số đã ghi nhớ trên máy|–|
|4|**Merchant Identity Service**|**Kiểm tra tồn tại tài khoản**  <br>• Có `person` gắn với `msisdn` → **sang Bước 6**  <br>• Không có → **sang Bước 5**|–|`person`|
|5|**Merchant Identity Service**|**Trả lỗi không tìm thấy tài khoản**  <br>Trả `PIN-404-PERSON`. App hiện NB-0C trạng thái lỗi|Hết luồng. Nút **Sign up** mang theo số đã nhập sang NB-01|`person`|
|6|**Merchant Identity Service**|**Kiểm tra trạng thái tài khoản**  <br>• `Locked` → **sang Bước 7**  <br>• `Terminated` → **sang Bước 8**  <br>• `Active` → **sang Bước 9**|`person.status` chỉ có 3 giá trị. Khóa do sai PIN **không** nằm ở đây|`person`|
|7|**Merchant Identity Service**|**Trả lỗi tài khoản đang bị khóa**  <br>Trả `PIN-422-ACCLOCKED`. App hiện lỗi|Hết luồng. Đây là **khóa khẩn**, không phải khóa do sai PIN. Thao tác mở lại nằm trên portal BRH|`person`|
|8|**Merchant Identity Service**|**Trả lỗi tài khoản đã đóng**  <br>Trả `PIN-422-ACCCLOSED`. App hiện lỗi, hướng dẫn đăng ký mới|Hết luồng. `Terminated` là trạng thái cuối, không có đường phục hồi trong app|`person`|
|9|**Merchant Identity Service**|**Kiểm tra khóa đăng nhập**  <br>• `person` đang có `login_lock` còn hiệu lực → **sang Bước 10**  <br>• Không có → **sang Bước 11**|**(*) MỚI ở v1.1 — QĐ-30.** Kiểm ở đây để **không gửi OTP vô ích** cho tài khoản đang bị khóa đăng nhập. Ở v1.0 việc này chỉ làm ở Luồng 3 · Bước 3, tức sau màn PIN|`login_lock`|
|10|**Merchant Identity Service**|**Trả trạng thái khóa đăng nhập**  <br>Trả `` PIN-422-`PINLOCKED` `` kèm `details.locked_until`.<br><br>App mở **NB-00 ở trạng thái khóa** — banner **Sign-in locked**, đồng hồ **Try again in**, nút **Reset PIN**. **Kết thúc**|Hết luồng. **Không** gửi OTP, **không** qua NB-0D — kể cả khi thiết bị lạ.  <br>Thông báo nêu **đúng trạng thái tài khoản**, không dùng câu trung tính _(QĐ-30)_|`login_lock`|
|11|**Merchant Identity Service**|**Trả thông tin hiển thị và cờ thiết bị**  <br>Trả `msisdn`, tên person _(nếu có)_ để app dựng control **Account card**, kèm cờ **`device_known`** cho biết `device_id` này đã từng đăng nhập thành công chưa|**(*) Trường mới ở v1.1.** Ngoài hai thứ này, precheck **không** trả `kyc_level`, `pin_hash`, hay số lần sai PIN|`person` · `auth_session`|
|12|**App Peye-Haiti**|**Định tuyến theo thiết bị**  <br>• `device_known = false` → mở **NB-0D**, **sang Luồng 4** để xác thực OTP trước  <br>• `device_known = true` → mở **NB-00**, **sang Luồng 3** để nhập PIN|**Đây là điểm đảo thứ tự của v1.1.** Ở v1.0, mọi đường đều vào NB-00 trước và OTP chỉ xuất hiện sau khi PIN đã đúng|`auth_session`|
|—||**Luồng dữ liệu rẽ nhánh**|||
|2a|**Người dùng**|**Đăng ký chủ động**  <br>Bấm **Sign up** → chuyển sang NB-01 _(thuộc CN-01)_|Ngoài phạm vi tài liệu này|–|
|2b|**Người dùng**|**Quay lại NB-00**  <br>Bấm **Back** _(control 1)_ → quay lại NB-00 với số điện thoại cũ|Chỉ khả dụng khi vào NB-0C từ NB-00. Không xóa gì trên máy|–|
|3a|**App Peye-Haiti**|**Precheck không gọi được server — đường đăng nhập mới**  <br>Thông báo _"No connection — please try again"_, **giữ nguyên số đã nhập**, cho bấm thử lại|**Không** đi tiếp sang NB-0D hay NB-00 khi chưa precheck được|–|
|3b|**App Peye-Haiti**|**Precheck không gọi được server — đường xác thực lại**  <br>Vào từ Luồng 1 · Bước 8: thông báo riêng _"You need a connection to confirm it is you. Try again when you are online."_  <br>**Tuyệt đối KHÔNG xóa refresh token và KHÔNG xóa số điện thoại đã ghi nhớ**|Thông báo phải **khác** nhánh 3a: ở 3a người dùng đang đăng nhập mới, ở 3b họ vẫn đang đăng nhập và chỉ đang thiếu mạng|`auth_session`|
|5a|**App Peye-Haiti**|**Số đã ghi nhớ nhưng tài khoản không còn**  <br>Precheck trả `PIN-404-PERSON` cho số **đọc từ máy** → app xóa số điện thoại đã ghi nhớ và xóa refresh token, rồi hiện NB-0C trống với nút Back ẩn|Xảy ra khi tài khoản bị xóa phía server hoặc số đã đổi chủ. Đây là **server từ chối rõ ràng**, nên xóa token ở đây là đúng|–|

### 3.2.3. Luồng 3 — Xác thực mã PIN

|   |   |   |   |   |
|---|---|---|---|---|
|Bước|Đối tượng|Mô tả|Ghi chú|Bảng/Thực thể liên quan|
|—||**Luồng dữ liệu chính**|||
|1|**Người dùng**|**Nhập mã PIN**<br><br>Nhập đủ ký tự vào control **PIN input**; app **tự thực hiện Bước 2** khi đủ ký tự||–|
|2|**App Peye-Haiti**|**Gửi yêu cầu xác thực**<br><br>Gửi `msisdn`, PIN và `device_id`||–|
|3|**Merchant Identity Service**|**Kiểm tra trạng thái khóa đăng nhập:**  <br>• **Không** có khóa còn hiệu lực → **sang Bước 4**  <br>• Đang bị khóa → trả `` PIN-422-`PINLOCKED` `` kèm `details.locked_until`, **sang nhánh 3a**|`person.status` vẫn là `Active` trong suốt thời gian khóa đăng nhập — hai khái niệm độc lập|`login_lock`|
|4|**Merchant Identity Service**|**So khớp mã PIN**<br><br>So khớp PIN với `person.pin_hash`:  <br>• Đúng → **sang Bước 9**  <br>• Sai → **sang Bước 5**|**Không bao giờ lưu PIN rõ.** Thời gian trả lời phải **như nhau** cho PIN đúng và PIN sai|`person`|
|5|**Merchant Identity Service**|**Tăng số lần sai**<br><br>Ghi nhận số lần sai PIN của `person`:  <br>• Chưa đủ `PIN_MAX_ATTEMPTS` → **sang Bước 8**  <br>• Đã đủ `PIN_MAX_ATTEMPTS` → **sang Bước 6**|Đếm theo `person`, **không theo thiết bị**. Bộ đếm **dùng chung** với xác thực nâng cấp của `SRS-COMMON-01`|`login_lock`|
|6|**Merchant Identity Service**|**Khóa đăng nhập**<br><br>Tạo/cập nhật `login_lock` với `locked_until = now + PIN_LOCK_DURATION`.|Người dùng **vẫn vào được** luồng đặt lại PIN của `SRS-CN03` khi đang bị khóa. Không thu hồi phiên là quyết định có chủ đích|`login_lock` · `person`|
|7|**Merchant Identity Service  <br>**|**Gọi đi — gửi SMS cảnh báo khóa đăng nhập**  <br>Gọi Notification Service để gửi SMS qua Natcom (N1) _(nhóm `D.5`)_ — mẫu tin `MS00002` với tham số `{minutes}`|Nội dung tin và hạn mức: xem `CFG-02`. Gửi trong ≤ 10 giây. **Gửi thất bại KHÔNG làm thất bại việc khóa**|`notification`|
|8|**Merchant Identity Service**|**Trả lỗi sai PIN**<br><br>Trả `PIN-401-PINWRONG` kèm `details.tries_left`. App hiện control **PIN error** và cho nhập lại||`login_lock`|
|9|**Merchant Identity Service**|**Kiểm tra thiết bị**  <br>• `device_id` đã từng đăng nhập thành công → **sang Bước 10**  <br>• Thiết bị mới, **không** kèm `verify_token` → trả `PIN-401-NEWDEVICE`; app tự mở NB-0D, **sang Luồng 4**  <br>• Thiết bị mới, `verify_token` sai / hết `STEPUP_TTL` / đã dùng → trả `PIN-401-STEPUP`; app mở lại NB-0D, **sang Luồng 4**  <br>• Thiết bị mới, `verify_token` hợp lệ _(đúng `purpose` và `msisdn`)_ → **sang Bước 10**|Bước này chỉ chạy khi PIN **đã đúng** — OTP không bù cho PIN sai|`auth_session`|
|10|**Merchant Identity Service**|**Mở phiên mới**<br><br>Ghi phiên gắn `device_id` + băm refresh token; đặt `auth_time` và `last_auth_at` về hiện tại; **xóa `login_lock` của `person;`** tiêu verify_token nếu có||`auth_session` · `login_lock`|
|11|**Merchant Identity Service**|**Trả token và hồ sơ**<br><br>Trả cặp token _(access `ACCESS_TOKEN_TTL` / refresh `REFRESH_TOKEN_TTL`)_ kèm `person` và `merchant` để app dựng menu||`person` · `merchant` · `auth_session`|
|12|**App Peye-Haiti**|**Điều hướng vào app**<br><br>Lưu refresh token và số điện thoại lên máy _(mã hóa)_; gửi ngôn ngữ app đang dùng lên để cập nhật `person.lang`; rồi điều hướng NB-03 Trang chủ||`person` · `merchant`|
|—||**Luồng dữ liệu rẽ nhánh**|||
|3a|**Người dùng**|**Màn khóa đăng nhập**<br><br>NB-00 chuyển trạng thái khóa đăng nhập: banner **Sign-in locked**, đồng hồ **Try again in**, nút **Reset PIN**|`PIN-422-PINLOCKED`. Đào tạo hiện trường phải nhấn: **chờ hết giờ là lựa chọn đầu tiên**; đặt lại PIN thu hồi phiên trên **mọi** thiết bị|`login_lock`|
|10a|**Merchant Identity Service**|**Nhánh xác thực lại** **(re-authentication)**<br><br>khi vào NB-00 từ Luồng 1 · Bước 8 — phiên vẫn còn — thì Bước 10 **không** áp dụng. Thay vào đó **chỉ cập nhật `last_auth_at`** và cấp access token mới với `auth_time` hiện tại|Endpoint riêng. **Không** ghi phiên mới · **không** xoay refresh token · **không** đổi `device_id`.  <br>Bước 12 điều hướng **về đúng chỗ người dùng đang làm**, không về Trang chủ|`auth_session`|
|12a|**Người dùng**|**Gian hàng bị tạm khóa:**<br><br>Vẫn cho đăng nhập, vào app chế độ **chỉ đọc**; mọi thao tác ghi nghiệp vụ bị chặn kèm lý do `PIN-422-SHOPHOLD`;<br><br>NB-1C hiện lý do tạm khóa|BIZ-MERCHANT-STATE|`merchant`|

### 3.2.4. Luồng 4 — Xác thực thiết bị mới bằng OTP

**Điểm vào:** Luồng 2 · Bước 12 khi `device_known = false`. **Điểm ra:** NB-00 để nhập PIN — Luồng 3.

|   |   |   |   |   |
|---|---|---|---|---|
|Bước|Đối tượng|Mô tả|Ghi chú|Bảng/Thực thể liên quan|
|—||**Luồng dữ liệu chính**|||
|1|**App Peye-Haiti**|**Yêu cầu gửi OTP**  <br>Gọi API gửi OTP với `purpose = login_new_device` ngay khi mở NB-0D  <br>• Còn trong `OTP_MAX_PER_DAY` → **sang Bước 2**  <br>• Vượt hạn mức → trả `PIN-422-OTPLIMIT`, **sang nhánh 1a**||–|
|2|**Merchant Identity Service  <br>**|**Gọi đi — gửi SMS chứa mã OTP**  <br>Gọi Notification Service để gửi SMS qua Natcom (N1) _(nhóm `D.5`)_ — mẫu tin `MS00001` với tham số `{otp}` và `{ttl_min}`|Nội dung tin: xem `CFG-02`.  <br>Tin này **kiêm vai trò cảnh báo** cho chủ số. Ở v1.1 nó tới **trước** khi ai đó nhập PIN, nên người nhận có thể hoàn toàn không thao tác gì — mẫu tin **bắt buộc** có câu hướng dẫn gọi 8686|`notification`|
|3|**Người dùng**|**Nhập mã OTP**  <br>Nhập vào control **OTP input** tại NB-0D; app **tự xác nhận** khi đủ ký tự|Trường **OTP**: xem `PL-02`|–|
|4|**App Peye-Haiti**|**Gửi yêu cầu xác thực OTP**  <br>Gửi mã và mã tham chiếu OTP|–|–|
|5|**Merchant Identity Service**|**Kiểm tra mã OTP**  <br>• Đúng và còn hiệu lực → **sang Bước 6**  <br>• Sai → trả `PIN-422-OTPWRONG`, **sang nhánh 5a**  <br>• Quá `OTP_TTL` → trả `PIN-422-OTPEXPIRED`, **sang nhánh 5a**  <br>• Mã tham chiếu không tồn tại → trả `PIN-404-OTP`, **sang nhánh 5a**|**(*) Đổi theo CFG-03 v2.0:** sai **một lần** là mã bị **hủy ngay**, không còn số lượt nhập lại cho cùng một mã|–|
|6|**Merchant Identity Service**|**Cấp `verify_token`**  <br>Cấp `verify_token` hiệu lực `STEPUP_TTL`, `purpose = login_new_device`, `amr = ["pin","otp"]`||–|
|7|**App Peye-Haiti**|**Mở màn nhập PIN**  <br>Giữ `verify_token` trong bộ nhớ, mở **NB-00** với banner **Device verified**. **Sang Luồng 3**||–|
|—||**Luồng dữ liệu rẽ nhánh**|||
|1a|**Người dùng**|**Vượt hạn mức OTP trong ngày**  <br>Chặn gửi thêm, hướng dẫn thử lại ngày kế tiếp|`PIN-422-OTPLIMIT.`Vì hạn mức đếm chung cả 4 `purpose`, cạn quota chặn luôn đường **đặt lại PIN** và đường **khóa khẩn bằng OTP** — xem điểm mở ở cuối tài liệu|–|
|4a|**App Peye-Haiti**|**Người dùng thoát giữa luồng**  <br>Bấm **Back** _(control 1)_ hoặc đóng app → **hủy mã OTP đang chờ**; quay lại **NB-0C**, phải bắt đầu lại từ số điện thoại||–|
|5a|**App Peye-Haiti**|**Mã bị hủy — gửi lại mã**  <br>Xóa ô nhập, dừng đồng hồ, hiện control **OTP error theo mã lỗi cụ thể** và **bật ngay** **Resend code**. Người dùng bấm Resend code → **quay lại Bước 1** _(tiêu thêm một lượt `OTP_MAX_PER_DAY`)_||–|

### 3.2.5. Luồng 5 — Phiên hết hạn hoặc cần xác thực lại giữa lúc đang dùng app

|   |   |   |   |   |
|---|---|---|---|---|
|Bước|Đối tượng|Mô tả|Ghi chú|Bảng/Thực thể liên quan|
|—||**Luồng dữ liệu chính**|||
|1|**Người dùng**|**Vào chức năng cần gọi API**  <br>Ví dụ mở két tiền, đồng bộ sổ nợ, xem báo cáo doanh thu|**Chức năng chỉ đọc dữ liệu cục bộ không kích hoạt luồng này. Sinh QR — cả tĩnh lẫn động — cũng không**: QR luôn render tại máy|–|
|2|**App Peye-Haiti**|**Gửi yêu cầu kèm access token**  <br>Gắn access token và `device_id` vào yêu cầu|–|–|
|3|**Merchant Identity Service**|**Kiểm tra access token**  <br>• Còn hiệu lực và còn trong `PIN_REAUTH_INTERVAL` → **sang Bước 4**  <br>• Hết hạn `ACCESS_TOKEN_TTL` → **sang Bước 5**  <br>• Còn hiệu lực nhưng quá `PIN_REAUTH_INTERVAL` → **sang nhánh 3a**|Ba kết quả **loại trừ nhau** — server chỉ trả một `details` cho mỗi lỗi|`auth_session`|
|4|**Merchant Identity Service**|**Trả kết quả nghiệp vụ**  <br>Xử lý bình thường theo từng chức năng. **Kết thúc**|–|Theo từng chức năng|
|5|**Merchant Identity Service**|**Trả lỗi access token hết hạn**  <br>Trả `PIN-401-EXPIRED`|App **không** hiện lỗi này cho người dùng — xử lý ngầm ở Bước 6|–|
|6|**App Peye-Haiti**|**Gia hạn phiên ngầm**  <br>Tự động gọi API gia hạn phiên với refresh token + `device_id`, **không hỏi người dùng**|Chỉ thử **một lần** cho mỗi lỗi 401; nhiều yêu cầu song song phải **dồn về một** lần gia hạn|`auth_session`|
|7|**App Peye-Haiti**|**Phân biệt lỗi mạng với việc server từ chối**  <br>• **Không nhận được phản hồi nào** — mất mạng, timeout → **sang Bước 8**  <br>• Nhận được phản hồi từ server → **sang Bước 9**|**Đây là bước quan trọng nhất của luồng.** Gộp hai trường hợp này lại là lỗi nghiêm trọng: người bán mất mạng sẽ bị xóa phiên và **không đăng nhập lại được cho tới khi có mạng**|–|
|8|**App Peye-Haiti**|**Giữ token, chuyển chế độ ngoại tuyến**  <br>**Giữ nguyên** access token và refresh token trên máy. Hiện chỉ báo ngoại tuyến, cho tiếp tục đọc/ghi cục bộ và sinh QR; **Không** đưa về NB-00. **Kết thúc**|Chức năng cần server bị vô hiệu kèm lý do, không hiện mã lỗi kỹ thuật|–|
|9|**Merchant Identity Service**|**Kiểm tra refresh token**  <br>• Còn hiệu lực và chưa bị thu hồi → **sang Bước 10**  <br>• Hết hạn `REFRESH_TOKEN_TTL` → **sang Bước 11**  <br>• Đã bị thu hồi _(khóa khẩn, đặt lại PIN, phát hiện tái dùng token cũ)_ → **sang Bước 11**|Tái dùng refresh token cũ ⇒ **thu hồi cả chuỗi phiên**|`auth_session`|
|10|**App Peye-Haiti**|**Gọi lại API nghiệp vụ**  <br>Nhận access token mới, gọi lại đúng yêu cầu ban đầu; **người dùng không thấy gián đoạn**. **Kết thúc**|Ghi refresh token mới thay bản cũ lên máy|–|
|11|**App Peye-Haiti**|**Xóa phiên trên máy**  <br>Xóa access token và refresh token khỏi bộ nhớ và khỏi máy|Server trả `PIN-401-SESSION`. **Chỉ tới bước này khi server đã từ chối rõ ràng.** **Giữ nguyên** số điện thoại đã ghi nhớ và **giữ nguyên** kho dữ liệu cục bộ|–|
|12|**App Peye-Haiti**|**Thoát về màn nhập PIN**  <br>Đặt ngữ cảnh **đăng nhập mới**, **sang Luồng 2**; NB-00 hiện banner **Session expired**, nút Back **ẩn**|Thao tác nghiệp vụ đang dở **không** được lưu tự động|–|
|—||**Luồng dữ liệu rẽ nhánh**|||
|3a|**Merchant Identity Service**|**Hết chu kỳ xác thực lại**  <br>Access token chưa hết hạn nhưng `now − auth_time` > `PIN_REAUTH_INTERVAL` → trả `PIN-401-REAUTH`. App **không** gia hạn ngầm, mà đi thẳng tới NB-00 banner **Routine check**||`auth_session`|

##   
3.4. Bảng / thực thể liên quan

Đây là **mô hình dữ liệu logic**. Tài liệu không quy định tầng lưu trữ vật lý — team kỹ thuật tự quyết định.

|   |   |   |   |   |   |
|---|---|---|---|---|---|
|STT|Thực thể|Mô tả|Trường chính|Thao tác|Ghi chú|
|1|`person`|Danh tính cá nhân — nguồn xác thực của chức năng này|`id` · `msisdn` · `pin_hash` · `status` · `lang` · `kyc_level` · `full_name`|**R** _(precheck, xác thực PIN)_ · **U** _(cập nhật `lang`)_|`msisdn` **duy nhất** — là danh tính đăng nhập, kênh OTP và kênh khóa khẩn. `pin_hash` = Argon2id _(m = 64MB, t = 3, p = 1)_, chỉ có **một** cột băm PIN. `lang` mặc định `ht`|
|2|`auth_session`|Phiên đăng nhập của app|`id` · `person_id` · `device_id` · `fingerprint` · `is_agent_session` · `refresh_hash` · `expires_at` · `revoked` · `last_auth_at`|**C** _(đăng nhập mới)_ · **U** _(xoay refresh token; `last_auth_at` khi xác thực lại; `revoked` khi đặt lại PIN / khóa khẩn / phát hiện tái dùng token)_ · **R**|`device_id` là giá trị **đục, client sinh, không khóa ngoại, không duy nhất** ⇒ hệ thống **không giới hạn số phiên/thiết bị** trên một `person`. Chỉ lưu **băm** refresh token.  <br>`last_auth_at` là nguồn của claim `auth_time`; **rỗng** nghĩa là buộc xác thực lại ngay. **Gia hạn ngầm KHÔNG ghi trường này**|
|3|`login_lock`|**Trạng thái khóa đăng nhập do sai PIN** — tách khỏi `person.status`|`person_id` · `failed_count` · `locked_until`|**C · R · U · D** _(xóa khi đăng nhập thành công hoặc đặt lại PIN)_|Là **khóa tạm theo hành vi**, không phải trạng thái của `person`. Bộ đếm **dùng chung** với `SRS-COMMON-01`. Hiệu lực tự hết theo `locked_until`|
|4|`merchant`|Hồ sơ gian hàng — dùng để điều hướng sau đăng nhập và hiển thị tên ở **Account card**|`id` · `code` · `shop_name` · `status`|**R**|Trả ở precheck _(chỉ `shop_name`)_ và ở kết quả đăng nhập _(đầy đủ)_. `status = suspended` → vào app chế độ chỉ đọc|
|5|`param`|Tham số hệ thống|Xem `CFG-01`|**R**|Giá trị, khoảng hợp lệ và ràng buộc kiểm chéo: **toàn bộ ở `CFG-01`**|
|6|`notification`|Thông báo và bản ghi SMS đã gửi|`id` · `person_id` · `kind` · `template_code` · `channel` · `status` · `acked_at`|**C**|Dùng cho `MS00001` và `MS00002`. Nội dung mẫu tin: xem `CFG-02`|

**Trạng thái `person`**

|   |   |   |   |
|---|---|---|---|
|Giá trị|Nghĩa|Đăng nhập được?|Đường ra|
|`Active`|Hoạt động bình thường. **Bao gồm cả trường hợp đang bị khóa đăng nhập do sai PIN**|Có — trừ khi đang có `login_lock` còn hiệu lực|–|
|`Locked`|Bị khóa để bảo vệ: khóa khẩn qua hotline khi mất máy, yêu cầu của chủ số, hoặc quyết định của BRH|**Không** — precheck trả `BIZ-PERSON-LOCKED`|Gọi hotline 8686; **OPs BRH mở lại trên portal BRH** theo runbook|
|`Terminated`|Tài khoản đã đóng. **Trạng thái cuối**|**Không** — precheck trả `BIZ-PERSON-TERMINATED` **(*)**|**Không có** đường tự phục hồi trong app|

**Phân biệt trạng thái tài khoản với khóa tạm theo hành vi** — điểm thiết kế cốt lõi:

- `person.status` là trạng thái **nghiệp vụ**, do con người hoặc quy trình quyết định, đổi ít, có vết kiểm toán.
- `login_lock` là khóa **tạm theo hành vi**, do hệ thống tự đặt và tự hết, đổi thường xuyên, không đổi trạng thái nghiệp vụ.
- Sai PIN đủ ngưỡng **không** làm tài khoản thành `Locked`. Nếu trộn hai khái niệm, báo cáo _"số tài khoản đang bị khóa"_ sẽ đếm lẫn cả người quên PIN, và luồng mở khóa khẩn _(cần OTP + định danh lại)_ sẽ bị áp oan cho người chỉ cần chờ hết giờ.

## 3.5. Điểm tiếp xúc hệ thống ngoài

|   |   |   |   |   |   |
|---|---|---|---|---|---|
|STT|Hệ thống ngoài|Điểm tiếp xúc|Chiều|Kết quả nghiệp vụ|Xử lý khi lỗi / suy giảm|
|1|**Natcom SMS (N1)**|Gửi OTP thiết bị mới — `MS00001` với `purpose = login_new_device`|MMS → Natcom|Người dùng nhận mã OTP trên mọi mạng|Lỗi hệ thống → thử lại 3 lần **giữ nguyên mã tham chiếu**. Mạch ngắt mở hoặc bảo trì → `PIN-503-DEP`, hướng dẫn gọi hotline 8686 nhận OTP qua thoại|
|2|**Natcom SMS (N1)**|Cảnh báo khóa đăng nhập do sai PIN — `MS00002`|MMS → Natcom|Chủ tài khoản biết có người đang thử đăng nhập|Template chưa đăng ký — xem `CFG-02`. Gửi thất bại **không** làm thất bại việc khóa|
|3|**Portal BRH (BRH-03)**|**Khóa khẩn và mở khóa khẩn** — chuyển `person.status` sang `Locked` / về `Active`, thu hồi mọi phiên|OPs BRH → MMS|Mọi phiên bị thu hồi; QR vẫn nhận tiền bình thường|**App không có chức năng này**: người dùng gọi hotline 8686, OPs BRH thao tác trên portal. Thiết bị bị thu hồi phát hiện ở lần gọi API kế tiếp _(Luồng 5 · Bước 9)_; precheck lần sau trả `BIZ-PERSON-LOCKED`.  <br>**Cửa sổ có hiệu lực chưa chốt — xem mục 4.4**|

# 4. Danh sách mã lỗi

## 4.1. Danh mục mã lỗi của chức năng

|STT|Mã lỗi|Tình huống phát sinh|Hành động tiếp theo|
|---|---|---|---|
|1|`PIN-400-PHONEFMT`|Số điện thoại sai `FORMAT_MSISDN` / độ dài|Sửa số. App kiểm trước tại máy — mã server chỉ xuất hiện khi client cũ hoặc bị can thiệp|
|2|`PIN-400-VAL`|**Mã dự phòng** — thiếu `device_id` hoặc trường thiết bị bắt buộc|Ghi log cảnh báo — xuất hiện nghĩa là bug client|
|3|`PIN-401-EXPIRED`|Access token hết `ACCESS_TOKEN_TTL`|Gia hạn ngầm **một lần** rồi gọi lại yêu cầu gốc _(B6)_|
|4|`PIN-401-REAUTH`|Phiên còn nhưng quá `PIN_REAUTH_INTERVAL`, hoặc `last_auth_at` rỗng|Sang Luồng 2 với ngữ cảnh xác thực lại; nhập PIN đúng → nhánh 10a, **quay lại đúng chỗ đang làm**|
|5|`PIN-401-SESSION`|Refresh token sai / hết `REFRESH_TOKEN_TTL` / đã thu hồi / tái dùng|Xóa token trên máy, **giữ** số điện thoại; sang Luồng 2|
|6|`PIN-401-PINWRONG`|Sai PIN, chưa đủ `PIN_MAX_ATTEMPTS`|Nhập lại. **Không** tiêu `verify_token`|
|7|`PIN-401-NEWDEVICE`|PIN đúng, thiết bị chưa từng đăng nhập, **không** kèm `verify_token`|Tự mở NB-0D, sang Luồng 4|
|8|`PIN-401-STEPUP`|`verify_token` sai / hết `STEPUP_TTL` / đã dùng|Mở lại NB-0D, xin mã mới — **tiêu thêm một lượt OTP trong ngày**|
|9|`PIN-404-PERSON`|Số điện thoại chưa có tài khoản|Số đọc từ máy → xóa số và refresh token _(5a)_|
|10|`PIN-404-OTP`|`otp_id` không tồn tại|Bật ngay **Resend code**|
|11|`PIN-422-OTPWRONG`|Nhập sai OTP — mã bị hủy ngay|Xóa ô, dừng đồng hồ, bật ngay **Resend code**. **Không** hiện số lượt còn lại|
|12|`PIN-422-OTPEXPIRED`|OTP quá `OTP_TTL`|Như mã 11, **khác câu**|
|13|`PIN-422-OTPLIMIT`|Vượt `OTP_MAX_PER_DAY` _(đếm chung mọi mục đích)_|Chặn gửi thêm trong ngày; thử lại ngày mai hoặc gọi 8686|
|14|`PIN-422-PINLOCKED`|Có `login_lock` còn hiệu lực|Hai lối ra: chờ hết giờ _(khuyến nghị)_ hoặc đặt lại PIN _(SRS-CN03)_. `person.status` **vẫn** `Active`|
|15|`PIN-422-ACCLOCKED`|`person.status = Locked` — khóa khẩn|**Không** dùng được luồng đặt lại PIN|
|16|`PIN-422-ACCCLOSED`|`person.status = Terminated`|**Không** có đường tự phục hồi trong app|
|17|`PIN-422-SHOPHOLD`|Gian hàng `suspended` / `closed`, gọi thao tác **ghi**|**Vẫn** cho đăng nhập, app ở chế độ chỉ đọc; NB-1C hiện lý do|
|18|`PIN-422-SMSUNREACH`|Natcom báo số không tồn tại / bị chặn SMS _(`N1-422-MSISDN`)_|**Không** tự thử lại; gọi 8686 hoặc nhờ nhân viên hiện trường|
|19|`PIN-429-OTPWAIT`|Bấm **Resend code** khi mã còn sống|Vô hiệu (7), chạy đồng hồ theo `Retry-After`. Thông điệp **trung tính**|
|20|`PIN-429-RATE`|Vượt hạn mức tần suất chung _(chống dò số / dò PIN theo IP, thiết bị)_|Chờ theo `Retry-After`|
|21|`PIN-500-SYS`|Lỗi hệ thống MMS|**Ở Luồng 5 đi nhánh Bước 8** — giữ token, **không** xóa phiên|
|22|`PIN-503-OTPSEND`|Không gửi được OTP _(Natcom lỗi, mạch ngắt mở, bảo trì)_|**Không** tiêu lượt OTP; bấm Resend hoặc gọi 8686 nhận OTP qua thoại|
|23|`PIN-000-UNKNOWN`|App nhận mã không có trong bảng này|**Luôn** ghi log cảnh báo kèm `trace_id`|

## 4.2. Phân biệt các mã 401

Ở v1.0 ba tình huống dùng chung `PIN-401-AUTH` và phải đọc `details`. Ở v1.1 **mỗi tình huống một mã** — bảng này giữ lại để nhấn mạnh hành vi **không được làm**.

|Mã|Phiên còn không?|App phải làm gì|**Không** được làm gì|
|---|---|---|---|
|`PIN-401-EXPIRED`|Còn|Gia hạn ngầm **một lần**, rồi gọi lại yêu cầu gốc. Người dùng không thấy gì|Không hiện lỗi · không hỏi PIN|
|`PIN-401-REAUTH`|**Còn**|Sang Luồng 2 ngữ cảnh xác thực lại → NB-00 banner **Routine check**; nhập PIN đúng → nhánh 10a và **quay lại đúng chỗ đang làm**|**Không** gia hạn ngầm · **không** xóa refresh token · **không** tạo phiên mới|
|`PIN-401-SESSION`|**Không**|Xóa token, giữ số điện thoại, sang Luồng 2 → NB-00 banner **Session expired**|Không xóa kho dữ liệu cục bộ|
|`PIN-401-NEWDEVICE`|Chưa có|Tự mở **NB-0D**, sang Luồng 4|Không hiện lỗi · không quay về NB-0C|
|`PIN-401-STEPUP`|Chưa có|Mở lại **NB-0D**, báo sẽ tiêu một lượt OTP|Không tự xin mã mới khi người dùng chưa bấm|

**Lỗi mạng không thuộc nhóm nào ở đây** — nó đi nhánh Luồng 5 · Bước 8, giữ nguyên token.

# 5. Chức năng ảnh hưởng

|   |   |   |   |
|---|---|---|---|
|STT|Kênh thực hiện|Chức năng|Nội dung ảnh hưởng|
|1|App|**CN-01** · Đăng ký, chọn vai & định danh|CN-02 tiêu thụ đầu ra của CN-01. Ngược lại CN-01 phải sửa hai điểm:<br><br>① NB-0B _(Choose your language)_ **đứng trước** NB-01, nên trường ngôn ngữ ở bước đăng ký lấy giá trị từ đây thay vì để người dùng chọn lại;<br><br>② NB-01 phải **nhận tham số số điện thoại** ở điểm vào, để nút **Sign up** của NB-0C không bắt người dùng nhập lại|
|2|App|**`CN-03`** · Quên PIN & đặt lại PIN|CN-02 refer sang qua control **Forgot PIN? Verify by OTP** và  **Reset PIN** của NB-00. Hai điểm nối phải khớp:<br><br>① luồng đặt lại PIN **vẫn vào được khi đang có `login_lock`**;<br><br>② đặt lại PIN thành công thì **xóa `login_lock`** và **thu hồi mọi phiên**.<br><br>NB-0D được dùng chung|
|3|App|**`COMMON-01`** · Xác thực nâng cấp cho hành động nhạy cảm|Ba thứ **dùng chung** với CN-02:<br><br>① `person.pin_hash`;<br><br>② bộ đếm sai PIN trong `login_lock` — sai PIN đủ ngưỡng khi xác thực nâng cấp sẽ khóa cả đường đăng nhập;<br><br>③ claim `auth_time` — xác thực nâng cấp thành công **làm mới** `auth_time`, nên người dùng hay dùng chức năng này sẽ ít gặp màn xác thực lại|
|4|App|**CN-06 / CN-07** · Đơn tính tiền · Sổ nợ & khách quen|Hai chức năng đọc/ghi kho dữ liệu cục bộ. Khóa mã hóa không phụ thuộc PIN<br><br>⇒ ① đặt lại PIN **không** mất dữ liệu;<br><br>② vào Trang chủ không cần PIN vẫn đọc được sổ nợ.  <br>Phiên còn dùng được + mất mạng ⇒ **vẫn mở được app**, dùng được sổ nợ, đơn tính tiền và **sinh được QR cả tĩnh lẫn động**.  <br>**Hai trường hợp vẫn không mở được app khi mất mạng:**  ① hết phiên; ② hết `PIN_REAUTH_INTERVAL`.<br><br>Cần thiết kế hàng đợi đồng bộ chịu được việc app mở offline nhiều ngày liền|
|5|App|**CN-13** · Hồ sơ, cài đặt & ngoại tuyến|NB-14 là nơi đổi ngôn ngữ sau khi đăng ký và hiển thị hàng đợi đồng bộ. Bị đẩy về màn PIN _(Luồng 5 · Bước 12)_ sẽ **cắt ngang** hàng đợi đang chạy — cần định nghĩa hành vi tiếp tục sau khi đăng nhập lại.  <br>**Chỉ báo trạng thái ngoại tuyến** _(Luồng 5 · Bước 8)_ thuộc màn này|
|6|App|**CN-08 / CN-10** · Thanh toán trong app & liên kết nguồn trả|PIN app cũng là bậc xác thực thứ nhất của mọi lệnh trả; dùng chung `person.pin_hash` và chung `login_lock`. Bị khóa đăng nhập do sai PIN ⇒ **cũng không xác nhận được lệnh trả**|
|7|App|**CN-05 / CN-30** · Két tiền, báo Có & khớp lệnh|Báo Có **không phụ thuộc phiên app** — khóa khẩn thu hồi phiên nhưng **QR vẫn nhận tiền bình thường**. Cần nêu rõ trong đào tạo hiện trường để người bán không hiểu sai|
|8|Portal BRH|**CN-17** · Hậu kiểm & quản lý người bán|Ba điểm: ① cán bộ BRH tạm khóa **gian hàng** → người bán **vẫn đăng nhập được** nhưng vào chế độ chỉ đọc; ② portal phải phân biệt rõ **`person.status = Locked`** _(khóa tài khoản, chặn đăng nhập)_ với **`login_lock`** _(khóa đăng nhập tạm do sai PIN, tài khoản vẫn `Active`)_; ③ **portal là nơi duy nhất thực hiện khóa khẩn / mở khóa khẩn** — cần đặc tả thao tác và runbook hotline 8686 tương ứng|
|9|App|**Đăng xuất**|Đăng nhập xong có thể đăng xuất|
|10|App|**Đổi PIN**|Đăng nhập xong có thể đổi PIN|