---
trigger: always_on
---

# Project Facts: iil-relaunch

> Website relaunch assets

## Meta

- **Type**: `infra`
- **GitHub**: `https://github.com/achimdehnert/iil-relaunch`
- **Branch**: `main` — push: `git push` (SSH-Key konfiguriert)

## System (Hetzner Server)

- devuser hat **KEIN sudo-Passwort** → System-Pakete immer via SSH als root:
  ```bash
  ssh root@localhost "apt-get install -y <package>"
  ```

## Secrets / Config

- **Secrets**: `.env` (nicht in Git) — Template: `.env.example`
