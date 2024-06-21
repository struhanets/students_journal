from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from students.models import Student, Subject, Teacher


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
