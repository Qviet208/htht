import os
import subprocess

download_path = "/sdcard/Download/htht.7z"
extract_path = "/sdcard/Download/htht_game"

def ensure_storage_permission():
    try:
        subprocess.call(["termux-setup-storage"])
    except FileNotFoundError:
        print("⚠️ Lệnh termux-setup-storage không khả dụng ngoài Termux.")

def extract_file(filename, path):
    os.makedirs(path, exist_ok=True)
    subprocess.run(["7z", "x", filename, f"-o{path}", "-y"], check=True)

def run_sh(script, path):
    script_path = os.path.join(path, script)
    if os.path.exists(script_path):
        subprocess.call(["chmod", "+x", script_path])
        subprocess.call(["sh", script_path])
    else:
        print(f"⚠️ Không tìm thấy {script}")

def main():
    ensure_storage_permission()

    if os.path.exists(download_path):
        print("✅ Đã tìm thấy file:", download_path)
    else:
        print("❌ Không có file htht.7z trong thư mục Download.")
        print("👉 Hãy tải file htht.7z thủ công vào /sdcard/Download rồi chạy lại.")
        return

    print("📦 Đang giải nén...")
    extract_file(download_path, extract_path)

    print(f"\n✅ Giải nén xong tại: {extract_path}")
    print("👉 Vào thư mục này để cài đặt htht.apk\n")

    input("📌 Sau khi cài xong htht.apk, nhấn Enter để tiếp tục...")

    run_sh("install.sh", extract_path)
    run_sh("menu.sh", extract_path)

if __name__ == "__main__":
    main()
