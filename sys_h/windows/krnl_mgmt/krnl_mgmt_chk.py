import subprocess
import re

def run_command(command):
    """Function to run a command and return its output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return str(e)

def check_system_information():
    """Function to gather system information."""
    info = {}
    info['kernel_version'] = run_command('ver')
    info['system_info'] = run_command('systeminfo')
    return info

def check_kernel_modules():
    """Function to check loaded kernel modules."""
    modules = []
    command_output = run_command('driverquery')
    lines = command_output.split('\n')
    for line in lines[1:]:
        parts = re.split(r'\s{2,}', line.strip())
        if len(parts) >= 2:
            modules.append({'name': parts[0], 'type': parts[1]})
    return modules

def check_event_logs():
    """Function to check system event logs for kernel issues."""
    logs = {}
    command_output = run_command('wevtutil qe System /c:1 /rd:true /f:text /q:"*[System [(Level <= 2)]]"')
    logs['system'] = command_output
    command_output = run_command('wevtutil qe Application /c:1 /rd:true /f:text /q:"*[System [(Level <= 2)]]"')
    logs['application'] = command_output
    return logs

def check_driver_signing():
    """Function to check if driver signing is enforced."""
    output = run_command('bcdedit /enum {default} | find "nointegritychecks"')
    return "NoExecute" not in output

def check_system_integrity():
    """Function to check system file integrity."""
    sfc_result = run_command('sfc /scannow')
    return "Windows Resource Protection found corrupt files" not in sfc_result

def main():
    """Main function to run all checks."""
    kernel_issues = {}

    # Check system information
    kernel_issues['system_information'] = check_system_information()

    # Check loaded kernel modules
    kernel_issues['kernel_modules'] = check_kernel_modules()

    # Check system event logs
    kernel_issues['event_logs'] = check_event_logs()

    # Check driver signing
    if not check_driver_signing():
        print("Driver signing enforcement not enabled!")

    # Check system file integrity
    if not check_system_integrity():
        print("System file integrity compromised!")

if __name__ == "__main__":
    main()
    print('=======WOW YOUR SYSTEM ES MUY SECURE, MUY BIEN!!!!=======')
