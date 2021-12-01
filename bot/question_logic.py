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
    print(question.qd)
    update.message.reply_text(str(question.qd), reply_markup=ReplyKeyboardMarkup(keyboard=get_variants_for_buttons(question.qv), resize_keyboard=True))
    a = Answer_index.objects.create(end=False, user_id=update.message.chat.id)
    Answer.objects.create(end=False, user = user, st = question.st, sn = question.sn, qn = question.qn, index = a.pk)
    return CONTINUE_ANSWERING


alpha = ['a','b', 'c', 'd', 'e', 'f', 'g']


@is_start
def loop_answering(update, context):
    bot = context.bot
    user = get_user_by_id(update.message.chat.id)
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
    
    if not answer in l_q.qv and (l_ans.sn, l_ans.qn) != (2, 3) and (l_ans.sn, l_ans.qn) != (2, 4) and (l_ans.sn, l_ans.qn) != (2, 10)and (l_ans.sn, l_ans.qn) != (3, 2)and not ((l_ans.sn, l_ans.qn) in [(1, 2), (1, 3), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14), (3, 15), (4, 2), (4, 4) ]):
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
        q_3_1 = Question.objects.get(lang=user.lang, sn=3, qn=1)
        a_3_1 = Answer.objects.get(date=None, user__user_id=user.user_id, sn = 3, qn = 1)
        answers = variants_to_list(a_3_1.ans)

        v, v_a = str(q_3_1.qv).split('\\')
        all_variants = get_variants_as_list(v)
        for i in all_variants[l_ans.qn-1:]:
            print(i)
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


    elif (l_ans.sn, l_ans.qn) in [(3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14)]:
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

            


        # this_ans = Answer.objects.get(user__user_id = user.user_id, date=None, sn=2, qn=3)
        # this_ques = Question.objects.get(sn=2, qn=3, lang=user.lang)
        # if not this_ans.ans in get_variants_as_list(this_ques.qv)[:-2]: # спросить тех кто не выбрал код 6 в Q2e 
        #     next_q = sections_and_questions[sections_and_questions.index((2, 9))] # next question (sn, qn)
    
    l_ans.ans = answer
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
        update.message.reply_text(str(q.qd) + '  (мм.гггг)', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    elif next_q == (2, 1) or next_q == (3, 1) or next_q == (3, 16):
        v, v_a = str(q.qv).split('\\')
        variants = get_variants_as_list(v)
        var_answers = get_variants_as_list(v_a)
        if next_q == (3, 1) or next_q == (3, 16):
            variants = []
            ans_2_1 = Answer.objects.get(user__user_id = user.user_id, date = None, sn=2, qn = 1)
            ans_list = variants_to_list(ans_2_1.ans)
            for al in ans_list:
                if int(ans_list[al]) != 4:
                    variants.append(al)
            if variants == []:
                next_q = (4, 1)
                q = Question.objects.get(sn = next_q[0], qn = next_q[1], lang=user.lang) # Question
                update.message.reply_text(str(q.qd)+add_text, reply_markup=ReplyKeyboardMarkup(keyboard=get_variants_for_buttons(q.qv), resize_keyboard=True))
                Answer.objects.create(index = l_ans.index, end=False, user = user, st = q.st, sn = q.sn, qn = q.qn, ans='')
                return CONTINUE_ANSWERING
        inline_button = []
        # if next_q == (3, 16):
            
        #     part = []
        #     a = ['a','b', 'c', 'd', 'e', 'f', 'g']
        #     for v in variants:
        #         part.append(InlineKeyboardButton(text=a[variants.index(v)], callback_data='nothing'))
        #     inline_button.append(part)
        #     for i in var_answers:
        #         part = []
        #         for v in variants:
        #             text = str(int(float(i)))
        #             part.append(InlineKeyboardButton(text=text, callback_data='{}_{}_{}_{}'.format(q.sn, q.qn, v, text)))
        #         inline_button.append(part)

        # else:
        if next_q == (3, 16):
            for v in variants:
                part = []
                # part.append(InlineKeyboardButton(text=v, callback_data='nothing'))
                for i in range(1, len(var_answers)+1):
                    part.append(InlineKeyboardButton(text=str(i), callback_data='{}_{}_{}_{}'.format(q.sn, q.qn, v, i)))  # section number _ question nummber _ variant name _ answer
                inline_button.append(part)
                break


        else:
            for v in variants:
                part = []
                part.append(InlineKeyboardButton(text=v, callback_data='nothing'))
                for i in range(1, len(var_answers)+1):
                    part.append(InlineKeyboardButton(text=str(i), callback_data='{}_{}_{}_{}'.format(q.sn, q.qn, v, i)))  # section number _ question nummber _ variant name _ answer
                inline_button.append(part)
        inline_button.append([InlineKeyboardButton(text=get_word('next', update), callback_data='next_question')])
        del_msg = update.message.reply_text(str(q.qd), reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
        bot.delete_message(update.message.chat.id, del_msg.message_id)


        add_text = '\n\n'
        index = 1
        if next_q != (3, 16):
            for i in var_answers:
                add_text += '\n{}.{}'.format(index, i)
                index += 1
        else:
            a = ['a','b', 'c', 'd', 'e', 'f', 'g']
            for i in variants:
                add_text += '{}.{}    '.format(a[variants.index(i)], i) 
        bot.send_message(update.message.chat.id, str(q.qd)+add_text, reply_markup = InlineKeyboardMarkup(inline_button))
        Answer.objects.create(index = l_ans.index, end=False, user = user, st = q.st, sn = q.sn, qn = q.qn, ans='')
        return INLINE_ANSWERING
    
    elif next_q == (1, 3):
        keys = get_variants_for_buttons(q.qv)
        keys.insert(-1, [get_word('city_chirchik', update)])
        keys.insert(-1, [get_word('city_gulistan', update)])
        update.message.reply_text(str(q.qd)+add_text, reply_markup=ReplyKeyboardMarkup(keyboard=keys, resize_keyboard=True))
    
    else:
        update.message.reply_text(str(q.qd)+add_text, reply_markup=ReplyKeyboardMarkup(keyboard=get_variants_for_buttons(q.qv), resize_keyboard=True))
    
    Answer.objects.create(index = l_ans.index, end=False, user = user, st = q.st, sn = q.sn, qn = q.qn, ans='')
    return CONTINUE_ANSWERING

@is_start
def inline_answering(update, context):
    bot = context.bot

    update = update.callback_query
    user = get_user_by_id(update.message.chat.id)
    if update.data == 'next_question':
        current_answer = Answer.objects.get(user__user_id = user.user_id, end=False)
        current_question = Question.objects.get(sn = current_answer.sn, qn = current_answer.qn, lang=user.lang)
        answers = variants_to_list(current_answer.ans)
        v, v_a = str(current_question.qv).split('\\')
        required_answers = get_variants_as_list(v)
        if (int(current_answer.sn) == 3 and int(current_answer.qn) == 1) or (int(current_answer.sn) == 3 and int(current_answer.qn) == 16):
            variants = []
            ans_2_1 = Answer.objects.get(user__user_id = user.user_id, date = None, sn=2, qn = 1)
            ans_list = variants_to_list(ans_2_1.ans)
            for al in ans_list:
                if int(ans_list[al]) != 4:
                    variants.append(al)
            required_answers = variants
    
        if len(answers) == len(required_answers) or (int(current_answer.sn) == 3 and int(current_answer.qn) == 17):
            current_answer.end = True
            current_answer.save()
            bot.delete_message(update.message.chat.id, update.message.message_id)
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
                    # a = ['a','b', 'c', 'd', 'e', 'f', 'g']
                    # for v in variants:
                    #     part.append(InlineKeyboardButton(text=a[variants.index(v)], callback_data='nothing'))
                    # inline_button.append(part)
                    # for i in var_answers:
                    #     part = []
                    #     for v in variants:
                    #         text = str(int(float(i)))
                    #         part.append(InlineKeyboardButton(text=text, callback_data='{}_{}_{}_{}'.format(q.sn, q.qn, v, text)))
                    #     inline_button.append(part)
                    for v in variants:
                        part = []
                        part.append(InlineKeyboardButton(text=v, callback_data='nothing'))
                        for i in range(1, len(var_answers)+1):
                            part.append(InlineKeyboardButton(text=str(i), callback_data='{}_{}_{}_{}'.format(q.sn, q.qn, v, i)))  # section number _ question nummber _ variant name _ answer
                        inline_button.append(part)
                else:
                    var_answers = []

                    for al in ans_list:
                        if int(ans_list[al]) != 4:
                            var_answers.append(al)

                    
                    for v in range(1, len(variants)+1):
                        part = []
                        part.append(InlineKeyboardButton(text=v, callback_data='nothing'))
                        
                        for i in var_answers:
                            part.append(InlineKeyboardButton(text=alpha[var_answers.index(i)], callback_data='{}_{}_{}_{}'.format(q.sn, q.qn, v, i)))  # section number _ question nummber _ variant name _ answer
                        inline_button.append(part)
                inline_button.append([InlineKeyboardButton(text=get_word('next', update), callback_data='next_question')])


                add_text = '\n\n'
                if next_q == (3, 17):
                    for i in var_answers:
                        add_text += '{}.{}   '.format(alpha[var_answers.index(i)], i)
                    add_text += '\n\n'
                    index = 1
                    for i in variants:
                        add_text += '\n{}.{}'.format(index, i)
                        index += 1
                else:  # elif 3 , 16
                    a = ['a','b', 'c', 'd', 'e', 'f', 'g']
                    for i in variants:
                        add_text += '{}.{}    '.format(a[variants.index(i)], i)
                bot.send_message(update.message.chat.id, str(q.qd)+add_text, reply_markup = InlineKeyboardMarkup(inline_button))
                # Answer.objects.create(index = l_ans.index, end=False, user = user, st = q.st, sn = q.sn, qn = q.qn, ans='')
                return INLINE_ANSWERING













            else:
                bot.send_message(update.message.chat.id, str(q.qd)+add_text, reply_markup=ReplyKeyboardMarkup(keyboard=get_variants_for_buttons(q.qv), resize_keyboard=True))

                return CONTINUE_ANSWERING
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
        if (sn == 3 and qn == 1) or (sn == 3 and qn == 16):
            variants = []
            ans_2_1 = Answer.objects.get(user__user_id = user.user_id, date = None, sn=2, qn = 1)
            ans_list = variants_to_list(ans_2_1.ans)
            for al in ans_list:
                if int(ans_list[al]) != 4:
                    variants.append(al)
        elif (sn == 3 and qn == 17):
            var_answers = []
            ans_2_1 = Answer.objects.get(user__user_id = user.user_id, date = None, sn=2, qn = 1)
            ans_list = variants_to_list(ans_2_1.ans)
            for al in ans_list:
                if int(ans_list[al]) != 4:
                    var_answers.append(al)

        inline_button = []


        # a = ['a','b', 'c', 'd', 'e', 'f', 'g']
        # if (sn == 3 and qn == 16):
        #     part = []
        #     for v in variants:
        #         part.append(InlineKeyboardButton(text=a[variants.index(v)], callback_data='nothing'))
        #     inline_button.append(part)
        #     for i in var_answers:
        #         part = []
        #         for v in variants:
        #             text = str(int(float(i)))
        #             if (text == ans and v == vn) or '{}={};'.format(v, text) in l_ans.ans:
        #                 part.append(InlineKeyboardButton(text=text + ' 🔘', callback_data='{}_{}_{}_{}'.format(this_q.sn, this_q.qn, v, text)))
        #             else:
        #                 part.append(InlineKeyboardButton(text=text, callback_data='{}_{}_{}_{}'.format(this_q.sn, this_q.qn, v, text)))

        #         inline_button.append(part)
    


        # else:

        
        index = 1
        for v in variants:
            part = []
    
            if (sn == 3 and qn == 17):
                part.append(InlineKeyboardButton(text=str(index), callback_data='nothing'))
                for i in var_answers:
                    if str(index) in list_ans:
                        if i in list_ans[str(index)]:
                            part.append(InlineKeyboardButton(text=alpha[var_answers.index(i)] + '🔘', callback_data='{}_{}_{}_{}'.format(this_q.sn, this_q.qn, str(index), i)))  # section number _ question nummber _ variant name _ answer
                        else:
                            part.append(InlineKeyboardButton(text=alpha[var_answers.index(i)], callback_data='{}_{}_{}_{}'.format(this_q.sn, this_q.qn, str(index), i)))  # section number _ question nummber _ variant name _ answer
                    else:
                        part.append(InlineKeyboardButton(text=alpha[var_answers.index(i)], callback_data='{}_{}_{}_{}'.format(this_q.sn, this_q.qn, str(index), i)))  # section number _ question nummber _ variant name _ answer
                index += 1
            elif (sn == 3 and qn == 16):
                # part.append(InlineKeyboardButton(text=v, callback_data='nothing'))
                
                if v in vn or vn in v:
    
                    for i in range(1, len(var_answers)+1):
                        if (str(i) == ans and v == vn) or '{}={}'.format(v, i) in l_ans.ans:
                            part.append(InlineKeyboardButton(text=str(i) + '🔘', callback_data='{}_{}_{}_{}'.format(this_q.sn, this_q.qn, v, i)))  # section number _ question nummber _ variant name _ answer
                        else:
                            part.append(InlineKeyboardButton(text=str(i), callback_data='{}_{}_{}_{}'.format(this_q.sn, this_q.qn, v, i)))  # section number _ question nummber _ variant name _ answer
                    inline_button.append(part)
                    break
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
            
        inline_button.append([InlineKeyboardButton(text=get_word('next', update), callback_data='next_question')])

        add_text = '\n\n'

        index = 1
        if not (sn == 3 and qn == 16) and not (sn == 3 and qn == 17):
            for i in var_answers:
                add_text += '\n{}.{}'.format(index, i)
                index += 1
        if (sn == 3 and qn == 17):
            for i in var_answers:
                add_text += '{}.{}   '.format(alpha[var_answers.index(i)], i)
            add_text += '\n\n'
            for i in variants:
                add_text += '\n{}.{}'.format(index, i)
                index += 1

        elif (sn == 3 and qn == 16):
            a = ['a','b', 'c', 'd', 'e', 'f', 'g']
            for i in variants:
                add_text += '{}.{}    '.format(a[variants.index(i)], i)
        update.edit_message_text(str(this_q.qd)+add_text, reply_markup = InlineKeyboardMarkup(inline_button))
        return INLINE_ANSWERING
    else:
        return CONTINUE_ANSWERING
        
