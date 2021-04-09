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
            "box" : [(175,437,332,465)],
            "color"  : (166,49,58)
            },
        "classnote":{
            "box" : [(403,475,545,563)],
            "color" : (0,0,0)
            },
        "drake":{
            "box" : [(368,38,652,296),(368,368,652,652)],
            "color" : (0,0,0)
            },
        "nofear":{
            "box" : [(285,108,400,233)],
            "color" : (0,0,0)
            },
        "spider":{
            "box" : [(75,470,220,538)],
            "color" : (0,0,0)
            },
        "worthless":{
            "box" : [(98,73,333,203)],
            "color" : (0,0,0)
            },

        }

def help(update,context):
    message = """Use \list to see all available templates,
    then make a meme by doing \<template name> <text>.
    Separate multi-texts with an underscore"""
    update.message.reply_text(message)

def list_templates(update,context):
    message = "The list of templates is the following:\n"
    for key in templates:
        message+=key
        message+="\n"
    update.message.reply_text(message)

def make_meme(update,context,template):
    Nboxes = len(templates[template]["box"])
    rawtext = context.args
    fittext = [l.split(',') for l in ','.join(rawtext).split('_')]
    if len(fittext)!=Nboxes:
        update.message.reply_text("Please make sure that the number of texts matches the number of places")
        return 
    text = []
    for ip, phrase in enumerate(fittext):
        text.append("")
        for word in phrase:
            text[ip]+=word
            text[ip]+=" "
        if not text[ip]: text = "YOUR TEXT HERE "
        text[ip] = text[ip][0:-1]
    color = templates[template]["color"]
    img = Image.open('Templates/{}.png'.format(template))
    draw = ImageDraw.Draw(img)
    boxes = templates[template]["box"]
    for ib, box in enumerate(boxes):
        x1,y1,x2,y2 = box
        Dx = x2-x1
        Dy = y2-y1
        wrap,size = BU.get_wrapped_text(text[ib],draw,Dx,Dy)
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
