from django.urls import path

from journal import views
from journal.views import (
    StudentListView,
    TeacherListView,
    GroupListView,
    SubjectListView,
    StudentDetailView,
    TeacherDetailView,
)


urlpatterns = [
    path("", views.index, name="index"),
    path("students/", StudentListView.as_view(), name="students-list"),
    path("students/<int:pk>/", StudentDetailView.as_view(), name="students-detail"),
    path("teachers/", TeacherListView.as_view(), name="teachers-list"),
    path("teachers/<int:pk>/", TeacherDetailView.as_view(), name="teachers-detail"),
    path("groups/", GroupListView.as_view(), name="groups-list"),
    path("subjects/", SubjectListView.as_view(), name="subjects-list"),


]

app_name = "journal"
