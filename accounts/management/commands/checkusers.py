from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from mysite.settings import PASSWORD_RESET_TIMEOUT
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Helper command to delete inactive users older than specified time.'
    UserModel = get_user_model()
    current_time = timezone.now()
    time_kwarg = {'seconds': PASSWORD_RESET_TIMEOUT}

    def handle(self, *args, **options):
        deleted_users = 0
        inactive_users = self.UserModel.objects.filter(is_active=False)

        for user in inactive_users:
            if self.current_time >= user.date_joined + timedelta(**self.time_kwarg):
                user.delete()
                deleted_users += 1

        self.stdout.write(f'Deleted {deleted_users} inactive {"users" if deleted_users in (0, 2) else "user"}!')
