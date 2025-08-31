import zlib, base64, os, requests, subprocess, platform, py7zr

def dec(s: str) -> str:
    return zlib.decompress(base64.b64decode(s)).decode()

GAME_URL   = dec("eJyrVkosyczPz0ksSU1VyM+zU9JRyE9VcMsvz89T0lFQ0lFKLEnMz1PIz0ksyUhVslIKLUnMycxJzEvXUYpVSMxLBQCS+RUM")
GAME_FILE  = dec("eJwrTi0uzszPS8zJBgABawHh")
APK_FILE   = dec("eJwrTk0tSkzPTczJBgCvPgbF")
INSTALL_SH = dec("eJwrzi8tSk0sKcrMSwcA3P4GAg==")
MENU_SH    = dec("eJwrTi0uzszPS8zJBwCyHQer")

def find_file(filename, search_path="."):
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return None

def download_game():
    if not os.path.exists(GAME_FILE):
        print("📥 Đang tải game...")
        r = requests.get(GAME_URL, allow_redirects=True)
        with open(GAME_FILE, "wb") as f:
            f.write(r.content)
        print("✅ Tải xong!")

def extract_game():
    if GAME_FILE.endswith(".7z"):
        with py7zr.SevenZipFile(GAME_FILE, "r") as archive:
            archive.extractall(".")
        print("📂 Đã giải nén game!")

def install_apk():
    apk_path = find_file(APK_FILE)
    if apk_path:
        print(f"🚀 Đang cài {apk_path} ...")
        system = platform.system()
        if system == "Windows":
            print("⚠️ Windows cần giả lập Android + adb install htht.apk")
        elif system in ["Linux", "Darwin"]:
            subprocess.call(["adb", "install", "-r", apk_path])
        else:
            print("❌ Không xác định hệ điều hành!")
    else:
        print(f"❌ Không tìm thấy {APK_FILE}")

def run_install():
    script_path = find_file(INSTALL_SH)
    if script_path:
        print(f"⚙️ Đang chạy {script_path}...")
        subprocess.call(["bash", script_path])
    else:
        print("❌ Không tìm thấy install.sh")

def run_menu():
    script_path = find_file(MENU_SH)
    if script_path:
        print(f"▶️ Đang chạy {script_path}...")
        subprocess.call(["bash", script_path])
    else:
        print("❌ Không tìm thấy menu.sh")

if __name__ == "__main__":
    download_game()
    extract_game()
    install_apk()
    run_install()
    run_menu()
