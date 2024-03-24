import subprocess

def configure_login():
    opsys = subprocess.check_output(["uname", "-s"]).decode().strip()
    if opsys == "Linux":
        print("Configuring login settings...")

        if "Ubuntu" in subprocess.check_output(["lsb_release", "-d"]).decode().strip():
            print("Ubuntu detected.")
            log_time = subprocess.check_output(["date", "+%Y-%m-%d %H:%M:%S"]).decode().strip()
            username = subprocess.check_output(["whoami"]).decode().strip()

            # Configure /etc/lightdm/lightdm.conf
            print(f"{log_time} uss: [{username}]# Creating /etc/lightdm/lightdm.conf for 12.04 compatibility.")
            if subprocess.run(["ls", "/etc/lightdm/lightdm.conf"]).returncode == 0:
                subprocess.run(["sed", "-i", "$a", "allow-guest=false", "/etc/lightdm/lightdm.conf"])
                subprocess.run(["sed", "-i", "$a", "greeter-hide-users=true", "/etc/lightdm/lightdm.conf"])
                subprocess.run(["sed", "-i", "$a", "greeter-show-manual-login=true", "/etc/lightdm/lightdm.conf"])

                autologin_user = subprocess.check_output(["grep", "autologin-user", "/etc/lightdm/lightdm.conf"]).decode().strip()
                if autologin_user:
                    user = autologin_user.split("=")[-1]
                    if user != "none":
                        print(f"{user} has been set to autologin.")
                        subprocess.run(["sed", "-i", f"s/autologin-user=.*/autologin-user=none/", "/etc/lightdm/lightdm.conf"])
                else:
                    subprocess.run(["sed", "-i", "$a", "autologin-user=none", "/etc/lightdm/lightdm.conf"])

                with open("/etc/lightdm/lightdm.conf", "r") as lightdm_conf:
                    print(lightdm_conf.read())
                    input("Press Enter to continue...")

            else:
                with open("/etc/lightdm/lightdm.conf", "w") as lightdm_conf:
                    lightdm_conf.write("[SeatDefault]\n")
                    lightdm_conf.write("allow-guest=false\n")
                    lightdm_conf.write("greeter-hide-users=true\n")
                    lightdm_conf.write("greeter-show-manual-login=true\n")

                autologin_user = subprocess.check_output(["grep", "autologin-user", "/etc/lightdm/lightdm.conf"]).decode().strip()
                if autologin_user:
                    user = autologin_user.split("=")[-1]
                    if user != "none":
                        print(f"{user} has been set to autologin.")
                        subprocess.run(["sed", "-i", f"s/autologin-user=.*/autologin-user=none/", "/etc/lightdm/lightdm.conf"])
                else:
                    subprocess.run(["sed", "-i", "$a", "autologin-user=none", "/etc/lightdm/lightdm.conf"])

                with open("/etc/lightdm/lightdm.conf", "r") as lightdm_conf:
                    print(lightdm_conf.read())
                    input("Press Enter to continue...")

            print(f"{log_time} uss: [{username}]# Editing the ../50-ubuntu.conf for Ubuntu 14.04")
            subprocess.run(["sed", "-i", "$a", "greeter-hide-users=true", "/usr/share/lightdm/lightdm.conf.d/50-ubuntu.conf"])
            subprocess.run(["sed", "-i", "$a", "greeter-show-manual-login=true", "/usr/share/lightdm/lightdm.conf.d/50-ubuntu.conf"])
            subprocess.run(["sed", "-i", "$a", "allow-guest=false", "/usr/share/lightdm/lightdm.conf.d/50-ubuntu.conf"])

            autologin_user = subprocess.check_output(["grep", "autologin-user", "/etc/lightdm/lightdm.conf"]).decode().strip()
            if autologin_user:
                user = autologin_user.split("=")[-1]
                if user != "none":
                    print(f"{user} has been set to autologin.")
                    subprocess.run(["sed", "-i", f"s/autologin-user=.*/autologin-user=none/", "/etc/lightdm/lightdm.conf"])
            else:
                subprocess.run(["sed", "-i", "$a", "autologin-user=none", "/etc/lightdm/lightdm.conf"])

            print(f"{log_time} uss: [{username}]# Lightdm files have been configured")
            with open("/usr/share/lightdm/lightdm.conf.d/50-ubuntu.conf", "r") as conf_file:
                print(conf_file.read())
                input("Press Enter to continue...")
            print("Only Ubuntu is supported for now.")
    else:
        print("Operating system is not Linux.")

def install_pam_cracklib():
    print("Installing pam_cracklib...")
    # Example: Install pam_cracklib using the system's package manager
    subprocess.run(["sudo", "apt-get", "install", "pam_cracklib", "-y"])
    print("pam_cracklib installed.")

def set_password_policy():
    print("Setting password policy...")
    log_time = subprocess.check_output(["date", "+%Y-%m-%d %H:%M:%S"]).decode().strip()
    username = subprocess.check_output(["whoami"]).decode().strip()

    with open("output.log", "a") as log_file:
        log_file.write(f"{log_time} uss: [{username}]# Setting password policy...\n")
        log_file.write(f"{log_time} uss: [{username}]# Installing Craklib...\n")

# Install cracklib using system's package manager
    if subprocess.run(["apt-get", "install", "libpam-cracklib", "-y"]).returncode != 0:
        print("Failed to install libpam-cracklib using apt-get")
        # Handle failure here, if necessary

        with open("output.log", "a") as log_file:
            log_file.write(f"{log_time} uss: [{username}]# Cracklib installed.\n")

    # Modify /etc/login.defs for password aging policies
    subprocess.run(["sed", "-i.bak", "-e", "s/PASS_MAX_DAYS\\t[[:digit:]]\\+/PASS_MAX_DAYS\\t90/", "/etc/login.defs"])
    subprocess.run(["sed", "-i", "-e", "s/PASS_MIN_DAYS\\t[[:digit:]]\\+/PASS_MIN_DAYS\\t10/", "/etc/login.defs"])
    subprocess.run(["sed", "-i", "-e", "s/PASS_WARN_AGE\\t[[:digit:]]\\+/PASS_WARN_AGE\\t7/", "/etc/login.defs"])

    # Modify /etc/pam.d/common-password for password complexity
    subprocess.run(["sed", "-i", "-e", "s/difok=3\\+/difok=3 ucredit=-1 lcredit=-1 dcredit=-1 ocredit=-1/", "/etc/pam.d/common-password"])

    with open("output.log", "a") as log_file:
        log_file.write(f"{log_time} uss: [{username}]# Password Policy.\n")

    input("Press Enter to continue...")

def configure_pam():
    print("Configuring PAM (Pluggable Authentication Modules)...")
    # Example: Configure PAM to enforce password complexity using pam_cracklib
    with open("/etc/pam.d/common-password", "a") as pam_config_file:
        pam_config_file.write("\npassword   required   pam_cracklib.so retry=3 minlen=8 difok=3")
    print("PAM configuration updated.")

def enable_firewall():
    print("Enabling firewall...")
    # Example: Enable firewall (iptables/firewalld)
    subprocess.run(["sudo", "systemctl", "start", "firewalld"])
    subprocess.run(["sudo", "systemctl", "enable", "firewalld"])
    print("Firewall enabled.")

def enable_ssh_key_authentication():
    print("Enabling SSH key-based authentication...")
    # Example: Modify SSH configuration to enable key-based authentication
    with open("/etc/ssh/sshd_config", "a") as ssh_config_file:
        ssh_config_file.write("\nPasswordAuthentication no")
    subprocess.run(["sudo", "systemctl", "restart", "ssh"])
    print("SSH key-based authentication enabled.")

def lockout_policy():
    try:
        log_time = subprocess.check_output(["date", "+%Y-%m-%d %H:%M:%S"]).decode().strip()
        username = subprocess.check_output(["whoami"]).decode().strip()

        # Setting lockout policy
        with open("output.log", "a") as log_file:
            log_file.write(f"{log_time} uss: [{username}]# Setting lockout policy...\n")

        # Modify /etc/pam.d/common-auth to set lockout policy
        subprocess.run(["sed", "-i", "s/auth\trequisite\t\t\tpam_deny.so\+/auth\trequired\t\t\tpam_deny.so/", "/etc/pam.d/common-auth"])
        subprocess.run(["sed", "-i", "$a", "auth\trequired\t\t\tpam_tally2.so deny=5 unlock_time=1800 onerr=fail", "/etc/pam.d/common-auth"])

        # Modify /etc/pam.d/common-password to set password policy
        subprocess.run(["sed", "-i", "s/sha512\+/sha512 remember=13/", "/etc/pam.d/common-password"])

        with open("output.log", "a") as log_file:
            log_file.write(f"{log_time} uss: [{username}]# Lockout policy set.\n")

        input("Press Enter to continue...")
    except subprocess.CalledProcessError:
        print("Failed to set lockout policy.")

def main():
    #LIGHTDM STUFF
    configure_login()

    # Install pam_cracklib
    install_pam_cracklib()

    # Set password policy
    set_password_policy()

    # Configure PAM
    configure_pam()

    # Enable firewall
    enable_firewall()

    # Enable SSH key-based authentication
    enable_ssh_key_authentication()

    # Apply Lockout Policy mwahahahahahah
    lockout_policy()



    print("Security configurations applied successfully.")

if __name__ == "__main__":
    main()
