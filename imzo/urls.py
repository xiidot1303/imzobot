"""imzo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from config import TOKEN, WHERE
from app.views.main import *
from app.views.upload import *
from app.views.get import *
from app.views.report import *
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeDoneView, PasswordChangeView


urlpatterns = [
    path('accounts/login/', LoginView.as_view()),

    path('xiidot1303/', admin.site.urls),
    path(TOKEN, bot_webhook),
    path('', report_by_index, name='main_menu'),
    path('report_by_index', report_by_index, name='report_by_index'),
    path('report_answer/<int:pk>/', report_answer, name='report_answer'),

    path('get_answers_excel/<int:index>/', get_answers_excel, name='get_answers_excel'),

    path('upload_file', upload_file, name='upload_file'),
    path('files/excel/<str:file_name>/', get_excel, name='get_excel'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
