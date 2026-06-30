#!/usr/bin/env python3
import os
import stat
import sys

# Detect destination bin directory automatically
if os.path.exists("/data/data/com.termux"):
    BIN_DIR = "/data/data/com.termux/files/usr/bin"
else:
    BIN_DIR = "/usr/local/bin"

TEA_PATH = os.path.join(BIN_DIR, "tea")

# Fixed payload: Cleaned inner quotes to prevent SyntaxErrors
TEA_PAYLOAD = """#!/usr/bin/env python3
import sys, os, urllib.request, traceback, datetime

GLOBAL_REGISTRY_URL = "https://raw.githubusercontent.com/TeaInMud/Tea-Package-Manager/refs/heads/master/tpm/registry/tpm.reg.py"
LOG_DIR = os.path.expanduser("~/.tea")
LOG_FILE = os.path.join(LOG_DIR, "errors.log")

def log_error(err_type, message):
    os.makedirs(LOG_DIR, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {err_type}: {message}\\n")

def load_registry():
    global PACKAGES
    try:
        with urllib.request.urlopen(GLOBAL_REGISTRY_URL) as resp:
            exec(resp.read().decode('utf-8'), globals())
    except Exception as e: 
        log_error("RegistryFetchError", str(e))
        PACKAGES = {}

def download_custom_package(name):
    if not name or name not in PACKAGES:
        print(f"Package '{name}' not found in global registry.")
        return False
    url = PACKAGES[name]
    try:
        b_dir = "/data/data/com.termux/files/usr/bin" if os.path.exists("/data/data/com.termux") else "/usr/local/bin"
        target_path = os.path.join(b_dir, name)
        with urllib.request.urlopen(url) as resp:
            content = resp.read().decode('utf-8')
        with open(target_path, "w") as f: 
            f.write(content)
        os.chmod(target_path, 0o755)
        return True
    except Exception as e:
        print(f"Failed handling raw file download for {name}: {e}")
        log_error(f"DownloadError ({name})", traceback.format_exc().splitlines()[-1])
        return False

def main():
    load_registry()
    if len(sys.argv) < 2:
        print("TEA: tea add -c <name>   | tea add <pkg>")
        print("     tea update <name>   | tea update all")
        print("     tea search <query>  | tea list")
        return
    cmd = sys.argv[1]
    if cmd == "add" and len(sys.argv) > 2 and sys.argv[2] == "-c":
        name = sys.argv[3] if len(sys.argv) > 3 else None
        if download_custom_package(name):
            print(f"[OK] Installed {name}")
    elif cmd == "add": 
        fallback_system("add " + " ".join(sys.argv[2:]))
    elif cmd == "update":
        if len(sys.argv) < 3:
            print("Usage: tea update <custom-package-name> | tea update all")
            return
        target = sys.argv[2]
        if target == "all":
            print("Checking local binary directory for custom updates...")
            b_dir = "/data/data/com.termux/files/usr/bin" if os.path.exists("/data/data/com.termux") else "/usr/local/bin"
            updated_count = 0
            for pkg_name in PACKAGES:
                local_file = os.path.join(b_dir, pkg_name)
                if os.path.exists(local_file):
                    print(f"Updating {pkg_name}...")
                    if download_custom_package(pkg_name): updated_count += 1
            print(f"✨ Bulk update complete! Updated {updated_count} package(s).")
        else:
            print(f"Updating custom package '{target}'...")
            if download_custom_package(target):
                print(f"[OK] {target} successfully updated to the latest version!")
    elif cmd == "search":
        if len(sys.argv) < 3:
            print("Usage: tea search <package-name>")
            return
        query = sys.argv[2].lower()
        results = [pkg for pkg in PACKAGES if query in pkg.lower()]
        if results:
            print(f"Found {len(results)} package(s):")
            for pkg in sorted(results): print(f"  - {pkg}")
        else:
            print(f"No custom packages match '{query}'.")
    elif cmd == "list":
        if PACKAGES:
            print(f"Available custom packages ({len(PACKAGES)}):")
            for pkg in sorted(PACKAGES): print(f"  - {pkg}")
        else:
            print("The global registry is empty or couldn't be loaded.")
    else: 
        fallback_system(cmd + " " + " ".join(sys.argv[2:]))

def fallback_system(full_args):
    if os.path.exists("/data/data/com.termux"):
        os.system(f"pkg {full_args}")
    else:
        os.system(f"apk {full_args}")

if __name__ == '__main__': 
    main()
"""

# Write and set permissions
os.makedirs(BIN_DIR, exist_ok=True)
with open(TEA_PATH, "w") as f:
    f.write(TEA_PAYLOAD)

os.chmod(TEA_PATH, os.stat(TEA_PATH).st_mode | stat.S_IEXEC)
print("[OK] Tea has been successfully deployed globally!")
