
# cd /opt/fastapi
# git pull

# RESTART:
# sudo systemctl restart fastapi
# sudo systemctl daemon-reload

# EDIT SERVICE:
# sudo nano /etc/systemd/system/fastapi.service

# To Start The App as a service So it will stay when disconnected
# sudo systemctl start fastapi
# sudo systemctl status fastapi # To VIEW LOGS
# sudo tail -f /var/log/nginx/access.log
# sudo tail -f /var/log/nginx/error.log
# CTRL + C (To Exit LOGS)

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "api.index:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
