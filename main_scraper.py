import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from datetime import datetime

# ----------------- Cấu hình -----------------
HTML_SOURCE = "https://trends24.in/united-states/"
OUTPUT_FILE = "hashtags.txt"
TOP10_FILE = "top10_trends.txt" # Tên file tạm thời mới
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
# --------------------------------------------

def load_html(url):
    # ... (giữ nguyên hàm load_html từ câu trả lời trước)
    print(f"Bắt đầu tải nội dung từ: {url}")
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        print("✅ Tải HTML thành công.")
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"❌ Lỗi khi tải URL {url}: {e}")
        return None

def analyze_trends(html_content):
    # ... (giữ nguyên hàm analyze_trends từ câu trả lời trước)
    if not html_content: return []
    soup = BeautifulSoup(html_content, 'html.parser')
    trend_data = {}
    list_containers = soup.find_all('div', class_='list-container')

    for container in list_containers:
        trend_links = container.select('ol.trend-card__list a.trend-link')
        for rank, link in enumerate(trend_links):
            trend_name = link.text.strip()
            cleaned_key = trend_name.lstrip('#')
            
            if cleaned_key not in trend_data:
                trend_data[cleaned_key] = [trend_name, 0, rank + 1]
            
            trend_data[cleaned_key][1] += 1
            if rank + 1 < trend_data[cleaned_key][2]:
                trend_data[cleaned_key][2] = rank + 1

    sorted_trends = sorted(
        trend_data.values(), 
        key=lambda x: (-x[1], x[2], x[0])
    )
    return sorted_trends


def generate_output(sorted_trends):
    """Tạo file hashtags.txt (full list) và top10_trends.txt (cho Telegram)."""
    
    # 1. Tạo nội dung cho file hashtags.txt (Full list)
    txt_content = ""
    for name, count, best_rank in sorted_trends:
        url_key = quote(name.lstrip('#').replace(' ', ' '))
        txt_content += f"{name}|{url_key}|{count}|{best_rank}\n"
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(txt_content)
    
    print(f"✅ Đã lưu {len(sorted_trends)} trends vào {OUTPUT_FILE} (Full List).")

    # 2. Tạo nội dung cho file top10_trends.txt (Chỉ 10 trend đầu)
    top10_content = ""
    for i, (name, count, best_rank) in enumerate(sorted_trends[:10]):
        # Format: #Rank. TrendName (Tần suất: Count, Top: #BestRank)
        top10_content += f"*{i+1}. {name}* (Tần suất: {count}, Top: #{best_rank})\n"
        
    with open(TOP10_FILE, "w", encoding="utf-8") as f:
        f.write(top10_content)

    print(f"✅ Đã lưu Top 10 trends vào {TOP10_FILE} (Cho Telegram).")
    
    # Trả về thông tin cần thiết cho Git Pusher (dù Git Pusher không dùng, nhưng là best practice)
    return len(sorted_trends)


if __name__ == "__main__":
    print("--- Bắt đầu quét và phân tích xu hướng ---")
    
    html_content = load_html(HTML_SOURCE)
    
    if html_content:
        sorted_trends = analyze_trends(html_content)
        if sorted_trends:
            trend_count = generate_output(sorted_trends)
        else:
            print("Lỗi: Không tìm thấy trends nào trong nội dung HTML.")
    
    print("--- Kết thúc main_scraper ---")