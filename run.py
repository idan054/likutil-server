
# cd /opt/fastapi
# sudo nano /etc/systemd/system/fastapi.service
# To Start The App as a service So it will stay when disconnected
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "api.index:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
