from app.models import *
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from bot.conversationList import *
from telegram.ext import ConversationHandler
from bot.functions import *


def select_lang(update, context):
    text = update.message.text
    if 'UZ' in text:
        Bot_user.objects.get_or_create(user_id=update.message.chat.id, lang='uz')
        update.message.reply_text(get_word('type name', update), reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
        return SEND_NAME
    elif 'RU' in text:
        Bot_user.objects.get_or_create(user_id=update.message.chat.id, lang='ru')
        update.message.reply_text(get_word('type name', update), reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
        return SEND_NAME
    else:
        update.message.reply_text('Bot tilini tanlang\n\nВыберите язык бота', update)


def send_name(update, context):
    obj = Bot_user.objects.get(user_id=update.message.chat.id)
    obj.name=update.message.text
    obj.save()
    i_contact = KeyboardButton(text=get_word('leave number', update), request_contact=True)
    update.message.reply_text(get_word('send number', update), reply_markup=ReplyKeyboardMarkup([[i_contact]], resize_keyboard=True))
    return SEND_CONTACT

def send_contact(update, context):
    if update.message.contact == None or not update.message.contact:
        update.message.reply_text(get_word('enter button', update))
        return SEND_CONTACT
    else:
        phone_number = update.message.contact.phone_number
    # check that phone is available or no
    is_available = Bot_user.objects.filter(phone=phone_number)
    if is_available:
        update.message.reply_text(get_word('number is logged',update))
        return SEND_CONTACT
    obj = Bot_user.objects.get(user_id=update.message.chat.id)
    obj.phone = phone_number
    obj.save()
    main_menu(update, context)
    return ConversationHandler.END


