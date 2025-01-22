from django.contrib import admin
from users.models import User


@admin.register(User)
class TableAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "phone",
        "country",
        "about_me",
        "avatar",
    )
    list_filter = ("email", "phone")
    search_fields = ("email", "phone", "first_name", "last_name")
