from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ("phone_number", "first_name", "last_name", "father_name")

    list_display = ("phone_number", "first_name", "last_name")
