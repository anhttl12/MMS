  
![](http://10.254.136.32:8090/plugins/servlet/confluence/placeholder/macro?definition=e3RvY30&locale=en_US&version=2)

**BẢNG GHI NHẬN THAY ĐỔI**

|   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|
|Ngày|Vị trí|A/M/D|Nguồn gốc|PB cũ|Mô tả thay đổi|PB mới|
|08/09/2026|Toàn bộ|A||—|Thêm mới|1.0|

---

## 1. DANH MỤC THAM SỐ

Cột **Khoảng hợp lệ** là ràng buộc hệ thống phải kiểm khi lưu — ngoài khoảng thì từ chối với `PIN-400-VAL`.

### 1.1. Nhóm phiên đăng nhập & xác thực lại

|   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|
|Tên tham số|Giá trị mặc định|Kiểu|Khoảng hợp lệ|Trả lời câu hỏi|Ý nghĩa nghiệp vụ|Dùng ở đâu|
|#### `ACCESS_TOKEN_TTL`|15 phút|duration (phút)|5 – 60|thời hạn hiệu lực token là bao lâu?|Thời gian một access token còn được server chấp nhận. Hết hạn thì app **tự gia hạn ngầm** (silent refresh), người dùng không thấy gì. <br><br>**Tăng** ⇒ nhẹ mạng 2G nhưng token bị lộ dùng được lâu hơn và khóa khẩn chậm có hiệu lực, có thể vượt mốc 60 giây của AC-10.1. <br><br>**Giảm** ⇒ thu hồi phiên nhanh nhưng gọi gia hạn dày, tốn dữ liệu và pin trên máy giá rẻ|CN-02 ,`CN-01`, `CN-03`, `CN-05`|
|#### `REFRESH_TOKEN_TTL`|30 ngày|duration (ngày)|7 – 90|Thiết bị này còn được coi là đã đăng nhập trong bao lâu?|Tuổi thọ của phiên. Hết hạn ⇒ người dùng đăng nhập lại **từ đầu** và hệ thống tạo phiên mới. <br><br>**Tăng** ⇒ ít phải đăng nhập lại, nhưng **chưa có chức năng đăng xuất** nên phiên dài là rủi ro thật khi cho người khác dùng máy. <br><br>**Giảm** ⇒ hay phải nhập lại số điện thoại và PIN, bất lợi với người bán ít dùng smartphone|CN-02 ,`CN-01`, `CN-03`, `CN-05`|
|#### `PIN_REAUTH_INTERVAL`|7 ngày|duration (ngày)|1 – 30|Tối đa bao lâu không nhập PIN thì bị hỏi lại?|**Re-authentication interval** (khoảng thời gian tái xác thực) là khoảng thời gian quy định mà sau đó hệ thống sẽ yêu cầu người dùng hoặc thiết bị phải đăng nhập hoặc xác thực lại danh tính để tiếp tục duy trì quyền truy cập vào ứng dụng<br><br>— mốc tuyệt đối tính từ `auth_time`. Quyết định bao lâu thì màn nhập PIN bật ra dù phiên vẫn còn.<br><br>Mọi lần con người nhập PIN hoặc OTP đều đặt lại mốc này; **gia hạn ngầm thì không**.<br><br> **Tăng** ⇒ gần như không thấy màn xác thực lại, nhưng máy mất mà phiên còn hạn thì người lạ dùng được các chức năng không cần xác thực lâu hơn. <br><br>**Giảm** ⇒ thấy màn PIN thường xuyên, mất tính đăng nhập nhanh.<br><br>**Khi mất mạng**: còn trong hạn thì **app mở được** dù không gọi được server; vượt hạn thì chặn hẳn, không vào được app. Vì vậy tham số này cũng là **thời gian tối đa một máy offline còn dùng được app** — và là mốc duy nhất giới hạn việc đọc dữ liệu cục bộ trên máy bị mất|CN-02, COMMON-01|
|#### `STEPUP_TTL`|10 phút|duration (phút)|1 – 30|Step-up token sống bao lâu?|Tuổi thọ `verify_token` cấp sau khi xác thực lại cho một hành động.<br><br>Token **dùng một lần**, nên tham số này chỉ là thời gian tối đa từ lúc xác thực xong tới lúc hành động chạm server.<br><br> **Tăng** ⇒ token treo lâu hơn, cửa sổ lạm dụng rộng hơn.<br><br> **Giảm** ⇒ mạng chợ chậm làm token hết hạn trước khi hành động tới server, người dùng phải nhập PIN lại mà không hiểu vì sao; **không nên đặt dưới 3 phút** ở điều kiện pilot|COMMON-01|
|#### `STEPUP_AMOUNT_THRESHOLD`|5000|số tiền (HTG)|0 – 100.000|Bao nhiêu tiền thì cần thêm OTP, không chỉ PIN?|Ngưỡng nâng yêu cầu xác thực từ PIN lên PIN + OTP cho hành động **có số tiền**.<br><br>Tham số này **chỉ áp cho hành động có số tiền**. Hành động không có số tiền tự quy định bậc xác thực trong SRS của mình — đổi tài khoản nhận tiền _(CN-07)_ và hủy liên kết _(CN-08)_ **chỉ cần PIN** theo COMMON-01 · Luồng 1.<br><br> **Tăng** ⇒ ít SMS, tiết kiệm chi phí và đỡ cạn `OTP_MAX_PER_DAY`, nhưng khoản lớn chỉ cần PIN. <br><br>**Giảm** ⇒ nhiều thao tác cần OTP, rất dễ cạn hạn mức OTP trong ngày|COMMON-01|

**Ràng buộc kiểm chéo — phải kiểm khi lưu, không chỉ kiểm từng khoảng riêng lẻ:**

- `ACCESS_TOKEN_TTL` < `REFRESH_TOKEN_TTL`
- `PIN_REAUTH_INTERVAL` ≤ `REFRESH_TOKEN_TTL` — lớn hơn thì phiên hết trước, mốc xác thực lại vô nghĩa
- `ACCESS_TOKEN_TTL` phải đủ nhỏ để khóa khẩn có hiệu lực trong **60 giây** theo AC-10.1. Nếu muốn đặt lớn thì phải bổ sung danh sách đen token — hiện chưa có trong đặc tả

### 1.2. Nhóm mã PIN & khóa đăng nhập

|   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|
|Tên tham số|Giá trị mặc định|Kiểu|Khoảng hợp lệ|Trả lời câu hỏi|Ý nghĩa nghiệp vụ|Dùng ở đâu|
|#### `PIN_MAX_ATTEMPTS`|5|int|3 – 10|Sai PIN mấy lần thì khóa đăng nhập?|Số lần sai PIN liên tiếp trước khi khóa đăng nhập.<br><br>Đếm theo `person`, **dùng chung** giữa màn đăng nhập và step-up, màn đổi PIN<br><br>Đếm reset về 0 khi đăng nhập thành công hoặc đặt lại PIN/ _đổi PIN thành công_<br><br>**Tăng** ⇒ người bán nhớ PIN kém ít bị khóa oan, nhưng kẻ dò có nhiều lượt hơn.<br><br> **Giảm** ⇒ chặn dò tốt hơn, nhưng vì đếm theo `person` nên người lạ biết số điện thoại có thể khóa tài khoản người khác từ xa quá dễ|CN-02<br><br>COMMON-01<br><br>CN-05|
|#### `PIN_LOCK_DURATION`|60 phút|duration (phút)|15 – 240|Khóa đăng nhập bao lâu?|Thời gian khóa đăng nhập sau khi sai đủ `PIN_MAX_ATTEMPTS` lần.<br><br>Là **nguồn của biến** `{minutes}` trong mẫu tin `MS00002` · `LOGIN_LOCK` <br><br>Trong thời gian này người dùng **vẫn vào được luồng đặt lại PIN bằng OTP**.<br><br>**Tăng** ⇒ chặn dò lâu, nhưng khóa oan làm người bán mất giờ buôn bán.<br><br>**Giảm** ⇒ nhanh quay lại bán hàng, nhưng kẻ dò chờ hết giờ là có thêm lượt; **dưới 15 phút thì cơ chế khóa gần như mất tác dụng**|CN-02, `CN-01`, `CN-03,` `CN-05`|

**Lưu ý mô hình dữ liệu:** khóa do sai PIN **không** làm đổi `person.status`. `person.status` chỉ có `Active` / `Locked` / `Terminated`; trạng thái khóa đăng nhập lưu ở thực thể `login_lock` riêng. Xem `PEYE-HT-2026-SRS-CN02` · Mục 4.

### 1.3. Nhóm OTP

|   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|
|Tên tham số|Giá trị mặc định|Kiểu|Khoảng hợp lệ|Trả lời câu hỏi|Ý nghĩa nghiệp vụ|Dùng ở đâu|
|#### `OTP_TTL`|120 giây|duration (giây)|60 – 300|Mã OTP còn dùng được bao lâu?|Hiệu lực một mã OTP, tính từ lúc phát sinh. **Không** phải mốc cho phép gửi lại mã — đồng hồ **Resend code** đếm từ `OTP_RESEND_AFTER`. Hết đồng hồ Resend mà mã còn trong `OTP_TTL` thì mã vẫn nhập được<br><br>**Tăng** ⇒ vùng sóng yếu có thời gian nhận và nhập, nhưng cửa sổ đọc lỏm mã dài hơn.<br><br>**Giảm** ⇒ cửa sổ tấn công ngắn, nhưng SMS qua 2G vùng sâu có thể tới sau khi mã đã hết hạn; **không nên đặt dưới 90 giây** ở điều kiện pilot|CN-02 · 3.3 · CN-03 · COMMON-01|
|#### `OTP_RESEND_AFTER`|60 giây|duration (giây)|30 – `OTP_TTL`|Mã còn sống thì phải chờ bao lâu mới được xin mã mới?|Thời gian chờ tối thiểu, tính từ lúc gửi mã, trước khi được bấm **Resend code** khi mã hiện tại **còn hiệu lực**. Bấm sớm hơn thì server trả `PIN-429-OTPWAIT`.  <br>  <br>**Không áp khi mã đã bị hủy** (nhập sai, hết hạn) — lúc đó nút gửi lại bật ngay.  <br>  <br>**Tăng** ⇒ ít SMS thừa, đỡ tiêu `OTP_MAX_PER_DAY`, nhưng người dùng vùng sóng yếu chờ lâu khi SMS không tới.  <br>  <br>**Giảm** ⇒ bấm gửi lại liên tục khi SMS đến chậm, dễ cạn hạn mức trong ngày và tạo nhiều mã song song|CN-01 · 2.2.2, 3.2.1 (nhánh 8a) · CN-02 · 3.3|
|#### `OTP_MAX_PER_DAY`|5 lần/số/ngày|int|3 – 10|Một số điện thoại được nhận bao nhiêu OTP mỗi ngày?|Hạn mức chống lạm dụng SMS. **Hiện đếm tổng cho cả 4 mục đích** `login_new_device`, `pin_reset`, `step_up, register` — nên đăng nhập thiết bị mới thất bại vài lần sẽ dùng hết quota đặt lại PIN trong ngày.<br><br>**Tăng** ⇒ ít bị chặn oan nhưng chi phí SMS tăng và số có thể thành đích quấy rối. <br><br>**Giảm** ⇒ rủi ro người bán **bị kẹt hoàn toàn**: quên PIN và đã tiêu hết quota thì phải chờ sang ngày hoặc gọi hotline|CN-02 · 3.3 · CN-03 · COMMON-01|

### 1.4. Nhóm số điện thoại

|   |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|
|Tên tham số|Giá trị mặc định|Kiểu|Khoảng hợp lệ|Trả lời câu hỏi|Ý nghĩa nghiệp vụ|Dùng ở đâu|Trạng thái|
|#### `FORMAT_MSISDN`|^\+509[3-4]\d{7}$|biểu thức|–|Đầu số nào được coi là hợp lệ?|Danh sách đầu số di động Haiti được chấp nhận. Đổi tham số này khi nhà mạng mở dải số mới, **không** phải phát hành app mới. App kiểm định dạng tại máy, server kiểm lại|PL-02 · CN-02 · 3.2|**(*) MỚI** — cần Natcom xác nhận dải số|

### 1.5. Nhóm SMS

|   |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|
|Tên tham số|Giá trị mặc định|Kiểu|Khoảng hợp lệ|Trả lời câu hỏi|Ý nghĩa nghiệp vụ|Dùng ở đâu|Trạng thái|
|#### `SMS_RATE_LIMIT`|5 tin/giờ/merchant|int|1 – 20|Một gian hàng nhận bao nhiêu SMS nghiệp vụ mỗi giờ?|Hạn mức SMS chung. **Không áp cho OTP và không áp cho tin cảnh báo khóa đăng nhập**<br><br>**Tăng** ⇒ nhận đủ thông báo, chi phí SMS tăng. <br><br>**Giảm** ⇒ thông báo nghiệp vụ bị rơi, người bán không biết trạng thái|CFG-02|Có sẵn _(TSD §13.3)_|

### 1.6. Nhóm định danh eKYC

|Tên tham số|Giá trị mặc định|Kiểu|Khoảng hợp lệ|Trả lời câu hỏi|Ý nghĩa nghiệp vụ|Dùng ở đâu|
|---|---|---|---|---|---|---|
|#### `AUTO_ACTIVATE_SCORE`|0.85|decimal (0..1)|0.70 – 0.99|Điểm đối chiếu định danh tối thiểu bao nhiêu thì được đi tiếp?|Ngưỡng điểm tin cậy BRH-System (E1) trả về. Chỉ khi `matched = true` **và** `score ≥` ngưỡng thì hồ sơ đi tiếp; dưới ngưỡng thì yêu cầu chụp lại (`PIN-422-EKYCLOWSCORE`) và tính một vòng vào EKYC_RETAKE_MAX_PER_DAY.  <br>  <br>**Pilot:** đây là **cổng chặn cứng** — không còn nhánh gắn cờ hậu kiểm hay chuyển cán bộ BRH xem tay.  <br>  <br>**Tăng** ⇒ giảm rủi ro mạo danh, nhưng nhiều người bán thật bị bắt chụp lại (ánh sáng chợ kém, thẻ CIN cũ) và nhanh chạm trần.  <br>  <br>**Giảm** ⇒ onboarding trơn hơn, nhưng hồ sơ khớp yếu được kích hoạt ngay mà không có hậu kiểm|CN-01 · 3.1.5a · API Spec D.1|
|#### `EKYC_RETAKE_MAX_PER_DAY   `|5|int|3 – 10|Được đối chiếu không đạt bao nhiêu lần/ngày trước khi bị chặn?|Số lần đối chiếu **không đạt** tối đa/ngày cho một hồ sơ. Chạm trần thì chặn chụp tiếp, trả `PIN-422-EKYCLIMIT.` mốc reset dùng chung với OTP_MAX_PER_DAY.  <br>  <br>**Tính một vòng**: ảnh không đạt chuẩn, không khớp, điểm dưới ngưỡng, không đối chiếu được số CIN.  <br>**Không tính**: chụp lại trước khi gửi đối chiếu; lỗi hệ thống / timeout (`PIN-503-EKYC`); chụp lại do hết `EKYC_RESULT_TTL`.  <br>  <br>**Tăng** ⇒ người bán thật có thêm cơ hội, nhưng kẻ gian thử được nhiều ảnh hơn và tốn phí gọi E1.  <br>**Giảm** ⇒ nhiều người bán thật không eKYC được, trong khi pilot **không có công cụ duyệt tay** để hoàn tất hồ sơ|CN-01 · Mục 1 (Post-condition), 3.1.5a · CFG-03 · PIN-422-EKYCLIMIT|
|#### `EKYC_PHOTO_MAX_SIZE`|200 KB|int (KB)|100 – 500|Mỗi ảnh định danh được tải lên tối đa bao nhiêu?|Kích thước tối đa của một ảnh (CIN mặt trước, CIN mặt sau, selfie) sau khi app nén. App nén xuống dưới ngưỡng trước khi tải; server từ chối ảnh vượt ngưỡng bằng `PIN-400-PHOTO`.  <br>  <br>**Tăng** ⇒ ảnh rõ hơn, E1 ít từ chối vì chất lượng, nhưng tải chậm và dễ đứt trên 2G.  <br>  <br>**Giảm** ⇒ tải nhanh, nhưng ảnh nén mạnh dễ bị E1 trả `E1-422-QUALITY`, tiêu 1 lần vào EKYC_RETAKE_MAX_PER_DAY|CN-01 · 3.2.4 (Bước 4, Bước 7) · API Spec E.2.1|
|**`DRAFT_TTL_DAYS`**|7 ngày|duration (ngày)|3 – 30|Hồ sơ gian hàng dở dang bao lâu thì nhắc người bán?|Mốc phát mẫu tin `MS00005` / thông báo `NOTI020001` nhắc hoàn tất hồ sơ — **phát một lần**, không lặp.<br><br>**Phạm vi:** chỉ áp cho hồ sơ gian hàng dở dang của tài khoản **đã có**. **Không** áp cho `person` nháp đang chờ OTP — bản ghi đó bị xóa ngay khi thoát app _(CN-01 nhánh 9a)_.<br><br>Hồ sơ **không bị xóa** khi quá hạn: ảnh định danh đã tải lên là dữ liệu cá nhân, xóa phải theo chính sách lưu trữ chứ không theo bộ đếm ngày.|`CN-01` · 3.2.8 _(nhánh 10b)_ · CR-E|

### 1.7. Nhóm liên kết tài khoản nhận tiền **(*) MỚI · 15/09**

|Tên tham số|Giá trị mặc định|Kiểu|Khoảng hợp lệ|Trả lời câu hỏi|Ý nghĩa nghiệp vụ|Dùng ở đâu|
|---|---|---|---|---|---|---|
|#### `LINK_SESSION_TTL`|15 phút|duration (phút)|5 – 60|Phiên liên kết tài khoản nhận tiền sống được bao lâu?|Thời gian từ lúc MMS mở phiên liên kết _(định chế đã gửi OTP tới chủ tài khoản)_ tới lúc phải hoàn tất xác nhận. Quá hạn thì phiên bị hủy, trả `PIN-404-LINK`, người bán phải chọn lại nơi nhận tiền.<br><br>**Ràng buộc kiểm chéo bắt buộc:** `LINK_CONFIRM_RETRY_MAX` × tổng `LINK_CONFIRM_RETRY_BACKOFF` < tham số này.<br><br>- **Tăng** ⇒ người bán vùng sóng yếu có thêm thời gian chờ tin của định chế, nhưng phiên treo lâu và trong suốt thời gian đó mọi lối tạo liên kết mới bị khóa<br>    <br>- **Giảm** ⇒ giải phóng nhanh, nhưng người bán chưa kịp nhập mã đã phải làm lại từ đầu|`CN-01` · 3.1.7a · 3.2.7 _(B8, 9a, 11b, B12)_|
|#### `LINK_CONFIRM_RETRY_MAX`|3 lần|int|1 – 5|Xác nhận liên kết bị lỗi hệ thống thì server tự thử lại mấy lần?|Số lần MMS tự gửi lại yêu cầu xác nhận OTP sang định chế khi gặp lỗi hệ thống hoặc timeout (`account_link = confirming`). Mọi lần thử **giữ nguyên Idempotency-Key**, giãn cách theo `LINK_CONFIRM_RETRY_BACKOFF`. Hết lượt, hoặc quá `LINK_SESSION_TTL`, thì chuyển `account_link = failed` và báo qua NB-1C + SMS.  <br>  <br>**Tăng** ⇒ ít ca thất bại do sự cố thoáng qua, nhưng người bán chờ lâu hơn ở trạng thái "đang xử lý".  <br>  <br>**Giảm** ⇒ báo kết quả nhanh, nhưng một lần nghẽn ngắn của định chế cũng buộc người bán liên kết lại từ đầu|CN-01 · 3.1.7a (Bước 12, Bước 13) · API Spec C.0|
|#### `LINK_CONFIRM_RETRY_BACKOFF`|[1, 2, 4] giây|danh sách duration (giây)|Mỗi phần tử 1 – 30; tăng dần; số phần tử = `LINK_CONFIRM_RETRY_MAX`|Giữa các lần tự thử lại xác nhận liên kết phải chờ bao lâu?|Khoảng chờ trước từng lần MMS tự gửi lại yêu cầu xác nhận OTP sang định chế (phần tử thứ _n_ là thời gian chờ trước lần thử lại thứ _n_). Trong suốt thời gian này `account_link = confirming`, app giữ NB-2D ở trạng thái "đang xử lý" và không cho bấm lại.  <br>  <br>Nếu định chế trả `Retry-After` thì dùng giá trị lớn hơn giữa `Retry-After` và phần tử tương ứng.  <br>  <br>**Tăng** ⇒ cho định chế thời gian hồi phục, ít dội tải khi định chế đang nghẽn, nhưng người bán chờ lâu hơn trên màn "đang xử lý" và dễ chạm `LINK_SESSION_TTL`.  <br>  <br>**Giảm** ⇒ có kết quả nhanh, nhưng các lần thử dồn sát nhau dễ thất bại cùng một sự cố và làm tăng tải lên định chế|CN-01 · 3.1.7a (Bước 12) · API Spec A.3, C.0|
|#### LINK_TOKEN_RENEW_BEFORE|7 ngày|duration (ngày)|1 – 30|Còn bao lâu tới hạn thì MMS cần tự gia hạn token liên kết?|Mốc trước `token.expires_at` mà job gia hạn bắt đầu chạy.<br><br>**Lưu ý:** hiệu lực của token do **định chế** cấp, MMS không đặt được — tham số này chỉ là mốc gia hạn phía MMS.<br><br>- **Tăng** ⇒ nhiều thời gian đệm khi định chế gián đoạn, nhưng gọi gia hạn sớm và nhiều lần hơn<br>    <br>- **Giảm** ⇒ ít lời gọi, nhưng một đợt bảo trì của định chế đủ làm token chết và **gian hàng ngừng nhận tiền**|`CN-01` · 3.2.7 _(B14)_ · thực thể `token`|
|#### `LINK_MAX_PER_PERSON` **(*) MỚI · 16/10**|5 liên kết|int|1 – 10|Một người được giữ tối đa bao nhiêu tài khoản liên kết cùng lúc?|Trần số liên kết của một `person`, đếm các liên kết `active` + `grace` + `confirming`; **không** tính `revoked`, `expired`, `failed`. **Một trần chung** — hệ thống không phân loại liên kết nhận/trả _(tài khoản nhận tiền đồng thời là nguồn trả)_. Chạm trần thì vô hiệu **Add an account** và server trả `PIN-422-LINKLIMIT`.<br><br>- **Tăng** ⇒ người dùng gom được nhiều nguồn trả, nhưng nhiều token phải gia hạn và nhiều liên kết treo khi người dùng bỏ app<br>    <br>- **Giảm** ⇒ ít token phải quản lý, nhưng người bán đang đổi tài khoản nhận _(tài khoản cũ còn `grace`)_ dễ chạm trần<br><br>**Giá trị mặc định là đề xuất của BA review — cần chốt.**|`CN-06` · NB-16 control (4) · Luồng 3 _(B4, B8, nhánh 8b)_|

---

## 2. QUY TRÌNH ĐỔI THAM SỐ

1. Người đề xuất nhập giá trị mới kèm lý do và ngày hiệu lực.

2. Hệ thống kiểm **khoảng hợp lệ** của từng tham số **và** các **ràng buộc kiểm chéo** ở §1.1. Vi phạm thì từ chối với `PIN-400-VAL`.

3. Người phê duyệt (khác người đề xuất) chấp thuận.

4. Giá trị có hiệu lực theo ngày đã khai.

**Thông báo trước cho đội hỗ trợ hiện trường** khi đổi tham số ảnh hưởng trực tiếp tới trải nghiệm đăng nhập