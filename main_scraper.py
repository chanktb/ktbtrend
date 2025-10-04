import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from datetime import datetime

# ----------------- Cấu hình -----------------
HTML_SOURCE = "https://trends24.in/united-states/"
OUTPUT_FILE = "hashtags.txt"
HEADERS = {
    # Giả mạo User-Agent của một trình duyệt phổ biến để tránh bị chặn
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
# --------------------------------------------

def load_html(url):
    """Tải nội dung HTML từ URL."""
    print(f"Bắt đầu tải nội dung từ: {url}")
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status() # Gây lỗi nếu mã trạng thái không phải 200 OK
        print("✅ Tải HTML thành công.")
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"❌ Lỗi khi tải URL {url}: {e}")
        return None

def analyze_trends(html_content):
    """Phân tích HTML và sắp xếp các trend."""
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, 'html.parser')
    trend_data = {}

    # Quét tất cả các cột list-container
    list_containers = soup.find_all('div', class_='list-container')

    for container in list_containers:
        # Lấy danh sách trends trong cột đó (thứ tự từ 1 đến 50)
        trend_links = container.select('ol.trend-card__list a.trend-link')
        
        for rank, link in enumerate(trend_links):
            trend_name = link.text.strip()
            
            # Xử lý tên trend cho Key và URL: Loại bỏ ký tự '#' nếu có
            cleaned_key = trend_name.lstrip('#')
            
            if cleaned_key not in trend_data:
                # [trend_name_gốc, số_lần_xuất_hiện, vị_trí_xuất_hiện_tốt_nhất (rank thấp nhất)]
                trend_data[cleaned_key] = [trend_name, 0, rank + 1]
            
            trend_data[cleaned_key][1] += 1
            # Cập nhật vị trí tốt nhất (nếu rank hiện tại tốt hơn)
            if rank + 1 < trend_data[cleaned_key][2]:
                trend_data[cleaned_key][2] = rank + 1

    # Sắp xếp theo: 1. Số lần xuất hiện (giảm dần), 2. Vị trí tốt nhất (tăng dần)
    sorted_trends = sorted(
        trend_data.values(), 
        key=lambda x: (-x[1], x[2], x[0])
    )

    return sorted_trends

def generate_output(sorted_trends):
    """Tạo nội dung file .txt (dùng để tạo Deeplink trong HTML)."""
    txt_content = ""
    for name, count, best_rank in sorted_trends:
        # Chuẩn hóa cho URL: Loại bỏ '#' và thay khoảng trắng bằng '+'
        # Sử dụng quote để đảm bảo an toàn cho mọi ký tự
        url_key = quote(name.lstrip('#').replace(' ', ' '))
        # Format: Tên_Gốc|Url_Key|Tần_suất|Top_Rank
        txt_content += f"{name}|{url_key}|{count}|{best_rank}\n"
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(txt_content)
    
    print(f"✅ Đã lưu {len(sorted_trends)} trends vào {OUTPUT_FILE}.")


if __name__ == "__main__":
    print("--- Bắt đầu quét và phân tích xu hướng ---")
    
    html_content = load_html(HTML_SOURCE)
    
    if html_content:
        sorted_trends = analyze_trends(html_content)
        if sorted_trends:
            generate_output(sorted_trends)
        else:
            print("Lỗi: Không tìm thấy trends nào trong nội dung HTML.")
    
    print("--- Kết thúc main_scraper ---")