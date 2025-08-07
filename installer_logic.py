import os
import platform
import shutil
import subprocess
import json
import requests

PKG_INFO_URL = "https://raw.githubusercontent.com/David7ce/toolbox-installer-cli/refs/heads/main/pkgs/packages-info.json"

def load_package_info(file=None):
    if file:
        with open(file) as f:
            return json.load(f)
    else:
        response = requests.get(PKG_INFO_URL)
        response.raise_for_status()
        return response.json()

def detect_native_package_manager():
    system = platform.system()
    if system == "Windows":
        return "winget"
    elif system == "Darwin":
        return "brew"
    elif system == "FreeBSD":
        return "pkg"
    elif system == "Linux":
        for mgr in ["pacman", "apt", "dnf", "emerge", "xbps-install"]:
            if shutil.which(mgr):
                return mgr
    return None

def get_install_command(manager, package_name):
    commands = {
        "apt": f"sudo apt install -y {package_name}",
        "pacman": f"sudo pacman -S --noconfirm {package_name}",
        "dnf": f"sudo dnf install -y {package_name}",
        "emerge": f"sudo emerge {package_name}",
        "xbps-install": f"sudo xbps-install -y {package_name}",
        "brew": f"brew install {package_name}",
        "nix": f"nix-env -iA nixpkgs.{package_name}",
        "flatpak": f"flatpak install -y {package_name}",
        "winget": f"winget install --silent {package_name}",
        "pkg": f"sudo pkg install -y {package_name}",
    }
    return commands.get(manager)

def install_package(package_name, pkg_data, native_mgr, prefer=None, no_execute=False):
    pkg_entry = pkg_data.get(package_name, {})
    cmd = None

    # 1. Native manager first
    if native_mgr in pkg_entry:
        cmd = get_install_command(native_mgr, pkg_entry[native_mgr])
    # 2. If not available, fall back
    elif prefer and prefer in pkg_entry:
        cmd = get_install_command(prefer, pkg_entry[prefer])
    elif "flatpak" in pkg_entry:
        cmd = get_install_command("flatpak", pkg_entry["flatpak"])

    if cmd:
        print(f"📦 Installing {package_name} using {cmd.split()[0]}...")
        if no_execute:
            print(f"[Dry Run] ➜ {cmd}")
        else:
            result = subprocess.run(cmd, shell=True)
            if result.returncode == 0:
                print("✅ Success")
            else:
                print("❌ Failed")
    else:
        print(f"⚠️ No available installer for {package_name}")
