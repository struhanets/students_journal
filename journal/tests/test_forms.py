from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from journal.forms import TeacherCreationForm, StudentCreationForm
from journal.models import Student

FORM_DATA = {
    "username": "test",
    "first_name": "first_test",
    "last_name": "last_test",
    "notes": "notes_test",
    "password1": "user_test_<PASSWORD>",
    "password2": "user_test_<PASSWORD>",
}

STUDENT_CREATION_FORM_DATA = {
    "first_name": "first_name_student",
    "last_name": "last_name_student",
    "birth_date": "",
    "notes": "notes_student",
}


class TeacherCreationFormTest(TestCase):
    def test_teacher_creation_form_with_customs_fields(self):
        form = TeacherCreationForm(data=FORM_DATA)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, FORM_DATA)


class PrivateTeacherCreationFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user123",
            password="test_user123*",
        )

        self.client.force_login(self.user)

    def test_teacher_creation_form(self):
        response = self.client.post(reverse("journal:teachers-create"), data=FORM_DATA)
        self.assertEqual(response.status_code, 302)

        new_teacher = get_user_model().objects.get(username=FORM_DATA["username"])
        self.assertEqual(new_teacher.username, FORM_DATA["username"])
        self.assertEqual(new_teacher.first_name, FORM_DATA["first_name"])
        self.assertEqual(new_teacher.last_name, FORM_DATA["last_name"])
        self.assertEqual(new_teacher.notes, FORM_DATA["notes"])


class TeacherSearchFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Volodymyr",
            password="Volodymyr<PASSWORD>",
        )

        self.client.force_login(self.user)

    def test_teacher_search_by_last_name(self):
        response = self.client.get(reverse("journal:teachers-list"), data=FORM_DATA)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, FORM_DATA["last_name"])


class StudentCreateFormTest(TestCase):
    def test_student_create_form_with_custom_fields(self):
        form = StudentCreationForm(data=STUDENT_CREATION_FORM_DATA)

        self.assertTrue(form.is_valid())
        cleaned_data = form.cleaned_data
        if STUDENT_CREATION_FORM_DATA["birth_date"] == "":
            self.assertIsNone(cleaned_data.get("birth_date"))
        else:
            self.assertEqual(
                cleaned_data.get("birth_date"), STUDENT_CREATION_FORM_DATA["birth_date"]
            )


class PrivateStudentCreateFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Volodymyr",
            password="Volodymyr<PASSWORD>",
        )
        self.client.force_login(self.user)

    def test_student_create_form(self):
        response = self.client.post(
            reverse("journal:students-create"), data=STUDENT_CREATION_FORM_DATA
        )
        self.assertEqual(response.status_code, 302)

        new_student = Student.objects.get(
            last_name=STUDENT_CREATION_FORM_DATA["last_name"]
        )
        self.assertEqual(
            new_student.first_name, STUDENT_CREATION_FORM_DATA["first_name"]
        )
        self.assertEqual(new_student.last_name, STUDENT_CREATION_FORM_DATA["last_name"])
        self.assertEqual(new_student.notes, STUDENT_CREATION_FORM_DATA["notes"])

        if STUDENT_CREATION_FORM_DATA["birth_date"]:
            self.assertEqual(
                new_student.birth_date.strftime("%Y-%m-%d"),
                STUDENT_CREATION_FORM_DATA["birth_date"],
            )
        else:
            self.assertIsNone(new_student.birth_date)


class StudentSearchFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user1", password="<PASSWORD1>"
        )

        self.client.force_login(self.user)

    def test_student_search_form_by_last_name(self):
        response = self.client.get(
            reverse("journal:students-list"), data=STUDENT_CREATION_FORM_DATA
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, STUDENT_CREATION_FORM_DATA["last_name"])


class SubjectSearchFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user1", password="<PASSWORD1>"
        )

        self.client.force_login(self.user)

    def test_subject_search_form_by_title(self):
        new_subject = {
            "title": "Test Subject",
            "teacher": FORM_DATA,
            "students": STUDENT_CREATION_FORM_DATA,
        }

        response = self.client.get(reverse("journal:subjects-list"), data=new_subject)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, new_subject["title"])
