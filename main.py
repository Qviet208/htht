import os, platform, subprocess, requests, zipfile, tarfile, shutil
import py7zr
from tqdm import tqdm
from colorama import Fore, Style, init

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
    game_dir = "game_data"

    if not os.path.exists(save_file):
        download_file(url, save_file)

    if not os.path.exists(game_dir):
        extract_file(save_file, game_dir)

    apk_path = os.path.abspath(os.path.join(game_dir, "htht.apk"))
    if os.path.exists(apk_path):
        print(Fore.GREEN + f"APK đã giải nén: {apk_path}")
        print(Fore.CYAN + "Hãy tự cài APK bằng lệnh trong Termux:")
        print(Fore.YELLOW + f"  adb install {apk_path}")
    else:
        print(Fore.RED + "Không tìm thấy file htht.apk trong gói game!")

    arch = platform.architecture()[0]
    if "32" in arch:
        folder = os.path.join(game_dir, "bin 32")
    else:
        folder = os.path.join(game_dir, "binx64")

    install_path = os.path.join(folder, "install.sh")
    menu_path = os.path.join(folder, "menu.sh")

    ok_install = run_script(install_path, "Đang cài đặt game")
    ok_menu = run_script(menu_path, "Đang khởi động menu")

    if not ok_install:
        run_script(os.path.join(game_dir, "install.sh"), "Fallback: cài đặt game")
    if not ok_menu:
        run_script(os.path.join(game_dir, "menu.sh"), "Fallback: khởi động menu")

if __name__ == "__main__":
    print(Fore.MAGENTA + "=== Hệ thống khởi động Huyền Thoại Hải Tặc ===")
    main()
