from bot.utils import not_subscribed
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant


@Client.on_message(filters.private & filters.create(not_subscribed))
async def is_not_subscribed(client, message):
    await message.reply_text(
       text="**DUE TO OVERLOAD ONLY CHANNEL MEMBERS CAN USE ME**",
       reply_markup=InlineKeyboardMarkup([
           [ InlineKeyboardButton(text="CLICK HERE TO JOIN MY CHANNEL", url=client.invitelink)]
           ])
       )
