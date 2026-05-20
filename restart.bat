@echo off
echo === Stopping all containers ===
docker compose down
echo === Rebuilding and starting with fresh env ===
docker compose up -d --force-recreate
echo === Done! Containers recreated with latest .env ===
docker compose ps
pause
