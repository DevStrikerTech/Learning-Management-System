from django.test import TestCase

from api import models
from userauths.models import User, Profile


class ApiModelTest(TestCase):
    """Test cases for Teacher, Category, Course models."""

    def test_create_teacher_with_required_fields(self):
        """Test creating a new Teacher instance with all required fields should be successful."""
        user = User.objects.create_user(
            email="teacher@example.com", username="teacher123", password="password123"
        )
        teacher = models.Teacher(user=user, full_name="John Doe")
        teacher.save()

        assert teacher.full_name == "John Doe"
        assert teacher.bio == None
        assert teacher.about == None
        assert teacher.country == None
        assert teacher.youtube == None
        assert teacher.github == None
        assert teacher.twitter == None
        assert teacher.linkedin == None

    def test_create_category_with_title_and_save(self):
        """Test creating a new category with a title and saving it should result in a new category object being created and saved to the database with a unique slug."""
        category = models.Category(title="Programming")
        category.save()

        assert models.Category.objects.count() == 1
        assert category.slug is not None

    def test_create_course_with_required_attributes(self):
        """Test course can be created with required attributes"""
        user = User.objects.create(email="test@example.com", username="test")

        category = models.Category.objects.create(title="Programming")
        teacher = models.Teacher.objects.create(full_name="John Doe", user=user)

        course = models.Course(
            category=category,
            teacher=teacher,
            title="Python Programming",
            price=49.99,
            language="English",
            level="Beginner",
            platform_status="Published",
            teacher_course_status="Published",
            featured=True,
        )

        assert course.category == category
        assert course.teacher == teacher
        assert course.title == "Python Programming"
        assert course.price == 49.99
        assert course.language == "English"
        assert course.level == "Beginner"
        assert course.platform_status == "Published"
        assert course.teacher_course_status == "Published"
        assert course.featured is True  # Use 'is' for boolean comparison

        course.save()
