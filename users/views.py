from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (
    PasswordResetView,
    LoginView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
)
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _

from config import settings
from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, CustomAuthenticationForm, UserProfileForm
from users.models import User


class UserRegisterView(CreateView):
    """
    Регистрация пользователя
    """

    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")


class CustomLoginView(LoginView):
    """
    Авторизация пользователя
    """

    form_class = CustomAuthenticationForm
    template_name = "users/login.html"
    success_url = reverse_lazy("restaurant:index")


class UserDetailView(LoginRequiredMixin, LoginView):
    """
    Просмотр профиля пользователя
    """

    model = User
    template_name = "users/profile.html"
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["note_text"] = self.request.user.notes
        return context

    def post(self, request, *args, **kwargs):
        note_text = request.POST.get("note-text")
        user = self.request.user
        user.notes = note_text
        user.save()
        return HttpResponseRedirect(reverse("users:profile"))


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """
    Редактирование информации пользователя
    """

    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        """
        Валидация формы
        """

        if form.is_valid:
            user = form.save(commit=True)
            user.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("users:profile", args=[self.kwargs.get("pk")])


class CustomPasswordResetView(PasswordResetView):
    """
    Сброса пароля - переопределение класса CustomPasswordResetView
    """

    template_name = "users/password_reset.html"
    success_url = reverse_lazy("users:password_reset_done")
    form_class = PasswordResetForm

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return super().form_valid(form)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_link = self.request.build_absolute_uri(
            reverse("users:password_reset_confirm", args=[uid, token])
        )

        subject = "Восстановление и сброс пароля"
        message = render_to_string(
            "users/password_reset_email.html",
            {
                "user": user,
                "reset_link": reset_link,
            },
        )

        send_mail(
            subject,
            strip_tags(message),
            EMAIL_HOST_USER,
            [user.email],
            html_message=message,
        )

        return HttpResponseRedirect(self.get_success_url())


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Подтверждение сброса пароля - переопределение класса PasswordResetConfirmView
    """

    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy("users:password_reset_complete")

    def form_valid(self, form):
        print("Форма валидна")  # Добавьте эту строку
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        print("POST запрос")  # Добавьте эту строку
        return super().post(request, *args, **kwargs)


class ResetPasswordCompleteView(PasswordResetCompleteView):
    """
    Завершение сброса пароля - переопределение класса PasswordResetCompleteView
    """

    template_name = "users/password_reset_complete.html"
    extra_context = {"title": _("Password reset complete")}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_url"] = resolve_url(settings.LOGIN_URL)
        return context
