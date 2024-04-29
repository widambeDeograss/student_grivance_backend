from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    RESP_PERSONAL = 1
    STUDENT = 2
    DIVISION = 3
    SUB_DIVISION = 4
    DTSO_SPORTS = 5
    DTSO_GENDER = 6
    DEPT_COMPUTER = 7
    DEPT_MECH = 8
    DEPT_ELECT = 9
    DEPT_ETE = 10
    IPT = 11
    ADM = 12

    SYSTEM_ROLES = (
        (RESP_PERSONAL, "Responsible Personal"),
        (STUDENT, "Student with grivance"),
        (DIVISION, "Division Admin"),
        (SUB_DIVISION, "Sub_division admin"),
    )
    GENDER = (
        ("M", "MALE"),
        ("F", "FEMALE")
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    gender = models.CharField(choices=GENDER, null=True, blank=True, max_length=6)
    profile = models.ImageField(upload_to="uploads/", null=True, blank=True)
    role = models.PositiveIntegerField(choices=SYSTEM_ROLES, default=STUDENT)
    created_at = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=12)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'
