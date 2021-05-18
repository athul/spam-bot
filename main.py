from fastapi import FastAPI, Request
from telegram.ext import Dispatcher, CommandHandler, CallbackContext
from telegram import Update, Bot
from deta import Deta
import os

db = Deta(os.getenv("PROJECT_KEY")).Base("redb")

TOKEN: str = os.getenv("TOKEN")


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


def clean_res(message):
    if "@" in message:
        username = message.split()[1].replace("@", "")
        if username != "spam_re_mon_bot":
            print(insert_to_db(username))
            return username
        else:
            return "Uvva, nee enikkit thanne RE adi"
    else:
        return None


def handle_re(bot: Update, _: CallbackContext):
    message = bot.message.text
    res = clean_res(message)
    if res is None:
        mess = "Username thaado"
    elif "Uvva" in res:
        mess = res
    else:
        mess = f"Re Count Updated for @{res}\.\n\n Re adikunne kollam".replace(
            "_", "\_")
    bot.message.reply_markdown_v2(mess)


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
        "Ellavidha Premium Accountukalkum @Gautam_krish ine sameepikkuka")


def handle_quantum(upd: Update, _: CallbackContext):
    upd.message.reply_markdown_v2(
        "**Condom** related kaaryangalk\n\n SPAthan enna swayamprakhyapitha **Condom Boi\(@thetronjohnson\)** ne vilikkuka")


def handle_gawd(upd: Update, _: CallbackContext):
    with open("stickers/levi.webp", 'rb') as f:
        upd.message.reply_sticker(f.read())


def get_dispatcher():
    bot = Bot(TOKEN)
    dp = Dispatcher(bot=bot, update_queue=None, use_context=True)
    dp.add_handler(CommandHandler("re", handle_re))
    dp.add_handler(CommandHandler("stats", restats))
    dp.add_handler(CommandHandler("pai", handle_pai))
    dp.add_handler(CommandHandler("gkr", handle_gkr))
    dp.add_handler(CommandHandler("qt", handle_quantum))
    dp.add_handler(CommandHandler("gawd", handle_gawd))
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
