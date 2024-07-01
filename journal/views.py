from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import (
    TeacherCreationForm,
    GroupCreationForm,
    SubjectCreationForm,
    StudentCreationForm,
)
from .models import Student, Subject, Teacher, Group


@login_required
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


class StudentListView(LoginRequiredMixin, generic.ListView):
    model = Student
    template_name = "students/student_list.html"
    paginate_by = 5


class StudentDetailView(LoginRequiredMixin, generic.DetailView):
    model = Student
    template_name = "students/student_detail.html"


class StudentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Student
    form_class = StudentCreationForm
    template_name = "students/students_form.html"
    success_url = reverse_lazy("students:student_list")


class StudentUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Student
    fields = "__all__"
    template_name = "students/students_form.html"
    success_url = reverse_lazy("journal:students-list")


class TeacherListView(LoginRequiredMixin, generic.ListView):
    model = Teacher
    template_name = "teachers/teacher_list.html"
    paginate_by = 2


class TeacherDetailView(LoginRequiredMixin, generic.DetailView):
    model = Teacher
    template_name = "teachers/teacher_detail.html"


class TeacherCreateView(LoginRequiredMixin, generic.CreateView):
    model = Teacher
    form_class = TeacherCreationForm
    template_name = "teachers/teacher_form.html"


class TeacherUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Teacher
    fields = ("username", "first_name", "last_name", "notes")
    template_name = "teachers/teacher_form.html"
    success_url = reverse_lazy("journal:teachers-list")


class GroupListView(LoginRequiredMixin, generic.ListView):
    model = Group
    template_name = "groups/group_list.html"
    queryset = Group.objects.select_related("leader")


class GroupDetailView(LoginRequiredMixin, generic.DetailView):
    model = Group
    template_name = "groups/group_detail.html"


class GroupCreateView(LoginRequiredMixin, generic.CreateView):
    model = Group
    form_class = GroupCreationForm
    template_name = "groups/group_form.html"


class GroupUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Group
    form_class = GroupCreationForm
    template_name = "groups/group_form.html"
    success_url = reverse_lazy("journal:group_list")


class SubjectListView(LoginRequiredMixin, generic.ListView):
    model = Subject
    template_name = "subjects/subject_list.html"
    queryset = Subject.objects.prefetch_related("students")


class SubjectDetailView(generic.DetailView):
    model = Subject
    template_name = "subjects/subject_detail.html"


class SubjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Subject
    form_class = SubjectCreationForm
    template_name = "subjects/subject_form.html"


class SubjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Subject
    form_class = SubjectCreationForm
    template_name = "subjects/subject_form.html"
    success_url = reverse_lazy("journal:subject_list")
