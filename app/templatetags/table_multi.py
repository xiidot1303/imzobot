from django import template
from app.models import Answer, Question
register = template.Library()


def variants_to_list(text):
    r_list = {}
    for i in list(text.split(';')):
        if i != '':
            variant, answer = i.split('=')
            r_list[variant] = answer
    return r_list


def get_variants_as_list(text):
    list_ = list(str(text).split('||'))
    list_.remove('')
    return list_



@register.filter
def table_multi(pk):
    pk = int(pk)
    a = Answer.objects.get(pk=pk)
    q = Question.objects.get(sn=a.sn, qn=a.qn, lang = a.user.lang)
    v, v_a = str(q.qv).split('\\')
    a_list = get_variants_as_list(v_a)
    r_list = []
    th_list = ['']
    for i in a_list:
        th_list.append(i)
    r_list.append(th_list)

    ans_list = variants_to_list(a.ans)
    q_v = get_variants_as_list(v)
    q_v = []
    ans_2_1 = Answer.objects.get(user__user_id = a.user.user_id, index = a.index, sn=2, qn = 1)
    ans_l = variants_to_list(ans_2_1.ans)
    for al in ans_l:
        if int(ans_l[al]) != 4:
            q_v.append(al)
    td_list = []
    for a in ans_list:
        n = 0   
        tr = []
        for i in th_list:

            if n == 0:
                tr.append(q_v[int(a)-1])
            elif i in str(ans_list[a]):
                tr.append('✅')
            else:
                tr.append(' ')
            n+=1
        td_list.append(tr)
    r_list.append(td_list)
    return r_list

