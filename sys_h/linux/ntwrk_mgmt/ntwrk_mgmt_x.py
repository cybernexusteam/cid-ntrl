import subprocess
from ntwrk_mgmt_chk import main

def fix_firewall_issues(issues):
    print("Fixing firewall issues...")
    # Installing iptables lmao
    subprocess.run(["sudo", "apt-get", "install", "iptables", "-y"])
    # Example: Allow incoming SSH traffic
    subprocess.run(["iptables", "-A", "INPUT", "-p", "tcp", "--dport", "22", "-j", "ACCEPT"])
    # Example: Allow incoming HTTP and HTTPS traffic
    subprocess.run(["iptables", "-A", "INPUT", "-p", "tcp", "--dport", "80", "-j", "ACCEPT"])
    subprocess.run(["iptables", "-A", "INPUT", "-p", "tcp", "--dport", "443", "-j", "ACCEPT"])
    # Example: Enable outgoing DNS traffic
    subprocess.run(["iptables", "-A", "OUTPUT", "-p", "udp", "--dport", "53", "-j", "ACCEPT"])
    print("Firewall issues fixed.")

def fix_ssh_issues(issues):
    print("Fixing SSH hardening issues...")
    # Disable root login and password authentication
    with open("/etc/ssh/sshd_config", "a") as ssh_config_file:
        ssh_config_file.write("\nPermitRootLogin no\nPasswordAuthentication no\n")
    # Set SSH protocol version to 2
    subprocess.run(["sed", "-i", "/^#?Protocol/s/.*/Protocol 2/", "/etc/ssh/sshd_config"])
    # Reload SSH daemon to apply changes
    subprocess.run(["systemctl", "reload", "ssh"])
    print("SSH hardening issues fixed.")

def fix_patch_issues(issues):
    print("Fixing patch management issues...")
    # Example: Update the system packages using apt-get (for Debian/Ubuntu)
    subprocess.run(["apt-get", "update"])
    subprocess.run(["apt-get", "upgrade", "-y"])
    print("Patch management issues fixed.")

def fix_access_control_issues(issues):
    print("Fixing user access control issues...")
    # Example: Start Polkit service
    subprocess.run(["systemctl", "start", "polkit"])
    # Example: Set SELinux to enforcing mode
    subprocess.run(["setenforce", "1"])
    print("User access control issues fixed.")

def fix_security_issues(issues):
    print("Fixing security issues...")
    if 'firewall_issues' in issues:
        fix_firewall_issues(issues['firewall_issues'])
    if 'ssh_issues' in issues:
        fix_ssh_issues(issues['ssh_issues'])
    if 'patch_issues' in issues:
        fix_patch_issues(issues['patch_issues'])
    if 'access_control_issues' in issues:
        fix_access_control_issues(issues['access_control_issues'])
    print("Security issues fixed.")

def main():
    # Simulated dictionary of security issues for testing
    security_issues = {
        'firewall_issues': {'firewall_status': 'Firewall rules are not configured properly.'},
        'ssh_issues': {},
        'patch_issues': {'kernel_version': 'Kernel version is not up to date.'},
        'access_control_issues': {'rbac_status': 'RBAC is not enforcing.'}
    }

    # Fix security issues if any
    fix_security_issues(security_issues)

if __name__ == "__main__":
    main()
