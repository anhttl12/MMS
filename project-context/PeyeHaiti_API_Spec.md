# API Spec — Đặc tả API chi tiết từng trường & mã lỗi · Giải pháp Merchant Peye-Haiti

<!-- TOC -->
<a id="muc-luc"></a>

**Mục lục**

- [A. Chuẩn chung](#muc-a-chuan-chung)
  - [A.1. Base URL & nhóm xác thực](#muc-a-1-base-url-nhom-xac-thuc)
  - [A.1b. Thẻ hệ thống TỰ KÝ — MỘT thẻ cho cả DANH TÍNH lẫn NỘI DUNG «v3.4»](#muc-a-1b-the-he-thong-tu-ky-mot-the-cho-ca-danh-tinh-lan-noi-dun)
  - [A.2. Header chuẩn](#muc-a-2-header-chuan)
  - [A.3. Envelope lỗi (mọi API mọi nhóm)](#muc-a-3-envelope-loi-moi-api-moi-nhom)
  - [A.4. Bảng mã lỗi CHUNG (mọi endpoint đều có thể trả — bảng lỗi riêng từng endpoint chỉ liệt kê lỗi ĐẶC THÙ)](#muc-a-4-bang-ma-loi-chung-moi-endpoint-deu-co-the-tra-bang-loi-r)
  - [A.5. Quy ước dữ liệu (áp cho mọi API trong tài liệu)](#muc-a-5-quy-uoc-du-lieu-ap-cho-moi-api-trong-tai-lieu)
- [B. API MMS expose cho đối tác — `https://partner.peye-haiti.ht/v1`](#muc-b-api-mms-expose-cho-doi-tac-https-partner-peye-haiti-ht-v1)
  - [B.1. `POST /credit-events` — Webhook báo có M4 (bank NHẬN → MMS) — ĐƯỜNG GĂNG](#muc-b-1-post-credit-events-webhook-bao-co-m4-bank-nhan-mms-duong)
  - [B.2. `POST /sms-dlr` — Delivery report SMS (Natcom → MMS)](#muc-b-2-post-sms-dlr-delivery-report-sms-natcom-mms)
  - [B.3. `POST /eod-notifications` — Switch báo file E3 sẵn sàng (E3 push)](#muc-b-3-post-eod-notifications-switch-bao-file-e3-san-sang-e3-pu)
  - [B.4. `POST /payment-results` — Webhook KẾT QUẢ TRẢ M-PAY (bank TRẢ → Peye-Haiti) «Peye-Haiti 15/08»](#muc-b-4-post-payment-results-webhook-ket-qua-tra-m-pay-bank-tra)
  - [B.5. `POST /qr-inquiry` — Tra cứu QR & lấy tham chiếu trả (app định chế TRẢ → Peye-Haiti) «Peye-Haiti 16/08»](#muc-b-5-post-qr-inquiry-tra-cuu-qr-lay-tham-chieu-tra-app-dinh-c)
- [C. Open Banking bank NHẬN/TRẢ expose — MMS gọi ra (`{OB_BASE}/ob/v1`, hợp đồng D2 + phụ lục M-PAY)](#muc-c-open-banking-bank-nhan-tra-expose-mms-goi-ra-obbase-ob-v1)
  - [C.0. Mã lỗi OB chuẩn hóa & cách MMS xử lý (áp cho mọi API nhóm C)](#muc-c-0-ma-loi-ob-chuan-hoa-cach-mms-xu-ly-ap-cho-moi-api-nhom-c)
  - [C.1. M1 · `POST /ob/v1/links` — Khởi tạo liên kết TK đã có (bước 1/2)](#muc-c-1-m1-post-ob-v1-links-khoi-tao-lien-ket-tk-da-co-buoc-1-2)
  - [C.2. M1 · `POST /ob/v1/links/{link_id}/confirm` — Xác nhận OTP, nhận token (bước 2/2)](#muc-c-2-m1-post-ob-v1-links-linkid-confirm-xac-nhan-otp-nhan-tok)
  - [C.3. M1a · `POST /ob/v1/tokens/refresh` — Gia hạn token](#muc-c-3-m1a-post-ob-v1-tokens-refresh-gia-han-token)
  - [C.4. M1b · `POST /ob/v1/tokens/revoke` — Thu hồi token](#muc-c-4-m1b-post-ob-v1-tokens-revoke-thu-hoi-token)
  - [C.5. M3 · `GET /ob/v1/accounts/{link_id}/balance` — Số dư](#muc-c-5-m3-get-ob-v1-accounts-linkid-balance-so-du)
  - [C.6. M3 · `GET /ob/v1/accounts/{link_id}/transactions` — Lịch sử giao dịch](#muc-c-6-m3-get-ob-v1-accounts-linkid-transactions-lich-su-giao-d)
  - [C.7. M-PAY.1 · `POST /ob/v1/payments` — Khởi tạo lệnh trả (định chế TRẢ) «Peye-Haiti 15/08»](#muc-c-7-m-pay-1-post-ob-v1-payments-khoi-tao-lenh-tra-dinh-che-t)
  - [C.8. M-PAY.2 · `GET /ob/v1/payments/{ext_payment_id}` — Trạng thái lệnh trả «Peye-Haiti 15/08»](#muc-c-8-m-pay-2-get-ob-v1-payments-extpaymentid-trang-thai-lenh)
  - [C.9. M-PAY.3 · `POST /ob/v1/payments/{ext_payment_id}/sca` — Xác nhận OTP lệnh trả «v3.5»](#muc-c-9-m-pay-3-post-ob-v1-payments-extpaymentid-sca-xac-nhan-ot)
- [D. BRH-System (E1·E2) · Switch (E3·E3-reg) · Natcom (N1) — MMS gọi ra](#muc-d-brh-system-e1e2-switch-e3e3-reg-natcom-n1-mms-goi-ra)
  - [D.1. E1 · `POST {BRH_SYSTEM}/brh/ekyc/v1/verify` — Đối chiếu danh tính CIN + selfie ↔ ONI](#muc-d-1-e1-post-brhsystem-brh-ekyc-v1-verify-doi-chieu-danh-tinh)
  - [D.2. E2 · `POST {BRH_SYSTEM}/brh/aml/v1/screen` — Sàng lọc AML](#muc-d-2-e2-post-brhsystem-brh-aml-v1-screen-sang-loc-aml)
  - [D.3. E3 · `GET {SWITCH}/switch/v1/eod?biz_date={date}&session={n}` — Kéo bảng kê cuối phiên (kênh pull)](#muc-d-3-e3-get-switch-switch-v1-eod-bizdate-date-session-n-keo-b)
  - [D.4. E3-reg · `PUT {SWITCH}/switch/v1/account-registry` — Đăng ký danh mục TK NHẬN (qua BRH)](#muc-d-4-e3-reg-put-switch-switch-v1-account-registry-dang-ky-dan)
  - [D.5. N1 · `POST {NATCOM}/natcom/sms/v1/send` — Gửi SMS liên mạng, brandname Peye-Haiti](#muc-d-5-n1-post-natcom-natcom-sms-v1-send-gui-sms-lien-mang-bran)
- [E. BFF cho app & portal — `https://api.peye-haiti.ht/v1` (chi tiết hóa TSD §2c)](#muc-e-bff-cho-app-portal-https-api-peye-haiti-ht-v1-chi-tiet-hoa)
  - [E.1. Auth NB & portal (màn NB-00/02, BRH-01)](#muc-e-1-auth-nb-portal-man-nb-00-02-brh-01)
    - [E.1.1 · `POST /auth/register` — Khởi tạo đăng ký (công khai)](#muc-e-1-1-post-auth-register-khoi-tao-dang-ky-cong-khai)
    - [E.1.2 · `POST /auth/otp/send` — Gửi/gửi lại OTP (công khai)](#muc-e-1-2-post-auth-otp-send-gui-gui-lai-otp-cong-khai)
    - [E.1.3 · `POST /auth/otp/verify` — Xác thực OTP (công khai)](#muc-e-1-3-post-auth-otp-verify-xac-thuc-otp-cong-khai)
    - [E.1.4 · `POST /auth/pin/set` — Đặt PIN lần đầu (công khai + verify_token)](#muc-e-1-4-post-auth-pin-set-dat-pin-lan-dau-cong-khai-verifytoke)
    - [E.1.5 · `POST /auth/login` — Đăng nhập app (công khai)](#muc-e-1-5-post-auth-login-dang-nhap-app-cong-khai)
    - [E.1.6 · `POST /auth/token/refresh` — Xoay token phiên](#muc-e-1-6-post-auth-token-refresh-xoay-token-phien)
    - [E.1.7 · `POST /auth/pin/reset` — Quên PIN (US-38, công khai + verify_token)](#muc-e-1-7-post-auth-pin-reset-quen-pin-us-38-cong-khai-verifytok)
    - [E.1.8 · `POST /auth/emergency-lock` — Khóa khẩn (US-39, AC-10.1; công khai — gọi từ máy bất kỳ/hotline 8686)](#muc-e-1-8-post-auth-emergency-lock-khoa-khan-us-39-ac-10-1-cong)
    - [E.1.9 · `POST /admin/auth/login` — Portal bước 1/2 (công khai)](#muc-e-1-9-post-admin-auth-login-portal-buoc-1-2-cong-khai)
    - [E.1.10 · `POST /admin/auth/totp` — Portal bước 2/2 (công khai + mfa_token)](#muc-e-1-10-post-admin-auth-totp-portal-buoc-2-2-cong-khai-mfatok)
  - [E.2. eKYC (màn NB-2A/1C)](#muc-e-2-ekyc-man-nb-2a-1c)
    - [E.2.1 · `POST /ekyc/photos` — Upload ảnh eKYC · Quyền: merchant (status `draft`/`need_more`)](#muc-e-2-1-post-ekyc-photos-upload-anh-ekyc-quyen-merchant-status)
    - [E.2.2 · `POST /ekyc/submit` — Nộp hồ sơ eKYC · Quyền: merchant](#muc-e-2-2-post-ekyc-submit-nop-ho-so-ekyc-quyen-merchant)
    - [E.2.3 · `GET /applications/me` — Trạng thái hồ sơ (NB-1C) · Quyền: merchant](#muc-e-2-3-get-applications-me-trang-thai-ho-so-nb-1c-quyen-merch)
    - [E.2.4 · `POST /applications/me/resubmit` — Nộp lại theo yêu cầu bổ sung · Quyền: merchant](#muc-e-2-4-post-applications-me-resubmit-nop-lai-theo-yeu-cau-bo)
  - [E.3. Tài khoản nhận & liên kết (màn NB-2B/14 · luồng S4)](#muc-e-3-tai-khoan-nhan-lien-ket-man-nb-2b-14-luong-s4)
    - [E.3.1 · `GET /links` — Danh sách liên kết · Quyền: merchant](#muc-e-3-1-get-links-danh-sach-lien-ket-quyen-merchant)
    - [E.3.2 · `POST /links` — Liên kết TK đã có, bước 1: khởi tạo + gửi OTP (US-03) · Quyền: merchant (eKYC đã pass)](#muc-e-3-2-post-links-lien-ket-tk-da-co-buoc-1-khoi-tao-gui-otp-u)
    - [E.3.3 · `POST /links/confirm` — Bước 2: OTP bank → nhận token · Quyền: merchant](#muc-e-3-3-post-links-confirm-buoc-2-otp-bank-nhan-token-quyen-me)
    - [E.3.5 · `POST /links/change` — Đổi TK nhận (cutover S4 ①→⑤) · Quyền: merchant](#muc-e-3-5-post-links-change-doi-tk-nhan-cutover-s4-15-quyen-merc)
    - [E.3.6 · `POST /links/{link_id}/confirm-standee` — Xác nhận «đã dán standee mới» (S4 bước ④) · Quyền: merchant](#muc-e-3-6-post-links-linkid-confirm-standee-xac-nhan-da-dan-stan)
    - [E.3.7 · `POST /links/renew` — Gia hạn token thủ công (nút NB-14; job D-7 tự chạy) · Quyền: merchant](#muc-e-3-7-post-links-renew-gia-han-token-thu-cong-nut-nb-14-job)
  - [E.4. QR & bill (màn NB-04/07/08 · luồng S3)](#muc-e-4-qr-bill-man-nb-04-07-08-luong-s3)
    - [E.4.1 · `GET /qr/static` — Payload QR tĩnh hiện hành · Quyền: merchant](#muc-e-4-1-get-qr-static-payload-qr-tinh-hien-hanh-quyen-merchant)
    - [E.4.3 · `POST /bills` — Tạo đơn tính tiền (US-14/15) · Quyền: merchant](#muc-e-4-3-post-bills-tao-don-tinh-tien-us-14-15-quyen-merchant)
    - [E.4.4 · `GET /bills?status&biz_date&cursor&page_size` — Bill trong ngày, 3 nhóm (NB-08, US-17) · Quyền: merchant](#muc-e-4-4-get-bills-status-bizdate-cursor-pagesize-bill-trong-ng)
    - [E.4.5 · `POST /bills/{bill_id}/close-cash` — Đóng «đã thu TIỀN MẶT» (US-16) · Quyền: merchant](#muc-e-4-5-post-bills-billid-close-cash-dong-da-thu-tien-mat-us-1)
    - [E.4.6 · `POST /bills/{bill_id}/cancel` — Hủy bill · Quyền: merchant](#muc-e-4-6-post-bills-billid-cancel-huy-bill-quyen-merchant)
    - [E.4.7 · `GET /bills/{bill_id}/qr` — Payload QR động của bill (chia sẻ/in lại) · Quyền: merchant](#muc-e-4-7-get-bills-billid-qr-payload-qr-dong-cua-bill-chia-se-i)
  - [E.5. Tiền về & khớp (màn NB-05/09 · luồng S2/S7)](#muc-e-5-tien-ve-khop-man-nb-05-09-luong-s2-s7)
    - [E.5.1 · `GET /credit-events?from&to&match_level&cursor&page_size` — Danh sách tiền về («két tiền») · Quyền: merchant](#muc-e-5-1-get-credit-events-from-to-matchlevel-cursor-pagesize-d)
    - [E.5.2 · `POST /credit-events/{id}/confirm-match` — Xác nhận khớp mức ② (tay) / chốt đề xuất gạch nợ (S7) · Quyền: merchant](#muc-e-5-2-post-credit-events-id-confirm-match-xac-nhan-khop-muc)
    - [E.5.3 · `GET /credit-events/{id}/receipt` — Biên lai · Quyền: merchant](#muc-e-5-3-get-credit-events-id-receipt-bien-lai-quyen-merchant)
    - [E.5.4 · `POST /credit-events/{id}/report-issue` — Người bán báo sai giao dịch → mở case · Quyền: merchant](#muc-e-5-4-post-credit-events-id-report-issue-nguoi-ban-bao-sai-g)
    - [E.5.5 · `POST /credit-events/{id}/send-receipt` — Gửi biên lai cho khách (US-24) · Quyền: merchant](#muc-e-5-5-post-credit-events-id-send-receipt-gui-bien-lai-cho-kh)
    - [E.5.6 · `POST /credit-events/{id}/revenue-flag` — Đánh dấu «không phải doanh thu» (US-40, AC-2.7) · Quyền: merchant](#muc-e-5-6-post-credit-events-id-revenue-flag-danh-dau-khong-phai)
  - [E.6. Sổ nợ (màn NB-15 · luồng S7, offline-first 100%)](#muc-e-6-so-no-man-nb-15-luong-s7-offline-first-100)
    - [E.6.1 · `GET /debtors?q&cursor&page_size` — Danh sách khách nợ · Quyền: merchant](#muc-e-6-1-get-debtors-q-cursor-pagesize-danh-sach-khach-no-quyen)
    - [E.6.2 · `POST /debtors` — Thêm khách nợ · Quyền: merchant](#muc-e-6-2-post-debtors-them-khach-no-quyen-merchant)
    - [E.6.3 · `POST /debtors/{id}/entries` — Ghi nợ / ghi trả (US-18, ≤10 giây) · Quyền: merchant](#muc-e-6-3-post-debtors-id-entries-ghi-no-ghi-tra-us-18-10-giay-q)
    - [E.6.4 · `GET /debtors/{id}/entries?cursor` — Lịch sử một khách · Quyền: merchant](#muc-e-6-4-get-debtors-id-entries-cursor-lich-su-mot-khach-quyen)
    - [E.6.5 · `POST /debtors/{id}/remind` — Nhắc nợ 1 chạm qua SMS (US-19, AC-4.4) · Quyền: merchant](#muc-e-6-5-post-debtors-id-remind-nhac-no-1-cham-qua-sms-us-19-ac)
  - [E.7. Danh mục sản phẩm (màn NB-06 · hậu kiểm C9)](#muc-e-7-danh-muc-san-pham-man-nb-06-hau-kiem-c9)
    - [E.7.1 · `GET /products?include_deleted=false&cursor` — Danh mục món · Quyền: merchant](#muc-e-7-1-get-products-includedeleted-false-cursor-danh-muc-mon)
    - [E.7.2 · `POST /products` — Thêm món · Quyền: merchant](#muc-e-7-2-post-products-them-mon-quyen-merchant)
    - [E.7.3 · `PATCH /products/{id}` — Sửa / xóa mềm · Quyền: merchant](#muc-e-7-3-patch-products-id-sua-xoa-mem-quyen-merchant)
  - [E.8. Báo cáo & thông báo (màn NB-10/13)](#muc-e-8-bao-cao-thong-bao-man-nb-10-13)
    - [E.8.1 · `GET /reports/sales?range=day|week|month&date` — Báo cáo bán hàng · Quyền: merchant](#muc-e-8-1-get-reports-sales-range-day-week-month-date-bao-cao-ba)
    - [E.8.2 · `GET /notifications?unread&cursor` — Hộp thông báo · Quyền: merchant](#muc-e-8-2-get-notifications-unread-cursor-hop-thong-bao-quyen-me)
    - [E.8.3 · `POST /notifications/{id}/ack` — Xác nhận đã nhận · Quyền: merchant](#muc-e-8-3-post-notifications-id-ack-xac-nhan-da-nhan-quyen-merch)
  - [E.9. Đồng bộ offline (TSD §7)](#muc-e-9-dong-bo-offline-tsd-7)
    - [E.9.1 · `POST /sync/batch` — Đồng bộ 2 chiều theo lô · Quyền: merchant](#muc-e-9-1-post-sync-batch-dong-bo-2-chieu-theo-lo-quyen-merchant)
    - [E.9.2 · `POST /media` — Upload ảnh (sản phẩm, chứng cứ) · Quyền: merchant](#muc-e-9-2-post-media-upload-anh-san-pham-chung-cu-quyen-merchant)
  - [E.10. Hồ sơ người dùng (/me)](#muc-e-10-ho-so-nguoi-dung-me)
    - [E.10.4 · `GET /me` — Hồ sơ · Quyền: user có person (mọi vai — app dựng menu theo trạng thái merchant trả về)](#muc-e-10-4-get-me-ho-so-quyen-user-co-person-moi-vai-app-dung-me)
    - [E.10.5 · `PATCH /me` — Sửa hồ sơ nhẹ · Quyền: user có person (mọi vai)](#muc-e-10-5-patch-me-sua-ho-so-nhe-quyen-user-co-person-moi-vai)
  - [E.11. Portal BRH — hậu kiểm hồ sơ & quản lý merchant «v3.6» (màn BRH-03/04)](#muc-e-11-portal-brh-hau-kiem-ho-so-quan-ly-merchant-v3-6-man-brh)
    - [E.11.1 · `GET /admin/applications?status&flag&market_id&q&cursor` — Danh sách HẬU KIỂM hồ sơ («v3.6» — không phải hàng chặn: gian hàng đã active) · Quyền: approver (đọc: +supervisor_aml, inspector_read)](#muc-e-11-1-get-admin-applications-status-flag-marketid-q-cursor)
    - [E.11.2 · `POST /admin/applications/{id}/approve` — Đóng hậu kiểm OK («v3.6» — gian hàng vốn đã active; đây là kết luận hậu kiểm) · Quyền: approver](#muc-e-11-2-post-admin-applications-id-approve-dong-hau-kiem-ok-v)
    - [E.11.3 · `POST /admin/applications/{id}/reject` — Từ chối · Quyền: approver](#muc-e-11-3-post-admin-applications-id-reject-tu-choi-quyen-appro)
    - [E.11.4 · `POST /admin/applications/{id}/need-more` — Yêu cầu bổ sung · Quyền: approver](#muc-e-11-4-post-admin-applications-id-need-more-yeu-cau-bo-sung)
    - [E.11.5 · `GET /admin/merchants?status&market_id&q&cursor` — Danh sách merchant · Quyền: mọi vai trò portal (đọc)](#muc-e-11-5-get-admin-merchants-status-marketid-q-cursor-danh-sac)
    - [E.11.6 · `POST /admin/merchants/{id}/suspend` — Tạm khóa (US-28) · Quyền: supervisor_aml hoặc admin theo RBAC `/docs/rbac.csv`](#muc-e-11-6-post-admin-merchants-id-suspend-tam-khoa-us-28-quyen)
    - [E.11.7 · `POST /admin/merchants/{id}/resume` — Mở lại · Quyền: như E.11.6](#muc-e-11-7-post-admin-merchants-id-resume-mo-lai-quyen-nhu-e-11)
    - [E.11.8 · `POST /admin/merchants/{id}/close` — Đóng gian hàng (S8) · Quyền: admin (thao tác), theo quy trình checklist](#muc-e-11-8-post-admin-merchants-id-close-dong-gian-hang-s8-quyen)
    - [E.11.9 · `PATCH /admin/merchants/{id}/standee` — Cập nhật tracking standee (BRH-04) · Quyền: admin/approver theo RBAC](#muc-e-11-9-patch-admin-merchants-id-standee-cap-nhat-tracking-st)
  - [E.12. Portal BRH — giám sát GD, case, AML (màn BRH-05/06/07)](#muc-e-12-portal-brh-giam-sat-gd-case-aml-man-brh-05-06-07)
    - [E.12.1 · `GET /admin/transactions?from&to&merchant_id&ref_id&amount_min_ct&amount_max_ct&match_level&source&is_revenue&cursor` — Tra cứu giao dịch · Quyền: supervisor_aml, ops_read, inspector_read](#muc-e-12-1-get-admin-transactions-from-to-merchantid-refid-amoun)
    - [E.12.2 · `GET /admin/transactions/{credit_event_id}` — Truy vết 1 GD trọn chuỗi (AC-6.3) · Quyền: như E.12.1](#muc-e-12-2-get-admin-transactions-crediteventid-truy-vet-1-gd-tr)
    - [E.12.3 · `POST /admin/cases` — Mở case từ portal/hotline · Quyền: supervisor_aml](#muc-e-12-3-post-admin-cases-mo-case-tu-portal-hotline-quyen-supe)
    - [E.12.4 · `GET /admin/cases?status&type&overdue&assigned_to&cursor` — Hàng đợi case (US-32) · Quyền: supervisor_aml (đọc: inspector_read)](#muc-e-12-4-get-admin-cases-status-type-overdue-assignedto-cursor)
    - [E.12.5 · `POST /admin/cases/{id}/evidence` — Đính chứng cứ 2 phía · Quyền: supervisor_aml](#muc-e-12-5-post-admin-cases-id-evidence-dinh-chung-cu-2-phia-quy)
    - [E.12.6 · `POST /admin/cases/{id}/conclude` — Kết luận case (kèm XÁC MINH hoàn — AC-7.1) · Quyền: supervisor_aml](#muc-e-12-6-post-admin-cases-id-conclude-ket-luan-case-kem-xac-mi)
    - [E.12.7 · `GET /admin/aml-alerts?status&source&rule_code&merchant_id&cursor` — Hàng đợi cảnh báo AML (US-33) · Quyền: supervisor_aml (đọc: inspector_read)](#muc-e-12-7-get-admin-aml-alerts-status-source-rulecode-merchanti)
    - [E.12.8 · `POST /admin/aml-alerts/{id}/decide` — Quyết định AML (US-34, AC-8.3) · Quyền: supervisor_aml](#muc-e-12-8-post-admin-aml-alerts-id-decide-quyet-dinh-aml-us-34)
    - [E.12.9 · `GET /admin/cases/{id}` — Chi tiết case: hồ sơ + chứng cứ + dòng thời gian (BRH-06) · Quyền: supervisor_aml (đọc: inspector_read)](#muc-e-12-9-get-admin-cases-id-chi-tiet-case-ho-so-chung-cu-dong)
  - [E.13. Portal BRH — báo cáo, audit, người dùng (màn BRH-08/11/12) + tham số qua API (không màn — BRH-09 bỏ 04/08)](#muc-e-13-portal-brh-bao-cao-audit-nguoi-dung-man-brh-08-11-12-th)
    - [E.13.1 · `GET /admin/reports/kpi?range=day|week|month&from&to&city&market_id&format=json|csv|pdf` — KPI pilot (US-29) · Quyền: mọi vai trò portal](#muc-e-13-1-get-admin-reports-kpi-range-day-week-month-from-to-ci)
    - [E.13.2 · `GET /admin/params` — Danh sách tham số (§13.3) · Quyền: admin (đọc: mọi vai trò)](#muc-e-13-2-get-admin-params-danh-sach-tham-so-13-3-quyen-admin-d)
    - [E.13.3 · `PUT /admin/params/{key}` — Đề xuất thay đổi (maker) · Quyền: admin](#muc-e-13-3-put-admin-params-key-de-xuat-thay-doi-maker-quyen-adm)
    - [E.13.4 · `POST /admin/params/{key}/approve` — Phê duyệt 4 mắt (checker) · Quyền: admin (khác người đề xuất)](#muc-e-13-4-post-admin-params-key-approve-phe-duyet-4-mat-checker)
    - [E.13.5 · `GET /admin/audit?actor&action&target&from&to&cursor` — Nhật ký bất biến (US-31) · Quyền: inspector_read, admin (đọc)](#muc-e-13-5-get-admin-audit-actor-action-target-from-to-cursor-nh)
    - [E.13.6 · `GET /admin/users?role&status&cursor` — Người dùng portal · Quyền: admin](#muc-e-13-6-get-admin-users-role-status-cursor-nguoi-dung-portal)
    - [E.13.7 · `POST /admin/users` — Tạo người dùng · Quyền: admin](#muc-e-13-7-post-admin-users-tao-nguoi-dung-quyen-admin)
    - [E.13.8 · `PATCH /admin/users/{id}` — Sửa/khóa/reset 2FA · Quyền: admin](#muc-e-13-8-patch-admin-users-id-sua-khoa-reset-2fa-quyen-admin)
    - [E.13.9 · `POST /admin/adjustments/{id}/approve` · `POST /admin/adjustments/{id}/reject` — Duyệt/từ chối bút toán điều chỉnh (luồng 4 mắt duy nhất `draft→approved→posted`) · Quyền: approver (người duyệt PHẢI khác người tạo nháp — AC-6.2)](#muc-e-13-9-post-admin-adjustments-id-approve-post-admin-adjustme)
  - [E.14. Console vận hành VDS (màn AQ-00/01/03/04)](#muc-e-14-console-van-hanh-vds-man-aq-00-01-03-04)
    - [E.14.1 · `GET /ops/connections` — Sức khỏe kết nối đối tác (US-35) · Quyền: ops_read+](#muc-e-14-1-get-ops-connections-suc-khoe-ket-noi-doi-tac-us-35-qu)
    - [E.14.2 · `GET /ops/tokens?status=expiring|revoked|active&days=7&cursor` — Kho token sắp hết hạn · Quyền: ops_read+](#muc-e-14-2-get-ops-tokens-status-expiring-revoked-active-days-7)
    - [E.14.4 · `GET /ops/health` — Sức khỏe nội bộ MMS · Quyền: ops_read+](#muc-e-14-4-get-ops-health-suc-khoe-noi-bo-mms-quyen-opsread)
    - [E.14.5 · `GET /ops/recon-runs?biz_date&status&cursor` — Các phiên đối soát (AQ-03) · Quyền: ops_read+](#muc-e-14-5-get-ops-recon-runs-bizdate-status-cursor-cac-phien-do)
    - [E.14.6 · `GET /ops/discrepancies?status&dtype&run_id&overdue&cursor` — Hàng đợi chênh lệch (AQ-04, US-36) · Quyền: ops_read+](#muc-e-14-6-get-ops-discrepancies-status-dtype-runid-overdue-curs)
    - [E.14.7 · `POST /ops/discrepancies/{id}/resolve` — Xử lý một khoản lệch · Quyền: ops ghi](#muc-e-14-7-post-ops-discrepancies-id-resolve-xu-ly-mot-khoan-lec)
  - [E.15. Portal BRH — dashboard tổng quan & bổ khuyết portal (màn BRH-02 · bổ sung BRH-04/06/08)](#muc-e-15-portal-brh-dashboard-tong-quan-bo-khuyet-portal-man-brh)
    - [E.15.1 · `GET /admin/dashboard?city&market_id` — Bảng điều khiển tổng quan (BRH-02, US-27) · Quyền: mọi vai trò portal (đọc — chỉ số liệu TỔNG HỢP; drill-down mở màn đích theo RBAC của màn đó)](#muc-e-15-1-get-admin-dashboard-city-marketid-bang-dieu-khien-ton)
    - [E.15.2 · `GET /admin/merchants/{id}/activity?types&from&to&cursor` — Dòng thời gian hoạt động 1 merchant (BRH-04 tab «Hoạt động») · Quyền: approver, supervisor_aml, inspector_read (đầy đủ) · ops_read (chỉ `link/standee/system`) · admin (chỉ `application/admin` — KHÔNG sự kiện GD, nhất quán E.13.7)](#muc-e-15-2-get-admin-merchants-id-activity-types-from-to-cursor)
    - [E.15.3 · `POST /admin/cases/{id}/request-info` — Yêu cầu bổ sung thông tin case (BRH-06, US-32) · Quyền: supervisor_aml](#muc-e-15-3-post-admin-cases-id-request-info-yeu-cau-bo-sung-thon)
  - [E.16. Thanh toán trong app — DÙNG CHUNG MỌI VAI (màn NM-01→05 · luồng S9) «v3.5»](#muc-e-16-thanh-toan-trong-app-dung-chung-moi-vai-man-nm-0105-luo)
    - [E.16.1 · `POST /payments` — Quét QR → trả (US-41) · Quyền: user](#muc-e-16-1-post-payments-quet-qr-tra-us-41-quyen-user)
    - [E.16.2 · `POST /payments/{id}/confirm` — Xác nhận trả sau khi thấy tên (1 chạm) · Quyền: user](#muc-e-16-2-post-payments-id-confirm-xac-nhan-tra-sau-khi-thay-te)
    - [E.16.3 · `GET /payments/{id}` — Trạng thái/biên lai số (US-43) · Quyền: user](#muc-e-16-3-get-payments-id-trang-thai-bien-lai-so-us-43-quyen-us)
    - [E.16.4 · `GET /payments?from&to&cursor` — Lịch sử trả (NM-04) · Quyền: user](#muc-e-16-4-get-payments-from-to-cursor-lich-su-tra-nm-04-quyen-u)
    - [E.16.5 · `POST /payments/{id}/dispute` — Khiếu nại khoản đã trả (US-45) · Quyền: user](#muc-e-16-5-post-payments-id-dispute-khieu-nai-khoan-da-tra-us-45)
    - [E.16.6 · `POST /payments/{id}/sca` — Nộp OTP xác thực bổ sung «v3.5» · Quyền: user](#muc-e-16-6-post-payments-id-sca-nop-otp-xac-thuc-bo-sung-v3-5-qu)
- [P. API công khai — `https://api.peye-haiti.ht/public` (không xác thực) «Peye-Haiti 15/08»](#muc-p-api-cong-khai-https-api-peye-haiti-ht-public-khong-xac-thu)
    - [P.1 · `GET /public/merchants/{code}` — Trang xác minh merchant (yêu cầu C-CLIENTS «Vérification»)](#muc-p-1-get-public-merchants-code-trang-xac-minh-merchant-yeu-ca)
- [F. Phụ lục](#muc-f-phu-luc)
  - [F.1. Bảng tổng hợp TOÀN BỘ mã lỗi (danh mục đóng — 41 mã: 11 PIN + 14 OB + 16 BIZ)](#muc-f-1-bang-tong-hop-toan-bo-ma-loi-danh-muc-dong-41-ma-11-pin)
    - [F.1.1. `PIN-xxx` — 11 mã chung MMS (chuẩn gốc: A.4)](#muc-f-1-1-pin-xxx-11-ma-chung-mms-chuan-goc-a-4)
    - [F.1.2. `OB-xxx` — 14 mã Open Banking bank NHẬN (chuẩn gốc: C.0; cột cuối = mã MMS nổi lên BFF)](#muc-f-1-2-ob-xxx-14-ma-open-banking-bank-nhan-chuan-goc-c-0-cot)
    - [F.1.3. `BIZ-*` — 16 mã nghiệp vụ (luôn đi trong `PIN-422-BIZ`, HTTP 422; gốc TSD §13.1 + mở rộng)](#muc-f-1-3-biz-16-ma-nghiep-vu-luon-di-trong-pin-422-biz-http-422)
  - [F.2. Ma trận endpoint × màn hình (truy vết 2 chiều với wireframes)](#muc-f-2-ma-tran-endpoint-man-hinh-truy-vet-2-chieu-voi-wireframe)
    - [F.2.1. App người bán (NB)](#muc-f-2-1-app-nguoi-ban-nb)
    - [F.2.2. App mọi vai — chọn vai & thanh toán (CH-00 + NM) «v3.6»](#muc-f-2-2-app-moi-vai-chon-vai-thanh-toan-ch-00-nm-v3-6)
    - [F.2.3. Portal BRH](#muc-f-2-3-portal-brh)
    - [F.2.4. Console vận hành VDS (AQ)](#muc-f-2-4-console-van-hanh-vds-aq)
  - [F.3. Con dấu nội dung & THẺ RESPONSE «v3.4» — thay chuẩn JWS detached cũ](#muc-f-3-con-dau-noi-dung-the-response-v3-4-thay-chuan-jws-detach)
  - [F.4. Hồ sơ kết nạp đối tác (onboarding) «v3.2»](#muc-f-4-ho-so-ket-nap-doi-tac-onboarding-v3-2)
  - [F.5. VÍ DỤ BẢN TIN ĐẦY ĐỦ TOÀN LUỒNG «v3.4» — nhìn vào làm theo](#muc-f-5-vi-du-ban-tin-day-du-toan-luong-v3-4-nhin-vao-lam-theo)

<!-- /TOC -->

| Trường | Nội dung |
|---|---|
| Mã | Peye-Haiti-API-001 · **v3.7** — 24/08/2026 · **«v3.7» (chốt 5 câu hỏi tích hợp của dev — KHÔNG đổi endpoint/field bắt buộc/enum/mã lỗi; 109 mục/110 HTTP · OB 12 API · 41 mã · 42 màn GIỮ NGUYÊN):** ① **thẻ hệ thống chuyển sang header riêng `x-system-token`** (JWT trần — không tiền tố «Bearer») cho MỌI API đối tác nhóm B/C/D, cả hai chiều; `Authorization` từ nay CHỈ thuộc phiên người dùng BFF; route nhóm đối tác TỪ CHỐI request mang `Authorization` (chặn lẫn thẻ — 401 `details.issue="header"`); lý do: về đúng thông lệ OAuth2, hết xung đột plugin mặc định của API Gateway/middleware — A.1/A.1b.5/A.2/F.5 cập nhật, xóa ghi chú «lệch thông lệ có chủ đích»; ② **F.3 BỎ `req_sha256` với GET** (C.5/C.6/C.8) — toàn chuẩn không còn hash URL; thẻ response GET = `iss`/`aud`/`exp` + `body_sha256`; bù bằng quy tắc: MMS đối chiếu ĐỊNH DANH TRONG BODY với tài nguyên đã gọi (C.5/C.6 echo `link_id` — C.6 +trường echo top-level; C.8 sẵn `ext_payment_id`); POST giữ `req_sha256` = hash body request; ③ **A.2 chốt ca idempotency ĐANG XỬ LÝ**: bản ghi `idem_key` tạo NGAY khi bắt đầu xử lý; trùng key + cùng body khi chưa có response chốt → `409` tái dùng `PIN-409-IDEM`/`OB-409-IDEM` kèm `details.state="processing"` + `retryable=true` + `Retry-After: 1` — client GIỮ NGUYÊN key retry; có response chốt → replay như cũ; ④ **thống nhất thuật ngữ 4 trục** (vai giao diện · quyền gọi API · loại liên kết · bên giao dịch): nhãn quyền nhóm E «buyer» → **`user`** (mọi person đã đăng nhập — người bán thanh toán được); C.1/A.1b.4/C.7/E.3 gọi theo LOẠI LIÊN KẾT — **liên kết NHẬN TIỀN (receiving — `merchant_ref`, gắn gian hàng, KYC2)** / **liên kết NGUỒN TRẢ (funding — `person_ref`, gắn cá nhân, MỌI vai, KYC1)**; định chế VALIDATE BẮT BUỘC `requested_scope` theo A.1b.4 (không tin dữ liệu truyền sang); E.12 chú nghĩa `side` theo BÊN giao dịch (buyer = bên trả); ⑤ chuẩn triển khai phía dịch vụ (3 SecurityWebFilterChain + phân vùng gateway) chuyển sang TSD v4.6 §8b · **v3.6** — 20/08/2026 tối · **«v3.6» (user chốt bổ sung):** ① CH-00 chọn vai TRƯỚC eKYC (vai mua không chạy E1/E2); ② **TẠO LÀ ACTIVE** — bỏ cổng duyệt trước: E.2.2 pipeline kích hoạt NGAY khi eKYC pass + đủ hồ sơ + TK nhận; E.11.1 = danh sách HẬU KIỂM (không phải hàng chặn), E.11.2 approve = ĐÓNG hậu kiểm, reject = suspend + yêu cầu bổ sung; E2 5xx KHÔNG chặn kích hoạt (sàng lọc bù); endpoint & mã lỗi & số đếm KHÔNG đổi · **v3.5 (họp BRH 20/08 — user chốt 3 điểm):** ① **MỘT app, CHỌN VAI sau đăng ký** (mua/bán — khác nhau ở nhóm menu quản lý bán hàng; NGƯỜI BÁN THANH TOÁN ĐƯỢC như người mua): E.16 áp dụng MỌI người dùng; nút «Trở thành người bán» = kích hoạt onboarding merchant hiện có (E.2.x), app chuyển vai khi merchant `active` — KHÔNG endpoint mới; +màn CH-00 chọn vai (42 màn); ② **HAI BẬC XÁC THỰC** (bỏ trần cứng 5.000/GD): ≤ **`PAY_SCA_THRESHOLD` = 5.000 HTG** → chỉ PIN app; **> 5.000 → PIN + SMS OTP DO ĐỊNH CHẾ GỬI** (ngưỡng CHUẨN HÓA — định chế được chặt hơn, không được lỏng hơn): khôi phục **C.9 + E.16.6 + nhánh `sca_required`** trên nền an ninh v3.4 (thẻ kèm hash body); `PAY_DAY_MAX` chỉ đếm lệnh bậc-PIN; ③ rà SMS GW: OTP thanh toán = SMS GW CỦA ĐỊNH CHẾ (điều kiện kết nạp F.4, tái dùng năng lực C.2); Peye giữ nguyên N1. **Tổng 109 mục / 110 HTTP (B 5 · C 9 · D 5 · E 89 · P 1) · bộ chuẩn OB 12 API (M-PAY ×4) · 41 mã GIỮ · 42 màn** · **v3.4 (bản chốt AuthOB — 4 chỉnh sửa SA):** ① **MỘT THẺ K2 kiêm con dấu nội dung**: thẻ hệ thống A.1b thêm claim `body_sha256` = **hash body** (SHA-256 của raw body) cho MỌI request có body — thẻ dùng MỘT LẦN; GET không body: thẻ sống ≤5′ dùng lại được; **BỎ `kid` + `jti`** (JWKS thường 1 khóa — giao thời thử cả 2; chống replay = mTLS + hạn 5′ + dedup event_id/Idempotency); request KHÔNG còn `x-jws-signature` — header này chỉ còn cho THẺ RESPONSE tài chính (F.3 viết lại); ② **danh tính = TÊN TỔ CHỨC** (`iss`/`sub`/`aud` = «Peye-Haiti» · «NatCash» · «MonCash» · «UniBank»… — danh mục BRH cấp, ánh xạ 1–1 mã 9332xx); ③ **xác thực người mua thuộc PEYE-HAITI, PIN-only**: hạn mức pilot **≤ 5.000 HTG/GD** (`PAY_MAX_PILOT`) — chỉ nhập PIN app; hạn mức cao hơn + OTP = phiên bản sau; **BỎ C.9 + E.16.6 + toàn bộ nhánh `sca_*`** (định chế KHÔNG hỏi người dùng — thực thi theo token liên kết + hạn mức tự áp); ④ +**F.5 «Ví dụ bản tin đầy đủ toàn luồng»** — tài liệu nhìn-vào-làm-theo cho dev. **Tổng 107 mục / 108 HTTP (B 5 · C 8 · D 5 · E 88 · P 1) · bộ chuẩn OB 11 API (M-PAY ×3) · 41 mã lỗi GIỮ · 41 màn GIỮ** · **v3.3 cùng ngày (2 quyết định SA):** ① **thẻ hệ thống A.1b CHUYỂN VỀ `Authorization: Bearer` cho MỌI API nhóm B/C/D, cả hai chiều** — API Gateway hai phía xác thực tập trung tại cổng; token liên kết chuyển sang header MỚI **`x-account-token`** (C.5/C.6/C.7/C.9); BỎ x-client-assertion; ghi chú lệch thông lệ OAuth2 có chủ đích tại A.1b.5; ② **SCA đầy đủ — xác thực người dùng bằng SMS OTP cho lệnh trả:** +**C.9** (M-PAY.3/OB-P.4) `POST /ob/v1/payments/{id}/sca`; C.7 response thêm nhánh `status:"sca_required"` + object `sca{}`; +**E.16.6** `POST /payments/{id}/sca` (nhập OTP là TRẠNG THÁI của màn NM-03 — KHÔNG thêm màn, 41 màn giữ); trạng thái payment +`sca_required` (TSD §6b) · `failure_reason` +`sca_failed` (giá trị dữ liệu); mã lỗi GIỮ 41 — tái dùng OB-422-OTP/OB-423-LOCK (+C.9) · OB-404-LINK mở nghĩa «định danh tài nguyên» (+C.8/C.9) · BIZ-OTP-INVALID (+E.16.6); ngưỡng kích hoạt SCA = chính sách của định chế; **tổng 109 mục / 110 HTTP (B 5 · C 9 · D 5 · E 89 · P 1) · bộ chuẩn OB 12 API (M-PAY ×4)** · **19/08 (AN NINH ĐỐI TÁC — chốt mô hình B «JWT tự ký», theo rà soát authen/authz):** +**A.1b «Danh tính hệ thống đối tác — JWT tự ký (private_key_jwt)»**: KHÔNG token endpoint — bên gọi tự ký JWT ES256 bằng khóa đã công bố trong JWKS (CHUNG bộ khóa với chữ ký F.3); ruột thẻ chuẩn `iss=sub=client_id` (mã định chế BRH cấp) · `aud`=bên nhận · `exp≤300s` · `jti` duy nhất (JWT MỚI cho từng request) · verify 5 bước đối xứng hai chiều; +**A.1b.4 bảng scope token OB chuẩn** (C.1/C.2 quy chiếu); **C.7 bắt buộc ký JWS detached trên REQUEST** (`x-jws-signature`, F.3 — lệnh trả = thông điệp tài chính, đồng bộ lời hứa MOU A.6.1; lỗi chữ ký phía bank trả `OB-401-AUTH` kèm `details.issue="jws"` — danh mục 41 mã GIỮ NGUYÊN); F.3 mở rộng phạm vi áp dụng (+ request C.7) + ghi chú JWKS dùng chung (thẻ hệ thống + con dấu bản tin); A.2 cập nhật mô tả `x-jws-signature`; +**F.4 «Hồ sơ kết nạp đối tác»** (bảng thông số trao 1 lần + trình tự sandbox→chứng nhận→production + bộ vector auth `/docs/auth-vectors/`); mọi chỗ «JWT client-credentials» đọc là mô hình A.1b; **endpoint & mã lỗi KHÔNG đổi (107 mục / 108 HTTP · 41 mã)** · **16/08 (B.5 QR-inquiry — góp ý SA: «app định chế phải TRA CỨU vào Peye-Haiti trước, lệnh trả mới đi đường Open Banking/nội bộ»):** +**B.5** `POST /qr-inquiry` — app/backend định chế TRẢ gọi VÀO Peye-Haiti sau khi quét HTQR: xác minh TÊN/trạng thái merchant + bill/số tiền + nhận `payment_ref` (TTL 15′) đem theo lệnh chuyển · B.1 `addenda` +`payment_ref` optional → nhánh khớp tự động ① thành ĐÍCH DANH (hết lệ thuộc thuần số tiền khi app định chế có mạng; offline-first A9 GIỮ NGUYÊN — không gọi được B.5 vẫn trả như cũ) · tổng **107 mục / 108 HTTP** (B 5 · C 8 · D 5 · E 88 · P 1) · mã lỗi GIỮ 41 (không mã mới — dùng PIN-400-VAL/PIN-404-NF/PIN-429-RATE; không trả được = dữ liệu `payable:false`) · **15/08 (Peye-Haiti — app chung, mô hình BiMPay):** đổi tên PINASSI→HaitiPay (domain `peye-haiti.ht`; prefix `PIN-` giữ); +module NGƯỜI MUA: nhóm **E.16** (5 endpoint app profile Client) · **P.1** trang công khai xác minh merchant · **C.7/C.8** M-PAY khởi tạo trả (bank TRẢ expose) · **B.4** webhook kết quả trả — tổng **106 mục / 107 HTTP** (B 4 · C 8 · D 5 · E 88 · P 1); mã lỗi GIỮ 41 (thất bại thanh toán = dữ liệu `payment.failure_reason`, không phải mã lỗi mới) · **15/08 (CR BRH)**: E.4.1/E.4.7 payload theo HTQR 1.0 + trường `mcc` (CR-1/3) · B.1 +2 trường optional `payer.person_id`/`payer.operator` (CR-7) · E.2.2 +`nif_no` optional (CR-5) · nguyên tắc «3 KHÔNG» dữ liệu ra hệ thống quốc gia (CR-8); **endpoint & mã lỗi KHÔNG đổi số lượng** — theo `BRH/PeyeHaiti_CR_BRH_LuuTru_NhatKy.md` (đối chiếu văn bản BRH 12/08) · **04/08**: F.2.4 hoán đúng vai AQ-00 ↔ AQ-01 (khớp thân tài liệu + wireframes); bỏ màn BRH-09 «Cấu hình» — tham số qua E.13.x, vận hành Natcom · **02/08**: rút gọn pilot (S1–S10) — gỡ mở-TK-mới-qua-API, gỡ bắn-lại-báo-có của bank (phục hồi = M3-poll quét lịch sử + đối soát E3), gỡ khai báo QR động best-effort (khớp thuần số tiền + cửa sổ), gỡ app người mua (endpoint danh bạ/biên lai buyer), gỡ đặt lịch email báo cáo định kỳ · mục C đánh số lại **C.0–C.6** (6 endpoint OB — GIỮ M3 số dư theo yêu cầu 02/08) · matching còn **2 mức** · mã lỗi **44→41** (11 PIN + 14 OB + 16 BIZ) · chốt **97 mục / 98 HTTP endpoint** (B3 · C6 · D5 · E83) · **v2.3** 25/07/2026: bỏ API M5 (đối chiếu tên — bank tự xác thực qua OTP) + gộp còn 1 bậc KYC · sắp xếp mục C theo luồng onboarding · tích hợp 17→15, mã lỗi 48→44 · đồng bộ tên ví Natcash→wallet2 (NatTransfer), mã ví dụ NATC→NTRF (đồng bộ quyết định chốt: tên dịch vụ nội bộ remap sang **4 dịch vụ** — đối soát/AML nay thuộc module Compliance của **Back-office**; event bus **Kafka** (DLQ `<topic>.dlq`); **endpoint giữ nguyên**. Nền v1.2: vá preamble F.2 — NB-01/NB-03 có gọi API; chốt 91 mục / 93 HTTP endpoint) |
| Nguồn | `PeyeHaiti_TSD.md` (§1 chuẩn API, §2/§2b/§2c contract, §3 M4, §13.1/§13.3) · `PeyeHaiti_SSD.md` (§5 S1–S9, §7) · `PeyeHaiti_PRD.md` (AC, hạn mức D5) |
| Mục tiêu | Đủ chi tiết TỪNG TRƯỜNG + MÃ LỖI TỪNG ENDPOINT để dev code không phải hỏi lại; là nguồn sinh OpenAPI YAML (`/docs/openapi/bff.yaml`, `/docs/openapi/partner.yaml`, `/docs/openapi/ob-client.yaml`) |
| Phạm vi | (A) chuẩn chung · (B) API MMS expose cho đối tác · (C) Open Banking bank NHẬN expose · (D) BRH-System + Switch + Natcom · (E) BFF app/portal · (F) phụ lục mã lỗi, ma trận màn hình, chuẩn JWS, hồ sơ kết nạp đối tác |
| Ràng buộc đã chốt | KHÔNG có VA/M2/M6/M6b/USSD/N2 (USSD: chỉ là giá trị enum kênh tra cứu B.5 cho GĐ2 — không có luồng USSD trong pilot). M4 do BANK NHẬN cung cấp (không phải ACI/Switch). Tiền = `BIGINT` centime HTG (1 G = 100 ct). QR do client render offline. Go-live 01/10/2026. |

---

<a id="muc-a-chuan-chung"></a>
## A. Chuẩn chung

<a id="muc-a-1-base-url-nhom-xac-thuc"></a>
### A.1. Base URL & nhóm xác thực

| # | Nhóm | Base URL | Chiều | AuthN |
|---|---|---|---|---|
| 1 | BFF app người bán / người mua / portal BRH / console AQ | `https://api.peye-haiti.ht/v1` | client → MMS | OAuth2 password+PIN → **JWT ES256** access 15 phút / refresh 30 ngày (app), gắn `device_id`; portal: email + mật khẩu + TOTP (2FA), access 15 phút / refresh 12 giờ |
| 2 | Partner inbound (đối tác gọi VÀO MMS): webhook M4, **kết quả trả M-PAY (B.4)**, **tra cứu QR (B.5)**, DLR SMS, thông báo file E3 | `https://partner.peye-haiti.ht/v1` | đối tác → MMS | **mTLS** (cert riêng per đối tác, TLS 1.2+) + **thẻ hệ thống TỰ KÝ theo A.1b ở header `x-system-token`** (`aud="Peye-Haiti"`) — request có body thì thẻ kèm **hash body** (`body_sha256`) + IP allowlist |
| 3 | Open Banking bank NHẬN (MMS gọi RA) | `https://ob.{bank}.ht/ob/v1` (domain thực theo hợp đồng D2; sandbox bắt buộc T7/2026) | MMS → bank | mTLS + **thẻ hệ thống TỰ KÝ của MMS theo A.1b, đặt ở header riêng `x-system-token` (JWT trần)** (`aud=` TÊN định chế, vd `"UniBank"`); API theo tài khoản mang thêm token liên kết ở header **`x-account-token`** (A.1b.5); request có body → thẻ kèm hash body («v3.4» — C.7 nhờ đó tự chống chối bỏ); **response tài chính bank ký THẺ RESPONSE** (F.3) |
| 4 | BRH-System (E1/E2) · Switch (E3, E3-reg) · Natcom (N1) | `https://brh-system.gov.ht` · `https://switch.brh.ht` · `https://sms.natcom.ht` (đại diện — chốt theo hợp đồng) | MMS → đối tác | mTLS + thẻ hệ thống tự ký (A.1b — hoặc phương án tương đương chốt tại hợp đồng kênh từng đối tác); E3 file ký số; SFTP dự phòng cho E3 |
| P | **Công khai** (không xác thực): trang xác minh merchant «Peye-Haiti 15/08» | `https://api.peye-haiti.ht/public` | mọi người → MMS | Không auth · rate-limit theo IP · chỉ dữ liệu công khai (P.1) |

- Mọi kết nối đối tác đi qua VPN site-to-site + IP allowlist. Versioning: path `/v1`; thay đổi phá vỡ tương thích → `/v2`, chạy song song ≥6 tháng.
- Circuit breaker per đối tác: mở khi 50% lỗi / 20 request, half-open 30s (TSD §10). Khi mở → BFF trả `PIN-503-DEP`.


<a id="muc-a-1b-the-he-thong-tu-ky-mot-the-cho-ca-danh-tinh-lan-noi-dun"></a>
### A.1b. Thẻ hệ thống TỰ KÝ — MỘT thẻ cho cả DANH TÍNH lẫn NỘI DUNG «v3.4»

> Trả lời dứt điểm câu «JWT do bên nào phát hành, kiểm bằng gì»: **không có máy chủ cấp token nào cả.** Bên gọi tự ký JWT ngắn hạn bằng khóa riêng của mình; bên nhận kiểm bằng khóa công khai mà bên gọi đã công bố qua JWKS. «v3.4»: thẻ này **kiêm luôn con dấu nội dung** — request có body thì khắc **hash body** (`body_sha256`) vào chính thẻ; không còn chữ ký JWS tách rời cho request. Một bên tham gia chỉ cần **một cặp khóa + một URL JWKS + một hàm verify**. Mô hình đối xứng: Peye-Haiti kiểm định chế đúng như định chế kiểm Peye-Haiti.

**A.1b.1. Phát hành (phía bên gọi):** request **CÓ BODY** → sinh thẻ MỚI cho từng request (có `body_sha256` — thẻ gắn chặt body đó, retry phải ký lại với `iat` mới); request **KHÔNG body** (GET) → thẻ không có `body_sha256`, được dùng lại tới khi hết hạn (≤5′). Ký ES256 bằng khóa riêng — mỗi bên MỘT cặp khóa hiệu lực, không phải chọn khóa.

**A.1b.2. Ruột thẻ chuẩn (claims — bắt buộc đủ, không thêm bớt nghĩa):**

| Trường | Quy định | Ví dụ |
|---|---|---|
| header `alg` | Chỉ `ES256` — danh sách trắng, từ chối mọi giá trị khác (kể cả `none`) | `"ES256"` |
| header `typ` | `"JWT"` | — |
| `iss` = `sub` | **TÊN TỔ CHỨC bên gọi** theo danh mục BRH cấp («v3.4» — danh từ gần gũi cho dev): `"NatCash"` · `"MonCash"` · `"UniBank"` · `"Sogebank"`…; nền tảng = `"Peye-Haiti"`. Ánh xạ 1–1 với mã 9332xx (mã số vẫn dùng trong QR tag định chế + danh bạ; hồ sơ kết nạp F.4 ghi cả hai) | `"NatCash"` |
| `aud` | **TÊN bên nhận** («v3.4»): thẻ gọi vào nền tảng: `"Peye-Haiti"`; nền tảng gọi ra: tên định chế (`"UniBank"`…). Thẻ sai `aud` bị từ chối (không dùng lại được cho bên thứ ba) | `"Peye-Haiti"` |
| `iat` / `exp` | Thời điểm ký / hết hạn; **`exp − iat ≤ 300 giây`**; lệch đồng hồ cho phép ±30s (NTP bắt buộc như F.3) | — |
| `body_sha256` | «v3.4» — **hash body**: SHA-256 (hex, chữ thường) của **raw body bytes**; BẮT BUỘC khi request có body, KHÔNG có với GET. Lệch 1 byte là hash lệch — thẻ chính là con dấu nội dung | `"9f2a4c…e81d"` |

**A.1b.3. Trình tự kiểm thẻ (tối đa BA bước «v3.4» — đối xứng hai chiều, fail bước nào dừng bước đó):**

1. Lấy **JWKS của bên gọi theo `iss` trong thẻ** (cache 1h; bảng thường chỉ 1 khóa — lúc bên gọi giao thời thay khóa thì có 2, thử lần lượt; fail hết → refresh đúng 1 lần rồi thôi, negative-cache 5 phút).
2. Gọi MỘT lệnh thư viện: `jwt.verify(thẻ, khóa, {alg:["ES256"], aud:"tên mình"})` — thư viện tự kiểm chữ ký · hạn thẻ · đúng người nhận (dung sai giờ ±30s, NTP bắt buộc).
3. Thẻ có `body_sha256` → tự tính hash body nhận được, so khớp; **khớp mới parse JSON** + khử trùng `event_id`/`Idempotency-Key`; dữ liệu phải THUỘC đúng bên đang gọi (thẻ nói «tôi là NatCash» → kiểm bằng JWKS NatCash; báo Có của liên kết nhà ai chỉ nhà ấy được báo).

Sai bước nào: MMS trả `PIN-401-AUTH` (danh tính: `details.issue` = `alg`/`sig`/`aud`/`expired`/`header` — «header» = gửi nhầm thẻ vào `Authorization` trên route đối tác) hoặc `PIN-401-JWS` (nội dung: `details.issue` = `body-hash`/`body-hash-missing`); chiều định chế trả `OB-401-AUTH` cùng quy ước. **Chống phát lại: mTLS bó kênh + hạn thẻ 5′ + khử trùng `event_id`/`Idempotency-Key` — KHÔNG kho `jti`, KHÔNG `kid`.** Danh mục 41 mã giữ nguyên.

**A.1b.4. Bảng scope chuẩn của token liên kết tài khoản (nguồn quy chiếu duy nhất — C.1/C.2 dẫn về đây):**

| Scope | Quyền | Liên kết NHẬN TIỀN (receiving — gắn gian hàng, `merchant_ref`) | Liên kết NGUỒN TRẢ (funding — gắn cá nhân, `person_ref`, MỌI vai) |
|---|---|---|---|
| `balance` | Đọc số dư (C.5) | ✔ mặc định | — |
| `history` | Đọc lịch sử (C.6) | ✔ mặc định | ✔ |
| `credit-notify` | Bank bật gửi báo Có M4 cho link (B.1) | ✔ mặc định | — |
| `payment` | Khởi tạo lệnh trả từ TK nguồn (C.7) + xác nhận OTP lệnh trả (C.9 «v3.5») | — | ✔ |

Token thiếu scope khi DÙNG → `OB-403-SCOPE`. **Định chế VALIDATE BẮT BUỘC tại C.1 — không tin `requested_scope` truyền sang:** liên kết nhận tiền chỉ nhận ⊆ {`balance` · `history` · `credit-notify`}, liên kết nguồn trả chỉ nhận ⊆ {`payment` · `history`}; xin ngoài tổ hợp → từ chối NGAY tại C.1 (400 validate — không cấp-rồi-cắt); token cấp đúng bộ đã duyệt, không tự nới. Triển khai phía định chế bằng BẢNG CẤU HÌNH đánh phiên bản theo chuẩn (không hard-code) — thêm scope mới = CR nâng phiên bản bộ chuẩn OB + bộ vector mới.

**A.1b.5. Cách đặt thẻ trong request:**

- **MỘT quy tắc cho mọi API đối tác (nhóm B · C · D, cả HAI chiều): thẻ hệ thống A.1b luôn nằm ở header riêng `x-system-token`** — giá trị là JWT TRẦN (không tiền tố «Bearer» — cùng kiểu với `x-account-token`). API Gateway của cả hai phía xác thực thẻ hệ thống tập trung ngay tại cổng, tầng ứng dụng phía sau không phải làm lại. `Authorization` từ nay CHỈ thuộc phiên người dùng BFF (nhóm E); **route nhóm đối tác TỪ CHỐI request mang `Authorization`** — trả 401 (`PIN-401-AUTH`/`OB-401-AUTH`) kèm `details.issue="header"`, để bắt lỗi lẫn thẻ/cấu hình nhầm ngay từ sandbox.
- **Token liên kết** (định chế cấp tại C.2) đi ở header riêng **`x-account-token`** với các API theo tài khoản: C.5 · C.6 · C.7 · C.9. API không dùng token liên kết chỉ cần thẻ hệ thống (`x-system-token`): C.1 · C.2 (token chỉ SINH RA trong response) · C.3 (refresh_token nằm trong body) · C.4 · **C.8** (lưới đỡ — phải chạy cả khi token liên kết hết hạn/thu hồi).
- *Ghi chú thông lệ:* cách đặt này VỀ ĐÚNG thông lệ — `Authorization` không bị trưng dụng cho danh tính hệ thống, nên plugin OAuth2 mặc định của mọi API Gateway/middleware không còn chặn nhầm; ba header ba tầng đọc là hiểu: `Authorization` = phiên NGƯỜI DÙNG · `x-system-token` = danh tính TỔ CHỨC · `x-account-token` = ưng thuận TÀI KHOẢN. Bộ vector sandbox (A.1b.6/F.4) ép mọi bên cùng một kiểu.
- **Nhóm D:** như trên, hoặc phương án tương đương chốt tại hợp đồng kênh từng đối tác.
- Nhóm 1 (BFF app/portal) KHÔNG thuộc mục này — người dùng cuối xác thực OAuth2 password+PIN như bảng A.1 nhóm 1 (máy chủ danh tính nội bộ — xem TSD).

**A.1b.6. Bộ ca kiểm thử bắt buộc (sandbox — điều kiện chứng nhận kết nối, xem F.4):** thẻ đúng (GET + POST) · sai `alg` · sai chữ ký · sai `aud` · hết hạn · **thiếu `body_sha256` khi có body** · **hash body lệch (body đổi 1 byte)** · **gửi nhầm thẻ vào `Authorization` trên route đối tác (→ 401 `details.issue="header"`) «v3.7»** — bên tích hợp phải ĐẠT toàn bộ (đọc đúng thẻ hợp lệ, từ chối đúng thẻ hỏng). Vector mẫu tại `/docs/auth-vectors/` (bộ duy nhất — jws-vectors cũ gộp vào đây).

<a id="muc-a-2-header-chuan"></a>
### A.2. Header chuẩn

| Header | Chiều | Bắt buộc | Mô tả |
|---|---|---|---|
| `Authorization: Bearer {jwt}` | request | Nhóm E (trừ E.1 công khai) | **CHỈ BFF** = JWT phiên người dùng (kid rotation 90 ngày); route nhóm đối tác từ chối header này (A.1b.5) |
| `x-system-token: {jwt}` | request | Nhóm B · C · D (mọi chiều) | **Thẻ hệ thống A.1b — JWT TRẦN, thống nhất MỌI chiều đối tác**; API Gateway hai phía xác thực tập trung tại cổng |
| `x-account-token: {access_token}` | request (MMS → định chế: C.5/C.6/C.7/C.9) | Có theo A.1b.5 | Token liên kết định chế cấp tại C.2 — tầng ứng dụng OB của định chế kiểm scope theo A.1b.4 |
| `Idempotency-Key: {uuid v4}` | request | Có với MỌI POST ghi | TTL **48h** (bảng `idem_key` — bản ghi tạo NGAY khi bắt đầu xử lý); trùng key + cùng body ĐÃ có response chốt → replay response cũ kèm header `Idempotency-Replayed: true`; trùng key + cùng body nhưng request trước CHƯA có response chốt (đang xử lý) → `409 PIN-409-IDEM` kèm `details.state="processing"` + `retryable=true` + `Retry-After: 1` — client GIỮ NGUYÊN key và retry backoff, tuyệt đối không sinh key mới; trùng key + body KHÁC → `PIN-409-IDEM` (retryable=false) |
| `Accept-Language: fr` \| `ht` | request | Không (mặc định `ht`) | Ngôn ngữ của `error.message` và text hiển thị (fr = tiếng Pháp, ht = Kreyòl) |
| `X-Device-Id: {uuid}` | request (app) | Có với app NB | Fingerprint phiên thiết bị — gắn phiên với thiết bị, truy vết phiên hỗ trợ hiện trường |
| `x-jws-signature` | **response** («v3.4» — request KHÔNG còn dùng) | Có với RESPONSE tài chính: C.5 · C.6 · C.7 · C.8 · C.9 | **Thẻ response** cùng định dạng A.1b (có `body_sha256` của body trả về) — chuẩn tại F.3 |
| `X-Trace-Id` | response | Luôn | Trùng `error.trace_id`; gắn OpenTelemetry, nối `ref_id`/`event_id` xuyên service |
| `Retry-After: {giây}` | response | Khi 429/503 · 409 idempotency đang-xử-lý («v3.7») | Client/đối tác chờ đúng số giây trước khi thử lại |
| `Content-Type: application/json; charset=utf-8` | cả hai | Có | Ngoại lệ: upload media = `multipart/form-data` |

<a id="muc-a-3-envelope-loi-moi-api-moi-nhom"></a>
### A.3. Envelope lỗi (mọi API mọi nhóm)

```json
{
  "error": {
    "code": "PIN-422-BIZ",
    "biz_code": "BIZ-OTP-INVALID",
    "message": "Kòd OTP a pa bon oswa li ekspire (fr/ht theo Accept-Language)",
    "trace_id": "3f9d2c81a4b04c6e",
    "retryable": false,
    "details": [
      { "field": "otp", "issue": "invalid", "hint": "Còn 2 lần thử" }
    ]
  }
}
```

| Trường | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `error.code` | string | Có | Mã lỗi máy đọc: `PIN-xxx-YYY` (MMS) · `OB-xxx-YYY` (bank) · `E1/E2/E3/N1-xxx-YYY` (đối tác khác) |
| `error.biz_code` | string | Chỉ khi `code=PIN-422-BIZ` | Mã nghiệp vụ `BIZ-*` (danh mục F.1.3, gốc TSD §13.1) |
| `error.message` | string | Có | Cho người đọc, đã bản địa hóa fr/ht; app KHÔNG hiện mã kỹ thuật cho người bán (UX-6) |
| `error.trace_id` | string | Có | Mã truy vết tương quan (= `ref_id` trong error model TSD §1 — đổi tên để không nhầm với RefID của Switch; ý nghĩa không đổi) |
| `error.retryable` | bool | Có | `true` với nhóm 5xx/429 và riêng ca 409 idempotency đang-xử-lý (`details.state="processing"` «v3.7»); client retry backoff 1s→2s→4s tối đa 3 lần, GIỮ NGUYÊN `Idempotency-Key`. **Không bao giờ tự hoàn tiền theo lỗi 5xx** |
| `error.details[]` | array | Không | Từng vi phạm: `field` (JSON pointer hoặc tên trường), `issue` (mã ngắn: `required`, `format`, `min`, `max`, `enum`, `limit_exceeded`, `state`, …), `hint` (gợi ý sửa) |

<a id="muc-a-4-bang-ma-loi-chung-moi-endpoint-deu-co-the-tra-bang-loi-r"></a>
### A.4. Bảng mã lỗi CHUNG (mọi endpoint đều có thể trả — bảng lỗi riêng từng endpoint chỉ liệt kê lỗi ĐẶC THÙ)

| Mã | HTTP | Nghĩa | Khi nào | retryable |
|---|---|---|---|---|
| `PIN-400-VAL` | 400 | Validate dữ liệu vào | Thiếu trường bắt buộc, sai kiểu/format/enum, JSON hỏng, vượt kích thước (batch >200 entry / body >500KB / ảnh >200KB) | false |
| `PIN-401-AUTH` | 401 | Không xác thực được | JWT thiếu/hết hạn/sai chữ ký/sai `aud`; mTLS cert sai/revoked; sai PIN/mật khẩu/TOTP (kèm `details.attempts_left`) | false |
| `PIN-401-JWS` | 401 | Hash body trong thẻ không khớp | «v3.4»: thẻ thiếu `body_sha256` khi request có body, hoặc hash lệch với body nhận được (`details.issue` = `body-hash`/`body-hash-missing`) — danh tính sai thì là `PIN-401-AUTH` | false |
| `PIN-403-SCOPE` | 403 | Đúng danh tính, thiếu quyền | Sai vai trò RBAC, token OB thiếu scope, truy cập tài nguyên của merchant khác | false |
| `PIN-404-NF` | 404 | Không tìm thấy | Resource id không tồn tại hoặc không thuộc quyền nhìn của caller (không phân biệt để chống dò) | false |
| `PIN-409-IDEM` | 409 | Idempotency conflict | Trùng `Idempotency-Key`: body KHÁC lần trước (retryable=false) HOẶC cùng body nhưng lần trước đang xử lý — `details.state="processing"` (retryable=true, giữ key retry theo `Retry-After`) | false · processing: true |
| `PIN-409-STATE` | 409 | Sai trạng thái / xung đột version | Chuyển trạng thái không hợp lệ theo state machine; optimistic lock thua (`details.server_state` chứa trạng thái server hiện tại) | false |
| `PIN-422-BIZ` | 422 | Vi phạm quy tắc nghiệp vụ | Dữ liệu hợp lệ về hình thức nhưng nghiệp vụ từ chối — LUÔN kèm `biz_code` (F.1.3) | false |
| `PIN-429-RATE` | 429 | Vượt rate limit | Vượt hạn ngạch endpoint/thiết bị/OTP/SMS — kèm `Retry-After` | true |
| `PIN-500-SYS` | 500 | Lỗi hệ thống MMS | Exception chưa phân loại, DB lỗi | true |
| `PIN-503-DEP` | 503 | Phụ thuộc không sẵn sàng | Circuit breaker đối tác đang mở, bảo trì có kế hoạch — kèm `Retry-After` | true |

> Quy ước đọc tài liệu: mục «Lỗi» của từng endpoint bên dưới KHÔNG lặp lại 11 mã chung này trừ khi endpoint có ngữ nghĩa riêng (ví dụ 404 của webhook M4 có hành vi retry riêng của bank).

<a id="muc-a-5-quy-uoc-du-lieu-ap-cho-moi-api-trong-tai-lieu"></a>
### A.5. Quy ước dữ liệu (áp cho mọi API trong tài liệu)

| Chủ đề | Quy ước |
|---|---|
| Tiền | `amount_ct` / `*_ct`: **int64 (BIGINT), đơn vị centime HTG**, 1 Gourde = 100 ct, luôn > 0 trừ khi ghi rõ; `currency` luôn `"HTG"` (hiển thị USD chỉ là quy đổi client-side theo tham số C5, KHÔNG có trường USD trong API) |
| Thời gian | RFC3339/ISO8601 UTC, hậu tố `Z`: `2026-10-01T13:24:05Z`; `biz_date` = `YYYY-MM-DD` theo giờ Haiti `America/Port-au-Prince` |
| SĐT | `msisdn` chuẩn **E.164**: `+50937123456`; trường masked giữ 4 số cuối: `+509****3456` |
| ID | `*_id` phía MMS = **UUID v7** (PK server sinh — sắp theo thời gian); `client_uuid` & `Idempotency-Key` = **UUID v4** (client sinh); id đối tác (`link_id` bank cấp, `event_id`, `ref_id`, `sms_id`) = string ≤64, opaque — KHÔNG parse cấu trúc |
| Mã hiển thị | merchant `PIN-M-000241` · bill `B-<ddMM>-<seq>` (`B-1007-17`, seq client reset theo ngày) · RefID Switch `PIN-2026-000123` · case `CS-2026-000045` |
| Phân trang | Query `?page_size` (mặc định 20, **≤100**) `&cursor` (opaque base64, do server phát); response `{ "items": [...], "next_cursor": "..." \| null }`; cursor hết hạn/sai → `PIN-400-VAL` |
| Sắp xếp | Mặc định mới nhất trước (`created_at`/`booked_at` DESC) trừ khi ghi khác |
| Envelope thành công | KHÔNG bọc — 2xx trả thẳng object/list như đặc tả; lỗi LUÔN bọc envelope A.3 |
| Idempotency offline | Thực thể client tạo offline (`bill`, `bill_item`, `ledger_entry`, `debtor`, `product`) mang `client_uuid` (UUID v4 do client sinh, unique toàn cục): trùng `client_uuid` + payload GIỐNG → server trả bản ghi cũ (2xx, idempotent); trùng + payload KHÁC → `PIN-422-BIZ` / `BIZ-DUP-CLIENT-UUID` |
| Enum & tên trường | `snake_case`; enum chữ thường; trường mới thêm phải optional (backward-compatible) — client BỎ QUA trường lạ |
| Rate limit BFF | Mặc định 60 req/phút/token (đề xuất, cấu hình được); OTP ≤5 lần gửi/ngày/số (`OTP_MAX_PER_DAY`); SMS ≤5/giờ/merchant trừ OTP (`SMS_RATE_LIMIT`) |
| Retry phía client | Chỉ khi `retryable=true`: backoff 1s→2s→4s, tối đa 3; POST luôn kèm lại đúng `Idempotency-Key` |
| Tham số `UPPER_CASE` | Là key trong bảng `param` (TSD §13.3), đổi qua `E.13.3`/`E.13.4` (vận hành Natcom, 4 mắt — màn portal BRH-09 đã bỏ 04/08) — giá trị ghi trong tài liệu là mặc định |

---

> **Nguyên tắc dữ liệu RA hệ thống quốc gia (3 KHÔNG — CR-8, 15/08):** mọi khai báo/báo cáo MMS gửi cho nhật ký giao dịch quốc gia, RNI hay BRH KHÔNG BAO GIỜ chứa ① chuỗi QR thô, ② bí mật sống (token OAuth/chữ ký HMAC — chỉ gửi mã khóa/băm), ③ số tài khoản đầy đủ (chỉ bản che). Bản đồ khai báo nhóm A–G: DataDict §6.

<a id="muc-b-api-mms-expose-cho-doi-tac-https-partner-peye-haiti-ht-v1"></a>
## B. API MMS expose cho đối tác — `https://partner.peye-haiti.ht/v1`

> Chuẩn chung nhóm B: mTLS + thẻ hệ thống tự ký theo **A.1b** (danh tính = TÊN tổ chức BRH cấp, vd `iss:"NatCash"` · `aud:"Peye-Haiti"`); request có body → thẻ kèm **hash body** («v3.4» — không còn x-jws-signature cho request). MMS trả lời ≤2s, xử lý sau đó async. **Quy tắc retry đối tác: 4xx = KHÔNG retry (lỗi dữ liệu/cấu hình → DLQ phía đối tác + kênh vận hành D8); 429 = retry theo `Retry-After`; 5xx = retry backoff.**

<a id="muc-b-1-post-credit-events-webhook-bao-co-m4-bank-nhan-mms-duong"></a>
### B.1. `POST /credit-events` — Webhook báo có M4 (bank NHẬN → MMS) — ĐƯỜNG GĂNG

Bank NHẬN bắn 1 request cho MỖI bút toán ghi Có vào tài khoản đã liên kết (mọi kênh: qua Switch lẫn on-us nội bộ bank). Nguồn của «ting ting»; SLA P95 ≤5s từ T0 (bank ghi Có) tới T1 (app ack).

**Headers riêng:** KHÔNG có (thẻ hệ thống ở `x-system-token` đã kèm `body_sha256`, xem A.1b). Không dùng `Idempotency-Key` — `event_id` chính là khóa idempotent. **Giới hạn body: ≤64KB** — vượt trả `413` (xem bảng lỗi).

**Request:**

| Trường | Kiểu | Bắt buộc | Mô tả | Ví dụ |
|---|---|---|---|---|
| `event_id` | string ≤64 | **Có** | UUID do bank sinh, **duy nhất toàn cục vĩnh viễn** (dedup tầng 1) | `"9b2f0c4e-71d3-4a8e-b1aa-0f3c9d2e5a10"` |
| `link_id` | string ≤64 | **Có** | Định danh TK liên kết do bank cấp từ M1 — mọi TK nhận đều qua liên kết (D2); MMS map `account_link.ext_link_id` → merchant | `"lnk_01HX4Y7Q2K"` |
| `account_no_masked` | string ≤32 | Không | Chỉ để hiển thị, 4 số cuối | `"…7709"` |
| `ref_id` | string ≤64 \| null | Có điều kiện | RefID do Switch sinh — **BẮT BUỘC với GD qua Switch; NULL với GD on-us** (nội bộ bank, không qua Switch, E3 bỏ qua) | `"PIN-2026-000123"` |
| `amount_ct` | int64 | **Có** | Số tiền ghi Có, centime HTG, > 0 | `150000` |
| `currency` | string(3) | **Có** | Luôn `"HTG"` — giá trị khác → từ chối | `"HTG"` |
| `booked_at` | RFC3339 | **Có** | Thời điểm bank GHI CÓ (T0 đo SLA); không dùng chống replay (đó là việc của hạn thẻ A.1b ≤5′) | `"2026-10-01T13:24:05Z"` |
| `payer` | object | **Có** | Thông tin người trả (nuôi biên lai & khớp bill) — bắt buộc **ít nhất một trong** `msisdn` / `holder_name` | — |
| `payer.msisdn` | E.164 | Có điều kiện | SĐT người trả (dùng đối chiếu và gửi biên lai qua SMS) | `"+50937123456"` |
| `payer.holder_name` | string ≤140 | Có điều kiện | Tên người trả, bank được phép mask một phần | `"J. PIERRE"` |
| `payer.bank_code` | string(4) | Không | Mã bank/ví bên trả theo danh mục BRH | `"NTRF"` |
| `payer.person_id` | string ≤64 | Không | PersonID quốc gia (mã đục RNI) của người trả — trường CHỜ «CR-7 15/08»: định chế gửi khi liên thông quốc gia bật; lưu `credit_event.payer_person_id` | `"prn_9f2a…"` |
| `payer.operator` | string(6) | Không | Mã định chế bên trả dải 9332xx (HTQR) — trường CHỜ «CR-7 15/08», về sau thay `bank_code` 4 ký tự; lưu `credit_event.payer_operator` | `"933201"` |
| `narrative` | string ≤280 | Không | Nội dung chuyển khoản — KHÔNG tin cậy để khớp (A5), chỉ hiển thị | `"toi da chuyen tien rau"` |
| `addenda` | object | Không | Dữ liệu cấu trúc bảo toàn từ QR (tag 62) — chỉ khi D1/D2 bảo toàn | — |
| `addenda.bill_id` | string ≤32 | Không | Mã bill từ QR động loại ③ → gạch mức ① trực tiếp | `"B-1007-17"` |
| `addenda.payment_ref` | string ≤40 | Không | «Peye-Haiti 16/08»: tham chiếu do **B.5** cấp khi app định chế tra cứu QR trước khi trả — có mặt → khớp mức ① ĐÍCH DANH (tra Redis `qrinq:{ref}`), ưu tiên trên `bill_id` | `"qi_01JD8Z…"` |

**Response `200` (luôn ≤2s, mọi xử lý matching/notification async):**

| Trường | Kiểu | Mô tả | Ví dụ |
|---|---|---|---|
| `status` | enum | `accepted` = đã nhận vào hàng xử lý · `duplicate` = `event_id` (hoặc `ref_id` tầng 2 với cùng amount+link) đã tồn tại — bank coi như thành công, KHÔNG gửi lại | `"accepted"` |
| `event_id` | string | Echo lại để bank đối chiếu log | — |

**Lỗi & hành vi retry của bank:**

| HTTP | Mã | Khi nào | Bank làm gì |
|---|---|---|---|
| 400 | `PIN-400-VAL` | Thiếu trường bắt buộc; `amount_ct ≤ 0`; `currency ≠ HTG`; thiếu cả `payer.msisdn` lẫn `payer.holder_name`; GD qua Switch mà `ref_id=null` không chứng minh được on-us | KHÔNG retry — vào DLQ bank, sửa dữ liệu, đối chiếu bù qua E3 + M3-poll |
| 413 | `PIN-400-VAL` | Body vượt giới hạn **64KB** của webhook M4 (v1.1) | KHÔNG retry — rút gọn `narrative`/`addenda` rồi gửi lại; lặp lại → DLQ bank + kênh vận hành D8 |
| 401 | `PIN-401-AUTH` | mTLS/JWT sai, cert hết hạn | KHÔNG retry tự động — cảnh báo vận hành 2 bên (D8); sau khi sửa, bù bằng M3-poll + đối soát E3 |
| 401 | `PIN-401-JWS` | Hash body trong thẻ lệch/thiếu («v3.4»). Lưu ý: bank phải **ký thẻ MỚI (iat mới, hash đúng body) ở MỖI lần gửi, kể cả retry** | KHÔNG retry với thẻ cũ — ký thẻ mới rồi gửi; lặp lại lỗi → DLQ + cảnh báo |
| 404 | `PIN-404-NF` | `link_id` không tồn tại, hoặc đã bị thu hồi QUÁ hạn grace (link trạng thái `grace` 30 ngày VẪN được chấp nhận) | KHÔNG retry — DLQ; hai bên đối chiếu qua E3 + case |
| 422 | `PIN-422-BIZ` / `BIZ-REF-CONFLICT` | Dedup tầng 2: `ref_id` đã tồn tại nhưng gắn `event_id` khác VÀ khác `amount_ct`/`link_id` → nghi ngờ dữ liệu, mở discrepancy | KHÔNG retry — phối hợp đối soát |
| 429 | `PIN-429-RATE` | Vượt công suất nhận (thiết kế 50 GD/giây bền vững = 3.000 GD/phút — TSD §9.1; chịu burst ngắn cao hơn qua hàng đợi) | Retry sau `Retry-After` |
| 500/503 | `PIN-500-SYS` / `PIN-503-DEP` | MMS lỗi/bảo trì | **Retry backoff `5s→30s→2m→10m→30m`, tối đa 24h**; hết 24h → dừng, ghi nhận để MMS bù bằng M3-poll + đối soát E3 |

**Xử lý phía MMS sau `accepted`:** verify thẻ + hash body — A.1b.3 (trước khi parse) → dedup 2 tầng (unique `event_id` toàn cục; unique `ref_id` xuyên nguồn m4/m3poll — bản ghi poll sinh `event_id = "poll:"+ref_id`) → normalize → «Peye-Haiti 16/08»: nếu có `addenda.payment_ref` thì tra Redis `qrinq:{ref}` (B.5) gắn đích danh merchant/bill trước → ghi `credit_event` → phát `credit.received` → Matching 2 mức.

<a id="muc-b-2-post-sms-dlr-delivery-report-sms-natcom-mms"></a>
### B.2. `POST /sms-dlr` — Delivery report SMS (Natcom → MMS)

Natcom báo trạng thái chuyển phát của SMS đã gửi qua N1 (D.5). Phục vụ Delivery Tracker + đo T1 khi kênh báo có là SMS.

**Request:**

| Trường | Kiểu | Bắt buộc | Mô tả | Ví dụ |
|---|---|---|---|---|
| `sms_id` | string ≤64 | **Có** | ID Natcom trả về khi nhận gửi (N1) | `"sms_8842190"` |
| `msisdn` | E.164 | Không | Số nhận — đối chiếu chéo | `"+50937123456"` |
| `status` | enum | **Có** | `delivered` · `failed` · `expired` (hết hạn retry mạng) · `rejected` (số sai/chặn) | `"delivered"` |
| `done_at` | RFC3339 | **Có** | Thời điểm trạng thái cuối tại SMSC | `"2026-10-01T13:24:20Z"` |
| `error_code` | string ≤16 | Không | Mã lỗi SMSC khi `failed/rejected` | `"UNDELIV_ABSENT"` |

**Response `200`:** `{ "status": "accepted" }` — kể cả khi `sms_id` không còn trong hệ thống (notification giữ 12 tháng) thì trả `{ "status": "ignored" }` để Natcom không dồn DLQ (DLR là telemetry best-effort).

**Lỗi:** chỉ `PIN-400-VAL` (thiếu `sms_id`/`status`), `PIN-401-AUTH`, `PIN-429-RATE`, `PIN-5xx` — Natcom retry tối đa 3 lần với 5xx.

<a id="muc-b-3-post-eod-notifications-switch-bao-file-e3-san-sang-e3-pu"></a>
### B.3. `POST /eod-notifications` — Switch báo file E3 sẵn sàng (E3 push)

Switch (qua BRH) chủ động thông báo file bảng kê phiên đã phát hành; MMS tải file qua `file_url` (hoặc SFTP), verify chữ ký + checksum rồi mở `recon_run`. Đây là kênh push; kênh pull chủ động là D.3 (`GET /switch/v1/eod`). Hai kênh cùng dữ liệu — dedup theo (`biz_date`,`session_no`).

**Request:**

| Trường | Kiểu | Bắt buộc | Mô tả | Ví dụ |
|---|---|---|---|---|
| `biz_date` | date | **Có** | Ngày nghiệp vụ theo giờ Haiti | `"2026-10-01"` |
| `session_no` | int | **Có** | Phiên quyết toán trong ngày, `1..3` (C18 — 3 phiên/ngày) | `2` |
| `file_url` | string URL | **Có** | HTTPS presigned tải file **JSONL** (mỗi dòng: `{ref_id, account_no, amount_ct, direction, booked_at, session_no}`), TTL ≥24h | `"https://switch.brh.ht/files/…"` |
| `checksum_sha256` | string(64) hex | **Có** | SHA-256 của file — MMS verify trước khi ingest | `"a3f0…"` |
| `signature_url` | string URL | Không | File chữ ký số detached `.sig`; vắng → chữ ký nhúng theo chuẩn Switch | — |
| `record_count` | int | Không | Số dòng — đối chiếu nhanh | `1874` |
| `generated_at` | RFC3339 | **Có** | Thời điểm Switch chốt file | `"2026-10-01T21:05:00Z"` |

**Response `202`:** `{ "status": "accepted", "run_id": "{uuid recon_run}" }` · trùng (`biz_date`,`session_no`) đã ingest → `200 { "status": "duplicate", "run_id": "..." }`.

**Lỗi:**

| HTTP | Mã | Khi nào | Switch làm gì |
|---|---|---|---|
| 400 | `PIN-400-VAL` | `session_no` ngoài 1..3, URL sai, checksum sai format | Không retry — sửa rồi gửi lại |
| 401 | `PIN-401-AUTH` | mTLS/JWT sai | Không retry — vận hành |
| 422 | `PIN-422-BIZ` (`details.issue="checksum_mismatch"`) | MMS tải xong file nhưng checksum/chữ ký lệch (trả qua callback vận hành nếu đã 202 — chỉ 422 đồng bộ khi phát hiện được ngay) | Phát hành lại file |
| 5xx | `PIN-500-SYS` / `PIN-503-DEP` | MMS lỗi | Retry backoff; MMS còn kênh pull D.3 + cảnh báo AQ-01 khi thiếu file > 2h |

---

<a id="muc-b-4-post-payment-results-webhook-ket-qua-tra-m-pay-bank-tra"></a>
### B.4. `POST /payment-results` — Webhook KẾT QUẢ TRẢ M-PAY (bank TRẢ → Peye-Haiti) «Peye-Haiti 15/08»

Định chế TRẢ báo kết quả cuối của lệnh trả đã khởi tạo qua C.7. Chuẩn an ninh như B.1 (mTLS + thẻ kèm hash body «v3.4»). **Quy tắc xử lý «Peye-Haiti 15/08»:** tra payment theo `client_ref` TRƯỚC, `ext_payment_id` sau (đóng race kết quả về trước khi C.7 kịp trả lời); chấp nhận khi payment ở `created`/`submitted`/`sca_required` («v3.5»)/`timeout`; `succeeded`/`failed` là trạng thái CUỐI bất biến — bắn trùng không đổi lần hai, kết quả MÂU THUẪN với trạng thái cuối → giữ nguyên + mở `discrepancy` (state machine: TSD §6b).

**Request:** `{ "event_id" (UUID định chế sinh, DUY NHẤT — khóa dedup như B.1 — Redis `payres:{event_id}` TTL 48h, gặp lại trả 200 không xử lý; «v3.4»: mọi endpoint đối tác có body đều có khóa khử trùng tường minh), "ext_payment_id", "client_ref" (= payment.id), "status": "succeeded"|"failed", "failure_reason": "insufficient_funds"|"declined"|"limit"|"sca_failed" («v3.5»)|"other"|null, "ref_id" (RefID Switch, null nếu on-us), "finished_at" }` → **Response `200`:** `{ "received": true }` ≤2s, xử lý async: cập nhật `payment` + thông báo người mua (đích SLA tổng ≤3s P95 từ lúc bấm trả — `PAY_CONFIRM_SLA`).

**Lỗi riêng:** `PIN-404-NF` không có payment tương ứng (định chế retry theo quy tắc nhóm B).

<a id="muc-b-5-post-qr-inquiry-tra-cuu-qr-lay-tham-chieu-tra-app-dinh-c"></a>
### B.5. `POST /qr-inquiry` — Tra cứu QR & lấy tham chiếu trả (app định chế TRẢ → Peye-Haiti) «Peye-Haiti 16/08»

App của ĐỊNH CHẾ TRẢ (NatCash agent/customer · MonCash · app bank — qua backend của định chế) gọi NGAY SAU khi quét HTQR, TRƯỚC khi trừ tiền, để lấy ba thứ mà payload QR không tự chứng minh được: ① **tên + trạng thái người bán đã XÁC MINH** từ sổ đăng ký Peye-Haiti (chống QR dán đè, chặn merchant bị thu hồi/tạm khóa); ② **bill/số tiền chính xác** với QR động (kể cả khi bill đã thanh toán/hủy/hết hạn); ③ **`payment_ref`** — tham chiếu Peye-Haiti cấp, định chế ĐEM THEO lệnh chuyển (M4 `addenda.payment_ref`; qua ATS: trường remittance của pacs.008) → khớp lệnh mức ① thành ĐÍCH DANH. **Offline-first A9 giữ nguyên:** mất mạng/Peye-Haiti bảo trì thì app vẫn cho trả theo dữ liệu QR như cũ — B.5 là lớp GIA CỐ, không phải điều kiện.

**Auth:** mTLS + thẻ hệ thống tự ký (A.1b — request CÓ BODY nên thẻ kèm hash body như mọi nhóm B) · KHÔNG yêu cầu thẻ response (read-only, không phải số liệu tài chính) · rate limit theo đối tác · **response KHÔNG chứa số TK** (app đã có từ QR; Peye-Haiti không cấp thêm dữ liệu nhạy cảm).

**Request:** `{ "qr_payload" (chuỗi TLV đầy đủ, ≤512) HOẶC "merchant_code" + "bill_id"|null, "channel": "app"|"ussd" }`

**Response `200`:**

| Trường | Kiểu | Mô tả |
|---|---|---|
| `merchant` | object | `{ "code", "display_name" (tên ĐÃ XÁC MINH để hiện màn xác nhận), "status": "active"\|"suspended"\|"revoked", "mcc", "city" }` |
| `payable` | bool | `false` khi merchant không active, hoặc bill đã `paid`/`cancelled`/`expired`, hoặc QR phiên bản cũ (`qr_version` lệch) |
| `reason` | enum\|null | `merchant_suspended` · `merchant_revoked` · `bill_paid` · `bill_cancelled` · `bill_expired` · `qr_stale` — app HIỂN THỊ cảnh báo và không cho trả |
| `order` | object\|null | QR động: `{ "bill_id", "amount_ct", "currency", "expires_at" }` — app khóa số tiền theo bill |
| `payment_ref` | string\|null | `qi_`+ULID, chỉ cấp khi `payable=true`; TTL 15 phút (hằng nội bộ module Khớp lệnh — không phải tham số hệ thống); dùng MỘT lần |
| `ref_ttl_s` | int | Giây còn hiệu lực (mặc định 900) — quá hạn thì app tra cứu lại |

**Lỗi (không thêm mã mới):** `PIN-400-VAL` payload TLV hỏng/CRC sai · `PIN-404-NF` merchant không tồn tại (không phân biệt lý do — chống dò) · `PIN-429-RATE` vượt hạn mức đối tác.

**Phía Peye-Haiti:** ghi `payment_ref` vào Redis `qrinq:{ref}` = `{merchant_id, bill_id|null, amount_ct|null}` TTL 15′ — KHÔNG bảng mới, KHÔNG tham số hệ thống mới; M4 mang `addenda.payment_ref` → Ingest tra Redis gắn đích danh rồi mới phát `credit.received` (hết TTL/không thấy → rơi tự nhiên về khớp cũ). USSD (`channel:"ussd"`): NatCash gateway có thể gọi B.5 để hiện TÊN merchant trên menu xác nhận — tùy chọn giai đoạn 2, pilot không yêu cầu.

<a id="muc-c-open-banking-bank-nhan-tra-expose-mms-goi-ra-obbase-ob-v1"></a>
## C. Open Banking bank NHẬN/TRẢ expose — MMS gọi ra (`{OB_BASE}/ob/v1`, hợp đồng D2 + phụ lục M-PAY)

> Contract MMS YÊU CẦU bank nhận (wallet2 + 1 bank) expose theo chuẩn OB BRH. *(wallet2 = ví do NatTransfer vận hành; các mã `bank_code` trong tài liệu — `NTRF`, `BANK`… — là mã ví dụ, mã chính thức lấy từ danh mục bank do BRH cấp khi ban hành chuẩn — phụ thuộc D1.)* Sandbox bắt buộc T7/2026. Mọi request MMS→bank: mTLS + thẻ hệ thống tự ký của MMS (A.1b — request có body thì thẻ kèm **hash body**, «v3.4»: chính thẻ đã là bằng chứng chống chối bỏ của lệnh trả, bank lưu thẻ + body 5 năm; C.9 «v3.5» cùng chuẩn) + `Idempotency-Key` (bank phải hỗ trợ, TTL ≥48h); response tài chính bank ký **thẻ response** ở `x-jws-signature` (F.3). **Ngưỡng xác thực bổ sung CHUẨN HÓA «v3.5»:** lệnh trả > `PAY_SCA_THRESHOLD` (500.000 ct = 5.000 HTG) → định chế BẮT BUỘC trả nhánh `sca_required` tại C.7 và TỰ gửi SMS OTP tới SĐT chủ TK mình đang giữ (cùng kênh OTP đã dùng ở C.2 — SMS GW của định chế, không phải của Peye); ≤ ngưỡng → thực thi thẳng, KHÔNG hỏi người dùng thêm. Định chế được CHẶT hơn (hạ ngưỡng theo hồ sơ rủi ro — MMS chấp nhận `sca_required` ở MỌI mức tiền «L1») — không được lỏng hơn; MMS cũng chủ động yêu cầu thách OTP bằng `sca_hint` (chống chẻ nhỏ lệnh). Bank chuẩn hóa mã lỗi `OB-xxx` theo bảng C.0; connector per-bank (`/connectors/ob-*`) chỉ map format, KHÔNG map lại ngữ nghĩa. **OB-M1.3 «trạng thái liên kết» của bộ chuẩn OB:** chốt phương án TRƯỜNG TRẠNG THÁI, không endpoint riêng — hiệu lực liên kết đọc từ response C.3 (gia hạn) + tín hiệu `OB-401-EXPIRED`/`OB-401-REVOKED` chuẩn hóa ở mọi call mang token; đối chiếu định kỳ = job token-renewal D-7.

<a id="muc-c-0-ma-loi-ob-chuan-hoa-cach-mms-xu-ly-ap-cho-moi-api-nhom-c"></a>
### C.0. Mã lỗi OB chuẩn hóa & cách MMS xử lý (áp cho mọi API nhóm C)

| Mã OB | HTTP | Nghĩa | MMS xử lý | Nổi lên BFF thành |
|---|---|---|---|---|
| `OB-400-VAL` | 400 | Request sai format | Bug connector — log + alert, không retry | `PIN-500-SYS` |
| `OB-401-AUTH` | 401 | Thẻ hệ thống A.1b/mTLS sai (`details.issue` = `alg`/`sig`/`aud`/`expired`/`body-hash`/`header`) | Alert AQ-00, circuit breaker, không retry; riêng lỗi `body-hash` ở C.7/C.9: ký thẻ mới với `iat` mới, thử đúng 1 lần — vẫn lỗi → alert khóa; payment giữ NGUYÊN trạng thái hiện tại (`created`: người dùng confirm lại E.16.2 hoặc sweeper `PAY_CREATE_TTL` chốt `failed('expired')`; `sca_required`: sweeper hỏi C.8 sau `expires_at`+5′ «v3.5») | `PIN-503-DEP` |
| `OB-401-EXPIRED` | 401 | `access_token` của link hết hạn | Tự gọi M1a refresh rồi **retry đúng 1 lần**; refresh fail → như REVOKED | trong suốt với client |
| `OB-401-REVOKED` | 401 | Token đã thu hồi (M1b hoặc bank chủ động) | Set `token.status=revoked`, `account_link.status=revoked`, phát `token.revoked`, ghim cảnh báo NB + AQ-00; yêu cầu re-link | `PIN-422-BIZ` / `BIZ-TOKEN-REVOKED` |
| `OB-403-SCOPE` | 403 | Token thiếu scope theo bảng A.1b.4 (`balance`/`history`/`credit-notify`/`payment`) | Lỗi cấu hình liên kết — alert, không retry; riêng C.7: payment chuyển `failed` + báo người mua đổi nguồn trả | `PIN-503-DEP` (C.7: `PIN-422-BIZ`) |
| `OB-404-ACC` | 404 | Số TK không tồn tại tại bank | Trả người dùng nhập lại | `PIN-422-BIZ` / `BIZ-ACC-NOT-FOUND` |
| `OB-404-LINK` | 404 | Định danh tài nguyên không tồn tại (`link_id`/`ext_payment_id`) | Đối chiếu kho token/payment; nghi lệch dữ liệu → alert | `PIN-404-NF` |
| `OB-409-IDEM` | 409 | Idempotency-Key trùng: body khác, HOẶC cùng body đang xử lý (`details.state="processing"`) | Body khác = bug connector — alert; processing = chờ `Retry-After` rồi gửi lại CÙNG key, hoặc chuyển C.8 hỏi trạng thái — KHÔNG phải bug | body khác: `PIN-500-SYS` · processing: retry nội bộ, không nổi lỗi |
| `OB-422-OTP` | 422 | OTP sai/hết hạn (kèm `details.attempts_left`) — C.2 liên kết · C.9 SCA «v3.5» | Cho nhập lại | `PIN-422-BIZ` / `BIZ-OTP-INVALID` |
| `OB-422-RANGE` | 422 | Khoảng thời gian M3 vượt giới hạn bank | Chia nhỏ khoảng rồi gọi lại | `PIN-400-VAL` |
| `OB-423-LOCK` | 423 | TK bị phong tỏa / link request bị khóa do sai OTP quá số lần | Dừng luồng, hướng dẫn ra bank | `PIN-422-BIZ` / `BIZ-ACC-LOCKED` |
| `OB-429-RATE` | 429 | Bank rate limit | Retry theo `Retry-After`, tôn trọng circuit breaker | `PIN-429-RATE` |
| `OB-500-SYS` | 500 | Bank lỗi | Retry backoff 1s→2s→4s (chỉ GET/idempotent); POST chỉ retry khi có Idempotency-Key | `PIN-503-DEP` |
| `OB-503-DOWN` | 503 | Bank bảo trì | Circuit breaker; kích hoạt degrade (M4↓ → M3-poll 5 phút/lần) | `PIN-503-DEP` |

**Timeout/retry mặc định nhóm C** (connector cấu hình được): connect 2s; read: M3 (số dư/lịch sử) = 5s · M1/M1a/M1b = 10s. Retry GET tối đa 3; POST tối đa 1 lần lặp khi timeout mạng VÀ có Idempotency-Key. Nhận `OB-409-IDEM` với `details.state="processing"` → KHÔNG phải lỗi: chờ `Retry-After` rồi gửi lại CÙNG key (tối đa 3), hoặc chuyển C.8 hỏi trạng thái.

> **Thứ tự gọi (dễ hình dung):** Onboarding lấy tài khoản nhận = **C.1→C.2** (liên kết TK có sẵn). Vòng đời token = **C.3** (gia hạn) · **C.4** (thu hồi). Truy vấn & phục hồi khi vận hành = **C.5** số dư · **C.6** lịch sử.
>
> **Ai là chủ tài khoản do BANK quyết:** MMS không đối chiếu tên. Khi liên kết (C.1), bank gửi OTP tới **SĐT chủ TK mà bank đang giữ**; chỉ chính chủ nhận được OTP mới hoàn tất được liên kết. Người bán nhập nhầm TK người khác → OTP về máy chủ TK thật → không có OTP → không cấp token.

<a id="muc-c-1-m1-post-ob-v1-links-khoi-tao-lien-ket-tk-da-co-buoc-1-2"></a>
### C.1. M1 · `POST /ob/v1/links` — Khởi tạo liên kết TK đã có (bước 1/2)

Bank gửi OTP tới **SĐT chủ TK mà bank đang giữ** để lấy consent; bank tự phán định TK có thuộc người này không (MMS không đối chiếu tên).

**Request:**

| Trường | Kiểu | Bắt buộc | Mô tả | Ví dụ |
|---|---|---|---|---|
| `merchant_ref` | string ≤32 | Có* | Mã merchant MMS — bank lưu đối chiếu; có giá trị ⇔ **liên kết NHẬN TIỀN (receiving)** của gian hàng. \* **Liên kết NGUỒN TRẢ (funding — MỌI vai, kể cả chủ gian hàng)**: thay bằng `person_ref`. Đúng MỘT trong hai trường — cả hai có hoặc cả hai thiếu → 400. Với định chế cả hai ref là chuỗi OPAQUE: chỉ kiểm không-rỗng + độ dài, KHÔNG parse cấu trúc | `"PIN-M-000241"` |
| `person_ref` | string ≤64 | Có* | Mã đục person MMS — CHỈ **liên kết NGUỒN TRẢ (funding)**; người bán liên kết nguồn trả cá nhân cũng đi nhánh này (đúng một trong `merchant_ref`/`person_ref`). Quy tắc sinh «v3.4»: `"prn_" + HMAC-SHA256(person.id, khóa nội bộ nền tảng)[:22]` — deterministic, tái lập được, KHÔNG suy ngược ra person | `"prn_9f2a…"` |
| `requested_scope` | array | Không | Theo **bảng scope chuẩn A.1b.4** — mặc định theo LOẠI liên kết: nhận tiền `["balance","history","credit-notify"]` · nguồn trả `["payment","history"]`; **định chế validate bắt buộc theo A.1b.4, không tin giá trị truyền sang** | — |
| `account_no` | string ≤32 | **Có** | Số TK/ví đầy đủ tại bank | `"50912347709"` |
| `msisdn` | E.164 | **Có** | SĐT merchant khai — bank đối chiếu với SĐT gắn TK trước khi gửi OTP | `"+50937123456"` |
| `otp_channel` | enum | **Có** | `sms` (footprint chỉ SMS) | `"sms"` |
| `kyc_evidence_ref` | string ≤64 | Có* | `ref` kết quả định danh E1 (provider `BRH-E1`) — bank ghi nhận để gắn liên kết với danh tính đã xác minh. \* Bắt buộc với liên kết NHẬN TIỀN (KYC2); liên kết NGUỒN TRẢ (KYC1): bỏ qua | `"E1-2026-88121"` |

**Response `201`:**

| Trường | Kiểu | Mô tả | Ví dụ |
|---|---|---|---|
| `link_id` | string | Định danh liên kết bank cấp — trạng thái chờ OTP, dùng cho bước confirm và là `link_id` trong M4 sau này | `"lnk_01HX4Y7Q2K"` |
| `status` | enum | `otp_sent` | — |
| `otp_expires_at` | RFC3339 | Hạn OTP phía bank | — |
| `msisdn_masked` | string | Số bank đã gửi OTP (mask) — hiển thị cho merchant biết OTP về đâu | `"+509****3456"` |

**Lỗi riêng:** `OB-404-ACC` (số TK không tồn tại) · `OB-423-LOCK` (TK phong tỏa). Timeout 10s.

<a id="muc-c-2-m1-post-ob-v1-links-linkid-confirm-xac-nhan-otp-nhan-tok"></a>
### C.2. M1 · `POST /ob/v1/links/{link_id}/confirm` — Xác nhận OTP, nhận token (bước 2/2)

**Request:** | `otp` | string(6) | **Có** | OTP chủ TK nhận từ bank | `"482913"` |

**Response `200`:**

| Trường | Kiểu | Mô tả |
|---|---|---|
| `link_id` | string | Như C.1 |
| `token.access_token` | string | Token truy cập theo link — MMS mã hóa envelope (Vault) trước khi lưu, **không bao giờ log** |
| `token.expires_at` | RFC3339 | +90 ngày (C4) |
| `token.refresh_token` | string | Đổi access mới qua M1a |
| `token.refresh_expires_at` | RFC3339 | +12 tháng (C4) |
| `token.scope` | array\<string\> | Trả ĐÚNG theo bộ scope đã duyệt tại C.1 (validate theo A.1b.4); ví dụ liên kết nhận tiền: `["balance","history","credit-notify"]` — `credit-notify` = bank bật gửi M4 cho link này |
| `account_no_masked` | string | `"…7709"` |
| `holder_name` | string | Tên chủ TK — bank trả đầy đủ tại đây vì chủ TK đã consent bằng OTP; MMS lưu để hiển thị xác nhận cho người bán |

**Lỗi riêng:** `OB-422-OTP` (kèm `attempts_left`) · `OB-423-LOCK` (sai quá số lần — link request khóa, phải tạo lại từ C.1) · `OB-404-LINK` (link_id sai/hết hạn khởi tạo — bank tự định TTL ≥15 phút).

<a id="muc-c-3-m1a-post-ob-v1-tokens-refresh-gia-han-token"></a>
### C.3. M1a · `POST /ob/v1/tokens/refresh` — Gia hạn token

Job `token-renewal` gọi khi còn **D-7** (`TOKEN_RENEW_BEFORE=7 ngày`), hoặc on-demand khi gặp `OB-401-EXPIRED`, hoặc merchant bấm «gia hạn» (E.3.7).

**Request:** | `refresh_token` | string | **Có** |

**Response `200`:** `token{access_token, expires_at, refresh_token, refresh_expires_at, scope}` — refresh token XOAY (bản cũ vô hiệu ngay).

**Lỗi riêng:** `OB-401-REVOKED` (đã thu hồi) · `OB-401-EXPIRED` (refresh quá 12 tháng → bắt buộc re-link M1; MMS ghim cảnh báo NB-14 + AQ-00 `token_expiring_7d`).

<a id="muc-c-4-m1b-post-ob-v1-tokens-revoke-thu-hoi-token"></a>
### C.4. M1b · `POST /ob/v1/tokens/revoke` — Thu hồi token

Gọi khi: đổi TK xong grace (S4 bước ⑤), merchant đóng (S8), nghi ngờ gian lận. **Idempotent**: revoke lần 2 vẫn `200`.

**Request:**

| Trường | Kiểu | Bắt buộc | Mô tả | Ví dụ |
|---|---|---|---|---|
| `link_id` | string | **Có** | Link cần thu hồi | `"lnk_01HX4Y7Q2K"` |
| `reason` | enum | **Có** | `account_change` \| `closure` \| `fraud` | `"account_change"` |

**Response `200`:** `{ "link_id": "...", "revoked_at": "2026-11-01T09:00:00Z" }` — sau đó: mọi call token cũ = `OB-401-REVOKED`; **bank NGỪNG gửi M4** cho link; MMS cập nhật E3-reg (D.4).

**Lỗi riêng:** `OB-404-LINK`.

<a id="muc-c-5-m3-get-ob-v1-accounts-linkid-balance-so-du"></a>
### C.5. M3 · `GET /ob/v1/accounts/{link_id}/balance` — Số dư

Header: `x-account-token: {access_token của link}` (thẻ hệ thống ở `x-system-token` — A.1b.5). Dùng: hiển thị NB-09 (kéo-làm-mới, cache 60s phía MMS).

**Response `200`:**

| Trường | Kiểu | Mô tả | Ví dụ |
|---|---|---|---|
| `link_id` | string | Echo — MMS đối chiếu với `link_id` trên path (F.3 «v3.7») | — |
| `account_no_masked` | string | — | `"…7709"` |
| `balance_ct` | int64 | Số dư khả dụng, centime | `4250000` |
| `currency` | string | `"HTG"` | — |
| `as_of` | RFC3339 | Thời điểm bank chốt số | — |

**Lỗi riêng:** `OB-401-EXPIRED` (→ M1a + retry 1) · `OB-401-REVOKED` · `OB-403-SCOPE` (thiếu scope `balance`).

<a id="muc-c-6-m3-get-ob-v1-accounts-linkid-transactions-lich-su-giao-d"></a>
### C.6. M3 · `GET /ob/v1/accounts/{link_id}/transactions` — Lịch sử giao dịch

Query: `?from&to` (RFC3339, bắt buộc, khoảng ≤31 ngày/call — quá → `OB-422-RANGE`) `&cursor&page_size(≤100)`. Dùng: NB-09, đối chiếu theo `ref_id`/amount+booked_at (phục hồi/đối soát/xác minh hoàn — KHÔNG còn là một mức khớp), M3-poll khi webhook down (5 phút/lần), **xác minh bút toán hoàn S5**, đối soát.

**Response `200`:** top-level `{ "link_id" (echo — MMS đối chiếu với path theo F.3), "items": [...], "next_cursor" }` — `items[]`:

| Trường | Kiểu | Mô tả | Ví dụ |
|---|---|---|---|
| `txn_id` | string | ID bút toán phía bank — poll sinh `event_id="poll:"+ref_id` (fallback `poll:`+txn_id khi on-us) | `"txn_77120031"` |
| `ref_id` | string \| null | RefID Switch; null khi on-us | `"PIN-2026-000123"` |
| `amount_ct` | int64 | > 0 | `150000` |
| `currency` | string | `"HTG"` | — |
| `direction` | enum | `credit` \| `debit` — debit dùng xác minh hoàn (S5) | `"credit"` |
| `counterparty.name` | string | Đối ứng (bank có thể mask) | `"J. PIERRE"` |
| `counterparty.msisdn` | E.164 | Không bắt buộc | — |
| `counterparty.bank_code` | string(4) | Không bắt buộc | `"NTRF"` |
| `narrative` | string ≤280 | — | — |
| `booked_at` | RFC3339 | — | — |

**Lỗi riêng:** `OB-401-EXPIRED` · `OB-401-REVOKED` · `OB-403-SCOPE` (`history`) · `OB-422-RANGE`. Retry GET tối đa 3.

---

<a id="muc-c-7-m-pay-1-post-ob-v1-payments-khoi-tao-lenh-tra-dinh-che-t"></a>
### C.7. M-PAY.1 · `POST /ob/v1/payments` — Khởi tạo lệnh trả (định chế TRẢ) «Peye-Haiti 15/08»

Gọi bằng token liên kết scope `payment` của **liên kết NGUỒN TRẢ (funding — C.1/C.2 nhánh `person_ref`, MỌI vai — người bán trả tiền cũng nhánh này)**. **An ninh «v3.4»: thẻ hệ thống kèm hash body (A.1b) — chính thẻ là bằng chứng chống chối bỏ của lệnh trả; bank verify hash TRƯỚC khi xử lý, lưu thẻ + body 5 năm.** Người dùng (mọi vai «v3.5») đã được PEYE-HAITI xác thực bằng PIN app (E.16.2) TRƯỚC khi lệnh này được gửi. **Hai bậc «v3.5»:** lệnh ≤ `PAY_SCA_THRESHOLD` → định chế KHÔNG hỏi người dùng thêm gì — thực thi theo token liên kết + HẠN MỨC tự áp (vượt → `failed`/`limit` hoặc `declined` qua B.4); lệnh > ngưỡng → định chế BẮT BUỘC nhánh `sca_required` (SMS OTP do ĐỊNH CHẾ gửi tới chủ TK, xác nhận tại C.9). Trách nhiệm xác thực: bậc PIN thuộc Peye-Haiti · bậc OTP thuộc định chế — ghi thành điều khoản hợp đồng D2. `target.account` lấy từ Redis tạm của E.16.1 (xóa sau 202 — không ghi đĩa). Body: `{ "client_ref" (= payment.id, idempotent), "link_id" (TK nguồn), "target": { "operator" (9332xx), "account" (số TK đích từ QR — relay, không lưu), "name_hint" (tên merchant đã resolve) }, "amount_ct", "currency", "bill_code" | null }` → `202` MỘT trong hai nhánh «v3.5»: `{ "ext_payment_id", "status": "submitted" }` — lệnh ≤ ngưỡng, đi thẳng; hoặc **`{ "ext_payment_id", "status": "sca_required", "sca": { "challenge_id", "otp_channel": "sms", "msisdn_masked", "expires_at", "attempts_left" } }`** — lệnh > `PAY_SCA_THRESHOLD`: định chế ĐÃ tự gửi OTP tới SĐT chủ TK mình giữ, chờ xác nhận tại C.9. Token liên kết đặt ở `x-account-token` (A.1b.5). Kết quả cuối về qua **B.4**; thiếu số dư/từ chối là KẾT QUẢ (`failed` + `failure_reason`), không phải lỗi API.

<a id="muc-c-8-m-pay-2-get-ob-v1-payments-extpaymentid-trang-thai-lenh"></a>
### C.8. M-PAY.2 · `GET /ob/v1/payments/{ext_payment_id}` — Trạng thái lệnh trả «Peye-Haiti 15/08»

Lưới đỡ khi B.4 sót: job hỏi lại sau `PAY_TIMEOUT`; với payment ở `sca_required`: hỏi sau `expires_at` + 5 phút («v3.5» — hằng số ân hạn, không thêm tham số). Response: `{ "ext_payment_id", "status", "failure_reason", "ref_id", "finished_at" }`.

<a id="muc-c-9-m-pay-3-post-ob-v1-payments-extpaymentid-sca-xac-nhan-ot"></a>
### C.9. M-PAY.3 · `POST /ob/v1/payments/{ext_payment_id}/sca` — Xác nhận OTP lệnh trả «v3.5»

Hoàn tất lệnh trả đang ở `sca_required` (lệnh > `PAY_SCA_THRESHOLD` = 5.000 HTG): người dùng nhập mã OTP (do ĐỊNH CHẾ gửi qua SMS tới chủ TK ở bước C.7) trên app Peye-Haiti (E.16.6), MMS chuyển tiếp sang định chế. An ninh: thẻ hệ thống kèm **hash body** (A.1b — thông điệp tài chính, cùng chuẩn C.7) + `x-account-token`.

**Request:** `{ "challenge_id", "otp" (6 số) }` → **Response `202`:** `{ "ext_payment_id", "status": "submitted" }` — kết quả cuối vẫn về qua B.4 (response ký thẻ response F.3).

**Lỗi riêng:** `OB-422-OTP` OTP sai/hết hạn (kèm `details.attempts_left` — app cho nhập lại) · `OB-423-LOCK` sai quá số lần → định chế chốt lệnh `failed` + `failure_reason:"sca_failed"` qua B.4 · `OB-404-LINK` `ext_payment_id`/`challenge_id` không tồn tại. Quá `expires_at` chưa xác nhận: định chế TỰ chốt `failed`/`sca_failed` qua B.4; PHÒNG B.4 thất lạc, sweeper của MMS hỏi C.8 khi payment còn `sca_required` quá `expires_at` + 5 phút. KHÔNG có API gửi lại OTP: hết hạn thì tạo lệnh mới từ E.16.1 — tránh biến chuẩn thành kênh spam SMS (SMS GW là CỦA ĐỊNH CHẾ — điều kiện kết nạp F.4).

<a id="muc-d-brh-system-e1e2-switch-e3e3-reg-natcom-n1-mms-goi-ra"></a>
## D. BRH-System (E1·E2) · Switch (E3·E3-reg) · Natcom (N1) — MMS gọi ra

> Chuẩn chung nhóm D: mTLS + JWT hệ thống tự ký (A.1b, hoặc tương đương theo hợp đồng kênh); `Idempotency-Key` với POST/PUT; envelope lỗi A.3 với prefix mã theo đối tác. Bảng SLA gốc: TSD §2b.

<a id="muc-d-1-e1-post-brhsystem-brh-ekyc-v1-verify-doi-chieu-danh-tinh"></a>
### D.1. E1 · `POST {BRH_SYSTEM}/brh/ekyc/v1/verify` — Đối chiếu danh tính CIN + selfie ↔ ONI

Gọi từ pipeline `POST /ekyc/submit` (E.2.2). Ảnh KHÔNG gửi kèm body — truyền **presigned URL nội bộ** (MinIO, TTL 15 phút, chỉ IP BRH-System).

**Request:**

| Trường | Kiểu | Bắt buộc | Mô tả | Ví dụ |
|---|---|---|---|---|
| `cin_no` | string ≤20 | **Có** | Số CIN khai báo | `"003-118-224-7"` |
| `front_key` | string URL | **Có** | Presigned URL ảnh CIN mặt trước (jpeg ≤200KB) | `"https://minio…/ekyc/f_9d2.jpg?X-Amz…"` |
| `back_key` | string URL | **Có** | Ảnh CIN mặt sau | — |
| `selfie_key` | string URL | **Có** | Selfie (đã chống giả mạo client-side) | — |

**Response `200`:**

| Trường | Kiểu | Mô tả | Ví dụ |
|---|---|---|---|
| `matched` | bool | Khớp/không khớp với dữ liệu ONI (C3: KHÔNG trả ảnh gốc, không trả thông tin ONI) | `true` |
| `score` | number 0..1 | Điểm tin cậy — auto-activate cần `matched AND score ≥ AUTO_ACTIVATE_SCORE(0.85)` | `0.94` |
| `ref` | string ≤64 | Mã tham chiếu kết quả — nuôi `kyc_evidence_ref` (M1) | `"E1-2026-88121"` |
| `checked_at` | RFC3339 | — | — |

**Lỗi & xử lý MMS:**

| Mã | HTTP | Khi nào | MMS xử lý |
|---|---|---|---|
| `E1-422-QUALITY` | 422 | Ảnh mờ/chói/thiếu góc — `details[].field` ∈ `front\|back\|selfie`, `issue="quality"` | NB-1C chuyển `need_more` yêu cầu chụp lại đúng ảnh đó (AC-1.2), KHÔNG nhập lại thông tin |
| `E1-404-CIN` | 404 | CIN không tồn tại trong ONI | Hồ sơ cờ vàng → duyệt tay BRH-03 |
| `E1-400-VAL` | 400 | URL hết hạn/format sai | Bug/độ trễ pipeline — regenerate presigned + retry 1 |
| `E1-401-AUTH` | 401 | mTLS/JWT sai | Alert AQ-00 |
| `E1-429-RATE` | 429 | Quá hạn ngạch | Hàng đợi lại, backoff |
| `E1-500-SYS` / `E1-503-DOWN` | 5xx | BRH-System lỗi/bảo trì | **Degrade runbook**: hồ sơ vào hàng đợi + duyệt tay ảnh; `e1_error_rate>5%/15'` → cảnh báo trực ban ≤5 phút (AC-9.3) |

SLA p95 ≤3s; timeout 10s; nếu chờ >10s app hiện «Đang đối chiếu — bạn có thể để máy đó» (xử lý async, kết quả về qua `GET /applications/me` + notification).

<a id="muc-d-2-e2-post-brhsystem-brh-aml-v1-screen-sang-loc-aml"></a>
### D.2. E2 · `POST {BRH_SYSTEM}/brh/aml/v1/screen` — Sàng lọc AML

Gọi khi: onboarding (sau E1 pass, trước auto-activate) và monitoring định kỳ/khi có alert.

**Request:**

| Trường | Kiểu | Bắt buộc | Mô tả | Ví dụ |
|---|---|---|---|---|
| `person.full_name` | string ≤140 | **Có** | — | `"MARIE DELVA"` |
| `person.dob` | date | **Có** | — | `"1988-03-14"` |
| `person.cin_no` | string ≤20 | **Có** | — | `"003-118-224-7"` |
| `merchant_ref` | string ≤32 | **Có** | — | `"PIN-M-000241"` |
| `context` | enum | **Có** | `onboarding` \| `monitoring` | `"onboarding"` |

**Response `200`:**

| Trường | Kiểu | Mô tả | Ví dụ |
|---|---|---|---|
| `hit` | bool | `true` ⇒ MMS tạo `aml_alert(source=e2)` + gắn cờ `post_review` vào danh sách hậu kiểm ưu tiên BRH-03 — gian hàng VẪN active («v3.6» tạo-là-active, không chặn kích hoạt) | `false` |
| `lists[]` | array | Mỗi phần tử: `{list_code, entry_ref?, match_strength?}` — danh sách trúng (PEP/sanction/nội bộ BRH) | `[{"list_code":"BRH-WATCH"}]` |
| `score` | number 0..1 | Mức tương đồng | `0.12` |

**Lỗi:** `E2-400-VAL` · `E2-401-AUTH` · `E2-429-RATE` · `E2-500-SYS`/`E2-503-DOWN` — khi 5xx trong onboarding «v3.6»: KHÔNG chặn kích hoạt — gian hàng vẫn active + cờ `post_review`, sàng lọc BÙ khi E2 về; monitoring: retry job sau. SLA p95 ≤2s; timeout 5s.

<a id="muc-d-3-e3-get-switch-switch-v1-eod-bizdate-date-session-n-keo-b"></a>
### D.3. E3 · `GET {SWITCH}/switch/v1/eod?biz_date={date}&session={n}` — Kéo bảng kê cuối phiên (kênh pull)

Kênh chủ động của module Đối soát (**Back-office**) — bổ trợ push B.3. 3 phiên/ngày (C18), quyết toán T+1.

**Response `200`:** `{ "file_url": "...", "checksum_sha256": "...", "record_count": 1874, "generated_at": "..." }` — file **JSONL ký số**, mỗi dòng:

| Trường (dòng JSONL) | Kiểu | Mô tả | Ví dụ |
|---|---|---|---|
| `ref_id` | string | RefID Switch — khóa so khớp với `credit_event.ref_id` (bản ghi on-us KHÔNG có trong E3, đối soát bỏ qua) | `"PIN-2026-000123"` |
| `account_no` | string | Số TK nhận ĐẦY ĐỦ — so với `account_link.account_no_enc` giải mã; file đã LỌC theo danh mục E3-reg (quá độ: nhận full, MMS tự lọc, hủy phần thừa) | `"50912347709"` |
| `amount_ct` | int64 | — | `150000` |
| `direction` | enum | `credit` \| `debit` | `"credit"` |
| `booked_at` | RFC3339 | — | — |
| `session_no` | int 1..3 | — | `2` |

**Lỗi & xử lý:**

| Mã | HTTP | Khi nào | MMS xử lý |
|---|---|---|---|
| `E3-404-NOTREADY` | 404 | File phiên chưa phát hành | Retry mỗi 15 phút; **thiếu quá 2h sau giờ chốt phiên → cảnh báo AQ-01, đối soát dời phiên** |
| `E3-401-AUTH` / `E3-403-SCOPE` | 401/403 | Chứng thực sai | Alert vận hành |
| `E3-500-SYS` | 5xx | Switch lỗi | Retry + chuyển **SFTP dự phòng**: `sftp://{SWITCH_SFTP}/eod/YYYYMMDD_S{n}.jsonl` + `.jsonl.sig` |

Verify BẮT BUỘC trước ingest: chữ ký số file + `checksum_sha256`; lệch → không ingest, yêu cầu phát hành lại (422 luồng B.3).

<a id="muc-d-4-e3-reg-put-switch-switch-v1-account-registry-dang-ky-dan"></a>
### D.4. E3-reg · `PUT {SWITCH}/switch/v1/account-registry` — Đăng ký danh mục TK NHẬN (qua BRH)

**PUT thay thế trọn bộ** danh mục TK nhận hiện hành để Switch lọc E3 (S6). Gọi lại MỖI KHI: liên kết mới (M1), đổi TK (S4 — gồm cả TK cũ đang grace), hết grace/thu hồi (M1b), merchant đóng. Job đối chiếu đêm gửi lại toàn bộ để tự sửa lệch.

**Request:**

| Trường | Kiểu | Bắt buộc | Mô tả | Ví dụ |
|---|---|---|---|---|
| `accounts[]` | array ≤10.000/call | **Có** | Toàn bộ danh mục hiện hành (active + grace); >10.000 → chia trang theo `page`/`total_pages` | — |
| `accounts[].bank_code` | string(4) | **Có** | Danh mục mã bank BRH | `"NTRF"` |
| `accounts[].account_no` | string ≤32 | **Có** | Số TK đầy đủ (kênh mTLS + VPN; Switch lưu để lọc) | `"50912347709"` |
| `page` / `total_pages` | int | Không (mặc định 1/1) | Phân mảnh khi vượt 10.000 | `1` / `1` |

**Response `200`:** `{ "accepted_count": 612, "effective_at": "..." }` — hiệu lực từ phiên E3 kế tiếp.

**Lỗi:** `E3-400-VAL` (bank_code lạ, account rỗng — `details[]` chỉ rõ index) · `E3-401-AUTH` · `E3-413-SIZE` (vượt 10.000 không phân trang) · `E3-500-SYS` (retry + alert; danh mục cũ tiếp tục hiệu lực).

<a id="muc-d-5-n1-post-natcom-natcom-sms-v1-send-gui-sms-lien-mang-bran"></a>
### D.5. N1 · `POST {NATCOM}/natcom/sms/v1/send` — Gửi SMS liên mạng, brandname Peye-Haiti

Mọi SMS đi qua Notification service (ưu tiên push → chờ ack 60s → SMS; rate limit 5 SMS/giờ/merchant trừ OTP). Template ĐĂNG KÝ TRƯỚC với Natcom (D6).

**Request:**

| Trường | Kiểu | Bắt buộc | Mô tả | Ví dụ |
|---|---|---|---|---|
| `msisdn` | E.164 | **Có** | Số nhận, mọi mạng | `"+50937123456"` |
| `template_id` | string ≤32 | **Có** | Mã template đã đăng ký: `OTP_GENERIC` · `CREDIT_ALERT` (báo có) · `DEBT_REMIND` (nhắc nợ) · `APP_STATUS` (trạng thái hồ sơ) · `TOKEN_EXPIRY` · `RECEIPT_SHARE` · `EMERGENCY_LOCK` · `MERCHANT_STATUS` | `"CREDIT_ALERT"` |
| `params` | object | **Có** | Biến của template (chỉ giá trị, không PII thừa), ví dụ `{amount:"1.500 G", payer:"J. PIERRE", time:"13:24"}` | — |
| `lang` | enum | Không (mặc định `ht`) | `fr` \| `ht` — Natcom render đúng bản dịch template | `"ht"` |
| `brand` | string | **Có** | Luôn `"Peye-Haiti"` | — |
| `client_ref` | string ≤64 | Không | Mã idempotency phía MMS (= notification_id) — Natcom dedup 24h | — |

**Response `200`:** `{ "sms_id": "sms_8842190", "accepted_at": "..." }` — trạng thái chuyển phát về qua DLR B.2.

**Lỗi & xử lý:**

| Mã | HTTP | Khi nào | MMS xử lý |
|---|---|---|---|
| `N1-400-TPL` | 400 | `template_id` chưa đăng ký / thiếu biến | Bug cấu hình — alert, không retry |
| `N1-400-VAL` | 400 | msisdn sai format | Đánh dấu notification `failed` |
| `N1-422-MSISDN` | 422 | Số không tồn tại/bị chặn | `failed`, không retry |
| `N1-401-AUTH` | 401 | Chứng thực sai | Alert AQ-00 |
| `N1-429-RATE` | 429 | Quá throughput hợp đồng | Hàng đợi lại theo `Retry-After` |
| `N1-500-SYS` | 5xx | Natcom lỗi | Retry 3 lần (giữ `client_ref`); OTP có thủ tục fallback thoại (runbook Natcom); báo có chỉ còn push |

SLA p95 gửi ≤10s (`n1_latency>10s` → cảnh báo).

---

<a id="muc-e-bff-cho-app-portal-https-api-peye-haiti-ht-v1-chi-tiet-hoa"></a>
## E. BFF cho app & portal — `https://api.peye-haiti.ht/v1` (chi tiết hóa TSD §2c)

> Quy ước nhóm E: mọi endpoint yêu cầu `Authorization: Bearer` trừ nhóm E.1 công khai. Cột «Quyền»: `merchant` (JWT chứa `person_id`+`merchant_id`+`device_id` — gian hàng active) · `user` (MỌI person đã đăng nhập, CẢ HAI VAI — nhóm E.16 dùng nhãn này) · vai trò portal (`admin`/`approver`/`supervisor_aml`/`ops_read`/`inspector_read` — RBAC C11, nguyên tắc không vai trò nào vừa tạo vừa duyệt). Merchant ở trạng thái `suspended/closed` bị chặn mọi thao tác GHI nghiệp vụ → `PIN-422-BIZ`/`BIZ-MERCHANT-STATE` (đọc vẫn được). Mọi POST ghi: `Idempotency-Key`. Lỗi chung A.4 không nhắc lại.

<a id="muc-e-1-auth-nb-portal-man-nb-00-02-brh-01"></a>
### E.1. Auth NB & portal (màn NB-00/02, BRH-01)

<a id="muc-e-1-1-post-auth-register-khoi-tao-dang-ky-cong-khai"></a>
#### E.1.1 · `POST /auth/register` — Khởi tạo đăng ký (công khai)

Tạo bản ghi đăng ký (`registration_id`, person nháp) + tự gửi OTP tới `msisdn`. «v3.6»: đăng ký CHUNG một app — KHÔNG khai vai/gian hàng ở bước này (vai chọn ở CH-00 sau OTP+PIN; thông tin gian hàng khai ở NB-2B, nộp cùng E.2.2).

**Request:**

| Trường | Kiểu | Bắt buộc | Mô tả | Ví dụ |
|---|---|---|---|---|
| `msisdn` | E.164 | **Có** | SĐT chính chủ — unique theo person | `"+50937123456"` |
| `lang` | enum | **Có** | `fr` \| `ht` — chọn ngay màn đầu (UX-4) | `"ht"` |
| `agent_code` | string ≤16 | Không | Mã NV hỗ trợ `NAT-xxx` (US-06); phiên trên máy agent đánh dấu `is_agent_session=true` để truy vết. «v3.6»: giá trị GHI vào `merchant.agent_code` khi nộp E.2.2 (app truyền lại) — vai mua chỉ giữ vết ở `auth_session` | `"NAT-014"` |
**Response `201`:** `{ "registration_id": "{uuid}", "otp": { "otp_id": "{uuid}", "sent_to_masked": "+509****3456", "expires_in_s": 120, "resend_after_s": 60 } }`

**Lỗi riêng:** `PIN-409-STATE` msisdn đã có tài khoản active (`details.hint`="đăng nhập hoặc quên PIN") · `BIZ-OTP-LIMIT` quá 5 OTP/ngày/số · `PIN-400-VAL` `agent_code` không tồn tại (`details.field`).

> «v3.6» các trường `kind`/`shop_name`/`business_type`/`market_id` RỜI khỏi E.1.1: person tạo mặc định `kyc_level=1` (vai mua); chọn «người bán» ở CH-00 chỉ mở nhánh onboarding — vai chính thức xác lập khi E.2.2 được nộp (kèm gian hàng).

<a id="muc-e-1-2-post-auth-otp-send-gui-gui-lai-otp-cong-khai"></a>
#### E.1.2 · `POST /auth/otp/send` — Gửi/gửi lại OTP (công khai)

| Trường | Kiểu | Bắt buộc | Mô tả | Ví dụ |
|---|---|---|---|---|
| `purpose` | enum | **Có** | `register` \| `login_new_device` \| `pin_reset` \| `emergency_lock` | `"pin_reset"` |
| `msisdn` | E.164 | **Có** | — | — |

**Response `200`:** `{ "otp_id": "{uuid}", "expires_in_s": 120, "resend_after_s": 60 }` — OTP 6 số, TTL 120s (`OTP_TTL`), so sánh constant-time. Để chống dò số: msisdn KHÔNG tồn tại vẫn trả `200` (không gửi gì).

**Lỗi riêng:** `BIZ-OTP-LIMIT` (5/ngày/số — `OTP_MAX_PER_DAY`) · `PIN-429-RATE` (resend trước `resend_after_s`).

<a id="muc-e-1-3-post-auth-otp-verify-xac-thuc-otp-cong-khai"></a>
#### E.1.3 · `POST /auth/otp/verify` — Xác thực OTP (công khai)

| Trường | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `otp_id` | uuid | **Có** | Từ E.1.1/E.1.2 |
| `code` | string(6) | **Có** | 6 số |

**Response `200`:** `{ "verify_token": "{JWT 10 phút, aud=step-up, claim purpose}" }` — dùng đúng 1 lần cho bước kế (`pin/set`, `pin/reset`, `emergency-lock`, đăng nhập máy mới).

**Lỗi riêng:** `BIZ-OTP-INVALID` sai mã (kèm `details.attempts_left`; hết lượt → OTP hủy, phải gửi lại) hoặc hết hạn (`details.issue="expired"`) · `PIN-429-RATE`.

<a id="muc-e-1-4-post-auth-pin-set-dat-pin-lan-dau-cong-khai-verifytoke"></a>
#### E.1.4 · `POST /auth/pin/set` — Đặt PIN lần đầu (công khai + verify_token)

| Trường | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `verify_token` | string | **Có** | purpose=`register` |
| `pin` | string(6) | **Có** | 6 số; từ chối chuỗi yếu (`111111`, `123456`, lặp/tăng đều) |
| `pin_confirm` | string(6) | **Có** | Phải trùng `pin` |
| `device` | object | **Có** | `{device_id, fingerprint, model?, os?}` — thiết bị gắn với phiên (phiên agent được đánh dấu riêng) |

**Response `201`:** `{ "person_id": "{uuid}", "access_token": "...", "refresh_token": "...", "token_type": "Bearer", "expires_in": 900, "next_step": "choose_role" | "home" }` — PIN băm Argon2id (m=64MB, t=3, p=1). «v3.6»: đăng ký MỚI trả `next_step:"choose_role"` (server chưa biết vai — màn CH-00 ngay sau đó); `home` chỉ cho luồng đặt lại PIN trên tài khoản đã có. «user» là quyền của MỌI person đã đăng nhập (chủ gian hàng kyc_level=2 dùng chức năng thanh toán bằng CHÍNH tài khoản này), không phải điều kiện kyc_level=1.

**Lỗi riêng:** `PIN-400-VAL` PIN yếu/không trùng · `PIN-401-AUTH` verify_token sai/hết hạn/đã dùng.

<a id="muc-e-1-5-post-auth-login-dang-nhap-app-cong-khai"></a>
#### E.1.5 · `POST /auth/login` — Đăng nhập app (công khai)

| Trường | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `msisdn` | E.164 | **Có** | — |
| `pin` | string(6) | **Có** | — |
| `device` | object | **Có** | `{device_id, fingerprint, sim_ref?, model?, os?}` — `sim_ref` đọc được thì gửi — phục vụ truy vết phiên thiết bị |
| `verify_token` | string | Không | Bắt buộc khi thiết bị MỚI (purpose=`login_new_device`); thiếu → lỗi dưới |

**Response `200`:**

| Trường | Kiểu | Mô tả |
|---|---|---|
| `access_token` / `refresh_token` / `token_type` / `expires_in` | — | JWT ES256; access 15 phút, refresh 30 ngày; refresh gắn `device_id` (bảng `auth_session`) |
| `person` | object | `{id, kind, lang, msisdn_masked}` — `kind` = suy diễn từ tồn tại merchant («v3.6», xem note E.10.4) |
| `merchant` | object | `{id, code, shop_name, status}` |

**Lỗi riêng:** `PIN-401-AUTH` sai PIN (`details.attempts_left`) · `BIZ-PIN-LOCKED` khóa 60 phút sau 5 lần sai (`details.locked_until`) · `BIZ-PERSON-LOCKED` đang khóa khẩn (mở lại: OTP + re-eKYC theo runbook hotline) · `PIN-401-AUTH` + `details.issue="new_device_otp_required"` thiết bị mới chưa kèm `verify_token` (client gọi E.1.2 purpose=`login_new_device`).

<a id="muc-e-1-6-post-auth-token-refresh-xoay-token-phien"></a>
#### E.1.6 · `POST /auth/token/refresh` — Xoay token phiên

| Trường | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `refresh_token` | string | **Có** | — |
| `device_id` | uuid | **Có** | Phải khớp phiên |

**Response `200`:** cặp token mới (refresh XOAY — bản cũ vô hiệu; tái sử dụng bản cũ ⇒ thu hồi cả chuỗi phiên, nghi lộ token).

**Lỗi riêng:** `PIN-401-AUTH` refresh sai/hết hạn/đã revoke (đăng nhập lại).

<a id="muc-e-1-7-post-auth-pin-reset-quen-pin-us-38-cong-khai-verifytok"></a>
#### E.1.7 · `POST /auth/pin/reset` — Quên PIN (US-38, công khai + verify_token)

Request: `{ verify_token (purpose=pin_reset), new_pin, new_pin_confirm }` → **Response `200`:** `{ "status": "ok", "sessions_revoked": true }` — mọi phiên cũ thu hồi, đăng nhập lại. Lỗi như E.1.4.

<a id="muc-e-1-8-post-auth-emergency-lock-khoa-khan-us-39-ac-10-1-cong"></a>
#### E.1.8 · `POST /auth/emergency-lock` — Khóa khẩn (US-39, AC-10.1; công khai — gọi từ máy bất kỳ/hotline 8686)

| Trường | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `msisdn` | E.164 | **Có** | SIM đăng ký |
| `otp_id` + `code` | uuid + string(6) | **Có** | OTP purpose=`emergency_lock` gửi về SIM đăng ký (hotline đọc hộ thao tác) |

**Response `200`:** `{ "status": "locked", "locked_at": "...", "sessions_revoked": true }` — mọi phiên thu hồi ≤60s; **QR vẫn nhận tiền bình thường** (M4 không phụ thuộc phiên app); SMS xác nhận. Msisdn không tồn tại vẫn trả `200 {status:"locked"}` (chống dò).

**Lỗi riêng:** `BIZ-OTP-INVALID`.

<a id="muc-e-1-9-post-admin-auth-login-portal-buoc-1-2-cong-khai"></a>
#### E.1.9 · `POST /admin/auth/login` — Portal bước 1/2 (công khai)

Request: `{ email, password }` → **Response `200`:** `{ "mfa_token": "{JWT 5 phút}", "totp_required": true }`. Lỗi: `PIN-401-AUTH` (không phân biệt email/mật khẩu sai; `details.attempts_left`; khóa 15 phút sau 5 lần) · `PIN-409-STATE` user `disabled`.

<a id="muc-e-1-10-post-admin-auth-totp-portal-buoc-2-2-cong-khai-mfatok"></a>
#### E.1.10 · `POST /admin/auth/totp` — Portal bước 2/2 (công khai + mfa_token)

Request: `{ mfa_token, totp_code (6 số, TOTP RFC6238 ±1 bước) }` → **Response `200`:** `{ access_token (15 phút, claim role/org), refresh_token (12 giờ), user: {id, email, role, org} }`. Lỗi: `PIN-401-AUTH` (mã sai/mfa_token hết hạn).

<a id="muc-e-2-ekyc-man-nb-2a-1c"></a>
### E.2. eKYC (màn NB-2A/1C)

<a id="muc-e-2-1-post-ekyc-photos-upload-anh-ekyc-quyen-merchant-status"></a>
#### E.2.1 · `POST /ekyc/photos` — Upload ảnh eKYC · Quyền: merchant (status `draft`/`need_more`)

`multipart/form-data`:

| Part | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `side` | enum | **Có** | `front` \| `back` \| `selfie` |
| `file` | jpeg ≤200KB | **Có** | Đã nén + chấm mờ tại máy (UX-2); server chỉ kiểm type/size |

**Response `201`:** `{ "object_key": "ekyc/{person_id}/front_9d2.jpg", "side": "front", "uploaded_at": "..." }` — key giữ 5 năm sau đóng gian (retention); upload lại cùng `side` → key mới thay thế.

**Lỗi riêng:** `PIN-400-VAL` sai type/size · `PIN-409-STATE` hồ sơ không ở trạng thái cho phép (đã `approved`).

<a id="muc-e-2-2-post-ekyc-submit-nop-ho-so-ekyc-quyen-merchant"></a>
#### E.2.2 · `POST /ekyc/submit` — Nộp hồ sơ eKYC · Quyền: merchant

Chạy pipeline async «v3.6 — TẠO LÀ ACTIVE»: E1 verify (PASS = điều kiện kỹ thuật KYC2) → hoàn tất gian hàng + TK nhận → merchant `active` NGAY (KHÔNG cổng duyệt) + sinh QR/lệnh standee; E2 screen chạy song song: `hit` HOẶC `score < AUTO_ACTIVATE_SCORE(0.85)` HOẶC E2 5xx → VẪN active + cờ `post_review` vào danh sách hậu kiểm BRH-03 (≤24h, suspend 1 chạm); hồ sơ sạch hậu kiểm mẫu 10%.

**Request:**

| Trường | Kiểu | Bắt buộc | Mô tả | Ví dụ |
|---|---|---|---|---|
| `full_name` | string ≤140 | **Có** | Đúng theo CIN (C1) | `"MARIE DELVA"` |
| `dob` | date | **Có** | — | `"1988-03-14"` |
| `cin_no` | string ≤20 | **Có** | Số CIN — unique theo person | `"003-118-224-7"` |
| `nif_no` | string ≤20 | Không | Số NIF (BRH III.1.A chấp nhận CIN hoặc NIF — CIN-first, NIF bổ sung khi có) «CR-5 15/08» | `"NIF-884-221-9"` |
| `front_key` / `back_key` / `selfie_key` | string | **Có** | `object_key` từ E.2.1 | — |
| `shop_name` | string ≤80 | **Có** | «v3.6» — chuyển từ E.1.1 sang (khai ở NB-2B) | `"Boutique Marie"` |
| `business_type` | string ≤40 | Không | «v3.6» — chuyển từ E.1.1 sang; danh mục cấu hình — KHÔNG lưu cột riêng, chỉ dùng suy `merchant.mcc` (ánh xạ trong `param`) | `"legume"` |
| `market_id` | uuid | **Có** | «v3.6» — chuyển từ E.1.1 sang; danh mục 9 chợ · 3 TP | — |
| `agent_code` | string ≤16 | Không | «v3.6» — app truyền lại từ bước đăng ký; ghi `merchant.agent_code` (US-06) | `"NAT-014"` |

**Response `202`:** `{ "application_id": "{uuid}", "status": "processing" }` — kết quả về qua notification + E.2.3 (E1 >10s: app hiện «để máy đó, xong sẽ báo»).

**Lỗi riêng:** `PIN-409-STATE` đang `processing`/đã `approved` · `PIN-400-VAL` thiếu key/CIN sai format/`market_id` không tồn tại · `PIN-422-BIZ`/`BIZ-DUP-CLIENT-UUID` không áp dụng; CIN đã thuộc person khác → `PIN-409-STATE` (`details.field="cin_no"`).

<a id="muc-e-2-3-get-applications-me-trang-thai-ho-so-nb-1c-quyen-merch"></a>
#### E.2.3 · `GET /applications/me` — Trạng thái hồ sơ (NB-1C) · Quyền: merchant

**Response `200`:**

| Trường | Kiểu | Mô tả |
|---|---|---|
| `application_id` | uuid | — |
| `status` | enum | `processing` · `pending_review` (cờ HẬU KIỂM — gian hàng VẪN active «v3.6») · `need_more` · `approved` · `rejected` — ánh xạ từ enum DB (DataDict §3): `submitted`→`processing`, `auto_approved`→`approved` (đa số hồ sơ «v3.6»), còn lại 1–1 |
| `steps.ekyc` | object | `{status: pending\|passed\|failed\|need_retake, score?, reason?}` — reason đã bản địa hóa kiểu UX-6 («Ảnh mờ — chụp lại chỗ sáng hơn») |
| `steps.aml` | object | `{status: pending\|clear\|review}` — KHÔNG lộ chi tiết danh sách trúng |
| `steps.account_link` | object | `{status: pending\|linked\|opened\|failed, account_no_masked?}` |
| `need_more` | object \| null | `{items: [{side\|field, reason}], message}` — khi `need_more` |
| `rejected_reason` | string \| null | Bắt buộc có khi `rejected` (AC-6.1) |
| `submitted_at` / `decided_at` | RFC3339 | `decided_at` null khi chưa kết luận; SLA HẬU KIỂM hồ sơ có cờ ≤24h («v3.6») |

<a id="muc-e-2-4-post-applications-me-resubmit-nop-lai-theo-yeu-cau-bo"></a>
#### E.2.4 · `POST /applications/me/resubmit` — Nộp lại theo yêu cầu bổ sung · Quyền: merchant

Request: chỉ các trường cần sửa `{ front_key?, back_key?, selfie_key?, cin_no?, full_name?, dob? }` → **Response `202`** như E.2.2 (không nhập lại phần đã đạt — AC-1.2). **Lỗi riêng:** `PIN-409-STATE` không ở `need_more`.

<a id="muc-e-3-tai-khoan-nhan-lien-ket-man-nb-2b-14-luong-s4"></a>
### E.3. Tài khoản nhận & liên kết (màn NB-2B/14 · luồng S4)

<a id="muc-e-3-1-get-links-danh-sach-lien-ket-quyen-merchant"></a>
#### E.3.1 · `GET /links` — Danh sách liên kết · Quyền: merchant

**Response `200` — `items[]`:**

| Trường | Kiểu | Mô tả | Ví dụ |
|---|---|---|---|
| `link_id` | uuid | ID phía MMS (`account_link.id`) | — |
| `ext_link_id` | string | ID bank cấp (khớp `link_id` trong M4) | `"lnk_01HX4Y7Q2K"` |
| `bank_code` / `bank_name` | string | — | `"NTRF"` / `"wallet2"` |
| `account_no_masked` | string | — | `"…7709"` |
| `holder_name` | string | Từ M1 confirm | `"MARIE DELVA"` |
| `status` | enum | `active` · `grace` (TK cũ trong 30 ngày sau đổi — vẫn nhận M4) · `revoked` | — |
| `grace_until` | RFC3339 \| null | Khi `grace` | — |
| `token` | object | `{status: active\|expiring\|revoked, expires_at}` — `expiring` khi ≤ D-7 → app ghim cảnh báo | — |
| `is_primary` | bool | TK in trên QR/standee hiện hành | `true` |


> «Peye-Haiti 15/08» — nhóm E.3 áp dụng cho CẢ HAI LOẠI liên kết: **NHẬN TIỀN (receiving — gắn gian hàng)** và **NGUỒN TRẢ (funding — holder=person, MỌI vai)**: liên kết nguồn trả không cần eKYC (KYC1); request thêm `requested_scope:["payment","history"]`; trần riêng **2 liên kết nguồn trả active/person**.
<a id="muc-e-3-2-post-links-lien-ket-tk-da-co-buoc-1-khoi-tao-gui-otp-u"></a>
#### E.3.2 · `POST /links` — Liên kết TK đã có, bước 1: khởi tạo + gửi OTP (US-03) · Quyền: merchant (eKYC đã pass)

Server gọi M1 (C.1) → **bank gửi OTP tới SĐT chủ TK mà bank đang giữ**. Bank tự phán định TK có thuộc người này không — MMS không đối chiếu tên; chỉ chính chủ nhận được OTP mới hoàn tất được ở bước E.3.3.

**Request:**

| Trường | Kiểu | Bắt buộc | Mô tả | Ví dụ |
|---|---|---|---|---|
| `bank_code` | string(4) | **Có** | Danh mục bank tham gia OB (footprint: wallet2 + 1 bank) | `"NTRF"` |
| `account_no` | string ≤32 | **Có** | Số TK/ví — chỉ dùng trong luồng, lưu mã hóa | `"50912347709"` |

**Response `201`:**

| Trường | Kiểu | Mô tả |
|---|---|---|
| `link_request_id` | uuid | Phiên liên kết MMS (TTL 15 phút) |
| `otp` | object | `{sent_to_masked, expires_in_s}` — OTP do BANK gửi tới SĐT gắn TK |

**Lỗi riêng:** `BIZ-ACC-NOT-FOUND` (OB-404-ACC — số TK không tồn tại) · `BIZ-ACC-LOCKED` (OB-423-LOCK) · `BIZ-EKYC-PENDING` chưa pass eKYC (CHỈ liên kết NHẬN TIỀN — liên kết NGUỒN TRẢ (KYC1) không áp dụng) · `PIN-409-STATE` đã đủ trần link active (nhận tiền 1–2 bank; nguồn trả 2 liên kết/người) · `PIN-503-DEP` bank down. *(Không có bước đối chiếu tên: chủ TK không đúng → không nhận được OTP → dừng ở E.3.3.)*

<a id="muc-e-3-3-post-links-confirm-buoc-2-otp-bank-nhan-token-quyen-me"></a>
#### E.3.3 · `POST /links/confirm` — Bước 2: OTP bank → nhận token · Quyền: merchant

**Request:** `{ "link_request_id": "{uuid}", "otp": "482913" }`

**Response `200`:**

| Trường | Kiểu | Mô tả |
|---|---|---|
| `link_id` / `ext_link_id` | uuid / string | Link mới `active` |
| `bank_code` / `account_no_masked` / `holder_name` | — | — |
| `token_expires_at` | RFC3339 | +90 ngày |
| `qr` | object | `{payload, qr_version}` — payload EMVCo tĩnh theo TK này (client lưu render offline); nếu là cutover: `qr_version` tăng + lệnh in standee tự tạo |
| `cutover` | object \| null | Khi từ E.3.5: `{old_link_id, old_status: "grace", grace_until}` |

Side-effect: lưu token vault (envelope AES-256-GCM) · cập nhật E3-reg (D.4) · phát `merchant`-QR mới nếu cutover.

**Lỗi riêng:** `BIZ-OTP-INVALID` (OB-422-OTP, `attempts_left`) · `BIZ-ACC-LOCKED` (OB-423-LOCK — phiên khóa, làm lại từ E.3.2) · `PIN-404-NF` `link_request_id` sai/hết hạn 15 phút.

<a id="muc-e-3-5-post-links-change-doi-tk-nhan-cutover-s4-15-quyen-merc"></a>
#### E.3.5 · `POST /links/change` — Đổi TK nhận (cutover S4 ①→⑤) · Quyền: merchant

Khởi động quy trình đổi TK (S4 — trình tự nhiều bước có bù trừ, KHÁC với khớp tiền vốn là transaction đơn): sau khi confirm (E.3.3) — ① token MỚI trên TK mới · ② QR mới (`qr_version`+1) + lệnh in standee + app cho in QR giấy A5 tạm · ③ TK cũ `grace` `OLD_LINK_GRACE=30 ngày` (M4 TK cũ vẫn về, vẫn «ting ting» + gạch bill — AC-2.4) · ④ merchant xác nhận đã dán (E.3.6) · ⑤ hết grace + đã dán → M1b thu hồi + E3-reg cập nhật.

**Request:**

| Trường | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `old_link_id` | uuid | **Có** | Link đang `active` bị thay |
| `bank_code` | string(4) | **Có** | Bank của TK mới |
| `account_no` | string ≤32 | **Có** | TK mới |

**Response `201`:** như E.3.2 + `cutover_preview: { old_link_id, grace_until_estimate }` — tiếp tục bằng E.3.3 với `link_request_id`.

**Lỗi riêng:** `BIZ-TOKEN-REVOKED` old link đã revoked · `PIN-409-STATE` đang có cutover dở (grace chưa xong với chính bank đó — DDL cho phép tối đa 2 link song song cùng bank trong grace) · + toàn bộ lỗi của E.3.2.

<a id="muc-e-3-6-post-links-linkid-confirm-standee-xac-nhan-da-dan-stan"></a>
#### E.3.6 · `POST /links/{link_id}/confirm-standee` — Xác nhận «đã dán standee mới» (S4 bước ④) · Quyền: merchant

Request: `{}` → **Response `200`:** `{ "link_id": "...", "standee_status": "mounted", "mounted_at": "..." }` — điều kiện cần để bước ⑤ thu hồi TK cũ chạy khi hết grace; đồng bộ tracking BRH-04. **Lỗi riêng:** `PIN-409-STATE` link không trong cutover/không có standee `replacing`.

<a id="muc-e-3-7-post-links-renew-gia-han-token-thu-cong-nut-nb-14-job"></a>
#### E.3.7 · `POST /links/renew` — Gia hạn token thủ công (nút NB-14; job D-7 tự chạy) · Quyền: merchant

**Request:** `{ "link_id": "{uuid}" }` → gọi M1a (C.3).

**Response `200`:** `{ "link_id": "...", "token": { "status": "active", "expires_at": "+90d mới" } }`

**Lỗi riêng:** `BIZ-TOKEN-REVOKED` (→ CTA re-link E.3.2) · `PIN-422-BIZ`/`BIZ-TOKEN-REVOKED` với `details.issue="refresh_expired"` refresh quá 12 tháng — bắt buộc liên kết lại · `PIN-503-DEP`.

<a id="muc-e-4-qr-bill-man-nb-04-07-08-luong-s3"></a>
### E.4. QR & bill (màn NB-04/07/08 · luồng S3)

> Nguyên tắc A9: **QR luôn render OFFLINE phía app** (payload §13.4 TSD); API dưới đây chỉ tăng độ chính xác gạch & tiện ích chia sẻ — KHÔNG BAO GIỜ là điều kiện để thu được tiền.

<a id="muc-e-4-1-get-qr-static-payload-qr-tinh-hien-hanh-quyen-merchant"></a>
#### E.4.1 · `GET /qr/static` — Payload QR tĩnh hiện hành · Quyền: merchant

**Response `200`:**

| Trường | Kiểu | Mô tả | Ví dụ |
|---|---|---|---|
| `link_id` | uuid | TK liên kết đang là primary | — |
| `payload` | string | Chuỗi EMVCo theo **HTQR 1.0** (tag 38: 00=GUID `ht.brh.htqr` · 01=định chế 9332xx · 02=SỐ TK THẬT; 52=MCC; 53=332; 58=HT; 59 tên; 60 TP; 63 CRC — TSD §13.4, CR-3) — client cache & render offline | `"000201010211…6304A1B2"` |
| `mcc` | string(4) | Tag 52 — `merchant.mcc` (CR-1) | `"5411"` |
| `qr_version` | int | Tăng khi đổi TK — client thấy tăng thì thay payload cache + nhắc thay standee | `2` |
| `account_no_masked` / `bank_code` | string | Hiển thị dưới QR | `"…7709"` |
| `merchant_name` / `city` | string | Tag 59/60 | `"MARIE DELVA"` / `"PETION-VILLE"` |
| `updated_at` | RFC3339 | — | — |

**Lỗi riêng:** `PIN-409-STATE` chưa có link active (chưa xong onboarding).

<a id="muc-e-4-3-post-bills-tao-don-tinh-tien-us-14-15-quyen-merchant"></a>
#### E.4.3 · `POST /bills` — Tạo đơn tính tiền (US-14/15) · Quyền: merchant

**Request:**

| Trường | Kiểu | Bắt buộc | Mô tả | Ví dụ |
|---|---|---|---|---|
| `client_uuid` | uuid | **Có** | Idempotency offline | — |
| `code` | string ≤16 | **Có** | `B-<ddMM>-<seq>` client sinh, seq reset theo ngày; unique (merchant, biz_date, code) | `"B-1007-17"` |
| `items[]` | array ≥1 | **Có** | Món trong bill | — |
| `items[].product_id` | uuid \| null | Không | Null = món gõ tay | — |
| `items[].name` | string ≤80 | **Có** | Snapshot tên tại thời điểm bán | `"Diri (sak)"` |
| `items[].qty` | int ≥1 | **Có** | — | `2` |
| `items[].price_ct` | int64 ≥0 | **Có** | Đơn giá snapshot | `100000` |
| `total_ct` | int64 | **Có** | Server verify `= Σ qty×price_ct` — lệch → `PIN-400-VAL` | `214000` |
| `note` | string ≤140 | Không | — | — |
| `created_at_client` | RFC3339 | **Có** | — | — |

**Response `201`:**

| Trường | Kiểu | Mô tả |
|---|---|---|
| `bill_id` / `code` | uuid / string | — |
| `status` | enum | `open` |
| `total_ct` | int64 | — |
| `qr_expires_at` | RFC3339 | +`QR_DYNAMIC_TTL` 15 phút (TTL của MÃ với người quét — app tự xoay; matching KHÔNG giới hạn 15 phút) |
| `expires_at` | RFC3339 | +`BILL_TTL` 24h — hết hạn tự `expired` (job server, giờ server) |
| `biz_date` | date | = `created_at_client` quy về múi giờ Haiti (`America/Port-au-Prince`) — chốt v1.1 |
| `version` | int | `0` — optimistic lock |

**Lỗi riêng:** `BIZ-DUP-CLIENT-UUID` (trùng uuid khác payload; trùng + giống → `200` bill cũ) · `BIZ-MERCHANT-STATE` · `PIN-409-STATE` trùng (merchant, biz_date, code) với bill khác. (bill offline sync KHÔNG bao giờ bị từ chối; giám sát AML hậu kiểm qua sự kiện `limit.breached`.)

<a id="muc-e-4-4-get-bills-status-bizdate-cursor-pagesize-bill-trong-ng"></a>
#### E.4.4 · `GET /bills?status&biz_date&cursor&page_size` — Bill trong ngày, 3 nhóm (NB-08, US-17) · Quyền: merchant

Query: `status` ∈ `open|paid|cash|cancelled|expired|credit` (bỏ trống = tất cả), `biz_date` mặc định hôm nay.

**Response `200`:** `items[]`:

| Trường | Kiểu | Mô tả |
|---|---|---|
| `bill_id` / `code` / `status` / `total_ct` / `biz_date` / `version` | — | — |
| `items_count` | int | Số dòng món |
| `created_at` / `expires_at` | RFC3339 | — |
| `paid_at` | RFC3339 \| null | Khi `paid` |
| `credit_event_id` | uuid \| null | Khoản tiền đã gạch vào |
| `debtor_id` | uuid \| null | Khi `credit` (bán chịu) |

+ `summary`: `{ open: {count, total_ct}, paid: {...}, cash: {...}, credit: {...}, cancelled: {...}, expired: {...} }` — một nguồn số liệu khớp NB-08/09/10 (AC-3.1).

<a id="muc-e-4-5-post-bills-billid-close-cash-dong-da-thu-tien-mat-us-1"></a>
#### E.4.5 · `POST /bills/{bill_id}/close-cash` — Đóng «đã thu TIỀN MẶT» (US-16) · Quyền: merchant

**Request:** `{ "version": 0 }` → **Response `200`:** `{ "bill_id", "status": "cash", "closed_at", "version": 1 }` — nằm NGOÀI dòng tiền QR/đối soát (AC-3.4).

**Lỗi riêng:** `BIZ-BILL-STATE` bill không ở `open` (vd đã `paid` — «đã có tiền về», kèm `details.server_state`) · `PIN-409-STATE` version lệch (`details.server_state` để client tự merge).

<a id="muc-e-4-6-post-bills-billid-cancel-huy-bill-quyen-merchant"></a>
#### E.4.6 · `POST /bills/{bill_id}/cancel` — Hủy bill · Quyền: merchant

**Request:** `{ "version": 0, "reason": "khach doi y" }` (reason ≤140, không bắt buộc — ghi log) → **Response `200`:** `{ "status": "cancelled", ... }`. **Lỗi riêng:** như E.4.5.

<a id="muc-e-4-7-get-bills-billid-qr-payload-qr-dong-cua-bill-chia-se-i"></a>
#### E.4.7 · `GET /bills/{bill_id}/qr` — Payload QR động của bill (chia sẻ/in lại) · Quyền: merchant

**Response `200`:** `{ "bill_id", "code", "amount_ct", "payload" (HTQR 1.0 động: point 12, tag 52 MCC, tag 54 = số tiền, tag 62-01 = bill code — chỉ khi D1/D2 bảo toàn addenda; TSD §13.4), "qr_expires_at" (server tính lại theo TTL còn lại) }` — app offline vẫn tự render, endpoint này cho nhu cầu share link/in.

**Lỗi riêng:** `BIZ-BILL-STATE` bill không `open`.

<a id="muc-e-5-tien-ve-khop-man-nb-05-09-luong-s2-s7"></a>
### E.5. Tiền về & khớp (màn NB-05/09 · luồng S2/S7)

<a id="muc-e-5-1-get-credit-events-from-to-matchlevel-cursor-pagesize-d"></a>
#### E.5.1 · `GET /credit-events?from&to&match_level&cursor&page_size` — Danh sách tiền về («két tiền») · Quyền: merchant

Query: `from/to` RFC3339 (mặc định hôm nay theo giờ Haiti); `match_level` ∈ `PENDING|LINK|MANUAL|STRAY`.

**Response `200`:** `items[]`:

| Trường | Kiểu | Mô tả | Ví dụ |
|---|---|---|---|
| `credit_event_id` | uuid | — | — |
| `amount_ct` / `currency` | int64 / string | — | `150000` / `"HTG"` |
| `booked_at` / `received_at` | RFC3339 | T0 bank ghi Có / MMS nhận | — |
| `ref_id` | string \| null | RefID Switch — hiển thị trên biên lai để khiếu nại; null = on-us | `"PIN-2026-000123"` |
| `account_no_masked` / `bank_code` | string | TK nhận | `"…7709"` |
| `payer` | object | `{name: "J. PIERRE", msisdn_masked: "+509****3456", bank_code}` | — |
| `narrative` | string \| null | — | — |
| `source` | enum | `m4` · `m3poll` | — |
| `replayed` / `late_auto` | bool | Bản phát lại / khớp-muộn sau xác nhận tay | — |
| `match` | object | `{level, target_type: bill\|ledger\|stray \| null, target_id, target_label}` — `target_label` vd `"B-1007-17"` hoặc `"Nợ · Jean"` | — |
| `suggestion` | object \| null | Khi `PENDING` có nợ mở trùng tiền (S7): `{type: "ledger", debtor_id, debtor_name, entry_id, amount_ct}` — app hỏi «gạch nợ Jean?» | — |
| `is_revenue` | bool | `false` = đã đánh dấu «không phải doanh thu» (US-40) | `true` |
| `receipt_id` | uuid \| null | — | — |
| `case` | object \| null | `{case_code, status}` nếu có khiếu nại | — |

+ `summary`: `{ day_total_ct, day_count, pending_count }`.

<a id="muc-e-5-2-post-credit-events-id-confirm-match-xac-nhan-khop-muc"></a>
#### E.5.2 · `POST /credit-events/{id}/confirm-match` — Xác nhận khớp mức ② (tay) / chốt đề xuất gạch nợ (S7) · Quyền: merchant

**Request:**

| Trường | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `target_type` | enum | **Có** | `bill` · `ledger` · `stray` (`stray` = xác nhận là tiền vãng lai, đóng PENDING) |
| `target_id` | uuid | khi `bill`/`ledger` | `bill_id` đang `open` cùng số tiền, hoặc `ledger_entry_id` (khoản nợ `debt` mở) — gạch nợ tạo entry `repay(origin=auto)` tham chiếu credit; đã gạch-tay-trước → server tham chiếu vào entry đó, KHÔNG trừ 2 lần (AC-4.3) |

**Response `200`:** `{ "credit_event_id", "match": { "level": "MANUAL", "target_type", "target_id", "target_label", "matched_at" }, "receipt_id" }`

**Lỗi riêng:** `PIN-409-STATE` credit đã có đích (invariant «1 credit ↔ ≤1 đích»; `details.current_match`) · `BIZ-BILL-STATE` bill không còn `open`/khác số tiền · `PIN-404-NF` target không thuộc merchant.

<a id="muc-e-5-3-get-credit-events-id-receipt-bien-lai-quyen-merchant"></a>
#### E.5.3 · `GET /credit-events/{id}/receipt` — Biên lai · Quyền: merchant

**Response `200`:**

| Trường | Kiểu | Mô tả |
|---|---|---|
| `receipt_id` / `credit_event_id` | uuid | — |
| `merchant` | object | `{code, shop_name, market_name, city}` |
| `amount_ct` / `currency` / `booked_at` | — | — |
| `ref_id` | string \| null | Mã tham chiếu khiếu nại |
| `payer` | object | `{name, msisdn_masked, bank_code}` |
| `bill_code` | string \| null | Nếu đã gạch bill |
| `status` | enum | `normal` · `refunded` (case chốt «Đã hoàn» — AC-7.3, kèm `refund_case_code`) |
| `channels_sent[]` | array | `["app"]`, thêm `"sms"` nếu đã gửi khách |

<a id="muc-e-5-4-post-credit-events-id-report-issue-nguoi-ban-bao-sai-g"></a>
#### E.5.4 · `POST /credit-events/{id}/report-issue` — Người bán báo sai giao dịch → mở case · Quyền: merchant

**Request:**

| Trường | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `type` | enum | **Có** | `wrong_amount` · `not_received` · `duplicate` · `other` |
| `description` | string ≤500 | **Có** | Lời khai |
| `evidence_keys[]` | array\<string\> | Không | `object_key` từ `POST /media` |

**Response `201`:** `{ "case_id", "case_code": "CS-2026-000045", "ref_id", "sla": { "first_response_due_at": "+CASE_SLA_FIRST(24h)", "close_due_at": "+CASE_SLA_CLOSE(5 ngày làm việc)" } }`

**Lỗi riêng:** `PIN-409-STATE` đã có case mở cho credit này (`details.case_code`).

<a id="muc-e-5-5-post-credit-events-id-send-receipt-gui-bien-lai-cho-kh"></a>
#### E.5.5 · `POST /credit-events/{id}/send-receipt` — Gửi biên lai cho khách (US-24) · Quyền: merchant

**Request:** `{ "msisdn": "+50937123456" }` → **Response `202`:** `{ "channels": ["sms"], "sms_id": "..." }` — gửi biên lai cho khách qua SMS (người mua trả bằng app wallet2, nhận biên lai qua SMS — US-24).

**Lỗi riêng:** `PIN-429-RATE` vượt `SMS_RATE_LIMIT` 5/giờ/merchant · `PIN-400-VAL` msisdn.

<a id="muc-e-5-6-post-credit-events-id-revenue-flag-danh-dau-khong-phai"></a>
#### E.5.6 · `POST /credit-events/{id}/revenue-flag` — Đánh dấu «không phải doanh thu» (US-40, AC-2.7) · Quyền: merchant

**Request:** `{ "is_revenue": false, "reason": "personal" | "family" | "other" }` (đặt lại `true` để hoàn tác) → **Response `200`:** `{ "credit_event_id", "is_revenue": false }` — loại khỏi doanh số NB-10/BRH-08 & KPI matching, **VẪN tính trong giám sát AML**.

**Lỗi riêng:** không có lỗi đặc thù (mọi trạng thái match đều cho phép).

<a id="muc-e-6-so-no-man-nb-15-luong-s7-offline-first-100"></a>
### E.6. Sổ nợ (màn NB-15 · luồng S7, offline-first 100%)

<a id="muc-e-6-1-get-debtors-q-cursor-pagesize-danh-sach-khach-no-quyen"></a>
#### E.6.1 · `GET /debtors?q&cursor&page_size` — Danh sách khách nợ · Quyền: merchant

**Response `200`:** `items[]`: `{ debtor_id, name, msisdn (nullable), balance_ct (dư nợ hiện tại = Σ debt − Σ repay), open_entries_count, last_entry_at, last_remind_at }` + `summary: { total_outstanding_ct, debtor_count }`.

<a id="muc-e-6-2-post-debtors-them-khach-no-quyen-merchant"></a>
#### E.6.2 · `POST /debtors` — Thêm khách nợ · Quyền: merchant

**Request:** `{ "client_uuid": "{uuid}", "name": "Jean B.", "msisdn": "+50934567890" | null }` → **Response `201`:** `{ "debtor_id", "name", "msisdn", "balance_ct": 0 }`.

**Lỗi riêng:** `BIZ-DUP-CLIENT-UUID` · `PIN-400-VAL` name rỗng.

<a id="muc-e-6-3-post-debtors-id-entries-ghi-no-ghi-tra-us-18-10-giay-q"></a>
#### E.6.3 · `POST /debtors/{id}/entries` — Ghi nợ / ghi trả (US-18, ≤10 giây) · Quyền: merchant

**Request:**

| Trường | Kiểu | Bắt buộc | Mô tả | Ví dụ |
|---|---|---|---|---|
| `client_uuid` | uuid | **Có** | Idempotency — chống trừ 2 lần khi sync (AC-4.3) | — |
| `type` | enum | **Có** | `debt` (ghi nợ) \| `repay` (ghi trả tay, `origin=manual`; `repay origin=auto` CHỈ server tạo từ gạch nợ QR) | `"debt"` |
| `amount_ct` | int64 > 0 | **Có** | — | `90000` |
| `note` | string ≤140 | Không | — | — |
| `due_at` | RFC3339 | Không | Hẹn trả | — |
| `bill_id` | uuid | Không | Khi từ nút «Bán chịu» của bill (bill → `credit`) | — |
| `created_at_client` | RFC3339 | **Có** | — | — |

**Response `201`:** `{ "entry_id", "debtor_id", "type", "amount_ct", "origin": "manual", "balance_ct" (dư nợ mới), "version": 0 }` — entry KHÔNG sửa được, chỉ thêm bút ghi đảo.

**Lỗi riêng:** `BIZ-DUP-CLIENT-UUID` · `BIZ-BILL-STATE` bill kèm không ở `open` · `PIN-404-NF` debtor. (`repay` vượt dư nợ vẫn CHO PHÉP — sổ tay lệch thực tế, app cảnh báo client-side.)

<a id="muc-e-6-4-get-debtors-id-entries-cursor-lich-su-mot-khach-quyen"></a>
#### E.6.4 · `GET /debtors/{id}/entries?cursor` — Lịch sử một khách · Quyền: merchant

**Response `200`:** `items[]`: `{ entry_id, type, amount_ct, origin: "manual"|"auto", credit_event_id (nullable — khi gạch bằng QR), note, due_at, created_at, reversed_by_entry_id (nullable) }` + `debtor: {debtor_id, name, balance_ct}`.

<a id="muc-e-6-5-post-debtors-id-remind-nhac-no-1-cham-qua-sms-us-19-ac"></a>
#### E.6.5 · `POST /debtors/{id}/remind` — Nhắc nợ 1 chạm qua SMS (US-19, AC-4.4) · Quyền: merchant

**Request:** `{}` (template `DEBT_REMIND`, ngôn ngữ theo merchant, kèm tên gian + dư nợ) → **Response `202`:** `{ "sms_id", "sent_at" }` — SMS tới khách ≤10 giây.

**Lỗi riêng:** `BIZ-REMIND-LIMIT` đã nhắc hôm nay (tối đa 1 tin/khách/ngày — `details.next_allowed_at`) · `PIN-400-VAL` debtor không có `msisdn` · `PIN-409-STATE` dư nợ = 0.

<a id="muc-e-7-danh-muc-san-pham-man-nb-06-hau-kiem-c9"></a>
### E.7. Danh mục sản phẩm (màn NB-06 · hậu kiểm C9)

<a id="muc-e-7-1-get-products-includedeleted-false-cursor-danh-muc-mon"></a>
#### E.7.1 · `GET /products?include_deleted=false&cursor` — Danh mục món · Quyền: merchant

**Response `200`:** `items[]`: `{ product_id, name, price_ct, photo_key (nullable), photo_url (presigned GET, nullable), moderation: "pending"|"ok"|"removed" (nhãn «chờ kiểm duyệt» CHỈ nội bộ — hiển thị NGAY cho khách trừ `removed`), removed_reason (nullable), deleted_at (nullable), updated_at, version }`.

<a id="muc-e-7-2-post-products-them-mon-quyen-merchant"></a>
#### E.7.2 · `POST /products` — Thêm món · Quyền: merchant

**Request:** `{ "client_uuid", "name" ≤80, "price_ct" ≥ 0, "photo_key" (từ POST /media, nullable) }` → **Response `201`:** `{ product_id, name, price_ct, photo_key, moderation: "pending", version: 1 }` — hiển thị ngay (hậu kiểm).

**Lỗi riêng:** `BIZ-DUP-CLIENT-UUID` · `PIN-400-VAL`.

<a id="muc-e-7-3-patch-products-id-sua-xoa-mem-quyen-merchant"></a>
#### E.7.3 · `PATCH /products/{id}` — Sửa / xóa mềm · Quyền: merchant

**Request (mọi trường optional, gửi trường nào sửa trường đó):** `{ "name"?, "price_ct"?, "photo_key"?, "deleted"?: true, "version": n }` → **Response `200`:** bản ghi mới. Sửa nội dung sau khi `removed` → `moderation` quay về `pending` (khắc phục vi phạm, hậu kiểm lại).

**Lỗi riêng:** `PIN-409-STATE` version lệch (`details.server_state`) · `PIN-404-NF`.

<a id="muc-e-8-bao-cao-thong-bao-man-nb-10-13"></a>
### E.8. Báo cáo & thông báo (màn NB-10/13)

<a id="muc-e-8-1-get-reports-sales-range-day-week-month-date-bao-cao-ba"></a>
#### E.8.1 · `GET /reports/sales?range=day|week|month&date` — Báo cáo bán hàng · Quyền: merchant

`date` = mốc trong kỳ (mặc định hôm nay, giờ Haiti).

**Response `200`:**

| Trường | Kiểu | Mô tả |
|---|---|---|
| `range` / `from` / `to` | — | Kỳ báo cáo (biz_date) |
| `totals.qr_ct` | int64 | Tiền QR đã khớp (loại `is_revenue=false` và khoản đã hoàn) |
| `totals.stray_ct` | int64 | Vãng lai (STRAY/MANUAL-stray, vẫn là doanh thu) |
| `totals.cash_ct` | int64 | Bill đóng tiền mặt |
| `totals.credit_extended_ct` / `totals.repaid_ct` | int64 | Bán chịu mới / nợ đã thu |
| `totals.refunded_ct` | int64 | Đã hoàn (trừ khỏi doanh số — AC-7.3) |
| `totals.non_revenue_ct` | int64 | Khoản «không phải doanh thu» (chỉ tham khảo) |
| `counts` | object | `{qr, cash, bills_open, bills_expired}` |
| `by_day[]` | array | `{date, qr_ct, cash_ct, stray_ct, count}` — vẽ biểu đồ |
| `top_products[]` | array ≤10 | `{name, qty, amount_ct}` |
| `settled_through` | date | Số liệu CHỐT theo ngày đối soát gần nhất (sau đó là tạm tính — AC-6.4) |

<a id="muc-e-8-2-get-notifications-unread-cursor-hop-thong-bao-quyen-me"></a>
#### E.8.2 · `GET /notifications?unread&cursor` — Hộp thông báo · Quyền: merchant

**Response `200`:** `items[]`: `{ notification_id, kind: "credit"|"token_expiry"|"application"|"case"|"standee"|"system", title, body (đã bản địa hóa), params (object thô cho deep-link: {credit_event_id?...}), channel: "push"|"sms"|"inapp", status: "queued"|"sent"|"acked"|"failed", created_at, acked_at }` + `unread_count`.

<a id="muc-e-8-3-post-notifications-id-ack-xac-nhan-da-nhan-quyen-merch"></a>
#### E.8.3 · `POST /notifications/{id}/ack` — Xác nhận đã nhận · Quyền: merchant

Request `{}` → **Response `200`:** `{ "acked_at": "..." }`. Ack thông báo `credit` trong ≤60s là tín hiệu DỪNG fallback SMS (T1 của SLA ≤5s — AC-2.2); notification đã `acked` → idempotent `200`.

<a id="muc-e-9-dong-bo-offline-tsd-7"></a>
### E.9. Đồng bộ offline (TSD §7)

<a id="muc-e-9-1-post-sync-batch-dong-bo-2-chieu-theo-lo-quyen-merchant"></a>
#### E.9.1 · `POST /sync/batch` — Đồng bộ 2 chiều theo lô · Quyền: merchant

**Request:**

| Trường | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `device_id` | uuid | **Có** | — |
| `entries[]` | array ≤200, tổng body ≤500KB | **Có** | Hàng đợi client (client giữ ≤2.000 — cảnh báo NB-14) |
| `entries[].entity` | enum | **Có** | `bill` · `bill_item` · `ledger_entry` · `debtor` · `product` |
| `entries[].op` | enum | **Có** | `upsert` \| `delete` (delete chỉ `product` — soft) |
| `entries[].client_uuid` | uuid | **Có** | Khóa idempotent |
| `entries[].version` | int | **Có** | Version client biết lần cuối (0 = mới) |
| `entries[].payload` | object | **Có** | Body như POST tương ứng (E.4.3/E.6.2/E.6.3/E.7.2) |
| `entries[].client_ts` | RFC3339 | **Có** | Giờ thao tác tại máy |

**Response `200`:** `{ "server_time": "...", "results": [...] }` — MỖI entry một kết quả, CÙNG THỨ TỰ:

| Trường kết quả | Kiểu | Mô tả |
|---|---|---|
| `client_uuid` | uuid | Echo |
| `status` | enum | `applied` (kèm `server_id`, `version` mới) · `conflict` (kèm `server_state` — toàn bộ bản ghi server; client PHẢI lấy server làm chuẩn với TIỀN) · `rejected` (kèm `reason` = mã lỗi, vd `BIZ-BILL-STATE`, `PIN-400-VAL`) |
| `server_id` / `version` / `server_state` / `reason` | — | Theo status |

**Quy tắc xung đột (chốt):** TIỀN = server thắng — `bill.status` do server quyết theo credit_event, client KHÔNG BAO GIỜ set `paid`; ghi chú/danh mục = client thắng theo `client_ts` mới hơn; `ledger_entry` trùng `client_uuid` = idempotent. **Ma trận transition client-được-phép-set (bill):**

| Server đang | Client được set | Bị từ chối (`conflict{server_state}`) |
|---|---|---|
| `open` | `cash` · `cancelled` · `credit` | `paid` (chỉ server qua matching) |
| `paid` / `expired` | — (chỉ đọc) | mọi thay đổi |
| `cash` / `cancelled` / `credit` | — | mọi thay đổi |

**Lỗi envelope-level:** `PIN-400-VAL` >200 entries / >500KB / entity lạ (cả batch bị từ chối — client tự cắt lô).

<a id="muc-e-9-2-post-media-upload-anh-san-pham-chung-cu-quyen-merchant"></a>
#### E.9.2 · `POST /media` — Upload ảnh (sản phẩm, chứng cứ) · Quyền: merchant

`multipart/form-data`: `{ purpose: "product"|"evidence", file: jpeg/png ≤200KB }` → **Response `201`:** `{ "object_key": "media/{merchant_id}/p_8817.jpg", "url": "presigned GET TTL 1h", "expires_at" }`.

**Lỗi riêng:** `PIN-400-VAL` size/type (`details.hint`="nén ≤200KB").

<a id="muc-e-10-ho-so-nguoi-dung-me"></a>
### E.10. Hồ sơ người dùng (/me)

<a id="muc-e-10-4-get-me-ho-so-quyen-user-co-person-moi-vai-app-dung-me"></a>
#### E.10.4 · `GET /me` — Hồ sơ · Quyền: user có person (mọi vai — app dựng menu theo trạng thái merchant trả về)

**Response `200`:** `{ person_id, kind, msisdn_masked, display_name, lang, created_at }` (+ merchant: `{merchant: {code, shop_name, status, market}}`).

> «v3.6» `kind` = giá trị SUY DIỄN (`merchant` nếu person có bản ghi merchant, ngược lại `buyer`) — không phải cột DB (E.1.1 không còn nhận `kind`); app dùng nó + `merchant.status` để dựng menu sau CH-00.

<a id="muc-e-10-5-patch-me-sua-ho-so-nhe-quyen-user-co-person-moi-vai"></a>
#### E.10.5 · `PATCH /me` — Sửa hồ sơ nhẹ · Quyền: user có person (mọi vai)

**Request:** `{ "display_name"?, "lang"?: "fr"|"ht" }` → **Response `200`:** bản ghi mới. (Đổi msisdn KHÔNG hỗ trợ qua API này — xử lý qua kênh hỗ trợ có định danh lại.)

<a id="muc-e-11-portal-brh-hau-kiem-ho-so-quan-ly-merchant-v3-6-man-brh"></a>
### E.11. Portal BRH — hậu kiểm hồ sơ & quản lý merchant «v3.6» (màn BRH-03/04)

<a id="muc-e-11-1-get-admin-applications-status-flag-marketid-q-cursor"></a>
#### E.11.1 · `GET /admin/applications?status&flag&market_id&q&cursor` — Danh sách HẬU KIỂM hồ sơ («v3.6» — không phải hàng chặn: gian hàng đã active) · Quyền: approver (đọc: +supervisor_aml, inspector_read)

Query `status` ∈ `pending_review|need_more|approved|rejected|processing`; `flag` ∈ `ekyc_low_score|aml_hit|name_mismatch|e1_manual|sampled`.

**Response `200`:** `items[]`:

| Trường | Kiểu | Mô tả |
|---|---|---|
| `application_id` | uuid | — |
| `merchant` | object | `{id, code (null trước kích hoạt), shop_name, market: {name, city}, agent_code}` |
| `person` | object | `{full_name, dob, cin_masked ("003-***-**4-7"), msisdn_masked}` |
| `ekyc` | object | `{matched, score, ref, photos: {front_url, back_url, selfie_url — presigned 15 phút, chỉ vai trò approver}}` |
| `aml` | object | `{hit, lists[], score}` |
| `flags[]` | array | Lý do cờ vàng |
| `status` / `submitted_at` / `sla_due_at` | — | SLA hậu kiểm hồ sơ có cờ ≤24h («v3.6» — US-26 đổi nghĩa) |
| `assigned_to` | string \| null | Email cán bộ nhận ca |

<a id="muc-e-11-2-post-admin-applications-id-approve-dong-hau-kiem-ok-v"></a>
#### E.11.2 · `POST /admin/applications/{id}/approve` — Đóng hậu kiểm OK («v3.6» — gian hàng vốn đã active; đây là kết luận hậu kiểm) · Quyền: approver

**Request:** `{ "note"? ≤500 }` → **Response `200`:** `{ "application_id", "status": "approved", "merchant": { "id", "code": "PIN-M-000241", "status": "active", "activated_at" } }` — «v3.6»: QR/standee/SMS/`merchant.activated` đã phát từ lúc KÍCH HOẠT (E.2.2); endpoint này chỉ ghi kết luận hậu kiểm (`decided_by`/`decided_at`) + tắt cờ `post_review`.

**Lỗi riêng:** `PIN-409-STATE` không ở `pending_review` · `PIN-422-BIZ`/`BIZ-EKYC-PENDING` hồ sơ chưa đủ bước (chưa liên kết TK).

<a id="muc-e-11-3-post-admin-applications-id-reject-tu-choi-quyen-appro"></a>
#### E.11.3 · `POST /admin/applications/{id}/reject` — Từ chối · Quyền: approver

**Request:** `{ "reason" ≤500 — BẮT BUỘC (AC-6.1) }` → **Response `200`:** `{ "status": "rejected" }` — merchant nhận SMS + NB-1C đổi trạng thái, audit ghi vết.

**Lỗi riêng:** `BIZ-REASON-REQUIRED` thiếu reason · `PIN-409-STATE`.

<a id="muc-e-11-4-post-admin-applications-id-need-more-yeu-cau-bo-sung"></a>
#### E.11.4 · `POST /admin/applications/{id}/need-more` — Yêu cầu bổ sung · Quyền: approver

**Request:** `{ "items": [{"target": "front"|"back"|"selfie"|"cin_no"|"other", "reason" ≤200}], "message"? ≤500 }` → **Response `200`:** `{ "status": "need_more" }` — merchant nhận SMS + NB-1C hướng dẫn chụp lại đúng mục.

**Lỗi riêng:** `PIN-400-VAL` items rỗng · `PIN-409-STATE`.

<a id="muc-e-11-5-get-admin-merchants-status-marketid-q-cursor-danh-sac"></a>
#### E.11.5 · `GET /admin/merchants?status&market_id&q&cursor` — Danh sách merchant · Quyền: mọi vai trò portal (đọc)

**Response `200`:** `items[]`: `{ merchant_id, code, national_merchant_id (null ở pilot — cột chờ CR-2), mcc, shop_name, market: {name, city}, status: "active"|"suspended"|"closed"|..., activated_at, links: [{bank_code, account_no_masked, status, token_status}], standee: {status, qr_ver}, last_credit_at, today_total_ct, open_cases, agent_code }`.

<a id="muc-e-11-6-post-admin-merchants-id-suspend-tam-khoa-us-28-quyen"></a>
#### E.11.6 · `POST /admin/merchants/{id}/suspend` — Tạm khóa (US-28) · Quyền: supervisor_aml hoặc admin theo RBAC `/docs/rbac.csv`

**Request:** `{ "reason" — BẮT BUỘC }` → **Response `200`:** `{ "status": "suspended" }` — phát `merchant.suspended`: gắn cờ hạn chế gian hàng (`merchant_flag`); TK vẫn nhận tiền (ngoài đường tiền), app bị chặn thao tác ghi.

**Lỗi riêng:** `BIZ-REASON-REQUIRED` · `PIN-409-STATE` đã `suspended/closed`.

<a id="muc-e-11-7-post-admin-merchants-id-resume-mo-lai-quyen-nhu-e-11"></a>
#### E.11.7 · `POST /admin/merchants/{id}/resume` — Mở lại · Quyền: như E.11.6

**Request:** `{ "reason" — BẮT BUỘC }` → **Response `200`:** `{ "status": "active" }`. **Lỗi riêng:** `BIZ-REASON-REQUIRED` · `PIN-409-STATE` không ở `suspended`.

<a id="muc-e-11-8-post-admin-merchants-id-close-dong-gian-hang-s8-quyen"></a>
#### E.11.8 · `POST /admin/merchants/{id}/close` — Đóng gian hàng (S8) · Quyền: admin (thao tác), theo quy trình checklist

**Request:** `{ "reason" — BẮT BUỘC, "checklist": { "standee_recalled": true } }` → **Response `200`:** `{ "status": "closed", "revoked_links": ["..."] }` — side-effect: M1b thu hồi mọi token (bank ngừng M4) + E3-reg cập nhật + `merchant.closed`; tiền quét QR cũ (nếu còn) về TK thật của chính chủ — ngoài phạm vi hệ thống.

**Lỗi riêng:** `BIZ-REASON-REQUIRED` · `PIN-409-STATE` còn case `open`/`investigating` (đóng case trước) · `PIN-400-VAL` checklist chưa tick.

<a id="muc-e-11-9-patch-admin-merchants-id-standee-cap-nhat-tracking-st"></a>
#### E.11.9 · `PATCH /admin/merchants/{id}/standee` — Cập nhật tracking standee (BRH-04) · Quyền: admin/approver theo RBAC

**Request:** `{ "status": "ordered"|"printed"|"delivered"|"mounted"|"replacing"|"recalled", "note"? , "mounted_at"? }` — thứ tự hợp lệ theo state machine standee; `mounted` đồng bộ với xác nhận app (E.3.6).

**Response `200`:** `{ "standee": { "id", "merchant_id", "account_link_id", "qr_ver", "status", "mounted_at" } }`

**Lỗi riêng:** `PIN-409-STATE` transition sai (vd `ordered` → `mounted` bỏ qua giao nhận — `details.allowed=[...]`).

<a id="muc-e-12-portal-brh-giam-sat-gd-case-aml-man-brh-05-06-07"></a>
### E.12. Portal BRH — giám sát GD, case, AML (màn BRH-05/06/07)

<a id="muc-e-12-1-get-admin-transactions-from-to-merchantid-refid-amoun"></a>
#### E.12.1 · `GET /admin/transactions?from&to&merchant_id&ref_id&amount_min_ct&amount_max_ct&match_level&source&is_revenue&cursor` — Tra cứu giao dịch · Quyền: supervisor_aml, ops_read, inspector_read

**Response `200`:** `items[]`: `{ credit_event_id, ref_id, merchant: {code, shop_name, market_name}, amount_ct, currency, booked_at, received_at, payer: {name, msisdn_masked, bank_code}, account_no_masked, source, replayed, match: {level, target_type, target_label}, is_revenue, receipt_sent, case_code, notify: {t0t1_ms, channel} }`.

<a id="muc-e-12-2-get-admin-transactions-crediteventid-truy-vet-1-gd-tr"></a>
#### E.12.2 · `GET /admin/transactions/{credit_event_id}` — Truy vết 1 GD trọn chuỗi (AC-6.3) · Quyền: như E.12.1

**Response `200`:** bản ghi đầy đủ như E.12.1 + `timeline[]` — chuỗi sự kiện trong 1 màn:

| Trường timeline | Kiểu | Mô tả |
|---|---|---|
| `at` | RFC3339 | — |
| `stage` | enum | `booked` (bank ghi Có) · `received` (M4/M3poll vào module Ingest của Commerce) · `deduped` · `matched` (kèm level/target) · `notified` (push/SMS + t0t1_ms) · `receipt_created` · `case_opened` · `case_concluded` · `adjusted` |
| `detail` | object | Dữ liệu stage (vd `{level:"LINK", bill_code:"B-1007-17"}`) |
| `trace_id` | string | Nối OpenTelemetry |

Tra theo RefID: dùng E.12.1 `?ref_id=` rồi mở chi tiết.

<a id="muc-e-12-3-post-admin-cases-mo-case-tu-portal-hotline-quyen-supe"></a>
#### E.12.3 · `POST /admin/cases` — Mở case từ portal/hotline · Quyền: supervisor_aml

**Request:**

| Trường | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `ref_id` HOẶC `credit_event_id` | string / uuid | **Có** (một trong hai) | Case bám RefID (Q6) |
| `merchant_id` | uuid | **Có** | — |
| `type` | enum | **Có** | `wrong_amount` · `not_received` · `duplicate` · `fraud_suspect` · `other` |
| `description` | string ≤1000 | **Có** | — |
| `source` | enum | **Có** | `portal` · `hotline` · (case từ app tự mang `merchant_app`) |

**Response `201`:** `{ case_id, case_code, status: "open", sla: {first_response_due_at, close_due_at} }` — phát `case.opened`.

**Lỗi riêng:** `PIN-409-STATE` ref_id đã có case mở (`details.case_code`) · `PIN-404-NF` ref/credit không tồn tại.

<a id="muc-e-12-4-get-admin-cases-status-type-overdue-assignedto-cursor"></a>
#### E.12.4 · `GET /admin/cases?status&type&overdue&assigned_to&cursor` — Hàng đợi case (US-32) · Quyền: supervisor_aml (đọc: inspector_read)

**Response `200`:** `items[]`: `{ case_id, case_code, ref_id, merchant: {code, shop_name}, type, status: "open"|"awaiting_merchant"|"investigating"|"concluded_refund"|"concluded_reject"|"closed", opened_at, sla_due_at, overdue: bool, refund_verified: bool, assigned_to, evidence_count, last_action_at }` + `summary: {open, overdue}` — quá SLA nổi đỏ BRH-02 + email nhắc (AC-7.2).

<a id="muc-e-12-5-post-admin-cases-id-evidence-dinh-chung-cu-2-phia-quy"></a>
#### E.12.5 · `POST /admin/cases/{id}/evidence` — Đính chứng cứ 2 phía · Quyền: supervisor_aml

**Request:** `{ "kind": "screenshot"|"bank_statement"|"document"|"other", "object_key" (từ POST /media purpose=evidence), "side": "merchant"|"buyer"|"brh", "note"? ≤300 }` — `side` là BÊN của GIAO DỊCH: buyer = bên TRẢ, merchant = bên NHẬN (không phải vai app). → **Response `201`:** `{ "evidence_id", "uploaded_by", "at" }`.

**Lỗi riêng:** `PIN-409-STATE` case đã `closed/concluded_*` · `PIN-404-NF` object_key.

<a id="muc-e-12-6-post-admin-cases-id-conclude-ket-luan-case-kem-xac-mi"></a>
#### E.12.6 · `POST /admin/cases/{id}/conclude` — Kết luận case (kèm XÁC MINH hoàn — AC-7.1) · Quyền: supervisor_aml

**Request:**

| Trường | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `verdict` | enum | **Có** | `refund` \| `reject` |
| `reason` | string ≤1000 | **Có** | Mọi quyết định bắt buộc lý do |
| `refund_verify` | object | khi `refund`: **Có** | Bằng chứng merchant ĐÃ chuyển trả |
| `refund_verify.method` | enum | **Có** | `m3` (server đọc lịch sử M3 qua token, tìm bút toán `debit` khớp `amount_ct` + người nhận trong ±3 ngày) \| `document` (cán bộ đính chứng từ) |
| `refund_verify.amount_ct` | int64 | **Có** | Số tiền hoàn |
| `refund_verify.txn_id` | string | method=m3: Không (server tự dò nếu thiếu) | Bút toán bank |
| `refund_verify.evidence_key` | string | method=document: **Có** | Chứng từ |

**Response `200`:** `{ "case_id", "status": "concluded_refund"|"concluded_reject", "refund_verified": true|false, "adjustment_id" (nullable — bút toán điều chỉnh NHÁP, vào luồng 4 mắt duy nhất draft→approved→posted của **Back-office**), "concluded_at" }` — side-effect: `case.concluded` (cờ refund dùng nội bộ Compliance — module Đối soát loại khỏi doanh thu bán mới), trạng thái «Đã hoàn» hiện ngược ở NB-09.

**Lỗi riêng:** `BIZ-REFUND-UNVERIFIED` verdict=refund nhưng method=m3 KHÔNG tìm thấy bút toán khớp và không có chứng từ (hệ thống CHẶN — không thể «Đã hoàn» tay không) · `BIZ-REASON-REQUIRED` · `PIN-409-STATE` case đã kết luận.

<a id="muc-e-12-7-get-admin-aml-alerts-status-source-rulecode-merchanti"></a>
#### E.12.7 · `GET /admin/aml-alerts?status&source&rule_code&merchant_id&cursor` — Hàng đợi cảnh báo AML (US-33) · Quyền: supervisor_aml (đọc: inspector_read)

**Response `200`:** `items[]`:

| Trường | Kiểu | Mô tả |
|---|---|---|
| `alert_id` | uuid | — |
| `merchant` | object | `{id, code, shop_name, market_name}` — bối cảnh |
| `source` | enum | `e2` (danh sách) · `rule` (ngưỡng C14) · `limit` (hậu kiểm hạn mức ngày) |
| `rule_code` | string | `AML_TX_FLAG` (≥10.000.000 ct/GD) · `AML_DAY_FLAG` (≥50.000.000 ct/ngày — AC-8.1, kèm gắn cờ hạn chế) · `AML_SMURF` (≥5 GD ∈ 80–100% ngưỡng/24h — AC-8.2) |
| `context` | object | `{day_total_ct?, txn_count?, txn_ids?[], lists?[], merchant_flag: bool}` |
| `status` | enum | `open` · `awaiting_reply` · `investigating` · `dismissed` · `escalated` |
| `created_at` / `decided_at` / `decided_by` / `reason` | — | — |

<a id="muc-e-12-8-post-admin-aml-alerts-id-decide-quyet-dinh-aml-us-34"></a>
#### E.12.8 · `POST /admin/aml-alerts/{id}/decide` — Quyết định AML (US-34, AC-8.3) · Quyền: supervisor_aml

**Request:** `{ "decision": "dismiss"|"request_info"|"suspend_merchant"|"escalate", "reason" — BẮT BUỘC ≤1000 }` → **Response `200`:** `{ "alert_id", "status", "decided_at" }` — `dismiss` alert nguồn `limit` → bỏ cờ hạn chế; `suspend_merchant` → như E.11.6 (ghi cùng reason); audit đầy đủ.

**Lỗi riêng:** `BIZ-REASON-REQUIRED` thiếu lý do (hệ thống TỪ CHỐI lưu) · `PIN-409-STATE` alert đã đóng.

<a id="muc-e-12-9-get-admin-cases-id-chi-tiet-case-ho-so-chung-cu-dong"></a>
#### E.12.9 · `GET /admin/cases/{id}` — Chi tiết case: hồ sơ + chứng cứ + dòng thời gian (BRH-06) · Quyền: supervisor_aml (đọc: inspector_read)

**Response `200`:** bản ghi đầy đủ như item E.12.4 + `evidence[]`: `{ id, side: "merchant"|"buyer"|"brh", type ("screenshot"|"bank_statement"|"document"|"other"), key (object_key MinIO — mở qua presigned URL có TTL), note, uploaded_by, at }` + `timeline[]` hành động: `{ at, action ("opened"|"assigned"|"request_info"|"evidence_added"|"concluded"|"closed"), by, detail }` — đủ tái hiện luồng xử lý E.12.3 → E.15.3 → E.12.5 → E.12.6.

**Lỗi riêng:** `PIN-404-NF` case không tồn tại / không thuộc quyền nhìn.

<a id="muc-e-13-portal-brh-bao-cao-audit-nguoi-dung-man-brh-08-11-12-th"></a>
### E.13. Portal BRH — báo cáo, audit, người dùng (màn BRH-08/11/12) + tham số qua API (không màn — BRH-09 bỏ 04/08)

<a id="muc-e-13-1-get-admin-reports-kpi-range-day-week-month-from-to-ci"></a>
#### E.13.1 · `GET /admin/reports/kpi?range=day|week|month&from&to&city&market_id&format=json|csv|pdf` — KPI pilot (US-29) · Quyền: mọi vai trò portal

**Response `200` (json):**

| Trường | Kiểu | Mô tả |
|---|---|---|
| `kpis.merchants_activated` | int | Mục tiêu 601 |
| `kpis.weekly_active_pct` | number | ≥1 GD/tuần trên merchant kích hoạt (mục tiêu ≥50%) |
| `kpis.avg_txn_per_merchant_week` | number | Mục tiêu ≥3 |
| `kpis.onboarding` | object | `{started, submitted, activated, median_minutes (mục tiêu <10), review_sla_hit_pct («v3.6»: SLA hậu kiểm hồ sơ cờ ≤24h)}` |
| `kpis.notify_p95_ms` | int | T0→T1 (mục tiêu ≤5000) |
| `kpis.match_auto_rate` | number | KPI ≥0.95 — công thức TSD §6 (loại STRAY/PENDING khỏi mẫu số, loại non-revenue cả hai) |
| `kpis.uptime_pct` | number | 99,5% synthetic |
| `kpis.cases` | object | `{open, overdue, avg_close_days}` |
| `kpis.discrepancies` | object | `{open, closed_in_sla_pct}` |
| `by_market[]` | array | Từng chỉ số theo chợ/TP |
| `settled_through` | date | Chốt theo ngày đối soát |

`format=csv|pdf` → file stream (job email lịch C15 dùng chung generator). **Lỗi riêng:** `PIN-400-VAL` range quá 12 tháng.

<a id="muc-e-13-2-get-admin-params-danh-sach-tham-so-13-3-quyen-admin-d"></a>
#### E.13.2 · `GET /admin/params` — Danh sách tham số (§13.3) · Quyền: admin (đọc: mọi vai trò)

**Response `200`:** `items[]`: `{ key ("QR_DYNAMIC_TTL"...), value (JSON), value_pending (JSON \| null), effective_from, status: "active"|"pending_approval", maker, checker, updated_at, description }`.

<a id="muc-e-13-3-put-admin-params-key-de-xuat-thay-doi-maker-quyen-adm"></a>
#### E.13.3 · `PUT /admin/params/{key}` — Đề xuất thay đổi (maker) · Quyền: admin

**Request:** `{ "value": {...} | scalar, "effective_from": "2026-11-01", "reason" — BẮT BUỘC }` → **Response `202`:** `{ "key", "status": "pending_approval", "maker": "a@brh.ht" }` — CHƯA hiệu lực.

**Lỗi riêng:** `PIN-400-VAL` value sai kiểu/khoảng cho key (schema per-key: số dương, enum...) · `PIN-409-STATE` key đang có đề xuất chờ duyệt · `BIZ-REASON-REQUIRED` · `PIN-404-NF` key lạ.

<a id="muc-e-13-4-post-admin-params-key-approve-phe-duyet-4-mat-checker"></a>
#### E.13.4 · `POST /admin/params/{key}/approve` — Phê duyệt 4 mắt (checker) · Quyền: admin (khác người đề xuất)

**Request:** `{ "decision": "approve"|"reject", "reason"? (reject: BẮT BUỘC) }` → **Response `200`:** `{ "key", "status": "active"|"rejected", "effective_from" }` — approve: ghi `param` + phát `param.changed` (cache-bust mọi service).

**Lỗi riêng:** `BIZ-FOUR-EYES` checker trùng maker (AC-6.2 — hệ thống chặn) · `PIN-409-STATE` không có đề xuất chờ · `BIZ-REASON-REQUIRED` reject thiếu lý do.

<a id="muc-e-13-5-get-admin-audit-actor-action-target-from-to-cursor-nh"></a>
#### E.13.5 · `GET /admin/audit?actor&action&target&from&to&cursor` — Nhật ký bất biến (US-31) · Quyền: inspector_read, admin (đọc)

**Response `200`:** `items[]`: `{ seq (BIGSERIAL — thứ tự chuỗi hash), at, actor: {id, email, role}, action ("application.approve", "param.change", "case.conclude"...), target ("merchant:PIN-M-000241"), payload (JSON đã che PII theo vai trò), chain: {hash_prefix, verified: true} }` — job `audit-verify` hằng đêm kiểm chuỗi (AC-6.5); xuất bằng chứng: `?format=csv` + chữ ký số file.

<a id="muc-e-13-6-get-admin-users-role-status-cursor-nguoi-dung-portal"></a>
#### E.13.6 · `GET /admin/users?role&status&cursor` — Người dùng portal · Quyền: admin

**Response `200`:** `items[]`: `{ user_id, email, role: "admin"|"approver"|"supervisor_aml"|"ops_read"|"inspector_read", org: "BRH"|"VDS"|"Natcom", status: "invited"|"active"|"disabled", totp_enabled, last_login_at, created_at }`.

<a id="muc-e-13-7-post-admin-users-tao-nguoi-dung-quyen-admin"></a>
#### E.13.7 · `POST /admin/users` — Tạo người dùng · Quyền: admin

**Request:** `{ "email", "role", "org" }` → **Response `201`:** `{ "user_id", "status": "invited" }` — email mời đặt mật khẩu + enroll TOTP (link 24h). Nhắc RBAC: admin KHÔNG xem dữ liệu GD; không vai trò nào vừa tạo vừa duyệt.

**Lỗi riêng:** `PIN-409-STATE` email đã tồn tại · `PIN-400-VAL` role/org ngoài danh mục.

<a id="muc-e-13-8-patch-admin-users-id-sua-khoa-reset-2fa-quyen-admin"></a>
#### E.13.8 · `PATCH /admin/users/{id}` — Sửa/khóa/reset 2FA · Quyền: admin

**Request:** `{ "role"?, "status"?: "active"|"disabled", "reset_totp"?: true }` → **Response `200`:** bản ghi mới; `disabled` → thu hồi phiên ngay.

**Lỗi riêng:** `PIN-409-STATE` tự khóa/tự hạ quyền chính mình · `PIN-404-NF`.

<a id="muc-e-13-9-post-admin-adjustments-id-approve-post-admin-adjustme"></a>
#### E.13.9 · `POST /admin/adjustments/{id}/approve` · `POST /admin/adjustments/{id}/reject` — Duyệt/từ chối bút toán điều chỉnh (luồng 4 mắt duy nhất `draft→approved→posted`) · Quyền: approver (người duyệt PHẢI khác người tạo nháp — AC-6.2)

Nháp sinh từ E.12.6 (kết luận case) hoặc E.14.7 (`action=adjust`); duyệt xong hệ thống TỰ ghi sổ (không có bước post tay).

**Request (approve):** `{ "note"? ≤500 }` → **Response `200`:** `{ "adjustment_id", "status": "posted", "checker", "posted_at" }` — chuỗi `draft→approved→posted` chạy trong MỘT giao dịch; cập nhật doanh số merchant + audit ghi vết.

**Request (reject):** `{ "reason" — BẮT BUỘC ≤1000 }` → **Response `200`:** `{ "adjustment_id", "status": "rejected", "rejected_by", "rejected_at" }` — nháp hủy hiệu lực, KHÔNG ghi sổ (muốn điều chỉnh lại: tạo nháp mới từ E.12.6/E.14.7); `rejected` là trạng thái API trả về (như E.13.4), lý do giữ vết audit — danh mục `adjustment.status` DB không đổi.

**Lỗi riêng:** `BIZ-FOUR-EYES` người duyệt trùng `maker` (hệ thống chặn) · `BIZ-REASON-REQUIRED` reject thiếu lý do · `PIN-409-STATE` không ở `draft` · `PIN-404-NF`.

<a id="muc-e-14-console-van-hanh-vds-man-aq-00-01-03-04"></a>
### E.14. Console vận hành VDS (màn AQ-00/01/03/04)

<a id="muc-e-14-1-get-ops-connections-suc-khoe-ket-noi-doi-tac-us-35-qu"></a>
#### E.14.1 · `GET /ops/connections` — Sức khỏe kết nối đối tác (US-35) · Quyền: ops_read+

**Response `200`:** `items[]` (mỗi đối tác/connector):

| Trường | Kiểu | Mô tả |
|---|---|---|
| `partner` | enum | `ob_wallet2` · `ob_bank2` · `brh_e1` · `brh_e2` · `switch_e3` · `natcom_n1` |
| `status` | enum | `up` · `degraded` · `down` |
| `circuit` | object | `{state: "closed"\|"open"\|"half_open", opened_at?}` — mở khi 50% lỗi/20 req |
| `latency_p95_ms` / `error_rate_15m` | int / number | Ngưỡng cảnh báo C12 (webhook lỗi >1%/15’, E1 >5%...) |
| `last_ok_at` / `last_error` | RFC3339 / object | `{code, at}` |
| `webhook_gap_min` | int \| null | Riêng OB: phút không có M4 khi có GD kỳ vọng (>10’ giờ chợ → alert + tự M3-poll) |

<a id="muc-e-14-2-get-ops-tokens-status-expiring-revoked-active-days-7"></a>
#### E.14.2 · `GET /ops/tokens?status=expiring|revoked|active&days=7&cursor` — Kho token sắp hết hạn · Quyền: ops_read+

**Response `200`:** `items[]`: `{ link_id, ext_link_id, merchant_code, bank_code, account_no_masked, token_status, expires_at, days_left, refresh_expires_at, last_renew_at, renew_fail_count, last_renew_error }` + `summary: {expiring_7d}` (>20 → chiến dịch nhắc).

<a id="muc-e-14-4-get-ops-health-suc-khoe-noi-bo-mms-quyen-opsread"></a>
#### E.14.4 · `GET /ops/health` — Sức khỏe nội bộ MMS · Quyền: ops_read+

**Response `200`:** `{ services: [{name (4 dịch vụ + bff + connectors), status, replicas_ready: "2/2"}], bus: { lag_max, dlq: [{topic: "credit.received.dlq", count}] }, db: {status, replication_lag_s}, redis: {status}, minio: {status}, synthetic: { journeys: [{name ("login","qr","credit_notify","sync","report"), ok, last_run_at, p95_ms}] } }` — 5 hành trình vàng fail ≥1 → tính downtime 99,5%.

<a id="muc-e-14-5-get-ops-recon-runs-bizdate-status-cursor-cac-phien-do"></a>
#### E.14.5 · `GET /ops/recon-runs?biz_date&status&cursor` — Các phiên đối soát (AQ-03) · Quyền: ops_read+

**Response `200`:** `items[]`: `{ run_id, biz_date, session_no, status: "ingesting"|"matched"|"discrepancy"|"closed", source: "push"|"pull"|"sftp", e3_file_key, checksum_verified, total_e3, total_matched, total_onus_skipped (bản ghi on-us MMS có nhưng E3 không — bỏ qua theo thiết kế), discrepancies: {open, closed}, started_at, closed_at }`.

<a id="muc-e-14-6-get-ops-discrepancies-status-dtype-runid-overdue-curs"></a>
#### E.14.6 · `GET /ops/discrepancies?status&dtype&run_id&overdue&cursor` — Hàng đợi chênh lệch (AQ-04, US-36) · Quyền: ops_read+

**Response `200`:** `items[]`:

| Trường | Kiểu | Mô tả |
|---|---|---|
| `discrepancy_id` / `run_id` / `biz_date` / `session_no` | — | — |
| `dtype` | enum | `missing_in_mms` (Switch có – MMS không thấy) · `missing_in_e3` (MMS có ref_id – E3 không) · `amount_diff` |
| `ref_id` | string \| null | — |
| `account_no_masked` / `merchant_code` | string \| null | Map được thì kèm |
| `amount_e3_ct` / `amount_mms_ct` | int64 \| null | So lệch |
| `status` | enum | `open` · `polling` · `adjusting` · `case` · `closed` |
| `sla_due_at` / `overdue` | RFC3339 / bool | `DISCREPANCY_SLA` 2 ngày làm việc |
| `resolution` | object \| null | `{action, note, by, at}` — vết đầy đủ nguyên nhân → hành động (AC-9.2) |

<a id="muc-e-14-7-post-ops-discrepancies-id-resolve-xu-ly-mot-khoan-lec"></a>
#### E.14.7 · `POST /ops/discrepancies/{id}/resolve` — Xử lý một khoản lệch · Quyền: ops ghi

**Request:**

| Trường | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `action` | enum | **Có** | `poll_m3` (tự tạo yêu cầu M3-poll qua C.6 theo link/khoảng) · `adjust` (tạo NHÁP bút toán — vào luồng duyệt 4 mắt draft→approved→posted của **Back-office**) · `to_case` (mở case điều tra) · `dismiss` (giải trình được — vd on-us/refund flag) |
| `note` | string ≤1000 | **Có** | Nguyên nhân → hành động (vết AC-9.2) |
| `adjustment` | object | action=adjust: **Có** | `{merchant_id, amount_ct, direction: "debit"\|"credit", original_ref_id}` — mẫu bút toán đảo có tham chiếu gốc (C19) |

Với `action=poll_m3`: server TỰ SUY `{link_id, from, to}` = map `discrepancy.account_no` → `account_link` (qua `account_no_enc`) + khoảng thời gian phiên của `recon_run` chứa khoản lệch — không cần nhập tay (v1.1).

**Response `200`:** `{ "discrepancy_id", "status": "polling"|"adjusting"|"case"|"closed", "next": { "poll_id"? | "adjustment_id" (status=draft)? | "case_code"? } }`

**Lỗi riêng:** `BIZ-REASON-REQUIRED` thiếu note · `PIN-409-STATE` đã closed/đang action khác · `PIN-400-VAL` adjustment thiếu trường.

<a id="muc-e-15-portal-brh-dashboard-tong-quan-bo-khuyet-portal-man-brh"></a>
### E.15. Portal BRH — dashboard tổng quan & bổ khuyết portal (màn BRH-02 · bổ sung BRH-04/06/08)

<a id="muc-e-15-1-get-admin-dashboard-city-marketid-bang-dieu-khien-ton"></a>
#### E.15.1 · `GET /admin/dashboard?city&market_id` — Bảng điều khiển tổng quan (BRH-02, US-27) · Quyền: mọi vai trò portal (đọc — chỉ số liệu TỔNG HỢP; drill-down mở màn đích theo RBAC của màn đó)

Một call trả đủ widget BRH-02. Server cache 30s, client refresh 60s; mọi con số là aggregate — admin xem được (nguyên tắc «admin không xem dữ liệu GD» chỉ áp cho chi tiết từng GD ở E.12.1).

**Request (query):**

| Trường | Kiểu | Bắt buộc | Mô tả | Ví dụ |
|---|---|---|---|---|
| `city` | string | Không | Lọc theo TP (3 TP pilot) | `"Port-au-Prince"` |
| `market_id` | uuid | Không | Lọc theo chợ (9 chợ) — bỏ trống = toàn pilot | — |

**Response `200`:**

| Trường | Kiểu | Mô tả |
|---|---|---|
| `as_of` | RFC3339 | Thời điểm chốt số (cache 30s) |
| `merchants` | object | `{active, suspended, pending_review, activated_today}` — tiến độ so mục tiêu 601 |
| `today` | object | `{txn_count, txn_amount_ct (int64, centime), receipt_auto_pct, notify_p95_ms}` — theo `biz_date` giờ Haiti |
| `onboarding` | object | `{queue_pending, overdue_sla, median_minutes}` — `overdue_sla` (quá 24h hậu kiểm «v3.6», US-26) nổi đỏ, click → BRH-03 |
| `cases` | object | `{open, overdue}` — quá SLA nổi đỏ (AC-7.2), click → BRH-06 (E.12.4) |
| `aml` | object | `{alerts_open, escalated}` — click → BRH-07 (E.12.7) |
| `recon` | object | `{last_run: {biz_date, session_no, status}, discrepancies_open, discrepancies_overdue}` — nguồn E.14.5/E.14.6 |
| `connections[]` | array | Rút gọn E.14.1: `{partner, status: "up"\|"degraded"\|"down"}` — chỉ trạng thái, không số kỹ thuật |
| `tokens_expiring_7d` | int | >20 → cảnh báo vàng (chiến dịch nhắc gia hạn — E.14.2) |
| `alerts[]` | array | Feed cảnh báo đang mở: `{severity: "red"\|"yellow", kind: "case_sla"\|"aml"\|"webhook_gap"\|"recon_late"\|"token_expiring"\|"onboarding_sla", count, link}` |

**Lỗi riêng:** không có — chỉ lỗi chung A.4 (`PIN-400-VAL` khi `city`/`market_id` ngoài danh mục).

<a id="muc-e-15-2-get-admin-merchants-id-activity-types-from-to-cursor"></a>
#### E.15.2 · `GET /admin/merchants/{id}/activity?types&from&to&cursor` — Dòng thời gian hoạt động 1 merchant (BRH-04 tab «Hoạt động») · Quyền: approver, supervisor_aml, inspector_read (đầy đủ) · ops_read (chỉ `link/standee/system`) · admin (chỉ `application/admin` — KHÔNG sự kiện GD, nhất quán E.13.7)

Hợp nhất mọi sự kiện quanh MỘT merchant thành một dòng thời gian — bổ trợ E.12.2 (vốn truy theo một GD): kích hoạt/hậu kiểm hồ sơ, liên kết/token, standee, tổng tiền về theo ngày, case, AML, thao tác quản trị.

**Request (query):**

| Trường | Kiểu | Bắt buộc | Mô tả | Ví dụ |
|---|---|---|---|---|
| `types` | csv enum | Không | `application` · `link` · `standee` · `credit_summary` · `case` · `aml` · `admin` · `system` — bỏ trống = mọi loại trong quyền | `"case,aml"` |
| `from` / `to` | RFC3339 | Không | Mặc định 30 ngày gần nhất; tối đa 12 tháng | — |
| `cursor` | string | Không | Phân trang A.5 | — |

**Response `200`:** `items[]`:

| Trường | Kiểu | Mô tả |
|---|---|---|
| `at` | RFC3339 | — |
| `type` | enum | Như `types` |
| `title` | string | Bản địa hóa («Hồ sơ đã kết luận hậu kiểm», «Token bị thu hồi», «Mở case»…) |
| `detail` | object | Payload theo type; `credit_summary` CHỈ là tổng ngày `{biz_date, txn_count, total_ct}` — chi tiết từng GD phải qua E.12.1 (đúng RBAC) |
| `actor` | object \| null | `{kind: "system"\|"merchant"\|"portal", label}` — email portal che theo vai trò người xem |
| `ref` | object \| null | `{kind: "application"\|"case"\|"alert"\|"credit_event"\|"link", id, code}` — deep-link mở màn tương ứng |

**Lỗi riêng:** `PIN-404-NF` merchant không tồn tại · `PIN-400-VAL` khoảng >12 tháng / `types` ngoài danh mục.

<a id="muc-e-15-3-post-admin-cases-id-request-info-yeu-cau-bo-sung-thon"></a>
#### E.15.3 · `POST /admin/cases/{id}/request-info` — Yêu cầu bổ sung thông tin case (BRH-06, US-32) · Quyền: supervisor_aml

Gửi yêu cầu tới merchant qua app + SMS; case chuyển `awaiting_merchant`. Đồng hồ SLA close VẪN CHẠY (chỉ dừng khi kết luận E.12.6) — tránh treo case bằng cách «hỏi thêm».

**Request:**

| Trường | Kiểu | Bắt buộc | Mô tả | Ví dụ |
|---|---|---|---|---|
| `to` | enum | **Có** | `merchant` | `"merchant"` |
| `needed` | array enum ≥1 | **Có** | `photo` · `bank_statement` · `description` · `other` | `["photo"]` |
| `message` | string ≤500 | **Có** | Nội dung hiển thị trong app (cán bộ soạn, fr/ht) | — |
| `due_hours` | int 1..168 | Không (mặc định 48) | Hạn phản hồi — quá hạn nổi nhắc tại BRH-06 | `48` |

**Response `200`:** `{ "case_id", "status": "awaiting_merchant", "requested_at", "due_at" }` — app hiện mục «Cần bạn bổ sung» ở NB-09 + notification; phản hồi của người dùng vào case dưới dạng evidence (E.12.5, `side` tương ứng); audit ghi vết.

**Lỗi riêng:** `PIN-409-STATE` case đã `concluded_*`/`closed` · `PIN-400-VAL` `needed` rỗng / thiếu `message` · `PIN-404-NF` case.

---

<a id="muc-e-16-thanh-toan-trong-app-dung-chung-moi-vai-man-nm-0105-luo"></a>
### E.16. Thanh toán trong app — DÙNG CHUNG MỌI VAI (màn NM-01→05 · luồng S9) «v3.5»

> «v3.5» (họp BRH 20/08): MỘT app — sau đăng ký CHỌN VAI (màn CH-00); NGƯỜI BÁN CŨNG THANH TOÁN ĐƯỢC → nhóm E.16 áp dụng MỌI người dùng đã đăng nhập — nhãn quyền: **`user`** (cả hai vai); khác biệt vai chỉ ở nhóm menu quản lý bán hàng. Nút «Trở thành người bán» (trong hồ sơ) — **HOÃN SAU PILOT (user chốt 20/08)**; khi làm sẽ CHỈ bổ sung phần vai bán còn thiếu, KHÔNG lặp lại bước đã làm: ① eKYC bậc 2 nếu chưa có (E.2.x — khung KYC BRH: bán = KYC2) ② hồ sơ gian hàng ③ liên kết TK NHẬN (khác scope TK nguồn trả) → kích hoạt tự động (C10 «v3.6» — tạo là active, hậu kiểm sau); trong PILOT: vai chọn MỘT lần ở CH-00 (đặt NGAY SAU OTP+PIN, TRƯỚC eKYC — «v3.6»: vai mua không chạy E1/E2), đổi vai qua kênh hỗ trợ/field agent; `GET /me` (E.10.4) trả trạng thái merchant để app dựng menu. Đăng ký/OTP/PIN/khóa khẩn DÙNG LẠI E.1.x (person, `kyc_level=1`); liên kết TK nguồn trả DÙNG LẠI E.3.x với `holder=person` + scope `payment`. QR parse OFFLINE phía app (A9) — server chỉ nhận kết quả parse.

<a id="muc-e-16-1-post-payments-quet-qr-tra-us-41-quyen-user"></a>
#### E.16.1 · `POST /payments` — Quét QR → trả (US-41) · Quyền: user

**Request:** `{ "client_uuid" (idempotent), "funding_link_id", "target": { "operator", "account", "merchant_hint" | null }, "amount_ct" (QR động: từ tag 54, khóa không sửa; QR tĩnh: người mua nhập), "currency", "bill_code" | null }` → **Response `201`:** `{ "payment_id", "status": "created", "expires_at" (+`PAY_CREATE_TTL` 15′), "merchant": { "merchant_id" | null, "shop_name", "mcc", "city", "verified": true|false } }` — server resolve đích để app hiện **TÊN người bán** trước khi xác nhận (chốt chống dán đè, AC-11.1); người mua bấm xác nhận → server gọi C.7.

**Thuật toán resolve «Peye-Haiti 15/08»:** ① tag 38-01 (9332xx) → `bank_code` qua danh mục `OPERATOR_DIRECTORY` (param §13.3 TSD, seed cùng D1) → ② tra `account_link` theo (`bank_code`, `account_no_hmac` = HMAC nội bộ của số TK trong QR, index partial status active·grace) → ③ có dòng → merchant của dòng đó: trả `shop_name` từ danh bạ (nguồn sự thật) + `verified:true`; merchant `suspended` → kèm cảnh báo như P.1. **Không tìm thấy** (TK ngoài Peye-Haiti) → `merchant_id:null, verified:false`, `shop_name` = tag 59 của QR kèm nhãn «chưa xác thực» — app buộc hiển thị cảnh báo trước khi cho xác nhận. **Chống chẻ nhỏ lệnh «v3.5» (L3):** tổng CÙNG-ĐÍCH đã trả trong ngày + lệnh mới > `PAY_SCA_THRESHOLD` → lệnh bị đẩy lên BẬC OTP dù món ≤ ngưỡng (MMS đặt `sca_hint:"required"` ở C.7 — định chế PHẢI thách OTP). Số TK đích ĐẦY ĐỦ giữ tạm trong Redis (`pay:{payment_id}:target`, TTL = `PAY_CREATE_TTL`, xóa ngay sau C.7 trả 202) — KHÔNG ghi PostgreSQL/log, giữ đúng «không ghi đĩa».

**Hai bậc xác thực «v3.5» (họp BRH 20/08 — thay trần cứng 5.000/GD):** KHÔNG còn trần giá trị/giao dịch phía nền tảng — hạn mức giá trị do ĐỊNH CHẾ tự áp theo mức KYC (`failed`/`limit`) + AML hậu kiểm. `amount_ct` ≤ **`PAY_SCA_THRESHOLD` = 500.000 ct (5.000 HTG)**: chỉ PIN app; **> ngưỡng: PIN app + SMS OTP của ĐỊNH CHẾ** (C.7 trả `sca_required` → nhập OTP tại E.16.6). **Hạn mức ngày `PAY_DAY_MAX`** (2.500.000 ct và ≤20 lệnh/người/ngày; «ngày» = `biz_date` giờ Haiti) **CHỈ đếm lệnh bậc-PIN** (≤ ngưỡng; đếm cả `failed`/`timeout`, không đếm `created` chưa confirm/`expired`; lệnh có OTP KHÔNG tính — đã có yếu tố thứ hai của định chế + hạn mức định chế) — vượt → `PIN-422-BIZ`/`details.issue="daily_limit"` (app chặn trước bằng cùng tham số).

**Sóng yếu:** request đứt → app retry CÙNG `client_uuid` (an toàn tuyệt đối); KHÔNG bao giờ sinh client_uuid mới cho cùng một lần quét.

**Lỗi riêng:** `BIZ-DUP-CLIENT-UUID` trùng `client_uuid` khác payload (trùng + giống → `200` payment cũ) · `PIN-409-STATE` kèm `details.pending_payment_id` — cùng person còn lệnh `submitted`/`sca_required`/`timeout` chưa chốt tới CÙNG đích (operator + account_no_hmac + amount_ct): chặn trả-đúp (kể cả lệnh đang chờ OTP «v3.5»), app hiện lệnh đang treo · `BIZ-TOKEN-REVOKED` consent nguồn trả hết hạn → CTA liên kết lại.

<a id="muc-e-16-2-post-payments-id-confirm-xac-nhan-tra-sau-khi-thay-te"></a>
#### E.16.2 · `POST /payments/{id}/confirm` — Xác nhận trả sau khi thấy tên (1 chạm) · Quyền: user

`{ "pin" }` (PIN của app Peye-Haiti — PIN riêng của nền tảng, lưu băm `person.pin_hash`, KHÔNG phải PIN ví/ngân hàng) → `202 { "status": "submitted" }`; hoặc, lệnh > `PAY_SCA_THRESHOLD` («v3.5»): `202 { "status": "sca_required", "sca": { "msisdn_masked", "expires_at", "attempts_left" } }` → màn NM-03 chuyển TRẠNG THÁI NHẬP OTP (không thêm màn) → nộp qua E.16.6; kết quả cuối đẩy notification (topic `payment.finished`) + poll E.16.3 (P95 ≤3s — `PAY_CONFIRM_SLA`; nhánh OTP: đồng hồ tính LẠI từ lúc nộp OTP E.16.6 — thời gian người dùng gõ OTP không tính). **Đứt mạng SAU confirm:** khi online lại app poll E.16.3 — trạng thái cuối thì hiển thị kết quả; `sca_required` còn hạn thì mở lại trạng thái nhập OTP (E.16.3 kèm object `sca`); tuyệt đối không tạo payment mới.

**Lỗi riêng:** `PIN-401-AUTH` sai PIN (kèm `details.attempts_left`; 5 lần → khóa 60′ như C2) · `PIN-409-STATE` payment không ở `created` hoặc đã quá `PAY_CREATE_TTL` (quét lại từ đầu) · `BIZ-TOKEN-REVOKED` consent bị thu hồi giữa chừng · `PIN-503-DEP` định chế trả down (circuit breaker C.7 — payment giữ `created`, bấm lại được).

<a id="muc-e-16-3-get-payments-id-trang-thai-bien-lai-so-us-43-quyen-us"></a>
#### E.16.3 · `GET /payments/{id}` — Trạng thái/biên lai số (US-43) · Quyền: user

Response: `{ "payment_id", "status", "failure_reason", "merchant": {...}, "amount_ct", "ref_id", "finished_at", "receipt": { "no", "issued_at" } | null, "dispute": { "case_code", "status" } | null, "sca": { "msisdn_masked", "expires_at", "attempts_left" } | null }` — `dispute`: hiện diện khi khoản có khiếu nại (E.16.5, đọc qua `case.payment_id`) để người dùng THEO DÕI ĐƯỢC trạng thái (AC-11.5); `sca` («v3.5»): chỉ khi `status:"sca_required"` — phục vụ resume nhập OTP sau đứt mạng — `no` = dẫn xuất (`ref_id`; on-us: `payment_id` rút gọn), `issued_at = finished_at`; không cột riêng.

<a id="muc-e-16-4-get-payments-from-to-cursor-lich-su-tra-nm-04-quyen-u"></a>
#### E.16.4 · `GET /payments?from&to&cursor` — Lịch sử trả (NM-04) · Quyền: user

Phân trang cursor như A.5; response: `{ "items": [ phần tử rút gọn của E.16.3 — payment_id, status, failure_reason, merchant.shop_name, amount_ct, finished_at ], "next_cursor" }` — chỉ trả lệnh của chính person trong JWT (lọc `person_id`, chống dò `PIN-404-NF` như quy ước A.4).

<a id="muc-e-16-5-post-payments-id-dispute-khieu-nai-khoan-da-tra-us-45"></a>
#### E.16.5 · `POST /payments/{id}/dispute` — Khiếu nại khoản đã trả (US-45) · Quyền: user

`{ "reason" ≤280 }` → `201 { "case_id", "case_code" }` — người mua theo dõi tiếp qua trường `dispute` của E.16.3 + notification khi case chốt («v3.4», AC-11.5); sinh `case` nguồn `buyer_app` với `case.payment_id` (quy tắc «một trong ref_id/credit_event_id/payment_id»; `merchant_id` của case được NULL khi payment chưa resolve), SLA `CASE_SLA_FIRST` như case merchant; hiện trong hàng đợi E.12.4 với bộ lọc nguồn.

<a id="muc-e-16-6-post-payments-id-sca-nop-otp-xac-thuc-bo-sung-v3-5-qu"></a>
#### E.16.6 · `POST /payments/{id}/sca` — Nộp OTP xác thực bổ sung «v3.5» · Quyền: user

`{ "otp" (6 số) }` — MMS ghép `challenge_id` đã lưu theo payment rồi chuyển tiếp sang C.9 → `202 { "status": "submitted" }`; kết quả cuối như E.16.2 (notification + poll E.16.3). OTP ở đây là **OTP CỦA ĐỊNH CHẾ NGUỒN** gửi tới SĐT chủ TK — KHÔNG phải OTP Peye-Haiti; app hiển thị `msisdn_masked` để người dùng biết mã về số nào.

**Lỗi riêng:** `PIN-422-BIZ`/`BIZ-OTP-INVALID` OTP sai/hết hạn (kèm `attempts_left` từ định chế) · `PIN-409-STATE` payment không ở `sca_required` · sai quá số lần → định chế chốt `failed`/`failure_reason:"sca_failed"` (app nhận qua notification/E.16.3). Quá `expires_at` → lệnh tự chốt `failed`; muốn trả tiếp thì tạo lệnh mới từ E.16.1.

<a id="muc-p-api-cong-khai-https-api-peye-haiti-ht-public-khong-xac-thu"></a>
## P. API công khai — `https://api.peye-haiti.ht/public` (không xác thực) «Peye-Haiti 15/08»

<a id="muc-p-1-get-public-merchants-code-trang-xac-minh-merchant-yeu-ca"></a>
#### P.1 · `GET /public/merchants/{code}` — Trang xác minh merchant (yêu cầu C-CLIENTS «Vérification»)

Ai cũng mở được (quét QR → link, hoặc nhập mã in trên standee). Response: `{ "code", "shop_name", "mcc", "mcc_label_fr", "market": { "name", "city" }, "public_phone" | null (merchant opt-in), "status": "active"|"suspended", "verified_badge": true }` — KHÔNG BAO GIỜ trả số TK, SĐT cá nhân hay doanh số. Rate-limit theo IP; `suspended` hiện cảnh báo «ngưng xác thực»; mọi trạng thái khác (draft·pending·rejected·closed) → `404` không phân biệt (chống dò).

<a id="muc-f-phu-luc"></a>
## F. Phụ lục

<a id="muc-f-1-bang-tong-hop-toan-bo-ma-loi-danh-muc-dong-41-ma-11-pin"></a>
### F.1. Bảng tổng hợp TOÀN BỘ mã lỗi (danh mục đóng — 41 mã: 11 PIN + 14 OB + 16 BIZ)

Quy tắc tra cứu: client CHỈ xử lý theo `error.code` (`PIN-xxx`); `biz_code` (F.1.3) tinh chỉnh thông điệp/hướng dẫn. Mã `OB-xxx` là mã bank trả cho connector — KHÔNG bao giờ lộ nguyên văn ra app/portal (luôn map theo cột cuối C.0). Mã đối tác khác (`E1-422-QUALITY`, `E1-404-CIN`, `E2-*`, `E3-404-NOTREADY`, `E3-413-SIZE`, `N1-400-TPL`, `N1-422-MSISDN`…) là contract nhóm D, nổi lên BFF thành `PIN-503-DEP` hoặc kết quả nghiệp vụ (danh mục tại D.1–D.5, không lặp lại ở đây).

<a id="muc-f-1-1-pin-xxx-11-ma-chung-mms-chuan-goc-a-4"></a>
#### F.1.1. `PIN-xxx` — 11 mã chung MMS (chuẩn gốc: A.4)

| Mã | HTTP | Nghĩa | Endpoint dùng |
|---|---|---|---|
| `PIN-400-VAL` | 400 | Dữ liệu vào sai (thiếu trường, sai kiểu/format/enum, quá kích thước, cursor hỏng) | Mọi endpoint; ngữ nghĩa riêng tại B.1 (bank KHÔNG retry), B.3, E.13.3 (schema per-key), E.15.2 (khoảng >12 tháng) |
| `PIN-401-AUTH` | 401 | Không xác thực được (JWT/mTLS/PIN/TOTP) | Mọi endpoint; riêng: E.1.5 (`attempts_left`, `new_device_otp_required`), E.1.9, B.1 (bank không retry tự động — kênh D8) |
| `PIN-401-JWS` | 401 | Hash body trong thẻ hệ thống lệch/thiếu («v3.4» — `details.issue`=`body-hash`/`body-hash-missing`) | B.1 · B.4 · B.5 · B.2/B.3 (mọi request đối tác có body) |
| `PIN-403-SCOPE` | 403 | Đúng danh tính, thiếu quyền (RBAC/scope/khác merchant) | Mọi endpoint có RBAC — toàn bộ `/admin/*`, `/ops/*` |
| `PIN-404-NF` | 404 | Không tìm thấy / không thuộc quyền nhìn (không phân biệt — chống dò) | Mọi endpoint có `{id}` — nêu riêng: E.12.9, E.13.9; riêng B.1 (`link_id` quá hạn grace → DLQ bank, không retry) |
| `PIN-409-IDEM` | 409 | Trùng `Idempotency-Key`: body khác (48h), hoặc cùng body đang xử lý (`details.state="processing"`, retryable=true) | Mọi POST ghi (header A.2) |
| `PIN-409-STATE` | 409 | Sai trạng thái state machine / optimistic lock thua | Mọi endpoint chuyển trạng thái — dày nhất ở E.1.1, E.2.2, E.3.x, E.4.5/4.6, E.5.2, E.11.x, E.12.x, E.13.x, E.14.7 · E.16.1/E.16.2/E.16.6 (payment «Peye-Haiti 15/08 · v3.5») |
| `PIN-422-BIZ` | 422 | Vi phạm quy tắc nghiệp vụ — LUÔN kèm `biz_code` (F.1.3) | Mọi endpoint nghiệp vụ; danh sách theo từng `biz_code` bên dưới |
| `PIN-429-RATE` | 429 | Vượt rate limit (kèm `Retry-After`) | Mọi endpoint; ngưỡng riêng: E.1.2 (OTP), E.5.5/E.6.5 (SMS), B.1 (công suất thiết kế 50 GD/giây = 3.000 GD/phút — TSD §9.1) |
| `PIN-500-SYS` | 500 | Lỗi hệ thống MMS (retryable) | Mọi endpoint; cũng là mã nổi lên khi bug connector (C.0: `OB-400-VAL`, `OB-409-IDEM`) |
| `PIN-503-DEP` | 503 | Phụ thuộc không sẵn sàng — circuit breaker mở / bảo trì | Mọi endpoint gọi xuyên đối tác: E.3.2–E.3.7, nhóm B khi MMS bảo trì; mã nổi lên của đa số lỗi OB/E1/E2/E3/N1 hạ tầng |

<a id="muc-f-1-2-ob-xxx-14-ma-open-banking-bank-nhan-chuan-goc-c-0-cot"></a>
#### F.1.2. `OB-xxx` — 14 mã Open Banking bank NHẬN (chuẩn gốc: C.0; cột cuối = mã MMS nổi lên BFF)

| Mã | HTTP | Nghĩa | API dùng (nhóm C) | Nổi lên BFF thành |
|---|---|---|---|---|
| `OB-400-VAL` | 400 | Request MMS sai format (bug connector) | Mọi API C | `PIN-500-SYS` |
| `OB-401-AUTH` | 401 | Thẻ hệ thống A.1b/mTLS của MMS sai (`details.issue`=`alg`/`sig`/`aud`/`expired`/`body-hash`/`header`) | Mọi API C | `PIN-503-DEP` |
| `OB-401-EXPIRED` | 401 | `access_token` của link hết hạn | C.5/C.6/C.7/C.9 (call mang access token) | Trong suốt (MMS tự M1a + retry 1 lần) |
| `OB-401-REVOKED` | 401 | Token đã thu hồi (M1b/bank chủ động) | C.3–C.7 · C.9; hệ quả tại E.3.5/E.3.7 | `PIN-422-BIZ` / `BIZ-TOKEN-REVOKED` |
| `OB-403-SCOPE` | 403 | Token thiếu scope theo bảng A.1b.4 (`balance`/`history`/`credit-notify`/`payment`) | C.5, C.6, C.7, C.9 | `PIN-503-DEP` (C.7: `PIN-422-BIZ`) |
| `OB-404-ACC` | 404 | Số TK không tồn tại tại bank | C.1 | `PIN-422-BIZ` / `BIZ-ACC-NOT-FOUND` |
| `OB-404-LINK` | 404 | Định danh tài nguyên không tồn tại (`link_id` / `ext_payment_id` / `challenge_id` «v3.5») | C.2, C.4, C.8, C.9 | `PIN-404-NF` |
| `OB-409-IDEM` | 409 | Idempotency-Key trùng: body khác (bug connector) hoặc cùng body đang xử lý (processing — chờ rồi gửi lại cùng key) | Mọi POST nhóm C | body khác: `PIN-500-SYS` · processing: retry nội bộ |
| `OB-422-OTP` | 422 | OTP bank sai/hết hạn (`details.attempts_left`) | C.2, C.9 «v3.5» | `PIN-422-BIZ` / `BIZ-OTP-INVALID` |
| `OB-422-RANGE` | 422 | Khoảng thời gian vượt giới hạn bank | C.6 (MMS tự chia nhỏ khoảng) | `PIN-400-VAL` |
| `OB-423-LOCK` | 423 | TK phong tỏa / link request hoặc challenge SCA khóa do sai OTP quá lần «v3.5» | C.1, C.2, C.9 | `PIN-422-BIZ` / `BIZ-ACC-LOCKED` |
| `OB-429-RATE` | 429 | Bank rate limit | Mọi API C (đậm: C.5) | `PIN-429-RATE` |
| `OB-500-SYS` | 500 | Bank lỗi hệ thống | Mọi API C | `PIN-503-DEP` |
| `OB-503-DOWN` | 503 | Bank bảo trì — kích hoạt degrade M4↓ → M3-poll 5’/lần | Mọi API C | `PIN-503-DEP` |

<a id="muc-f-1-3-biz-16-ma-nghiep-vu-luon-di-trong-pin-422-biz-http-422"></a>
#### F.1.3. `BIZ-*` — 16 mã nghiệp vụ (luôn đi trong `PIN-422-BIZ`, HTTP 422; gốc TSD §13.1 + mở rộng)

| `biz_code` | HTTP | Nghĩa | Endpoint dùng |
|---|---|---|---|
| `BIZ-ACC-LOCKED` | 422 | TK bank bị phong tỏa / khóa do sai OTP quá số lần (map `OB-423-LOCK`) | E.3.2, E.3.3 |
| `BIZ-ACC-NOT-FOUND` | 422 | Số TK không tồn tại tại bank (map `OB-404-ACC`) | E.3.2 |
| `BIZ-BILL-STATE` | 422 | Bill không ở trạng thái hợp lệ cho thao tác (đã thu/hủy/hết hạn) | E.4.5, E.4.6, E.5.2, E.6.3, E.9.1 (từng entry batch) |
| `BIZ-DUP-CLIENT-UUID` | 422 | Trùng `client_uuid` nhưng payload KHÁC (idempotency offline A.5) | E.2.2, E.4.3, E.6.2, E.6.3, E.7.2 (+ mọi entity trong E.9.1) · E.16.1 «Peye-Haiti 15/08» |
| `BIZ-EKYC-PENDING` | 422 | eKYC chưa pass / hồ sơ chưa đủ bước cho thao tác | E.3.2, E.11.2 |
| `BIZ-FOUR-EYES` | 422 | Nguyên tắc 4 mắt: checker trùng maker — hệ thống chặn (AC-6.2) | E.13.4, E.13.9 |
| `BIZ-MERCHANT-STATE` | 422 | Merchant `suspended`/`closed` — chặn mọi thao tác GHI nghiệp vụ (quy ước nhóm E) | Mọi endpoint ghi của merchant; nêu riêng: E.4.3 |
| `BIZ-OTP-INVALID` | 422 | OTP sai/hết hạn (`details.attempts_left`) | E.1.3, E.1.8, E.3.3 (OTP bank — map `OB-422-OTP`), E.16.6 (OTP SCA — map `OB-422-OTP` «v3.5») |
| `BIZ-OTP-LIMIT` | 422 | Quá 5 OTP/ngày/số (`OTP_MAX_PER_DAY`) | E.1.1, E.1.2 |
| `BIZ-PERSON-LOCKED` | 422 | Tài khoản đang khóa khẩn (US-39) — mở lại theo runbook hotline | E.1.5 |
| `BIZ-PIN-LOCKED` | 422 | Khóa 60 phút sau 5 lần sai PIN (`details.locked_until`) | E.1.5 |
| `BIZ-REASON-REQUIRED` | 422 | Thiếu lý do bắt buộc — mọi quyết định portal/ops phải có `reason`/`note` | E.11.3, E.11.6, E.11.7, E.11.8, E.12.6, E.12.8, E.13.3, E.13.4, E.13.9, E.14.7 |
| `BIZ-REF-CONFLICT` | 422 | Dedup tầng 2: `ref_id` đã tồn tại với `event_id`/`amount_ct`/`link_id` khác → nghi lệch dữ liệu, mở discrepancy | B.1 |
| `BIZ-REFUND-UNVERIFIED` | 422 | Chặn kết luận «Đã hoàn» khi CHƯA xác minh merchant chuyển trả (không dò thấy bút toán M3 khớp và không có chứng từ — AC-7.1) | E.12.6 |
| `BIZ-REMIND-LIMIT` | 422 | Quá 1 SMS nhắc nợ/khách/ngày (`details.next_allowed_at`) | E.6.5 |
| `BIZ-TOKEN-REVOKED` (E.16.1/E.16.2 dùng chung «Peye-Haiti 15/08») | 422 | Token liên kết đã bị thu hồi — yêu cầu re-link (map `OB-401-REVOKED`) | E.3.5, E.3.7 |

<a id="muc-f-2-ma-tran-endpoint-man-hinh-truy-vet-2-chieu-voi-wireframe"></a>
### F.2. Ma trận endpoint × màn hình (truy vết 2 chiều với wireframes)

> «Peye-Haiti 15/08»: 5 màn người mua **NM-01..05** (Quét & nhập tiền · Xác nhận tên+nguồn · Kết quả & biên lai · Lịch sử & khiếu nại · Liên kết TK trả) map E.16.1–6 + E.3.x («v3.5»: nhập OTP định chế = TRẠNG THÁI của màn NM-03, không thêm màn; NM-01..05 và CH-00 ĐỀU ĐÃ CÓ trong wireframes (42 màn)); trang công khai PUB (P.1) là web, không tính màn app.

Nhóm B/C/D là API máy-máy (không gắn màn hình). **Mọi màn nghiệp vụ đều được liệt kê** — **NB-01 là màn ĐĂNG KÝ chung một app (gọi `E.1.1` — «v3.6» không còn trường gian hàng)**, **NB-03 là trang chủ động (gọi `E.5.1` tiền về hôm nay + `E.8.1` tổng doanh số)**; chỉ các màn thuần tĩnh (hướng dẫn/onboarding, màn lỗi) là không gọi API và không liệt kê.

**Kiểm đếm mục E:** 89 mục đánh số / **90 HTTP endpoint** (`E.13.9` chứa 2 endpoint approve + reject; +E.16.1–6 «v3.5»). Tổng B+C+D+E+P = **109 mục / 110 HTTP endpoint** (B 5 · C 9 · D 5 · E 89 · P 1 — «v3.5»: khôi phục C.9/E.16.6, hai bậc xác thực PIN ≤5.000 / +OTP định chế >5.000).

<a id="muc-f-2-1-app-nguoi-ban-nb"></a>
#### F.2.1. App người bán (NB)

| Màn | Nội dung | Endpoint (mục) |
|---|---|---|
| NB-00/01/02 | Đăng nhập · **đăng ký (NB-01: SĐT · mã NAT-xxx — «v3.6» gian hàng khai ở NB-2B)** · OTP · PIN | E.1.1 · E.1.2 · E.1.3 · E.1.4 · E.1.5 · E.1.6 · E.1.7 (+ E.1.8 khóa khẩn — gọi được từ máy bất kỳ) |
| NB-2A | Chụp & nộp eKYC | E.2.1 · E.2.2 |
| NB-1C | Trạng thái hồ sơ · bổ sung | E.2.3 · E.2.4 |
| NB-2B | Khai gian hàng («v3.6» — nộp cùng E.2.2) + liên kết TK nhận | E.2.2 (phần gian hàng) · E.3.1 · E.3.2 · E.3.3 |
| **NB-03** | **Trang chủ** — tiền về hôm nay · tổng doanh số · hiển thị USD (C5) | **E.5.1 · E.8.1** |
| NB-04 | QR tĩnh | E.4.1 |
| NB-05 | Két tiền — tiền về realtime | E.5.1 · E.5.2 |
| NB-06 | Danh mục món | E.7.1 · E.7.2 · E.7.3 |
| NB-07 | Tính tiền · QR động | E.4.3 · E.4.7 |
| NB-08 | Bill trong ngày (3 nhóm) | E.4.4 · E.4.5 · E.4.6 |
| NB-09 | Lịch sử & biên lai · báo sai · gửi biên lai · cờ doanh thu | E.5.3 · E.5.4 · E.5.5 · E.5.6 |
| NB-10 | Báo cáo bán hàng | E.8.1 |
| NB-13 | Hộp thông báo | E.8.2 · E.8.3 |
| NB-14 | Quản lý liên kết · đổi TK (S4) · standee · gia hạn token | E.3.1 · E.3.5 · E.3.6 · E.3.7 |
| NB-15 | Sổ nợ (offline-first) | E.6.1 · E.6.2 · E.6.3 · E.6.4 · E.6.5 |
| Mọi màn | Đồng bộ offline · upload ảnh · hồ sơ | E.9.1 · E.9.2 · E.10.4 · E.10.5 |

<a id="muc-f-2-2-app-moi-vai-chon-vai-thanh-toan-ch-00-nm-v3-6"></a>
#### F.2.2. App mọi vai — chọn vai & thanh toán (CH-00 + NM) «v3.6»

| Màn | Chức năng | Endpoint |
|---|---|---|
| CH-00 | Chọn vai (sau OTP+PIN, trước eKYC) | `E.10.4 GET /me` (trạng thái vai — app dựng menu) |
| NM-01 | Quét QR & nhập tiền | `E.16.1 POST /payments` |
| NM-02 | Xác nhận TÊN + nguồn trả | `E.16.2 POST /payments/{id}/confirm` |
| NM-03 | Kết quả & biên lai (+nhập OTP >5.000 G) | `E.16.3 GET /payments/{id}` · `E.16.6 POST /payments/{id}/sca` |
| NM-04 | Lịch sử & khiếu nại | `E.16.4 GET /payments` · `E.16.5 POST /payments/{id}/dispute` |
| NM-05 | Liên kết TK nguồn trả | E.3.x (`holder=person`, scope `payment`) |

<a id="muc-f-2-3-portal-brh"></a>
#### F.2.3. Portal BRH

| Màn | Nội dung | Endpoint (mục) |
|---|---|---|
| BRH-01 | Đăng nhập 2 bước (mật khẩu + TOTP) | E.1.9 · E.1.10 |
| BRH-02 | Dashboard tổng quan | E.15.1 (drill-down → E.11.1, E.12.4, E.12.7, E.14.6) |
| BRH-03 | Hậu kiểm hồ sơ gian hàng «v3.6» | E.11.1 · E.11.2 · E.11.3 · E.11.4 |
| BRH-04 | Quản lý merchant · standee · dòng hoạt động | E.11.5 · E.11.6 · E.11.7 · E.11.8 · E.11.9 · E.15.2 |
| BRH-05 | Tra cứu & truy vết giao dịch | E.12.1 · E.12.2 |
| BRH-06 | Case (mở · hàng đợi · chứng cứ · yêu cầu bổ sung · kết luận) | E.12.3 · E.12.4 · E.12.5 · E.15.3 · E.12.6 |
| BRH-07 | Cảnh báo AML | E.12.7 · E.12.8 |
| BRH-08 | KPI & báo cáo | E.13.1 |
| — (vận hành, không màn) | Tham số hệ thống (4 mắt, Natcom ops — màn BRH-09 bỏ 04/08) | E.13.2 · E.13.3 · E.13.4 |
| BRH-11 | Audit log bất biến | E.13.5 |
| BRH-12 | Người dùng & phân quyền | E.13.6 · E.13.7 · E.13.8 |

<a id="muc-f-2-4-console-van-hanh-vds-aq"></a>
#### F.2.4. Console vận hành VDS (AQ)

| Màn | Nội dung | Endpoint (mục) |
|---|---|---|
| AQ-00 | Đầu nối Open Banking · kho token · M3-poll | E.14.1 · E.14.2 |
| AQ-01 | Tổng quan sức khỏe (nội bộ + đối tác) · cảnh báo trực ban | E.14.4 · E.14.1 |
| AQ-03 | Phiên đối soát E3 | E.14.5 |
| AQ-04 | Hàng đợi chênh lệch & xử lý | E.14.6 · E.14.7 |

<a id="muc-f-3-con-dau-noi-dung-the-response-v3-4-thay-chuan-jws-detach"></a>
### F.3. Con dấu nội dung & THẺ RESPONSE «v3.4» — thay chuẩn JWS detached cũ

**Request (mọi chiều): KHÔNG còn chữ ký tách rời.** Toàn vẹn + chống chối bỏ của request nằm ngay trong thẻ hệ thống A.1b: claim `body_sha256` = **hash body** (SHA-256 hex của raw body bytes — không canonicalize JSON, mọi byte đổi = hash đổi). Bên nhận verify theo A.1b.3.

**Response tài chính (C.5 số dư · C.6 lịch sử · C.7/C.8/C.9 lệnh trả — C.9 là POST, thẻ kèm `req_sha256` như C.7): bên trả lời ký THẺ RESPONSE cùng định dạng A.1b** — `iss`/`sub` = tên mình (vd `"UniBank"`), `aud` = tên bên gọi (`"Peye-Haiti"`), `iat`/`exp ≤ 5′`, `body_sha256` = hash raw body của RESPONSE — với **POST** (C.7) kèm thêm claim **`req_sha256`** = hash body của REQUEST tương ứng để buộc chặt «response này trả lời cho đúng request nào»; với **GET** (C.5 · C.6 · C.8): **KHÔNG có `req_sha256`** — toàn chuẩn không hash URL. Bù cho GET bằng quy tắc BẮT BUỘC phía MMS: sau khi verify thẻ, **đối chiếu định danh trong body với tài nguyên đã gọi** — C.5/C.6 body echo `link_id` phải khớp `link_id` trên path; C.8 body `ext_payment_id` phải khớp path; lệch → coi response hỏng, không tin số liệu (ràng buộc cặp request–response lúc chạy đã có mTLS + hạn thẻ 5′ lo). Thẻ đặt ở header **`x-jws-signature: {jwt}`**. MMS verify đúng 3 bước A.1b.3 (+ so `req_sha256` với POST · + đối chiếu định danh với GET) rồi mới tin số liệu. Response khác (B.5, C.1–C.4, nhóm D) không bắt buộc ký — mTLS + không chứa số liệu tài chính.

**Vì sao response cần thẻ riêng:** response không có header thẻ (`x-system-token`); thẻ response là bằng chứng «định chế đã trả lời đúng nội dung này» khi đối soát/tranh chấp. Cùng khóa, cùng hàm ký — dev không học thêm gì mới.

**JWKS:** mỗi bên publish `https://<domain>/.well-known/jwks.json` (chỉ khóa PUBLIC, kty=EC, crv=P-256 — **không cần `kid`**); bên verify cache 1h. **MỘT cặp khóa cho mọi việc** (thẻ request + thẻ response).

**Xoay khóa:** thêm khóa MỚI vào JWKS (tạm thời 2 khóa) ≥7 ngày trước khi dùng — bên verify thử lần lượt từng khóa trong bảng; sau 7 ngày gỡ khóa cũ. Thu hồi KHẨN (nghi lộ khóa): gỡ ngay khỏi JWKS + báo kênh vận hành D8 — thẻ ký khóa cũ fail chữ ký, bên gửi ký lại bằng khóa mới (không mất dữ liệu nhờ chính sách retry B.1 + M3-poll).

**Đồng hồ:** NTP bắt buộc hai bên, dung sai ±30s (đã nằm trong verify A.1b.3).

**B.3 (Switch báo file E3):** giữ chữ ký FILE riêng của Switch — ngoài phạm vi mục này.

**Test vectors:** bộ duy nhất `/docs/auth-vectors/` (khóa mẫu · thẻ mẫu GET/POST · body mẫu · ca lỗi: sai alg · sai chữ ký · sai aud · hết hạn · thiếu/lệch `body_sha256` · thẻ response mẫu) — deliverable sandbox T7/2026, điều kiện nghiệm thu kết nối D2 (TSD §12).

---

<a id="muc-f-4-ho-so-ket-nap-doi-tac-onboarding-v3-2"></a>
### F.4. Hồ sơ kết nạp đối tác (onboarding) «v3.2»

Mỗi định chế/đối tác gia nhập trao đổi với Peye-Haiti MỘT LẦN bảng thông số dưới đây (hai chiều — Peye-Haiti cũng cung cấp bộ của mình cho đối tác); bảng đã ký xác nhận là căn cứ cấu hình AQ-00 và không thay đổi ngoài quy trình:

| # | Thông số | Ghi chú |
|---|---|---|
| 1 | **Tên tổ chức** (giá trị `iss`/`aud` — vd `"UniBank"`) + **mã số 9332xx** — cùng danh mục BRH cấp «v3.4» | Tên dùng trong thẻ A.1b; mã số dùng trong QR (tag định chế) + danh bạ — một danh tính xuyên suốt, ánh xạ 1–1 |
| 2 | URL JWKS (`https://<domain>/.well-known/jwks.json`) | MỘT cặp khóa cho thẻ hệ thống A.1b (kiêm hash body) + thẻ response F.3; xoay khóa theo quy trình chồng lấp F.3 |
| 3 | Chứng chỉ mTLS (CSR/CA phát hành) + dải IP nguồn | Tầng đường truyền — cấu hình một lần, đội hạ tầng hai bên quản |
| 4 | URL nhận webhook + URL API OB của định chế | Webhook B.1/B.4 (chiều vào MMS ghi tại hồ sơ MMS); domain `ob.<bank>.ht` cho nhóm C |
| 5 | Đầu mối vận hành 2 bên (kênh D8) + cửa sổ bảo trì | Phục vụ cảnh báo khóa/chứng chỉ sắp hết hạn, sự cố kết nối |
| 6 | Năng lực SMS OTP tới chủ TK «v3.5» | ĐỊNH CHẾ phải gửi được SMS OTP tới SĐT chủ TK mình giữ — đã dùng ở C.2 (liên kết), TÁI DÙNG cho C.9 (lệnh > 5.000 HTG); SMS GW là của định chế, Peye-Haiti không gửi OTP thanh toán |

**Trình tự kết nạp:** ① ký hồ sơ thông số → ② sandbox: chạy đạt bộ vector auth (A.1b.6 — đã gồm ca hash body, bộ duy nhất `/docs/auth-vectors/`) + kịch bản tích hợp theo ma trận vai trò của bộ chuẩn OB (chiều nhận: 8 API chuẩn = M1×5 + M3×2 + M4×1 · có chiều trả: đủ **12** = +M-PAY×4 (C.7 · C.8 · C.9 · B.4) «v3.5» — khớp ma trận phụ lục MOU A.6.1) → ③ cấp chứng nhận kết nối → ④ mở production (chứng chỉ + IP production riêng, khác sandbox). Đổi bất kỳ thông số nào sau kết nạp: qua kênh vận hành D8 + cập nhật hồ sơ có xác nhận hai bên; riêng xoay khóa theo chu trình chuẩn F.3 thì không cần xác nhận lại.

<a id="muc-f-5-vi-du-ban-tin-day-du-toan-luong-v3-4-nhin-vao-lam-theo"></a>
### F.5. VÍ DỤ BẢN TIN ĐẦY ĐỦ TOÀN LUỒNG «v3.4» — nhìn vào làm theo

> Nhân vật xuyên suốt: người mua **JEAN PIERRE** — TK nguồn trả tại **UniBank**; người bán **MARIE DELVA** (mã `PIN-M-000241`) — TK nhận tại **NatCash** (mã số danh bạ `933201`). Món hàng **1.500 G = 150000 centime** (≤ NGƯỠNG OTP 5.000 HTG — bậc chỉ-PIN; món lớn hơn xem BƯỚC 5-OTP «v3.5»). JWT viết dạng GIẢI MÃ để đọc; trên dây là 3 khúc base64url `header.payload.signature` (rút gọn `eyJ…`). Mọi kết nối đã nằm trong mTLS + VPN (K1). `body_sha256` = **hash body** — SHA-256 hex của đúng chuỗi byte gửi đi.

**BƯỚC 1 — Liên kết TK nguồn trả (C.1, Peye-Haiti → UniBank), làm MỘT lần:**

```http
POST /ob/v1/links HTTP/1.1
Host: ob.unibank.ht
x-system-token: eyJ…                  ← thẻ K2, giải mã:
  header  { "alg": "ES256", "typ": "JWT" }
  payload { "iss": "Peye-Haiti", "sub": "Peye-Haiti", "aud": "UniBank",
            "iat": 1760012340, "exp": 1760012640,
            "body_sha256": "c81d9f2a…44e0" }   ← hash của body bên dưới
Idempotency-Key: 7c9e6679-7425-40de-963d-1a8f30e7a9b4
Content-Type: application/json; charset=utf-8

{ "person_ref": "prn_9f2a71", "requested_scope": ["payment","history"],
  "account_no": "50912340022", "msisdn": "+50937123456", "otp_channel": "sms" }
```
```http
HTTP/1.1 201 Created
Content-Type: application/json; charset=utf-8
X-Trace-Id: tr-8812a4

{ "link_id": "lnk_ub_01HX4Y", "status": "otp_sent",
  "otp_expires_at": "2026-10-01T13:05:00Z", "msisdn_masked": "+509****3456" }
```
*UniBank tự nhắn OTP tới SĐT chủ TK — sự ưng thuận nằm ở đây. (Buyer = KYC1, không gửi `kyc_evidence_ref`.)*

**BƯỚC 2 — Nộp OTP, nhận token liên kết K3 (C.2):**

```http
POST /ob/v1/links/lnk_ub_01HX4Y/confirm HTTP/1.1
Host: ob.unibank.ht
x-system-token: eyJ…                  ← thẻ K2 MỚI (body khác → hash khác)
Idempotency-Key: 913f0e6a-2b1c-47d1-8b0e-55c02f19a001
Content-Type: application/json; charset=utf-8

{ "otp": "482913" }
```
```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{ "link_id": "lnk_ub_01HX4Y",
  "token": { "access_token": "at_ub_7Kp93q…", "expires_at": "2026-12-30T13:05:00Z",
             "refresh_token": "rt_ub_2Mn81c…", "refresh_expires_at": "2027-10-01T13:05:00Z",
             "scope": ["payment","history"] },
  "account_no_masked": "…0022", "holder_name": "JEAN PIERRE" }
```
*`access_token` cất Vault mã hóa — không bao giờ ghi log. Từ đây Peye-Haiti có «bằng chứng ưng thuận» để khởi tạo lệnh trả.*

**BƯỚC 2b — (minh họa GET) hỏi lịch sử (C.6): thẻ KHÔNG có hash body, dùng lại được ≤5′:**

```http
GET /ob/v1/accounts/lnk_ub_01HX4Y/transactions?from=2026-10-01T00:00:00Z&to=2026-10-01T23:59:59Z HTTP/1.1
Host: ob.unibank.ht
x-system-token: eyJ…                  ← payload: { "iss":"Peye-Haiti","sub":"Peye-Haiti","aud":"UniBank","iat":…,"exp":… }  (không body_sha256)
x-account-token: at_ub_7Kp93q…
```
```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
x-jws-signature: eyJ…                 ← THẺ RESPONSE của UniBank, giải mã:
  payload { "iss": "UniBank", "sub": "UniBank", "aud": "Peye-Haiti",
            "iat": 1760012400, "exp": 1760012700,
            "body_sha256": "77b1a0…9c3e" }  ← GET: chỉ hash body response — KHÔNG req_sha256; MMS đối chiếu link_id trong body với path (F.3)

{ "link_id": "lnk_ub_01HX4Y", "items": [ … ], "next_cursor": null }
```

**BƯỚC 3 — Người mua quét QR của MARIE DELVA, app tạo lệnh (E.16.1, app → BFF):**

```http
POST /v1/payments HTTP/1.1
Host: api.peye-haiti.ht
Authorization: Bearer eyJ…            ← JWT PHIÊN NGƯỜI DÙNG của Jean (BFF — khác thẻ K2)
X-Device-Id: 3d1f9a7e-…
Content-Type: application/json; charset=utf-8

{ "client_uuid": "b41c2f6a-9e10-4dd1-a5f7-6b2f0c4e71d3",
  "funding_link_id": "lnk_ub_01HX4Y",
  "target": { "operator": "933201", "account": "50912347709", "merchant_hint": "MARIE DELVA" },
  "amount_ct": 150000, "currency": "HTG", "bill_code": "B-1007-17" }
```
```http
HTTP/1.1 201 Created

{ "payment_id": "pay_ph_4Q8Z1M", "status": "created", "expires_at": "2026-10-01T13:19:00Z",
  "merchant": { "merchant_id": "m01hx4y7q2k8w", "shop_name": "MARIE DELVA",
                "mcc": "5411", "city": "Pétion-Ville", "verified": true } }
```
*App hiện: «Trả 1.500 G cho **MARIE DELVA** ✔ Đã xác thực» — người mua thấy TÊN rồi mới xác nhận (chống QR dán đè). Món > 5.000 HTG: tạo lệnh bình thường — bậc OTP xử lý ở BƯỚC 5-OTP.*

**BƯỚC 4 — Xác nhận bằng PIN app (E.16.2) — bậc 1 (mọi lệnh; món ≤ 5.000 G thì đây là bước duy nhất):**

```http
POST /v1/payments/pay_ph_4Q8Z1M/confirm HTTP/1.1
Host: api.peye-haiti.ht
Authorization: Bearer eyJ…            ← JWT phiên người dùng
Content-Type: application/json; charset=utf-8

{ "pin": "••••••" }                    ← PIN của app Peye-Haiti (server so băm Argon2id — không log)
```
```http
HTTP/1.1 202 Accepted

{ "status": "submitted" }
```

**BƯỚC 5 — Peye-Haiti khởi tạo lệnh trả tại UniBank (C.7):**

```http
POST /ob/v1/payments HTTP/1.1
Host: ob.unibank.ht
x-system-token: eyJ…                  ← thẻ K2 MỚI, giải mã:
  payload { "iss": "Peye-Haiti", "sub": "Peye-Haiti", "aud": "UniBank",
            "iat": 1760012501, "exp": 1760012801,
            "body_sha256": "4fa2c9…b7d1" }   ← chính thẻ này = bằng chứng chống chối bỏ (UniBank lưu 5 năm)
x-account-token: at_ub_7Kp93q…         ← K3 scope "payment" — ưng thuận đã cấp ở BƯỚC 2
Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000
Content-Type: application/json; charset=utf-8

{ "client_ref": "pay_ph_4Q8Z1M", "link_id": "lnk_ub_01HX4Y",
  "target": { "operator": "933201", "account": "50912347709", "name_hint": "MARIE DELVA" },
  "amount_ct": 150000, "currency": "HTG", "bill_code": "B-1007-17" }
```
```http
HTTP/1.1 202 Accepted
x-jws-signature: eyJ…                 ← thẻ response UniBank (body_sha256 của body dưới + req_sha256 = hash body request — POST)

{ "ext_payment_id": "pay_ub_889AZ", "status": "submitted" }
```
*Món 1.500 G ≤ ngưỡng 5.000 → UniBank KHÔNG hỏi Jean thêm gì — thực thi theo K3 + hạn mức tự áp. Tiền đi Switch/on-us như mọi lệnh chuyển thường.*

**BƯỚC 5-OTP — BIẾN THỂ món > 5.000 HTG «v3.5»** (ví dụ Jean trả nhà cung cấp 12.000 G = 1200000 ct — giao dịch bán-với-bán): BƯỚC 3–5 y hệt, nhưng UniBank trả nhánh OTP:

```http
HTTP/1.1 202 Accepted
x-jws-signature: eyJ…                 ← thẻ response UniBank

{ "ext_payment_id": "pay_ub_912KX", "status": "sca_required",
  "sca": { "challenge_id": "chl_7Y2Q", "otp_channel": "sms",
           "msisdn_masked": "+509****3456",
           "expires_at": "2026-10-01T13:07:00Z", "attempts_left": 3 } }
```
*UniBank ĐÃ tự nhắn OTP tới SĐT của Jean (bằng SMS GW CỦA UNIBANK — Peye-Haiti không gửi gì). App chuyển màn NM-03 sang trạng thái nhập OTP.*

Jean gõ OTP trong app (E.16.6) → Peye-Haiti chuyển tiếp sang UniBank (C.9):

```http
POST /ob/v1/payments/pay_ub_912KX/sca HTTP/1.1
Host: ob.unibank.ht
x-system-token: eyJ…                  ← thẻ K2 MỚI (body_sha256 của body dưới)
x-account-token: at_ub_7Kp93q…
Idempotency-Key: 6ba7b810-9dad-41d1-80b4-00c04fd430c8
Content-Type: application/json; charset=utf-8

{ "challenge_id": "chl_7Y2Q", "otp": "735120" }
```
```http
HTTP/1.1 202 Accepted
x-jws-signature: eyJ…

{ "ext_payment_id": "pay_ub_912KX", "status": "submitted" }
```
*Từ đây giống BƯỚC 6 — kết quả cuối về qua webhook. OTP sai → `422 OB-422-OTP` kèm `attempts_left`; sai quá số lần hoặc quá hạn → định chế chốt `failed`/`sca_failed`.*

**BƯỚC 6 — UniBank báo kết quả cuối (B.4, UniBank → Peye-Haiti):**

```http
POST /v1/payment-results HTTP/1.1
Host: partner.peye-haiti.ht
x-system-token: eyJ…                  ← thẻ K2 của UNIBANK, giải mã:
  payload { "iss": "UniBank", "sub": "UniBank", "aud": "Peye-Haiti",
            "iat": 1760012504, "exp": 1760012804, "body_sha256": "e01b77…2a9f" }
Content-Type: application/json; charset=utf-8

{ "event_id": "f7a1d2c9-3b60-4e2f-9d11-8c5a0b7e4f22",
  "ext_payment_id": "pay_ub_889AZ", "client_ref": "pay_ph_4Q8Z1M",
  "status": "succeeded", "failure_reason": null,
  "ref_id": "PIN-2026-000123", "finished_at": "2026-10-01T13:04:07Z" }
```
```http
HTTP/1.1 200 OK

{ "received": true }
```
*Thất bại thì `status:"failed"` + `failure_reason` (`insufficient_funds`/`declined`/`limit`/`other`) — là DỮ LIỆU, không phải lỗi HTTP.*

**BƯỚC 7 — NatCash (bank NHẬN của MARIE) báo Có (B.1, NatCash → Peye-Haiti) — «ting ting»:**

```http
POST /v1/credit-events HTTP/1.1
Host: partner.peye-haiti.ht
x-system-token: eyJ…                  ← thẻ K2 của NATCASH:
  payload { "iss": "NatCash", "sub": "NatCash", "aud": "Peye-Haiti",
            "iat": 1760012506, "exp": 1760012806, "body_sha256": "9f2a4c…e81d" }
Content-Type: application/json; charset=utf-8

{ "event_id": "9b2f0c4e-71d3-4a8e-b1aa-0f3c9d2e5a10",
  "link_id": "lnk_nc_88213", "account_no_masked": "…7709",
  "ref_id": "PIN-2026-000123", "amount_ct": 150000, "currency": "HTG",
  "booked_at": "2026-10-01T13:04:07Z",
  "payer": { "msisdn": "+50937123456", "holder_name": "J. PIERRE", "bank_code": "UNIB" },
  "addenda": { "bill_id": "B-1007-17" } }
```
```http
HTTP/1.1 200 OK

{ "status": "accepted", "event_id": "9b2f0c4e-71d3-4a8e-b1aa-0f3c9d2e5a10" }
```
*Hai phía độc lập gặp nhau tại `ref_id` = `PIN-2026-000123`; bill B-1007-17 gạch tự động (luồng S2).*

**BƯỚC 8 — App người mua lấy biên lai (E.16.3):**

```http
GET /v1/payments/pay_ph_4Q8Z1M HTTP/1.1
Host: api.peye-haiti.ht
Authorization: Bearer eyJ…            ← JWT phiên người dùng
```
```http
HTTP/1.1 200 OK

{ "payment_id": "pay_ph_4Q8Z1M", "status": "succeeded", "failure_reason": null,
  "merchant": { "shop_name": "MARIE DELVA", "mcc": "5411" },
  "amount_ct": 150000, "ref_id": "PIN-2026-000123",
  "finished_at": "2026-10-01T13:04:07Z",
  "receipt": { "no": "PIN-2026-000123", "issued_at": "2026-10-01T13:04:07Z" } }
```

**CÁC CA LỖI HAY GẶP (để dev test tay):**

| Ca | Bên phát hiện | Trả về |
|---|---|---|
| Body bị sửa 1 byte trên đường (hash lệch) | Bên nhận, bước 3 verify A.1b.3 | `401 PIN-401-JWS` / `OB-401-AUTH` + `details.issue:"body-hash"` — KHÔNG parse body |
| Thẻ quá 5 phút (retry bằng thẻ cũ) | Bên nhận, bước 2 | `401` + `details.issue:"expired"` — ký thẻ MỚI rồi gửi lại |
| Thẻ của MonCash nhưng dữ liệu của liên kết NatCash | Tầng ứng dụng sau verify | `404 PIN-404-NF` — «báo Có của liên kết nhà ai chỉ nhà ấy được báo» |
| Món 6.000 G (> ngưỡng 5.000) | UniBank tại C.7 | `202` + `status:"sca_required"` — KHÔNG phải lỗi: app chuyển trạng thái nhập OTP (BƯỚC 5-OTP) |
| Nhập sai OTP định chế | UniBank tại C.9 | `422 OB-422-OTP` + `details.attempts_left`; sai quá số lần → `failed`/`sca_failed` qua webhook |
| Lệnh bậc-PIN vượt trần ngày (`PAY_DAY_MAX`) | E.16.1 (app đã chặn từ trước) | `422 PIN-422-BIZ` + `details.issue:"daily_limit"` |
| Gửi thẻ K2 vào `Authorization` thay vì `x-system-token` | Gateway route đối tác | `401` + `details.issue:"header"` — chuyển thẻ sang `x-system-token` («v3.7») |
| Trùng `Idempotency-Key` + cùng body khi lệnh trước đang xử lý | Bên nhận, tầng idempotency | `409` + `details.state:"processing"` + `Retry-After: 1` — GIỮ key, chờ rồi gửi lại («v3.7») |
| Token K3 bị chủ TK thu hồi giữa chừng | UniBank tại C.7 | `401 OB-401-REVOKED` → app báo «liên kết lại nguồn trả» |

*Hết tài liệu. Nguồn đồng bộ: TSD §2c (danh mục endpoint), §3 (M4), §13.1/§13.3 (mã BIZ, tham số); Data Dictionary đi kèm cho định nghĩa trường mức DB. OpenAPI YAML sinh từ tài liệu này (`/docs/openapi/bff.yaml`) là deliverable bắt buộc sprint 1 — mọi sai khác giữa YAML và tài liệu này: tài liệu này thắng.*
