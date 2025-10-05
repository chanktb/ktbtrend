import requests
import os
import sys
from datetime import datetime
from dotenv import load_dotenv 

# Tải biến môi trường từ file .env (cho môi trường cục bộ)
load_dotenv() 

# ----------------- Cấu hình -----------------
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GIT_STATUS_FILE = "git_status.txt"
TOP10_FILE = "top10_trends.txt"
# --------------------------------------------

def build_telegram_message():
    """Đọc dữ liệu và tạo nội dung tin nhắn Telegram."""
    
    # 1. Lấy Timestamp (+07 GMT/ICT)
    # Lấy giờ hiện tại và định dạng theo múi giờ Việt Nam (ICT/GMT+7)
    current_time_gmt7 = datetime.now().strftime('%Y-%m-%d %H:%M:%S +07') 
    
    # 2. Lấy Top 10 Trends
    try:
        with open(TOP10_FILE, 'r', encoding='utf-8') as f:
            top10_trends = f.read().strip()
    except FileNotFoundError:
        top10_trends = "Không tìm thấy danh sách Top 10 trends. (Lỗi Scraper?)"
        
    # 3. Lấy Trạng thái Git Push
    try:
        with open(GIT_STATUS_FILE, 'r', encoding='utf-8') as f:
            git_status = f.read().strip()
    except FileNotFoundError:
        git_status = "⚠️ Trạng thái Git Push không xác định. (Lỗi Pusher?)"
    
    # 4. Định dạng Tin nhắn
    message = (
        "*ktbtrend report*\n"
        f"Timestamp: {current_time_gmt7}\n"
        "\n"
        "--- Top 10 Trends ---\n"
        f"{top10_trends}\n"
        "---------------------\n"
        "khuetran.com/trend/\n"
        f"Status: {git_status}"
    )
    
    return message

def send_telegram_message(message):
    """Gửi tin nhắn thông báo qua API Telegram Bot."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Lỗi cấu hình: Biến môi trường Telegram chưa được đặt.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown' # Sử dụng Markdown để in đậm và định dạng
    }

    try:
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
        print("✅ Thông báo Telegram đã được gửi thành công.")

    except requests.exceptions.RequestException as e:
        print(f"❌ Lỗi khi gửi thông báo Telegram: {e}")
        sys.exit(1)


if __name__ == "__main__":
    print("--- Bắt đầu gửi thông báo Telegram ---")
    
    final_message = build_telegram_message()
    send_telegram_message(final_message)
    
    print("--- Kết thúc telegram_notifier ---")