from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.conf import settings
from .models import *


# general Variables
company = CompanyInfo.objects.last()

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        if 'register-submit' in request.POST:
            email = request.POST['email']
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password2 == password1:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Sorry this email has already been taken!')
                else:
                    if User.objects.filter(username=username).exists():
                        messages.error(request, 'Sorry this username has been picked!')
                    else:
                        # Saving user and user instances
                        user = User.objects.create_user(email=email, password=password2)
                        user.username = username
                        user.save()
                        messages.success(request, 'Your account has successfully been created... you can now sign in!')
            else:
                messages.error(request, 'Passwords does not match... Please try again')  
    return render(request, 'register.html')

def login(request):
    if request.method == "POST":
        if 'login-submit' in request.POST:
            email = request.POST['email']
            password = request.POST['password']

            user = auth.authenticate(email=email, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/account/')
            else:
                messages.error(request, 'Invalid credentials..   Please try again')
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def about(request):
    return render(request, 'about.html')

def faq(request):
    return render(request, 'faq.html')

def contact(request):
    if request.method == 'POST':
        if 'message' in request.POST:
            name = request.POST['name']
            location = request.POST['location']
            email = request.POST['email']
            subject = request.POST['subject']
            message = request.POST['message']

            try:
                email.index('@') and email.index('.')
            except ValueError:
                messages.info(request, 'Your email is not valid')
            else:
                try:
                    # Trying to notify company or admins via mail
                    send_mail(
                    f'{subject} ({location})', message, email, [company.email1, company.email2], fail_silently=False
                    )
                    print(f'Message was successfully sent to admins...')
                except:
                    pass
                message = Message.objects.create(name=name, location=location, email=email, subject=subject, message=message)
                message.save()
                messages.success(request, 'Your message was sent successfully')
    return render(request, 'contact.html')

@login_required
def account(request):
    user = request.user

    if not user.is_authenticated:
        return redirect('/login/')
    return render(request, 'dashboard.html', {'user':user})


@login_required
def withdrawalHistory(request):
    user = request.user

    if not user.is_authenticated:
        return redirect('/login/')
    return render(request, 'withdrawal_history.html', {'user':user})


@login_required
def withdrawalAssets(request):
    user = request.user

    if not user.is_authenticated:
        return redirect('/login/')
    return render(request, 'withdraw_assets.html', {'user':user})



@login_required
def createInvest(request):
    user = request.user

    if not user.is_authenticated:
        return redirect('/login/')
    return render(request, 'create_invest.html', {'user':user})