from django.urls import path
from spam_sms import views

urlpatterns = [
    path('', views.spam_sms, name='home'),
]