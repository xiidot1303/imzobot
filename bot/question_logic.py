from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
import telegram
from app.models import *
from bot.conversationList import SELECT_LANG
from bot.functions import *
from bot.conversationList import *
sections_and_questions = [
    (1, 1), (1, 2), (1, 3), 
    (2, 1), (2, 2),(2, 3),(2, 4),(2, 5),(2, 6),(2, 7),(2, 8),(2, 9),(2, 10),
    (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14), (3, 15), (3, 16), (3, 17), 
    (4, 1), (4, 2), (4, 3), (4, 4),
    (5, 1),  
]


def take_question(update, context):
    user = get_user_by_id(update.message.chat.id)
    question = Question.objects.get(sn=1, qn=1, lang=user.lang)
    keys = get_variants_for_buttons(question.qv)
    keys.append([get_word('main menu', update)])
    update.message.reply_text(str(question.qd), reply_markup=ReplyKeyboardMarkup(keyboard=keys, resize_keyboard=True))

    Answer_index.objects.get_or_create(end=False, user_id=update.message.chat.id)
    a = Answer_index.objects.get(end=False, user_id=update.message.chat.id)
    Answer.objects.create(end=False, user = user, st = question.st, sn = question.sn, qn = question.qn, index = a.pk)
    return CONTINUE_ANSWERING


alpha = ['a','b', 'c', 'd', 'e', 'f', 'g']


@is_start
def loop_answering(update, context):
    bot = context.bot
    user = get_user_by_id(update.message.chat.id)
    try:
        answer = update.data
    except:
        answer = update.message.text
    
    l_ans = Answer.objects.get(user__user_id = user.user_id, end=False)  # last answer

    l_q = Question.objects.get(sn = l_ans.sn, qn = l_ans.qn, lang=user.lang)

    if (l_ans.sn, l_ans.qn) == (5, 1):
        l_ans.ans = answer
        l_ans.end = True
        l_ans.save()
        update.message.reply_text(get_word('stop answering', update), reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
        stop_answering(update.message.chat.id)
        main_menu(update, context)
        return ConversationHandler.END 
    

    next_q = sections_and_questions[sections_and_questions.index((l_ans.sn, l_ans.qn)) + 1] # next question (sn, qn)
    is_end = True
    if answer == get_word('back', update):
        l_ans.delete()
        l_ans = Answer.objects.filter(user__user_id = user.user_id, date=None).order_by('-sn', '-qn')[0]
        next_q = sections_and_questions[sections_and_questions.index((l_ans.sn, l_ans.qn))]
        l_ans.delete()
        try:
            l_ans = Answer.objects.filter(user__user_id = user.user_id, date=None).order_by('-sn', '-qn')[0]
            answer = l_ans.ans
        except:
            take_question(update, context)
            return CONTINUE_ANSWERING
    elif not answer in l_q.qv and (l_ans.sn, l_ans.qn) != (2, 3) and (l_ans.sn, l_ans.qn) != (2, 4) and (l_ans.sn, l_ans.qn) != (2, 10)and (l_ans.sn, l_ans.qn) != (3, 2)and not ((l_ans.sn, l_ans.qn) in [(1, 2), (1, 3), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14), (3, 15), (3, 1), (4, 2), (4, 4) ]):
        update.message.reply_text(get_word('send again', update))
        return 
    elif (l_ans.sn, l_ans.qn) == (1, 2):
        try:
            m, y = answer.split('.')
            m = int(m)
            y = int(y)
            if m > 31 or y < 1000:
                update.message.reply_text(get_word('error date', update))
                return
        except:
            update.message.reply_text(get_word('error date', update))
            return 
    elif (l_ans.sn, l_ans.qn) == (2, 2):
        if get_variants_as_list(l_q.qv)[-1] == answer: # спросить тех кто не выбрал код 6 в Q2e 
            next_q = sections_and_questions[sections_and_questions.index((2, 7))] # next question (sn, qn)
    elif (l_ans.sn, l_ans.qn) == (2, 5):
        this_ans = Answer.objects.get(user__user_id = user.user_id, date=None, sn=2, qn=3)
        this_ques = Question.objects.get(sn=2, qn=3, lang=user.lang)
        if not this_ans.ans in get_variants_as_list(this_ques.qv)[:-2]: # спросить тех кто не выбрал код 6 в Q2e 
            next_q = sections_and_questions[sections_and_questions.index((2, 7))] # next question (sn, qn)
    elif (l_ans.sn, l_ans.qn) == (2, 7):
        try:
            this_ans = Answer.objects.get(user__user_id = user.user_id, date=None, sn=2, qn=3)
            this_ques = Question.objects.get(sn=2, qn=3, lang=user.lang)
            if not this_ans.ans in get_variants_as_list(this_ques.qv)[:-2]: # спросить тех кто не выбрал код 6 в Q2e 
                next_q = sections_and_questions[sections_and_questions.index((2, 9))] # next question (sn, qn)
        except:
            next_q = sections_and_questions[sections_and_questions.index((2, 9))] # next question (sn, qn)
    elif (l_ans.sn, l_ans.qn) == (2, 9):
        #check stop answering or not!
        this_ans = Answer.objects.get(user__user_id = user.user_id, date=None, sn=2, qn=2)
        this_ques = Question.objects.get(sn=2, qn=2, lang=user.lang)
        current_ques = Question.objects.get(sn=2, qn=9, lang=user.lang)
        if this_ans.ans == get_variants_as_list(this_ques.qv)[5] and answer == get_variants_as_list(current_ques.qv)[5]:
            l_ans.ans = answer
            l_ans.end = True
            l_ans.save()
            update.message.reply_text(get_word('stop answering', update), reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
            stop_answering(update.message.chat.id)
            main_menu(update, context)
            return ConversationHandler.END
        elif answer == get_variants_as_list(current_ques.qv)[5]:
            next_q = sections_and_questions[sections_and_questions.index((3, 1))] 

    elif (l_ans.sn, l_ans.qn) == (1, 3):

        if answer == get_variants_as_list(l_q.qv)[-1]:
            l_ans.ans = answer
            l_ans.end = True
            l_ans.save()
            update.message.reply_text(get_word('stop answering', update), reply_markup = ReplyKeyboardRemove(remove_keyboard=True))
            stop_answering(update.message.chat.id)
            main_menu(update, context)
            return ConversationHandler.END
        elif not answer in get_variants_as_list(l_q.qv) and answer != get_word('city_chirchik', update) and answer != get_word('city_gulistan', update):
        
            update.message.reply_text(get_word('send again', update))
            return 

    elif (l_ans.sn, l_ans.qn) == (4, 1):
        if answer != get_variants_as_list(l_q.qv)[0]:
            next_q = sections_and_questions[sections_and_questions.index((4, 3))] # next question (sn, qn)

    elif (l_ans.sn, l_ans.qn) == (4, 3):
        if answer != get_variants_as_list(l_q.qv)[0]:
            next_q = sections_and_questions[sections_and_questions.index((5, 1))] # next question (sn, qn)


    elif (l_ans.sn, l_ans.qn) in [(3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7)]:
        if answer == get_word('next', update):
            q_3_1 = Question.objects.get(lang=user.lang, sn=3, qn=1)
            a_3_1 = Answer.objects.get(date=None, user__user_id=user.user_id, sn = 3, qn = 1)
            answers = variants_to_list(a_3_1.ans)

            v, v_a = str(q_3_1.qv).split('\\')
            all_variants = get_variants_as_list(v)
            for i in all_variants[l_ans.qn-1:]:

                if i in answers:
                    if int(answers[i]) == 3:
                        break
                next_q = (next_q[0], next_q[1] + 1)
            else:
                for i in all_variants:
                    if i in answers:
                        if int(answers[i]) == 1:
                            break
                    next_q = (next_q[0], next_q[1] + 1)
        else:
            next_q = (l_ans.sn, l_ans.qn)
            if '✅' in answer:
                last_answers = get_answers_as_list(l_ans.ans)
                last_answers.remove(answer[2:])
                new_ans = get_answers_as_text(last_answers)

            else:
                new_ans = l_ans.ans + answer + ';'

            l_ans.ans = new_ans
            l_ans.save()
            is_end = False
        answer = l_ans.ans

    elif (l_ans.sn, l_ans.qn) in [(3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14), (3, 15)]:
        if answer == get_word('next', update):
            q_3_1 = Question.objects.get(lang=user.lang, sn=3, qn=1)
            a_3_1 = Answer.objects.get(date=None, user__user_id=user.user_id, sn = 3, qn = 1)
            answers = variants_to_list(a_3_1.ans)

            v, v_a = str(q_3_1.qv).split('\\')
            all_variants = get_variants_as_list(v)
            for i in all_variants[l_ans.qn-1-7:]:
                if i in answers:
                    if int(answers[i]) == 1:
                        break
                next_q = (next_q[0], next_q[1] + 1)
        else:
            next_q = (l_ans.sn, l_ans.qn)

            if '✅' in answer:
                last_answers = get_answers_as_list(l_ans.ans)
                last_answers.remove(answer[2:])
                new_ans = get_answers_as_text(last_answers)
                
            else:
                new_ans = l_ans.ans + answer + ';'
            l_ans.ans = new_ans
            l_ans.save()
            is_end = False
        answer = l_ans.ans

    elif (l_ans.sn, l_ans.qn) in [(4, 2), (4, 4)]:
        if answer != get_word('next', update):
            next_q = (l_ans.sn, l_ans.qn)

            if '✅' in answer:
                last_answers = get_answers_as_list(l_ans.ans)
                last_answers.remove(answer[2:])
                new_ans = get_answers_as_text(last_answers)
                
            else:
                new_ans = l_ans.ans + answer + ';'
            l_ans.ans = new_ans
            l_ans.save()
            is_end = False
        answer = l_ans.ans

    
    l_ans.ans = answer

    if is_end:
        l_ans.end = True
    l_ans.save()
    
    q = Question.objects.get(sn = next_q[0], qn = next_q[1], lang=user.lang) # Question
 

    # additional text
    if next_q in [(2, 3), (2, 4), (2, 10), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14), (3, 15), (4, 2), (4, 4)]:
        add_text = '\n\n' + get_word('if other', update)
        q_list = get_variants_as_list(q.qv)[:-1] # remove last variant 
        q.qv = get_variants_as_text(q_list)

    else:
        add_text = ''

    if next_q == (1, 2):
        update.message.reply_text(str(q.qd) + '  (мм.гггг)', reply_markup=ReplyKeyboardMarkup(keyboard=[[get_word('back', update)], [get_word('main menu', update)]], resize_keyboard=True))
    elif next_q == (2, 1) or next_q == (3, 1) or next_q == (3, 16) or next_q == (3, 17):
        v, v_a = str(q.qv).split('\\')
        variants = get_variants_as_list(v)
        var_answers = get_variants_as_list(v_a)
        if next_q == (3, 1) or next_q == (3, 16) or next_q == (3, 16):
            variants = []
            ans_2_1 = Answer.objects.get(user__user_id = user.user_id, date = None, sn=2, qn = 1)
            ans_list = variants_to_list(ans_2_1.ans)
            for al in ans_list:
                if int(ans_list[al]) != 4:
                    variants.append(al)
            if variants == []:
                next_q = (4, 1)
                q = Question.objects.get(sn = next_q[0], qn = next_q[1], lang=user.lang) # Question
                keys = get_variants_for_buttons(q.qv)
                keys.append([get_word('back', update)])
                keys.append([get_word('main menu', update)])
                update.message.reply_text(str(q.qd)+add_text, reply_markup=ReplyKeyboardMarkup(keyboard=keys, resize_keyboard=True))
                Answer.objects.create(index = l_ans.index, end=False, user = user, st = q.st, sn = q.sn, qn = q.qn, ans='')
                return CONTINUE_ANSWERING
        # elif next_q == (3, 17):
        #     var_answers = []
        #     ans_2_1 = Answer.objects.get(user__user_id = user.user_id, date = None, sn=2, qn = 1)
        #     ans_list = variants_to_list(ans_2_1.ans)
        #     for al in ans_list:
        #         if int(ans_list[al]) != 4:
        #             var_answers.append(al)
                         
        inline_button = []

        if next_q == (3, 16):
            for v in variants:
                part = []
                
                # part.append(InlineKeyboardButton(text=v, callback_data='nothing'))
                for i in range(1, len(var_answers)+1):
                    part.append(InlineKeyboardButton(text=str(i), callback_data='{}_{}_{}_{}'.format(q.sn, q.qn, v, i)))  # section number _ question nummber _ variant name _ answer
                    if len(part) == 6:
                        inline_button.append(part)
                        part = []        
                inline_button.append(part)
                add_text = '\n\n🔸   0️⃣    <b>{}</b>    🔟    🔹'.format(v)
                break

        
        elif next_q == (3, 17):
            for v in range(1, len(variants)+1):
                for i in var_answers:
                    inline_button.append([InlineKeyboardButton(text=i, callback_data='{}_{}_{}_{}'.format(q.sn, q.qn, v, i))])  # section number _ question nummber _ variant name _ answer
                add_text = '\n\n💬    ⬛️◼️◾️▪️  <b>{}</b>   ▫️◽️◻️⬜️   🗯    '.format(variants[v-1])
                break


        else:
            for v in variants:
                part = []
                part.append(InlineKeyboardButton(text=v, callback_data='nothing'))
                for i in range(1, len(var_answers)+1):
                    part.append(InlineKeyboardButton(text=str(i), callback_data='{}_{}_{}_{}'.format(q.sn, q.qn, v, i)))  # section number _ question nummber _ variant name _ answer
                inline_button.append(part)
        inline_button.append([InlineKeyboardButton(text=get_word('back', update), callback_data='prev_question-0'), InlineKeyboardButton(text=get_word('next', update), callback_data='next_question-2')])
        inline_button.append([InlineKeyboardButton(text=get_word('main menu', update), callback_data='main_menu')])
        del_msg = update.message.reply_text(str(q.qd), reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
        bot.delete_message(update.message.chat.id, del_msg.message_id)


        index = 1
        if next_q != (3, 16) and next_q != (3, 17):
            add_text = '\n\n'
            for i in var_answers:
                add_text += '\n{}.{}'.format(index, i)
                index += 1
        
        bot.send_message(update.message.chat.id, str(q.qd)+add_text, reply_markup = InlineKeyboardMarkup(inline_button), parse_mode=telegram.ParseMode.HTML)
        Answer.objects.create(index = l_ans.index, end=False, user = user, st = q.st, sn = q.sn, qn = q.qn, ans='')
        return INLINE_ANSWERING
    
    elif next_q == (1, 3):
        keys = get_variants_for_buttons(q.qv)
        keys.insert(-1, [get_word('city_chirchik', update)])
        keys.insert(-1, [get_word('city_gulistan', update)])
        keys.append([get_word('back', update)])
        keys.append([get_word('main menu', update)])
        update.message.reply_text(str(q.qd)+add_text, reply_markup=ReplyKeyboardMarkup(keyboard=keys, resize_keyboard=True))
    

    elif not is_end:
        keys = []
        current_answers = get_answers_as_list(l_ans.ans)
        for i in get_variants_as_list(q.qv):
            if i in l_ans.ans:
                keys.append(['✅ {}'.format(i)])
            else:
                keys.append([i])
        
        for i in current_answers:
            if not i in q.qv:
                keys.append(['✅ {}'.format(i)])
        keys.append([get_word('back', update), get_word('next', update)])
        keys.append([get_word('main menu', update)])
        try:
            bot.delete_message(update.message.chat.id, update.message.message_id)
            bot.delete_message(update.message.chat.id, update.message.message_id-1)
        except:
            dda=0
        add_text += '\n\n\n<b>{}</b>\n'.format(get_word('your answers', update))
        for i in current_answers:
            add_text += '✅ <i>{}</i>;\n'.format(i)
        bot.send_message(update.message.chat.id, str(q.qd)+add_text, reply_markup=ReplyKeyboardMarkup(keyboard=keys, resize_keyboard=True), parse_mode=telegram.ParseMode.HTML)  

    else:
        keys = get_variants_for_buttons(q.qv)
        keys.append([get_word('back', update)])
        keys.append([get_word('main menu', update)])
        update.message.reply_text(str(q.qd)+add_text, reply_markup=ReplyKeyboardMarkup(keyboard=keys, resize_keyboard=True))
    if is_end:
        Answer.objects.create(index = l_ans.index, end=False, user = user, st = q.st, sn = q.sn, qn = q.qn, ans='')
    return CONTINUE_ANSWERING

@is_start
def inline_answering(update, context):
    bot = context.bot

    update = update.callback_query
    
    user = get_user_by_id(update.message.chat.id)
    if '_question' in update.data:
        current_answer = Answer.objects.get(user__user_id = user.user_id, end=False)
        current_question = Question.objects.get(sn = current_answer.sn, qn = current_answer.qn, lang=user.lang)
        answers = variants_to_list(current_answer.ans)
        v, v_a = str(current_question.qv).split('\\')
        required_answers = get_variants_as_list(v)
        if (int(current_answer.sn) == 3 and int(current_answer.qn) == 1) or (int(current_answer.sn) == 3 and int(current_answer.qn) == 16) or (int(current_answer.sn) == 3 and int(current_answer.qn) == 17):
            variants = []
            ans_2_1 = Answer.objects.get(user__user_id = user.user_id, date = None, sn=2, qn = 1)
            ans_list = variants_to_list(ans_2_1.ans)
            for al in ans_list:
                if int(ans_list[al]) != 4:
                    variants.append(al)
            required_answers = variants
        if '-' in str(update.data):
            
            sth_text, index_of_ = str(update.data).split('-')
        else:
            index_of_ = '0'
        if len(answers) == len(required_answers) or ((int(current_answer.sn) == 3 and int(current_answer.qn) == 17  and len(required_answers)+1 <= int(index_of_))) or ('prev' in update.data and not (int(current_answer.sn) == 3 and int(current_answer.qn) == 17) and not (int(current_answer.sn) == 3 and int(current_answer.qn) == 16) ):
            current_answer.end = True
            current_answer.save()
            if 'prev' in update.data:
                current_answer.delete()
                current_answer = Answer.objects.filter(user__user_id = user.user_id, date=None).order_by('-sn', '-qn')[0]
                current_answer.delete()
                current_answer = Answer.objects.filter(user__user_id = user.user_id, date=None).order_by('-sn', '-qn')[0]
                bot.delete_message(update.message.chat.id, update.message.message_id)
            else:
                update.edit_message_text(text_after_inline(current_question, current_answer), parse_mode=telegram.ParseMode.HTML)
            
            next_q = sections_and_questions[sections_and_questions.index((current_answer.sn, current_answer.qn)) + 1] # next question (sn, qn)
            all_variants = get_variants_as_list(v)
            if int(current_answer.sn) == 3 and int(current_answer.qn) == 1:
                for i in all_variants:
                    if i in answers:
                        if int(answers[i]) == 3:

                            break
                    next_q = (next_q[0], next_q[1] + 1)
                else:
                    for i in all_variants:
                        if i in answers:
                            if int(answers[i]) == 1:

                                break
                        next_q = (next_q[0], next_q[1] + 1)
            
            q = Question.objects.get(sn = next_q[0], qn = next_q[1], lang=user.lang) # Question
            Answer.objects.create(index = current_answer.index, end=False, user = user, st = q.st, sn = q.sn, qn = q.qn, ans='')
            if next_q in [(2, 3), (2, 4), (2, 10), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14), (3, 15), (4, 2), (4, 4)]:
                add_text = '\n\n' + get_word('if other', update)
                q_list = get_variants_as_list(q.qv)[:-1] # remove last variant 
                q.qv = get_variants_as_text(q_list)

            else:
                add_text = ''


            if next_q == (3, 17) or next_q == (3, 16):


                v, v_a = str(q.qv).split('\\')
                variants = get_variants_as_list(v)
                var_answers = get_variants_as_list(v_a)
                
                ans_2_1 = Answer.objects.get(user__user_id = user.user_id, date = None, sn=2, qn = 1)
                ans_list = variants_to_list(ans_2_1.ans)
                

                inline_button = []
                
                if next_q == (3, 16):
                    variants = []
                    for al in ans_list:
                        if int(ans_list[al]) != 4:
                            variants.append(al)
                    
                    part = []
               
                    for v in variants:
                        part = []
                        for i in range(1, len(var_answers)+1):
                            part.append(InlineKeyboardButton(text=str(i), callback_data='{}_{}_{}_{}'.format(q.sn, q.qn, v, i)))  # section number _ question nummber _ variant name _ answer
                            if len(part) == 6:
                                inline_button.append(part)
                                part = []
                        add_text = '\n\n🔸   0️⃣     <b>{}</b>    🔟    🔹'.format(v)
                        inline_button.append(part)
                        break
                else:  # (3, 17)
                    variants = []

                    for al in ans_list:
                        if int(ans_list[al]) != 4:
                            variants.append(al)

                    
                    for v in range(1, len(variants)+1):
                        for i in var_answers:
                            inline_button.append([InlineKeyboardButton(text=i, callback_data='{}_{}_{}_{}'.format(q.sn, q.qn, v, i))])  # section number _ question nummber _ variant name _ answer
                        add_text = '\n\n💬    ⬛️◼️◾️▪️  <b>{}</b>   ▫️◽️◻️⬜️   🗯    '.format(variants[v-1])
                        break
                inline_button.append([InlineKeyboardButton(text=get_word('back', update), callback_data='prev_question-0'), InlineKeyboardButton(text=get_word('next', update), callback_data='next_question-2')])
                inline_button.append([InlineKeyboardButton(text=get_word('main menu', update), callback_data='main_menu')])

                bot.send_message(update.message.chat.id, str(q.qd)+add_text, reply_markup = InlineKeyboardMarkup(inline_button), parse_mode=telegram.ParseMode.HTML)
                # Answer.objects.create(index = l_ans.index, end=False, user = user, st = q.st, sn = q.sn, qn = q.qn, ans='')
                return INLINE_ANSWERING



            else:
                keys = get_variants_for_buttons(q.qv)
                if next_q == (1, 3):
                    keys.insert(-1, [get_word('city_chirchik', update)])
                    keys.insert(-1, [get_word('city_gulistan', update)])                
                keys.append([get_word('back', update)])
                keys.append([get_word('main menu', update)])
                bot.send_message(update.message.chat.id, str(q.qd)+add_text, reply_markup=ReplyKeyboardMarkup(keyboard=keys, resize_keyboard=True))

                return CONTINUE_ANSWERING
        else:
            if (int(current_answer.sn) == 3 and int(current_answer.qn) == 17) or (int(current_answer.sn) == 3 and int(current_answer.qn) == 16):
                list_ans = variants_to_list(current_answer.ans)

                v, v_a = str(current_question.qv).split('\\')
                variants = get_variants_as_list(v)
                var_answers = get_variants_as_list(v_a)
                
                ans_2_1 = Answer.objects.get(user__user_id = user.user_id, date = None, sn=2, qn = 1)
                ans_list = variants_to_list(ans_2_1.ans)
                
                inline_button = []



                if (int(current_answer.sn) == 3 and int(current_answer.qn) == 16) and 'prev' in update.data and '-0' in update.data:
                    current_answer.delete()
                    
                    
                    
                    current_answer = Answer.objects.filter(user__user_id = user.user_id, date=None).order_by('-sn', '-qn')[0]
                    current_answer.delete()
                    
                    current_answer = Answer.objects.filter(user__user_id = user.user_id, date=None).order_by('-sn', '-qn')[0]
                    current_answer.end = False
                    new_data = current_answer.ans
                    current_answer.ans = ""
                    current_answer.save()
                    update.data = new_data
                    
                    bot.delete_message(update.message.chat.id, update.message.message_id)
                    loop_answering(update, context)
                    if current_answer.sn == 2:
                        return INLINE_ANSWERING
                    else:
                        return CONTINUE_ANSWERING
                    
                elif (int(current_answer.sn) == 3 and int(current_answer.qn) == 16) or ((int(current_answer.sn) == 3 and int(current_answer.qn) == 17) and 'prev' in update.data and '-0' in update.data):
                    if (int(current_answer.sn) == 3 and int(current_answer.qn) == 17):
                        current_answer.delete()
                        current_answer = Answer.objects.get(user__user_id = user.user_id, sn = 3, qn = 16, date=None)
                        current_answer.end = False
                        current_answer.ans = ""
                        current_answer.save()
                        current_question = Question.objects.get(sn = current_answer.sn, qn = current_answer.qn, lang=user.lang)

                    variants = []
                    ans_2_1 = Answer.objects.get(user__user_id = user.user_id, date = None, sn=2, qn = 1)
                    ans_list = variants_to_list(ans_2_1.ans)
                    for al in ans_list:
                        if int(ans_list[al]) != 4:
                            variants.append(al)
                    for v in variants:
                        prev_next_qn = variants.index(v) + 1
                        part = []
                        next_q_text = str(update.data)
                        trash, next_q_n = next_q_text.split('-')
                        if next_q_n == '0':
                            next_q_n = '1'
                            var_answers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                            
                        if int(next_q_n) == variants.index(v)+1:
                            # if list_ans == []:
                            #     bot.answer_callback_query(callback_query_id=update.id, text=get_word('click all', update), show_alert=True)
                            #     return                            
                            for i in range(1, len(var_answers)+1):
                                if '{}={};'.format(v, i) in current_answer.ans:
                                    part.append(InlineKeyboardButton(text=str(i) + '🔘', callback_data='{}_{}_{}_{}'.format(current_answer.sn, current_answer.qn, v, i)))  # section number _ question nummber _ variant name _ answer
                                else:    
                                    part.append(InlineKeyboardButton(text=str(i), callback_data='{}_{}_{}_{}'.format(current_answer.sn, current_answer.qn, v, i)))  # section number _ question nummber _ variant name _ answer
                                if len(part) == 6:
                                    inline_button.append(part)
                                    part = []
                            add_text = '\n\n🔸   0️⃣     <b>{}</b>    🔟    🔹'.format(v)
                            inline_button.append(part)
                            
                            break


                elif (int(current_answer.sn) == 3 and int(current_answer.qn) == 17):
                    variants = []
                    ans_2_1 = Answer.objects.get(user__user_id = user.user_id, date = None, sn=2, qn = 1)
                    ans_list = variants_to_list(ans_2_1.ans)
                    for al in ans_list:
                        if int(ans_list[al]) != 4:
                            variants.append(al)
                    
                    
                    for v in range(1, len(variants)+1):
                
                        next_q_text = str(update.data)
                        trash, next_q_n = next_q_text.split('-')
                        if int(next_q_n) == v:
                            for i in var_answers:
                                if str(v) in list_ans:
                                    if i in list_ans[str(v)]:
                                        inline_button.append([InlineKeyboardButton(text=i + '🔘', callback_data='{}_{}_{}_{}'.format(current_question.sn, current_question.qn, v, i))])
                                    else:
                                        inline_button.append([InlineKeyboardButton(text=i, callback_data='{}_{}_{}_{}'.format(current_question.sn, current_question.qn, v, i))])  # section number _ question nummber _ variant name _ answer
                                else:
                                    inline_button.append([InlineKeyboardButton(text=i, callback_data='{}_{}_{}_{}'.format(current_question.sn, current_question.qn, v, i))])  # section number _ question nummber _ variant name _ answer
                            
                            add_text = '\n\n💬    ⬛️◼️◾️▪️  <b>{}</b>   ▫️◽️◻️⬜️   🗯    '.format(variants[v-1])
                            break

                    


                try:
                    index = int(v)
                except:
                    index = prev_next_qn
                inline_button.append([InlineKeyboardButton(text=get_word('back', update), callback_data='prev_question-{}'.format(index-1)), InlineKeyboardButton(text=get_word('next', update), callback_data='next_question-{}'.format(index+1))])
                inline_button.append([InlineKeyboardButton(text=get_word('main menu', update), callback_data='main_menu')])
                try:
                    update.edit_message_text(str(current_question.qd)+add_text, reply_markup = InlineKeyboardMarkup(inline_button), parse_mode=telegram.ParseMode.HTML)
                except:
                    
                    bot.answer_callback_query(callback_query_id=update.id, text=get_word('click all', update), show_alert=True)

                return
            else:
                bot.answer_callback_query(callback_query_id=update.id, text=get_word('click all', update), show_alert=True)
            
    elif '_' in update.data:
        sn, qn , vn, ans = str(update.data).split('_')
        sn = int(sn)
        qn = int(qn)
        
        l_ans = Answer.objects.get(user__user_id = user.user_id, end=False, qn = qn, sn = sn)  # last answer
        this_q = Question.objects.get(sn = sn, qn = qn, lang=user.lang)  # this question
        list_ans = variants_to_list(l_ans.ans) # list of current answers 
        if sn == 3 and qn == 17:
            if vn in list_ans:
                if not ans in list_ans[vn]: 
                    list_ans[vn] += '{},'.format(ans)
                else:
                    list_ans[vn] = str(list_ans[vn]).replace('{},'.format(ans), '')
            else:
                list_ans[vn] = '{},'.format(ans)
        else:
            list_ans[vn] = ans  # change answer
        l_ans.ans = list_to_variants(list_ans) # set answer as string;
        l_ans.save()
        v, v_a = str(this_q.qv).split('\\')
        variants = get_variants_as_list(v)
        var_answers = get_variants_as_list(v_a)

        if (sn == 3 and qn == 1) or (sn == 3 and qn == 16) or (sn == 3 and qn == 17):
            variants = []
            ans_2_1 = Answer.objects.get(user__user_id = user.user_id, date = None, sn=2, qn = 1)
            ans_list = variants_to_list(ans_2_1.ans)
            for al in ans_list:
                if int(ans_list[al]) != 4:
                    variants.append(al)
        # elif (sn == 3 and qn == 17):
        #     var_answers = []
        #     ans_2_1 = Answer.objects.get(user__user_id = user.user_id, date = None, sn=2, qn = 1)
        #     ans_list = variants_to_list(ans_2_1.ans)
        #     for al in ans_list:
        #         if int(ans_list[al]) != 4:
        #             var_answers.append(al)

        inline_button = []

        
        
        index = 1
        for v in variants:
            part = []
    
            if (sn == 3 and qn == 17):
                if str(index) == vn:
                    for i in var_answers:
                    
                        if str(index) in list_ans:
                            if i in list_ans[str(index)]:
                                inline_button.append([InlineKeyboardButton(text=i + '🔘', callback_data='{}_{}_{}_{}'.format(this_q.sn, this_q.qn, str(index), i))])  # section number _ question nummber _ variant name _ answer
                            else:
                                inline_button.append([InlineKeyboardButton(text=i, callback_data='{}_{}_{}_{}'.format(this_q.sn, this_q.qn, str(index), i))])  # section number _ question nummber _ variant name _ answer
                        else:
                            inline_button.append([InlineKeyboardButton(text=i, callback_data='{}_{}_{}_{}'.format(this_q.sn, this_q.qn, str(index), i))])  # section number _ question nummber _ variant name _ answer
                    add_text = '\n\n💬    ⬛️◼️◾️▪️  <b>{}</b>   ▫️◽️◻️⬜️   🗯    '.format(v)                    
                    break
                else:
                    index += 1
                    continue
                index += 1
            elif (sn == 3 and qn == 16):
                
                
                if v in vn or vn in v:
    
                    for i in range(1, len(var_answers)+1):
                        if (str(i) == ans and v == vn) or '{}={};'.format(v, i) in l_ans.ans:
                            part.append(InlineKeyboardButton(text=str(i) + '🔘', callback_data='{}_{}_{}_{}'.format(this_q.sn, this_q.qn, v, i)))  # section number _ question nummber _ variant name _ answer
                        else:
                            part.append(InlineKeyboardButton(text=str(i), callback_data='{}_{}_{}_{}'.format(this_q.sn, this_q.qn, v, i)))  # section number _ question nummber _ variant name _ answer
                        if len(part) == 6:
                            inline_button.append(part)
                            part = []

                    # inline_button.append(part)
                    add_text = '\n\n🔸   0️⃣     <b>{}</b>    🔟    🔹'.format(v)
                    index = variants.index(v) + 1
                else:
                    continue


            else:
                part.append(InlineKeyboardButton(text=v, callback_data='nothing'))
                for i in range(1, len(var_answers)+1):
                    if (str(i) == ans and v == vn) or '{}={}'.format(v, i) in l_ans.ans:
                        part.append(InlineKeyboardButton(text=str(i) + '🔘', callback_data='{}_{}_{}_{}'.format(this_q.sn, this_q.qn, v, i)))  # section number _ question nummber _ variant name _ answer
                    else:
                        part.append(InlineKeyboardButton(text=str(i), callback_data='{}_{}_{}_{}'.format(this_q.sn, this_q.qn, v, i)))  # section number _ question nummber _ variant name _ answer
            inline_button.append(part)
        
        inline_button.append([InlineKeyboardButton(text=get_word('back', update), callback_data='prev_question-{}'.format(index-1)), InlineKeyboardButton(text=get_word('next', update), callback_data='next_question-{}'.format(index+1))])
        inline_button.append([InlineKeyboardButton(text=get_word('main menu', update), callback_data='main_menu')])

        index = 1
        if not (sn == 3 and qn == 16) and not (sn == 3 and qn == 17):
            add_text = '\n\n'
            for i in var_answers:
                add_text += '\n{}.{}'.format(index, i)
                index += 1

        update.edit_message_text(str(this_q.qd)+add_text, reply_markup = InlineKeyboardMarkup(inline_button), parse_mode=telegram.ParseMode.HTML)
        
        return INLINE_ANSWERING
    elif 'nothing' in update.data:
        return
    
    else:
        return CONTINUE_ANSWERING
        
