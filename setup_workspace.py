"""
Setup Script.

Use this script to cerate the user.email and user.name entries necessary in .gitconfig
This script will also link the current project into your Python environment.

NOTE: this script is intended to be run on the level 3 windows computers. Having said that it
should work on your personal computers (regardless of OS) but has not been tested on an OS other
than Windows.
"""
import sys
import json
import logging
import platform
from pathlib import Path
from subprocess import run
logging.basicConfig(level=logging.INFO, format="%(levelname)-7s : %(message)s")


logging.info("Starting script...")

logging.info("Detecting platform...")
SYSTEM = platform.system()
if not SYSTEM:
    logging.error("Couldn't determine the operating system")
    sys.exit(1)
logging.info("Found operating system: %s", 'MacOS' if SYSTEM == 'Darwin' else SYSTEM)

logging.info("GitHub information required")
name = input("Enter your name: ")
email = input("Enter the email address registered with GitHub: ")
run(['git', 'config', '--global', 'user.name', name], check=False, stdout=sys.stdout, stderr=sys.stderr)
run(['git', 'config', '--global', 'user.email', email], check=False, stdout=sys.stdout, stderr=sys.stderr)

logging.info("Linking current project into Python environment...")
run([sys.executable, "-m", "pip", "install", "--user", "-e", "."], check=False, stdout=sys.stdout, stderr=sys.stderr)

logging.info("Setup complete!")

logging.info("Hiding setup script from workspace...")
try:
    SETTINGS_FILE = Path('.vscode').joinpath("settings.json")
    with open(SETTINGS_FILE, "r", encoding='utf-8') as settings_file:
        settings = json.load(settings_file)

    settings["files.exclude"]['**/setup_workspace.py'] = True

    with open(SETTINGS_FILE, "w", encoding='utf-8') as settings_file:
        json.dump(settings, settings_file, indent=4)
    run(['git', 'update-index', '--assume-unchanged', str(SETTINGS_FILE)],
        check=False, stdout=sys.stdout, stderr=sys.stderr)
    logging.info("Setup script sucessfully hiden.")
except:  # noqa: E722  # pylint: disable=bare-except
    logging.error("Failed to hide setup script.")

logging.info("Script finished.")
logging.warning("Please re-launch the terminal for changes to take effect.")
