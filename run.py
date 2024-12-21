
# Make sure ur using PORT 8000
# ssh root@185.28.154.36
# Enter Password (Available in Kametra-Bitwarden)
# cd /opt/fastapi
# git pull

# EDIT:
# sudo nano /etc/nginx/sites-available/fastapi
# sudo nano /etc/systemd/system/fastapi.service # TO EDIT

# RESTART:
# sudo systemctl restart fastapi
# sudo systemctl daemon-reload

# VIEW:
# sudo systemctl start fastapi
# sudo systemctl stop fastapi
# sudo systemctl status fastapi
# sudo tail -f /var/log/nginx/access.log
# sudo tail -f /var/log/nginx/error.log
# CTRL + C (To Exit LOGS)

# git pull && sudo systemctl restart fastapi && sudo tail -f /var/log/nginx/access.log
import uvicorn
from pip._internal.cli.cmdoptions import debug_mode

if __name__ == "__main__":
    uvicorn.run(
        "api.index:app",
        host="0.0.0.0",
        port=8000 if debug_mode else 8000,
        reload=debug_mode,
    )

