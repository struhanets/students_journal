from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from settings import AUTH_USER_MODEL


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ("last_name",)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("journal:students-detail", args=[str(self.id)])


class Teacher(AbstractUser):
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ("username",)

    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("journal:teachers-detail", args=[str(self.id)])


class Group(models.Model):
    title = models.CharField(max_length=255, unique=True)
    leader = models.OneToOneField(
        Student, on_delete=models.PROTECT, related_name="leader"
    )
    students = models.ManyToManyField(Student, related_name="groups")
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ("title",)

    def __str__(self) -> str:
        return f"Group {self.title}"

    def get_absolute_url(self):
        return reverse("journal:groups-detail", args=[str(self.id)])


class Subject(models.Model):
    title = models.CharField(max_length=255, unique=True)
    teacher = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.PROTECT)
    students = models.ManyToManyField(Student, related_name="subjects")

    class Meta:
        ordering = ("title",)

    def __str__(self):
        return f"{self.title} - {self.teacher}"

    def get_absolute_url(self):
        return reverse("journal:subjects-detail", args=[str(self.id)])
