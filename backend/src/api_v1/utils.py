from contextlib import asynccontextmanager
from starlette.websockets import WebSocket


@asynccontextmanager
async def WebSocketManager(websocket: WebSocket):  # NOQA
    try:
        await websocket.accept()
        yield
    finally:
        await websocket.close()
