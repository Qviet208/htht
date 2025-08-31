import os, platform, subprocess, requests, zipfile, tarfile, shutil
import py7zr

def download_file(url, save_path):
    print(f"▶ Đang tải game từ {url}")
    r = requests.get(url, stream=True)
    with open(save_path, "wb") as f:
        shutil.copyfileobj(r.raw, f)
    print(f"✔ Đã tải về {save_path}")

def extract_file(path, extract_to):
    print(f"▶ Đang giải nén {path}")
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
        print("⚠ Định dạng file không hỗ trợ.")
    print(f"✔ Đã giải nén vào {extract_to}")

def run_script(path, desc=""):
    if os.path.exists(path):
        try:
            print(f"▶ {desc} -> {path}")
            subprocess.call(["bash", path])
            return True
        except Exception as e:
            print(f"Lỗi khi chạy {path}: {e}")
    else:
        print(f"⚠ Không tìm thấy {path}")
    return False

def main():
    url = "https://www.mediafire.com/file/tq38a4bszstqvry/htht.7z/file"
    save_file = "htht.7z"
    game_dir = "game_data"

    if not os.path.exists(save_file):
        download_file(url, save_file)

    if not os.path.exists(game_dir):
        extract_file(save_file, game_dir)

    print("✔ Giải nén xong, hãy tự cài đặt file htht.apk trong thư mục game_data")

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
    print("=== Hệ thống khởi động Huyền Thoại Hải Tặc ===")
    main()

