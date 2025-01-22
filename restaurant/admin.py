from django.contrib import admin
from restaurant.models import Table, Booking, BookingHistory


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "number",
        "seats",
    )
    list_filter = (
        "seats",
        "number",
    )
    search_fields = ("number",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    # form = BookingForm
    list_display = (
        "id",
        "table",
        "client",
        "date_reserved",
        "time_reserved",
        "duration",
        "is_active",
    )
    list_filter = ("table",)
    search_fields = ("table", "client", "date_reserved")


@admin.register(BookingHistory)
class BookingHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "table",
        "cancelled_at",
    )
    list_filter = (
        "table",
        "cancelled_at",
    )
    search_fields = (
        "table",
        "cancelled_at",
    )
