# (c) @AbirHasan2005

from bot.client import Client
from pyrogram import *
from pyrogram.types import *
from bot.core.db.add import add_user_to_database
from configs import OWNER_ID

@Client.on_message(filters.private & filters.command("start")) 
async def start(bot, message):
    mr = await bot.get_me() 
    await message.reply_photo(
        photo="https://graph.org/file/a0757f99b243b1df37507.jpg",
        caption=f"""Hi {message.from_user.mention}
I Can Rename Files Without Downloading And Permanent Thumb Support.

Send Me Any Files And Enjoyy""",
        reply_markup=types.InlineKeyboardMarkup([[
            InlineKeyboardButton("BOT OWNER", user_id=OWNER_ID),
            InlineKeyboardButton("UPDATES", url="https://t.me/Beta_BotZ")
            ],[           
            InlineKeyboardButton("SHOW SETTINGS", callback_data="showSettings"),
            ]]
            )
        )

@Client.on_message(filters.command("help") & filters.private & ~filters.edited)
async def help_handler(c: Client, m: "types.Message"):
    if not m.from_user:
        return await m.reply_text("I don't know about you sar :(")
    await add_user_to_database(c, m)
    await c.send_flooded_message(
        chat_id=m.chat.id,
        text="I can rename media without downloading it!\n"
             "Speed depends on your media DC.\n\n"
             "Just send me media and reply to it with /rename command.\n\n"
             "To set custom thumbnail reply to any image with /set_thumbnail\n\n"
             "To see custom thumbnail press /show_thumbnail",
        reply_markup=types.InlineKeyboardMarkup([[
           types.InlineKeyboardButton("Show Settings",
                                      callback_data="showSettings")]])
    )
