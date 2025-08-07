# 📦 Toolbox Installer CLI

> Cross-platform, cross-distro package installer that prioritizes your native system manager — with intelligent fallback to Flatpak, Brew, or Nix.

## ✅ Features

✅ Detects your OS and native package manager (apt, pacman, dnf, winget, brew, etc.)
✅ Installs only via your native manager by default
✅ If package is missing → auto-installs from Flatpak
✅ Optional: --prefer flatpak|brew|nix to override behavior
✅ Interactive checkbox UI for package selection
✅ Support for import/export of package lists
✅ Dry-run mode with --no-execute to preview commands
✅ Designed for Linux, macOS, Windows, and BSD


## 🛠 Install

Clone the repo and install locally:

git clone https://github.com/David7ce/toolbox-installer-cli.git
cd toolbox-installer-cli
pip install .

> This will make the toolbox command globally available.


## 🚀 Usage

toolbox [OPTIONS]

Interactive CLI (default)

toolbox

Presents you with a checkbox list of tools to install

Installs with native package manager, falling back to Flatpak


## 🔧 Options

Flag	Description

`--prefer flatpak	brew
--import FILE	Import a list of package names to install from JSON
--export FILE	Export selected packages to JSON
--file FILE	Use a custom JSON file for package mappings
--no-execute	Dry-run mode — print install commands, don't run them


### 📁 Example packages-info.json Format

{
  "vlc": {
    "apt": "vlc",
    "dnf": "vlc",
    "pacman": "vlc",
    "flatpak": "org.videolan.VLC",
    "brew": "vlc",
    "winget": "VideoLAN.VLC",
    "nix": "vlc",
    "category": "Media"
  }
}

By default, the CLI fetches this from:

https://raw.githubusercontent.com/David7ce/toolbox-installer-cli/refs/heads/main/pkgs/packages-info.json

You can override it with --file.


### 🔄 Example Workflows

```sh
## Install with preferred fallback:
toolbox --prefer flatpak

## Export selected tools to JSON:
toolbox --export mytools.json

## Import and install from JSON:
toolbox --import mytools.json

## Simulate actions (dry-run):
toolbox --no-execute
```

---

### 🧭 Supported Operating Systems & Package Managers

| OS / Distro Family   | Native Package Manager |
|----------------------|------------------------|
| **Windows**          | `winget`               |
| **macOS**            | `brew`                 |
| **FreeBSD**          | `pkg`                  |
| **Debian-based**     | `apt`                  |
| **Arch-based**       | `pacman`               |
| **Fedora-based**     | `dnf`                  |
| **Gentoo-based**     | `emerge`               |
| **Void-based**       | `xbps-install`         |
| **NixOS**            | `nix-env`              |
| **Other Linux**      | _Best match auto-detected_ |

> 🔁 If a package is unavailable in your native manager, the CLI falls back to **Flatpak** (or `brew`/`nix` if preferred via `--prefer`).

---

## 🧪 Development

To run locally:

```python
python -m toolbox_installer.cli --no-execute
```

---

### ⚠️ Notes

sudo is used automatically for Linux/Unix systems — make sure you trust the commands being run.

Package names vary between distros — ensure packages-info.json is complete and accurate.

Flatpak support assumes Flatpak is installed and set up.
