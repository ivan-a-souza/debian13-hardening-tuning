#!/usr/bin/env python3
"""Testinfra tests for debian-hardening role."""

import re


def test_ssh_config(host):
    """SSH hardening: root login disabled, password auth disabled."""
    sshd = host.file("/etc/ssh/sshd_config")
    assert sshd.contains(r"^PermitRootLogin\s+no")
    assert sshd.contains(r"^PasswordAuthentication\s+no")
    assert sshd.contains(r"^Port\s+22")


def test_firewall_ufw(host):
    """UFW is enabled and active."""
    # Check service enabled (systemd)
    ufw = host.service("ufw")
    assert ufw.is_enabled
    assert ufw.is_running


def test_sshd_running(host):
    """sshd service running."""
    svc = host.service("ssh")
    assert svc.is_running


def test_fail2ban_installed(host):
    """Fail2Ban installed and running."""
    pkg = host.package("fail2ban")
    assert pkg.is_installed
    svc = host.service("fail2ban")
    assert svc.is_running


def test_fail2ban_config_exists(host):
    """Fail2Ban config present."""
    jail_conf = host.file("/etc/fail2ban/jail.conf")
    jail_local = host.file("/etc/fail2ban/jail.local")
    assert jail_conf.exists or jail_local.exists


def test_unattended_upgrades_installed(host):
    """unattended-upgrades installed and config present."""
    pkg = host.package("unattended-upgrades")
    assert pkg.is_installed
    cfg = host.file("/etc/apt/apt.conf.d/50unattended-upgrades")
    assert cfg.exists
    assert cfg.is_file


def test_postfix_installed(host):
    """Postfix installed and running."""
    pkg = host.package("postfix")
    assert pkg.is_installed
    svc = host.service("postfix")
    assert svc.is_running


def test_permissions_core_files(host):
    """Core system files permissions (shadow 640, passwd 644)."""
    passwd = host.file("/etc/passwd")
    shadow = host.file("/etc/shadow")
    assert passwd.mode == 0o644
    assert shadow.mode in (0o640, 0o600)


def test_auditd_installed(host):
    """Auditd installed and running."""
    pkg = host.package("auditd")
    assert pkg.is_installed
    svc = host.service("auditd")
    assert svc.is_running


def test_sysctl_hardening(host):
    """Check certain hardening sysctl values."""
    sysctl = host.sysctl
    # Randomize VA space
    assert sysctl("kernel.randomize_va_space") == "2"
    # Disable IP forwarding (default)
    assert sysctl("net.ipv4.ip_forward") == "0"
    # ICMP redirects off
    assert sysctl("net.ipv4.conf.all.accept_redirects") == "0"


def test_sysctl_tuning_io(host):
    """Check I/O tuning sysctl."""
    sysctl = host.sysctl
    # vm.swappiness tuned
    assert sysctl("vm.swappiness") == "10"
    # vm.dirty_ratio
    assert sysctl("vm.dirty_ratio") == "15"


def test_sysctl_tuning_network(host):
    """Check network tuning sysctl."""
    sysctl = host.sysctl
    # Congestion control
    assert sysctl("net.ipv4.tcp_congestion_control") == "bbr"
    # TCP fast open
    assert sysctl("net.ipv4.tcp_fastopen") == "3"


def test_ufw_allows_ssh(host):
    """UFW allows SSH port (default 22)."""
    status = host.check_output("ufw status")
    assert "22" in status


def test_auditd_rules_file(host):
    """Auditd rules file present."""
    rules = host.file("/etc/audit/rules.d/audit.rules")
    assert rules.exists
    assert rules.is_file


def test_sysctl_files_exist(host):
    """Hardening and tuning sysctl config files exist."""
    assert host.file("/etc/sysctl.d/99-hardening.conf").exists
    assert host.file("/etc/sysctl.d/99-tuning-io.conf").exists
    assert host.file("/etc/sysctl.d/99-tuning-net.conf").exists


def test_sysctl_conf_content(host):
    """Check sysctl config files contain key settings."""
    io_conf = host.file("/etc/sysctl.d/99-tuning-io.conf")
    net_conf = host.file("/etc/sysctl.d/99-tuning-net.conf")
    assert io_conf.contains("vm.swappiness")
    assert net_conf.contains("net.ipv4.tcp_congestion_control")


def test_banner_files(host):
    """Banner files exist."""
    issue = host.file("/etc/issue")
    issue_net = host.file("/etc/issue.net")
    assert issue.exists
    assert issue_net.exists


def test_pam_password_policy(host):
    """PAM password policy (pwquality) present."""
    pam = host.file("/etc/pam.d/common-password")
    assert pam.contains("pam_pwquality")


def test_cron_anacron_installed(host):
    """Cron/Anacron installed."""
    cron_pkg = host.package("cron")
    assert cron_pkg.is_installed
    anacron_pkg = host.package("anacron")
    assert anacron_pkg.is_installed


def test_grub_cfg_permissions(host):
    """GRUB config has restrictive permissions."""
    grub = host.file("/boot/grub/grub.cfg")
    if grub.exists:
        assert grub.mode <= 0o640


def test_modprobe_blacklist(host):
    """Modprobe blacklist file exists (if provided)."""
    blk = host.file("/etc/modprobe.d/blacklist.conf")
    # Not fatal if absent, but check presence if shipped
    if blk.exists:
        assert blk.is_file


def test_user_ssh_key_permissions(host):
    """SSH authorized_keys file permissions secure."""
    ssh_dir = host.file("/home/admin_user/.ssh")
    if ssh_dir.exists:
        assert ssh_dir.mode == 0o700
        auth_keys = host.file("/home/admin_user/.ssh/authorized_keys")
        if auth_keys.exists:
            assert auth_keys.mode == 0o600
