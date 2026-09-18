from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("IELTS profile", {
            "fields": (
                "full_name", "exam_date", "preferred_theme",
                "CL", "CR", "CW", "CS", "CO",
                "TL", "TR", "TW", "TS", "TO",
            )
        }),
    )
    list_display = ("username", "full_name", "CO", "TO", "exam_date")


admin.site.register(CustomUser, CustomUserAdmin)