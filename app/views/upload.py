from django.http import HttpResponse, FileResponse
from django.shortcuts import render


from app.forms import *
from app.models import *
from app.functions import list_to_text

import pandas as pd
import os
import xlrd
from django.contrib.auth.decorators import login_required 

@login_required
def upload_file(request):
    if request.method == 'POST':
        bbf = UploadFileFrom(request.POST, request.FILES)
        if bbf.is_valid():
            lang = bbf.cleaned_data['lang']
            Excel.objects.get_or_create(lang=lang)
            excel = Excel.objects.get(lang=lang)
            excel.file = bbf.cleaned_data['file']
            excel.save()
            book = xlrd.open_workbook('files/{}'.format(str(excel.file)))
            sh = book.sheet_by_index(0)

            print(sh.cell_value(195, 3))

            print(sh.col(3)[197:203])
            col3 = sh.col(3)


            # first delete all questions
            for q in Question.objects.filter(lang=lang):
                q.delete()



            Question.objects.create(lang=lang, sn = 1, st = 'Демография', qn = 1, qd = col3[3].value, qv = list_to_text(col3[5:7]))

            Question.objects.create(lang=lang, sn = 1, st = 'Демография', qn = 2, qd = col3[8].value, qv = list_to_text(col3[10:12]))

            Question.objects.create(lang=lang, sn = 1, st = 'Демография', qn = 3, qd = col3[13].value, qv = list_to_text(col3[15:28]))

            Question.objects.create(lang=lang, sn = 2, st = 'Опыт и намерение приобретения окон', qn = 1, qd = col3[32].value, qv = '{}\\{}'.format(list_to_text(col3[34:41]), list_to_text(sh.row(33)[4:8])))

            Question.objects.create(lang=lang, sn = 2, st = 'Опыт и намерение приобретения окон', qn = 2, qd = col3[42].value, qv = list_to_text(col3[44:50]))

            Question.objects.create(lang=lang, sn = 2, st = 'Опыт и намерение приобретения окон', qn = 3, qd = col3[51].value, qv = list_to_text(col3[53:62]))

            Question.objects.create(lang=lang, sn = 2, st = 'Опыт и намерение приобретения окон', qn = 4, qd = col3[63].value, qv = list_to_text(col3[65:72]))

            Question.objects.create(lang=lang, sn = 2, st = 'Опыт и намерение приобретения окон', qn = 5, qd = col3[73].value, qv = list_to_text(col3[75:77]))

            Question.objects.create(lang=lang, sn = 2, st = 'Опыт и намерение приобретения окон', qn = 6, qd = col3[78].value, qv = list_to_text(col3[80:85]))

            Question.objects.create(lang=lang, sn = 2, st = 'Опыт и намерение приобретения окон', qn = 7, qd = col3[134].value, qv = list_to_text(col3[136:138]))

            Question.objects.create(lang=lang, sn = 2, st = 'Опыт и намерение приобретения окон', qn = 8, qd = col3[139].value, qv = list_to_text(col3[141:146]))

            Question.objects.create(lang=lang, sn = 2, st = 'Опыт и намерение приобретения окон', qn = 9, qd = col3[195].value, qv = list_to_text(col3[197:203]))

            Question.objects.create(lang=lang, sn = 2, st = 'Опыт и намерение приобретения окон', qn = 10, qd = col3[205].value, qv = list_to_text(col3[207:216]))

            Question.objects.create(lang=lang, sn = 3, st = 'Восприятия бренда', qn = 1, qd = col3[219].value, qv = '{}\\{}'.format(list_to_text(col3[221:228]), list_to_text(sh.row(220)[4:7])))

            Question.objects.create(lang=lang, sn = 3, st = 'Восприятия бренда', qn = 2, qd = col3[229].value, qv = list_to_text(col3[231:238]))

            Question.objects.create(lang=lang, sn = 3, st = 'Восприятия бренда', qn = 3, qd = col3[239].value, qv = list_to_text(col3[241:248]))

            Question.objects.create(lang=lang, sn = 3, st = 'Восприятия бренда', qn = 4, qd = col3[249].value, qv = list_to_text(col3[251:258]))

            Question.objects.create(lang=lang, sn = 3, st = 'Восприятия бренда', qn = 5, qd = col3[259].value, qv = list_to_text(col3[261:268]))

            Question.objects.create(lang=lang, sn = 3, st = 'Восприятия бренда', qn = 6, qd = col3[269].value, qv = list_to_text(col3[271:278]))

            Question.objects.create(lang=lang, sn = 3, st = 'Восприятия бренда', qn = 7, qd = col3[279].value, qv = list_to_text(col3[281:288]))

            Question.objects.create(lang=lang, sn = 3, st = 'Восприятия бренда', qn = 8, qd = col3[289].value, qv = list_to_text(col3[291:298]))

            Question.objects.create(lang=lang, sn = 3, st = 'Восприятия бренда', qn = 9, qd = col3[299].value, qv = list_to_text(col3[301:308]))

            Question.objects.create(lang=lang, sn = 3, st = 'Восприятия бренда', qn = 10, qd = col3[309].value, qv = list_to_text(col3[311:318]))

            Question.objects.create(lang=lang, sn = 3, st = 'Восприятия бренда', qn = 11, qd = col3[319].value, qv = list_to_text(col3[321:328]))

            Question.objects.create(lang=lang, sn = 3, st = 'Восприятия бренда', qn = 12, qd = col3[329].value, qv = list_to_text(col3[331:338]))

            Question.objects.create(lang=lang, sn = 3, st = 'Восприятия бренда', qn = 13, qd = col3[339].value, qv = list_to_text(col3[341:348]))

            Question.objects.create(lang=lang, sn = 3, st = 'Восприятия бренда', qn = 14, qd = col3[349].value, qv = list_to_text(col3[351:358]))

            Question.objects.create(lang=lang, sn = 3, st = 'Восприятия бренда', qn = 15, qd = col3[359].value, qv = list_to_text(col3[361:368]))

            Question.objects.create(lang=lang, sn = 3, st = 'Восприятия бренда', qn = 16, qd = col3[369].value, qv = '{}\\{}'.format(list_to_text(col3[371:378]), list_to_text(sh.row(370)[4:14])))

            Question.objects.create(lang=lang, sn = 3, st = 'Восприятия бренда', qn = 17, qd = col3[379].value, qv = '{}\\{}'.format(list_to_text(col3[382:390]), list_to_text(sh.row(381)[4:11])))

            Question.objects.create(lang=lang, sn = 4, st = 'Отличия в продукции', qn = 1, qd = col3[393].value, qv = list_to_text(col3[395:397]))

            Question.objects.create(lang=lang, sn = 4, st = 'Отличия в продукции', qn = 2, qd = col3[398].value, qv = list_to_text(col3[400:411]))

            Question.objects.create(lang=lang, sn = 4, st = 'Отличия в продукции', qn = 3, qd = col3[412].value, qv = list_to_text(col3[414:416]))

            Question.objects.create(lang=lang, sn = 4, st = 'Отличия в продукции', qn = 4, qd = col3[417].value, qv = list_to_text(col3[419:428]))

            Question.objects.create(lang=lang, sn = 5, st = 'Благосостояние семьи', qn = 1, qd = col3[431].value, qv = list_to_text(col3[433:437]))

            

            


            

            

            


            



    else:
        bbf = UploadFileFrom()
    if Excel.objects.all():
        file_path = Excel.objects.all()[0].file
    else:
        file_path = ''
    return render(request, 'upload/excel.html', {'form': bbf, 'file_path': file_path})

@login_required
def handle_uploaded_file(f):
    with open('files/excel/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

