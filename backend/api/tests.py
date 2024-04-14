from django.test import TestCase

from api import models
from userauths.models import User, Profile


class ApiModelTest(TestCase):
    """Test cases for Teacher, Category, Course, Variant, VariantItem, QuestionAnswer, QuestionAnswerMessage, Cart, CartOrder, CartOrderItem, Certificate, CompletedLesson, EnrolledCourse, Note, Review, Notification, Coupon, Wishlist and Country models."""

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

        course.save()

        assert course.category == category
        assert course.teacher == teacher
        assert course.title == "Python Programming"
        assert course.price == 49.99
        assert course.language == "English"
        assert course.level == "Beginner"
        assert course.platform_status == "Published"
        assert course.teacher_course_status == "Published"
        assert course.featured is True  # Use 'is' for boolean comparison

    def test_create_variant_with_valid_course_and_title(self):
        """Test creating a Variant instance with valid course and title should be successful."""
        user = User.objects.create(email="test@example.com", username="test")
        teacher = models.Teacher.objects.create(user=user, full_name="Jane Smith")
        course = models.Course.objects.create(
            teacher=teacher,
            title="Python Programming",
            price=50.00,
            language="English",
            level="Beginner",
            platform_status="Published",
            teacher_course_status="Published",
            featured=True,
            course_id=1,
        )

        variant = models.Variant(course=course, title="Test Variant")

        variant.save()

        assert variant.course == course
        assert variant.title == "Test Variant"
        assert variant.variant_id is not None
        assert variant.date is not None

    def test_variant_item_creation_with_required_fields(self):
        """Test VariantItem can be created with required fields"""
        user = User.objects.create(email="test@example.com", username="test")
        teacher = models.Teacher.objects.create(user=user, full_name="Jane Smith")
        course = models.Course.objects.create(
            teacher=teacher,
            title="Python Programming",
            price=50.00,
            language="English",
            level="Beginner",
            platform_status="Published",
            teacher_course_status="Published",
            featured=True,
            course_id=1,
        )
        variant = models.Variant.objects.create(course=course, title="Test Variant")

        variant_item = models.VariantItem.objects.create(
            variant=variant, title="Test Item"
        )

        assert variant_item.variant == variant
        assert variant_item.title == "Test Item"
        assert variant_item.description == None
        assert variant_item.file == None
        assert variant_item.duration == None
        assert variant_item.content_duration == None
        assert variant_item.preview == False
        assert variant_item.variant_item_id != None
        assert variant_item.date != None

    def test_create_question_answer_with_valid_arguments(self):
        """Test creating a new QuestionAnswer with valid parameters should successfully create a new instance."""
        user = User.objects.create(email="test@example.com", username="test")
        teacher = models.Teacher.objects.create(user=user, full_name="Jane Smith")
        course = models.Course.objects.create(
            teacher=teacher,
            title="Python Programming",
            price=50.00,
            language="English",
            level="Beginner",
            platform_status="Published",
            teacher_course_status="Published",
            featured=True,
            course_id=1,
        )

        question_answer = models.QuestionAnswer(course=course, user=user, title=None)

        question_answer.save()

        assert question_answer.course == course
        assert question_answer.user == user
        assert question_answer.title is None

    def test_create_question_answer_message_with_required_fields(self):
        """Test creating a new QuestionAnswerMessage with all required fields should successfully save to the database."""
        user = User.objects.create(email="test@example.com", username="test")
        teacher = models.Teacher.objects.create(user=user, full_name="Jane Smith")
        course = models.Course.objects.create(
            teacher=teacher,
            title="Python Programming",
            price=50.00,
            language="English",
            level="Beginner",
            platform_status="Published",
            teacher_course_status="Published",
            featured=True,
            course_id=1,
        )
        question_answer = models.QuestionAnswer.objects.create(course=course)

        message = models.QuestionAnswerMessage(
            course=course,
            question=question_answer,
            user=user,
            message="This is a test message",
        )

        message.save()

        assert models.QuestionAnswerMessage.objects.count() == 1
        assert message.course == course
        assert message.question == question_answer
        assert message.user == user
        assert message.message == "This is a test message"

    def test_create_cart_with_course_and_user(self):
        """Test creating a new cart with a course and user sets the correct course and user."""
        user = User.objects.create(email="test@example.com", username="test")
        teacher = models.Teacher.objects.create(user=user, full_name="Jane Smith")
        course = models.Course.objects.create(
            teacher=teacher,
            title="Python Programming",
            price=50.00,
            language="English",
            level="Beginner",
            platform_status="Published",
            teacher_course_status="Published",
            featured=True,
            course_id=1,
        )

        cart = models.Cart(
            course=course,
            user=user,
            price=19.99,
            tax_fee=2.00,
            total=21.99,
            country="USA",
        )

        cart.save()

        assert cart.course == course
        assert cart.user == user

    def test_create_cart_order_valid_arguments(self):
        """Test creating a new CartOrder instance with valid arguments should create a new order with the given attributes."""
        cart_order = models.CartOrder()

        cart_order.student = User.objects.create(
            email="test@example.com", username="test"
        )
        cart_order.sub_total = 100.00
        cart_order.tax_fee = 10.00
        cart_order.total = 110.00
        cart_order.initial_total = 120.00
        cart_order.saved = 10.00
        cart_order.payment_status = "Paid"
        cart_order.full_name = "John Doe"
        cart_order.email = "johndoe@example.com"
        cart_order.country = "United States"
        cart_order.stripe_session_id = "session_id_123"
        cart_order.order_id = "ABC123"

        cart_order.save()

        assert cart_order.student == User.objects.get(id=1)
        assert cart_order.sub_total == 100.00
        assert cart_order.tax_fee == 10.00
        assert cart_order.total == 110.00
        assert cart_order.initial_total == 120.00
        assert cart_order.saved == 10.00
        assert cart_order.payment_status == "Paid"
        assert cart_order.full_name == "John Doe"
        assert cart_order.email == "johndoe@example.com"
        assert cart_order.country == "United States"
        assert cart_order.stripe_session_id == "session_id_123"
        assert cart_order.order_id == "ABC123"

        order_items = cart_order.order_items()

        assert list(order_items) == []
        assert str(cart_order) == "ABC123"

    def test_create_new_cart_order_item_with_valid_data(self):
        """Test creating a new CartOrderItem with valid order, course, and teacher should successfully create a new instance."""
        user = User.objects.create(email="test@example.com", username="test")
        order = models.CartOrder.objects.create(
            student=user,
            sub_total=100.00,
            tax_fee=10.00,
            total=110.00,
            initial_total=120.00,
            saved=10.00,
            payment_status="Processing",
            full_name="John Doe",
            email="johndoe@example.com",
            country="USA",
            stripe_session_id="1234567890",
            order_id=1,
        )
        teacher = models.Teacher.objects.create(user=user, full_name="Jane Smith")
        course = models.Course.objects.create(
            teacher=teacher,
            title="Python Programming",
            price=50.00,
            language="English",
            level="Beginner",
            platform_status="Published",
            teacher_course_status="Published",
            featured=True,
            course_id=1,
        )

        order_item = models.CartOrderItem.objects.create(
            order=order,
            course=course,
            teacher=teacher,
            price=50.00,
            tax_fee=5.00,
            total=55.00,
            initial_total=60.00,
            saved=5.00,
            applied_coupon=False,
            order_id=1,
        )

        assert isinstance(order_item, models.CartOrderItem)
        assert order_item.order == order
        assert order_item.course == course
        assert order_item.teacher == teacher
        assert order_item.price == 50.00
        assert order_item.tax_fee == 5.00
        assert order_item.total == 55.00
        assert order_item.initial_total == 60.00
        assert order_item.saved == 5.00
        assert order_item.applied_coupon == False
        assert order_item.order_id == 1
        assert order_item.date is not None

    def test_create_certificate_with_valid_course_and_user(self):
        """Test creating a certificate with a valid course and user should be successful."""
        user = User.objects.create(email="test@example.com", username="test")
        teacher = models.Teacher.objects.create(user=user, full_name="Jane Smith")
        course = models.Course.objects.create(
            teacher=teacher,
            title="Python Programming",
            price=50.00,
            language="English",
            level="Beginner",
            platform_status="Published",
            teacher_course_status="Published",
            featured=True,
            course_id=1,
        )

        certificate = models.Certificate(course=course, user=user)

        certificate.save()

        assert certificate.course == course
        assert certificate.user == user

    def test_valid_completed_lesson_creation(self):
        """Test creating a CompletedLesson object with valid course, user, and variant_item should create a new instance of CompletedLesson."""
        user = User.objects.create(email="test@example.com", username="test")
        teacher = models.Teacher.objects.create(user=user, full_name="Jane Smith")
        course = models.Course.objects.create(
            teacher=teacher,
            title="Python Programming",
            price=50.00,
            language="English",
            level="Beginner",
            platform_status="Published",
            teacher_course_status="Published",
            featured=True,
            course_id=1,
        )
        variant = models.Variant.objects.create(course=course, title="Test Variant")
        variant_item = models.VariantItem.objects.create(
            variant=variant, title="Test Item"
        )

        completed_lesson = models.CompletedLesson(
            course=course, user=user, variant_item=variant_item
        )

        completed_lesson.save()

        assert isinstance(completed_lesson, models.CompletedLesson)
        assert completed_lesson.course == course
        assert completed_lesson.user == user
        assert completed_lesson.variant_item == variant_item

    def test_create_note_with_required_fields(self):
        """Test creating a note with all required fields should save successfully."""
        user = User.objects.create(email="test@example.com", username="testuser")
        teacher = models.Teacher.objects.create(user=user, full_name="Jane Smith")
        course = models.Course.objects.create(
            teacher=teacher,
            title="Python Programming",
            price=50.00,
            language="English",
            level="Beginner",
            platform_status="Published",
            teacher_course_status="Published",
            featured=True,
            course_id=1,
        )

        note = models.Note(user=user, course=course, note="This is a test note")

        note.save()

        assert note.id is not None
        assert note.user == user
        assert note.course == course
        assert note.title is None
        assert note.note == "This is a test note"
        assert note.date is not None

    def test_create_review_with_required_fields(self):
        """Test creating a review with all required fields should save successfully."""
        user = User.objects.create(email="test@example.com", username="testuser")
        teacher = models.Teacher.objects.create(user=user, full_name="Jane Smith")
        course = models.Course.objects.create(
            teacher=teacher,
            title="Python Programming",
            price=50.00,
            language="English",
            level="Beginner",
            platform_status="Published",
            teacher_course_status="Published",
            featured=True,
            course_id=1,
        )

        review = models.Review(
            user=user,
            course=course,
            review="This course is amazing! I learned so much.",
            rating=5,
            reply="Thank you for your feedback!",
            active=True,
        )

        review.save()

        assert review.id is not None
        assert review.user == user
        assert review.course == course
        assert review.review == "This course is amazing! I learned so much."
        assert review.rating == 5
        assert review.reply == "Thank you for your feedback!"
        assert review.active is True

    def test_notification_creation_with_required_fields(self):
        """Test notification object can be created with required fields"""
        user = User.objects.create(email="test@example.com", username="testuser")

        notification = models.Notification(user=user, type="New Order")

        notification.save()

        assert notification.user == user
        assert notification.type == "New Order"
        assert notification.seen == False

    def test_create_coupon_with_valid_data(self):
        """Test creating a new coupon with valid data should save it to the database and return the coupon code."""
        coupon = models.Coupon.objects.create(code="ABC123", discount=10, active=True)

        assert coupon.code == "ABC123"
        assert coupon.discount == 10
        assert coupon.active is True
        assert models.Coupon.objects.filter(code="ABC123").exists()

    def test_valid_wishlist_instance(self):
        """Test creating a Wishlist object with a user and a course should return a valid Wishlist instance."""
        user = User.objects.create(email="test@example.com", username="testuser")
        teacher = models.Teacher.objects.create(user=user, full_name="Jane Smith")
        course = models.Course.objects.create(
            teacher=teacher,
            title="Python Programming",
            price=50.00,
            language="English",
            level="Beginner",
            platform_status="Published",
            teacher_course_status="Published",
            featured=True,
            course_id=1,
        )

        wishlist = models.Wishlist(user=user, course=course)

        wishlist.save()

        assert isinstance(wishlist, models.Wishlist)

    def test_valid_country_object(self):
        """Test creating a new Country object with valid name, tax_rate, and active values should return a valid instance of the Country class."""
        country = models.Country(name="UK", tax_rate=10, active=True)

        assert isinstance(country, models.Country)
