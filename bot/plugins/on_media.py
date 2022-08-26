from pyrogram.file_id import FileId
import asyncio
from bot.client import Client
from bot.core.display import humanbytes
from bot.core.db.add import (
    add_user_to_database
)
from pyrogram import (
    filters,
    types
)
from bot.core.file_info import (
    get_media_file_id,
    get_media_file_size,
    get_media_file_name,
    get_file_type,
    get_file_attr
)


@Client.on_message((filters.video | filters.audio | filters.document) & ~filters.channel & ~filters.edited)
async def on_media_handler(c: Client, m: "types.Message"):
    if not m.from_user:
        return await m.reply_text("I don't know about you sar :(")
    await add_user_to_database(c, m)
    await c.send_flooded_message(
        chat_id=m.chat.id,
        text="**__What do you want me to do with this file?__**",
        reply_markup=types.InlineKeyboardMarkup(
            [[types.InlineKeyboardButton("✏️ 𝙍𝙀𝙉𝘼𝙈𝙀", callback_data="rename")],
             [types.InlineKeyboardButton("❌ 𝘾𝘼𝙉𝘾𝙀𝙇", callback_data="closeMessage")]]
        ),
        disable_web_page_preview=True,
        reply_to_message_id=m.message_id
    )







#gg
