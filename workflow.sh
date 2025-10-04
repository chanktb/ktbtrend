#!/bin/bash
# file: workflow.sh
echo "--- Bắt đầu Workflow Tìm kiếm Trend Áo Thun ---"

# --- 1. Chạy Scraper để lấy và sắp xếp hashtag ---
echo "Bước 1: Chạy main_scraper.py..."
python main_scraper.py
if [ $? -ne 0 ]; then
    echo "LỖI: main_scraper.py thất bại. Dừng workflow."
    exit 1
fi

# --- 2. Chạy Git Pusher để cập nhật GitHub ---
echo "Bước 2: Chạy git_pusher.py..."
python git_pusher.py
# Lưu ý: Lệnh này được phép thất bại nếu không có thay đổi nào.

# --- 3. Chạy Telegram Notifier để gửi báo cáo ---
echo "Bước 3: Chạy telegram_notifier.py..."
# Đảm bảo bạn đã export các biến môi trường này trước khi chạy:
# export TELEGRAM_BOT_TOKEN="YOUR_TOKEN"
# export TELEGRAM_CHAT_ID="YOUR_CHAT_ID"
python telegram_notifier.py

echo "--- Workflow HOÀN TẤT. Kiểm tra GitHub và Telegram ---"