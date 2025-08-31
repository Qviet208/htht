import os
import requests
import subprocess
from tqdm import tqdm

# Link Mediafire (link public dạng /file/xxx/file chứ không phải direct)
url = "https://download1478.mediafire.com/rdtmd023udygbjDOL3FpCN5hZNEK9WLmh6Ra432mO14R3g-ldvdrcazDMchZ8fC14yHHILJZchlyralnyaBGT_sQ3Izi4219lxeYdEA7gBHgPGRP1XPzfp-a9kZ_p5aB0JC73tqJRoal3tdG9xHv3AnRFG6KDjqMLNmcFsDgvFM_Wg/tq38a4bszstqvry/htht.7z"

download_path = "/sdcard/Download/htht.7z"
extract_path = "/sdcard/Download/htht_game"

def ensure_storage_permission():
    try:
        subprocess.call(["termux-setup-storage"])
    except FileNotFoundError:
        print("⚠️ Lệnh termux-setup-storage không khả dụng ngoài Termux.")

def get_direct_mediafire(url):
    """
    Lấy link tải trực tiếp từ Mediafire bằng cách follow redirect
    """
    session = requests.Session()
    resp = session.get(url, allow_redirects=True)
    # Mediafire thường trả về link thật trong resp.url
    return resp.url

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
    # Dùng 7z CLI thay vì py7zr để tránh lỗi build
    os.makedirs(path, exist_ok=True)
    subprocess.run(["7z", "x", filename, f"-o{path}", "-y"], check=True)

def run_sh(script, path):
    script_path = os.path.join(path, script)
    if os.path.exists(script_path):
        subprocess.call(["sh", script_path])
    else:
        print(f"⚠️ Không tìm thấy {script}")

def main():
    ensure_storage_permission()

    print("🔍 Lấy link tải trực tiếp từ Mediafire...")
    direct_url = get_direct_mediafire(url)
    print("✅ Link direct:", direct_url)

    print("⬇️ Đang tải game...")
    download_file(direct_url, download_path)

    print("📦 Đang giải nén game...")
    extract_file(download_path, extract_path)

    print(f"\n✅ Game đã được giải nén tại: {extract_path}")
    print("👉 Vui lòng mở file htht.apk trong thư mục này để cài đặt game.\n")

    input("📌 Sau khi cài xong htht.apk, nhấn Enter để tiếp tục...")

    run_sh("install.sh", extract_path)
    run_sh("menu.sh", extract_path)

if __name__ == "__main__":
    main()
