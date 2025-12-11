# from fastmcp import FastMCP
# import asyncio
# from db import init_db, save_message, fetch_messages
# from pydantic import BaseModel

# class SaveMessageInput(BaseModel):
#     user_id: str
#     message: str

# class GetMessagesInput(BaseModel):
#     user_id: str


# app = FastMCP("sqlite-mcp-server")

# # print(dir(app))

# init_db()

# @app.tool()
# def save_user_message(data: SaveMessageInput):
#     """Save a message into the SQLite database."""
#     save_message(data.user_id, data.message)
#     return {"status": "saved", "user_id": data.user_id}

# @app.tool()
# def get_user_messages(data: GetMessagesInput):
#     """Retrieve all messages for the given user."""
#     rows = fetch_messages(data.user_id)
#     messages = [
#         {
#             "id": r[0],
#             "message": r[1],
#             "created_at": r[2],
#         }
#         for r in rows
#     ]
#     return {"user_id": data.user_id, "messages": messages}


# # @app.custom_route("/", methods=["GET"])
# # def root():
# #     return {"status": "ok", "message": "MCP server is running"}



# if __name__ == "__main__":
#     app.run()
#     # asyncio.run(app(transport="http", host="0.0.0.0"))

from fastmcp import FastMCP
from pydantic import BaseModel
from db import init_db, save_message, fetch_messages
from starlette.responses import JSONResponse

class SaveMessageInput(BaseModel):
    user_id: str
    message: str

class GetMessagesInput(BaseModel):
    user_id: str

app = FastMCP("sqlite-mcp-server")

init_db()

@app.tool()
def save_user_message(data: SaveMessageInput):
    save_message(data.user_id, data.message)
    return {"status": "saved", "user_id": data.user_id}

@app.tool()
def get_user_messages(data: GetMessagesInput):
    rows = fetch_messages(data.user_id)
    return {
        "user_id": data.user_id,
        "messages": [
            {"id": r[0], "message": r[1], "created_at": r[2]} for r in rows
        ],
    }

# Optional health check
@app.custom_route("/health", methods=["GET"])
async def health(request):
    return JSONResponse({"status": "healthy"})

if __name__ == "__main__":
    app.run(transport="http", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
