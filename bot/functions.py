from telegram import ReplyKeyboardMarkup, KeyboardButton
import telegram
from bot.uz_ru import lang_dict
from app.models import *
from telegram.ext import ConversationHandler
from datetime import date, datetime
def main_menu(update, context):
    try:
        a = update.callback_query.id
        update = update.callback_query
    except:
        www= 0 # do nothing
    
    bot = context.bot
    bot.send_message(update.message.chat.id, get_word('main menu', update), reply_markup=ReplyKeyboardMarkup(keyboard=[[get_word('take ques', update)], [get_word('change lang', update)]], resize_keyboard=True))


def get_word(text, update):
    user = Bot_user.objects.get(user_id=update.message.chat.id)
    if user.lang == 'uz':
        return lang_dict[text][0]
    else:
        return lang_dict[text][1]


def is_registered(id):
    if Bot_user.objects.filter(user_id=id):
        return True
    else:
        return False
def get_user_by_id(id):
    user = Bot_user.objects.get(user_id=id)
    return user

def get_variants_for_buttons(text):
    list_ = list(str(text).split('||'))
    list_.remove('')
    r_list = [[i] for i in list_]
    return r_list

def get_variants_as_list(text):
    list_ = list(str(text).split('||'))
    list_.remove('')
    return list_

def get_variants_as_text(l):
    text_ = ''
    for i in l:
        text_ += i+'||'
    return text_


def is_start(func):
    def func_arguments(*args, **kwargs):
        try:
            lalal = args[0].message.text
            update = args[0]
        except:
           update = args[0].callback_query  
        id = update.message.chat.id
        if update.message.text == '/start':
            try:
                a_index = Answer_index.objects.get(end=False, user_id = id)
                a_index.delete()
                for a in Answer.objects.filter(date=None, user__user_id = id):
                    a.delete()
            except:
                csf = 0
            main_menu(args[0], args[1])
            return ConversationHandler.END
        else:
            return func(*args, **kwargs)
    return func_arguments


def variants_to_list(text):
    r_list = {}
    for i in list(text.split(';')):
        if i != '':
            variant, answer = i.split('=')
            r_list[variant] = answer
    return r_list

def list_to_variants(l):
    r_text = ''
    for i in l:
        r_text += '{}={};'.format(i, l[i])
    return r_text





def stop_answering(id):
    a_index = Answer_index.objects.get(user_id = id, end=False)
    a_index.end = True
    a_index.date = datetime.now()
    a_index.save()
    for a in Answer.objects.filter(user__user_id = id, date=None):
        a.date = date.today()   
        a.save()