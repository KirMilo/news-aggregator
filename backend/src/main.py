from datetime import datetime

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware

from api_v1.router import router as v1_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(v1_router, prefix="/api/v1")


# @app.get("/")
# def check():
#     return {"message": "Hello World"}


@app.get("/mynews")
async def my_news():
    return [
        {"id": 1, "title": "title1", "body": "body1", "published_at": datetime.now(), "categories": ["cat1", "cat2", "cat3"]},
        {"id": 2, "title": "title1", "body": "body1", "published_at": datetime.now(), "categories": ["cat3", "cat4"]},
        {"id": 3, "title": "title1", "body": "body1", "published_at": datetime.now(), "categories": ["cat5", "cat6"]},
        ]

# html = """
# <!DOCTYPE html>
# <html>
#     <head>
#         <title>Chat</title>
#     </head>
#     <body>
#         <h1>WebSocket Chat</h1>
#         <form action="" onsubmit="sendMessage(event)">
#             <input type="text" id="messageText" autocomplete="off"/>
#             <button>Send</button>
#         </form>
#         <ul id='messages'>
#         </ul>
#         <script>
#             var ws = new WebSocket("ws://localhost:8001/api/v1/news/updates");
#             ws.onmessage = function(event) {
#                 var messages = document.getElementById('messages')
#                 var message = document.createElement('li')
#                 var content = document.createTextNode(event.data)
#                 message.appendChild(content)
#                 messages.appendChild(message)
#             };
#             function sendMessage(event) {
#                 var input = document.getElementById("messageText")
#                 ws.send(input.value)
#                 input.value = ''
#                 event.preventDefault()
#             }
#         </script>
#     </body>
# </html>
# """
#
# @app.get("/")
# async def get():
#     return HTMLResponse(html)


# @asynccontextmanager
# async def WebSocketManager(websocket: WebSocket):  # noqa
#     try:
#         await websocket.accept()
#         yield
#     except WebSocketDisconnect:
#         del websocket
#
# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     async with WebSocketManager(websocket):
#         while True:
#             data = await websocket.receive_text()
#             # await websocket.send_text(f"Message text was: {data}")
#             await websocket.send_json(
#                 {"message":"Hello, World!"},
#                 mode="text",
#             )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True, workers=1)

