from django.db import models
from django.contrib.auth.models import User
class Person(models.Model):
    class UserRole(models.TextChoices):
        manager = 'ma', 'Manager'
        worker = 'wo', 'Worker'

    class StaffType(models.TextChoices):
        frontend = 'fr', 'Frontend'
        backend = 'ba', 'Backend'
        ux = 'ux', 'UX'
        qa = 'qa', 'QA'
        SystemsAnalysis = 'sa', 'Systems Analysis'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nameStaff = models.CharField(max_length=3, choices=StaffType.choices)
    role = models.CharField(max_length=2, choices=UserRole.choices, default=UserRole.worker)
    def __str__(self):
        return f'{self.user.username} ({self.role})'


class Task(models.Model):
    class TaskStatus(models.TextChoices):
        new = 'nw', 'New'
        In_process = 'ip', 'In_Process'
        completed = 'co', 'Completed'

    nameStaff = models.CharField(max_length=2, choices=Person.StaffType.choices)
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    end_date = models.DateField()
    executor = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(
        max_length=2,
        choices=TaskStatus.choices,
        default=TaskStatus.new
    )

    def __str__(self):
        return self.name