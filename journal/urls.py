from django.urls import path

from journal import views
from journal.views import (

    TeacherListView,
    TeacherDetailView,
    TeacherCreateView,
    TeacherUpdateView,
    StudentListView,
    StudentDetailView,
    StudentCreateView,
    StudentUpdateView,
    GroupListView,
    GroupDetailView,
    GroupCreateView,
    GroupUpdateView,
    SubjectListView,
    SubjectDetailView,
    SubjectCreateView,
    SubjectUpdateView,
)


urlpatterns = [
    path("", views.index, name="index"),
    path("students/", StudentListView.as_view(), name="students-list"),
    path("students/<int:pk>/", StudentDetailView.as_view(), name="students-detail"),
    path("students/create/", StudentCreateView.as_view(), name="students-create"),
    path("students/<int:pk>/update/", StudentUpdateView.as_view(), name="students-update"),

    path("teachers/", TeacherListView.as_view(), name="teachers-list"),
    path("teachers/<int:pk>/", TeacherDetailView.as_view(), name="teachers-detail"),
    path("teachers/create/", TeacherCreateView.as_view(), name="teachers-create"),
    path("teachers/<int:pk>/update/", TeacherUpdateView.as_view(), name="teachers-update"),

    path("groups/", GroupListView.as_view(), name="groups-list"),
    path("groups/<int:pk>/", GroupDetailView.as_view(), name="groups-detail"),
    path("groups/create/", GroupCreateView.as_view(), name="groups-create"),
    path("groups/<int:pk>/update/", GroupUpdateView.as_view(), name="groups-update"),

    path("subjects/", SubjectListView.as_view(), name="subjects-list"),
    path("subjects/<int:pk>/", SubjectDetailView.as_view(), name="subjects-detail"),
    path("subjects/create/", SubjectCreateView.as_view(), name="subjects-create"),
    path("subjects/<int:pk>/update/", SubjectUpdateView.as_view(), name="subjects-update"),

]

app_name = "journal"
