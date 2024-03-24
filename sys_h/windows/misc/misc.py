import subprocess

def run_powershell_command(command):
    """Function to execute PowerShell commands."""
    try:
        subprocess.run(["powershell", "-Command", command], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing PowerShell command: {command}")
        print(e)
        return False

def disable_remote_access():
    """Disable Remote Access."""
    if run_powershell_command("Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server' -Name fDenyTSConnections -Value 1"):
        print("Good Job! Your device had Remote Access Disabled already!")
    else:
        run_powershell_command("Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server' -Name fDenyTSConnections -Value 1")
        print("Remote Access Disabled!")

def remove_powershell_v2():
    """Remove PowerShell version 2.0 or earlier."""
    if run_powershell_command("Get-WindowsFeature -Name PowerShell-V2"):
        run_powershell_command("Uninstall-WindowsFeature -Name PowerShell-V2")
        print("PowerShell version 2.0 or earlier Removed!")
    else:
        print("PowerShell version 2.0 or earlier already Removed!")

def set_powershell_constrained_mode():
    """Set PowerShell to Constrained Language Mode."""
    if run_powershell_command("Set-ExecutionPolicy -ExecutionPolicy Restricted -Scope LocalMachine -Force"):
        print("Good Job! Your device had PowerShell set to Constrained Language Mode already!")
    else:
        run_powershell_command("Set-ExecutionPolicy -ExecutionPolicy Restricted -Scope LocalMachine -Force")
        print("PowerShell set to Constrained Language Mode!")

def enable_powershell_logging():
    """Enable PowerShell logging."""
    if not run_powershell_command("Get-Item -Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\PowerShell' -Name ScriptBlockLogging"):
        run_powershell_command("New-Item -Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\PowerShell' -Name ScriptBlockLogging -Force")
        run_powershell_command("Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\PowerShell' -Name EnableScriptBlockLogging -Value 1 -Force")
        print("PowerShell logging enabled!")
    else:
        print("PowerShell logging already enabled!")

def set_execution_policy():
    """Set execution policy."""
    if run_powershell_command("Get-ExecutionPolicy -List | Select-Object -ExpandProperty Scope | Where-Object { $_ -eq 'LocalMachine' }"):
        print("Good Job! Your device had Execution Policy already set!")
    else:
        run_powershell_command("Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine -Force")
        print("Execution Policy set!")

def enable_auto_updates():
    """Enable Auto-Updates."""
    if run_powershell_command("Get-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\WindowsUpdate\\Auto Update' -Name AUOptions"):
        print("Good Job! Your device had Auto-Updates enabled already!")
    else:
        run_powershell_command("Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\WindowsUpdate\\Auto Update' -Name AUOptions -Value 4")
        print("Auto-Updates enabled!")

def disable_guest_account():
    """Disable Guest Account."""
    if not run_powershell_command("Get-LocalUser -Name Guest"):
        run_powershell_command("Disable-LocalUser -Name Guest")
        print("Guest Account Disabled!")
    else:
        print("Guest Account already Disabled!")

def enable_ctrl_alt_del_requirement():
    """Enable ctrl+alt+del requirement."""
    if run_powershell_command("Get-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Name DisableCAD"):
        print("Good Job! Your device had ctrl+alt+del requirement enabled already!")
    else:
        run_powershell_command("Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Name DisableCAD -Value 0")
        print("ctrl+alt+del requirement enabled!")

def enable_password_policy():
    """Enable and configure password policy to standard levels."""
    if not run_powershell_command("Get-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Name MaximumPasswordAge"):
        run_powershell_command("New-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Name MaximumPasswordAge -Value 30")
        print("Maximum Password Age configured!")
    else:
        print("Maximum Password Age already configured!")

    if not run_powershell_command("Get-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Name MinimumPasswordLength"):
        run_powershell_command("New-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Name MinimumPasswordLength -Value 8")
        print("Minimum Password Length configured!")
    else:
        print("Minimum Password Length already configured!")

    if not run_powershell_command("Get-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Name MinimumPasswordAge"):
        run_powershell_command("New-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Name MinimumPasswordAge -Value 7")
        print("Minimum Password Age configured!")
    else:
        print("Minimum Password Age already configured!")

    if not run_powershell_command("Get-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Name PasswordHistorySize"):
        run_powershell_command("New-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Name PasswordHistorySize -Value 1")
        print("Password History Size configured!")
    else:
        print("Password History Size already configured!")
def enable_lockout_policy():
    """Enable and configure Lockout policy to standard levels."""
    if not run_powershell_command("Get-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Name LockoutBadCount"):
        run_powershell_command("New-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Name LockoutBadCount -Value 5")
        print("Lockout Bad Count configured!")
    else:
        print("Lockout Bad Count already configured!")

    if not run_powershell_command("Get-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Name ResetLockoutCount"):
        run_powershell_command("New-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Name ResetLockoutCount -Value 30")
        print("Reset Lockout Count configured!")
    else:
        print("Reset Lockout Count already configured!")

    if not run_powershell_command("Get-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Name LockoutDuration"):
        run_powershell_command("New-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System' -Name LockoutDuration -Value 30")
        print("Lockout Duration configured!")
    else:
        print("Lockout Duration already configured!")

if __name__ == "__main__":
    disable_remote_access()
    remove_powershell_v2()
    set_powershell_constrained_mode()
    enable_powershell_logging()
    set_execution_policy()
    enable_auto_updates()
    disable_guest_account()
    enable_ctrl_alt_del_requirement()
    enable_password_policy()
    enable_lockout_policy()
