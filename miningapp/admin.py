from django.contrib import admin
from .models import *

class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance', 'referral_balance', 'total_balance')
    list_filter = ()
    list_per_page = 20

    def name(self, obj):
        if obj.user.fullname:
            name = obj.user.fullname
        elif obj.user.username:
            name = obj.user.username
        elif obj.user.first_name:
            name = obj.user.first_name
        else:
            name = obj.user.email
        return name


class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')


class DepositAdmin(admin.ModelAdmin):
    list_display = ( 'date', 'user', 'amount')
    list_display_links = ('date',)
    list_per_page = 20


class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('date', 'user', 'package', 'amount', 'payment_method', 'approved_date', 'end_date', 'status', 'returns')
    list_filter = ('date','user', 'package', 'payment_method', 'status',)
    list_display_links = ('date', 'user', 'amount',)
    list_per_page = 20

    # Render filtered options only after 5 characters were entered
    filter_input_length = {
        "user": 3,
    }

    def investor(self, obj):
        if obj.user.fullname:
            name = obj.user.fullname
        elif obj.user.username:
            name = obj.user.username
        elif obj.user.first_name:
            name = obj.user.first_name
        else:
            name = obj.user.email
        return name


class MessageAdmin(admin.ModelAdmin):
    list_display = ('date_received', 'subject', 'name', 'email')
    list_filter = ('date_received',)
    list_per_page = 20


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('date', 'name', 'message')
    list_filter = ('date',)
    list_per_page = 20

    def name(self, obj):
        if obj.user.fullname:
            name = obj.user.fullname
        elif obj.user.username:
            name = obj.user.username
        elif obj.user.first_name:
            name = obj.user.first_name
        else:
            name = obj.user.email
        return name


class PackageAdmin(admin.ModelAdmin):
    list_display = ('package', 'daily_profit_percentage', 'minimum_amount', 'maximum_amount', 'duration_in_days')
    list_per_page = 10


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('profile_user', 'location', 'ref_code', 'upliner')
    list_per_page = 20

    def profile_user(self, obj):
        if obj.user.fullname:
            name = obj.user.fullname
        elif obj.user.username:
            name = obj.user.username
        elif obj.user.first_name:
            name = obj.user.first_name
        else:
            name = obj.user.email
        return name

    def upliner(self, obj):
        if obj.upline != None:
            if obj.upline.fullname:
                name = obj.upline.fullname
            elif obj.upline.username:
                name = obj.upline.username
            elif obj.upline.first_name:
                name = obj.upline.first_name
            else:
                name = obj.upline.email
            return name
        else:
            return '-'



class UserAdmin(admin.ModelAdmin):
    list_display = ( 'fullname', 'email',)
    list_display_links = ('fullname', 'email')
    list_per_page = 20



class WithdrawAdmin(admin.ModelAdmin):
    list_display = ('date', 'user', 'amount', 'payment_method', 'status')
    list_display_links = ('date', 'user', 'amount',)
    list_filter = ('date', 'user', 'status', 'payment_method',)
    list_per_page = 20


# Register your models here.
admin.site.register(Account, AccountAdmin)
admin.site.register(CompanyInfo, CompanyInfoAdmin)
admin.site.register(Deposit)
admin.site.register(Investment, InvestmentAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Withdraw, WithdrawAdmin)
