from typing import Text
from django.db.models.base import ModelState
from telegram import Bot
from telegram.ext import Dispatcher, ConversationHandler, PicklePersistence
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from dotenv import load_dotenv
import os
from config import TOKEN, WHERE

from bot.main import *
from bot.login import *
from bot.changing_lang import *
from bot.uz_ru import lang_dict
from bot.question_logic import *

from bot.conversationList import *

import requests

# requests.get('http://127.0.0.1:8000/1419841495:AAFniTJIRIGAd1q_F10gCquoRPchNoHSmPg')

bot_obj = Bot(TOKEN)
persistence = PicklePersistence(filename='filebot')



if WHERE == 'SERVER':
    updater = 1213
    dp = Dispatcher(bot_obj, None, workers=0, use_context=True, persistence=persistence)
else:
    
    updater = Updater(token=TOKEN, use_context=True, persistence=persistence)
    dp = updater.dispatcher



login_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states = {
        SELECT_LANG: [MessageHandler(Filters.text(['UZ 🇺🇿', 'RU 🇷🇺']), select_lang)],
        SEND_NAME: [MessageHandler(Filters.text, send_name)],
        SEND_CONTACT: [MessageHandler(Filters.all, send_contact)],
    },
    fallbacks= [],
    name='login',
    persistent=True,
)


change_lang_handler = ConversationHandler(
    entry_points = [MessageHandler(Filters.text(lang_dict['change lang']), change_lang)],
    states= {
        CLICK_LANG: [CallbackQueryHandler(click_lang), CommandHandler('start', click_lang)],
    },
    fallbacks=[],
    name = 'change_lang',
    persistent=True,
)



question_logic_handler = ConversationHandler(
    entry_points = [MessageHandler(Filters.text(lang_dict['take ques']), take_question)],
    states= {
        CONTINUE_ANSWERING: [MessageHandler(Filters.text, loop_answering)],
        INLINE_ANSWERING: [CallbackQueryHandler(inline_answering), CommandHandler('start', inline_answering)],
    },
    fallbacks=[],
    name = 'question_logic',
    persistent=True,
)







dp.add_handler(question_logic_handler)

dp.add_handler(change_lang_handler)



dp.add_handler(login_handler)