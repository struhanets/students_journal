from django import forms
from django.contrib.auth.forms import UserCreationForm

from journal.models import Teacher, Group, Student, Subject


class TeacherCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)

    class Meta(UserCreationForm.Meta):
        model = Teacher
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "notes",)


class GroupCreationForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Group
        fields = "__all__"


class StudentCreationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ("first_name", "last_name", "birth_date", "notes",)


class SubjectCreationForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Subject
        fields = "__all__"


class StudentLatsNameSearchForm(forms.Form):
    last_name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "last_name"})
    )


class TeacherLatsNameSearchForm(forms.Form):
    last_name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "last_name"})
    )


class SubjectTitleSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "title"})
    )
