**![](http://10.254.136.32:8090/plugins/servlet/confluence/placeholder/macro?definition=e3RvY30&locale=en_US&version=2)  
**

**Bảng ghi nhận thay đổi tài liệu**

A – Tạo mới, M – Sửa đổi, D – Xóa bỏ

đổi

|            |         |       |                  |                                          |        |
| ---------- | ------- | ----- | ---------------- | ---------------------------------------- | ------ |
| Ngày       | Vị trí  | A/M/D | Nguồn gốc        | Mô tả thay đổi                           | PB mới |
| 16/09/2026 | Toàn bộ | A     | Yêu cầu BA 16/09 | Tạo mới phụ lục Thông báo App Peye-Haiti |        |

# 1. Quy tắc đặt mã thông báo

## 1.1. Format mã

## NOTI NN NNNN

```
      │   └── số thứ tự trong nhóm, cấp tăng dần, KHÔNG dùng lại
      └────── mã nhóm nghiệp vụ, xem 1.2
```

Bốn quy tắc bắt buộc:

1. **Đúng 10 ký tự:**`NOTI` + 2 chữ số nhóm + 4 chữ số thứ tự. Ví dụ `NOTI040001`.
2. **Số thứ tự cấp tăng dần trong nhóm và không bao giờ dùng lại**
3. **Một mã = một tình huống = một cặp `Title` + `Content`.** Hai tình huống mà người dùng cần đọc hai câu khác nhau thì phải là **hai mã**, dù cùng nhóm và cùng kênh.  
      
    

## 1.2. Danh mục nhóm

|   |   |   |
|---|---|---|
|Nhóm|Miền nghiệp vụ|Dải mã|
|**01**|Tài khoản và an toàn|`NOTI01xxxx`|
|**02**|Hồ sơ người bán|`NOTI02xxxx`|
|**03**|Tài khoản nhận tiền · token · standee|`NOTI03xxxx`|
|**04**|Tiền về và biên lai|`NOTI04xxxx`|
|**05**|Đơn tính tiền và sổ nợ|`NOTI05xxxx`|
|**06**|Khiếu nại và hoàn tiền|`NOTI06xxxx`|
|**07**|Người mua|`NOTI07xxxx`|
|**08**|Hệ thống khác|`NOTI08xxxx`|

## 1.3. Khi nào cần một mã mới

Ba câu hỏi, cả ba đều **có** thì mới cần mã mới:

1. **Người dùng có cần đọc một câu khác không?** Nếu chỉ khác giá trị biến _(số tiền, tên khách)_ thì **dùng lại mã cũ**, thay biến.
    
2. **Sự kiện phát có khác không?** Cùng một sự kiện Kafka mà đẻ ra hai mã là dấu hiệu đang mã hóa trạng thái vào mã — xem quy tắc 4 ở 2.1.
3. **Hành động tiếp theo có khác không?** Cùng câu chữ, cùng đích chạm thì không cần tách.

## 1.4. Checklist trước khi đăng ký một mã mới

1. Đã tra danh mục xem có mã nào cùng tình huống chưa?
2. Nhóm đã đúng miền nghiệp vụ chưa?
3. Sự kiện phát đã có thật trong thiết kế chưa, hay mới chỉ có trong đầu?
4. `Title` ≤ **40 ký tự**, `Content` ≤ **120 ký tự**; nếu có nhánh SMS thì cả câu SMS ≤ **140 ký tự** kể cả biến đã điền?
5. Có lộ thông tin nhạy cảm khi hiện trên màn khóa không — số tài khoản đầy đủ, số CIN, số tiền của giao dịch lớn?

# 2. Nguyên tắc viết thông báo

1. **Nói kết quả trước, lý do sau.** Người bán đọc thông báo trong lúc đang bchờ thu hồig, thường chỉ đọc dòng đầu.
2. **Không bao giờ hiện mã kỹ thuật** — không mã lỗi, không tên tham số, không `trace_id`, không tên dịch vụ.
3. **Tiền luôn kèm đơn vị và định dạng theo `PL-02`:** `1,500 HTG`. **Không** viết tắt đơn vị.
4. **Số tài khoản luôn ở bản che** — bốn số cuối. Số CIN **không bao giờ** xuất hiện trong thông báo.
5. **Không hứa thời gian nếu hệ thống không bảo đảm được.** Viết _"We will update you here"_, không viết _"within 5 minutes"_
6. **Thông báo về tiền không được mang giọng quảng cáo** và không có biểu tượng cảm xúc.
7. **Câu chữ ở đây là bản đề xuất của BA**, chưa qua rà soát ngôn ngữ của BRH

# 3. Danh mục thông báo

## 3.1. Nhóm 01 — Tài khoản và an toàn

|   |   |   |   |   |   |
|---|---|---|---|---|---|
||Notification Code|Notification Name|Title|Content|Kênh · biến|
|1|`NOTI010001`|||||

## 3.2. Nhóm 02 — Hồ sơ người bán

|   |   |   |   |   |   |
|---|---|---|---|---|---|
||Notification Code|Notification Name|Title|Content|Kênh · biến|
|1|`NOTI020001`|Nhắc người bán quay lại hoàn tất hồ sơ dở dang|_Finish your shop setup_|_Your shop cannot receive money until _shop setup is_ done._|**Push**|
|2|`NOTI020002`|Báo gian hàng đã kích hoạt và nhận được tiền|_{shop_name} is active_|_You can receive money now. Your QR is ready in the app._|**Push**|
|3|`NOTI020003`|Báo gian hàng bị tạm khóa|_Your shop is on hold_|_You can still open the app, but you cannot receive money. Call 8686 to support_|**Push**|
|4|`NOTI020004`|Báo gian hàng được mở lại|_Your shop is active again_|_You can receive money now._|**Push**|

## 3.3. Nhóm 03 — Tài khoản nhận tiền, token và standee

|   |   |   |   |   |
|---|---|---|---|---|
|Notification Code|Notification Name|Title|Content|Kênh · biến|
|`NOTI030001`|Báo liên kết tài khoản nhận tiền thành công|_Account linked_|_Money will go to {bank_name} **_{last4}__|**Push**|
|`NOTI030002`|Báo liên kết không thành công sau khi đã thử lại|_We could not link that account_|_Open the app and choose another account._|**Push**|
|`NOTI030003`|Cảnh báo quyền truy cập tài khoản chính sắp hết hiệu lực (người bán)|_Renew your account link_|_In {days} days your shop stops receiving money. Renew it in the app._|**Push**|
|`NOTI030004`|Báo quyền truy cập đã hết hiệu lực với tài khoản chính (người bán), ngừng nhận báo Có|_Your shop stopped receiving money_|_The link to {bank_name} expired. Renew it in the app to start again._|**Push**|
|`NOTI030005`|Báo đã đổi tài khoản nhận, có QR mới|_You have a new QR_|_Money now goes to {bank_name}_ **_{last4}. Print the new standee._|**Push**|
|`NOTI030006`|Báo tài khoản cũ (grace) đã hết thời gian chờ thu hồi|_Your old QR stopped working_|_Only the new standee works now._|**Push**|

## 3.4. Nhóm 04 — Tiền về và biên lai

|   |   |   |   |   |
|---|---|---|---|---|
|Notification Code|Notification Name|Title|Content|Kênh · biến|
|`NOTI040001`|Báo có tiền về — «ting ting»|_{amount} received_|_From {payer_name} at {time}._|**Push → SMS** · `{amount}` `{payer_name}` `{time}`|

## 3.5. Nhóm 05 — Đơn tính tiền và sổ nợ

|   |   |   |   |   |
|---|---|---|---|---|
|Notification Code|Notification Name|Title|Content|Kênh · biến|
|`NOTI050001`|||||

## 3.6. Nhóm 06 — Khiếu nại và hoàn tiền

|   |   |   |   |   |
|---|---|---|---|---|
|Notification Code|Notification Name|Title|Content|Kênh · biến|
|`NOTI060001`|||||

## 3.7. Nhóm 07 — Người mua

|   |   |   |   |   |
|---|---|---|---|---|
|Notification Code|Notification Name|Title|Content|Kênh · biến|
|`NOTI070001`|||||

# 3.8. Nhóm 08 — Hệ thống khác

|   |   |   |   |   |
|---|---|---|---|---|
|Notification Code|Notification Name|Title|Content|Kênh · biến|
|`NOTI080001`|Báo trước lịch bảo trì có gián đoạn|_Peye-Haiti will pause on {date}_|_From {from_time} to {to_time} you cannot receive money. Cash sales are not affected._|**Push** · `{date}` `{from_time}` `{to_time}`|
|`NOTI080002`|Báo đang có sự cố và đang khắc phục|_Some payments are slow right now_|_Your money is safe. We will tell you when it is fixed._|**Push**|