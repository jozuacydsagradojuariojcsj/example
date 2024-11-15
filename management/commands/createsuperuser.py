from django.contrib.auth.management.commands.createsuperuser import Command as BaseCommand
import getpass
from api.models import AppUserManager
class Command(BaseCommand):
    help = 'Create a superuser with custom user model'

    def add_arguments(self, parser):
        super().add_arguments(parser)
        # Here you can add custom arguments if needed

    def handle(self, *args, **options):
        username = options.get('username')
        email = options.get('email')

        if not email:
            email = input("Enter email: ")
        if not username:
            username = input("Enter username: ")

        password = None
        while not password:
            password = getpass.getpass("Password: ")
            password2 = getpass.getpass("Password (again): ")
            if password != password2:
                self.stderr.write("Passwords do not match. Please try again.")
                password = None

        try:
            AppUserManager.objects.get(email=email)
        except AppUserManager.DoesNotExist:
            AppUserManager.objects.create_superuser(email=email, username=username, password=password)
            self.stdout.write("Superuser created successfully.")
        else:
            self.stderr.write("A user with that email already exists.")