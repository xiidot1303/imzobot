from django.db import models
from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey

class Bot_user(models.Model):
    user_id = models.IntegerField(null=True)
    name = models.CharField(null=True, blank=True, max_length=100)
    phone = models.CharField(null=True, blank=True, max_length=40)
    lang = models.CharField(null=True, blank=True, max_length=5)

class Question(models.Model):
    sn = models.IntegerField(null=True, blank=True) # section number
    st = models.CharField(null=True, blank=True, max_length=10) # section title
    qn = models.IntegerField(null=True, blank=True) # questin number
    qd = models.CharField(null=True, blank=True, max_length=300) # question description
    qv = models.CharField(null=True, blank=True, max_length=1000) # question variants
    lang = models.CharField(null=True, blank=True, max_length=10) # question language
    
    
class Excel(models.Model):
    file = models.FileField(upload_to='excel/', null=True, blank=True)
    lang = models.CharField(null=True, blank=True, max_length=10)

class Answer(models.Model):
    user = ForeignKey('Bot_user', null=True, blank=False, on_delete=models.PROTECT)
    st = models.CharField(null=True, blank=True, max_length=10) # section title
    sn = models.IntegerField(null=True, blank=True) # section number
    qn = models.IntegerField(null=True, blank=True) # questin number
    ans = models.CharField(null=True, blank=True, max_length=300)
    end = models.BooleanField(null=True, blank=True) # completed answer or not
    date = models.DateField(null=True, blank=True, max_length=20)
    index = models.IntegerField(null=True)
class Answer_index(models.Model):
    user_id = models.IntegerField(null=True)
    end = models.BooleanField(null=True, blank=True) # completed answer or not
    date = models.DateTimeField(db_index = True, null=True, auto_now_add=True, blank=True)