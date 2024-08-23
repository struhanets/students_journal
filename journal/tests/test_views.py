from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from journal.models import Student, Group, Subject

STUDENT_URL = reverse("journal:students-list")


class PublicStudentTest(TestCase):
    def test_login_required(self):
        res = self.client.get(STUDENT_URL)
        self.assertNotEquals(res.status_code, 200)

    def test_retrieve_to_student_detail(self):
        student = Student.objects.create(
            first_name="first_test",
            last_name="last_test",
        )
        res = self.client.get(reverse("journal:students-detail", args=[student.id]))
        self.assertNotEquals(res.status_code, 200)


class PrivateStudentTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

    def test_retrieve_student(self):
        Student.objects.create(first_name="John", last_name="Doe")
        Student.objects.create(first_name="first_test", last_name="last_test")
        response = self.client.get(STUDENT_URL)
        self.assertEqual(response.status_code, 200)

        students = Student.objects.all()
        self.assertEqual(
            list(response.context["student_list"]),
            list(students),
        )
        self.assertTemplateUsed(response, "students/student_list.html")


class PublicTeacherTest(TestCase):
    def test_login_required(self):
        res = self.client.get(reverse("journal:teachers-list"))
        self.assertNotEquals(res.status_code, 200)

    def test_retrieve_to_teacher_detail(self):
        teacher = get_user_model().objects.create_user(
            username="teacher1",
            password="password_teacher1",
        )
        res = self.client.get(reverse("journal:teachers-detail", args=[teacher.id]))
        self.assertNotEquals(res.status_code, 200)


class PrivateTeacherTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password",
        )

        self.client.force_login(self.user)

    def test_retrieve_teacher(self):
        get_user_model().objects.create_user(
            username="teacher1",
            password="password_teacher1",
        )
        get_user_model().objects.create_user(
            username="teacher2",
            password="password_teacher2",
        )

        response = self.client.get(reverse("journal:teachers-list"))
        self.assertEqual(response.status_code, 200)
        teachers = get_user_model().objects.exclude(username=self.user.username)
        self.assertEqual(
            list(response.context["teacher_list"]),
            list(teachers),
        )
        self.assertTemplateUsed(response, "teachers/teacher_list.html")


class SubjectTest(TestCase):
    def test_retrieve_subjects(self):
        teacher = get_user_model().objects.create_user(
            username="teacher1",
            password="password_teacher1",
        )
        student1 = Student.objects.create(
            first_name="first_test1",
            last_name="last_test1",
        )
        student2 = Student.objects.create(
            first_name="first_test2",
            last_name="last_test2",
        )
        subject = Subject.objects.create(
            title="Test subject",
            teacher=teacher,
        )
        subject.students.set([student1, student2])

        subjects = Subject.objects.all()
        res = self.client.get(reverse("journal:subjects-list"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["subject_list"]),
            list(subjects),
        )
        self.assertTemplateUsed(res, "subjects/subject_list.html")
        response = self.client.get(
            reverse("journal:subjects-detail", args=[subject.id])
        )
        self.assertTemplateUsed(response, "subjects/subject_detail.html")


class PublicGroupTest(TestCase):

    def test_login_required(self):
        res = self.client.get(reverse("journal:groups-list"))
        self.assertNotEquals(res.status_code, 200)


class PrivateGroupTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password",
        )

        self.client.force_login(self.user)

    def test_retrieve_to_student_detail(self):
        student1 = Student.objects.create(
            first_name="first_test1",
            last_name="last_test1",
        )
        student2 = Student.objects.create(
            first_name="first_test2",
            last_name="last_test2",
        )
        group = Group.objects.create(
            title="Test group",
            leader=student1,
        )
        group.students.add(student1, student2)

        res = self.client.get(reverse("journal:groups-list"))
        self.assertEqual(res.status_code, 200)

        groups = Group.objects.all()
        self.assertEqual(
            list(res.context["group_list"]),
            list(groups),
        )
        self.assertTemplateUsed(res, "groups/group_list.html")
        response = self.client.get(reverse("journal:groups-detail", args=[group.id]))
        self.assertTemplateUsed(response, "groups/group_detail.html")
