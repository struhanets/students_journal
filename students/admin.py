from django.contrib import admin
from students.models import Student, Teacher, Group, Subject

admin.site.register(Student)
admin.site.register(Teacher)

admin.site.register(Group)
admin.site.register(Subject)
