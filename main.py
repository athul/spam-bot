from telegram.constants import PARSEMODE_MARKDOWN_V2
from telegram.ext import Dispatcher, CommandHandler, CallbackContext
from telegram import Update, Bot
from deta import Deta
import os

from telegram.parsemode import ParseMode

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
        if username!="spam_re_mon_bot":
            print(insert_to_db(username))
        else:
            return "Uvva, nee enikkit thanne RE adi"
        return username
    else:
        return None


def handle_re(bot: Update, _: CallbackContext):
    message = bot.message.text
    res = clean_res(message)
    mess = f"Re Count Updated for @{res}.\n\n Re adikunne kollam, Engaanum thett aanengil, suttiduve" if res != None else "Username thaado"
    if "Uvva" in res:
        mess = res
    bot.message.reply_text(mess,parse_mode=ParseMode.MARKDOWN_V2)

def restats(upd:Update,_:CallbackContext):
    stats = next(db.fetch())
    ll = [f"@{r['key']}: {r['re']}" for r in stats]
    data = "\n".join(ll)
    message = "```text\nTotal Stats\n----- -----\n\n"+data+"\n```\n"
    upd.message.reply_text(text=message,parse_mode=ParseMode.MARKDOWN_V2)

def get_dispatcher():
    bot = Bot(TOKEN)
    dp = Dispatcher(bot=bot,update_queue=None, use_context=True)
    dp.add_handler(CommandHandler("re", handle_re))
    dp.add_handler(CommandHandler("stats",restats))
    return dp


disp = get_dispatcher()
from fastapi import FastAPI,Request

app = FastAPI()

@app.get("/")
async def hello():
    return "Hallo Frande"
    
@app.post("/webhook")
async def handle_webhook(req: Request):
    data = await req.json()
    if data['message']['chat']['title'] == "SPAM":
        update = Update.de_json(data, disp.bot)
        disp.process_update(update)
    else:
        pass