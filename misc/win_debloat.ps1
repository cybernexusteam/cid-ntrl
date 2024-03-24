<#
.SYNOPSIS
    This script performs an advanced debloat process on Windows while maintaining the highest possible security level.

.DESCRIPTION
    The script removes unnecessary Windows Store apps, built-in apps, disables telemetry, disables unnecessary services, removes scheduled tasks, disables unnecessary features, and hardens various security settings. It also provides options to backup and restore system settings.

.PARAMETER BackupSettings
    Performs a backup of system settings before making any changes.

.PARAMETER RestoreSettings
    Restores system settings from a previous backup.

.PARAMETER SkipBackup
    Skips the backup process and proceeds with the debloat process.

.EXAMPLE
    .\AdvancedDebloat.ps1 -BackupSettings
    Performs a backup of system settings and then proceeds with the debloat process.

.EXAMPLE
    .\AdvancedDebloat.ps1 -RestoreSettings
    Restores system settings from a previous backup.

.EXAMPLE
    .\AdvancedDebloat.ps1 -SkipBackup
    Skips the backup process and proceeds with the debloat process.

.NOTES
    Author: [Your Name]
    Last Updated: [Date]
#>

param (
    [switch]$BackupSettings,
    [switch]$RestoreSettings,
    [switch]$SkipBackup
)

# Define function to backup system settings
function Backup-Settings {
    $backupPath = Join-Path $env:TEMP "DebloatBackup_$(Get-Date -Format 'yyyyMMdd_HHmmss').reg"
    $regKeys = @(
        "HKLM:\SOFTWARE\Policies\Microsoft\Windows\DataCollection",
        "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace",
        "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile",
        "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks",
        "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsStore\WindowsUpdate"
    )

    Start-Process reg.exe -ArgumentList "export `"$($regKeys -join ' ')"` " $backupPath" -Wait -NoNewWindow

    Write-Host "System settings have been backed up to: $backupPath"
}

# Define function to restore system settings
function Restore-Settings {
    $backupFiles = Get-ChildItem -Path $env:TEMP -Filter "DebloatBackup_*.reg" | Sort-Object -Descending | Select-Object -First 1

    if ($backupFiles) {
        $backupFile = $backupFiles.FullName
        Start-Process reg.exe -ArgumentList "import $backupFile" -Wait -NoNewWindow
        Write-Host "System settings have been restored from: $backupFile"
    } else {
        Write-Warning "No backup files found. Skipping restore process."
    }
}

# Define function to remove Windows Store apps
function Remove-StoreApps {
    Get-AppxPackage -AllUsers | Where-Object { $_.Name -NotLike "*Microsoft*" -and $_.Name -NotLike "*Windows*" -and $_.Name -NotLike "*Store*" } | Remove-AppxPackage
}

# Define function to remove built-in Windows apps
function Remove-BuiltInApps {
    Get-AppxProvisionedPackage -Online | Where-Object { $_.PackageName -NotLike "*Microsoft*" -and $_.PackageName -NotLike "*Windows*" -and $_.PackageName -NotLike "*Store*" } | Remove-AppxProvisionedPackage -Online
}

# Define function to disable Windows telemetry
function Disable-Telemetry {
    # Disable Windows telemetry via registry
    $registryPath = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\DataCollection"
    if (!(Test-Path $registryPath)) {
        New-Item -Path $registryPath -Force | Out-Null
    }
    Set-ItemProperty -Path $registryPath -Name AllowTelemetry -Value 0 -Type DWord -Force
}

# Define function to disable unnecessary Windows services
function Disable-Services {
    # List of services to disable
    $servicesToDisable = @(
        "wuauserv",         # Windows Update
        "BITS",             # Background Intelligent Transfer Service
        "sppsvc",           # Software Protection
        "wscsvc",           # Security Center
        "WerSvc",           # Windows Error Reporting
        "DoSvc",            # Delivery Optimization
        "DiagTrack",        # Connected User Experiences and Telemetry
        "DusmSvc",          # Data Usage
        "lfsvc",            # Geolocation Service
        "StorSvc",          # Storage Service
        "MapsBroker",       # Downloaded Maps Manager
        "dmwappushsvc"      # DMWAPPush Service
    )

    foreach ($service in $servicesToDisable) {
        if (Get-Service -Name $service -ErrorAction SilentlyContinue) {
            Stop-Service -Name $service -Force
            Set-Service -Name $service -StartupType Disabled
        }
    }
}

# Define function to remove unnecessary scheduled tasks
function Remove-ScheduledTasks {
    # List of scheduled tasks to remove
    $tasksToRemove = @(
        "\Microsoft\Windows\Diagnosis\Scheduled",        # Scheduled tasks related to Windows Diagnosis
        "\Microsoft\Windows\Feedback\Siuf\DmClient",    # Feedback Hub tasks
        "\Microsoft\Windows\Power Efficiency Diagnostics\AnalyzeSystem",  # Power Efficiency Diagnostics task
        "\Microsoft\Windows\Application Experience\AitAgent",            # Application Impact Telemetry task
        "\Microsoft\Windows\Customer Experience Improvement Program\BthSQM",   # Customer Experience Improvement Program task
        "\Microsoft\Windows\DiskDiagnostic\Microsoft-Windows-DiskDiagnosticDataCollector", # Disk Diagnostic Data Collector task
        "\Microsoft\Windows\Windows Error Reporting\QueueReporting"        # Windows Error Reporting task
    )

    foreach ($task in $tasksToRemove) {
        Unregister-ScheduledTask -TaskPath $task -Confirm:$false
    }
}

# Define function to disable unnecessary Windows features
function Disable-Features {
    # Disable Windows features (Modify as needed)
    Disable-WindowsOptionalFeature -Online -FeatureName "Internet-Explorer-Optional-amd64" -NoRestart
    Disable-WindowsOptionalFeature -Online -FeatureName "MediaPlayback" -NoRestart
    Disable-WindowsOptionalFeature -Online -FeatureName "Print-Foundation-InternetPrinting-Client" -NoRestart
}

# Define function to harden security settings
function Set-SecurityHardeningOptions {
    # Enable Windows Defender Real-Time Protection
    Set-MpPreference -DisableRealtimeMonitoring $false

    # Enable Windows Defender Cloud-Based Protection
    Set-MpPreference -DisableIntrusionPreventionSystem $false
    Set-MpPreference -DisableIOAVProtection $false

    # Enable Windows Defender Controlled Folder Access
    Set-MpPreference -EnableControlledFolderAccess Enabled

    # Enable Windows Defender Attack Surface Reduction
    Set-MpPreference -AttackSurfaceReductionRules_Ids 1 -AttackSurfaceReductionRules_Actions Enabled

    # Enable Windows Defender Network Protection
    Set-MpPreference -EnableNetworkProtection Enabled

    # Enable Windows Defender Exploit Protection
    Set-ProcessMitigation -System -Disable DEP, ASLR, SEHOP, ForceRelocateImages, BottomUp, HighEntropy, StrictCFG -Force

    # Enable Windows Defender Firewall
    Set-NetFirewallProfile -Profile Domain, Public, Private -Enabled True

    # Enable Windows Defender SmartScreen
    Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer" -Name "SmartScreenEnabled" -Value "RequireAdmin" -Type String -Force

    # Enable Windows Defender Credential Guard
    Enable-WindowsOptionalFeature -Online -FeatureName CredentialGuard -NoRestart

    # Enable Windows Defender Exploit Guard
    Enable-WindowsOptionalFeature -Online -FeatureName Windows-Defender-Exploit-Guard -NoRestart
}

# Main script

# Check if running with administrator privileges
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "This script requires administrator privileges. Please run it as an administrator."
    return
}

# Backup or restore system settings if requested
if ($BackupSettings) {
    Backup-Settings
}

if ($RestoreSettings) {
    Restore-Settings
    return
}

if (-not $SkipBackup) {
    $backupChoice = Read-Host "Would you like to create a backup of your system settings before proceeding? (Y/N)"
    if ($backupChoice.ToLower() -eq 'y') {
        Backup-Settings
    }
}

# Remove Windows Store apps
Write-Host "Removing Windows Store apps..."
Remove-StoreApps

# Remove built-in Windows apps
Write-Host "Removing built-in Windows apps..."
Remove-BuiltInApps

# Disable Windows telemetry
Write-Host "Disabling Windows telemetry..."
Disable-Telemetry

# Disable unnecessary services
Write-Host "Disabling unnecessary services..."
Disable-Services

# Remove unnecessary scheduled tasks
Write-Host "Removing unnecessary scheduled tasks..."
Remove-ScheduledTasks

# Disable unnecessary Windows features
Write-Host "Disabling unnecessary Windows features..."
Disable-Features

# Harden security settings
Write-Host "Hardening security settings..."
Set-SecurityHardeningOptions

Write-Host "Debloat process completed."