from django.urls import path
from spam_sms import views

urlpatterns = [
    path('', views.home, name='home'),
    path('', views.data, name='data'),
    path('', views.proses, name='proses'),
    path('', views.normalisasi, name='normalisasi'),
    path('', views.upload, name='upload'),
]
