from django.contrib.auth.decorators import login_required
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
    StudentLastNameSearchForm,
    TeacherLastNameSearchForm,
    SubjectTitleSearchForm,
)
from .models import Student, Subject, Teacher, Group


@login_required
def index(request: HttpRequest) -> HttpResponse:
    students = Student.objects.count()
    subjects = Subject.objects.count()
    teachers = Teacher.objects.count()
    groups = Group.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "students": students,
        "subjects": subjects,
        "teachers": teachers,
        "groups": groups,
        "num_visits": num_visits + 1,
    }
    return render(request, "students/index.html", context=context)


class StudentListView(LoginRequiredMixin, generic.ListView):
    model = Student
    template_name = "students/student_list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(StudentListView, self).get_context_data(**kwargs)
        last_name = self.request.GET.get("last_name", "")
        context["search_form"] = StudentLastNameSearchForm(
            initial={"last_name": last_name}
        )

        return context

    def get_queryset(self):
        queryset = Student.objects.all()
        form = StudentLastNameSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(last_name__icontains=form.cleaned_data["last_name"])
        return queryset


class StudentDetailView(LoginRequiredMixin, generic.DetailView):
    model = Student
    template_name = "students/student_detail.html"


class StudentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Student
    form_class = StudentCreationForm
    template_name = "students/student_form.html"
    success_url = reverse_lazy("journal:students-list")


class StudentUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Student
    fields = "__all__"
    template_name = "students/student_form.html"
    success_url = reverse_lazy("journal:students-list")


class StudentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Student
    template_name = "students/student_delete.html"
    success_url = reverse_lazy("journal:students-list")


class TeacherListView(LoginRequiredMixin, generic.ListView):
    model = Teacher
    template_name = "teachers/teacher_list.html"
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(TeacherListView, self).get_context_data(**kwargs)
        last_name = self.request.GET.get("last_name", "")
        context["search_form"] = TeacherLastNameSearchForm(
            initial={"last_name": last_name}
        )
        return context

    def get_queryset(self):
        queryset = Teacher.objects.all()
        form = TeacherLastNameSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(last_name__icontains=form.cleaned_data["last_name"])
        return queryset


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
    success_url = reverse_lazy("journal:groups-list")


class GroupUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Group
    form_class = GroupCreationForm
    template_name = "groups/group_form.html"
    success_url = reverse_lazy("journal:groups-list")


class GroupDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Group
    template_name = "groups/group_delete.html"
    success_url = reverse_lazy("journal:groups-list")


class SubjectListView(LoginRequiredMixin, generic.ListView):
    model = Subject
    template_name = "subjects/subject_list.html"

    def get_context_data(self, **kwargs):
        context = super(SubjectListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["search_form"] = SubjectTitleSearchForm(initial={"title": title})
        return context

    def get_queryset(self):
        queryset = Subject.objects.prefetch_related("students")
        form = SubjectTitleSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(title__icontains=form.cleaned_data["title"])
        return queryset


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
    success_url = reverse_lazy("journal:subjects-list")


class SubjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Subject
    template_name = "subjects/subject_delete.html"
    success_url = reverse_lazy("journal:subjects-list")
