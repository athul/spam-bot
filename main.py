from fastapi import FastAPI, Request
from telegram.chatpermissions import ChatPermissions
from telegram.ext import Dispatcher, CommandHandler, CallbackContext
from telegram import Update, Bot
from deta import Deta
import os
import time

db = Deta(os.getenv("PROJECT_KEY")).Base("redb")

TOKEN: str = os.getenv("TOKEN")
YARBASH:str = os.getenv("BASHETTAN")


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
            return f"Re Count Updated for @{username}\.\n\n Re adikunne kollam".replace(
                "_", "\_") if re else username.replace("_", "\_")
        else:
            return "Uvva, nee enikkit thanne adi"
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
    upd.message.reply_text("Hai Friends 👋")


def handle_gkr(upd: Update, _: CallbackContext):
    upd.message.reply_text(
        "Ellavidha Premium Accountukalkum GKR ine sameepikkuka")
    upd.message.reply_sticker(open("stickers/gkr.webp", "rb").read())


def handle_quantum(upd: Update, _: CallbackContext):
    upd.message.reply_markdown_v2(
        "**Condom** related kaaryangalk\n\n SPAthan enna swayamprakhyapitha **Condom Boi\(@thetronjohnson\)** ne vilikkuka")


def handle_gawd(upd: Update, _: CallbackContext):
    upd.message.reply_sticker(open("stickers/levi.webp", 'rb').read())


def handle_wow(upd: Update, _: CallbackContext):
    upd.message.reply_audio(open("audio/wow.mp3", "rb").read())


def handle_hbd(upd: Update, _: CallbackContext):
    uname = clean_res(upd.message.text, False)
    if "Uvva" in uname:
        message = uname
    elif "User" in uname:
        message = uname
    else:
        message = f"@{uname} in SPAMFAM inte Ellavidha Janmadina Aashamsakalum. Adichupolikkkkkk"

    upd.message.reply_text(message)
    if uname != message:
        upd.message.reply_animation(open("stickers/hbd.gif", "rb").read())


def ban_yarbash(upd: Update, _: CallbackContext):
    Bot(TOKEN).restrict_chat_member(chat_id=upd.message.chat_id, user_id=YARBASH, until_date=time.time()+60, permissions=ChatPermissions(
        can_send_messages=False,
        can_send_media_messages=False
    ))
    upd.message.reply_text(
        "Yarbash is Banned for 1 minute, enn parayaan paranju")
    upd.message.reply_sticker(open("stickers/yb.webp", "rb").read())


def handle_umma(upd: Update, _: CallbackContext):
    upd.message.reply_markdown_v2("Nanni und Mayire 😍\. You're Awesome ❤️",reply_to_message_id=)


def toss_idu(upd: Update, _: CallbackContext):
    upd.message.reply_dice()


def get_dispatcher():
    bot = Bot(TOKEN)
    dp = Dispatcher(bot=bot, update_queue=None, use_context=True)
    dp.add_handler(CommandHandler("re", handle_re))
    dp.add_handler(CommandHandler("stats", restats))
    dp.add_handler(CommandHandler("pai", handle_pai))
    dp.add_handler(CommandHandler("gkr", handle_gkr))
    dp.add_handler(CommandHandler("qt", handle_quantum))
    dp.add_handler(CommandHandler("gawd", handle_gawd))
    dp.add_handler(CommandHandler("wow", handle_wow))
    dp.add_handler(CommandHandler("banyarbash", ban_yarbash))
    dp.add_handler(CommandHandler("hbd", handle_hbd))
    dp.add_handler(CommandHandler("tq", handle_umma))
    dp.add_handler(CommandHandler("dice", toss_idu))
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
        if data['message']['chat']['title'] == "SPAM":
            update = Update.de_json(data, disp.bot)
            disp.process_update(update)
    except:
        return ""


# "from": {
#                 "id": 418225867,
#                 "is_bot": false,
#                 "first_name": "Yarbash",
#                 "username": "yarb_ash"
#             },
