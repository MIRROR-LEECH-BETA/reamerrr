# (c) @AbirHasan2005

from pyrogram import types
from bot.client import Client
from bot.core.db.database import db
from bot.core.file_info import (
    get_media_file_name,
    get_media_file_size,
    get_file_type,
    get_file_attr
)
from bot.core.display import humanbytes
from bot.core.handlers.settings import show_settings

import time
import mimetypes
import traceback
from bot.client import (
    Client
)
from pyrogram import filters
from pyrogram.file_id import FileId
from pyrogram.types import Message, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from bot.core.file_info import (
    get_media_file_id,
    get_media_file_size,
    get_media_file_name,
    get_file_type,
    get_file_attr
)
from configs import Config
from bot.core.display import progress_for_pyrogram
from bot.core.db.database import db
from bot.core.db.add import add_user_to_database
from bot.core.handlers.not_big import handle_not_big
from bot.core.handlers.time_gap import check_time_gap
from bot.core.handlers.big_rename import handle_big_rename


@Client.on_callback_query()
async def cb_handlers(c: Client, cb: "types.CallbackQuery"):
    if cb.data == "showSettings":
        await cb.answer()
        await show_settings(cb.message)
    elif cb.data == "showThumbnail":
        thumbnail = await db.get_thumbnail(cb.from_user.id)
        if not thumbnail:
            await cb.answer("You didn't set any custom thumbnail!", show_alert=True)
        else:
            await cb.answer()
            await c.send_photo(cb.message.chat.id, thumbnail, "Custom Thumbnail",
                               reply_markup=types.InlineKeyboardMarkup([[
                                   types.InlineKeyboardButton("𝘿𝙀𝙇𝙀𝙏𝙀 𝙏𝙃𝙐𝙈𝘽𝙉𝘼𝙄𝙇",
                                                              callback_data="deleteThumbnail")
                               ]]))
    elif cb.data == "deleteThumbnail":
        await db.set_thumbnail(cb.from_user.id, None)
        await cb.answer("Okay, I deleted your custom thumbnail. Now I will apply default thumbnail.", show_alert=True)
        await cb.message.delete(True)
    elif cb.data == "setThumbnail":
        await cb.answer()
        await cb.message.edit("Send me any photo to set that as custom thumbnail.\n\n"
                              "Press /cancel to cancel process.")
        from_user_thumb: "types.Message" = await c.listen(cb.message.chat.id)
        if not from_user_thumb.photo:
            await cb.message.edit("Process Cancelled!")
            return await from_user_thumb.continue_propagation()
        else:
            await db.set_thumbnail(cb.from_user.id, from_user_thumb.photo.file_id)
            await cb.message.edit("Okay!\n"
                                  "Now I will apply this thumbnail to next uploads.",
                                  reply_markup=types.InlineKeyboardMarkup(
                                      [[types.InlineKeyboardButton("𝙎𝙃𝙊𝙒 𝙎𝙀𝙏𝙏𝙄𝙉𝙂𝙎",
                                                                   callback_data="showSettings")]]
                                  ))
    elif cb.data == "setCustomCaption":
        await cb.answer()
        await cb.message.edit("Okay,\n"
                              "Send me your custom caption.\n\n"
                              "Press /cancel to cancel process.")
        user_input_msg: "types.Message" = await c.listen(cb.message.chat.id)
        if not user_input_msg.text:
            await cb.message.edit("Process Cancelled!")
            return await user_input_msg.continue_propagation()
        if user_input_msg.text and user_input_msg.text.startswith("/"):
            await cb.message.edit("Process Cancelled!")
            return await user_input_msg.continue_propagation()
        await db.set_caption(cb.from_user.id, user_input_msg.text.markdown)
        await cb.message.edit("Custom Caption Added Successfully!",
                              reply_markup=types.InlineKeyboardMarkup(
                                  [[types.InlineKeyboardButton("𝙎𝙃𝙊𝙒 𝙎𝙀𝙏𝙏𝙄𝙉𝙂𝙎",
                                                               callback_data="showSettings")]]
                              ))
    elif cb.data == "triggerApplyCaption":
        await cb.answer()
        apply_caption = await db.get_apply_caption(cb.from_user.id)
        if not apply_caption:
            await db.set_apply_caption(cb.from_user.id, True)
        else:
            await db.set_apply_caption(cb.from_user.id, False)
        await show_settings(cb.message)
    elif cb.data == "triggerApplyDefaultCaption":
        await db.set_caption(cb.from_user.id, None)
        await cb.answer("Okay, now I will keep default caption.", show_alert=True)
        await show_settings(cb.message)
    elif cb.data == "showCaption":
        caption = await db.get_caption(cb.from_user.id)
        if not caption:
            await cb.answer("You didn't set any custom caption!", show_alert=True)
        else:
            await cb.answer()
            await cb.message.edit(
                text=caption,
                parse_mode="Markdown",
                reply_markup=types.InlineKeyboardMarkup([[
                    types.InlineKeyboardButton("𝘽𝘼𝘾𝙆", callback_data="showSettings")
                ]])
            )
    elif cb.data == "triggerUploadMode":
        await cb.answer()
        upload_as_doc = await db.get_upload_as_doc(cb.from_user.id)
        if upload_as_doc:
            await db.set_upload_as_doc(cb.from_user.id, False)
        else:
            await db.set_upload_as_doc(cb.from_user.id, True)
        await show_settings(cb.message)
    elif cb.data == "showFileInfo":
        replied_m = cb.message.reply_to_message
        _file_name = get_media_file_name(replied_m)
        text = f"**File Name:** `{_file_name}`\n\n" \
               f"**File Extension:** `{_file_name.rsplit('.', 1)[-1].upper()}`\n\n" \
               f"**File Type:** `{get_file_type(replied_m).upper()}`\n\n" \
               f"**File Size:** `{humanbytes(get_media_file_size(replied_m))}`\n\n" \
               f"**File MimeType:** `{get_file_attr(replied_m).mime_type}`"
        await cb.message.edit(
            text=text,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=types.InlineKeyboardMarkup(
                [[types.InlineKeyboardButton("𝘾𝙇𝙊𝙎𝙀", callback_data="closeMessage")]]
            )
        )
    elif cb.data == "closeMessage":
        await cb.message.delete(True)
    elif cb.data == "about":
        await cb.message.edit(
            parse_mode='Markdown',
            text=f"""🍁 𝐑𝐄𝐍𝐀𝐌𝐄 𝐁𝐎𝐓 🍁

🚀 OWNER : [JEOL](https://t.me/ABOUT_JEOL)
💠 SUPPORT : [BETA SUPPORT](https://t.me/BETA_SUPPORT)
📡 SERVER : [HEROKU](https://heroku.com)
🗃️ DATABASE : [MONGO DB](https://www.mongodb.com)
📚 LANGUAGE : [PYTHON 3](https://www.python.org)
🔗 LIBRARY : [PYROGRAM 1.4.16](https://docs.pyrogram.org)
❣️ SOURCE CODE: [CLICK HERE](https://github.com/AbirHasan2005/Rename-Bot)
""",
            reply_markup=types.InlineKeyboardMarkup([[types.InlineKeyboardButton("𝘾𝙇𝙊𝙎𝙀", callback_data="closeMessage")]])
        )              
    elif cb.data == "rename":
        user_id = cb.message.chat.id
        date = cb.message.date
        await cb.message.delete()
        msgs = cb.message.reply_to_message
        file = msgs.document or msgs.video or msgs.audio
        dcid = FileId.decode(file.file_id).dc_id
        file_name = get_media_file_name(msgs)
        await cb.message.reply_text(f"**◈ Current File Name :** `{file_name}`\n\n**◈ DC ID :** `{dcid}`\n\n**__Please enter the new filename with extension and reply this message..**__",	
        reply_to_message_id=cb.message.reply_to_message.message_id,  
        reply_markup=ForceReply(True))


@Client.on_message(filters.private & filters.reply)
async def rename_func(c,m):
    if (m.reply_to_message.reply_markup) and isinstance(m.reply_to_message.reply_markup, ForceReply):
        user_input_msg = m.text
        await m.delete()
        media = await c.get_messages(m.chat.id,m.reply_to_message.message_id)
        file = media.reply_to_message
        _raw_file_name = get_media_file_name(file)
        await m.reply_to_message.delete()
        editable = await m.reply_text("processing..")
        file_name = user_input_msg[:255]
        is_big = get_media_file_size(file) > (10 * 1024 * 1024)
        await editable.edit("Please Wait ...")
    if not is_big:
        _default_thumb_ = await db.get_thumbnail(m.from_user.id)
        Image.open(_default_thumb_).convert("RGB").save(_default_thumb_)
        img = Image.open(_default_thumb_)
        img.resize((320, 320))
        img.save(_default_thumb_, "JPEG")
        if not _default_thumb_:
            _m_attr = get_file_attr(file)
            _default_thumb_ = _m_attr.thumbs[0].file_id \
                if (_m_attr and _m_attr.thumbs) \
                else None
        await handle_not_big(c, m, get_media_file_id(file), file_name,
                             editable, get_file_type(file), _default_thumb_)
        return
    file_type = get_file_type(file)
    _c_file_id = FileId.decode(get_media_file_id(file))
    try:
        c_time = time.time()
        file_id = await c.custom_upload(
            file_id=_c_file_id,
            file_size=get_media_file_size(file),
            file_name=file_name,
            progress=progress_for_pyrogram,
            progress_args=(
                "Uploading ...\n"
                f"DC: {_c_file_id.dc_id}",
                editable,
                c_time
            )
        )
        if not file_id:
            return await editable.edit("Failed to Rename!\n\n"
                                       "Maybe your file corrupted :(")
        await handle_big_rename(c, m, file_id, file_name, editable, file_type)
    except Exception as err:
        print(err)
        await editable.edit("Failed to Rename File!\n\n"
                            f"**Error:** `{err}`\n\n"
                            f"**Traceback:** `{traceback.format_exc()}`")















