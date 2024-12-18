#
# from flask import Flask
#
# from api.index import app
# from config import Config
#
#
#
# Flask
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=Config.PORT)
#
# FastAPI
# from api.index import app


import uvicorn

from api.config import Config

if __name__ == "__main__":
    uvicorn.run(
        "api.index:app",
        host="0.0.0.0",
        port=Config.PORT,
        reload=True,
        ssl_keyfile="selfsigned.key",
        ssl_certfile="selfsigned.crt"
    )
