# iil.ai — Relaunch

Moderne Landing Page für IIL (Institut für Informationslogistik) unter [iil.ai](https://iil.ai).

## Stack

- Pure static HTML/CSS/JS — kein Build-Step, kein Framework
- `index.html` + `impressum.html` + `datenschutz.html`
- Inter (Google Fonts), SVG-Icons, CSS Custom Properties
- Deployed via Nginx auf Hetzner (`88.198.191.108`)
- CI/CD via GitHub Actions (push to `main` → auto-deploy per SSH)

## Struktur

```
.
├── index.html                   # Landing Page
├── impressum.html               # Impressum
├── datenschutz.html             # Datenschutzerklärung
├── apps.json                    # App-Daten (name, desc, status, icon, color, tags)
├── env_loader.py                # Symlink → ~/.secrets/env_loader.py
├── nginx/
│   └── iil.ai.conf              # Nginx-Konfiguration (SSL, try_files, gzip)
├── scripts/
│   └── setup_email_forwarding.py  # E-Mail-Forwarding Setup (ForwardEmail + Cloudflare)
└── .github/
    └── workflows/
        └── deploy.yml           # CI/CD: main → rsync → Hetzner
```

## Seiten & Sections

### `index.html`
1. **Hero** — KI-Strategie & Digitale Transformation
2. **Trust Bar** — Technology-Pills
3. **Leistungen** — 6 Service-Cards (InnoVision, KI im Business, InnoCoach, InnoEdge, InnoAudit, Datenschutz)
4. **Über IIL** — Tech-Stack-Tiles + USP-Liste
5. **Eigenentwickelte KI-Produkte** — Zwei Sektionen (Produktiv / In Entwicklung), dynamisch aus `apps.json`
6. **Kontakt** — CTA, Telefon, Adresse

### `apps.json`
Verwaltet alle Plattform-Apps. Status-Werte steuern die Darstellung:

| Status | Darstellung |
|--------|-------------|
| `live` | Sektion "Produktiv", mit Link |
| `beta` | Sektion "In Entwicklung", ohne Link, Badge |
| `dev`  | Sektion "In Entwicklung", ohne Link, Badge |

```json
{
  "name": "Bieterpilot – Ausschreibungen",
  "url": "https://bieterpilot.de",
  "desc": "...",
  "icon": "clipboard",
  "color": { "bg": "rgba(34,197,94,0.12)", "fg": "#22c55e" },
  "tags": ["Procurement", "AI"],
  "status": "dev"
}
```

## E-Mail-Forwarding

Catch-All für alle Produkt-Domains → `ad@dehnert.team` via [ForwardEmail.net](https://forwardemail.net).

```bash
# Einmalig ausführen (oder nach neuen Domains):
python3 scripts/setup_email_forwarding.py
```

Konfigurierte Domains:

| Domain | DNS | Status |
|--------|-----|--------|
| `bieterpilot.de` | Cloudflare | ✅ |
| `nl2cad.de` | Cloudflare | ✅ |
| `prezimo.de` | Cloudflare | ✅ |
| `prezimo.com` | Cloudflare | ✅ |
| `drifttales.de` | Cloudflare | ✅ |
| `drifttales.app` | Cloudflare | ✅ |
| `drifttales.com` | Cloudflare | ✅ |
| `schutztat.de` | Cloudflare | ✅ |
| `schutztat.com` | Cloudflare | ✅ |
| `ai-trades.de` | Cloudflare | ✅ |
| `kiohnerisiko.de` | Cloudflare | ✅ |
| `iil.ai` | Microsoft 365 | eigenes Postfach |

## Secrets

Das Projekt nutzt die zentrale Secrets-Infrastruktur unter `~/.secrets/`.

```python
from env_loader import env

CF_TOKEN = env("CLOUDFLARE_WRITE_TOKEN", "cloudflare_write_token")
FE_TOKEN = env("FORWARDEMAIL_API_TOKEN", "forwardemail_api_token")
```

Bekannte Secret-Dateien:

| Datei | Verwendung |
|-------|-----------|
| `~/.secrets/cloudflare_write_token` | Cloudflare DNS API (Write) |
| `~/.secrets/cloudflare_api_token` | Cloudflare DNS API (Read) |
| `~/.secrets/hetzner_cloud_token` | Hetzner Cloud API |
| `~/.secrets/ionos_api_key` | IONOS DNS API |
| `~/.secrets/github_token` | GitHub PAT |
| `~/.secrets/forwardemail_api_token` | ForwardEmail API |
| `~/.secrets/mittwald_api_token` | Mittwald API |

Neues Repo einbinden:
```bash
bash ~/.secrets/deploy_env_loader.sh
```

## Deployment

### GitHub Actions (automatisch)

Jeder Push auf `main` deployt automatisch:
```
git push origin main  →  rsync → /opt/iil-ai/public/ auf 88.198.191.108
```

### GitHub Secrets

| Secret | Wert |
|--------|------|
| `DEPLOY_HOST` | `88.198.191.108` |
| `DEPLOY_USER` | `root` |
| `DEPLOY_KEY` | SSH Private Key |

### Manuelles Deployment

```bash
rsync -avz --delete \
  index.html impressum.html datenschutz.html apps.json \
  root@88.198.191.108:/opt/iil-ai/public/
```

### Nginx-Config aktualisieren

```bash
scp nginx/iil.ai.conf root@88.198.191.108:/etc/nginx/sites-enabled/iil.ai.conf
ssh root@88.198.191.108 "nginx -t && systemctl reload nginx"
```

### Erstinstallation Server

```bash
mkdir -p /opt/iil-ai/public
cp nginx/iil.ai.conf /etc/nginx/sites-enabled/iil.ai.conf
nginx -t && systemctl reload nginx
certbot --nginx -d iil.ai -d www.iil.ai
```

## DNS

| Record | Typ | Wert |
|--------|-----|------|
| `iil.ai` | A | `88.198.191.108` |
| `www.iil.ai` | A | `88.198.191.108` |
