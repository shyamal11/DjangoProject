from django.contrib import admin
from Loginify.models import UserDetails



@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('Username', 'Email')

