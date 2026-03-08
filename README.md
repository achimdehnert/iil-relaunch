# iil.gmbh — Relaunch

Modern landing page for IIL GmbH (Institut für Informationslogistik).

## Stack

- Pure static HTML/CSS/JS — no build step, no framework
- Single `index.html` + Inter font (Google Fonts)
- Deployed via Nginx on Hetzner (88.198.191.108)

## Structure

```
.
├── index.html              # Main landing page
├── nginx/
│   └── iil.gmbh.conf       # Nginx server config
└── .github/
    └── workflows/
        └── deploy.yml      # CI/CD: push main → auto-deploy
```

## Sections

1. **Hero** — KI-Strategie & Digitale Transformation
2. **AI Competency Band** — technology pills
3. **Leistungen** — 6 service cards (InnoVision, KI im Business, InnoCoach, InnoEdge, InnoAudit, Datenschutz)
4. **Platform Showcase** — 9 live AI products
5. **Über IIL** — tech stack + USPs
6. **Kontakt** — CTA, phone, address

## Deployment

### First-time server setup

```bash
# On Hetzner server (as root or with sudo)
mkdir -p /opt/iil-gmbh/public
chown deploy:deploy /opt/iil-gmbh

# Copy Nginx config
cp nginx/iil.gmbh.conf /etc/nginx/sites-available/iil.gmbh
ln -s /etc/nginx/sites-available/iil.gmbh /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx

# SSL via Certbot
certbot --nginx -d iil.gmbh -d www.iil.gmbh
```

### GitHub Secrets required

| Secret | Value |
|--------|-------|
| `DEPLOY_HOST` | `88.198.191.108` |
| `DEPLOY_USER` | `deploy` |
| `DEPLOY_KEY` | SSH private key for `deploy` user |

### DNS

Point `iil.gmbh` and `www.iil.gmbh` A-records to `88.198.191.108`.
