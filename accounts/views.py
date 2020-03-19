from django.shortcuts import redirect
from django.core.mail import send_mail
from django.contrib import messages

def send_login_email(request):
    '''отправить сообщение для входа в систему'''
    email = request.POST['email']  
    # print(type(send_mail))
    send_mail(
        'Your login link for Superlists',
        'Use this link to log in',
        'noreply@superlists',
        [email],
    )
    messages.success(
        request,
        "Check your email"
    )
    return redirect('/')
