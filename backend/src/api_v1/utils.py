from contextlib import asynccontextmanager
from starlette.websockets import WebSocket
from fastapi.security import HTTPBearer


@asynccontextmanager
async def WebSocketManager(websocket: WebSocket):  # NOQA
    try:
        await websocket.accept()
        yield
    finally:
        await websocket.close()


http_bearer = HTTPBearer()
