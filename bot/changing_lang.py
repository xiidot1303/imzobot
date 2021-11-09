from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler

from app.models import *
from bot.conversationList import *
from bot.functions import *


def change_lang(update, context):
    bot = context.bot
    current_lang = Bot_user.objects.get(user_id=update.message.chat.id).lang
    if current_lang == 'uz':
        uz_text = 'UZ \U0001F1FA\U0001F1FF   ✅'
        ru_text = 'RU \U0001F1F7\U0001F1FA'
    else:
        uz_text = 'UZ \U0001F1FA\U0001F1FF'
        ru_text = 'RU \U0001F1F7\U0001F1FA    ✅'
    
    i_uz = InlineKeyboardButton(text=uz_text, callback_data='set_lang_uz')
    i_ru = InlineKeyboardButton(text=ru_text, callback_data='set_lang_ru')
    i_back = InlineKeyboardButton(get_word('back', update), callback_data='back_main_menu')
    del_msg = update.message.reply_text(get_word('select lang', update), reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    bot.delete_message(update.message.chat.id, del_msg.message_id)
    bot.send_message(update.message.chat.id, get_word('select lang', update), reply_markup = InlineKeyboardMarkup([[i_uz], [i_ru], [i_back]]))
    return CLICK_LANG

@is_start
def click_lang(update, context):
    update = update.callback_query
    bot = context.bot
    data = str(update.data)
    user = Bot_user.objects.get(user_id=update.message.chat.id)
    if data == 'set_lang_uz':
        user.lang = 'uz'
        user.save()
    elif data == 'set_lang_ru':
        user.lang = 'ru'
        user.save()
    elif data == 'back_main_menu':
        bot.delete_message(update.message.chat.id, update.message.message_id)
        main_menu(update, context)
        return ConversationHandler.END
    current_lang = user.lang
    if current_lang == 'uz':
        uz_text = 'UZ \U0001F1FA\U0001F1FF   ✅'
        ru_text = 'RU \U0001F1F7\U0001F1FA'
    else:
        uz_text = 'UZ \U0001F1FA\U0001F1FF'
        ru_text = 'RU \U0001F1F7\U0001F1FA    ✅'
    
    i_uz = InlineKeyboardButton(text=uz_text, callback_data='set_lang_uz')
    i_ru = InlineKeyboardButton(text=ru_text, callback_data='set_lang_ru')
    i_back = InlineKeyboardButton(get_word('back', update), callback_data='back_main_menu')
    update.edit_message_text(get_word('select lang', update), reply_markup = InlineKeyboardMarkup([[i_uz], [i_ru], [i_back]]))