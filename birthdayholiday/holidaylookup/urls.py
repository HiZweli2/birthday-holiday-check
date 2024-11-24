from django.urls import path

from . import views

urlpatterns = [
    path('', views.check_holiday, name='check_holiday')
]