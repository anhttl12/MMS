**![](http://10.254.136.32:8090/plugins/servlet/confluence/placeholder/macro?definition=e3RvY30&locale=en_US&version=2)  
**

**Bảng ghi nhận thay đổi tài liệu**

A – Tạo mới, M – Sửa đổi, D – Xóa bỏ

|   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|
|Ngày|Vị trí|A/M/D|Nguồn gốc|PB cũ|Mô tả thay đổi|PB mới|
|08/09/2026|Toàn bộ|A||—|Tạo mới tài liệu|1.0|

## 1. MÔ TẢ CHUNG

|   |   |
|---|---|
|Hạng mục|Nội dung|
|**Mục đích**|Đặc tả **một lần** các thành phần xác thực dùng chung:<br><br>- màn nhập PIN (NB-0F)<br>- màn nhập OTP (NB-0G)<br>- luồng kiểm PIN<br>- luồng gửi OTP<br>- luồng xác thực OTP<br><br>Chức năng nghiệp vụ nào cần PIN hoặc OTP thì **tham chiếu** tới tài liệu này, **không mô tả lại**|
|**Loại chức năng**|Xác thực (V) — thành phần dùng chung, không có điểm vào riêng trên menu|
|**Đối tượng sử dụng**|Người bán / tiểu thương (vai BÁN) · Người mua (vai MUA) — theo hành động cụ thể|
|**Kênh**|App Peye-Haiti|
|**Đường dẫn**|_(Bất kỳ màn nghiệp vụ)_ → hành động cần PIN → **NB-0F** _(lớp phủ nhập PIN)_ → _(nếu cần OTP)_ **NB-0G** _(lớp phủ nhập OTP)_ → **quay lại đúng chỗ đang làm**|
|**Precondition**|1) Luồng 1 (PIN): người dùng đang có phiên đăng nhập hợp lệ  <br>2) Luồng 2, 3 (OTP): tùy `purpose` — có phiên hoặc chưa đăng nhập (đăng ký, quên PIN, khóa khẩn)  <br>3) Có kết nối mạng tới BFF|
|**Post-condition**|**PIN đúng:** bộ đếm sai reset về 0, hành động nghiệp vụ được thực hiện **trong cùng request.**<br><br>**PIN sai hết lượt  **`PIN_MAX_ATTEMPTS`**:** tạo `login_lock` với `PIN_LOCK_DURATION`, gửi SMS `MS00002`, hành động bị hủy<br><br>**OTP đúng:** cấp `verify_token` theo `purpose` (hiệu lực STEPUP_TTL, dùng một lần) dùng 1 lần, hành động nghiệp vụ được gọi kèm `verify_token` để hoàn tất hành động, `verify_token` bị đánh dấu đã dùng.<br><br>**OTP sai hết lượt:** mã bị hủy, người dùng phải gửi lại mã  <br><br>**Hủy giữa luồng:** không cấp `verify_token`; hành động nghiệp vụ **không** được thực hiện; người dùng quay lại **đúng trạng thái trước đó, không mất dữ liệu đang nhập**.|

### 1.1. Bảng thuật ngữ

|   |   |
|---|---|
|Thuật ngữ|Nghĩa trong tài liệu này|
|**PIN**|Mã 6 số của app Peye-Haiti, tách biệt PIN ví/ngân hàng. Lưu băm tại `person.pin_hash`|
|**OTP Peye-Haiti**|Mã 6 số do Merchant Identity Service sinh, gửi SMS qua Natcom N1|
|**OTP định chế**|Mã do định chế tài chính sinh và gửi qua SMS gateway của chính định chế (liên kết tài khoản, thanh toán > ngưỡng). MMS chỉ chuyển tiếp, không kiểm. Dùng lại NB-0G|
|`**purpose**`|Mục đích của một OTP: `register` · `login_new_device` · `pin_reset` · `emergency_lock`...|
|**`verify_token`**|Phiếu cấp sau khi OTP đúng: gắn `purpose`, **dùng một lần**, hiệu lực theo tham số `STEPUP_TTL`|
|**`auth_time`**|Claim chuẩn OIDC — mốc người dùng nhập PIN hoặc OTP thành công lần cuối. Step-up thành công **làm mới** mốc này|

**Danh mục tham số cấu hình sử dụng**

|STT|Mã / Tham số|Tài liệu nguồn|
|---|---|---|
|**A**|**Tham số hệ thống**||
|1|`PIN_MAX_ATTEMPTS` · `PIN_LOCK_DURATION`|CFG-01|
|2|`OTP_TTL` · `OTP_RESEND_AFTER` · `OTP_MAX_PER_DAY`|CFG-01|
|3|`OTP_MAX_ATTEMPTS`|CFG-01|
|4|`STEPUP_TTL` _(hạn `verify_token`)_|CFG-01|
|**B**|**Mẫu SMS**||
|5|`MS00001` · `OTP_GENERIC`|CFG-02|
|6|`MS00002` · `LOGIN_LOCK`|CFG-02|
|**C**|**Noti**||
|7|Không sử dụng|CFG-04|
|**D**|**Quy định control & input**||
|8|PIN · OTP|PL-02|
|9|`Bottomsheet` · `Label` · `Hyperlink` · `Pin input` · `Otp input` · `Confirmation`|PL-01|

# 2. Màn hình

## 2.1. Mô phỏng màn hình

|   |   |   |
|---|---|---|
|NB-0F · Enter PIN|NB-0F · Wrong PIN|NB-0F · Forgot PIN? → Leave this step|
|![](http://10.254.136.32:8090/download/attachments/105325969/image2026-9-25_14-39-52.png?version=1&modificationDate=1790321992516&api=v2 "Kinh doanh quốc tế > COMMON-01. PIN & OTP > image2026-9-25_14-39-52.png")|![](http://10.254.136.32:8090/download/attachments/105325969/image2026-9-25_14-39-40.png?version=1&modificationDate=1790321980584&api=v2 "Kinh doanh quốc tế > COMMON-01. PIN & OTP > image2026-9-25_14-39-40.png")|![](http://10.254.136.32:8090/download/attachments/105325969/NB-0F%20%C2%B7%20Forgot%20PIN%20%E2%86%92%20Leave%20this%20step-selection.png?version=1&modificationDate=1790321945929&api=v2 "Kinh doanh quốc tế > COMMON-01. PIN & OTP > NB-0F · Forgot PIN → Leave this step-selection.png")|
|NB-0G · Enter the code (countdown)|NB-0G · Wrong code|NB-0G · Countdown ended|
|![](http://10.254.136.32:8090/download/attachments/105325969/image2026-9-25_14-41-0.png?version=1&modificationDate=1790322060162&api=v2 "Kinh doanh quốc tế > COMMON-01. PIN & OTP > image2026-9-25_14-41-0.png")|![](http://10.254.136.32:8090/download/attachments/105325969/image2026-9-25_14-40-47.png?version=1&modificationDate=1790322047107&api=v2 "Kinh doanh quốc tế > COMMON-01. PIN & OTP > image2026-9-25_14-40-47.png")|![](http://10.254.136.32:8090/download/attachments/105325969/image2026-9-25_14-40-27.png?version=1&modificationDate=1790322027311&api=v2 "Kinh doanh quốc tế > COMMON-01. PIN & OTP > image2026-9-25_14-40-27.png")|

  

## 2.2. Các yếu tố trên màn hình

### 2.2.1. NB-0F - Enter PIN

||**Tên control**|**Loại control**|**Require**|**Maxlength**|**Giá trị mặc định**|**Mô tả**|
|---|---|---|---|---|---|---|
|1|(Khung bottom sheet)|`Bottomsheet`|–|–|–|Trượt từ dưới lên trên màn nghiệp vụ của chức năng gọi. Màn phía sau vẫn thấy, bị làm tối, **giữ nguyên dữ liệu đang nhập**|
|2|Enter your PIN|`Label`|–|–|–|Tiêu đề bottom sheet|
|3|(Nút đóng)|`Button` _(icon X)_|–|–|Enabled|Góc trên bên phải. Bấm → đóng bottom sheet, **không gọi API**, quay lại màn nghiệp vụ|
|4|PIN|`Pin input`|Có|6|Trống|Hiển thị 6 chấm tròn, luôn che ký tự. Nhập đủ 6 số → **app tự gửi** API nghiệp vụ của chức năng gọi. Không cho nhập trong lúc chờ kết quả. Lỗi hiện ngay dưới ô theo mã lỗi — xem Mục 4|
|5|Forgot PIN?|`Hyperlink`|–|–|Enabled|Mở `Confirmation`: _Leave this step? What you were doing will be cancelled._ · nút **Cancel**/ **Confirm**. Chọn **Confirm**→ hủy hành động đang dở, chuyển sang luồng quên PIN (CN-03)|

### 2.2.2. NB-0G - Enter the code

|**STT**|**Tên control**|**Loại control**|**Require**|**Maxlength**|**Giá trị mặc định**|**Mô tả**|
|---|---|---|---|---|---|---|
|1|(Khung bottom sheet)|`Bottomsheet`|–|–|–|Như NB-0F (1). Khi chưa đăng nhập (đăng ký, quên PIN, đăng nhập máy mới) hiển thị dạng **màn đầy đủ** thay vì bottom sheet — chức năng gọi chọn|
|2|Enter the code|`Label`|–|–|–|Tiêu đề|
|3|We sent a code to {msisdn_masked}|`Label`|–|–|–|Số nhận mã ở dạng bản che, vd _+509****3456_|
|4|(Nút đóng)|`Button` _(icon X)_|–|–|Enabled|Góc trên bên phải. Bấm → đóng, không cấp `verify_token`, quay lại trạng thái trước đó|
|5|Code|`Otp input`|Có|6|Trống|6 ô, hiện số đã nhập. Nhập đủ 6 số → **app tự gửi**. Lỗi hiện ngay dưới ô theo mã lỗi — xem Mục 4|
|6|Resend code {mm:ss}|`Hyperlink` + `Countdown timer`|–|–|Disabled|**Một dòng duy nhất dưới ô nhập.**<br><br>- Đang đếm ngược: hiện _Resend code 01:45_, màu xám, **không bấm được**. Mốc đếm lấy từ `resend_after_s` server trả về<br>- Hết đếm ngược: **ẩn bộ đếm**, chỉ còn _Resend code_, **bấm được**<br>    - Bấm → gửi lại mã theo Luồng 2, đếm ngược lại từ đầu<br>- Với **OTP định chế**: **ẩn hẳn** dòng này — định chế không cho gửi lại, thay bằng "Code expires in (mm:ss)" theo thời gian định chế trả về|

**Ghi chú:** Hết đếm ngược **không** làm hủy mã: mã còn trong `OTP_TTL` vẫn nhập được. NB-0G dùng cho cả OTP định chế — khác biệt: định chế kiểm mã và trả số lượt còn lại; với OTP qua định chế, **ẩn hẳn** dòng Resend code, hết hạn thì người dùng tạo lệnh trả mới, hiển thị dòng 

# 3. Luồng nghiệp vụ

## 3.1. Activity diagram

### 3.1.1. Luồng 1 — Xác thực PIN

|   |
|---|
|@startuml<br>!theme plain<br>skinparam backgroundColor #FFFFFF<br>skinparam ActivityBorderColor #4A90E2<br>skinparam ActivityBackgroundColor #FFFFFF<br>skinparam ActivityDiamondBackgroundColor #FFF2CC<br>skinparam ArrowColor #333333<br>skinparam ActivityFontSize 12<br>skinparam swimlaneWidth same<br><br>\|#F5F5F5\|Người dùng\|<br>start<br>:[Bước 1] Bấm hành động cần xác thực PIN tại màn nghiệp vụ;<br>\|#DAE8FC\|App Peye-Haiti\|<br>:[Bước 2] Mở bottom sheet NB-0F;<br>\|#F5F5F5\|Người dùng\|<br>:[Bước 3] Nhập đủ 6 số PIN;<br>\|#DAE8FC\|App Peye-Haiti\|<br>if ([Bước 4] Máy có kết nối mạng?) then (Không)<br>  #FFCCCC:[Bước 4a] Không gọi API, hiện lỗi PIN-000-OFFLINE, xóa ô PIN - quay lại Bước 3;<br>  stop<br>else (Có)<br>  :[Bước 4] Gọi API nghiệp vụ của chức năng gọi, kèm pin trong body;<br>endif<br>\|#D5E8D4\|Merchant Identity Service\|<br>if ([Bước 5] Đăng nhập đang bị khóa do sai PIN?) then (Có)<br>  :[Bước 5] Trả PIN-422-PINLOCKED;<br>elseif ([Bước 6] Tài khoản đang bị khóa khẩn?) then (Có)<br>  :[Bước 6] Trả PIN-422-ACCLOCKED;<br>elseif ([Bước 7] PIN khớp pin_hash?) then (Không)<br>  if ([Bước 8] Tăng bộ đếm sai - còn lượt thử?) then (Còn)<br>    :[Bước 8] Trả PIN-401-PINWRONG kèm tries_left;<br>  else (Hết)<br>    :[Bước 8] Khóa đăng nhập, thu hồi mọi phiên, gửi SMS MS00002, trả PIN-422-PINLOCKED;<br>  endif<br>else (Khớp)<br>  :[Bước 9] Reset bộ đếm sai PIN;<br>  :[Bước 10] Chức năng gọi thực hiện nghiệp vụ, trả kết quả;<br>endif<br>\|#DAE8FC\|App Peye-Haiti\|<br>switch ([Bước 11] Kết quả trả về?)<br>case (Thành công)<br>  #D5E8D4:[Bước 11] Đóng NB-0F, hiện kết quả nghiệp vụ. Kết thúc;<br>  stop<br>case (PIN-401-PINWRONG\nPIN-500-SYS)<br>  #FFCCCC:[Bước 11a] Hiện lỗi theo mã, xóa ô PIN - quay lại Bước 3;<br>  stop<br>case (PIN-422-PINLOCKED\nPIN-422-ACCLOCKED)<br>  #FFCCCC:[Bước 11b] Đóng NB-0F, hủy hành động, hiện lỗi theo mã. Kết thúc;<br>  stop<br>endswitch<br>@enduml|

### 3.1.2. Luồng 2 — Gửi OTP

|   |
|---|
|@startuml<br>!theme plain<br>skinparam backgroundColor #FFFFFF<br>skinparam ActivityBorderColor #4A90E2<br>skinparam ActivityBackgroundColor #FFFFFF<br>skinparam ActivityDiamondBackgroundColor #FFF2CC<br>skinparam ArrowColor #333333<br>skinparam ActivityFontSize 12<br>skinparam swimlaneWidth same<br><br>\|#DAE8FC\|App Peye-Haiti\|<br>start<br>:[Bước 1] Chức năng gọi cần OTP, hoặc người dùng bấm Resend code;<br>if ([Bước 2] Máy có kết nối mạng?) then (Không)<br>  #FFCCCC:[Bước 2a] Không gọi API, hiện lỗi PIN-000-OFFLINE. Kết thúc;<br>  stop<br>else (Có)<br>  :[Bước 2] Gọi API gửi OTP E.1.2 với purpose và msisdn;<br>endif<br>\|#D5E8D4\|Merchant Identity Service\|<br>if ([Bước 3] Vượt OTP_MAX_PER_DAY?) then (Có)<br>  :[Bước 3] Trả PIN-422-OTPLIMIT;<br>elseif ([Bước 4] Mã cũ còn sống và chưa đủ OTP_RESEND_AFTER?) then (Có)<br>  :[Bước 4] Trả PIN-429-OTPWAIT kèm Retry-After;<br>elseif ([Bước 5] msisdn có tài khoản, hoặc purpose là register?) then (Không)<br>  :[Bước 5] Trả 200 như bình thường, không sinh mã, không gửi SMS;<br>else (Có)<br>  :[Bước 6] Hủy mã cũ cùng purpose, sinh OTP mới, lưu dạng băm, đặt số lượt thử;<br>  \|#FFE6CC\|Notification + Natcom N1\|<br>  if ([Bước 7] Gửi SMS MS00001 thành công?) then (Không)<br>    \|#D5E8D4\|Merchant Identity Service\|<br>    :[Bước 7] Trả PIN-503-OTPSEND;<br>  else (Có)<br>    \|#D5E8D4\|Merchant Identity Service\|<br>    :[Bước 8] Trả otp_id, expires_in_s, resend_after_s;<br>  endif<br>endif<br>\|#DAE8FC\|App Peye-Haiti\|<br>switch ([Bước 9] Kết quả trả về?)<br>case (Thành công)<br>  #D5E8D4:[Bước 9] Mở hoặc làm mới NB-0G, đếm ngược Resend code. Sang Luồng 3;<br>  stop<br>case (PIN-422-OTPLIMIT\nPIN-429-OTPWAIT\nPIN-503-OTPSEND\nPIN-500-SYS)<br>  #FFCCCC:[Bước 9a] Hiện lỗi theo mã, xử lý Resend code theo mã. Kết thúc;<br>  stop<br>endswitch<br>@enduml|

### 3.1.3. Luồng 3 — Xác thực OTP

|   |
|---|
|@startuml<br>!theme plain<br>skinparam backgroundColor #FFFFFF<br>skinparam ActivityBorderColor #4A90E2<br>skinparam ActivityBackgroundColor #FFFFFF<br>skinparam ActivityDiamondBackgroundColor #FFF2CC<br>skinparam ArrowColor #333333<br>skinparam ActivityFontSize 12<br>skinparam swimlaneWidth same<br><br>\|#F5F5F5\|Người dùng\|<br>start<br>:[Bước 1] Nhập đủ 6 số OTP tại NB-0G;<br>\|#DAE8FC\|App Peye-Haiti\|<br>if ([Bước 2] Máy có kết nối mạng?) then (Không)<br>  #FFCCCC:[Bước 2a] Không gọi API, hiện lỗi PIN-000-OFFLINE, xóa ô nhập - quay lại Bước 1;<br>  stop<br>else (Có)<br>  :[Bước 2] Gọi API xác thực OTP E.1.3 với otp_id và code;<br>endif<br>\|#D5E8D4\|Merchant Identity Service\|<br>if ([Bước 3] otp_id còn tồn tại?) then (Không)<br>  :[Bước 3] Trả PIN-404-OTP;<br>elseif ([Bước 4] Mã còn hạn?) then (Không)<br>  :[Bước 4] Trả PIN-422-OTPEXPIRED;<br>elseif ([Bước 5] Mã khớp?) then (Không)<br>  if ([Bước 5] Trừ lượt - còn lượt thử?) then (Còn)<br>    :[Bước 5] Trả PIN-422-OTPWRONG kèm tries_left, giữ mã;<br>  else (Hết)<br>    :[Bước 5] Hủy mã, trả PIN-422-OTPLOCKED;<br>  endif<br>else (Khớp)<br>  :[Bước 6] Hủy mã, cấp verify_token, trả 200;<br>endif<br>\|#DAE8FC\|App Peye-Haiti\|<br>switch ([Bước 7] Kết quả trả về?)<br>case (PIN-422-OTPWRONG\nPIN-500-SYS)<br>  #FFCCCC:[Bước 7a] Hiện lỗi theo mã, xóa ô nhập, giữ đồng hồ - quay lại Bước 1;<br>  stop<br>case (PIN-404-OTP\nPIN-422-OTPEXPIRED\nPIN-422-OTPLOCKED)<br>  #FFCCCC:[Bước 7b] Hiện lỗi theo mã, vô hiệu ô nhập, bật Resend code. Kết thúc;<br>  stop<br>case (Thành công)<br>endswitch<br>if ([Bước 8] Máy có kết nối mạng?) then (Không)<br>  #FFCCCC:[Bước 8a] Không gọi API, hiện lỗi PIN-000-OFFLINE, giữ NB-0G. Kết thúc;<br>  stop<br>else (Có)<br>  :[Bước 8] Gọi API nghiệp vụ của chức năng gọi kèm verify_token;<br>endif<br>\|#D5E8D4\|Merchant Identity Service\|<br>if ([Bước 9] verify_token hợp lệ, đúng purpose, chưa dùng?) then (Không)<br>  :[Bước 9] Trả PIN-401-STEPUP;<br>else (Có)<br>  :[Bước 10] Tiêu phiếu và thực hiện nghiệp vụ trong cùng transaction;<br>endif<br>\|#DAE8FC\|App Peye-Haiti\|<br>switch ([Bước 11] Kết quả trả về?)<br>case (Thành công)<br>  #D5E8D4:[Bước 11] Đóng NB-0G, hiện kết quả nghiệp vụ. Kết thúc;<br>  stop<br>case (PIN-401-STEPUP)<br>  #FFCCCC:[Bước 11a] Hiện lỗi theo mã, quay lại Luồng 2. Kết thúc;<br>  stop<br>endswitch<br>@enduml|

  

## 3.2. Mô tả luồng nghiệp vụ

### 3.2.1. Luồng 1 — Xác thực PIN

|Bước|Đối tượng|Mô tả|Bảng/Thực thể liên quan|Ghi chú|
|---|---|---|---|---|
|—||**Luồng dữ liệu chính**|||
|1|**Người dùng**|**Bấm hành động cần xác thực PIN**  <br>Tại màn nghiệp vụ của chức năng gọi  <br>**Sang bước tiếp theo**||Chức năng gọi quy định hành động nào cần PIN|
|2|**App**|**Mở bottom sheet NB-0F**  <br>Bottom sheet trượt lên trên màn nghiệp vụ, ô PIN trống  <br>**Sang bước tiếp theo**|||
|3|**Người dùng**|**Nhập mã PIN**  <br>Nhập đủ 6 số, app tự gửi<br><br>- Bấm nút đóng X → **sang bước 3a**<br>- Bấm _Forgot PIN?_ → **sang bước 3b**<br>- Nhập đủ 6 số → **sang bước tiếp theo**|||
|4|**App**|**Kiểm kết nối mạng và gọi API nghiệp vụ của chức năng gọi**  <br>• Không có mạng → không gọi API, `PIN-000-OFFLINE`, **sang bước 4a**  <br>• Có mạng → gọi API. Body có trường `pin`, `Idempotency-Key` **cho mỗi lần nhập PIN**; thử lại do mất mạng của cùng lần nhập thì giữ key. **Sang bước tiếp theo**||Không có API kiểm PIN riêng cho app|
|5|**Merchant Identity Service**|**Kiểm khóa đăng nhập**  <br>• Đang khóa do sai PIN → trả `PIN-422-PINLOCKED` kèm thời gian còn lại  `details.locked_until`, **sang bước 11**  <br>• Không khóa → **sang bước tiếp theo**|login_lock||
|6|**Merchant Identity Service**|**Kiểm tra trạng thái tài khoản**<br><br>• `` Locked/`Terminated` `` → **sang Bước 11**  <br>• `Active` → **sang bước tiếp theo**|person||
|7|**Merchant Identity Service**|**Kiểm tra PIN**  <br>So khớp với `person.pin_hash`  <br>• Đúng → **sang bước 9**  <br>• Sai → **sang bước tiếp theo**|person|API nghiệp vụ thuộc dịch vụ khác gọi hàm kiểm PIN qua API nội bộ của Merchant Identity Service|
|8|**Merchant Identity Service**|**Tăng bộ đếm sai PIN**  <br>• Còn lượt → trả `PIN-401-PINWRONG` kèm `tries_left`, **sang bước 11**  <br>• Hết lượt → khóa đăng nhập, **thu hồi mọi phiên đăng nhập của người dùng** (kể cả phiên hiện tại), gửi SMS `MS00002`, trả `PIN-422-PINLOCKED`, **sang bước 11**|login_lock, auth_session, notification|Bộ đếm dùng chung với màn đăng nhập|
|9|**Merchant Identity Service**|**Reset bộ đếm sai PIN**  <br>**Sang bước tiếp theo**|login_lock||
|10|**Chức năng gọi**|**Thực hiện nghiệp vụ**  <br>Thực hiện hành động trong cùng request, trả kết quả nghiệp vụ  <br>**Sang bước tiếp theo**|Theo chức năng gọi|Nghiệp vụ lỗi sau khi PIN đúng → trả lỗi của nghiệp vụ|
|11|**App**|**Tiếp nhận kết quả**  <br>• Thành công → đóng NB-0F, hiện kết quả nghiệp vụ. **Kết thúc**  <br>• Thất bại `PIN-401-PINWRONG` → **sang bước 11a**  <br>• Thất bại `PIN-422-PINLOCKED` / `PIN-422-ACCLOCKED/ACCCLOSED` → **sang bước 11b**<br><br>• Thất bại `mã khác` **có phản hồi từ server** → **sang bước 11a**  <br>• **Không nhận được phản hồi nào:** app tự thử lại **cùng `Idempotency-Key`** (1s → 2s → 4s, tối đa 3 lần); vẫn không có sau 3 lần → `PIN-500-SYS` (app tự gán, do không nhận được phản hồi — không phải server trả về), **sang bước 11c**||`PIN-500-SYS` xuất hiện ở cả 11a (server trả lỗi thật) lẫn 11c (app không nhận được phản hồi) — **hai tình huống khác nhau, xử lý khác nhau**, xem ghi chú tại 11c|
|—||**Luồng dữ liệu rẽ nhánh**|||
|3a|**App**|**Đóng bottom sheet**  <br>Không gọi API, quay lại màn nghiệp vụ, giữ nguyên dữ liệu đang nhập. **Kết thúc**||Không tính lượt|
|3b|**App**|**Chuyển sang quên PIN**  <br>Hiện `Confirmation` rời bước; chọn **Leave** → hủy hành động, sang SRS-CN03; chọn **Stay** → **sang bước 3**|||
|4a|**App**|**Hiện lỗi không có mạng**  <br>Hiện lỗi `PIN-000-OFFLINE` dưới ô PIN, xóa ô PIN, giữ bottom sheet  <br>**Sang bước 3**||Chưa gửi request — không tính lượt sai, lần nhập sau dùng `Idempotency-Key` mới|
|11a|**App**|**Hiện lỗi, cho nhập lại**  <br>Hiện lỗi dưới ô PIN theo mã `PIN-401-PINWRONG` / `PIN-500-SYS`, xóa ô PIN, giữ bottom sheet  <br>**Sang bước 3**||`PIN-500-SYS` không tính lượt sai. Áp dụng khi server **có trả lời** (kể cả trả lời là lỗi 500) — request chắc chắn đã xử lý xong (thất bại), nhập lại PIN với `Idempotency-Key` mới là an toàn|
|11b|**App**|**Hiện lỗi, dừng luồng**  <br>Đóng NB-0F, hủy hành động, hiện `Alert` dạng Error theo mã lỗi  <br>**Kết thúc**|||
|11c|**App**|**Hiện lỗi không nhận được phản hồi**  <br>Đóng NB-0F, hiện lỗi theo mã `PIN-500-SYS`, **không** cho nhập lại PIN ngay; chức năng gọi kiểm lại kết quả nghiệp vụ theo SRS của mình  <br>**Kết thúc**||Request có thể đã được xử lý ở phía server dù app không biết — nhập PIN lần mới với `Idempotency-Key` mới có nguy cơ làm nghiệp vụ hai lần. Khác 11a: ở đây app **không hề nhận được** phản hồi (không phải nhận được lỗi 500), nên không thể coi là "request đã xử lý xong (thất bại)"|

### 3.2.2. Luồng 2 — Gửi OTP

|Bước|Đối tượng|Mô tả|Bảng/Thực thể liên quan|Ghi chú|
|---|---|---|---|---|
|—||**Luồng dữ liệu chính**|||
|1|**App**|**Khởi động gửi OTP**  <br>Chức năng gọi cần OTP và xác định `purpose`;<br><br>Hoặc người dùng bấm **Resend code** trên NB-0G  <br>**Sang bước tiếp theo**|||
|2|**App**|**Kiểm kết nối mạng và gọi API gửi OTP**  <br>• Không có mạng → không gọi API, `PIN-000-OFFLINE`, **sang bước 2a**  <br>• Có mạng → gọi E.1.2 `POST /auth/otp/send` với `purpose`, `msisdn`, **sang bước tiếp theo**||API công khai. Riêng `register`: lần gửi đầu nằm trong E.1.1|
|3|**Merchant Identity Service**|**Kiểm hạn mức OTP trong ngày**  <br>• Vượt → trả `PIN-422-OTPLIMIT`, **sang bước 9**  <br>• Chưa vượt → **sang bước tiếp theo**|otp_code||
|4|**Merchant Identity Service**|**Kiểm thời gian chờ gửi lại**  <br>• Mã cũ cùng `purpose` còn hiệu lực và chưa đủ thời gian chờ → trả `PIN-429-OTPWAIT` kèm `Retry-After`, **sang bước 9**  <br>• Ngược lại → **sang bước tiếp theo**|otp_code||
|5|**Merchant Identity Service**|**Kiểm số điện thoại**  <br>• `msisdn` có tài khoản, hoặc `purpose = register` → **sang bước tiếp theo**  <br>• Không có tài khoản → trả thành công như bình thường, không sinh mã, không gửi SMS, **sang bước 9**|person|Cố ý không báo lỗi — chống dò số|
|6|**Merchant Identity Service**|**Sinh mã OTP**  <br>Hủy mã cũ cùng `purpose`; sinh mã 6 số; lưu dạng băm kèm `otp_id`, `purpose`, `msisdn`, hạn hiệu lực, số lượt thử  <br>**Sang bước tiếp theo**|otp_code||
|7|**Merchant Identity Service**|**Gửi SMS chứa mã OTP**  <br>Gọi Notification gửi `MS00001`  <br>• Thành công → **sang bước tiếp theo**  <br>• Thất bại → trả `PIN-503-OTPSEND`, không tính lượt trong ngày, **sang bước 9**  <br>• Timeout → xử lý như Thất bại|notification|Mã lỗi Natcom: Mục 4.3|
|8|**Merchant Identity Service**|**Trả kết quả gửi**  <br>Trả `otp_id`, `expires_in_s`, `resend_after_s`  <br>**Sang bước tiếp theo**|||
|9|**App**|**Tiếp nhận kết quả**  <br>• Thành công → mở NB-0G (hoặc làm mới nếu đang mở): xóa ô nhập, hiện _Resend code {mm:ss}_ đếm ngược theo `resend_after_s`, **sang Luồng 3 · bước 1**  <br>• Thất bại → **sang bước 9a**  <br>• **Không nhận được phản hồi** → app tự gán `PIN-500-SYS`, **sang bước 9a**||Luồng này không tự động thử lại trước khi báo lỗi — khác Luồng 1. Nếu chức năng gọi cần tự thử lại thì tự quy định thêm|
|—||**Luồng dữ liệu rẽ nhánh**|||
|2a|**App**|**Hiện lỗi không có mạng**  <br>Hiện lỗi `PIN-000-OFFLINE`. Đang ở NB-0G → giữ NB-0G, giữ **Resend code** bấm được; chưa mở NB-0G → ở lại màn chức năng gọi  <br>**Kết thúc**||Chưa gửi request — không tính lượt trong ngày|
|9a|**App**|**Hiện lỗi gửi mã**  <br>Hiện lỗi theo mã, xử lý dòng **Resend code** theo mã:  <br>• `PIN-422-OTPLIMIT`: vô hiệu Resend code tới hết ngày  <br>• `PIN-429-OTPWAIT`: đếm ngược theo `Retry-After`, mã cũ vẫn nhập được  <br>• `PIN-503-OTPSEND` / `PIN-500-SYS`: bật Resend code  <br>**Kết thúc**||`PIN-500-SYS` ở đây gộp chung server lỗi thật và không nhận được phản hồi — cùng một hành động (bật Resend code) nên không cần tách|

### 3.2.3. Luồng 3 — Xác thực OTP

|Bước|Đối tượng|Mô tả|Bảng/Thực thể liên quan|Ghi chú|
|---|---|---|---|---|
|—||**Luồng dữ liệu chính**|||
|1|**Người dùng**|**Nhập mã OTP**  <br>Nhập đủ 6 số tại NB-0G, app tự gửi  <br>Bấm nút đóng X → **sang bước 1a**  <br>Nhập đủ 6 số → **sang bước tiếp theo**|||
|2|**App**|**Kiểm kết nối mạng và gọi API xác thực OTP**  <br>• Không có mạng → không gọi API, `PIN-000-OFFLINE`, **sang bước 2a**  <br>• Có mạng → gọi E.1.3 `POST /auth/otp/verify` với `otp_id`, `code`, **sang bước tiếp theo**|||
|3|**Merchant Identity Service**|**Kiểm mã tham chiếu**  <br>• `otp_id` không tồn tại → trả `PIN-404-OTP`, **sang bước 7**  <br>• Tồn tại → **sang bước tiếp theo**|otp_code||
|4|**Merchant Identity Service**|**Kiểm hạn hiệu lực**  <br>• Quá hạn → trả `PIN-422-OTPEXPIRED`, **sang bước 7**  <br>• Còn hạn → **sang bước tiếp theo**|otp_code||
|5|**Merchant Identity Service**|**Kiểm tra mã OTP**  <br>So sánh mã đúng không  <br>• Đúng → **sang bước tiếp theo**  <br>• Sai, còn lượt → trừ một lượt, **giữ mã**, trả `PIN-422-OTPWRONG` kèm `tries_left`, **sang bước 7**  <br>• Sai, hết lượt → hủy mã, trả `PIN-422-OTPLOCKED`, **sang bước 7**|otp_code|Không tính vào bộ đếm sai PIN|
|6|**Merchant Identity Service**|**Cấp verify_token**  <br>Hủy mã (mỗi mã dùng một lần), cấp `verify_token` gắn `purpose`, dùng một lần, hiệu lực `STEPUP_TTL`; trả `200`  <br>**Sang bước tiếp theo**|otp_code||
|7|**App**|**Tiếp nhận kết quả xác thực OTP**  <br>• Thành công → **sang bước 8**  <br>• Thất bại `PIN-422-OTPWRONG` / `PIN-500-SYS` → **sang bước 7a**  <br>• Thất bại `PIN-404-OTP` / `PIN-422-OTPEXPIRED` / `PIN-422-OTPLOCKED` → **sang bước 7b**  <br>• **Không nhận được phản hồi** → app tự gán `PIN-500-SYS`, **sang bước 7a**||Xác thực OTP an toàn để cho nhập lại ngay cả khi không chắc server đã xử lý — chưa tiêu `verify_token` nên không có rủi ro nhân đôi nghiệp vụ|
|8|**App**|**Kiểm kết nối mạng và gọi API nghiệp vụ của chức năng gọi**  <br>• Không có mạng → không gọi API, `PIN-000-OFFLINE`, **sang bước 8a**  <br>• Có mạng → gọi API kèm `verify_token` (vd E.1.7 đặt lại PIN, E.1.5 đăng nhập máy mới), **sang bước tiếp theo**|||
|9|**Merchant Identity Service**|**Kiểm verify_token**  <br>Chữ ký, còn trong `STEPUP_TTL`, `purpose` khớp API, chưa dùng  <br>• Hợp lệ → **sang bước tiếp theo**  <br>• Không hợp lệ → trả `PIN-401-STEPUP`, **sang bước 11**|verify_token_used||
|10|**Merchant Identity Service**|**Tiêu phiếu verify_token và thực hiện nghiệp vụ**  <br>Đánh dấu phiếu đã dùng, trả kết quả  <br>**Sang bước tiếp theo**|verify_token_used|Chống hai request dùng cùng một phiếu|
|11|**App**|**Tiếp nhận kết quả nghiệp vụ**  <br>• Thành công → đóng NB-0G, hiện kết quả nghiệp vụ. **Kết thúc**  <br>• Thất bại `PIN-401-STEPUP` → **sang bước 11a**  <br>• Thất bại khác (kể cả không nhận được phản hồi ở bước 8) → xử lý theo SRS của chức năng gọi — bước 8 đã **tiêu `verify_token`** cùng lúc thực hiện nghiệp vụ nên áp dụng cùng nguyên tắc thận trọng như Luồng 1 · 11c nếu không chắc chắn kết quả|||
|—||**Luồng dữ liệu rẽ nhánh**|||
|1a|**App**|**Đóng bottom sheet**  <br>Không cấp `verify_token`, quay lại trạng thái trước đó. **Kết thúc**|||
|2a|**App**|**Hiện lỗi không có mạng**  <br>Hiện Alert lỗi `PIN-000-OFFLINE`, xóa ô nhập, **giữ nguyên** dòng Resend code và đồng hồ  <br>**Sang bước 1**||Chưa gửi request — không trừ lượt thử|
|7a|**App**|**Hiện lỗi, cho nhập lại**  <br>Hiện lỗi dưới ô nhập theo mã `PIN-422-OTPWRONG` / `PIN-500-SYS`, xóa ô nhập, **giữ nguyên** dòng Resend code và đồng hồ  <br>**Sang bước 1**||An toàn cho nhập lại kể cả khi `PIN-500-SYS` do không nhận được phản hồi — xem ghi chú bước 7|
|7b|**App**|**Hiện lỗi, mã không còn dùng được**  <br>Hiện lỗi theo mã `PIN-404-OTP` / `PIN-422-OTPEXPIRED` / `PIN-422-OTPLOCKED`, xóa và vô hiệu ô nhập, ẩn đồng hồ, bật **Resend code**  <br>**Kết thúc** — bấm Resend code → **Luồng 2 · bước 1**|||
|8a|**App**|**Hiện lỗi không có mạng**  <br>Hiện `Confirmation` dạng Error theo `PIN-000-OFFLINE`, giữ NB-0G; `verify_token` vẫn dùng được trong `STEPUP_TTL`  <br>• Bấm **Try again** → **sang bước 8**  <br>• Bấm **Close** → đóng NB-0G. **Kết thúc**||Hết `STEPUP_TTL` → bước 9 trả `PIN-401-STEPUP`|
|11a|**App**|**Hiện lỗi phiếu hết hiệu lực**  <br>Hiện lỗi theo mã `PIN-401-STEPUP`  <br>**Sang Luồng 2 · bước 1**||Xin mã mới tiêu một lượt trong ngày|

## 3.3. Sơ đồ trạng thái

### 3.3.1. Sơ đồ trạng thái `otp_code`

  

|   |
|---|
|@startuml<br><br>!theme plain<br>!pragma layout smetana<br>skinparam backgroundColor #FFFFFF<br>skinparam StateBorderColor #4A90E2<br>skinparam ArrowColor #333333<br>[*] --> ACTIVE : sinh mã<br>ACTIVE --> ACTIVE : Nhập sai còn lượt<br>ACTIVE --> USED : Nhập đúng - cấp verify_token<br>ACTIVE --> CANCELLED : Nhập sai hết lượt<br>ACTIVE --> CANCELLED : Gửi lại mã<br>ACTIVE --> EXPIRED : Quá OTP_TTL<br>USED --> [*]<br>CANCELLED --> [*]<br>EXPIRED --> [*]<br>@enduml|

  

### 3.3.2. Mô tả chuyển đổi trạng thái

|STT|Trạng thái nguồn|Sự kiện|Trạng thái đích|Bước|
|---|---|---|---|---|
|1|–|Sinh mã mới|`ACTIVE`|Luồng 2 · bước 6|
|2|`ACTIVE`|Nhập sai, còn lượt — trừ một lượt|`ACTIVE`|Luồng 3 · bước 5|
|3|`ACTIVE`|Nhập đúng — cấp `verify_token`|`USED`|Luồng 3 · bước 6|
|4|`ACTIVE`|Nhập sai hết lượt|`CANCELLED`|Luồng 3 · bước 5|
|5|`ACTIVE`|Gửi lại mã cùng `purpose`|`CANCELLED`|Luồng 2 · bước 6|
|6|`ACTIVE`|Quá `OTP_TTL`|`EXPIRED`|Luồng 3 · bước 4|

## 3.4. Bảng / thực thể liên quan

|STT|Thực thể|Mô tả|Trường chính|Thao tác|Ghi chú|
|---|---|---|---|---|---|
|1|person|Danh tính cá nhân|id, msisdn, pin_hash, status|R|Dùng chung `pin_hash` với đăng nhập|
|2|login_lock|Bộ đếm sai PIN và khóa đăng nhập|person_id, failed_count, locked_until|C, R, U|Dùng chung với SRS-CN02. (*) Chưa có trong TSD / DataDict|
|3|auth_session|Phiên đăng nhập|id, person_id, revoked|U|Thu hồi mọi phiên khi sai PIN hết lượt (Luồng 1 · bước 8)|
|4|otp_code|Mã OTP đang hiệu lực|otp_id, purpose, msisdn, code_hash, attempts_left, status, expires_at|C, R, U|(*) Chưa có trong TSD / DataDict — đề xuất lưu Redis, TTL theo `OTP_TTL`|
|5|verify_token_used|Phiếu `verify_token` đã dùng|token_id, used_at, expires_at|C, R|(*) Chưa có trong TSD / DataDict|
|6|notification|SMS đã gửi|id, template_id, target_id, status|C|`MS00001`, `MS00002`|

## 4. Danh sách mã lỗi

## 4.1. Danh mục mã lỗi của chức năng

|STT|Mã lỗi|Tình huống phát sinh|Hành động tiếp theo|
|---|---|---|---|
|1|`PIN-401-PINWRONG`|Sai PIN, còn lượt|Xóa ô PIN, cho nhập lại (Luồng 1 · 11a)|
|2|`PIN-422-PINLOCKED`|Khóa đăng nhập do sai PIN quá số lần; mọi phiên đã bị thu hồi|Đóng NB-0F, hủy hành động, `Confirmation` Error; xóa phiên trên máy, về màn đăng nhập; nút Reset PIN (Luồng 1 · 11b)|
|3|`PIN-422-ACCLOCKED`|Tài khoản đang khóa khẩn|Đóng NB-0F, hủy hành động; nút Call 8686 (Luồng 1 · 11b)|
|4|`PIN-422-OTPLIMIT`|Vượt hạn mức OTP trong ngày|Vô hiệu Resend code tới hết ngày (Luồng 2 · 9a)|
|5|`PIN-429-OTPWAIT`|Gửi lại khi mã còn hiệu lực, chưa đủ thời gian chờ|Đếm ngược theo `Retry-After` (Luồng 2 · 9a)|
|6|`PIN-503-OTPSEND`|Không gửi được SMS OTP|Bật Resend code; không tính lượt (Luồng 2 · 9a)|
|7|`PIN-422-OTPWRONG`|(*) Nhập sai mã OTP, **còn lượt** — mã được giữ|Xóa ô, cho nhập lại (Luồng 3 · 7a)|
|8|`PIN-422-OTPLOCKED`|(*) Nhập sai mã OTP **hết lượt** — mã bị hủy|Vô hiệu ô nhập, bật Resend code (Luồng 3 · 7b)|
|9|`PIN-422-OTPEXPIRED`|Mã OTP quá hạn|Vô hiệu ô nhập, bật Resend code (Luồng 3 · 7b)|
|10|`PIN-404-OTP`|`otp_id` không tồn tại|Vô hiệu ô nhập, bật Resend code (Luồng 3 · 7b)|
|11|`PIN-401-STEPUP`|`verify_token` sai, hết hạn hoặc đã dùng|Quay lại gửi OTP (Luồng 3 · 11a)|
|12|`PIN-500-SYS`|**(*) mở rộng — xem file review.** Lỗi hệ thống MMS thật sự (server trả lỗi), **hoặc** máy vẫn có mạng nhưng app đã gửi request mà không nhận được phản hồi trong thời gian chờ (kể cả sau khi Luồng 1 tự thử lại đủ 3 lần)|Trường hợp server trả lỗi thật: giữ màn, cho thử lại ngay; không tính lượt (Luồng 1 · 11a · Luồng 2 · 9a · Luồng 3 · 7a). Trường hợp **không nhận được phản hồi** ở Luồng 1 sau khi đã tiêu request nghiệp vụ: đóng NB-0F, **không** cho nhập lại ngay, chức năng gọi tự kiểm lại kết quả (Luồng 1 · 11c)|

## 4.2. Mã lỗi phía app (không phải mã server trả về)

|STT|Mã lỗi|Tình huống phát sinh|Hành động tiếp theo|
|---|---|---|---|
|1|`PIN-000-OFFLINE`|App **phát hiện thiết bị không có kết nối mạng** — trước khi gửi request, hoặc phát hiện mất mạng ngay trong lúc chờ phản hồi. **Không dùng** cho trường hợp máy vẫn có mạng nhưng không nhận được phản hồi (dùng `PIN-500-SYS`, Mục 4.1)|Không gọi API, giữ màn và dữ liệu, không tính lượt sai / lượt gửi (Luồng 1 · 4a · Luồng 2 · 2a · Luồng 3 · 2a, 8a)|

# 5. Chức năng ảnh hưởng

||**Kênh thực hiện**|**Chức năng**|**Nội dung ảnh hưởng**|
|---|---|---|---|
|1|App|**CN-01** Đăng ký|Luồng 2, 3 với `purpose = register` — NB-0G dạng màn đầy đủ; API nhận: E.1.4|
|2|App|**CN-02** Đăng nhập|Luồng 2, 3 với `purpose = login_new_device`; dùng chung `pin_hash`, bộ đếm sai PIN, khóa đăng nhập|
|3|App|**CN-03** Quên PIN|Luồng 2, 3 với `purpose = pin_reset`; nút _Forgot PIN?_ trên NB-0F dẫn sang|
|5|App|Thanh toán|Luồng 1 tại E.16.2; lệnh > 5.000 HTG dùng NB-0G với OTP định chế (C.9)|
|6|App|Đổi Tài khoản nhận|Đổi tài khoản nhận chính dùng Luồng 1; liên kết tài khoản dùng NB-0G với OTP định chế (C.2)|