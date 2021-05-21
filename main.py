from fastapi import FastAPI, Request
from telegram.chatpermissions import ChatPermissions
from telegram.ext import Dispatcher, CommandHandler, CallbackContext, MessageHandler
from telegram import Update, Bot
from deta import Deta
import os
import time

from telegram.ext.filters import Filters

db = Deta(os.getenv("PROJECT_KEY")).Base("redb")

TOKEN: str = os.getenv("TOKEN")
YARBASH: str = os.getenv("BASHETTAN")
SPAM: str = os.getenv("SPAM")


def insert_to_db(usn: str) -> str:
    userdata = db.get(usn)
    if userdata is None:
        _ = db.put({"key": usn, "re": 1})
        print(_)
        return "New User Added to Table"
    else:
        updates = {"re": userdata["re"] + 1}
        db.update(updates, usn)
        return "Re Count Updated"


def clean_res(message, re: bool = True) -> str:
    if "@" in message:
        username = message.split()[1].replace("@", "")
        if username != "spam_re_mon_bot":
            print(insert_to_db(username))
            return f"Re Count Updated for @{username}\.\n\n Re അടിക്കുന്നത് കൊള്ളാം".replace(
                "_", "\_") if re else username.replace("_", "\_")
        else:
            return "ഉവ്വ, നീ എനിക്കിട്ട് തന്നെ അടി "
    else:
        return "Username thaado"


def handle_re(bot: Update, _: CallbackContext):
    message = bot.message.text
    res = clean_res(message)
    bot.message.reply_markdown_v2(res)


def restats(upd: Update, _: CallbackContext):
    stats = next(db.fetch())
    ll = [f"@{r['key']}: {r['re']}" for r in stats]
    data = "\n".join(ll)
    message = "```text\nTotal Stats\n----- -----\n\n"+data+"\n```\n"
    upd.message.reply_markdown_v2(text=message)


def handle_pai(upd: Update, _: CallbackContext):
    try:
        upd.message.reply_text(
            "Hai Friends 👋", reply_to_message_id=upd.message.reply_to_message.message_id)
    except:
        upd.message.reply_text("Hai Friends 👋")


def handle_kween(upd: Update, _: CallbackContext):
    try:
        upd.message.reply_text(
            "അലവലാതി", reply_to_message_id=upd.message.reply_to_message.message_id)
    except:
        upd.message.reply_text("അലവലാതി")


def handle_abru(upd: Update, _: CallbackContext):
    try:
        upd.message.reply_text(
            "ഞാൻ നന്നായി guis", reply_to_message_id=upd.message.reply_to_message.message_id)
    except:
        upd.message.reply_text("ഞാൻ നന്നായി guis")


def handle_githuboli(upd: Update, _: CallbackContext):
    try:
        upd.message.reply_text(
            "എന്നാ ഉണ്ട് ആശാനേ", reply_to_message_id=upd.message.reply_to_message.message_id)
    except:
        upd.message.reply_text("എന്നാ ഉണ്ട് ആശാനേ")


def handle_gkr(upd: Update, _: CallbackContext):
    upd.message.reply_text(
        "എല്ലാവിധ Premium Accountukalkum GKR'ne സമീപിക്കുക")
    upd.message.reply_sticker(open("stickers/gkr.webp", "rb").read())


def handle_quantum(upd: Update, _: CallbackContext):
    upd.message.reply_markdown_v2(
        "**Condom** related കാര്യങ്ങൾക്കു\n\n SPAthan എന്ന സ്വയംപ്രഖ്യാപിത **Condom Boi\(@thetronjohnson\)** ne vilikkuka")


def handle_gawd(upd: Update, _: CallbackContext):
    try:
        upd.message.reply_sticker(open("stickers/levi.webp", 'rb').read(),
                                  reply_to_message_id=upd.message.reply_to_message.message_id)
    except:
        upd.message.reply_sticker(open("stickers/levi.webp", 'rb').read())


def handle_wow(upd: Update, _: CallbackContext):
    upd.message.reply_audio(open("audio/wow.mp3", "rb").read(),
                            reply_to_message_id=upd.message.reply_to_message.message_id)


def handle_hbd(upd: Update, _: CallbackContext):
    uname = clean_res(upd.message.text, False)
    if "Uvva" in uname:
        message = uname
    elif "User" in uname:
        message = uname
    else:
        message = f"@{uname} in സ്പാം കുടുംബത്തിന്റെ എല്ലാവിധ ജന്മദിനാശംസകൾ... അടിച്ചു പോളിയ്ക്ക്"

    upd.message.reply_text(message)
    if uname != message:
        upd.message.reply_animation(open("stickers/hbd.gif", "rb").read())


def ban_yarbash(upd: Update, _: CallbackContext):
    bot = Bot(TOKEN)
    bot.restrict_chat_member(chat_id=upd.message.chat_id, user_id=YARBASH, until_date=time.time()+60, permissions=ChatPermissions(
        can_send_messages=False,
        can_send_media_messages=False
    ))
    try:
        bot.restrict_chat_member(chat_id=upd.message.chat_id, user_id=upd.message.from_user.id, until_date=time.time()+120, permissions=ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False
        ))
    except:
        pass
    upd.message.reply_text(
        f"Yarbash and @{upd.message.from_user.username} are Banned for 1 minute, എന്ന് പറയാൻ പറഞ്ഞു")
    upd.message.reply_sticker(open("stickers/yb.webp", "rb").read())
 
def ban_someone(upd: Update, _: CallbackContext):
    bot = Bot(TOKEN)
    uname = clean_res(upd.message.text, False)
    try:
        bot.restrict_chat_member(chat_id=upd.message.chat_id, user_id=uname, until_date=time.time()+60, permissions=ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False
        ))
        bot.restrict_chat_member(chat_id=upd.message.chat_id, user_id=upd.message.from_user.id, until_date=time.time()+120, permissions=ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False
        ))
    except:
        pass
    upd.message.reply_text(
        f"@{uname} and @{upd.message.from_user.username} are Banned for 1 minute, എന്ന് പറയാൻ പറഞ്ഞു")
    

def handle_umma(upd: Update, _: CallbackContext):
    upd.message.reply_text("നന്ദി ഉണ്ട് മയിരേ...😍 You're Awesome ❤️",
                           reply_to_message_id=upd.message.reply_to_message.message_id)


def toss_idu(upd: Update, _: CallbackContext):
    upd.message.reply_dice()


def handle_pewer(upd: Update, _: CallbackContext):
    try:
        upd.message.reply_text(
            "⚡️", reply_to_message_id=upd.message.reply_to_message.message_id)
    except:
        upd.message.reply_text("⚡️")


def respond_with_frande(upd: Update, _: CallbackContext):
    txt: str = (upd.message.text).lower().split()
    is_bot: bool = upd.message.from_user.is_bot
    words = ['hi', 'hello', 'hai', 'halo', 'hella', "hallo"]
    if not is_bot and any(x in txt for x in words):
        try:
            upd.message.reply_sticker(open("stickers/frand.webp", "rb").read(
            ), reply_to_message_id=upd.message.reply_to_message.message_id)
        except:
            upd.message.reply_sticker(open("stickers/frand.webp", "rb").read())


def get_dispatcher():
    bot = Bot(TOKEN)
    dp = Dispatcher(bot=bot, update_queue=None, use_context=True)
    dp.add_handler(CommandHandler("re", handle_re))
    dp.add_handler(CommandHandler("stats", restats))
    dp.add_handler(CommandHandler("pai", handle_pai))
    dp.add_handler(CommandHandler("kween", handle_kween))
    dp.add_handler(CommandHandler("abru", handle_abru))
    dp.add_handler(CommandHandler("githuboli", handle_githuboli))
    dp.add_handler(CommandHandler("gkr", handle_gkr))
    dp.add_handler(CommandHandler("qt", handle_quantum))
    dp.add_handler(CommandHandler("gawd", handle_gawd))
    dp.add_handler(CommandHandler("wow", handle_wow))
    dp.add_handler(CommandHandler("banyarbash", ban_yarbash))
    dp.add_handler(CommandHandler("kadakkpurath", ban_someone))
    dp.add_handler(CommandHandler("hbd", handle_hbd))
    dp.add_handler(CommandHandler("tq", handle_umma))
    dp.add_handler(CommandHandler("dice", toss_idu))
    dp.add_handler(CommandHandler("pewer", handle_pewer))
    dp.add_handler(MessageHandler(Filters.text, respond_with_frande))
    return dp


disp = get_dispatcher()

app = FastAPI()


@app.get("/")
async def hello():
    return "Hallo Frande"


@app.post("/webhook")
async def handle_webhook(req: Request):
    data = await req.json()
    # update = Update.de_json(data, disp.bot)
    # disp.process_update(update)
    try:
        if "SPAM" in data['message']['chat']['title']:
            update = Update.de_json(data, disp.bot)
            disp.process_update(update)
    except:
        return ""
