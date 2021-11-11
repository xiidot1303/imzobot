from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import Answer, Answer_index, Bot_user

@login_required
def report_by_index(request):
    answers = Answer_index.objects.filter(end=True).order_by('-date')
    users = []
    for a in answers:
        username = Bot_user.objects.get(user_id = a.user_id).name
        users.append(username)
    numbers = []
    for a in answers:
        phone = Bot_user.objects.get(user_id = a.user_id).phone
        numbers.append(phone)


    context = {'answers': answers, 'users': users, 'numbers': numbers}
    return render(request, 'report/by_index.html', context)


@login_required
def report_answer(request, pk):
    answers = Answer.objects.filter(index = pk).exclude(date=None)

    a = answers[0]
    title = '{} {}.{}.{}'.format(a.user.name, a.date.day, a.date.month, a.date.year)
    desc = '{} / {} / {}.{}.{}'.format(a.user.name, a.user.phone, a.date.day, a.date.month, a.date.year)
    context = {'answers': answers, 'title': title, 'desc': desc, 'index': pk}
    return render(request, 'report/answer.html', context)
