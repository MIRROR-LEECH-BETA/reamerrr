# (c) @AbirHasan2005

import asyncio
from pyrogram import types, errors
from configs import Config
from bot.core.db.database import db


async def show_settings(m: "types.Message"):
    usr_id = m.chat.id
    user_data = await db.get_user_data(usr_id)
    if not user_data:
        await m.edit("Failed to fetch your data from database!")
        return
    upload_as_doc = user_data.get("upload_as_doc", False)
    caption = user_data.get("caption", None)
    apply_caption = user_data.get("apply_caption", True)
    thumbnail = user_data.get("thumbnail", None)
    buttons_markup = [
        [types.InlineKeyboardButton(f"𝙐𝙋𝙇𝙊𝘼𝘿 𝘼𝙎 𝙁𝙄𝙇𝙀 {'✅' if upload_as_doc else '❌'}",
                                    callback_data="triggerUploadMode")],

        [types.InlineKeyboardButton(f"𝘼𝙋𝙋𝙇𝙔 𝘾𝘼𝙋𝙏𝙄𝙊𝙉 {'✅' if apply_caption else '❌'}",
                                    callback_data="triggerApplyCaption")],

        [types.InlineKeyboardButton(f"𝘼𝙋𝙋𝙇𝙔 𝘿𝙀𝙁𝘼𝙐𝙇𝙏 𝘾𝘼𝙋𝙏𝙄𝙊𝙉 {'❌' if caption else '✅'}",
                                    callback_data="triggerApplyDefaultCaption")],

        [types.InlineKeyboardButton("𝙎𝙀𝙏 𝘾𝙐𝙎𝙏𝙊𝙈 𝘾𝘼𝙋𝙏𝙄𝙊𝙉",
                                    callback_data="setCustomCaption")],

        [types.InlineKeyboardButton(f"{'𝘾𝙃𝘼𝙉𝙂𝙀' if thumbnail else '𝙎𝙀𝙏'} 𝙏𝙃𝙐𝙈𝘽𝙉𝘼𝙄𝙇",
                                    callback_data="setThumbnail")]
    ]
    if thumbnail:
        buttons_markup.append([types.InlineKeyboardButton("𝙎𝙃𝙊𝙒 𝙏𝙃𝙐𝙈𝘽𝙉𝘼𝙇𝙄",
                                                          callback_data="showThumbnail")])
    if caption:
        buttons_markup.append([types.InlineKeyboardButton("𝙎𝙃𝙊𝙒 𝘾𝘼𝙋𝙏𝙄𝙊𝙉",
                                                          callback_data="showCaption")])
    buttons_markup.append([types.InlineKeyboardButton("𝘾𝙇𝙊𝙎𝙀",
                                                      callback_data="closeMessage")])

    try:
        await m.edit(
            text="**Here you can setup your settings:**",
            reply_markup=types.InlineKeyboardMarkup(buttons_markup),
            disable_web_page_preview=True,
            parse_mode="Markdown"
        )
    except errors.MessageNotModified: pass
    except errors.FloodWait as e:
        await asyncio.sleep(e.x)
        await show_settings(m)
    except Exception as err:
        Config.LOGGER.getLogger(__name__).error(err)
