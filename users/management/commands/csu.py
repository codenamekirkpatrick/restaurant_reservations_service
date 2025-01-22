from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """
    Создание суперпользователя.
    """

    def handle(self, *args, **options):
        user = User.objects.create(
            email="admin@admin.com",
            first_name="admin",
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

        user.set_password("admin")
        user.save()

        self.stdout.write(self.style.SUCCESS(f"Суперпользователь создан: {user.email}"))
