import subprocess
import re

def check_weak_passwords(vuln_dict):
    command = 'net user'
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True, shell=True)
    output = result.stdout

    pattern = re.compile(r'User accounts for (.+):\n\n(.+)\n\nThe command completed successfully.')
    matches = pattern.findall(output)

    if matches:
        for match in matches:
            username = match[0]
            password_info = match[1]

            if "Password last set" in password_info and "Password expires" in password_info:
                password_set_date = re.search(r'Password last set\s+([^\n]+)', password_info).group(1)
                password_expires = re.search(r'Password expires\s+([^\n]+)', password_info).group(1)
                if "never" not in password_expires:
                    password_expires = re.search(r'(\d+/\d+/\d+)', password_expires).group(1)
                    if "Weak" in password_info or "Blank" in password_info:
                        vuln_dict[username] = f"Weak Password: Password last set: {password_set_date}, Password expires: {password_expires}"
            elif "Password last set" in password_info and "Password expires" not in password_info:
                if "Weak" in password_info or "Blank" in password_info:
                    vuln_dict[username] = "Weak Password: No expiration date"
            else:
                if "Weak" in password_info or "Blank" in password_info:
                    vuln_dict[username] = "Weak or Blank Password"

def check_inactive_accounts(vuln_dict):
    command = 'net user'
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True, shell=True)
    output = result.stdout

    pattern = re.compile(r'(\S+)\s+([^\n]+)Account\s+expires\s+([^\n]+)')
    matches = pattern.findall(output)

    if matches:
        for match in matches:
            username = match[0]
            account_expires = match[2]
            if "Never" in account_expires:
                vuln_dict[username] = "Inactive Account: Never Expires"

def check_excessive_privileges(vuln_dict):
    command = 'net localgroup'
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True, shell=True)
    output = result.stdout

    pattern = re.compile(r'The\s+([^\s]+)\s+members\s+are\s+:(.*)')
    matches = pattern.findall(output)

    if matches:
        for match in matches:
            group = match[0]
            members = match[1].strip().split()
            if len(members) > 5:  
                vuln_dict[group] = f"Excessive Privileges: Members: {', '.join(members)}"

if __name__ == "__main__":
    vuln_dict = {}
    print("Checking for user account vulnerabilities...")
    check_weak_passwords(vuln_dict)
    check_inactive_accounts(vuln_dict)
    check_excessive_privileges(vuln_dict)
    print("Vulnerability check completed.")

    if vuln_dict:
        print("\nVulnerabilities Found:")
        for key, value in vuln_dict.items():
            print(f"{key}: {value}")
    else:
        print("No vulnerabilities found.")
