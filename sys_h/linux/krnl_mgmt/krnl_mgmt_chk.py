import subprocess

def check_kernel():
    # Initialize an empty dictionary to store potential issues
    kernel_issues = {}

    # Check the current kernel version
    kernel_version = subprocess.check_output(["uname", "-r"]).decode().strip()
    kernel_issues["Kernel Version"] = kernel_version

    # Check for available updates using apt
    try:
        updates_available = subprocess.check_output(["apt", "list", "--upgradable"]).decode()
        if "linux-image" in updates_available or "linux-headers" in updates_available:
            kernel_issues["Available Updates"] = updates_available
    except subprocess.CalledProcessError:
        kernel_issues["Available Updates"] = "Failed to check for updates."

    # Check for any loaded kernel modules
    loaded_modules = subprocess.check_output(["lsmod"]).decode()
    kernel_issues["Loaded Kernel Modules"] = loaded_modules

    # Check for kernel command line parameters
    kernel_cmdline = subprocess.check_output(["cat", "/proc/cmdline"]).decode().strip()
    kernel_issues["Kernel Command Line Parameters"] = kernel_cmdline

    # Check for any dmesg errors
    dmesg_output = subprocess.check_output(["dmesg", "-T"]).decode()
    if "error" in dmesg_output.lower() or "warning" in dmesg_output.lower():
        kernel_issues["dmesg Output"] = dmesg_output

    return kernel_issues

if __name__ == "__main__":
    kernel_issues = check_kernel()
    print("Potential kernel issues:")
    for key, value in kernel_issues.items():
        print(f"{key}:")
        print(value)
        print("-" * 50)
