#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v ansible-lint >/dev/null 2>&1; then
  echo "ansible-lint not found; install with: pip install -r requirements-dev.txt" >&2
  exit 1
fi

export ANSIBLE_STDOUT_CALLBACK=yaml
export ANSIBLE_FORCE_COLOR=1

ansible-lint .
ansible-playbook -i inventory/test/hosts site.yml --check --diff
