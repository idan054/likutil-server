
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
# export OPENAI_API_KEY="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"


import uvicorn
from pip._internal.cli.cmdoptions import debug_mode

if __name__ == "__main__":
    uvicorn.run(
        "api.index:app",
        host="0.0.0.0",
        port=8001 if debug_mode else 8000,
        reload=debug_mode,
    )

