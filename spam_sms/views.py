from django.shortcuts import render

# Create your views here.
def spam_sms(request):
    return render(request, 'spam_sms.html', {})