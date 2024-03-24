import pwd
import os
import datetime
from collections import namedtuple

# Define a namedtuple to store user account security check results
UserResult = namedtuple('UserResult', ['has_password', 'valid_shell', 'home_dir_exists', 'home_dir_owned'])

def check_user_accounts():
    results = {}

    # Get all user accounts
    user_accounts = pwd.getpwall()

    for user in user_accounts:
        # Check if the user is a login user
        if os.access(f'/home/{user.pw_name}', os.R_OK):
            # Check if the user has no password set
            has_password = user.pw_passwd != ""

            # Check if the user has a valid shell
            valid_shell = user.pw_shell in ["/usr/bin/bash", "/usr/bin/sh", "/usr/bin/zsh"]

            # Check if the user's home directory exists
            home_dir_exists = os.path.exists(user.pw_dir)

            # Check if the user's home directory is owned by the user
            home_dir_owned = os.stat(user.pw_dir).st_uid == user.pw_uid

            user_result = UserResult(has_password, valid_shell, home_dir_exists, home_dir_owned)
            results[user.pw_name] = user_result

    return results

# Call the function and get the results
security_check_results = check_user_accounts()

# Print the results
for user, result in security_check_results.items():
    print(f"User: {user}")
    print(f"Has password: {result.has_password}")
    print(f"Valid shell: {result.valid_shell}")
    print(f"Home directory exists: {result.home_dir_exists}")
    print(f"Home directory owned by user: {result.home_dir_owned}")
    print()