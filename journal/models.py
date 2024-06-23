from django.contrib.auth.models import AbstractUser
from django.db import models
from settings import AUTH_USER_MODEL


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, unique=True)
    birth_date = models.DateField()
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ("last_name",)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} was born in {self.birth_date}"


class Teacher(AbstractUser):
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ("username",)

    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name}"


class Group(models.Model):
    title = models.CharField(max_length=255, unique=True)
    leader = models.ForeignKey(Student, on_delete=models.PROTECT)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ("title",)

    def __str__(self) -> str:
        return f"Group {self.title}, leader {self.leader}"


class Subject(models.Model):
    title = models.CharField(max_length=255, unique=True)
    teacher = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, related_name="subjects")

    class Meta:
        ordering = ("title",)

    def __str__(self):
        return f"{self.title} - {self.teacher}"