from fastapi import FastAPI, Request
from telegram.ext import Dispatcher, CommandHandler, CallbackContext, MessageHandler
from telegram import Update, Bot
from deta import Deta
import os
import toml
from functools import partial as __

from telegram.ext.filters import Filters


TOKEN: str = os.getenv("TOKEN")
SPAM: str = os.getenv("SPAM")


def clean_res(message, re: bool = True) -> str:
    if "@" in message:
        username = message.split()[1].replace("@", "")
        if username != "spam_re_mon_bot":
            return f"@{username} kutta, aa post Re aarunnu ketto".replace(
                "_", "\_") if re else username.replace("_", "\_")
        else:
            return "ഉവ്വ, നീ എനിക്കിട്ട് തന്നെ അടി "
    else:
        return "Username thaado"


def handle_re(bot: Update, _: CallbackContext):
    message = bot.message.text
    res = clean_res(message)
    bot.message.reply_markdown_v2(res)

def handle_one_liner(upd: Update, _: CallbackContext,message:str):
    try:
        upd.message.reply_text(message.replace(".","\."), reply_to_message_id=upd.message.reply_to_message.message_id)
        print(f"Onliner Sent for {message}")
        return 
    except:
        upd.message.reply_text(message)

def handle_sticker_only_messages(upd: Update, _: CallbackContext,sticker: str):
    try:
        upd.message.reply_sticker(open(sticker, 'rb').read(),
                                  reply_to_message_id=upd.message.reply_to_message.message_id)
        print(f"Sticker Sent for {sticker}")
    except:
        upd.message.reply_sticker(open(sticker, 'rb').read())

def handle_reply_only_onliner(upd: Update, _: CallbackContext,message: str):
    try:
        upd.message.reply_markdown_v2(message.replace(".","\.").replace("(","\(").replace(")","\)"))
        print(f"Reply Sent with {message}")
    except Exception as e:
        print(e)
    

def handle_messages_with_stickers(upd: Update, _: CallbackContext,message: str, sticker: str):
    try:
        upd.message.reply_text(message)
        upd.message.reply_sticker(open(sticker, "rb").read())
        print(f"Message and Sticker Sent for {message} and {sticker}")
    except Exception as e:
        print(e)

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

def toss_idu(upd: Update, _: CallbackContext):
    upd.message.reply_dice()


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

def handle_help(upd:Update,_: CallbackContext,message:str):
    upd.message.reply_markdown_v2(message.replace("-","\-").replace("/","\/").replace(".","\."))

data = toml.load("data.toml")

def get_dispatcher():
    bot = Bot(TOKEN)
    dp = Dispatcher(bot=bot, update_queue=None, use_context=True)
    for key,value in data["messages"]["one_liners"].items():
        dp.add_handler(CommandHandler(key, __(handle_one_liner,message=value)))

    for key,value in data["messages"]["reply_only_one_liners"].items():
        dp.add_handler(CommandHandler(key, __(handle_reply_only_onliner,message=value)))

    for key,value in data["messages"]["stickers"].items():
        dp.add_handler(CommandHandler(key, __(handle_sticker_only_messages,sticker=value)))

    for key,value in data["messages"]["messages_with_stickers"].items():
        dp.add_handler(CommandHandler(key,__(handle_messages_with_stickers,message=value[0], sticker=value[1])))

    dp.add_handler(CommandHandler("re", handle_re))
    dp.add_handler(CommandHandler("wow", handle_wow))
    dp.add_handler(CommandHandler("hbd", handle_hbd))
    dp.add_handler(CommandHandler("dice", toss_idu))
    dp.add_handler(CommandHandler("help", __(handle_help,message=data["constant"]["help"])))
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
