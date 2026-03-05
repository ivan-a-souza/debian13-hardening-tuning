#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v ansible-lint >/dev/null 2>&1; then
  echo "ansible-lint not found; install with: pip install -r requirements-dev.txt" >&2
  exit 1
fi

# Use the modern way to get YAML output if using ansible-core 2.13+
# This avoids the removal error of community.general.yaml
export ANSIBLE_STDOUT_CALLBACK=default
export ANSIBLE_CALLBACK_RESULT_FORMAT=yaml
export ANSIBLE_FORCE_COLOR=1

ansible-lint .
ansible-playbook -i inventory/test/hosts site.yml --check --diff
