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

You can customize the playbook behavior using the following variables in `roles/hardening/defaults/main.yml`.

### Global Toggles
| Variable | Default | Description |
|----------|---------|-------------|
| `hardening_ssh_enable` | `true` | Enables SSH hardening role. |
| `hardening_firewall_enable` | `true` | Enables UFW firewall configuration. |
| `hardening_pam_enable` | `true` | Enables PAM password quality and lockout policies. |
| `hardening_banners_enable` | `true` | Enables legal login banners (issue, motd). |
| `hardening_cron_enable` | `true` | Enables cron/at restriction hardening. |
| `hardening_modules_enable` | `true` | Enables kernel module hardening (legacy FS, uncommon net). |

### Granular Settings (Examples)
| Variable | Default | Description |
|----------|---------|-------------|
| `hardening_ssh_port` | `2222` | The new SSH port to use (if `hardening_ssh_configure_port` is true). |
| `hardening_pam_pwquality_minlen` | `14` | Minimum password length. |
| `hardening_permissions_logs` | `true` | Enforces 0750 permissions on `/var/log`. |
| `hardening_modules_disable_usb_storage` | `false` | Disables usb-storage module via modprobe. |

Refer to `roles/hardening/defaults/main.yml` for the full list of ~50 customizable variables.

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

- [x] Initial project setup.
- [x] Hardening roles:
    - [x] SSH Configuration.
    - [x] Firewall (UFW).
    - [x] PAM & Password Policies (New).
    - [x] Login Banners (New).
    - [x] Cron/Anacron Hardening (New).
    - [x] Kernel Module Hardening (New).
    - [x] Sysctl, Auditd, Postfix, Fail2Ban.
- [x] Tuning roles (I/O & Network).
- [x] Audit-only mode toggle.
- [x] CI/CD (GitHub Actions + Molecule Matrix).

## 🛠️ How to Execute

### 1. Configure Inventory
Edit `inventory/hosts` with your server IPs.

### 2. Run in Audit Mode (Simulation)
```bash
ansible-playbook -i inventory/hosts site.yml -e hardening_mode=audit
```

### 3. Apply Hardening
```bash
ansible-playbook -i inventory/hosts site.yml
```

### 4. Selective Execution (Tags)
```bash
ansible-playbook -i inventory/hosts site.yml --tags "ssh,firewall"
```

## 🧪 Validation
```bash
# Run lint + check-mode
scripts/test.sh
```
