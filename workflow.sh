#!/bin/bash
# file: workflow.sh
echo "--- Bắt đầu Workflow Tìm kiếm Trend Áo Thun ---"
# 1. Chạy Scraper
echo "Bước 1: Chạy main_scraper.py (Lấy data và Top 10)..."
python main_scraper.py
if [ $? -ne 0 ]; then
    echo "LỖI: main_scraper.py thất bại. Dừng workflow."
    exit 1
fi

# 2. Chạy Git Pusher
echo "Bước 2: Chạy git_pusher.py (Cập nhật GitHub và ghi trạng thái)..."
python git_pusher.py

# 3. Chạy Telegram Notifier
echo "Bước 3: Chạy telegram_notifier.py (Gửi báo cáo)..."
python telegram_notifier.py

echo "--- Workflow HOÀN TẤT. ---"
# --- BƯỚC MỚI: DỌN DẸP FILE TẠM TRÊN PC ---
echo "Dọn dẹp các file tạm thời..."
rm -f top10_trends.txt git_status.txt
read -p "Nhấn ENTER để đóng cửa sổ..."
