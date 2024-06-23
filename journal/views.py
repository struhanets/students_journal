from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic
from django.views.generic import ListView, DetailView

from .models import Student, Subject, Teacher, Group


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    students = Student.objects.all()
    subjects = Subject.objects.all()
    teachers = Teacher.objects.all()

    num_visits = request.session.get('num_visits', 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        'students': students,
        'subjects': subjects,
        'teachers': teachers,
        'num_visits': num_visits + 1,
    }
    return render(request, "students/index.html", context=context)


class StudentListView(generic.ListView):
    model = Student
    template_name = "students/student_list.html"


class StudentDetailView(generic.DetailView):
    model = Student
    template_name = "students/student_detail.html"


class TeacherListView(generic.ListView):
    model = Teacher
    template_name = "teachers/teacher_list.html"


class TeacherDetailView(generic.DetailView):
    model = Teacher
    template_name = "teachers/teacher_detail.html"

class GroupListView(generic.ListView):
    model = Group
    template_name = "groups/group_list.html"
    queryset = Group.objects.select_related("student")


class SubjectListView(generic.ListView):
    model = Subject
    template_name = "subjects/subject_list.html"
    queryset = Subject.objects.prefetch_related("students")



