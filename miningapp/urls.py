from django.urls import path
from . import views
from .views import PasswordsChangeView

app_name='mining'
urlpatterns = [
    # Page urls and paths
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    #path('team/', views.team, name='team'),
    path('reviews/', views.reviews, name='reviews'),
    path('services/', views.services, name='services'),
    path('tac/', views.tac, name='tac'),
    path('plans/', views.plans, name='plans'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('register/<str:refcode>/', views.uplineRegister, name='upline_register'),
    path('account/', views.account, name='account'),
    path('account/mining-history/',views.investHistory, name='invest_history'),
    path('account/mining/<str:investment_id>/',views.investmentDetail, name='investment_detail'),
    path('account/withdrawal-history/', views.withdrawalHistory, name='withdrawal_history'),
    path('account/withdraw/', views.withdrawalAssets, name='withdraw'),
    path('account/invest/', views.createInvest, name='invest'),
    path('account/invest/invoice/<str:investment_id>/', views.invoice, name='invoice'),
    path('account/profile/', views.profile, name='profile'),
    path('account/affiliates/', views.affiliates, name='affiliates'),
    path('account/notifications/', views.notifications, name='notifications'),
    path('account/change-password/', PasswordsChangeView.as_view(template_name="change_password.html")),
    path('account/change-password/success/', views.passwordChangeSuccess, name="password_change_success"),

    # Pseudo views
    path('process_message/', views.processMessage, name='process_message'),
    path('process_registeration/', views.processRegisteration, name='process_registeration'),
    path('process_investment/', views.processInvestment, name='process_investment'),
    path('invest_from_balance/', views.investFromBalance, name='invest_from_balance'),
    path('confirm_payment/', views.confirmPayment, name='confirm_payment'),
    path('investment-pdf/<str:investment_id>/', views.investmentPDF, name='investment_pdf'),
]