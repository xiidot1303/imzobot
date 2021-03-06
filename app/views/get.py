from django.http import HttpResponse, FileResponse
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from app.models import *

import os
import xlrd
from xlutils.copy import copy

from config import basedir

@login_required
def get_excel(request, file_name):
    f = open(basedir+'/files/excel/{}'.format(file_name), 'rb')
    return FileResponse(f)

@login_required
def get_answers_excel(request, index):
    index_list = [
        [5, 10, 15],
        [34, 44, 53, 65, 75, 80, 136, 141, 197, 207],
        [221, 231, 241, 251, 261, 271, 281, 291, 301, 311, 321, 331, 341, 351, 361, 371, 382],
        [395, 400, 414, 419],
        [433]
    ]

    main_excel_file = Excel.objects.get(lang="ru").file

    book = xlrd.open_workbook(basedir+"/files/"+str(main_excel_file))
    new_book = copy(book)
    sh = book.sheet_by_index(0)
    w = new_book.get_sheet(0)
    ans_index = Answer_index.objects.get(pk=index)
    first_ans = Answer.objects.filter(index=index)[0]
    w.write(0, 0, '{} {}'.format(first_ans.user.name, ans_index.date.date()))
    w.write(0, 1, first_ans.user.phone)
    w.write(0, 2, 'ID: {}'.format(index))
    for a in Answer.objects.filter(index=index):
        q = Question.objects.get(sn=a.sn, qn=a.qn, lang = a.user.lang)
        
        if (a.sn==2 and a.qn == 1) or (a.sn==3 and a.qn == 1) or (a.sn==3 and a.qn == 16):
            v, v_a = str(q.qv).split('\\')
            q_v_list = get_variants_as_list(v)
            ans_list = variants_to_list(a.ans)

            for i in ans_list:
                i_row = q_v_list.index(i)
                w.write(index_list[a.sn-1][a.qn-1] + i_row, 3+int(ans_list[i]), "✅")    


        elif (a.sn==3 and a.qn == 17):
            v, v_a = str(q.qv).split('\\')
            q_v_list = get_variants_as_list(v)
            q_v_a_list = get_variants_as_list(v_a)
            ans_list = variants_to_list(a.ans)
            variants = []
            ans_2_1 = Answer.objects.get(user__user_id = a.user.user_id, index = a.index, sn=2, qn = 1)
            ans_l = variants_to_list(ans_2_1.ans)
            for al in ans_l:
                if int(ans_l[al]) != 4:
                    variants.append(al)

        
            for i in ans_list:
                
                if ans_list[i]:

                    for x in list(ans_list[i].split(',')):
                        if x in q_v_a_list:
                            i_col = q_v_a_list.index(x)
                            v_name = variants[int(i) - 1]
                            i_row = q_v_list.index(v_name)
                            w.write(index_list[a.sn-1][a.qn-1] + i_row, 4+i_col, "✅")


        elif not (a.sn==1 and a.qn == 2):
            q_v_list = get_variants_as_list(q.qv)
            if a.ans in q_v_list:
                index_ans = q_v_list.index(a.ans)
            else:
                index_ans = len(q_v_list) - 1
            w.write(index_list[a.sn-1][a.qn-1] + index_ans, 3, "{}    ✅".format(a.ans))
        elif (a.sn==1 and a.qn == 2):
            m, y = str(a.ans).split('.')
            w.write(index_list[0][1], 3, m)
            w.write(index_list[0][1]+1, 3, y)



    new_file_path = "files/excel/answer_{}.xls".format(get_ip(request))
    new_book.save(new_file_path)
    f = open(new_file_path, 'rb')
    return FileResponse(f)

def get_variants_as_list(text):
    list_ = list(str(text).split('||'))
    list_.remove('')
    return list_



def variants_to_list(text):
    r_list = {}
    for i in list(text.split(';')):
        if i != '':
            variant, answer = i.split('=')
            r_list[variant] = answer
    return r_list







def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip   