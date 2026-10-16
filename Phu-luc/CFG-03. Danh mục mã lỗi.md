# ![](http://10.254.136.32:8090/plugins/servlet/confluence/placeholder/macro?definition=e3RvY30&locale=en_US&version=2)

**Bảng ghi nhận thay đổi tài liệu**

A – Tạo mới, M – Sửa đổi, D – Xóa bỏ

|   |   |   |   |   |   |
|---|---|---|---|---|---|
|Ngày thay đổi|Vị trí thay đổi|A, M, D|Nguồn gốc|Mô tả thay đổi|Phiên bản|
|14/09/2026|Toàn bộ|A||Tạo mới tài liệu|1.0|

# 1. Quy tắc đặt mã lỗi

Mục này dành cho người **thêm một mã mới** vào danh mục. Đọc xong phải trả lời được ba câu: _có cần mã mới không_ · _đặt tên thế nào_ · _chọn mã HTTP nào_.

## 1.1. Format mã

```
PIN - 422 - OTPEXPIRED
 │     │        └── TAG: nhãn duy nhất, nói CÁI GÌ SAI
 │     └─────────── mã HTTP thực sự trả về
 └───────────────── NƠI SINH RA LỖI (PIN (E1/OB...)
```

## 1.2. Đặt tên `TAG`

|   |   |   |   |
|---|---|---|---|
|#|Quy tắc|Vì sao|Sai → Đúng|
|5|**`TAG` nói CÁI GÌ SAI**, không nói _phải làm gì_|Hành động xử lý có thể đổi; bản chất lỗi thì không. Đặt theo hành động là phải đổi mã mỗi lần đổi UX|`PIN-422-RESENDOTP` _(hành động)_ → `PIN-422-OTPEXPIRED` _(bản chất)_|
|6|**Không nhét tên màn, tên endpoint, tên bảng hay tên biến vào `TAG`**|Cùng một lỗi xuất hiện ở nhiều màn; đổi tên màn hoặc đổi endpoint thì mã vẫn phải đứng yên|`PIN-422-NB02ERR` · `PIN-409-E11REGISTER` → `PIN-422-OTPWRONG` · `PIN-409-PHONETAKEN`|
|7|**Cấu trúc `<đối tượng><trạng thái>`, đọc lên thành câu**|Người đọc log đoán được nghĩa mà không cần tra bảng|`OTP`+`EXPIRED` · `BANK`+`BLOCKED` · `CIN`+`TAKEN` · `LINK`+`REVOKED`|
|8|**Dùng đúng từ vựng ở bảng 1.3, không tự đặt từ đồng nghĩa**|`ACCOUNT` / `ACC` / `WALLET` cho cùng một thứ là cách nhanh nhất để có hai mã trùng nghĩa|`PIN-422-WALLETNOTOK` → `PIN-422-BANKBLOCKED`|
|9|**Không đánh số thứ tự, không dùng mã nội bộ**|Số thứ tự không mang nghĩa, và luôn dẫn tới việc tra bảng mới hiểu|`PIN-422-ERR07` · `PIN-422-E1Q` → `PIN-422-EKYCPHOTO`|
|10|**Không viết tắt tới mức phải đoán**|`TAG` ngắn để gõ nhanh, không phải để đố nhau|`PIN-422-OCRUNRD` → `PIN-422-OCRREAD`|

## 1.3. Từ vựng chuẩn cho `TAG`

|   |   |   |
|---|---|---|
|Nhóm|Từ|Nghĩa|
|**Đối tượng**|`PHONE`|Số điện thoại người dùng|
||`OTP`|Mã xác thực **của Peye-Haiti**|
||`OBOTP`|Mã xác thực **của định chế** — luôn tách khỏi `OTP`|
||`PIN` _(trong TAG)_|Mã PIN 6 số của người dùng. **Không lẫn với tiền tố `PIN-`**|
||`CIN`|Thẻ căn cước|
||`EKYC`|Bước đối chiếu định danh|
||`OCR`|Thông tin đọc được từ thẻ|
||`SHOP`|Gian hàng|
||`BANK`|Tài khoản tại định chế|
||`LINK`|Liên kết tài khoản nhận tiền|
||`ACC`|Tài khoản người dùng trong Peye-Haiti|
||`BILL` · `REMIND`|Bill và nhắc nợ|
||`SMS`|Kênh tin nhắn|
|**Trạng thái**|`WRONG`|Nhập sai|
||`EXPIRED`|Quá hạn|
||`TAKEN`|Đã thuộc về người khác|
||`LOCKED` · `BLOCKED`|Bị khóa _(bên mình)_ · bị chặn _(bên đối tác)_|
||`CLOSED`|Đã đóng, không phục hồi|
||`REVOKED`|Bị thu hồi|
||`LIMIT`|Chạm trần|
||`NOTFOUND`|Không tồn tại|
||`FMT`|Sai định dạng|
||`STATE` · `STAGE`|Sai trạng thái · sai bước trong quy trình|
||`PROCESSING`|Đang xử lý, chưa có kết quả|

## 1.4. Chọn mã HTTP

|   |   |   |
|---|---|---|
||HTTP|Trương hợp|
|1|**400**|Dữ liệu gửi lên **sai định dạng, sai kiểu, thiếu trường, vượt kích thước**|
|2|**401**|**Chưa xác định được người gọi là ai**, hoặc bằng chứng xác thực sai/hết hạn|
|3|**403**|Biết rõ là ai, nhưng **người đó không được phép**|
|4|**404**|Tài nguyên **không tồn tại**, hoặc tồn tại nhưng **không được phép biết là có tồn tại**|
|5|**409**|Yêu cầu hợp lệ nhưng **xung đột với trạng thái hiện có**, hoặc **trùng lệnh đã gửi**|
|6|**422**|Định dạng đúng, quyền đúng, trạng thái đúng — nhưng **một quy tắc nghiệp vụ từ chối**|
|7|**429**|Gọi **quá nhanh hoặc quá nhiều**|
|8|**500**|**Lỗi của chính MMS**|
|9|**503**|**Phụ thuộc bên ngoài** không sẵn sàng — đối tác lỗi, bảo trì, mạch ngắt mở, timeout|

## 1.5. Khi nào cần một mã mới

Trả lời ba câu. **Một câu "có" là đủ để cần mã mới:**

|   |   |   |
|---|---|---|
|#|Câu hỏi|Nếu "có"|
|1|Người dùng có cần đọc **một câu khác** không?|Cần mã mới — vì một mã chỉ có một thông điệp|
|2|App có phải **đi một đường khác** không _(mở màn khác, bật control khác, im lặng thay vì hiện lỗi)_?|Cần mã mới|
|3|Vận hành có cần **đếm riêng** tình huống này không?|Cần mã mới|

**Ba câu đều "không" thì dùng lại mã có sẵn.** Cụ thể:

- **Không tách mã chỉ vì khác màn.** `PIN-422-OTPWRONG` dùng chung cho mọi màn nhập mã của Peye-Haiti.
- **Không tách mã chỉ vì khác endpoint.** `PIN-500-SYS` dùng chung toàn hệ thống.
- **Không tách mã chỉ vì khác nguyên nhân kỹ thuật** nếu người dùng đọc cùng một câu và app đi cùng một đường. `PIN-422-BANKBLOCKED` cố ý gộp _tài khoản phong tỏa_ · _chủ tài khoản không khớp_ · _phiên liên kết bị khóa_ — cả ba đều dừng luồng và đều chỉ tới định chế.

**Ngược lại, hai tình huống trông giống nhau mà tách mã, vì người dùng cần đọc khác nhau:** `PIN-422-OTPWRONG` _(gõ sai)_ và `PIN-422-OTPEXPIRED` _(để quá lâu)_ — cùng dẫn tới bấm **Resend code**, nhưng người dùng cần biết mình sai ở đâu.

# 2. Danh mục mã lỗi 

## 2.0 · `200` — thành công

  

|   |   |   |   |   |
|---|---|---|---|---|
||Mã|Tình huống|Message _(EN — bản nguồn)_|Hành động tiếp theo|
|`PIN-200-PINCHANGED`|200|Đổi PIN thành công, máy chủ đã trả cặp token mới|_Your PIN has been changed. Other devices have been signed out._|

## 2.1 · `400` — dữ liệu vào sai

Nhóm này hiện lỗi **ngay dưới đúng ô nhập**. App kiểm trước tại máy nên phần lớn không bao giờ đi tới server; mã server chỉ xuất hiện khi client cũ hoặc bị can thiệp.

|   |   |   |   |   |
|---|---|---|---|---|
||Mã|Tình huống|Message _(EN — bản nguồn)_|Hành động tiếp theo|
|1|`PIN-400-PHONEFMT`|Số điện thoại sai định dạng|_"Mobile number is invalid"_|Sửa ô số điện thoại|
|2|`PIN-400-PINWEAK`|PIN thuộc danh sách dễ đoán|_"_This PIN is too easy to guess_."_|Nhập PIN khác. **Không** tiêu `verify_token`|
|3|`PIN-400-PINMATCH`|Hai lần nhập PIN không trùng|_"The two PINs do not match."_|Nhập lại. **Không** tiêu `verify_token`|
|4|`PIN-400-AGENT`|Mã nhân viên hỗ trợ không tồn tại|_"We do not know this agent code. Leave it empty if you are not sure."_|Sửa hoặc để trống|
|5|`PIN-400-SHOPNAME`|Thiếu tên gian hàng|_"Your shop needs a name. Buyers see it before they pay."_|Nhập tên gian hàng|
|6|`PIN-400-MARKET`|Mã chợ không tồn tại hoặc chưa chọn|_"Choose your city and market."_|Chọn lại. Xảy ra khi danh mục trên máy đã cũ|
|7|`PIN-400-ACCOUNT`|Số tài khoản sai định dạng của ngân hàng đã chọn|_"Check the account number — {bank} numbers have {digits} digits."_|Sửa số tài khoản, **giữ** ngân hàng đã chọn|
|8|`PIN-400-PHOTO`|Ảnh sai kiểu tệp hoặc vượt kích thước|_"That photo did not upload. Take it again."_|App tự nén lại và tải lên lại; hiện thông điệp khi vẫn thất bại|
|9|`PIN-400-RANGE`|Khoảng thời gian vượt giới hạn của định chế|**—** _(im lặng)_|MMS tự chia nhỏ khoảng rồi gọi lại|
|10|`PIN-400-VAL`|**Mã dự phòng** — trường vi phạm chưa có mã riêng|_"Something in this form is not right. Check the highlighted field."_|**Mã này xuất hiện trong thống kê nghĩa là thiếu mã** — phải bổ sung một mã riêng cho trường đó|

## 2.2 · `401` — xác thực

|   |   |   |   |   |
|---|---|---|---|---|
||Mã|Tình huống|Message _(EN — bản nguồn)_|Hành động tiếp theo|
|1|`PIN-401-EXPIRED`|Token truy cập hết hạn|**—**|App làm mới token **ngầm một lần** rồi gọi lại yêu cầu gốc. **Không** hiện lỗi, **không** hỏi PIN|
|2|`PIN-401-NEWDEVICE`|PIN đúng nhưng thiết bị chưa từng đăng nhập|**—**|App **tự** chuyển sang màn nhập mã xác thực thiết bị mới|
|3|`PIN-401-REAUTH`|Hết chu kỳ xác thực lại|_"Routine check. Enter your PIN to continue. Nothing is wrong with your account."_|Nhập PIN đúng → **quay lại đúng chỗ đang làm dở**. **Không** làm mới ngầm, **không** xóa phiên|
|4|`PIN-401-PINWRONG`|Sai PIN|_"Wrong PIN — {tries_left} tries left."_|Cho nhập lại. Hết lượt → `PIN-422-PINLOCKED`|
|5|`PIN-401-STEPUP`|`verify_token` sai, hết hạn hoặc đã dùng|_"That took a while. We need to confirm your number again."_|Mở lại màn nhập mã OTP. **Nói rõ xin mã mới sẽ tiêu một lượt trong ngày**|
|6|`PIN-401-SESSION`|Refresh token sai, hết hạn hoặc đã thu hồi|_"You have been signed out. Sign in again to continue."_|Về màn đăng nhập, **xóa phiên trên máy**, giữ số điện thoại đã lưu|
|7|`PIN-401-JWS`|Chữ ký thẻ hệ thống lệch hoặc thiếu|**—** _(không bao giờ tới app)_|Kênh máy-máy. Cảnh báo vận hành, mở mạch ngắt|

## 2.3 · `403` · `404` — quyền và không tìm thấy

|   |   |   |   |   |
|---|---|---|---|---|
||Mã|Tình huống|Message _(EN — bản nguồn)_|Hành động tiếp theo|
|1|`PIN-403-SCOPE`|Đúng danh tính, thiếu quyền|_"You do not have access to this."_|Chủ yếu ở portal. Trên app xuất hiện là dấu hiệu client cũ — ghi log cảnh báo|
|2|`PIN-404-PERSON`|Số điện thoại chưa có tài khoản|_"We could not find an account for this number."_|Hai lối ra: **Try another number** và **Sign up**. **Không** nói số đó có ở đâu khác|
|3|`PIN-404-OTP`|Mã tham chiếu OTP _(`otp_id`)_ không tồn tại|_"This code is no longer valid. Tap Resend code to get a new one."_|Bật ngay control **Resend code**|
|4|`PIN-404-LINK`|Phiên liên kết tài khoản không tồn tại hoặc quá hạn|_"This step timed out. Choose where you want the money again."_|Về màn chọn nơi nhận tiền. **Không** giữ số tài khoản đã nhập|
|5|`PIN-404-NF`|**Mã dự phòng** — tài nguyên khác không tồn tại|_"We could not find what you were looking for."_|Chống dò: **không** phân biệt _không có_ với _không được xem_|

## 2.4 · `409` — trùng lệnh và sai trạng thái

|   |   |   |   |   |
|---|---|---|---|---|
||Mã|Tình huống|Message _(EN — bản nguồn)_|Hành động tiếp theo|
|`PIN-409-PROCESSING`|Trùng khóa khử trùng, **cùng nội dung đang xử lý**|**—** _(im lặng)_|App **giữ nguyên khóa khử trùng** và thử lại theo `Retry-After`. **Tuyệt đối không sinh khóa mới**|
|`PIN-409-IDEM`|Trùng khóa khử trùng, **nội dung khác**|_"Something went wrong on our side. Try again in a few minutes."_|Lỗi cấu hình client — ghi log cảnh báo kèm `trace_id`|
|`PIN-409-PHONETAKEN`|Số điện thoại **đã có** tài khoản|_"This number already has a Peye-Haiti account."_|Kèm hai liên kết: **Sign in** và **Reset PIN**. **Không** tạo hồ sơ mới|
|`PIN-409-SHOP`|Đã có gian hàng ở trạng thái khác `draft`|_"Your shop is already set up."_|Đưa về màn trạng thái hồ sơ hoặc Trang chủ vai BÁN **theo trạng thái thực tế**|
|`PIN-409-EKYCSTAGE`|Hồ sơ không ở trạng thái cho phép tải ảnh|_"We are already checking your photos. We will let you know as soon as it is done."_|Về màn trạng thái hồ sơ|
|`PIN-409-CINTAKEN`|Số CIN đã thuộc `person` khác|_"We cannot use this ID card. Call 8686 for support."_|Nút gọi 8686. **Cố ý không nói vì sao** — xem CC-E3|
|`PIN-409-STATE`|**Mã dự phòng** — sai trạng thái ở luồng khác|_"This has already been done."_|Làm mới màn rồi thử lại|
|`PIN-409-LINKBUSY`|Lệnh xác nhận liên kết đã gửi ra định chế, **chưa biết kết quả** — hệ thống đang tự thử lại|_"We are completing the link, we will update the result."_|**NB-2D** vào trạng thái _đang xử lý_: khóa ô nhập OTP, khóa **Resend**, khóa **Confirm and activate**, khóa **Choose another account**. Server **từ chối** mọi lệnh tạo liên kết mới của gian hàng này.<br><br>**Khác** `PIN-409-PROCESSING`: mã kia **im lặng** và app tự thử lại ngầm; mã này **có thông điệp** vì người bán đang đứng nhìn màn hình.|

## 2.5 · `422` — nghiệp vụ _(thay toàn bộ họ `BIZ-*` của bản 1.x)_

### Xác thực và tài khoản

|   |   |   |   |   |
|---|---|---|---|---|
||Mã|Tình huống|Message _(EN — bản nguồn)_|Hành động tiếp theo|
|`PIN-422-OTPWRONG`|**Nhập sai** mã OTP Peye-Haiti, **còn lượt** thử — mã được giữ|_"Wrong code — {tries_left} tries left."_|Xóa ô nhập, **giữ** đồng hồ Resend code, cho nhập lại ngay. `{tries_left}` lấy từ server. Hết `OTP_MAX_ATTEMPTS` → `PIN-422-OTPLOCKED`. Xem COMMON-01 · Luồng 3 · 7a|
|`PIN-422-OTPLOCKED`|Nhập sai mã OTP Peye-Haiti **hết lượt** — mã bị hủy|_"Too many wrong tries. This code no longer works — tap Resend code to get a new one."_|Xóa và vô hiệu ô nhập, ẩn đồng hồ, **bật ngay** **Resend code**. Xem COMMON-01 · Luồng 3 · 7b|
|`PIN-422-OTPEXPIRED`|Mã OTP Peye-Haiti **quá hạn**|_"That code has expired. Tap Resend code to get a new one."_|Cùng lối ra với 30 nhưng **khác câu**: người dùng cần biết mình gõ sai hay để quá lâu|
|`PIN-422-OTPLIMIT`|Vượt hạn mức OTP trong ngày|_"You have asked for too many codes today. Try again tomorrow."_|Chặn gửi thêm trong ngày. Hạn mức đếm **chung cho cả bốn mục đích**|
|`PIN-422-PINLOCKED`|Khóa đăng nhập do sai PIN quá số lần|_"Sign-in is locked for your safety. Try again in {countdown}, or reset your PIN with an SMS code."_|Hai lối ra: chờ hết giờ, hoặc đặt lại PIN bằng mã SMS. **Tài khoản vẫn hoạt động bình thường**|
|`PIN-422-ACCLOCKED`|Tài khoản đang bị khóa khẩn|_"Your account is locked to keep it safe. Call 8686 for support."_|**Không** dùng được luồng đặt lại PIN. Chỉ qua hotline|
|`PIN-422-ACCCLOSED`|Tài khoản đã đóng|_"This account is closed."_|**Không có đường tự phục hồi trong app**|
|`PIN-422-PINREUSED`|PIN mới trùng với PIN hiện tại|_"Choose a PIN you have not used before."_|`Inlineerror` dưới ô **New PIN**. **Không** tiêu `verify_token` — người dùng nhập PIN khác và gửi lại trong `STEPUP_TTL`. Server là nơi **duy nhất** kiểm được quy tắc này _(app không có PIN cũ)_.|
|PIN-422-EKYCLIMIT|Chạm trần `EKYC_RETAKE_MAX` vòng chụp lại mà vẫn không đối chiếu được|_"We could not verify your ID card, retry after {retry_after_hours} hours"_|**Chặn chụp tiếp.**|
|PIN-422-BANKBLOCKED|Tài khoản bị phong tỏa, **hoặc** chủ tài khoản không khớp, **hoặc** phiên liên kết bị khóa|_"We cannot link this account right now. Contact {bank}, then try again."_|Dừng luồng liên kết. **Cố ý không phân biệt ba nguyên nhân** — nói rõ _“tên không khớp”_ sẽ thành kênh dò thông tin tài khoản. Hồ sơ **giữ nguyên** trạng thái dở dang, gian hàng không bị hủy.|

### Gian hàng và tài khoản nhận tiền

|   |   |   |   |   |
|---|---|---|---|---|
||Mã|Tình huống|Message _(EN — bản nguồn)_|Hành động tiếp theo|
|1|`PIN-422-EKYCFIRST`|Khai gian hàng hoặc liên kết tài khoản khi định danh chưa đạt|_"Confirm your identity first, then you can add your account."_|Về màn trạng thái hồ sơ. **Không** áp cho liên kết nguồn trả của vai MUA|
|2|`PIN-422-PROFILE`|Gọi chức năng bán hàng khi hồ sơ còn dở dang|_"Finish setting up your shop to use this. {steps_left} step left."_|Nút **Continue** mở màn trạng thái hồ sơ. **Chức năng thanh toán vai MUA vẫn dùng được**|
|3|`PIN-422-SHOPHOLD`|Gian hàng bị tạm khóa hoặc đã đóng|_"Your shop is on hold. You can still look around, but not take payments yet."_|**Vẫn cho đăng nhập**, vào app chế độ chỉ đọc|
|4|`PIN-422-LINKGRACE` **(*) MỚI · 16/10**|Hủy một liên kết đang trong ân hạn (`grace`) sau khi đổi tài khoản nhận|_"This account still receives money from your old QR. It will be removed automatically after you put up the new standee and the grace period ends."_|`Confirmation` dạng Error, về NB-16A. **Không** cho hủy trực tiếp — liên kết `grace` chỉ chuyển `revoked` qua JOB của CN-07 khi hết `OLD_LINK_GRACE` **và** `standee_order.status = mounted`|

### Bán hàng, sổ nợ và portal

|   |   |   |   |   |
|---|---|---|---|---|
||Mã|Tình huống|Message _(EN — bản nguồn)_|Hành động tiếp theo|
|1|`PIN-422-BILLSTATE`|Bill không ở trạng thái hợp lệ cho thao tác|_"This bill is already closed."_|Làm mới danh sách bill|
|2|`PIN-422-REMINDLIMIT`|Quá hạn mức nhắc nợ trong ngày|_"You already sent a reminder to this customer today. You can send another one {next_allowed}."_|Chờ tới mốc cho phép|
|3|`PIN-422-DUPUUID`|Trùng `client_uuid` nhưng nội dung khác _(đồng bộ ngoại tuyến)_|**—** _(im lặng)_|App giữ bản ghi cũ, ghi log. **Không làm phiền người dùng bằng lỗi đồng bộ**|
|4|`PIN-422-REFCONFLICT`|Dedup tầng hai — nghi lệch dữ liệu|**—** _(không tới app)_|Mở phiếu lệch dữ liệu cho đội đối soát|
|5|`PIN-422-FOUREYES`|Nguyên tắc bốn mắt — người duyệt trùng người tạo|_"You cannot approve something you created. Ask a colleague to review it."_|**Portal**, không phát sinh trên app|
|6|`PIN-422-REASON`|Thiếu lý do bắt buộc cho một quyết định|_"Add a reason before you save this decision."_|**Portal**. Hệ thống **chặn** lưu — AC-6.1|
|7|`PIN-422-REFUNDUNVER`|Kết luận _"đã hoàn"_ khi chưa xác minh|_"We cannot mark this as refunded until the transfer is verified."_|**Portal** — AC-7.1|
|8|`PIN-422-SMSUNREACH`|Không gửi được SMS tới số này — số không tồn tại hoặc bị chặn|_"We could not reach this number by SMS. Check it, or ask a field agent for help."_|Kiểm tra lại số, hoặc nhờ nhân viên hiện trường. **Không** thử lại tự động|
|9|`PIN-422-OCRREVERIFY`|_(hoãn)_ Người bán sửa thông tin định danh, cần đối chiếu lại|_(chưa viết)_|**Đã đặc tả nhưng hoãn thi hành** — chỉ cần khi mở lại đường tự sửa, xem CC-10 của SRS-CN01|

## 2.6 · `429` · `5xx` — tần suất và hạ tầng

|   |   |   |   |   |
|---|---|---|---|---|
||Mã|Tình huống|Message _(EN — bản nguồn)_|Hành động tiếp theo|
|1|`PIN-429-OTPWAIT`|Bấm gửi lại mã khi mã còn sống|_"You can ask for a new code in {countdown}."_|Vô hiệu **Resend code**, chạy đồng hồ theo `Retry-After`. **Thông điệp phải trung tính**|
|2|`PIN-429-RATE`|Vượt hạn mức tần suất chung|_"Too many tries. Wait a few minutes and try again."_|Chờ theo `Retry-After`|
|3|`PIN-500-SYS`|Lỗi hệ thống phía MMS (server trả lỗi), **hoặc** máy vẫn có mạng nhưng app đã gửi request mà **không nhận được phản hồi** trong thời gian chờ — trường hợp này do app tự gán|_"System busy. Try again in a few minutes."_|Có tự thử lại trước khi hiện hay không, và có cho thao tác lại ngay hay không: theo **COMMON-01 Mục 4.1** và SRS của từng luồng. Hồ sơ đang dở **không bị hủy**|
|4|`PIN-503-OTPSEND`|Không gửi được mã OTP|_"We could not send the code right now. Try Resend."_|**Không** tiêu thêm lượt gửi trong ngày cho lần thất bại này|
|5|`PIN-503-EKYC`|Dịch vụ đối chiếu định danh không sẵn sàng|_"We could not check your identity right now. Try again in a few minutes."_|**Người dùng tự bấm thử lại.** Ảnh giữ nguyên, **không** tiêu vòng chụp lại nào|
|6|`PIN-503-BANK`|Định chế bận hoặc bảo trì|_"Your provider is busy right now. Try again in a few minutes."_|Hồ sơ giữ nguyên trạng thái dở dang|
|7|`PIN-503-DEP`|**Mã dự phòng** — phụ thuộc khác không sẵn sàng|_"This is not available right now. Try again in a few minutes."_|–|
|8|`PIN-000-UNKNOWN`|**Không phải mã server trả về** — app tự dùng khi gặp mã lạ|_"Something did not work. Try again, or call 8686 if it keeps happening."_|**Luôn ghi log cảnh báo kèm `trace_id`.** Xuất hiện trong thống kê nghĩa là có mã chưa khai báo|
|9|`PIN-000-OFFLINE`|**Không phải mã server trả về** — app tự dùng khi **phát hiện thiết bị không có kết nối mạng** (trước khi gửi, hoặc mất mạng ngay trong lúc chờ). **Không** dùng cho trường hợp máy vẫn có mạng mà không nhận được phản hồi — trường hợp đó là `PIN-500-SYS`. Xem COMMON-01 Mục 4.2|_"No connection — please try again."_|**Giữ nguyên** phiên, token và dữ liệu trên máy; người dùng thử lại khi có mạng|

## 2.7 · Đối chiếu định danh

||Mã|Tình huống|Message _(EN — bản nguồn)_|Hành động tiếp theo|
|---|---|---|---|---|
|1|`E1-422-QUALITY`|Một ảnh không đạt chuẩn — BRH **chỉ rõ ảnh nào**|_"One photo was not clear enough. Take {photo} again — the others are fine."_|Về **đúng màn camera của ảnh đó**. Hai ảnh còn lại giữ nguyên. Đếm một vòng|
|2|`E1-422-LOWSCORE`|Khớp nhưng `score < AUTO_ACTIVATE_SCORE`|_"We could not match your photos with your ID card closely enough. Take them again in better light."_|Chụp lại **cả ba** ảnh. **Không** nói cho người dùng biết có điểm số|
|3|`E1-422-NOMATCH`|`matched = false`|_"We could not match your photos with your ID card. Take them again."_|Chụp lại cả ba. Khác câu với 54 — người dùng cần biết là không khớp hẳn chứ không phải ảnh hơi mờ|
|4|`E1-404-CIN`|Không đối chiếu được số CIN với dữ liệu định danh quốc gia|_"We could not verify this ID card. Make sure the whole card is visible, then take the photos again."_|Chụp lại cả ba. **Cố ý không nói số CIN không tồn tại**|
|5|`E1-422-OCRREAD`|Không đọc được một trong **tám trường bắt buộc**|_"We could not read {field} on your card. Take the photos again."_|**Vô hiệu** nút xác nhận. Đường duy nhất là **Retake photos**|
|6|`E1-500-NOOCR`|BRH trả kết quả khớp nhưng **thiếu hẳn khối tám trường**|_"We could not check your identity right now. Try again in a few minutes."_|**Lỗi dịch vụ, không phải lỗi ảnh** — cảnh báo vận hành **ngay lần đầu**, **không** đếm vòng. Xem CC-2 của SRS-CN01|
|7|`E1-400-VAL`|Đường dẫn ảnh hết hạn hoặc sai format|**—** _(im lặng nếu thử lại thành công)_|MMS sinh lại đường dẫn và gọi lại **một lần**; vẫn hỏng thì rơi về 62|
|8|`E1-401-AUTH`|mTLS / JWT sai|_"We could not check your identity right now. Try again in a few minutes."_|Cảnh báo vận hành, **không** thử lại|
|9|`E1-429-RATE`|Vượt hạn ngạch gọi BRH|_"We could not check your identity right now. Try again in a few minutes."_|Giãn cách rồi thử lại|
|10|`E1-500-SYS`|Dịch vụ đối chiếu lỗi nội bộ|_"We could not check your identity right now. Try again in a few minutes."_|**Người dùng tự bấm thử lại.** Ảnh giữ nguyên, **không** tiêu vòng chụp lại nào|
|11|`E1-503-DOWN`|Dịch vụ đối chiếu bảo trì, hoặc timeout|_"We could not check your identity right now. Try again in a few minutes."_|Như 62|

## 2.8 · Open Banking

Toàn bộ nhóm này phát sinh ở bước liên kết tài khoản nhận tiền. **Điểm chung:** hồ sơ **luôn giữ nguyên** trạng thái dở dang — gian hàng không bị hủy vì một lần liên kết hỏng.

||Mã|Tình huống|Message _(EN — bản nguồn)_|Hành động tiếp theo|
|---|---|---|---|---|
|1|`OB-400-VAL`|Request của MMS sai format — **bug connector của mình**|_"Something went wrong on our side. Try again in a moment."_|Cảnh báo vận hành **ngay lần đầu**. Tiền tố `OB-` vì lỗi chỉ nhìn thấy được ở lời gọi OB|
|2|`OB-401-AUTH`|mTLS hoặc thẻ hệ thống của MMS sai|_"Your provider is busy right now. Try again in a few minutes."_|Cảnh báo vận hành, **không** thử lại|
|3|`OB-401-EXPIRED`|Token truy cập của liên kết hết hạn|**—** _(trong suốt)_|MMS tự gia hạn rồi thử lại **đúng một lần**. App không thấy gì|
|4|`OB-401-REVOKED`|Token liên kết bị định chế thu hồi|_"The link to your account has stopped working. Link it again to keep receiving money."_|Nút **Link again**. Ghim cho tới khi liên kết lại xong — đây là lỗi làm gian hàng **mất tiền về**|
|5|`OB-403-SCOPE`|Token thiếu phạm vi|_"Your provider is busy right now. Try again in a few minutes."_|Cảnh báo vận hành|
|6|`OB-404-ACC`|Số ví hoặc số tài khoản không tồn tại tại định chế|_"We could not find this account at {bank}. Check the number and try again."_|Cho nhập lại, **giữ** ngân hàng đã chọn|
|7|`OB-404-LINK`|`link_id` **phía định chế** không tồn tại hoặc quá hạn khởi tạo _(≥ 15 phút)_|_"This step timed out. Choose where you want the money again."_|Về màn chọn nơi nhận tiền. **Không lẫn với `PIN-404-LINK`**|
|8|`OB-409-IDEM`|`Idempotency-Key` trùng lần gọi trước nhưng `otp` gửi lên khác|_"Something went wrong on our side. Try again in a moment."_|Lỗi cấu hình phía MMS — ghi log cảnh báo kèm `trace_id`|
|9|`OB-409-STATE`|Trạng thái liên kết phía định chế không hợp lệ|_"This has already been done."_|Làm mới màn, hoặc làm lại từ màn chọn nơi nhận tiền|
|10|`OB-422-KYC`|Thông tin định danh gửi kèm **không khớp chủ tài khoản**|_"The name on this account does not match your ID. Call 8686 and we will help you."_|Dừng luồng liên kết. **Không** nêu tên định chế, **không** nói rõ trường nào lệch|
|11|`OB-422-OTP`|Sai mã OTP **của định chế**, hoặc mã đã hết hạn|_"Wrong code — {tries_left} tries left."_|Số lượt do **định chế** quy định. **Khác hẳn mã 30 — có chủ đích**, xem CC-E2|
|12|`OB-422-RANGE`|Khoảng thời gian vượt giới hạn của định chế|**—** _(im lặng)_|MMS tự chia nhỏ khoảng rồi gọi lại|
|13|`OB-423-LOCK`|Tài khoản phong tỏa, hoặc liên kết bị khóa do vượt số lần sai tối đa|_"We cannot link this account right now. Contact {bank}, then try again."_|Dừng luồng liên kết. **Cố ý không phân biệt hai nguyên nhân**|
|14|`OB-429-OTPWAIT`|Bấm gửi lại OTP **của định chế** trước mốc cho phép|_"You can ask for a new code in {countdown}."_|Vô hiệu nút gửi lại, chạy đồng hồ theo `Retry-After`. Đổi tên từ `OB-429-OTP` — xem CC-E10|
|15|`OB-429-OTPLIMIT`|Vượt số lần gửi OTP trong một đơn vị thời gian **của định chế**|_"You have asked for too many codes. Try again later, or contact {bank}."_|**Dừng luồng liên kết.** Đổi tên từ `OB-429-OTP-LIMIT` _(bốn đoạn)_ — xem CC-E10|
|16|`OB-429-RATE`|Định chế giới hạn tần suất gọi chung|_"Too many tries. Wait a moment and try again."_|Chờ theo `Retry-After`|
|17|`OB-500-SYS`|Định chế lỗi hệ thống nội bộ|_"Your provider is busy right now. Try again in a few minutes."_|Hồ sơ giữ nguyên trạng thái dở dang. MMS retry có `Idempotency-Key`, timeout mặc định **10 giây**|
|18|`OB-503-DOWN`|Định chế bảo trì, hoặc mất kết nối giữa chừng|_"Your provider is busy right now. Try again in a few minutes."_|Như 80. Định chế bảo đảm khử trùng _(TTL ≥ 48h)_ để **không cấp lặp token**|