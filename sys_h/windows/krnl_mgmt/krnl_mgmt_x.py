import subprocess
import re
import os

def run_command(command):
    """Function to run a command and return its output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return str(e)

def fix_driver_signing():
    """Function to enable driver signing."""
    try:
        subprocess.run('bcdedit /set nointegritychecks off', shell=True, check=True)
        print("Driver signing enforcement is enabled.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to enable driver signing: {e}")

def fix_system_integrity():
    """Function to fix system file integrity issues."""
    try:
        subprocess.run('sfc /scannow', shell=True, check=True)
        print("System file integrity has been restored.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to fix system file integrity: {e}")

def main():
    """Main function to fix all identified issues."""
    # Fix driver signing
    fix_driver_signing()

    # Fix system file integrity
    fix_system_integrity()

if __name__ == "__main__":
    main()
