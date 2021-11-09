from django.contrib import admin
from app.models import *

class Bot_userAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'phone')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('sn', 'st', 'qn', 'qd')

class ExcelAdmin(admin.ModelAdmin):
    list_display = ['file']

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('sn', 'st', 'qn', 'ans', 'date')

class Answer_indexAdmin(admin.ModelAdmin):
    list_display = ('pk', 'end', 'user_id', 'date')


admin.site.register(Bot_user, Bot_userAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Excel, ExcelAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Answer_index, Answer_indexAdmin)