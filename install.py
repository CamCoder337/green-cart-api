#!/usr/bin/env python3
"""
Simple installer for Django Boilerplate CLI
Downloads and installs the CLI tool
"""

import sys
import subprocess
import urllib.request
import os
from pathlib import Path


def download_cli():
    """Download the CLI script."""
    cli_url = "https://raw.githubusercontent.com/votre-username/django-boilerplate/main/create_django_project.py"

    print("📥 Downloading Django Boilerplate CLI...")

    try:
        urllib.request.urlretrieve(cli_url, "create_django_project.py")

        # Make executable on Unix systems
        if os.name != 'nt':
            os.chmod("create_django_project.py", 0o755)

        print("✅ CLI downloaded successfully!")
        print("\n🚀 Usage:")
        print("python create_django_project.py myproject")
        print("\n📚 For more options:")
        print("python create_django_project.py --help")

        return True
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return False


def main():
    """Main installer function."""
    print("🚀 Django Boilerplate CLI Installer")
    print("=" * 40)

    # Check Python version
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ required")
        sys.exit(1)

    # Download CLI
    if download_cli():
        print("\n🎉 Installation completed!")
    else:
        print("\n❌ Installation failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()