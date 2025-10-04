import subprocess
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# Tải biến môi trường từ file .env (cho môi trường cục bộ)
try:
    load_dotenv()
except ImportError:
    pass

# ----------------- Cấu hình -----------------
FILE_TO_COMMIT = "hashtags.txt" 
GIT_STATUS_FILE = "git_status.txt" 
BRANCH_NAME = "main" 
# --------------------------------------------

def git_push():
    """Thực hiện chuỗi lệnh Git: add, commit, push và ghi trạng thái."""
    print("--- Bắt đầu quá trình Git Commit & Push ---")
    
    status_message = "❌ Git Push Thất bại: Lỗi không xác định."

    if not os.path.exists(FILE_TO_COMMIT):
        status_message = f"❌ Git Push Thất bại: Không tìm thấy file {FILE_TO_COMMIT}."
        print(status_message)
        with open(GIT_STATUS_FILE, "w", encoding='utf-8') as f: f.write(status_message)
        return

    try:
        commit_message = f"Trend Update: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        # 1. Add ALL changes (bao gồm code và file output, nhưng bỏ qua file trong .gitignore)
        # Sử dụng git add -A để add tất cả các thay đổi (Modified, Added, Deleted)
        subprocess.run(["git", "add", "-A"], check=True, capture_output=True, text=True)
        print("✅ Git Add: Đã thêm tất cả các file có thay đổi.")

        # 2. Commit
        # Sử dụng git commit để commit các file đã được staging
        commit_result = subprocess.run(["git", "commit", "-m", commit_message], capture_output=True, text=True)

        if "nothing to commit" in commit_result.stdout or "nothing to commit" in commit_result.stderr:
            status_message = "⚠️ Git Push: Không có thay đổi nào cần commit. Bỏ qua push."
            print(status_message)
            return # Dừng nếu không có gì để push

        # Commit thành công, tiến hành Push
        commit_result.check_returncode() 
        print(f"✅ Git Commit: '{commit_message}'")

        # 3. Push
        subprocess.run(["git", "push", "origin", BRANCH_NAME], check=True, capture_output=True, text=True)
        status_message = "✅ Git Push thành công!"
        print(status_message)

    except subprocess.CalledProcessError as e:
        error_details = e.stderr.strip() or e.stdout.strip() or "Không có thông báo lỗi chi tiết."
        status_message = f"❌ Git Push Thất bại: {error_details}"
        print(f"❌ Git Push Thất bại: Lỗi khi chạy lệnh Git. Vui lòng kiểm tra Git Credentials.")
        print(f"Lỗi chi tiết từ Git: {error_details}")

    except FileNotFoundError:
        status_message = "❌ Git Push Thất bại: Lệnh 'git' không tìm thấy."
        print(status_message)
        
    finally:
        # 4. Ghi trạng thái cuối cùng vào file (encoding='utf-8')
        try:
            with open(GIT_STATUS_FILE, "w", encoding='utf-8') as f:
                f.write(status_message)
        except Exception as e:
            print(f"❌ CẢNH BÁO: Không thể ghi trạng thái Git vào file tạm. Lỗi: {e}")

    print("--- Kết thúc git_pusher ---")


if __name__ == "__main__":
    git_push()