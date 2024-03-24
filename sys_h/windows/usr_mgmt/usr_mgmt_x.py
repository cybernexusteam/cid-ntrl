import subprocess
import re

def fix_weak_passwords(username):
    try:
        # Generate a new strong password and set it for the user
        new_password = "NewStrongPassword123!"  # You can generate a strong password dynamically
        command = f"net user {username} {new_password}"
        subprocess.run(command, shell=True, check=True)
        print(f"Fixed weak password for user: {username}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to fix weak password for user {username}: {e}")

def fix_inactive_accounts(username):
    try:
        # Enable the inactive account
        command = f"net user {username} /active:yes"
        subprocess.run(command, shell=True, check=True)
        print(f"Fixed inactive account: {username}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to fix inactive account for user {username}: {e}")

def fix_excessive_privileges(group, unwanted_members):
    try:
        # Remove excessive members from the group
        for member in unwanted_members:
            command = f"net localgroup {group} {member} /delete"
            subprocess.run(command, shell=True, check=True)
        print(f"Fixed excessive privileges for group: {group}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to fix excessive privileges for group {group}: {e}")

def get_local_users():
    command = 'net user'
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True, shell=True)
    output = result.stdout

    pattern = re.compile(r'User accounts for (.+):\n\n(.+)\n\nThe command completed successfully.')
    matches = pattern.findall(output)

    local_users = []
    if matches:
        for match in matches:
            users = match[1].strip().split()
            local_users.extend(users)

    return local_users

def get_inactive_users():
    command = 'net user'
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True, shell=True)
    output = result.stdout

    pattern = re.compile(r'(\S+)\s+([^\n]+)Account\s+expires\s+([^\n]+)')
    matches = pattern.findall(output)

    inactive_users = []
    if matches:
        for match in matches:
            if "Never" in match[2]:
                inactive_users.append(match[0])

    return inactive_users

def get_excessive_privileges():
    command = 'net localgroup'
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True, shell=True)
    output = result.stdout

    pattern = re.compile(r'The\s+([^\s]+)\s+members\s+are\s+:(.*)')
    matches = pattern.findall(output)

    excessive_privileges = {}
    if matches:
        for match in matches:
            group = match[0]
            members = match[1].strip().split()
            if len(members) > 5:  
                excessive_privileges[group] = members

    return excessive_privileges

if __name__ == "__main__":
    print("Fixing vulnerabilities...")

    local_users = get_local_users()
    inactive_users = get_inactive_users()
    excessive_privileges = get_excessive_privileges()

    for user in local_users:
        if user in inactive_users:
            fix_inactive_accounts(user)

    for group, members in excessive_privileges.items():
        fix_excessive_privileges(group, members)

    print("Vulnerabilities fixed.")
