from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView, UpdateView
from config import settings
from restaurant.forms import TableForm, BookingForm, BookingUpdateForm
from restaurant.models import Table, Booking, BookingHistory
from restaurant.templatetags.custom_filters import formatting_date, formatting_time


class TableSelectionView(LoginRequiredMixin, View):
    """
    Отображает страницу со списком доступных столов и формой для выбора даты и времени бронирования.
    """

    @staticmethod
    def get(request):
        """
        Отображение формы выбора даты и времени бронирования.
        """
        form = TableForm()
        return render(request, "restaurant/table_list.html", {"form": form})

    @staticmethod
    def post(request):
        """
        Получение и проверка введенных даты и времени и отображение списка доступных столов.
        """
        form = TableForm(request.POST)
        if form.is_valid():
            date_reserved = form.cleaned_data["date_reserved"]
            time_reserved = datetime.strptime(
                form.cleaned_data["time_reserved"], "%H:%M:%S"
            ).time()

            # Получаем все столы и проверяем их доступность
            tables = Table.objects.all()
            table_statuses = []
            for table in tables:
                is_available = not Booking.objects.filter(
                    table=table,
                    date_reserved=date_reserved,
                    time_reserved__range=(
                        time_reserved,
                        (
                            datetime.combine(date_reserved, time_reserved)
                            + timedelta(hours=3)
                        ).time(),
                    ),
                ).exists()
                table_statuses.append((table, is_available))

            return render(
                request,
                "restaurant/table_list.html",
                {
                    "form": form,
                    "table_statuses": table_statuses,
                    "selected_date": date_reserved,
                    "selected_time": time_reserved,
                },
            )
        return render(request, "restaurant/table_list.html", {"form": form})


class BookingCreateView(LoginRequiredMixin, View):
    """
    Создание бронирования.
    """

    @staticmethod
    def get(request, table_id, date_reserved, time_reserved):
        """
        Получение информации о столе, дате и времени.
        """
        # Получаем информацию о столе
        table = Table.objects.get(id=table_id)

        # Создаем форму с предопределенными значениями
        form = BookingForm(
            initial={
                "table": table,
                "date_reserved": date_reserved,
                "time_reserved": time_reserved,
            }
        )

        return render(
            request,
            "restaurant/booking_form.html",
            {
                "form": form,
                "table": table,
                "date_reserved": date_reserved,
                "time_reserved": time_reserved,
            },
        )

    def post(self, request, table_id, date_reserved, time_reserved):
        """
        Создание бронирования.
        Присваивание текущего пользователя к заказу.
        Логирование данные перед сохранением.
        """
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.client = self.request.user
            booking.table_id = table_id
            booking.date_reserved = date_reserved
            booking.time_reserved = time_reserved
            booking.save()

            # Отправка письма пользователю
            subject = "Подтверждение бронирования стола"
            message = (
                f"Уважаемый(ая) {request.user.first_name},\n\n"
                f"Стол №{booking.table.number} [мест: {booking.table.seats}] на "
                f"{formatting_date(booking.date_reserved)} в {formatting_time(booking.time_reserved)} "
                f"успешно забронирован.\n\n"
                f"Спасибо за использование сервиса!\n"
                f"До скорой встречи!"
            )
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [request.user.email]
            send_mail(subject, message, from_email, recipient_list)

            return redirect("restaurant:booking_list")
        else:
            table = Table.objects.get(id=table_id)
            return render(
                request,
                "restaurant/booking_form.html",
                {
                    "form": form,
                    "table": table,
                    "date_reserved": date_reserved,
                    "time_reserved": time_reserved,
                },
            )


class BookingUpdateView(LoginRequiredMixin, UpdateView):
    """
    Редактирование бронирования.
    """

    model = Booking
    form_class = BookingUpdateForm
    success_url = reverse_lazy("restaurant:booking_list")

    def form_valid(self, form):
        """
        Переопределение формы валидации.
        Присваивание текущего пользователя к заказу.
        Логирование данные перед сохранением.
        """
        booking = form.save(commit=False)
        booking.client = self.request.user

        print(f"Дата бронирования: {booking.date_reserved}")
        print(f"Время бронирования: {booking.time_reserved}")
        print(f"Стол: {booking.table}")
        print(f"Клиент: {booking.client}")

        booking.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Вывод ошибки формы
        """
        print("Форма не прошла валидацию. Ошибки:", form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        """
        Дополнительная информация
        """
        context = super().get_context_data(**kwargs)
        table = Table.objects.get(pk=self.object.table.pk)

        context["table"] = table
        context["date"] = self.object.date_reserved
        context["is_edit"] = True

        return context


class BookingListView(LoginRequiredMixin, ListView):
    """
    Просмотр списка бронирований
    """

    model = Booking
    context_object_name = "bookings"

    def get_queryset(self):
        """
        Просмотр только своих бронирований
        """
        user = self.request.user

        # порядок отображения по дате и времени
        ordered = Booking.objects.filter(client=user).order_by(
            "date_reserved", "time_reserved"
        )
        print(ordered)
        return ordered

    @staticmethod
    def post(request):
        """
        Отмена бронирования
        """
        booking_id = request.POST.get("booking_id")
        booking = get_object_or_404(Booking, pk=booking_id, client=request.user)
        booking.cancel()
        messages.success(request, "Бронирование успешно отменено.")
        return redirect("restaurant:booking_list")

    def get_context_data(self, **kwargs):
        """
        Дополнительная информация
        """
        context = super().get_context_data(**kwargs)
        context["booking_history"] = BookingHistory.objects.filter(
            client=self.request.user
        ).order_by("-cancelled_at")
        # print(context['booking_history'])
        return context


class MainPageView(TemplateView):
    """
    Главная страница ресторана.
    """

    template_name = "restaurant/index.html"
    success_template = "restaurant/success_send_message.html"

    def post(self, request):
        """
        Обработка POST-запроса: получение данных из формы и отправка письма.
        """
        # Получение данных из формы
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        message_content = request.POST.get("message", "")

        # Проверка, что обязательные поля заполнены
        if not name or not email or not message_content:
            return HttpResponse("Пожалуйста, заполните все обязательные поля.")

        # Формирование сообщения
        message = f"""
               Поступила обратная связь от пользователя:
               Имя: {name}
               Email: {email}
               Телефон: {phone}
               Сообщение: {message_content}
               """

        # Отправка письма
        send_mail(
            f"Сообщение от пользователя {email}",
            message,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
        )

        # Отображение страницы успеха
        return render(request, self.success_template)


class AboutPageView(TemplateView):
    """
    Страница с информацией о ресторане.
    """

    template_name = "restaurant/about.html"


class MenuPageView(TemplateView):
    """
    Страница с меню.
    """

    template_name = "restaurant/menu.html"


class ContactPageView(View):
    template_name = "restaurant/contacts.html"
    success_template = "restaurant/success_send_message.html"

    def get(self, request):
        """
        Обработка GET-запроса: отображаем страницу с формой.
        """
        return render(request, self.template_name)

    def post(self, request):
        """
        Обработка POST-запроса: получение данных из формы и отправка письма.
        """
        # Получение данных из формы
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        message_content = request.POST.get("message", "")

        # Проверка, что обязательные поля заполнены
        if not name or not email or not message_content:
            return HttpResponse("Пожалуйста, заполните все обязательные поля.")

        # Формирование сообщения
        message = f"""
               Поступила обратная связь от пользователя:
               Имя: {name}
               Email: {email}
               Телефон: {phone}
               Сообщение: {message_content}
               """

        # Отправка письма
        send_mail(
            f"Сообщение от пользователя {email}",
            message,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
        )

        # Отображение страницы успеха
        return render(request, self.success_template)
