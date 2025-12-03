# Debian 13 Hardening & Tuning Playbook

This project aims to create an Ansible playbook to perform hardening (security) and tuning (performance optimization) on **Debian 13 (Trixie)** servers.

## 🎯 Scope

This playbook is specifically focused on:
- **Operating System**: Debian 13 (Trixie).
- **Hardening**: Implementation of security practices (CIS, STIG) to reduce the attack surface.
- **Tuning**: Kernel and service adjustments for performance optimization.

## ⚠️ Risk Warnings (Disclaimer)

> [!WARNING]
> **Attention**: Applying hardening rules can be restrictive and **break compatibility** with existing applications.

- **Test before applying**: Never run this playbook directly in production without first validating it in a staging environment.
- **SSH Access**: Some rules may change SSH configurations. Ensure you have an alternative access method (console/VNC) in case you lose connection.
- **Backup**: Always have up-to-date backups before applying structural changes to the system.

## 📋 Requirements

- Ansible installed on the control machine.
- SSH access to the target server(s) running Debian 13.
- Root or sudo privileges on the target server.

## ⚙️ Configuration

You can customize the playbook behavior using the following variables in `roles/hardening/defaults/main.yml` or your inventory variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `hardening_update_packages` | `true` | Updates all system packages and cleans up unused dependencies. |
| `hardening_ssh_disable_root` | `true` | Disables SSH root login (`PermitRootLogin no`). |
| `hardening_ssh_disable_password` | `true` | Disables password authentication (`PasswordAuthentication no`). |
| `hardening_ssh_configure_port` | `false` | Enables changing the SSH port. |
| `hardening_ssh_port` | `2222` | The new SSH port to use (requires `hardening_ssh_configure_port: true`). |
| `hardening_ssh_allow_users` | `[]` | List of users allowed to log in via SSH. Automatically includes `hardening_user_name` if user creation is enabled. |
| `hardening_ssh_login_grace_time` | `30` | Time in seconds to disconnect if not authenticated. |
| `hardening_ssh_max_auth_tries` | `3` | Maximum number of authentication attempts. |
| `hardening_firewall_enable` | `true` | Installs UFW, allows SSH port, and enables the firewall. |
| `hardening_unattended_upgrades_enable` | `true` | Installs and configures unattended-upgrades for automatic security updates. |
| `hardening_unattended_automatic_reboot` | `false` | Enables automatic reboot after updates if required. |
| `hardening_unattended_automatic_reboot_time` | `02:00` | Time to perform the automatic reboot (if enabled). |
| `hardening_user_create` | `false` | Creates a new user with sudo privileges. |
| `hardening_user_name` | `admin_user` | Username for the new user. |
| `hardening_user_password` | `""` | Password hash for the new user (Required if create is true). |
| `hardening_sudo_require_password` | `true` | Ensures sudo requires a password (`%sudo ALL=(ALL:ALL) ALL`). |
| `hardening_user_ssh_key_path` | `ssh/id_ed25519.pub` | Path to the public key to be added to the user's authorized_keys. |
| `hardening_fail2ban_enable` | `true` | Installs and configures Fail2Ban to protect SSH. |
| `hardening_fail2ban_maxretry` | `3` | Number of failures before banning. |
| `hardening_fail2ban_findtime` | `1h` | Time window to count failures. |
| `hardening_fail2ban_bantime` | `10m` | Duration of the ban. |
| `hardening_fail2ban_email_enable` | `false` | Enables email alerts for bans (requires MTA). |
| `hardening_postfix_enable` | `true` | Installs and configures Postfix as a relay MTA. |
| `hardening_postfix_relayhost` | `smtp.example.com` | The external SMTP server to relay emails to. |
| `hardening_postfix_mailname` | `{{ ansible_fqdn }}` | The system's mail name (FQDN). |
| `hardening_postfix_root_recipient` | `admin@example.com` | Email address to receive root's mail. |
| `hardening_postfix_sasl_enable` | `false` | Enables SMTP authentication (SASL). |
| `hardening_postfix_sasl_user` | `""` | Username for SMTP authentication. |
| `hardening_postfix_sasl_password` | `""` | Password for SMTP authentication. |
| `hardening_postfix_tls_enable` | `true` | Enables TLS for Postfix. |
| `hardening_postfix_tls_security_level` | `encrypt` | TLS security level (encrypt, may, none). |
| `hardening_postfix_tls_ca_file` | `/etc/ssl/certs/ca-certificates.crt` | Path to CA certificates file. |
| `hardening_sysctl_enable` | `true` | Enables kernel hardening via sysctl. |
| `hardening_sysctl_settings` | `{...}` | Dictionary of sysctl parameters (see defaults for full list). |

## 🔑 SSH Key Management

To securely manage SSH keys for the new user:

1. **Generate a new key pair** inside the `ssh/` directory (this directory is ignored by git):
    ```bash
    mkdir -p ssh
    ssh-keygen -t ed25519 -f ssh/id_ed25519 -C "admin_user"
    ```

2. **Configure the playbook** to use this key:
    - Ensure `hardening_user_ssh_key_path` points to your public key (default is `ssh/id_ed25519.pub`).
    - Enable user creation: `hardening_user_create: true`.

3. **Run the playbook**: The public key will be automatically added to the user's `authorized_keys` with correct permissions (`0700` for `.ssh` directory).

## 🚀 Roadmap

- [x] Initial project setup (directory structure, inventory).
- [ ] Creation of Hardening roles:
    - [x] SSH Configuration (disable root, change port, keys only).
    - [x] Firewall (UFW/NFTables).
    - [x] Automatic Updates (unattended-upgrades).
    - [x] Kernel Configurations (sysctl).
- [ ] Creation of Tuning roles:
    - [ ] I/O Optimization.
    - [ ] Network Optimization.
- [ ] Tests and Validation.

## 🛠️ How to Execute

### 1. Configure Inventory
Edit the `inventory/hosts` file (or similar) with the IPs of your servers:

```ini
[debian_servers]
192.168.1.10
192.168.1.11
```

### 2. Run in Dry-Run Mode (Simulation)
Always run first in check mode to see what will be changed without applying the changes:

```bash
ansible-playbook -i inventory/hosts site.yml --check --diff
```

### 3. Run the Playbook
To apply the configurations:

```bash
ansible-playbook -i inventory/hosts site.yml
```

### 4. Using Tags
You can run only specific parts of the playbook using tags (e.g., only hardening or only ssh):

```bash
# Run only hardening tasks
ansible-playbook -i inventory/hosts site.yml --tags "hardening"

# Run only SSH configuration
ansible-playbook -i inventory/hosts site.yml --tags "ssh"
```
