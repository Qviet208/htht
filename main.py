import os
import requests
from tqdm import tqdm
import subprocess

url = "https://www.mediafire.com/file/tq38a4bszstqvry/htht.7z/file"
download_path = "/sdcard/Download/htht.7z"
extract_path = "/sdcard/Download/htht_game"

def ensure_storage_permission():
    try:
        subprocess.call(["termux-setup-storage"])
    except FileNotFoundError:
        print("⚠️ Lệnh termux-setup-storage không khả dụng ngoài Termux.")

def download_file(url, filename):
    response = requests.get(url, stream=True)
    total = int(response.headers.get('content-length', 0))
    with open(filename, 'wb') as file, tqdm(
        desc=filename, total=total, unit='iB', unit_scale=True, unit_divisor=1024
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

def extract_file(filename, path):
    if not os.path.exists(path):
        os.makedirs(path)
    # dùng p7zip để giải nén thay cho py7zr
    subprocess.run(["7z", "x", filename, f"-o{path}", "-y"], check=True)

def run_sh(script, path):
    script_path = os.path.join(path, script)
    if os.path.exists(script_path):
        subprocess.call(["sh", script_path])
    else:
        print(f"❌ Không tìm thấy {script}")

def main():
    ensure_storage_permission()

    print("📥 Đang tải game...")
    download_file(url, download_path)

    print("📂 Đang giải nén game...")
    extract_file(download_path, extract_path)

    print(f"\n✅ Game đã được giải nén tại: {extract_path}")
    print("👉 Vui lòng mở file htht.apk trong thư mục này để tự cài đặt game.\n")

    input("📌 Sau khi bạn cài xong htht.apk, nhấn Enter để tiếp tục...")

    run_sh("install.sh", extract_path)
    run_sh("menu.sh", extract_path)

if __name__ == "__main__":
    main()
