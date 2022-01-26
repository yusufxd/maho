from config import LOG_GROUP_ID
from Yukki.Core.Clients.cli import LOG_CLIENT
from Yukki.Database import is_on_off


def logging(mystic):
    async def wrapper(_, message):
        if await is_on_off(5):
            if message.chat.username:
                chatusername = f"@{message.chat.username}"
            else:
                chatusername = "Gizli Grup"
            try:
                query = message.text.split(None, 1)[1]
                what = "Query Given"
            except:
                try:
                    if not message.reply_to_message:
                        what = "Sadece Verilen Komut"
                    else:
                        what = "Herhangi bir dosyaya cevap verdi."
                except:
                    what = "Komut"
            logger_text = f"""
__**Yeni {what}**__

**Grup:** {message.chat.title} [`{message.chat.id}`]
**Kullanıcı:** {message.from_user.mention}
**KullanıcıAdı:** @{message.from_user.username}
**Kullanıcı ID:** `{message.from_user.id}`
**Grup Linki:** {chatusername}
**Sorgu:** {message.text}"""
            if LOG_CLIENT != "None":
                await LOG_CLIENT.send_message(
                    LOG_GROUP_ID,
                    f"{logger_text}",
                    disable_web_page_preview=True,
                )
        return await mystic(_, message)

    return wrapper
