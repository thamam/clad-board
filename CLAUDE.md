# Bot Monitoring Dashboard

## Commands
```bash
python3 -m pytest backend/tests/ -v   # run from project root
docker compose up -d --build           # full stack
```

## Critical: Naive-UTC Datetimes
All datetimes must be naive-UTC (no tzinfo). Use `utcnow()` from `backend/models.py`, never `datetime.now(timezone.utc)`. SQLite strips timezone info on storage — mixing aware/naive causes TypeError on read-back.

## Deployment
- **EC2:** ubuntu@54.197.72.152 (SSH key: ~/.ssh/aws/open-claw-key.pem)
- **Domain:** dashboard.a2xautonomy.com (Cloudflare DNS, proxy OFF)
- **Caddy:** reverse_proxy dashboard.a2xautonomy.com → backend:8000
