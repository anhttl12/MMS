## ![](http://10.254.136.32:8090/plugins/servlet/confluence/placeholder/macro?definition=e3RvY30&locale=en_US&version=2)

BẢNG GHI NHẬN THAY ĐỔI

|   |   |   |   |   |   |
|---|---|---|---|---|---|
|Ngày|Vị trí|A/M/D|Nguồn gốc|Mô tả thay đổi|Phiên bản|
|08/09/2026|Toàn bộ|A||Tạo mới tài liệu|1.0|

## 1. QUY ƯỚC

|   |   |
|---|---|
|Hạng mục|Quy ước|
|`template_code`|Dạng `MSxxxxx`, `xxxxx` là số **tăng dần** từ `00001`. Đây là khóa mà SRS chức năng và mã nguồn tham chiếu tới — **không đổi sau khi đã phát hành**|
|`template_name`|Tên gợi nhớ, giữ nguyên giá trị `template_id` đang dùng trong đặc tả API|
|Tham số|Đặt trong ngoặc nhọn `{ }`. Mọi tham số khai ở cột _Tham số_ đều **bắt buộc** truyền, thiếu thì không gửi tin|
|Ngôn ngữ gửi|Theo `person.lang`. Chưa có bản dịch của ngôn ngữ đó thì gửi **en**|
|Độ dài|Mỗi tin ≤ **160 ký tự** sau khi thay tham số, để không bị tách thành nhiều SMS|

---

## 2. DANH MỤC MẪU TIN

|   |   |   |   |   |
|---|---|---|---|---|
|template_code|template_name|Mục đích|Tham số|Content (en)|
|#### MS00001|OTP_GENERIC|Gửi mã xác thực cho mọi `purpose.` Phát mỗi lần sinh OTP|`{otp}` · `{ttl_min}`|Your Peye-Haiti code is {otp}. Valid for {ttl_min} minutes. Do not share it with anyone.|
|#### MS00002|LOGIN_LOCK|Báo cho chủ số biết đăng nhập vừa bị khóa do nhập sai PIN đủ `PIN_MAX_ATTEMPTS`|`{minutes}`|Your Peye-Haiti sign-in is locked for {minutes} minutes after too many wrong PIN attempts.|
|#### MS00003|APP_STATUS|Báo người bán biết hồ sơ vừa đổi trạng thái mà không cần mở app|`{status_line}`|Your Peye-Haiti application: {status_line}. Open the app to continue.|
|#### MS00004|MERCHANT_STATUS|Báo gian hàng đã kích hoạt xong và bắt đầu nhận được tiền|shop_name|{shop_name} is ready to receive money on Peye-Haiti. Open the app to see your QR.|
|#### MS00005|APP_REMINDER|Kéo người bán quay lại hoàn tất hồ sơ dở dang quá lâu — **phát một lần**, không lặp|steps_left|Your Peye-Haiti shop is almost ready — {steps_left} step left. Open the app to finish.|
|#### MS00006|PIN_CHANGED|Báo chủ số biết PIN vừa bị đổi hoặc đặt lại|-|Your Peye-Haiti PIN has been successfully changed.|

## 3. TÍCH HỢP NATCOM (N1)

|                        |                                                                                                                                                                 |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Hạng mục               | Nội dung                                                                                                                                                        |
| Chiều                  | MMS → Natcom N1 → thuê bao                                                                                                                                      |
| Trạng thái chuyển phát | Mọi tin nhận lại DLR từ Natcom và ghi vào `notification.status`                                                                                                 |
| Xử lý lỗi              | Lỗi hệ thống → thử lại 3 lần **giữ nguyên mã tham chiếu**. Mạch ngắt đang mở hoặc bảo trì → trả `PIN-503-DEP`, hướng dẫn gọi hotline 8686 để nhận OTP qua thoại |
| Số bị chặn nhận SMS    | Hướng dẫn liên hệ hotline 8686                                                                                                                                  |