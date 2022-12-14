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
        [types.InlineKeyboardButton(f"πππππΌπΏ πΌπ ππππ {'β' if upload_as_doc else 'β'}",
                                    callback_data="triggerUploadMode")],

        [types.InlineKeyboardButton(f"πΌππππ πΎπΌπππππ {'β' if apply_caption else 'β'}",
                                    callback_data="triggerApplyCaption")],

        [types.InlineKeyboardButton(f"πΌππππ πΏπππΌπππ πΎπΌπππππ {'β' if caption else 'β'}",
                                    callback_data="triggerApplyDefaultCaption")],

        [types.InlineKeyboardButton("πππ πΎπππππ πΎπΌπππππ",
                                    callback_data="setCustomCaption")],

        [types.InlineKeyboardButton(f"{'πΎππΌπππ' if thumbnail else 'πππ'} πππππ½ππΌππ",
                                    callback_data="setThumbnail")]
    ]
    if thumbnail:
        buttons_markup.append([types.InlineKeyboardButton("ππππ πππππ½ππΌππ",
                                                          callback_data="showThumbnail")])
    if caption:
        buttons_markup.append([types.InlineKeyboardButton("ππππ πΎπΌπππππ",
                                                          callback_data="showCaption")])
    buttons_markup.append([types.InlineKeyboardButton("πΎππππ",
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
