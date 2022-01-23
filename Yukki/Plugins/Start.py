import asyncio
import random
import time
from sys import version as pyver
from typing import Dict, List, Union

import psutil
from pyrogram import filters
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaPhoto, Message)

from Yukki import ASSIDS, BOT_ID, MUSIC_BOT_NAME, OWNER_ID, SUDOERS, app
from Yukki import boottime as bot_start_time
from Yukki import db, random_assistant
from Yukki.Core.PyTgCalls import Yukki
from Yukki.Database import (add_nonadmin_chat, add_served_chat,
                            blacklisted_chats, get_assistant, get_authuser,
                            get_authuser_names, get_start, is_nonadmin_chat,
                            is_served_chat, remove_active_chat,
                            remove_nonadmin_chat, save_assistant, save_start)
from Yukki.Decorators.admins import ActualAdminCB
from Yukki.Decorators.permission import PermissionCheck
from Yukki.Inline import (custommarkup, dashmarkup, setting_markup,
                          setting_markup2, start_pannel, usermarkup, volmarkup)
from Yukki.Utilities.assistant import get_assistant_details
from Yukki.Utilities.ping import get_readable_time

welcome_group = 2

__MODULE__ = "Temel Bilgiler"
__HELP__ = """


/start 
- Botu çalıştır.


/help 
- Komutlar Yardımcı Menüsünü alın.


/settings 
- Ayarları al Komutu.
"""


@app.on_message(filters.new_chat_members, group=welcome_group)
async def welcome(_, message: Message):
    chat_id = message.chat.id
    if await is_served_chat(chat_id):
        pass
    else:
        await add_served_chat(chat_id)
    for member in message.new_chat_members:
        try:
            if member.id == BOT_ID:
                if chat_id in await blacklisted_chats():
                    await message.reply_text(
                        f"Hushh, Sohbet grubunuz[{message.chat.title}] kara listeye alındı!\n\nHerhangi bir Yönetici Kullanıcısından sohbetinizi beyaz listeye almasını isteyin"
                    )
                    return await app.leave_chat(chat_id)
                _assistant = await get_assistant(message.chat.id, "assistant")
                if not _assistant:
                    ran_ass = random.choice(random_assistant)
                    assis = {
                        "saveassistant": ran_ass,
                    }
                    await save_assistant(message.chat.id, "assistant", assis)
                else:
                    ran_ass = _assistant["saveassistant"]
                (
                    ASS_ID,
                    ASS_NAME,
                    ASS_USERNAME,
                    ASS_ACC,
                ) = await get_assistant_details(ran_ass)
                out = start_pannel()
                await message.reply_text(
                    f"{MUSIC_BOT_NAME} 𝗕𝘂 𝗚𝗿𝘂𝗯𝗮 𝗚𝗲𝗹𝗱𝗶𝗴̆𝗶𝗺 𝗜̇𝗰̧𝗶𝗻 𝗖̧𝗼𝗸 𝗠𝘂𝘁𝗹𝘂𝘆𝘂𝗺\n│\n╰𝐁𝐞𝐧𝐢 𝐠𝐫𝐮𝐛𝐮𝐧𝐮𝐳𝐝𝐚 𝐲𝐨̈𝐧𝐞𝐭𝐢𝐜𝐢 𝐨𝐥𝐚𝐫𝐚𝐤 𝐭𝐚𝐧𝐢𝐭𝐢𝐧.\n│\n╰𝗔𝐤𝐬𝐢 𝐡𝐚𝐥𝐝𝐞 𝐝𝐮̈𝐳𝐠𝐮̈𝐧 𝐜̧𝐚𝐥𝐢𝐬̧𝐦𝐚𝐲𝐚𝐜𝐚𝐠̆𝐢𝐦.\n│\n╰𝗬𝗮𝗿𝗱𝗶𝗺𝗰𝗶𝗺𝗶𝗻 𝗞𝘂𝗹𝗹𝗮𝗻𝗶𝗰𝗶 𝗔𝗱𝗶:- @{ASS_USERNAME}\n│\n╰𝗬𝗮𝗿𝗱𝗶𝗺𝗰𝗶𝗺𝗶𝗻 𝗞𝘂𝗹𝗹𝗮𝗻𝗶𝗰𝗶 𝗶𝗱:- {ASS_ID}\n│\n╰𝗦𝗮𝗵𝗶𝗯𝗶𝗺:- @{OWNER_ID}",
                    reply_markup=InlineKeyboardMarkup(out[1]),
                )
            if member.id in ASSIDS:
                return await remove_active_chat(chat_id)
            if member.id in OWNER_ID:
                return await message.reply_text(
                    f"{MUSIC_BOT_NAME}'𝘂𝗻 𝗦𝗮𝗵𝗶𝗯𝗶[{member.mention}] 𝗚𝗿𝘂𝗯𝘂𝗻𝘂𝘇𝗮 𝗸𝗮𝘁𝗶𝗹𝗱𝗶 𝗦̧𝗮𝗻𝘀𝗹𝗶𝘀𝗶𝗻𝗶𝘇."
                )
            if member.id in SUDOERS:
                return await message.reply_text(
                    f"{MUSIC_BOT_NAME}'𝘂𝗻 𝗬𝗼̈𝗻𝗲𝘁𝗶𝗰𝗶𝘀𝗶[{member.mention}] 𝗚𝗿𝘂𝗯𝘂𝗻𝘂𝘇𝗮 𝗸𝗮𝘁𝗶𝗹𝗱𝗶 𝗦̧𝗮𝗻𝘀𝗹𝗶𝘀𝗶𝗻𝗶𝘇."
                )
            return
        except:
            return


@app.on_message(filters.command(["help", "start"]) & filters.group)
@PermissionCheck
async def useradd(_, message: Message):
    out = start_pannel()
    await asyncio.gather(
        message.delete(),
        message.reply_text(
            f"𝗕𝗲𝗻𝗶 𝗶𝗰̧𝗲𝗿𝗶 𝗮𝗹𝗱𝗶𝗴̆𝗶𝗻𝗶𝘇 𝗶𝗰̧𝗶𝗻 𝘁𝗲𝘀̧𝗲𝗸𝗸𝘂̈𝗿𝗹𝗲𝗿 {message.chat.title}.\n│\n╰{MUSIC_BOT_NAME} 𝗬𝗮𝘀̧𝗶𝘆𝗼𝗿.\n│\n╰𝐇𝐞𝐫𝐡𝐚𝐧𝐠𝐢 𝐛𝐢𝐫 𝐲𝐚𝐫𝐝𝐢𝐦 𝐯𝐞𝐲𝐚 𝐲𝐚𝐫𝐝𝐢𝐦 𝐢𝐜̧𝐢𝐧 𝐝𝐞𝐬𝐭𝐞𝐤 𝐠𝐫𝐮𝐛𝐮𝐦𝐮𝐳𝐚 𝐯𝐞 𝐤𝐚𝐧𝐚𝐥𝐢𝐦𝐢𝐳𝐚 𝐠𝐨̈𝐳 𝐚𝐭𝐢𝐧.",
            reply_markup=InlineKeyboardMarkup(out[1]),
        ),
    )


@app.on_message(filters.command("settings") & filters.group)
@PermissionCheck
async def settings(_, message: Message):
    c_id = message.chat.id
    _check = await get_start(c_id, "assistant")
    if not _check:
        assis = {
            "volume": 100,
        }
        await save_start(c_id, "assistant", assis)
        volume = 100
    else:
        volume = _check["volume"]
    text, buttons = setting_markup2()
    await asyncio.gather(
        message.delete(),
        message.reply_text(
            f"{text}\n│\n╰**𝗚𝗿𝘂𝗽:** {message.chat.title}\n│\n╰**𝗚𝗿𝘂𝗽 𝗶𝗱:** {message.chat.id}\n│\n╰**𝗦𝗲𝘀 𝗦𝗲𝘃𝗶𝘆𝗲𝘀𝗶:** {volume}%",
            reply_markup=InlineKeyboardMarkup(buttons),
        ),
    )


@app.on_callback_query(filters.regex("okaybhai"))
async def okaybhai(_, CallbackQuery):
    await CallbackQuery.answer("𝗚𝗲𝗿𝗶 𝗗𝗼̈𝗻𝘂̈𝘆𝗼𝗿𝘂𝗺...")
    out = start_pannel()
    await CallbackQuery.edit_message_text(
        text=f"𝗕𝗲𝗻𝗶 𝗮𝗴̆𝗶𝗿𝗹𝗮𝗱𝗶𝗴̆𝗶𝗻𝗶𝘇 𝗶𝗰̧𝗶𝗻 𝘁𝗲𝘀̧𝗲𝗸𝗸𝘂̈𝗿 𝗲𝗱𝗲𝗿𝗶𝗺 {CallbackQuery.message.chat.title}.\n│\n╰{MUSIC_BOT_NAME}𝐡𝐚𝐥𝐚 𝐚𝐲𝐚𝐤𝐭𝐚.\n│\n╰𝗛𝗲𝗿𝗵𝗮𝗻𝗴𝗶 𝗯𝗶𝗿 𝘆𝗮𝗿𝗱𝗶𝗺 𝘃𝗲𝘆𝗮 𝘆𝗮𝗿𝗱𝗶𝗺 𝗶𝗰̧𝗶𝗻 𝗱𝗲𝘀𝘁𝗲𝗸 𝗴𝗿𝘂𝗯𝘂𝗺𝘂𝘇𝗮 𝘃𝗲 𝗸𝗮𝗻𝗮𝗹𝗶𝗺𝗶𝘇𝗮 𝗴𝗼̈𝘇 𝗮𝘁𝗶𝗻.",
        reply_markup=InlineKeyboardMarkup(out[1]),
    )


@app.on_callback_query(filters.regex("settingm"))
async def settingm(_, CallbackQuery):
    await CallbackQuery.answer("Bot Ayarları ...")
    text, buttons = setting_markup()
    c_title = CallbackQuery.message.chat.title
    c_id = CallbackQuery.message.chat.id
    chat_id = CallbackQuery.message.chat.id
    _check = await get_start(c_id, "assistant")
    if not _check:
        assis = {
            "volume": 100,
        }
        await save_start(c_id, "assistant", assis)
        volume = 100
    else:
        volume = _check["volume"]
    await CallbackQuery.edit_message_text(
        text=f"{text}\n│\n╰**𝗚𝗿𝘂𝗽:** {c_title}\n│\n╰**𝗚𝗿𝘂𝗽 𝗶𝗱:** {c_id}\n│\n╰**𝗦𝗲𝘀 𝗗𝘂̈𝘇𝗲𝘆𝗶:** {volume}%",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex("EVE"))
@ActualAdminCB
async def EVE(_, CallbackQuery):
    checking = CallbackQuery.from_user.username
    text, buttons = usermarkup()
    chat_id = CallbackQuery.message.chat.id
    is_non_admin = await is_nonadmin_chat(chat_id)
    if not is_non_admin:
        await CallbackQuery.answer("Değişiklikler Kaydedildi")
        await add_nonadmin_chat(chat_id)
        await CallbackQuery.edit_message_text(
            text=f"{text}\n│\n╰Yönetici Komutları Modu **Herkes**\n│\n╰Şimdi bu grup mevcut herkes atla, durdur, müzik durduramaz.\n│\n╰Tarafından Yapılan Değişiklikler @{checking}",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        await CallbackQuery.answer(
            "𝗞𝗼𝗺𝘂𝘁𝗹𝗮𝗿 𝗠𝗼𝗱𝘂 𝗭𝗮𝘁𝗲𝗻 𝗛𝗘𝗥𝗞𝗘𝗦𝗘 𝗔𝘆𝗮𝗿𝗹𝗮𝗻𝗱𝗶", show_alert=True
        )


@app.on_callback_query(filters.regex("AMS"))
@ActualAdminCB
async def AMS(_, CallbackQuery):
    checking = CallbackQuery.from_user.username
    text, buttons = usermarkup()
    chat_id = CallbackQuery.message.chat.id
    is_non_admin = await is_nonadmin_chat(chat_id)
    if not is_non_admin:
        await CallbackQuery.answer(
            "𝐊𝐨𝐦𝐮𝐭𝐥𝐚𝐫 𝐌𝐨𝐝𝐮 𝐙𝐚𝐭𝐞𝐧 𝐘𝐀𝐋𝐍𝐈𝐙𝐂𝐀 𝐘𝐎̈𝐍𝐄𝐓𝐈̇𝐂𝐈̇𝐋𝐄𝐑 𝐎𝐥𝐚𝐫𝐚𝐤 𝐀𝐲𝐚𝐫𝐥𝐚𝐧𝐝𝐢", show_alert=True
        )
    else:
        await CallbackQuery.answer("Değişiklikler Kaydedildi")
        await remove_nonadmin_chat(chat_id)
        await CallbackQuery.edit_message_text(
            text=f"{text}\n│\n╰Komut Modunu **Yönetici olarak Ayarla**\n│\n╰Şimdi bu grup içinde mevcut sadece Yöneticiler atla, durdur, devam, müzikleri kesebilir.\n│\n╰Tarafından Yapılan Değişiklikler @{checking}",
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@app.on_callback_query(
    filters.regex(
        pattern=r"^(AQ|AV|AU|Dashboard|HV|LV|MV|HV|VAM|Custommarkup|PTEN|MTEN|PTF|MTF|PFZ|MFZ|USERLIST|UPT|CPT|RAT|DIT)$"
    )
)
async def start_markup_check(_, CallbackQuery):
    command = CallbackQuery.matches[0].group(1)
    c_title = CallbackQuery.message.chat.title
    c_id = CallbackQuery.message.chat.id
    chat_id = CallbackQuery.message.chat.id
    if command == "AQ":
        await CallbackQuery.answer("𝗭𝗮𝘁𝗲𝗻 𝗲𝗻 𝗶𝘆𝗶 𝗞𝗮𝗹𝗶𝘁𝗲𝗱𝗲", show_alert=True)
    if command == "AV":
        await CallbackQuery.answer("Bot Ayarları ...")
        text, buttons = volmarkup()
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n│\n╰**𝗚𝗿𝘂𝗽:** {c_title}\n│\n╰**𝗚𝗿𝘂𝗽 𝗶𝗱:** {c_id}\n│\n╰**𝗦𝗲𝘀 𝗦𝗲𝘃𝗶𝘆𝗲𝘀𝗶:** {volume}%\n│\n╰**𝗦𝗲𝘀 𝗞𝗮𝗹𝗶𝘁𝗲𝘀𝗶:** 𝗩𝗮𝗿𝘀𝗮𝘆𝗶𝗹𝗮𝗻 𝗘𝗻 𝗜̇𝘆𝗶",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "AU":
        await CallbackQuery.answer("Bot Settings ...")
        text, buttons = usermarkup()
        is_non_admin = await is_nonadmin_chat(chat_id)
        if not is_non_admin:
            current = "Admins Only"
        else:
            current = "Everyone"
        await CallbackQuery.edit_message_text(
            text=f"{text}\n│\n╰**𝗚𝗿𝘂𝗽:** {c_title}\n│\n╰𝗦̧𝘂 𝗔𝗻𝗱𝗮 𝗞𝗶𝗺𝗹𝗲𝗿 {MUSIC_BOT_NAME} 𝗞𝘂𝗹𝗹𝗮𝗻𝗮𝗯𝗶𝗹𝗶𝗿:- **{current}**\n│\n╰**⁉️ 𝗡𝗲𝗱𝗶𝗿 𝗯𝘂?**\n│\n╰**👥 𝗛𝗲𝗿𝗸𝗲𝘀 :-**𝗕𝘂 𝗴𝗿𝘂𝗽𝘁𝗮 𝗯𝘂𝗹𝘂𝗻𝗮𝗻 {MUSIC_BOT_NAME} 𝗸𝗼𝗺𝘂𝘁𝗹𝗮𝗿𝗶𝗻𝗶 (𝗮𝘁𝗹𝗮, 𝗱𝘂𝗿𝗱𝘂𝗿, 𝗱𝗲𝘃𝗮𝗺 𝘃𝗯.) 𝗛𝗲𝗿𝗸𝗲𝘀 𝗸𝘂𝗹𝗹𝗮𝗻𝗮𝗯𝗶𝗹𝗶𝗿.\n│\n╰**🙍 𝗬𝗮𝗹𝗻𝗶𝘇𝗰𝗮 𝗬𝗼̈𝗻𝗲𝘁𝗶𝗰𝗶:-**  𝐘𝐚𝐥𝐧𝐢𝐳𝐜𝐚 𝐲𝐨̈𝐧𝐞𝐭𝐢𝐜𝐢𝐥𝐞𝐫 𝐯𝐞 𝐲𝐞𝐭𝐤𝐢𝐥𝐢 𝐤𝐮𝐥𝐥𝐚𝐧𝐢𝐜𝐢𝐥𝐚𝐫 {MUSIC_BOT_NAME} 𝐤𝐨𝐦𝐮𝐭𝐥𝐚𝐫𝐢𝐧𝐢𝐧 𝐭𝐮̈𝐦𝐮̈𝐧𝐮̈ 𝐤𝐮𝐥𝐥𝐚𝐧𝐚𝐛𝐢𝐥𝐢𝐫.",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "Dashboard":
        await CallbackQuery.answer("Dashboard...")
        text, buttons = dashmarkup()
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n│\n╰**𝗚𝗿𝘂𝗽:** {c_title}\n│\n╰**𝗚𝗿𝘂𝗽 𝗶𝗱:** {c_id}\n│\n╰**𝗦𝗲𝘀 𝗦𝗲𝘃𝗶𝘆𝗲𝘀𝗶:** {volume}%\n│\n╰Check {MUSIC_BOT_NAME}'𝘂𝗻 𝗚𝗼̈𝘀𝘁𝗲𝗿𝗴𝗲 𝗧𝗮𝗯𝗹𝗼𝘀𝘂𝗻𝗱𝗮𝗸𝗶 𝗦𝗶𝘀𝘁𝗲𝗺 𝗜̇𝘀𝘁𝗮𝘁𝗶𝘀𝘁𝗶𝗸𝗹𝗲𝗿𝗶 𝗕𝘂𝗿𝗮𝗱𝗮! 𝗗𝗮𝗵𝗮 𝗳𝗮𝘇𝗹𝗮 𝗢̈𝘇𝗲𝗹𝗹𝗶𝗸 𝗰̧𝗼𝗸 𝘆𝗮𝗸𝗶𝗻𝗱𝗮 𝗲𝗸𝗹𝗲𝗻𝗲𝗰𝗲𝗸! 𝗗𝗲𝘀𝘁𝗲𝗸 𝗞𝗮𝗻𝗮𝗹𝗶𝗻𝗶 𝗞𝗼𝗻𝘁𝗿𝗼𝗹 𝗘𝘁𝗺𝗲𝘆𝗲 𝗗𝗲𝘃𝗮𝗺 𝗲𝗱𝗶𝗻.",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "Custommarkup":
        await CallbackQuery.answer("Bot Ayarları ...")
        text, buttons = custommarkup()
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n│\n╰**𝗚𝗿𝘂𝗽:** {c_title}\n│\n╰**𝗚𝗿𝘂𝗽 𝗶𝗱:** {c_id}\n│\n╰**𝗦𝗲𝘀 𝗦𝗲𝘃𝗶𝘆𝗲𝘀𝗶:** {volume}%\n│\n╰**𝗦𝗲𝘀 𝗞𝗮𝗹𝗶𝘁𝗲𝘀𝗶:** 𝗩𝗮𝗿𝘀𝗮𝘆𝗶𝗹𝗮𝗻 𝗘𝗻 𝗜̇𝘆𝗶",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "LV":
        assis = {
            "volume": 25,
        }
        volume = 25
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("𝗦𝗲𝘀 𝗗𝗲𝗴̆𝗶𝘀̧𝗶𝗸𝗹𝗶𝗸𝗹𝗲𝗿𝗶𝗻𝗶 𝗔𝘆𝗮𝗿𝗹𝗮𝗺𝗮 ...")
        except:
            return await CallbackQuery.answer("𝗘𝘁𝗸𝗶𝗻 𝗦𝗲𝘀𝗹𝗶 𝗦𝗼𝗵𝗯𝗲𝘁 𝘆𝗼𝗸...")
        await save_start(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n│\n╰**𝗚𝗿𝘂𝗽:** {c_title}\n│\n╰**𝗚𝗿𝘂𝗽 𝗶𝗱:** {c_id}\n│\n╰**𝗦𝗲𝘀 𝗦𝗲𝘃𝗶𝘆𝗲𝘀𝗶:** {volume}%\n│\n╰**𝗦𝗲𝘀 𝗞𝗮𝗹𝗶𝘁𝗲𝘀𝗶:** 𝗩𝗮𝗿𝘀𝗮𝘆𝗶𝗹𝗮𝗻 𝗘𝗻 𝗜̇𝘆𝗶",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MV":
        assis = {
            "volume": 50,
        }
        volume = 50
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("𝗦𝗲𝘀 𝗗𝗲𝗴̆𝗶𝘀̧𝗶𝗸𝗹𝗶𝗸𝗹𝗲𝗿𝗶𝗻𝗶 𝗔𝘆𝗮𝗿𝗹𝗮𝗺𝗮 ...")
        except:
            return await CallbackQuery.answer("𝗘𝘁𝗸𝗶𝗻 𝗦𝗲𝘀𝗹𝗶 𝗦𝗼𝗵𝗯𝗲𝘁 𝘆𝗼𝗸...")
        await save_start(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n│\n╰**𝗚𝗿𝘂𝗽:** {c_title}\n│\n╰**𝗚𝗿𝘂𝗽 𝗶𝗱:** {c_id}\n│\n╰**𝗦𝗲𝘀 𝗦𝗲𝘃𝗶𝘆𝗲𝘀𝗶:** {volume}%\n│\n╰**𝗦𝗲𝘀 𝗞𝗮𝗹𝗶𝘁𝗲𝘀𝗶:** 𝗩𝗮𝗿𝘀𝗮𝘆𝗶𝗹𝗮𝗻 𝗘𝗻 𝗜̇𝘆𝗶",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "HV":
        assis = {
            "volume": 100,
        }
        volume = 100
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("𝗦𝗲𝘀 𝗗𝗲𝗴̆𝗶𝘀̧𝗶𝗸𝗹𝗶𝗸𝗹𝗲𝗿𝗶𝗻𝗶 𝗔𝘆𝗮𝗿𝗹𝗮𝗺𝗮 ...")
        except:
            return await CallbackQuery.answer("𝗘𝘁𝗸𝗶𝗻 𝗦𝗲𝘀𝗹𝗶 𝗦𝗼𝗵𝗯𝗲𝘁 𝘆𝗼𝗸...")
        await save_start(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n│\n╰**𝗚𝗿𝘂𝗽:** {c_title}\n│\n╰**𝗚𝗿𝘂𝗽 𝗶𝗱:** {c_id}\n│\n╰**𝗦𝗲𝘀 𝗦𝗲𝘃𝗶𝘆𝗲𝘀𝗶:** {volume}%\n│\n╰**𝗦𝗲𝘀 𝗞𝗮𝗹𝗶𝘁𝗲𝘀𝗶:** 𝗩𝗮𝗿𝘀𝗮𝘆𝗶𝗹𝗮𝗻 𝗘𝗻 𝗜̇𝘆𝗶",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "VAM":
        assis = {
            "volume": 200,
        }
        volume = 200
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("𝗦𝗲𝘀 𝗗𝗲𝗴̆𝗶𝘀̧𝗶𝗸𝗹𝗶𝗸𝗹𝗲𝗿𝗶𝗻𝗶 𝗔𝘆𝗮𝗿𝗹𝗮𝗺𝗮 ...")
        except:
            return await CallbackQuery.answer("𝗘𝘁𝗸𝗶𝗻 𝗦𝗲𝘀𝗹𝗶 𝗦𝗼𝗵𝗯𝗲𝘁 𝘆𝗼𝗸...")
        await save_start(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n│\n╰**𝗚𝗿𝘂𝗽:** {c_title}\n│\n╰**𝗚𝗿𝘂𝗽 𝗶𝗱:** {c_id}\n│\n╰**𝗦𝗲𝘀 𝗦𝗲𝘃𝗶𝘆𝗲𝘀𝗶:** {volume}%\n│\n╰**𝗦𝗲𝘀 𝗞𝗮𝗹𝗶𝘁𝗲𝘀𝗶:** 𝗩𝗮𝗿𝘀𝗮𝘆𝗶𝗹𝗮𝗻 𝗘𝗻 𝗜̇𝘆𝗶",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "PTEN":
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        volume = volume + 10
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("𝗦𝗲𝘀 𝗗𝗲𝗴̆𝗶𝘀̧𝗶𝗸𝗹𝗶𝗸𝗹𝗲𝗿𝗶𝗻𝗶 𝗔𝘆𝗮𝗿𝗹𝗮𝗺𝗮 ...")
        except:
            return await CallbackQuery.answer("𝗘𝘁𝗸𝗶𝗻 𝗦𝗲𝘀𝗹𝗶 𝗦𝗼𝗵𝗯𝗲𝘁 𝘆𝗼𝗸...")
        await save_start(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n│\n╰**𝗚𝗿𝘂𝗽:** {c_title}\n│\n╰**𝗚𝗿𝘂𝗽 𝗶𝗱:** {c_id}\n│\n╰**𝗦𝗲𝘀 𝗦𝗲𝘃𝗶𝘆𝗲𝘀𝗶:** {volume}%\n│\n╰**𝗦𝗲𝘀 𝗞𝗮𝗹𝗶𝘁𝗲𝘀𝗶:** 𝗩𝗮𝗿𝘀𝗮𝘆𝗶𝗹𝗮𝗻 𝗘𝗻 𝗜̇𝘆𝗶",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MTEN":
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        volume = volume - 10
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("𝗦𝗲𝘀 𝗗𝗲𝗴̆𝗶𝘀̧𝗶𝗸𝗹𝗶𝗸𝗹𝗲𝗿𝗶𝗻𝗶 𝗔𝘆𝗮𝗿𝗹𝗮𝗺𝗮 ...")
        except:
            return await CallbackQuery.answer("𝗘𝘁𝗸𝗶𝗻 𝗦𝗲𝘀𝗹𝗶 𝗦𝗼𝗵𝗯𝗲𝘁 𝘆𝗼𝗸...")
        await save_start(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n│\n╰**𝗚𝗿𝘂𝗽:** {c_title}\n│\n╰**𝗚𝗿𝘂𝗽 𝗶𝗱:** {c_id}\n│\n╰**𝗦𝗲𝘀 𝗦𝗲𝘃𝗶𝘆𝗲𝘀𝗶:** {volume}%\n│\n╰**𝗦𝗲𝘀 𝗞𝗮𝗹𝗶𝘁𝗲𝘀𝗶:** 𝗩𝗮𝗿𝘀𝗮𝘆𝗶𝗹𝗮𝗻 𝗘𝗻 𝗜̇𝘆𝗶",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "PTF":
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        volume = volume + 25
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("𝗦𝗲𝘀 𝗗𝗲𝗴̆𝗶𝘀̧𝗶𝗸𝗹𝗶𝗸𝗹𝗲𝗿𝗶𝗻𝗶 𝗔𝘆𝗮𝗿𝗹𝗮𝗺𝗮 ...")
        except:
            return await CallbackQuery.answer("𝗘𝘁𝗸𝗶𝗻 𝗦𝗲𝘀𝗹𝗶 𝗦𝗼𝗵𝗯𝗲𝘁 𝘆𝗼𝗸...")
        await save_start(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n│\n╰**𝗚𝗿𝘂𝗽:** {c_title}\n│\n╰**𝗚𝗿𝘂𝗽 𝗶𝗱:** {c_id}\n│\n╰**𝗦𝗲𝘀 𝗦𝗲𝘃𝗶𝘆𝗲𝘀𝗶:** {volume}%\n│\n╰**𝗦𝗲𝘀 𝗞𝗮𝗹𝗶𝘁𝗲𝘀𝗶:** 𝗩𝗮𝗿𝘀𝗮𝘆𝗶𝗹𝗮𝗻 𝗘𝗻 𝗜̇𝘆𝗶",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MTF":
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        volume = volume - 25
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("𝗦𝗲𝘀 𝗗𝗲𝗴̆𝗶𝘀̧𝗶𝗸𝗹𝗶𝗸𝗹𝗲𝗿𝗶𝗻𝗶 𝗔𝘆𝗮𝗿𝗹𝗮𝗺𝗮 ...")
        except:
            return await CallbackQuery.answer("𝗘𝘁𝗸𝗶𝗻 𝗦𝗲𝘀𝗹𝗶 𝗦𝗼𝗵𝗯𝗲𝘁 𝘆𝗼𝗸...")
        await save_start(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n│\n╰**𝗚𝗿𝘂𝗽:** {c_title}\n│\n╰**𝗚𝗿𝘂𝗽 𝗶𝗱:** {c_id}\n│\n╰**𝗦𝗲𝘀 𝗦𝗲𝘃𝗶𝘆𝗲𝘀𝗶:** {volume}%\n│\n╰**𝗦𝗲𝘀 𝗞𝗮𝗹𝗶𝘁𝗲𝘀𝗶:** 𝗩𝗮𝗿𝘀𝗮𝘆𝗶𝗹𝗮𝗻 𝗘𝗻 𝗜̇𝘆𝗶",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "PFZ":
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        volume = volume + 50
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("𝗦𝗲𝘀 𝗗𝗲𝗴̆𝗶𝘀̧𝗶𝗸𝗹𝗶𝗸𝗹𝗲𝗿𝗶𝗻𝗶 𝗔𝘆𝗮𝗿𝗹𝗮𝗺𝗮 ...")
        except:
            return await CallbackQuery.answer("𝗘𝘁𝗸𝗶𝗻 𝗦𝗲𝘀𝗹𝗶 𝗦𝗼𝗵𝗯𝗲𝘁 𝘆𝗼𝗸...")
        await save_start(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n│\n╰**𝗚𝗿𝘂𝗽:** {c_title}\n│\n╰**𝗚𝗿𝘂𝗽 𝗶𝗱:** {c_id}\n│\n╰**𝗦𝗲𝘀 𝗦𝗲𝘃𝗶𝘆𝗲𝘀𝗶:** {volume}%\n│\n╰**𝗦𝗲𝘀 𝗞𝗮𝗹𝗶𝘁𝗲𝘀𝗶:** 𝗩𝗮𝗿𝘀𝗮𝘆𝗶𝗹𝗮𝗻 𝗘𝗻 𝗜̇𝘆𝗶",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MFZ":
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        volume = volume - 50
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("𝗦𝗲𝘀 𝗗𝗲𝗴̆𝗶𝘀̧𝗶𝗸𝗹𝗶𝗸𝗹𝗲𝗿𝗶𝗻𝗶 𝗔𝘆𝗮𝗿𝗹𝗮𝗺𝗮 ...")
        except:
            return await CallbackQuery.answer("𝗘𝘁𝗸𝗶𝗻 𝗦𝗲𝘀𝗹𝗶 𝗦𝗼𝗵𝗯𝗲𝘁 𝘆𝗼𝗸...")
        await save_start(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n│\n╰**𝗚𝗿𝘂𝗽:** {c_title}\n│\n╰**𝗚𝗿𝘂𝗽 𝗶𝗱:** {c_id}\n│\n╰**𝗦𝗲𝘀 𝗦𝗲𝘃𝗶𝘆𝗲𝘀𝗶:** {volume}%\n│\n╰**𝗦𝗲𝘀 𝗞𝗮𝗹𝗶𝘁𝗲𝘀𝗶:** 𝗩𝗮𝗿𝘀𝗮𝘆𝗶𝗹𝗮𝗻 𝗘𝗻 𝗜̇𝘆𝗶",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "USERLIST":
        await CallbackQuery.answer("Auth Kullanıcıları!")
        text, buttons = usermarkup()
        _playlist = await get_authuser_names(CallbackQuery.message.chat.id)
        if not _playlist:
            return await CallbackQuery.edit_message_text(
                text=f"{text}\n\nYetkili Kullanıcı Bulunamadı\n\nYönetici olmayan herkesin yönetici komutlarımı /auth ile kullanmasına ve /unauth kullanarak silmesine izin verebilirsiniz",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        else:
            j = 0
            await CallbackQuery.edit_message_text(
                "𝗬𝗲𝘁𝗸𝗶𝗹𝗶 𝗞𝘂𝗹𝗹𝗮𝗻𝗶𝗰𝗶𝗹𝗮𝗿 𝗚𝗲𝘁𝗶𝗿𝗶𝗹𝗶𝘆𝗼𝗿... 𝗟𝘂̈𝘁𝗳𝗲𝗻 𝗕𝗲𝗸𝗹𝗲𝘆𝗶𝗻"
            )
            msg = f"**𝗬𝗲𝘁𝗸𝗶𝗹𝗶 𝗞𝘂𝗹𝗹𝗮𝗻𝗶𝗰𝗶 𝗟𝗶𝘀𝘁𝗲𝘀𝗶[AUL]:**\n\n"
            for note in _playlist:
                _note = await get_authuser(
                    CallbackQuery.message.chat.id, note
                )
                user_id = _note["auth_user_id"]
                user_name = _note["auth_name"]
                admin_id = _note["admin_id"]
                admin_name = _note["admin_name"]
                try:
                    user = await app.get_users(user_id)
                    user = user.first_name
                    j += 1
                except Exception:
                    continue
                msg += f"{j}➤ {user}[`{user_id}`]\n"
                msg += f"    ┗ 𝗧𝗮𝗿𝗮𝗳𝗶𝗻𝗱𝗮𝗻 𝗲𝗸𝗹𝗲𝗻𝗱𝗶:- {admin_name}[`{admin_id}`]\n\n"
            await CallbackQuery.edit_message_text(
                msg, reply_markup=InlineKeyboardMarkup(buttons)
            )
    if command == "UPT":
        bot_uptimee = int(time.time() - bot_start_time)
        Uptimeee = f"{get_readable_time((bot_uptimee))}"
        await CallbackQuery.answer(
            f"𝗕𝗼𝘁𝘂𝗻 𝗖̧𝗮𝗹𝗶𝘀̧𝗺𝗮 𝗦𝘂̈𝗿𝗲𝘀𝗶: {Uptimeee}", show_alert=True
        )
    if command == "CPT":
        cpue = psutil.cpu_percent(interval=0.5)
        await CallbackQuery.answer(
            f"𝗕𝗼𝘁𝘂𝗻 𝗖𝗽𝘂 𝗞𝘂𝗹𝗹𝗮𝗻𝗶𝗺𝗶: {cpue}%", show_alert=True
        )
    if command == "RAT":
        meme = psutil.virtual_memory().percent
        await CallbackQuery.answer(
            f"𝗕𝗼𝘁𝘂𝗻 𝗕𝗲𝗹𝗹𝗲𝗸 𝗞𝘂𝗹𝗹𝗮𝗻𝗶𝗺𝗶: {meme}%", show_alert=True
        )
    if command == "DIT":
        diske = psutil.disk_usage("/").percent
        await CallbackQuery.answer(
            f"𝗗𝗶𝘀𝗸 𝗞𝘂𝗹𝗹𝗮𝗻𝗶𝗺𝗶: {diske}%", show_alert=True
        )
