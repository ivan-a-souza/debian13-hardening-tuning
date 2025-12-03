# Debian 13 Hardening & Tuning Playbook

Este projeto tem como objetivo criar um playbook do Ansible para realizar o hardening (segurança) e tuning (otimização de performance) em servidores **Debian 13 (Trixie)**.

## 🎯 Escopo

Este playbook é focado especificamente em:
- **Sistema Operacional**: Debian 13 (Trixie).
- **Hardening**: Implementação de práticas de segurança (CIS, STIG) para reduzir a superfície de ataque.
- **Tuning**: Ajustes de kernel e serviços para otimização de performance.

## ⚠️ Avisos de Risco (Disclaimer)

> [!WARNING]
> **Atenção**: A aplicação de regras de hardening pode ser restritiva e **quebrar a compatibilidade** com aplicações existentes.

- **Teste antes de aplicar**: Nunca execute este playbook diretamente em produção sem antes validar em um ambiente de homologação.
- **Acesso SSH**: Algumas regras podem alterar configurações de SSH. Certifique-se de ter um método de acesso alternativo (console/VNC) caso perca a conexão.
- **Backup**: Sempre tenha backups atualizados antes de aplicar mudanças estruturais no sistema.

## 📋 Requisitos

- Ansible instalado na máquina de controle.
- Acesso SSH ao(s) servidor(es) alvo rodando Debian 13.
- Privilégios de root ou sudo no servidor alvo.

## 🚀 Roadmap

- [ ] Configuração inicial do projeto (estrutura de diretórios, inventory).
- [ ] Criação de roles para Hardening:
    - [ ] Configuração de SSH (desabilitar root, alterar porta, chaves apenas).
    - [ ] Firewall (UFW/NFTables).
    - [ ] Atualizações automáticas (unattended-upgrades).
    - [ ] Configurações de Kernel (sysctl).
- [ ] Criação de roles para Tuning:
    - [ ] Otimização de I/O.
    - [ ] Otimização de Rede.
- [ ] Testes e Validação.

## 🛠️ Como Executar

### 1. Configurar Inventário
Edite o arquivo `inventory/hosts` (ou similar) com os IPs dos seus servidores:

```ini
[debian_servers]
192.168.1.10
192.168.1.11
```

### 2. Executar em modo Dry-Run (Simulação)
Sempre execute primeiro em modo de verificação para ver o que será alterado sem aplicar as mudanças:

```bash
ansible-playbook -i inventory/hosts site.yml --check --diff
```

### 3. Executar o Playbook
Para aplicar as configurações:

```bash
ansible-playbook -i inventory/hosts site.yml
```

### 4. Usando Tags
Você pode rodar apenas partes específicas do playbook usando tags (ex: apenas hardening ou apenas ssh):

```bash
# Rodar apenas tarefas de hardening
ansible-playbook -i inventory/hosts site.yml --tags "hardening"

# Rodar apenas configuração de SSH
ansible-playbook -i inventory/hosts site.yml --tags "ssh"
```
