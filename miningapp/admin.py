from django.contrib import admin
from .models import *

class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance', 'referral_bonus', 'total_balance')
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


class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('date', 'amount', 'package', 'payment_method', 'approved_date', 'end_date', 'status')
    list_filter = ('date', 'package', 'payment_method', 'status',)
    list_display_links = ('date', 'amount',)
    list_per_page = 20

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
    list_display = ('date', 'name')
    list_filter = ('date',)
    list_per_page = 30

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


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'amount', 'type', 'payment_method', 'status')
    list_display_links = ('date', 'amount',)
    list_filter = ('date', 'type', 'status', 'payment_method',)
    list_per_page = 20


class UserAdmin(admin.ModelAdmin):
    list_display = ( 'fullname', 'email',)
    list_display_links = ('fullname', 'email')
    list_per_page = 20


# Register your models here.
admin.site.register(Account, AccountAdmin)
admin.site.register(CompanyInfo, CompanyInfoAdmin)
admin.site.register(Investment, InvestmentAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(User, UserAdmin)
