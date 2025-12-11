from fastmcp import FastMCP
import asyncio
from db import init_db, save_message, fetch_messages
from pydantic import BaseModel

class SaveMessageInput(BaseModel):
    user_id: str
    message: str

class GetMessagesInput(BaseModel):
    user_id: str


app = FastMCP("sqlite-mcp-server")

# print(dir(app))

init_db()

@app.tool()
def save_user_message(data: SaveMessageInput):
    """Save a message into the SQLite database."""
    save_message(data.user_id, data.message)
    return {"status": "saved", "user_id": data.user_id}

@app.tool()
def get_user_messages(data: GetMessagesInput):
    """Retrieve all messages for the given user."""
    rows = fetch_messages(data.user_id)
    messages = [
        {
            "id": r[0],
            "message": r[1],
            "created_at": r[2],
        }
        for r in rows
    ]
    return {"user_id": data.user_id, "messages": messages}

if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=8000)
    asyncio.run(app.run_streamable_http_async(host="0.0.0.0"))
