from django.urls import path, reverse_lazy
from . import views

app_name='mining'
urlpatterns = [
    # Page urls and paths
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('account/', views.account, name='account'),
    path('account/withdrawal-history/', views.withdrawalHistory, name='withdrawal_history'),
    path('account/withdraw/', views.withdrawalAssets, name='withdraw'),
]