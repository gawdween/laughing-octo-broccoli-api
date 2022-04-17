from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from api.models import User, CustomerProfile, CustomerTransaction

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email', 'phone_number', 'is_admin', 'is_staff', 'is_active', 'is_activated', 'registration_date')


class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'first_name', 'last_name', 'phone_number']


class CustomerTransactionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'owner', 'value', 'purchase_date', 'payment_status']
    
   


admin.site.register(User, UserAdmin)
admin.site.register(CustomerProfile, CustomerProfileAdmin)
admin.site.register(CustomerTransaction, CustomerTransactionAdmin)