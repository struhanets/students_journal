from django.contrib.auth.models import AbstractUser
from django.db import models

class Student(AbstractUser):
    class Mets:
        ordering = ("username",)
        

class 





  