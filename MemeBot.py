import logging
from telegram.ext import Updater, CommandHandler, CallbackContext
import telegram
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import functools
import sys
sys.path.append('../../BotUtils')
import Utils as BU
from pathlib import Path

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

templates = {
        "badness":{
            "box" : (175,437,332,465),
            "color"  : (166,49,58)
            },
        }

def help(update,context):
    message = """Use \list to see all available templates,
    then make a meme by doing \<template name> <text>"""

def list_templates(update,context):
    message = "The list of templates is the following:\n"
    for key in templates:
        message+=key
        message+="\n"
    update.message.reply_text(message)

def make_meme(update,context,template):
    text = ''
    for arg in context.args:
        text+=arg
        text+=" "
    text = text[0:-1]
    color = templates[template]["color"]
    x1,y1,x2,y2 = templates[template]["box"]
    Dx = x2-x1
    Dy = y2-y1
    img = Image.open('Templates/{}.png'.format(template))
    draw = ImageDraw.Draw(img)
    wrap,size = BU.get_wrapped_text(text,draw,Dx,Dy)
    draw.text((x1,y1,x2,y2),wrap,font=BU.get_font(size),fill=color)
    img.save("meme.png")
    png = open("meme.png",'rb')
    update.message.reply_photo(png)

def main():
    token = BU.getAccessToken('token.txt')
    bot = Updater(token,use_context=True)
    dispatcher = bot.dispatcher
    dispatcher.add_handler(CommandHandler("list",list_templates))
    for key in templates:
        dispatcher.add_handler(CommandHandler(key,functools.partial(make_meme,template=key)))
    bot.start_polling()
    bot.idle()

main()
