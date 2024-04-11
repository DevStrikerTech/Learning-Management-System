import math
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from moviepy.editor import VideoFileClip
from shortuuid.django_fields import ShortUUIDField

from userauths.models import User, Profile


LANGUAGE = (
    ("English", "English"),
    ("Spanish", "Spanish"),
    ("French", "French"),
)

LEVEL = (
    ("Beginner", "Beginner"),
    ("Intemediate", "Intemediate"),
    ("Advanced", "Advanced"),
)

TEACHER_STATUS = (
    ("Draft", "Draft"),
    ("Disabled", "Disabled"),
    ("Published", "Published"),
)

PLATFORM_STATUS = (
    ("Review", "Review"),
    ("Disabled", "Disabled"),
    ("Rejected", "Rejected"),
    ("Draft", "Draft"),
    ("Published", "Published"),
)

PAYMENT_STATUS = (
    ("Paid", "Paid"),
    ("Processing", "Processing"),
    ("Failed", "Failed"),
)

RATING = (
    (1, "1 Star"),
    (2, "2 Star"),
    (3, "3 Star"),
    (4, "4 Star"),
    (5, "5 Star"),
)

NOTIFICATION_TYPE = (
    ("New Order", "New Order"),
    ("New Review", "New Review"),
    ("New Course Question", "New Course Question"),
    ("Draft", "Draft"),
    ("Course Published", "Course Published"),
    ("Course Enrollment Completed", "Course Enrollment Completed"),
)


class Teacher(models.Model):
    """
    Represents a teacher profile.

    Attributes:
        user (User): The associated user for this teacher.
        image (FileField): An optional image file for the teacher's profile.
        full_name (str): The full name of the teacher.
        bio (str, optional): A short bio or description (can be blank).
        about (str, optional): A detailed description of the teacher (can be blank).
        country (str, optional): The country where the teacher resides (can be blank).
        youtube (URLField, optional): URL to the teacher's YouTube channel (can be blank).
        github (URLField, optional): URL to the teacher's GitHub profile (can be blank).
        twitter (URLField, optional): URL to the teacher's Twitter profile (can be blank).
        linkedin (URLField, optional): URL to the teacher's LinkedIn profile (can be blank).

    Methods:
        __str__(): Returns the full name of the teacher.
        students(): Returns a queryset of students associated with this teacher.
        courses(): Returns a queryset of courses taught by this teacher.
        review(): Returns the count of courses reviewed by students for this teacher.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(
        upload_to="course-file", blank=True, null=True, default="default.jpg"
    )
    full_name = models.CharField(max_length=100)
    bio = models.CharField(max_length=100, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)
    github = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.full_name

    def students(self):
        return CartOrderItem.objects.filter(teacher=self)

    def courses(self):
        return Course.objects.filter(teacher=self)

    def review(self):
        return Course.objects.filter(teacher=self).count()


class Category(models.Model):
    """
    Represents a category for courses.

    Args:
        models (module): The Django models module.

    Attributes:
        title (str): The title of the category.
        image (FileField, optional): An image file associated with the category (can be blank).
        active (bool): Indicates whether the category is active or not.
        slug (SlugField, optional): A unique slug for the category (can be blank).

    Meta:
        verbose_name_plural (str): The plural name for the category model.
        ordering (list): Specifies the default ordering of categories based on their titles.

    Methods:
        __str__(): Returns the title of the category.
        course_count(): Returns the count of courses associated with this category.
        save(*args, **kwargs): Overrides the default save method to set the slug if not provided.

    Example:
        category = Category(title="Programming", active=True)
        category.save()
    """

    title = models.CharField(max_length=100)
    image = models.FileField(
        upload_to="course-file", default="category.jpg", null=True, blank=True
    )
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Category"
        ordering = ["title"]

    def __str__(self):
        return self.title

    def course_count(self):
        return Course.objects.filter(category=self).count()

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.title)

        super(Category, self).save(*args, **kwargs)


class Course(models.Model):
    """
    Represents a course offered within the platform.

    Args:
        models.Model: The base model class.

    Returns:
        Course: An instance of the Course model.

    Attributes:
        category (ForeignKey): The category to which the course belongs.
        teacher (ForeignKey): The teacher associated with the course.
        file (FileField): Optional file attachment related to the course.
        image (FileField): Optional image associated with the course.
        title (CharField): The title of the course (maximum length: 200 characters).
        description (TextField): A detailed description of the course (nullable).
        price (DecimalField): The course price (maximum 12 digits, 2 decimal places).
        language (CharField): The language of the course (choices: English, etc.).
        level (CharField): The difficulty level of the course (choices: Beginner, etc.).
        platform_status (CharField): The status of the course on the platform (choices: Published, etc.).
        teacher_course_status (CharField): The status of the course from the teacher's perspective (choices: Published, etc.).
        featured (BooleanField): Indicates if the course is featured.
        course_id (ShortUUIDField): A unique short UUID for the course.
        slug (SlugField): A URL-friendly slug for the course (unique, nullable).
        date (DateTimeField): The creation date of the course (default: current timestamp).

    Methods:
        __str__(): Returns the title of the course.
        save(*args, **kwargs): Custom save method to generate a slug if not provided.
        students(): Returns a queryset of enrolled students for this course.
        curriculum(): Returns a queryset of variants (curriculum) associated with this course.
        lectures(): Returns a queryset of variant items (lectures) for this course.
        average_rating(): Calculates and returns the average rating for this course.
        rating_count(): Returns the total count of reviews/ratings for this course.
        reviews(): Returns a queryset of reviews for this course.
    """

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    file = models.FileField(upload_to="course-file", blank=True, null=True)
    image = models.FileField(upload_to="course-file", blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    language = models.CharField(choices=LANGUAGE, default="English", max_length=100)
    level = models.CharField(choices=LEVEL, default="Beginner", max_length=100)
    platform_status = models.CharField(
        choices=PLATFORM_STATUS, default="Published", max_length=100
    )
    teacher_course_status = models.CharField(
        choices=TEACHER_STATUS, default="Published", max_length=100
    )
    featured = models.BooleanField(default=False)
    course_id = ShortUUIDField(
        unique=True, length=6, max_length=20, alphabet="1234567890"
    )
    slug = models.SlugField(unique=True, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.title) + str(self.pk)
        super(Course, self).save(*args, **kwargs)

    def students(self):
        return EnrolledCourse.objects.filter(course=self)

    def curriculum(self):
        return Variant.objects.filter(course=self)

    def lectures(self):
        return VariantItem.objects.filter(variant__course=self)

    def average_rating(self):
        average_rating = Review.objects.filter(course=self, active=True).aggregate(
            avg_rating=models.Avg("rating")
        )
        return average_rating["avg_rating"]

    def rating_count(self):
        return Review.objects.filter(course=self, active=True).count()

    def reviews(self):
        return Review.objects.filter(course=self, active=True)


class Variant(models.Model):
    """
    Represents a variant of a course.

    Args:
        models (module): The Django models module.

    Attributes:
        course (ForeignKey): A foreign key to the associated course.
        title (CharField): The title of the variant (maximum length: 1000 characters).
        variant_id (ShortUUIDField): A unique identifier for the variant (length: 6 characters, alphabet: "1234567890").
        date (DateTimeField): The creation date of the variant (default: current time).

    Methods:
        __str__(): Returns the title of the variant.
        variant_items(): Returns a queryset of related variant items.
        items(): Alias for variant_items().
    """

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    variant_id = ShortUUIDField(
        unique=True, length=6, max_length=20, alphabet="1234567890"
    )
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def variant_items(self):
        return VariantItem.objects.filter(variant=self)

    def items(self):
        return VariantItem.objects.filter(variant=self)


class VariantItem(models.Model):
    """
    Represents an item within a course variant.

    Args:
        models (module): The Django models module.

    Attributes:
        variant (ForeignKey): A foreign key to the associated variant.
        title (CharField): The title of the variant item (maximum length: 1000 characters).
        description (TextField): A detailed description of the variant item (nullable).
        file (FileField): An optional file associated with the item (e.g., video, document).
        duration (DurationField): The duration of the item (nullable).
        content_duration (CharField): A human-readable representation of the item's duration (e.g., "5m 30s").
        preview (BooleanField): Indicates whether the item is a preview (default: False).
        variant_item_id (ShortUUIDField): A unique identifier for the variant item (length: 6 characters, alphabet: "1234567890").
        date (DateTimeField): The creation date of the variant item (default: current time).

    Methods:
        __str__(): Returns a formatted string with the variant title and item title.
        save(*args, **kwargs): Overrides the default save method to calculate and store content duration.
    """

    variant = models.ForeignKey(
        Variant, on_delete=models.CASCADE, related_name="variant_items"
    )
    title = models.CharField(max_length=1000)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to="course-file", null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    content_duration = models.CharField(max_length=1000, null=True, blank=True)
    preview = models.BooleanField(default=False)
    variant_item_id = ShortUUIDField(
        unique=True, length=6, max_length=20, alphabet="1234567890"
    )
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.variant.title} - {self.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.file:
            clip = VideoFileClip(self.file.path)
            duration_seconds = clip.duration

            minutes, remainder = divmod(duration_seconds, 60)

            minutes = math.floor(minutes)
            seconds = math.floor(remainder)

            duration_text = f"{minutes}m {seconds}s"
            self.content_duration = duration_text

            super().save(update_fields=["content_duration"])


class QuestionAnswer(models.Model):
    """
    Represents a question-answer pair related to a course.

    Args:
        models (module): The Django models module.

    Attributes:
        course (ForeignKey): A foreign key to the associated course.
        user (ForeignKey): A foreign key to the user who asked the question (nullable).
        title (CharField): The title of the question-answer pair (maximum length: 1000 characters, nullable).
        question_answer_id (ShortUUIDField): A unique identifier for the question-answer pair (length: 6 characters, alphabet: "1234567890").
        date (DateTimeField): The creation date of the question-answer pair (default: current time).

    Methods:
        __str__(): Returns a formatted string with the user's username and course title.
        messages(): Returns a queryset of related question-answer messages.
        profile(): Returns the user's profile associated with the question-answer pair.

    Meta:
        ordering = ['-date']
    """

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=1000, null=True, blank=True)
    question_answer_id = ShortUUIDField(
        unique=True, length=6, max_length=20, alphabet="1234567890"
    )
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"

    class Meta:
        ordering = ["-date"]

    def messages(self):
        return QuestionAnswerMessage.objects.filter(question=self)

    def profile(self):
        return Profile.objects.get(user=self.user)


class QuestionAnswerMessage(models.Model):
    """
    Represents a message within a question-answer pair related to a course.

    Args:
        models (module): The Django models module.

    Attributes:
        course (ForeignKey): A foreign key to the associated course.
        question (ForeignKey): A foreign key to the parent question-answer pair.
        user (ForeignKey): A foreign key to the user who sent the message (nullable).
        message (TextField): The content of the message (nullable).
        question_answer_message_id (ShortUUIDField): A unique identifier for the message (length: 6 characters, alphabet: "1234567890").
        question_answer_id (ShortUUIDField): A reference to the parent question-answer pair.
        date (DateTimeField): The creation date of the message (default: current time).

    Methods:
        __str__(): Returns a formatted string with the user's username and course title.
        profile(): Returns the user's profile associated with the message.

    Meta:
        ordering = ['date']
    """

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionAnswer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    question_answer_message_id = ShortUUIDField(
        unique=True, length=6, max_length=20, alphabet="1234567890"
    )
    question_answer_id = ShortUUIDField(
        unique=True, length=6, max_length=20, alphabet="1234567890"
    )
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"

    class Meta:
        ordering = ["date"]

    def profile(self):
        return Profile.objects.get(user=self.user)


class Cart(models.Model):
    """
    Represents a user's cart for purchasing courses.

    Args:
        models (module): The Django models module.

    Attributes:
        course (ForeignKey): A foreign key to the associated course.
        user (ForeignKey): A foreign key to the user who owns the cart (nullable).
        price (DecimalField): The total price of items in the cart (maximum digits: 12, decimal places: 2).
        tax_fee (DecimalField): The tax fee applied to the cart (maximum digits: 12, decimal places: 2).
        total (DecimalField): The overall total including tax (maximum digits: 12, decimal places: 2).
        country (CharField): The user's country (maximum length: 100 characters, nullable).
        cart_id (ShortUUIDField): A unique identifier for the cart (length: 6 characters, alphabet: "1234567890").
        date (DateTimeField): The creation date of the cart (default: current time).

    Methods:
        __str__(): Returns the title of the associated course.
    """

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    tax_fee = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    total = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    country = models.CharField(max_length=100, null=True, blank=True)
    cart_id = ShortUUIDField(length=6, max_length=20, alphabet="1234567890")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.course.title


class CartOrder(models.Model):
    """
    Represents an order for course items in a user's cart.

    Args:
        models (module): The Django models module.

    Attributes:
        student (ForeignKey): A foreign key to the user who placed the order (nullable).
        teachers (ManyToManyField): Many-to-many relationship with teachers associated with the order (blank).
        sub_total (DecimalField): The subtotal price of items in the order (maximum digits: 12, decimal places: 2).
        tax_fee (DecimalField): The tax fee applied to the order (maximum digits: 12, decimal places: 2).
        total (DecimalField): The overall total including tax (maximum digits: 12, decimal places: 2).
        initial_total (DecimalField): The initial total before any discounts or savings (maximum digits: 12, decimal places: 2).
        saved (DecimalField): The amount saved due to discounts (maximum digits: 12, decimal places: 2).
        payment_status (CharField): The status of payment (choices: "Processing", "Paid", etc., default: "Processing", maximum length: 100).
        full_name (CharField): The full name associated with the order (maximum length: 100, nullable).
        email (CharField): The email address associated with the order (maximum length: 100, nullable).
        country (CharField): The user's country (maximum length: 100, nullable).
        coupons (ManyToManyField): Many-to-many relationship with coupons applied to the order (blank).
        stripe_session_id (CharField): The Stripe session ID for payment (maximum length: 1000, nullable).
        order_id (ShortUUIDField): A unique identifier for the order (length: 6 characters, alphabet: "1234567890").
        date (DateTimeField): The creation date of the order (default: current time).

    Methods:
        order_items(): Returns a queryset of related order items.
        __str__(): Returns the order ID as a formatted string.

    Meta:
        ordering = ['-date']
    """

    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    teachers = models.ManyToManyField(Teacher, blank=True)
    sub_total = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    tax_fee = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    total = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    initial_total = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    saved = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    payment_status = models.CharField(
        choices=PAYMENT_STATUS, default="Processing", max_length=100
    )
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    coupons = models.ManyToManyField("api.Coupon", blank=True)
    stripe_session_id = models.CharField(max_length=1000, null=True, blank=True)
    order_id = ShortUUIDField(
        unique=True, length=6, max_length=20, alphabet="1234567890"
    )
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-date"]

    def order_items(self):
        return CartOrderItem.objects.filter(order=self)

    def __str__(self):
        return self.order_id


class CartOrderItem(models.Model):
    """
    Represents an item within a cart order for purchasing courses.

    Args:
        models (module): The Django models module.

    Attributes:
        order (ForeignKey): A foreign key to the associated cart order.
        course (ForeignKey): A foreign key to the course associated with the item.
        teacher (ForeignKey): A foreign key to the teacher associated with the item.
        price (DecimalField): The individual price of the item (maximum digits: 12, decimal places: 2).
        tax_fee (DecimalField): The tax fee applied to the item (maximum digits: 12, decimal places: 2).
        total (DecimalField): The total cost of the item including tax (maximum digits: 12, decimal places: 2).
        initial_total (DecimalField): The initial total before any discounts or savings (maximum digits: 12, decimal places: 2).
        saved (DecimalField): The amount saved due to discounts (maximum digits: 12, decimal places: 2).
        coupons (ManyToManyField): Many-to-many relationship with coupons applied to the item (blank).
        applied_coupon (BooleanField): Indicates whether a coupon was applied to the item (default: False).
        order_id (ShortUUIDField): A unique identifier for the item (length: 6 characters, alphabet: "1234567890").
        date (DateTimeField): The creation date of the item (default: current time).

    Methods:
        order_id(): Returns a formatted string with the item's order ID.
        payment_status(): Returns the payment status associated with the item.
        __str__(): Returns the item's order ID as a formatted string.

    Meta:
        ordering = ['-date']
    """

    order = models.ForeignKey(
        CartOrder, on_delete=models.CASCADE, related_name="orderitem"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="order_item"
    )
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    tax_fee = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    total = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    initial_total = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    saved = models.DecimalField(max_digits=12, default=0.00, decimal_places=2)
    coupons = models.ManyToManyField("api.Coupon", blank=True)
    applied_coupon = models.BooleanField(default=False)
    order_id = ShortUUIDField(
        unique=True, length=6, max_length=20, alphabet="1234567890"
    )
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-date"]

    def order_id(self):
        return f"Order ID #{self.order.order_id}"

    def payment_status(self):
        return f"{self.order.payment_status}"

    def __str__(self):
        return self.order_id


class Certificate(models.Model):
    """
    Represents a certificate awarded to a user upon course completion.

    Args:
        models (module): The Django models module.

    Attributes:
        course (ForeignKey): A foreign key to the associated course.
        user (ForeignKey): A foreign key to the user who received the certificate (nullable).
        certificate_id (ShortUUIDField): A unique identifier for the certificate (length: 6 characters, alphabet: "1234567890").
        date (DateTimeField): The creation date of the certificate (default: current time).

    Methods:
        __str__(): Returns the title of the associated course.
    """

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    certificate_id = ShortUUIDField(
        unique=True, length=6, max_length=20, alphabet="1234567890"
    )
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.course.title


class CompletedLesson(models.Model):
    """
    Represents a completed lesson within a course.

    Args:
        models (module): The Django models module.

    Attributes:
        course (ForeignKey): A foreign key to the associated course.
        user (ForeignKey): A foreign key to the user who completed the lesson (nullable).
        variant_item (ForeignKey): A foreign key to the specific lesson variant item.
        date (DateTimeField): The completion date of the lesson (default: current time).

    Methods:
        __str__(): Returns the title of the associated course.
    """

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    variant_item = models.ForeignKey(VariantItem, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.course.title


class EnrolledCourse(models.Model):
    """
    Represents a user's enrollment in a course.

    Args:
        models (module): The Django models module.

    Attributes:
        course (ForeignKey): A foreign key to the associated course.
        user (ForeignKey): A foreign key to the user who enrolled in the course (nullable).
        teacher (ForeignKey): A foreign key to the teacher associated with the course (nullable).
        order_item (ForeignKey): A foreign key to the cart order item related to the enrollment.
        enrollment_id (ShortUUIDField): A unique identifier for the enrollment (length: 6 characters, alphabet: "1234567890").
        date (DateTimeField): The enrollment date (default: current time).

    Methods:
        __str__(): Returns the title of the associated course.
        lectures(): Returns a queryset of related lesson variant items.
        completed_lesson(): Returns a queryset of completed lessons by the user.
        curriculum(): Returns a queryset of course variants.
        note(): Returns a queryset of notes related to the course and user.
        question_answer(): Returns a queryset of question-answer pairs related to the course.
        review(): Returns the first review associated with the course and user.
    """

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, blank=True
    )
    order_item = models.ForeignKey(CartOrderItem, on_delete=models.CASCADE)
    enrollment_id = ShortUUIDField(
        unique=True, length=6, max_length=20, alphabet="1234567890"
    )
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.course.title

    def lectures(self):
        return VariantItem.objects.filter(variant__course=self.course)

    def completed_lesson(self):
        return CompletedLesson.objects.filter(course=self.course, user=self.user)

    def curriculum(self):
        return Variant.objects.filter(course=self.course)

    def note(self):
        return Note.objects.filter(course=self.course, user=self.user)

    def question_answer(self):
        return QuestionAnswer.objects.filter(course=self.course)

    def review(self):
        return Review.objects.filter(course=self.course, user=self.user).first()


class Note(models.Model):
    """
    Represents a user's note related to a course.

    Args:
        models (module): The Django models module.

    Attributes:
        user (ForeignKey): A foreign key to the user who created the note (nullable).
        course (ForeignKey): A foreign key to the associated course.
        title (CharField): The title of the note (maximum length: 1000 characters, nullable).
        note (TextField): The content of the note.
        note_id (ShortUUIDField): A unique identifier for the note (length: 6 characters, alphabet: "1234567890").
        date (DateTimeField): The creation date of the note (default: current time).

    Methods:
        __str__(): Returns the title of the note.
    """

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000, null=True, blank=True)
    note = models.TextField()
    note_id = ShortUUIDField(
        unique=True, length=6, max_length=20, alphabet="1234567890"
    )
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Review(models.Model):
    """
    Represents a user's review for a course.

    Args:
        models (module): The Django models module.

    Attributes:
        user (ForeignKey): A foreign key to the user who submitted the review (nullable).
        course (ForeignKey): A foreign key to the associated course.
        review (TextField): The content of the review.
        rating (IntegerField): The numeric rating given by the user (choices: 1 to 5, default: None).
        reply (CharField): An optional reply from the course provider (maximum length: 1000 characters, nullable).
        active (BooleanField): Indicates whether the review is currently active (default: False).
        date (DateTimeField): The creation date of the review (default: current time).

    Methods:
        __str__(): Returns the title of the associated course.
        profile(): Returns the user's profile associated with the review.
    """

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    reply = models.CharField(null=True, blank=True, max_length=1000)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.course.title

    def profile(self):
        return Profile.objects.get(user=self.user)


class Notification(models.Model):
    """
    Represents a notification related to user activity.

    Args:
        models (module): The Django models module.

    Attributes:
        user (ForeignKey): A foreign key to the user associated with the notification (nullable).
        teacher (ForeignKey): A foreign key to the teacher associated with the notification (nullable).
        order (ForeignKey): A foreign key to the cart order related to the notification (nullable).
        order_item (ForeignKey): A foreign key to the cart order item related to the notification (nullable).
        review (ForeignKey): A foreign key to the review related to the notification (nullable).
        type (CharField): The type of notification (choices: "Order", "Review", etc., maximum length: 100).
        seen (BooleanField): Indicates whether the notification has been seen (default: False).
        date (DateTimeField): The creation date of the notification (default: current time).

    Methods:
        __str__(): Returns the type of the notification.
    """

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, blank=True
    )
    order = models.ForeignKey(
        CartOrder, on_delete=models.SET_NULL, null=True, blank=True
    )
    order_item = models.ForeignKey(
        CartOrderItem, on_delete=models.SET_NULL, null=True, blank=True
    )
    review = models.ForeignKey(Review, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=100, choices=NOTIFICATION_TYPE)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.type


class Coupon(models.Model):
    """
    Represents a coupon for discounts.

    Args:
        models (module): The Django models module.

    Attributes:
        teacher (ForeignKey): A foreign key to the teacher associated with the coupon (nullable).
        used_by (ManyToManyField): Many-to-many relationship with users who have used the coupon (blank).
        code (CharField): The coupon code (maximum length: 50 characters).
        discount (IntegerField): The discount percentage (default: 1).
        active (BooleanField): Indicates whether the coupon is currently active (default: False).
        date (DateTimeField): The creation date of the coupon (default: current time).

    Methods:
        __str__(): Returns the coupon code.
    """

    teacher = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, blank=True
    )
    used_by = models.ManyToManyField(User, blank=True)
    code = models.CharField(max_length=50)
    discount = models.IntegerField(default=1)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.code


class Wishlist(models.Model):
    """
    Represents a user's wishlist for courses.

    Args:
        models (module): The Django models module.

    Attributes:
        user (ForeignKey): A foreign key to the user who added the course to the wishlist (nullable).
        course (ForeignKey): A foreign key to the associated course.

    Methods:
        __str__(): Returns the title of the associated course.
    """

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.course.title)


class Country(models.Model):
    """
    Represents a country with associated tax information.

    Args:
        models (module): The Django models module.

    Attributes:
        name (CharField): The name of the country (maximum length: 100 characters).
        tax_rate (IntegerField): The tax rate applicable to the country (default: 5).
        active (BooleanField): Indicates whether the country is currently active (default: True).

    Methods:
        __str__(): Returns the name of the country.

    """

    name = models.CharField(max_length=100)
    tax_rate = models.IntegerField(default=5)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
