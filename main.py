import os, subprocess, requests, zipfile, tarfile
import py7zr
from tqdm import tqdm
from colorama import Fore, init

init(autoreset=True)

def download_file(url, save_path):
    print(Fore.CYAN + f"Tải game từ {url}")
    r = requests.get(url, stream=True)
    total = int(r.headers.get('content-length', 0))
    with open(save_path, "wb") as f, tqdm(
        desc=save_path, total=total, unit="B", unit_scale=True, unit_divisor=1024
    ) as bar:
        for data in r.iter_content(chunk_size=1024):
            size = f.write(data)
            bar.update(size)
    print(Fore.GREEN + f"Đã tải về {save_path}")

def extract_file(path, extract_to):
    print(Fore.CYAN + f"Đang giải nén {path}")
    if path.endswith(".zip"):
        with zipfile.ZipFile(path, 'r') as z:
            z.extractall(extract_to)
    elif path.endswith(".tar.gz") or path.endswith(".tgz"):
        with tarfile.open(path, "r:gz") as t:
            t.extractall(extract_to)
    elif path.endswith(".7z"):
        with py7zr.SevenZipFile(path, 'r') as z:
            z.extractall(extract_to)
    else:
        print(Fore.RED + "Định dạng file không hỗ trợ.")
    print(Fore.GREEN + f"Đã giải nén vào {extract_to}")

def run_script(path, desc=""):
    if os.path.exists(path):
        try:
            print(Fore.YELLOW + f"{desc}: {path}")
            subprocess.call(["sh", path])
            return True
        except Exception as e:
            print(Fore.RED + f"Lỗi khi chạy {path}: {e}")
    else:
        print(Fore.RED + f"Không tìm thấy {path}")
    return False

def main():
    url = "https://www.mediafire.com/file/tq38a4bszstqvry/htht.7z/file"
    save_file = "htht.7z"
    download_dir = "/sdcard/Download/htht_game"

    if not os.path.exists(save_file):
        download_file(url, save_file)

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    extract_file(save_file, download_dir)

    apk_path = os.path.join(download_dir, "htht.apk")
    if os.path.exists(apk_path):
        print(Fore.GREEN + f"APK đã giải nén: {apk_path}")
        print(Fore.CYAN + "Đang mở thư mục Download...")
        try:
            subprocess.Popen(["xdg-open", "/sdcard/Download"])
        except Exception as e:
            print(Fore.RED + f"Không mở được thư mục: {e}")
    else:
        print(Fore.RED + "Không tìm thấy file htht.apk!")

    install_path = os.path.join(download_dir, "install.sh")
    menu_path = os.path.join(download_dir, "menu.sh")

    run_script(install_path, "Đang cài đặt game")
    run_script(menu_path, "Đang khởi động menu")

if __name__ == "__main__":
    print(Fore.MAGENTA + "=== Hệ thống khởi động Huyền Thoại Hải Tặc ===")
    main()
