import os
import platform
import subprocess

def detect_platform():
    sys = platform.system()
    if sys == "Windows":
        return {"os": "windows", "manager": "winget"}
    elif sys == "Darwin":
        return {"os": "macos", "manager": "brew"}
    elif sys == "FreeBSD":
        return {"os": "freebsd", "manager": "pkg"}
    elif sys == "Linux":
        # Orden de preferencia para distros Linux
        if shutil.which("pacman"):
            return {"os": "linux", "manager": "pacman"}
        if shutil.which("apt"):
            return {"os": "linux", "manager": "apt"}
        if shutil.which("dnf"):
            return {"os": "linux", "manager": "dnf"}
        if shutil.which("yum"):
            return {"os": "linux", "manager": "dnf"}  # Fedora/Red Hat
        if shutil.which("emerge"):
            return {"os": "linux", "manager": "emerge"}
        if shutil.which("nix-env"):
            return {"os": "linux", "manager": "nix-env"}
        if shutil.which("xbps-install"):
            return {"os": "linux", "manager": "xbps-install"}
        # Si no detecta ninguno, usar flatpak
        return {"os": "linux", "manager": "flatpak"}
    else:
        return {"os": "unknown", "manager": "flatpak"}

def build_install_commands(selection, packages, manager):
    cmds = []
    pkg_lookup = {p['name']: p for group in packages.values() for p in group}
    for name in selection:
        pkg = pkg_lookup.get(name)
        if not pkg:
            continue
        cmd = pkg.get("install", {}).get(manager)
        if not cmd:
            # Si no tiene para ese gestor, usa flatpak si está
            cmd = pkg.get("install", {}).get("flatpak")
            if cmd:
                cmds.append(f"# No disponible para {manager}, usando Flatpak\n{cmd}")
            else:
                cmds.append(f"# No disponible para {manager} ni Flatpak: {name}")
        else:
            cmds.append(cmd)
    return cmds
