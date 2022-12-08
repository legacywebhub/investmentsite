from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, FileResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.conf import settings
from django.urls import reverse_lazy
from .models import *
import json
# Report lab imports
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


# Create your views here.

def index(request):
    company = CompanyInfo.objects.last()
    return render(request, 'index.html', {'company':company})



def register(request):
    company = CompanyInfo.objects.last()

    if request.method == "POST":
        if 'register-submit' in request.POST:
            email = request.POST['email']
            first_name = request.POST['first-name']
            last_name = request.POST['last-name']
            location = request.POST['location']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password2 == password1:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Sorry this email has already been taken!')
                else:
                    # Saving user and user instances
                    user = User.objects.create_user(email=email, first_name=first_name, last_name=last_name, password=password2)
                    user.save()
                    # On user save, a profile instance is created dynamically from signals.py
                    # Fetching profile of user created from signals.py to update upliner
                    profile = Profile.objects.get(user=user)
                    # Checking if user allowed location
                    if location != '' or location != ' ':
                        profile.location = location
                    profile.save()
                    messages.success(request, 'Your account has successfully been created... you can now sign in!')
                    return redirect('mining:login')
            else:
                messages.error(request, 'Passwords does not match... Please try again')
    return render(request, 'register.html', {'company':company})



def uplineRegister(request, refcode):
    try:
        upline = Profile.objects.get(ref_code=refcode)
    except:
        return redirect('mining:register')
    
    company = CompanyInfo.objects.last()

    if request.method == "POST":
        if 'register-submit' in request.POST:
            email = request.POST['email']
            first_name = request.POST['first-name']
            last_name = request.POST['last-name']
            location = request.POST['location']
            password1 = request.POST['password1']
            password2 = request.POST['password2']


            if password2 == password1:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Sorry this email has already been taken!')
                else:
                    # Saving user and user instances
                    user = User.objects.create_user(email=email, first_name=first_name, last_name=last_name, password=password2)
                    user.save()
                    # On user save, a profile instance is created dynamically from signals.py
                    # Fetching profile of user created from signals.py to update upliner
                    profile = Profile.objects.get(user=user)
                    profile.upline = upline.user
                    # Checking if user allowed location
                    if location != '' or location != ' ':
                        profile.location = location
                    profile.save()
                    # Updating downlines for upline
                    upline.downlines.add(user)
                    upline.save()
                    messages.success(request, 'Your account has successfully been created... you can now sign in!')
                    return redirect('mining:login')
            else:
                messages.error(request, 'Passwords does not match... Please try again')
    return render(request, 'register.html', {'company': company,'upline':upline})



def login(request):
    company = CompanyInfo.objects.last()

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
    return render(request, 'login.html', {'company':company})



def logout(request):
    auth.logout(request)
    return redirect('/')



def about(request):
    company = CompanyInfo.objects.last()
    return render(request, 'about.html', {'company':company})



def faq(request):
    company = CompanyInfo.objects.last()
    return render(request, 'faq.html', {'company':company})



def contact(request):
    company = CompanyInfo.objects.last()
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
                    f'{subject} ({location})', message, email, [company.email,], fail_silently=False
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
    company = CompanyInfo.objects.last()
    account = Account.objects.get(user=request.user)
    notifications = Notification.objects.filter(user=request.user).order_by('-date')[:4]

    context = {
        'company':company,
        'notifications':notifications,
        'account':account, 
    }
    return render(request, 'dashboard.html', context)



@login_required
def profile(request):
    user = request.user
    company = CompanyInfo.objects.last()
    notifications = Notification.objects.filter(user=request.user).order_by('-date')[:4]

    if request.method == 'POST':
        if 'profile-pic-submit' in request.POST:
            if 'picture' in request.FILES:
                pic = request.FILES['picture']

                profile = Profile.objects.get(user=request.user.id)
                profile.profile_pic = pic
                profile.save()
                messages.success(request, 'Profile picture successfully updated!')
        elif 'update-user-submit' in request.POST:
            first_name = request.POST['first-name'] or None
            last_name = request.POST['last-name'] or None
            email = request.POST['email'] or None

            if email=='' or email==None:
                email = request.user.email

            if first_name=='' or first_name==None:
                first_name = request.user.first_name

            if last_name=='' or last_name==None:
                last_name = request.user.last_name


            user = User.objects.get(id=request.user.id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            messages.success(request, 'Details successfully updated')
    return render(request, 'profile.html', {'user':user, 'company':company, 'notifications':notifications})



class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('mining:password_change_success')



@login_required
def passwordChangeSuccess(request):
    company = CompanyInfo.objects.last()
    return render(request, 'success.html', {'company':company})



@login_required
def investHistory(request):
    company = CompanyInfo.objects.last()
    notifications = Notification.objects.filter(user=request.user).order_by('-date')[:4]
    user_investments = Investment.objects.filter(user=request.user).order_by('-date')
    p = Paginator(user_investments, 10)
    page = request.GET.get('page')
    investments = p.get_page(page)
    context = {'company':company, 'notifications':notifications, 'investments':investments}
    return render(request, 'investment_history.html', context)



@login_required
def investmentDetail(request, investment_id):
    company = CompanyInfo.objects.last()
    notifications = Notification.objects.filter(user=request.user).order_by('-date')[:4]
    investment = get_object_or_404(Investment, investment_id=investment_id)
    context = {'company':company, 'notifications':notifications, 'investment':investment}
    return render(request, 'investment_detail.html', context)



@login_required
def withdrawalHistory(request):
    company = CompanyInfo.objects.last()
    notifications = Notification.objects.filter(user=request.user).order_by('-date')[:4]
    user_withdrawals = Transaction.objects.filter(user=request.user, type='withdraw').order_by('-date')
    p = Paginator(user_withdrawals, 10)
    page = request.GET.get('page')
    withdrawals = p.get_page(page)
    context = {'company': company,'notifications': notifications, 'withdrawals':withdrawals}
    return render(request, 'withdrawal_history.html', context)



@login_required
def withdrawalAssets(request):
    company = CompanyInfo.objects.last()
    notifications = Notification.objects.filter(user=request.user).order_by('-date')[:4]
    account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        if 'withdraw-submit' in request.POST:
            payment_method = request.POST['method']
            payment_addresss = request.POST['address']
            amount = int(request.POST['amount'])
            network = request.POST['network']

            if amount <= account.total_balance:
                try:
                    withdraw_request = Transaction.objects.create(
                        user=request.user,
                        type='withdraw',
                        payment_method=payment_method,
                        amount=amount,
                        payment_address=payment_addresss,
                        network=network
                    )
                    withdraw_request.save()
                    # Updating user account after placing withdrawal request
                    # adding up balance and referral bonus
                    account.balance += account.referral_bonus
                    # resetting referral bonus
                    account.referral_bonus = 0
                    # deducting from balance
                    account.balance = account.balance - amount
                    account.save()
                    messages.success(request, 'Withdraw request was successsfully placed')
                except Exception as e:
                    print(e)
                    messages.error(request, e)
            else:
                messages.error(request, 'Insufficient funds...')
    context = {'company':company, 'notifications':notifications}
    return render(request, 'withdraw_assets.html', context)



@login_required
def createInvest(request):
    company = CompanyInfo.objects.last()
    notifications = Notification.objects.filter(user=request.user).order_by('-date')[:4]
    packages = Package.objects.all()
    context = {'company':company, 'notifications': notifications, 'packages':packages}
    return render(request, 'create_invest.html', context)



@login_required
def invoice(request):
    company = CompanyInfo.objects.last()
    notifications = Notification.objects.filter(user=request.user).order_by('-date')[:4]
    try:
        investment = Investment.objects.filter(user=request.user).last()
        print(investment)
    except Exception as e:
        print(e)
        return render('/account/invest/')

    context = {
        'company':company,
        'notifications':notifications,
        'investment':investment, 
    }
    return render(request, 'invoice.html', context)



@login_required
def affiliates(request):
    company = CompanyInfo.objects.last()
    notifications = Notification.objects.filter(user=request.user).order_by('-date')[:4]
    profile = Profile.objects.get(user=request.user)
    p = Paginator(profile.downlines.all(), 10)
    page = request.GET.get('page')
    downlines = p.get_page(page)
    context = {'company':company, 'notifications':notifications, 'downlines':downlines}
    return render(request, 'affiliates.html', context)



def error404(request, exception):
    company = CompanyInfo.objects.last()
    notifications = Notification.objects.filter(user=request.user).order_by('-date')[:4]
    context = {'company':company, 'notifications':notifications}
    return render(request, 'error404.html', context)



def error500(request):
    company = CompanyInfo.objects.last()
    notifications = Notification.objects.filter(user=request.user).order_by('-date')[:4]
    context = {'company':company, 'notifications':notifications}
    return render(request, 'error500.html', context)



# Pseudo views

# View to start new mining investment
def processInvestment(request):
    data = json.loads(request.body)
    id = data['investment']['id']
    package = int(data['investment']['package'])
    payment = data['investment']['payment']
    amount = data['investment']['amount']
    package = Package.objects.get(id=2)
    
    try:
        investment = Investment.objects.create(
            investment_id = id,
            user = request.user,
            package = package,
            payment_method = payment,
            amount = amount
        )
        investment.save()
        return JsonResponse(f'Mining Investment was successfully placed', safe=False)
    except Exception as e:
        print(e)
        return JsonResponse("Mining project could not be placed", safe=False)


# View to invest from account balance
def investFromBalance(request):
    data = json.loads(request.body)
    print(data)
    id = data['investment']['id']
    action = data['investment']['action']
    amount = int(data['investment']['amount'])
    account = Account.objects.get(user=request.user)
    investment = Investment.objects.get(investment_id=id)

    if action == 'pay':
        if amount <= account.total_balance:
            # Merging up account balance and bonus
            account.balance += account.referral_bonus
            account.referral_bonus = 0
            # Deducting amount from account balance to fund investment
            account.balance -= amount
            account.save() 
            # Approving investment since user balance has sufficient funds
            investment.status == "approved"
            investment.save()
            # Adding to transaction history
            transaction = Transaction.objects.create(
                user=request.user,
                type='withdraw',
                amount=amount
            )
            transaction.save()
            return JsonResponse("Mining has been approved and successfully started", safe=False)
        else:
            return JsonResponse("Insufficient funds", safe=False)
    else:
        return JsonResponse("Invalid command", safe=False)


# view to alert admins of payment
def confirmPayment(request):
    data = json.loads(request.body)
    print(data)
    id = int(data['id'])
    investment = Investment.objects.get(investment_id=id)
    subject = f'PAYMENT CONFIRMATION FOR INVESTMENT {investment.investment_id}'
    message = f'*Investment ID - {investment.investment_id}\n*Payment Method - {investment.payment_method}\n*Amount - {investment.amount}\n*Date/Time - {investment.date}'
    print(message)

    try:
        # Trying to notify company or admins via mail
        send_mail(
            subject, message, request.user.email, [settings.EMAIL_HOST_USER,], fail_silently=False
        )
        print(f'Message was successfully sent to admins...')
    except:
        pass
    message = Message.objects.create(name=request.user.fullname, email=request.user.email, subject=subject, message=message)
    message.save()
    return JsonResponse("Your payment would be confirmed and updated... check back later", safe=False)


# view to allow users download investment info in PDF
def investmentPDF(request, investment_id):
    company = CompanyInfo.objects.last()
    #Get investment
    investment = get_object_or_404(Investment, investment_id=investment_id)
    #Create Bytestream buffer
    buf = io.BytesIO()
    #create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    #create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 12)

    #Add lines of text
    lines = [
    f'{company.name}',
    '',
    '===============================================================',
    '',
    'Mining details',
    '',
    '* Mining ID: ' + investment.investment_id,
    '',
    '* Investor name: ' + investment.user.fullname,
    '',
    '* Investor email: ' + investment.user.email,
    '',
    '* Mining package: ' + investment.package.package,
    '',
    '* Mining amount: $' + str(investment.amount),
    '',
    '* Mining daily profit: $' + str(investment.daily_profit),
    '',
    '* Mining total profits: $' + str(investment.total_profit),
    '',
    '* Mining returns: $' + str(investment.roi),
    '',
    '* Mining current returns: $' + str(investment.returns),
    '',
    '* Mining duration: ' + str(investment.package.duration_in_days) + 'days',
    '',
    '* Mining status: ' + investment.get_status_display(),
    '',
    '===============================================================',
    '',
    ]

    for line in lines:
        textob.textLine(line)
     
    #finish up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename=f'mining-info-{investment.investment_id}.pdf')