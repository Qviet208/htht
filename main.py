import os
import requests
import py7zr
import subprocess
from tqdm import tqdm

DOWNLOAD_DIR = "/sdcard/Download"
GAME_DIR = os.path.join(DOWNLOAD_DIR, "htht_game")
ARCHIVE_PATH = os.path.join(DOWNLOAD_DIR, "htht.7z")

# Link tải game (bạn có thể đổi tuỳ ý)
GAME_URL = "https://www.mediafire.com/file/tq38a4bszstqvry/htht.7z/file"

def download_file(url, dest):
    response = requests.get(url, stream=True)
    total = int(response.headers.get('content-length', 0))
    with open(dest, 'wb') as file, tqdm(
        desc="Đang tải game",
        total=total,
        unit='B',
        unit_scale=True,
        unit_divisor=1024
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

def extract_archive(archive_path, extract_to):
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)
    with py7zr.SevenZipFile(archive_path, mode='r') as archive:
        archive.extractall(path=extract_to)

def run_script(script_name):
    script_path = os.path.join(GAME_DIR, script_name)
    if os.path.exists(script_path):
        subprocess.call(["bash", script_path])
    else:
        print(f"Không tìm thấy {script_name}")

def main():
    print("=== Huyền Thoại Hải Tặc ===")

    # Bước 1: tải game
    if not os.path.exists(ARCHIVE_PATH):
        print("Bắt đầu tải game...")
        download_file(GAME_URL, ARCHIVE_PATH)
    else:
        print("Đã có file game, bỏ qua bước tải.")

    # Bước 2: giải nén
    print("Đang giải nén game...")
    extract_archive(ARCHIVE_PATH, GAME_DIR)

    # Bước 3: chạy install.sh
    print("Chạy install.sh...")
    run_script("install.sh")

    # Bước 4: chạy menu.sh
    print("Chạy menu.sh...")
    run_script("menu.sh")

if __name__ == "__main__":
    main()
