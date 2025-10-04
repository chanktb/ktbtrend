import subprocess
import sys
import os

# ----------------- Cấu hình -----------------
FILE_TO_COMMIT = "hashtags.txt" # Đã đổi tên
COMMIT_MESSAGE = f"Trend Update: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
BRANCH_NAME = "main" 
# --------------------------------------------

def git_push():
    """Thực hiện chuỗi lệnh Git: add, commit, push."""
    print("--- Bắt đầu quá trình Git Commit & Push ---")
    
    # Tạo một commit message chi tiết hơn
    global COMMIT_MESSAGE
    COMMIT_MESSAGE = f"Trend Update: {datetime.now().strftime('%Y-%m-%d %H:%M')}"

    if not os.path.exists(FILE_TO_COMMIT):
        print(f"Lỗi: Không tìm thấy file {FILE_TO_COMMIT}. Bỏ qua Git Push.")
        return

    try:
        # 1. Thêm file vào staging area
        subprocess.run(["git", "add", FILE_TO_COMMIT], check=True, capture_output=True, text=True)

        # 2. Commit các thay đổi
        commit_result = subprocess.run(["git", "commit", "-m", COMMIT_MESSAGE], capture_output=True, text=True)

        if "nothing to commit" in commit_result.stdout or "nothing to commit" in commit_result.stderr:
            print("⚠️ Git Commit: Không có thay đổi nào trong file. Bỏ qua push.")
            return

        commit_result.check_returncode() # Kiểm tra lỗi commit nghiêm trọng
        print(f"✅ Git Commit: '{COMMIT_MESSAGE}'")

        # 3. Đẩy lên remote
        subprocess.run(["git", "push", "origin", BRANCH_NAME], check=True, capture_output=True, text=True)
        print(f"✅ Git Push thành công lên branch: {BRANCH_NAME}")

    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi chạy lệnh Git (Commit hoặc Push thất bại):")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        sys.exit(1)

    except FileNotFoundError:
        print("❌ Lỗi: Lệnh 'git' không tìm thấy. Hãy đảm bảo Git đã được cài đặt.")
        sys.exit(1)

    print("--- Kết thúc git_pusher ---")


if __name__ == "__main__":
    from datetime import datetime # Import lại ở đây để đảm bảo chạy độc lập
    git_push()