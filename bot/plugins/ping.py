from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from bot.client import Client
from pyrogram import filters
from pyrogram import types
from bot.core.db.add import add_user_to_database


@Client.on_message(filters.command(["start", "ping"]) & filters.private & ~filters.edited)
async def ping_handler(c: Client, m: "types.Message"):
    await add_user_to_database(c, m)
    mr = await c.get_me() 
    await m.reply_photo(
       photo="https://graph.org/file/7f18f71076a3be3180cb3.jpg",
       caption=f"""Hi {m.from_user.mention}
Iam {mr.mention}
I Can Rename Files Without Downloading And Permanent Thumb Support.
Send Me Any Files And Enjoyy""",
       reply_markup=InlineKeyboardMarkup( [[
          InlineKeyboardButton("SUPPORT", url="t.me/beta_support"),
          InlineKeyboardButton("UPDATES", url="https://t.me/Beta_BotZ")
          ],[           
          InlineKeyboardButton("SHOW SETTINGS", callback_data="showSettings"),
          InlineKeyboardButton("ABOUT ME", callback_data="about")
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
             "To see custom thumbnail press /show_thumbnail",
        reply_markup=types.InlineKeyboardMarkup([[
           types.InlineKeyboardButton("𝙎𝙃𝙊𝙒 𝙎𝙀𝙏𝙏𝙄𝙉𝙂𝙎",
                                      callback_data="showSettings")]])
    )
