from django import forms
from django.utils import timezone
from datetime import timedelta, datetime
from .models import Booking


class StyleFormMixin:
    """
    Добавляет стилевые атрибуты к полям формы - стилизация формы.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-control"


class TableForm(StyleFormMixin, forms.ModelForm):
    """
    Форма выбора стола с поддержкой временных интервалов бронирования.
    """

    open_time = 10
    close_booking_time = 20
    time_step = 30
    time_reserved = forms.ChoiceField(label="Время бронирования")
    next_day = timezone.localdate() + timedelta(days=1)

    date_reserved = forms.DateField(
        label="Дата бронирования",
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "min": next_day.strftime("%Y-%m-%d"),
                "max": (next_day + timedelta(days=6)).strftime("%Y-%m-%d"),
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super(TableForm, self).__init__(*args, **kwargs)

        times = [
            (
                datetime.strptime(f"{hour:02d}:{minute:02d}", "%H:%M").time(),
                f"{hour:02d}:{minute:02d}",
            )
            for hour in range(self.open_time, self.close_booking_time + 1)
            for minute in [0, self.time_step]
            if hour < self.close_booking_time
            or (hour == self.close_booking_time and minute == 0)
        ]

        self.fields["time_reserved"].choices = times

    class Meta:
        model = Booking
        fields = ["date_reserved", "time_reserved"]


class BookingForm(StyleFormMixin, forms.ModelForm):
    """
    Форма бронирования с использованием стилей.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance")

        if instance:
            self.initial["date_reserved"] = instance.date_reserved
            self.initial["time_reserved"] = instance.time_reserved

    class Meta:
        model = Booking
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(
                attrs={"placeholder": "Дополнительная информация", "rows": 6}
            ),
        }


class BookingUpdateForm(StyleFormMixin, forms.ModelForm):
    """
    Форма редактирования бронирования с использованием стилей.
    """

    open_time = 10
    close_booking_time = 20
    time_step = 30
    time_reserved = forms.ChoiceField(label="Время бронирования")
    next_day = timezone.localdate() + timedelta(days=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance")

        if instance:
            self.initial["date_reserved"] = instance.date_reserved
            self.initial["time_reserved"] = instance.time_reserved

        all_times = [
            (
                datetime.strptime(f"{hour:02d}:{minute:02d}", "%H:%M").time(),
                f"{hour:02d}:{minute:02d}",
            )
            for hour in range(self.open_time, self.close_booking_time + 1)
            for minute in [0, self.time_step]
            if hour < self.close_booking_time
            or (hour == self.close_booking_time and minute == 0)
        ]

        # Получаем занятые времена для выбранного стола и даты
        booked_times = self.get_booked_times(
            instance.table, self.initial.get("date_reserved", self.next_day)
        )

        # Фильтруем список времен, оставляя только свободные
        available_times = [(t, s) for t, s in all_times if (t, s) not in booked_times]

        self.fields["time_reserved"].choices = available_times

    @staticmethod
    def get_booked_times(table, date):
        """
        Возвращает список занятых времен для указанного стола и даты.
        НЕОБХОДИМО РЕАЛИЗОВАТЬ ЗАПРОС К БАЗЕ ДАННЫХ.
        """
        from .models import Booking  # Импортируйте вашу модель Booking

        booked_slots = Booking.objects.filter(
            table=table, date_reserved=date
        ).values_list("time_reserved", flat=True)
        return [
            (datetime.strptime(str(slot), "%H:%M:%S").time(), str(slot)[:5])
            for slot in booked_slots
        ]

    class Meta:
        model = Booking
        fields = ["time_reserved", "message"]
        widgets = {
            "message": forms.Textarea(
                attrs={"placeholder": "Дополнительная информация", "rows": 6}
            ),
        }
