import argparse
import inquirer
from .installer_logic import (
    detect_native_package_manager,
    load_package_info,
    install_package,
)

def select_packages(pkg_data):
    choices = []
    for pkg in sorted(pkg_data.keys()):
        category = pkg_data[pkg].get("category", "Misc")
        label = f"{pkg} [{category}]"
        choices.append((label, pkg))

    questions = [
        inquirer.Checkbox(
            "selected",
            message="Select packages to install",
            choices=choices,
        )
    ]
    answers = inquirer.prompt(questions)
    return answers["selected"] if answers else []

def export_packages(packages, file):
    with open(file, "w") as f:
        json.dump({"packages": packages}, f, indent=2)
    print(f"📤 Exported package list to {file}")

def import_packages(file):
    with open(file) as f:
        data = json.load(f)
        return data.get("packages", [])

def main():
    parser = argparse.ArgumentParser(description="📦 Toolbox Installer CLI")
    parser.add_argument("--prefer", choices=["flatpak", "brew", "nix"], help="Preferred universal package manager")
    parser.add_argument("--import", dest="import_file", help="Import package list from file")
    parser.add_argument("--export", dest="export_file", help="Export selected packages to file")
    parser.add_argument("--file", help="Use a local JSON file instead of the default")
    parser.add_argument("--no-execute", action="store_true", help="Dry-run mode (print commands only)")

    args = parser.parse_args()

    pkg_data = load_package_info(args.file)
    native_mgr = detect_native_package_manager()

    if not native_mgr:
        print("❌ Could not detect native package manager")
        return

    if args.import_file:
        selected_packages = import_packages(args.import_file)
    else:
        selected_packages = select_packages(pkg_data)

    if args.export_file:
        export_packages(selected_packages, args.export_file)

    for pkg in selected_packages:
        install_package(pkg, pkg_data, native_mgr, prefer=args.prefer, no_execute=args.no_execute)
