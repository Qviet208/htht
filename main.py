import os
import requests
import subprocess
from tqdm import tqdm
from bs4 import BeautifulSoup

# Link Mediafire (link gốc, KHÔNG phải direct)
url = "https://www.mediafire.com/file/tq38a4bszstqvry/htht.7z/file"

download_path = "/sdcard/Download/htht.7z"
extract_path = "/sdcard/Download/htht_game"

def ensure_storage_permission():
    try:
        subprocess.call(["termux-setup-storage"])
    except FileNotFoundError:
        print("⚠️ Lệnh termux-setup-storage không khả dụng ngoài Termux.")

def get_direct_mediafire(url):
    """
    Parse HTML trang Mediafire để lấy link direct từ nút download
    """
    print("🔍 Đang phân tích link Mediafire...")
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    button = soup.find("a", {"id": "downloadButton"})
    if button and "href" in button.attrs:
        return button["href"]
    else:
        raise Exception("❌ Không tìm thấy link download trong Mediafire")

def download_file(url, filename):
    response = requests.get(url, stream=True)
    total = int(response.headers.get('content-length', 0))
    with open(filename, 'wb') as file, tqdm(
        desc="⬇️ Đang tải file", total=total, unit='iB', unit_scale=True, unit_divisor=1024
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

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

    if not os.path.exists(download_path):
        print("📂 File chưa có sẵn, tiến hành tải từ Mediafire...")
        direct_url = get_direct_mediafire(url)
        print("✅ Link direct:", direct_url)
        download_file(direct_url, download_path)
    else:
        print("✅ Đã tìm thấy file htht.7z, bỏ qua bước tải.")

    print("📦 Đang giải nén game...")
    extract_file(download_path, extract_path)

    print(f"\n✅ Game đã được giải nén tại: {extract_path}")
    print("👉 Vui lòng mở file htht.apk trong thư mục này để cài đặt game.\n")

    input("📌 Sau khi cài xong htht.apk, nhấn Enter để tiếp tục...")

    run_sh("install.sh", extract_path)
    run_sh("menu.sh", extract_path)

if __name__ == "__main__":
    main()
