from django.contrib import admin
from myauth.models import UserModel


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'gender', 'last_seen', )
    search_fields = ('user', 'gender')
