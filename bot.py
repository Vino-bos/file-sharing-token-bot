
from pyrogram import Client, filters
from pyrogram.types import Message
import os

API_ID = int(os.environ.get("APP_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")

app = Client("file_sharing_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Start command
@app.on_message(filters.command("start"))
async def start(_, message: Message):
    await message.reply_text(
        f"👋 Hello {message.from_user.mention}!\n\nSend me a file and I’ll give you a direct download link."
    )

# File handler
@app.on_message(filters.document | filters.video | filters.audio)
async def handle_file(_, message: Message):
    file = message.document or message.video or message.audio
    file_id = file.file_id
    file_name = file.file_name
    file_size = file.file_size

    # You could save this file info to a DB here if needed
    await message.reply_text(
        f"✅ File received: `{file_name}`\n\n🔗 Share link:\nhttps://t.me/{(await app.get_me()).username}?start={file_id}"
    )

# Handle link start with file ID
@app.on_message(filters.private & filters.regex(r"^/start (.+)"))
async def send_file_by_id(_, message: Message):
    file_id = message.text.split(None, 1)[1]
    try:
        await message.reply_document(file_id)
    except Exception as e:
        await message.reply_text("❌ Failed to send file. Maybe expired or invalid.")

app.run()
