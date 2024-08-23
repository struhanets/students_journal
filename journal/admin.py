from django.contrib import admin

from journal.models import Student, Teacher, Subject, Group

admin.site.register(Student)
admin.site.register(Teacher)

admin.site.register(Subject)
admin.site.register(Group)
