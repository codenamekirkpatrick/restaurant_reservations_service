from celery import shared_task
from django.utils import timezone
from datetime import timedelta, datetime
from restaurant.models import Booking


@shared_task
def cancel_expired_bookings():
    """
    Отменяет бронирование столов, если истек срок бронирования.
    """
    now = timezone.now()
    active_bookings = Booking.objects.filter(is_active=True)

    for booking in active_bookings:
        # Объединение даты и времени бронирования в объект datetime
        start_datetime = datetime.combine(booking.date_reserved, booking.time_reserved)

        # Проверка, что datetime без информации о временной зоне
        if timezone.is_naive(start_datetime):
            # Делаем datetime-aware, устанавливая текущую временную зону
            start_datetime = timezone.make_aware(
                start_datetime, timezone.get_current_timezone()
            )

        # Вычисляем время истечения бронирования
        expiration_time = start_datetime + timedelta(hours=booking.duration)

        # Если текущее время больше или равно времени истечения, отменяем бронирование
        if now >= expiration_time:
            booking.cancel()
            print(
                f"Бронирование для стола {booking.table.number} было отменено в связи с итсечением времени бронирования"
            )
