from django.db import models
import uuid
from user_management.models import User


class Division(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    admin = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'


class SubDivision(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'


class ProblemType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type_name = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    time_required = models.DurationField()
    responsible_division = models.ForeignKey(Division, on_delete=models.CASCADE)
    responsible_sub_divifany = models.ForeignKey(SubDivision, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.type_name}'


class SubmittedProblems(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    problem_type = models.ForeignKey(ProblemType, on_delete=models.CASCADE)
    current_responsible_division = models.ForeignKey(Division, on_delete=models.CASCADE)
    current_responsible_sub_divifany = models.ForeignKey(SubDivision, on_delete=models.CASCADE, null=True, blank=True)
    submitted_problem = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    problem_solved_state = models.BooleanField(default=False)
    user_submitted = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.id}'


class TrackProblem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    problem = models.ForeignKey(SubmittedProblems, on_delete=models.CASCADE)
    current_responsible_division = models.ForeignKey(Division, on_delete=models.CASCADE)
    current_responsible_sub_divifany = models.ForeignKey(SubDivision, on_delete=models.CASCADE, null=True, blank=True)
    time_since_submission = models.TimeField()


class ProblemEvidence(models.Model):
    TYPE = (
        (1, "AUDIO"),
        (2, "VIDEO"),
        (3, "IMAGE"),
        (4, "PDF"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    problem = models.ForeignKey(SubmittedProblems, on_delete=models.CASCADE)
    file_type = models.PositiveIntegerField(choices=TYPE, default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    evdc = models.FileField(upload_to="uploads/", null=True, blank=True)
    message = models.TextField(null=True, blank=True)


class Suggestions(models.Model):
    TYPE = (
        (1, "SUGGESTION"),
        (2, "PONGEZI"),

    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.PositiveIntegerField(choices=TYPE, default=1)
    message = models.TextField(null=True, blank=True)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)



class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, null=True, blank=True)
    sub_divifany = models.ForeignKey(SubDivision, on_delete=models.CASCADE, null=True, blank=True)
    notification = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)