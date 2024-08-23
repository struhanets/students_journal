from django.contrib.auth import get_user_model
from django.test import TestCase

from journal.models import Student, Group, Subject


class TestModels(TestCase):
    def test_student_str(self):
        student = Student.objects.create(
            first_name="first_test",
            last_name="last_test",
        )
        self.assertEqual(str(student), student.first_name + " " + student.last_name)

    def test_teacher_str(self):
        teacher = get_user_model().objects.create_user(
            username="test_user", password="test_<PASSWORD>"
        )
        self.assertEqual(
            str(teacher),
            teacher.username + ": " + teacher.first_name + " " + teacher.last_name,
        )

    def test_create_teacher_with_notes(self):
        username = "test_user"
        password = "test_<PASSWORD>"
        notes = "test_notes"
        teacher = get_user_model().objects.create_user(
            username=username,
            password=password,
            notes=notes,
        )

        self.assertEqual(teacher.username, username)
        self.assertEqual(teacher.check_password(password), True)
        self.assertEqual(teacher.notes, notes)

    def test_group_str(self):
        student1 = Student.objects.create(
            first_name="first_test1",
            last_name="last_test1",
        )

        group = Group.objects.create(
            title="test_group",
            leader=student1,
        )

        self.assertEqual(str(group), "Group " + group.title)

    def test_subject_str(self):
        teacher = get_user_model().objects.create_user(
            username="test_user",
            password="test_<PASSWORD>",
        )

        subject = Subject.objects.create(
            title="test_subject",
            teacher=teacher,
        )

        self.assertEqual(str(subject), subject.title + " - " + str(subject.teacher))
