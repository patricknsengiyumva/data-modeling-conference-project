import datetime
from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# https://djangoproject.com


class UserAccountManager(BaseUserManager):
    def create_user(self, email, username, name, password=None):
        if not email:
            raise ValueError("an email address is required for users")
        if not name:
            raise ValueError("You must provide your name")
        user = self.model(
            email=self.normalize_email(email),
            name=name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            name=name
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class EventPlanner(AbstractBaseUser):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, verbose_name='email', unique=True)
    password = models.CharField(max_length=255)
    # required fields
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True, null=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'name', 'password']

    objects = UserAccountManager()

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Conference(models.Model):
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    event_planner = models.ForeignKey(EventPlanner, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.title}"

    def get_conference_date(self):
        return self.date.strftime("%Y-%m-%d %I:%M %p")


class Speaker(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    contact_information = models.CharField(max_length=200)
    profile_picture = models.ImageField(upload_to='speakers/')
    areas_of_expertise = models.TextField()
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Session(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Attendee(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Reminder(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    reminder_date = models.DateTimeField()


class Attendance(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(auto_now_add=True)
