import requests
import os
import sys
from datetime import datetime

# ----------------- Cấu hình -----------------
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
REPO_URL = os.getenv("GITHUB_REPOSITORY_URL", "https://github.com/YOUR_USERNAME/YOUR_REPO")
# --------------------------------------------

def send_telegram_message(message):
    """Gửi tin nhắn thông báo qua API Telegram Bot."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Lỗi cấu hình: Biến môi trường Telegram chưa được đặt.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
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
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    report_message = (
        f"Trend Scraper Report - {current_time}\n"
        "🔥 **Workflow HOÀN TẤT!**\n\n"
        "1. Quét trends Mỹ (trends24.in) đã xong.\n"
        "2. File `hashtags.txt` đã được cập nhật và push lên GitHub.\n\n"
        f"🔗 [Xem kết quả trên Repo]({REPO_URL}/blob/main/hashtags.txt)"
    )
    
    send_telegram_message(report_message)
    
    print("--- Kết thúc telegram_notifier ---")