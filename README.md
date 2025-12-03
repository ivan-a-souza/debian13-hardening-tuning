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

## 🚀 Roadmap

- [ ] Initial project setup (directory structure, inventory).
- [ ] Creation of Hardening roles:
    - [ ] SSH Configuration (disable root, change port, keys only).
    - [ ] Firewall (UFW/NFTables).
    - [ ] Automatic Updates (unattended-upgrades).
    - [ ] Kernel Configurations (sysctl).
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
