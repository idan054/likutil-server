import uvicorn
from pip._internal.cli.cmdoptions import debug_mode

if __name__ == "__main__":
    uvicorn.run(
        "api.index:app",
        host="0.0.0.0",
        port=8001 if debug_mode else 8000,
        reload=debug_mode,
    )

