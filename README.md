# Bybit Familiar Seller Bot (Telegram)

Bot này sẽ tự động kiểm tra quảng cáo Bybit P2P và gửi thông báo Telegram khi phát hiện người bán quen.

## 🚀 Cách sử dụng (Railway)

1. Push thư mục này lên GitHub
2. Tạo Project mới trên https://railway.app → Chọn `Deploy from GitHub`
3. Vào tab `Variables`, thêm:
   - `TELEGRAM_TOKEN`: Token bot Telegram
   - `CHAT_ID`: Chat ID Telegram của bạn

Bot sẽ tự động chạy và gửi cảnh báo nếu phát hiện người bán trong danh sách `FAMILIAR_SELLERS`.

## 📁 Cấu trúc

- `main.py` – mã bot chính
- `payment_mapping.py` – mã hóa phương thức thanh toán
- `requirements.txt` – thư viện cần cài
- `.env.example` – ví dụ biến môi trường