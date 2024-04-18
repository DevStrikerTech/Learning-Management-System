from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api import models as api_models
from userauths.models import Profile, User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom TokenObtainPairSerializer with additional user information.

    Args:
        TokenObtainPairSerializer (type): The base TokenObtainPairSerializer class.

    Returns:
        type: A token containing user's full name, email, and username.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["full_name"] = user.full_name
        token["email"] = user.email
        token["username"] = user.username

        return token


class RegisterSerializer(serializers.ModelSerializer):
    """
    Custom serializer for user registration.

    Args:
        serializers (type): The base serializers class.

    Raises:
        serializers.ValidationError: Raised if password fields do not match.

    Returns:
        type: A new user instance.
    """

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password_matched = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["full_name", "email", "password", "password_matched"]

    def validate(self, attr):
        if attr["password"] != attr["password_matched"]:
            raise serializers.ValidationError(
                {"password": "Password fields do not match."}
            )

        return attr

    def create(self, validated_data):
        user = User.objects.create(
            full_name=validated_data["full_name"],
            email=validated_data["email"],
        )

        email_username, _ = user.email.split("@")
        user.username = email_username
        user.set_password(validated_data["password"])
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializes User model data.

    Args:
        serializers (type): The serializer class for User model.
    """

    class Meta:
        model = User
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializes Profile model data.

    Args:
        serializers (type): The serializer class for the Profile model.
    """

    class Meta:
        model = Profile
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializes the Category model.

    Args:
        serializers (type): The serializer class for the Category model.
    """

    class Meta:
        fields = ["id", "title", "image", "slug", "course_count"]
        model = api_models.Category


class TeacherSerializer(serializers.ModelSerializer):
    """
    Serializes the Teacher model.

    Args:
        serializers (type): The serializer class for the Teacher model.
    """

    class Meta:
        fields = [
            "user",
            "image",
            "full_name",
            "bio",
            "about",
            "country",
            "youtube",
            "github",
            "twitter",
            "linkedin",
            "courses",
            "review",
            "students",
        ]
        model = api_models.Teacher


class VariantItemSerializer(serializers.ModelSerializer):
    """
    Serializes the VariantItem model.

    Args:
        serializers (type): The serializer class for the VariantItem model.
    """

    class Meta:
        fields = "__all__"
        model = api_models.VariantItem

    def __init__(self, *args, **kwargs):
        super(VariantItemSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class VariantSerializer(serializers.ModelSerializer):
    """
    Serializes the Variant model.

    Args:
        serializers (type): The serializer class for the Variant model.
    """

    variant_items = VariantItemSerializer(many=True)
    items = VariantItemSerializer(many=True)

    class Meta:
        fields = "__all__"
        model = api_models.Variant

    def __init__(self, *args, **kwargs):
        super(VariantSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class QuestionAnswerMessageSerializer(serializers.ModelSerializer):
    """
    Serializes the QuestionAnswerMessage model.

    Args:
        serializers (type): The serializer class for the QuestionAnswerMessage model.
    """

    profile = ProfileSerializer(many=False)

    class Meta:
        fields = "__all__"
        model = api_models.QuestionAnswerMessage


class QuestionAnswerSerializer(serializers.ModelSerializer):
    """
    Serializes the QuestionAnswer model.

    Args:
        serializers (type): The serializer class for the QuestionAnswer model.
    """

    messages = QuestionAnswerMessageSerializer(many=True)
    profile = ProfileSerializer(many=False)

    class Meta:
        fields = "__all__"
        model = api_models.QuestionAnswer


class CartSerializer(serializers.ModelSerializer):
    """
    Serializes the Cart model.

    Args:
        serializers (type): The serializer class for the Cart model.
    """

    class Meta:
        fields = "__all__"
        model = api_models.Cart

    def __init__(self, *args, **kwargs):
        super(CartSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class CartOrderItemSerializer(serializers.ModelSerializer):
    """
    Serializes the CartOrderItem model.

    Args:
        serializers (type): The serializer class for the CartOrderItem model.
    """

    class Meta:
        fields = "__all__"
        model = api_models.CartOrderItem

    def __init__(self, *args, **kwargs):
        super(CartOrderItemSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class CartOrderSerializer(serializers.ModelSerializer):
    """
    Serializes the CartOrder model.

    Args:
        serializers (type): The serializer class for the CartOrder model.
    """

    order_items = CartOrderItemSerializer(many=True)

    class Meta:
        fields = "__all__"
        model = api_models.CartOrder

    def __init__(self, *args, **kwargs):
        super(CartOrderSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class CertificateSerializer(serializers.ModelSerializer):
    """
    Serializes the Certificate model.

    Args:
        serializers (type): The serializer class for the Certificate model.
    """

    class Meta:
        fields = "__all__"
        model = api_models.Certificate


class CompletedLessonSerializer(serializers.ModelSerializer):
    """
    Serializes the CompletedLesson model.

    Args:
        serializers (type): The serializer class for the CompletedLesson model.
    """

    class Meta:
        fields = "__all__"
        model = api_models.CompletedLesson

    def __init__(self, *args, **kwargs):
        super(CompletedLessonSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class NoteSerializer(serializers.ModelSerializer):
    """
    Serializes the Note model.

    Args:
        serializers (type): The serializer class for the Note model.
    """

    class Meta:
        fields = "__all__"
        model = api_models.Note


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializes the Review model.

    Args:
        serializers (type): The serializer class for the Review model.
    """

    profile = ProfileSerializer(many=False)

    class Meta:
        fields = "__all__"
        model = api_models.Review

    def __init__(self, *args, **kwargs):
        super(ReviewSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializes the Notification model.

    Args:
        serializers (type): The serializer class for the Notification model.
    """

    class Meta:
        fields = "__all__"
        model = api_models.Notification


class CouponSerializer(serializers.ModelSerializer):
    """
    Serializes the Coupon model.

    Args:
        serializers (type): The serializer class for the Coupon model.
    """

    class Meta:
        fields = "__all__"
        model = api_models.Coupon


class WishlistSerializer(serializers.ModelSerializer):
    """
    Serializes the Wishlist model.

    Args:
        serializers (type): The serializer class for the Wishlist model.
    """

    class Meta:
        fields = "__all__"
        model = api_models.Wishlist

    def __init__(self, *args, **kwargs):
        super(WishlistSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class CountrySerializer(serializers.ModelSerializer):
    """
    Serializes the Country model.

    Args:
        serializers (type): The serializer class for the Country model.
    """

    class Meta:
        fields = "__all__"
        model = api_models.Country


class EnrolledCourseSerializer(serializers.ModelSerializer):
    """
    Serializes the EnrolledCourse model.

    Args:
        serializers (type): The serializer class for the EnrolledCourse model.
    """

    lectures = VariantItemSerializer(many=True, read_only=True)
    completed_lesson = CompletedLessonSerializer(many=True, read_only=True)
    curriculum = VariantSerializer(many=True, read_only=True)
    note = NoteSerializer(many=True, read_only=True)
    question_answer = QuestionAnswerSerializer(many=True, read_only=True)
    review = ReviewSerializer(many=False, read_only=True)

    class Meta:
        fields = "__all__"
        model = api_models.EnrolledCourse

    def __init__(self, *args, **kwargs):
        super(EnrolledCourseSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializes the Course model.

    Args:
        serializers (type): The serializer class for the Course model.
    """

    students = EnrolledCourseSerializer(
        many=True,
        required=False,
        read_only=True,
    )
    curriculum = VariantSerializer(
        many=True,
        required=False,
        read_only=True,
    )
    lectures = VariantItemSerializer(
        many=True,
        required=False,
        read_only=True,
    )
    reviews = ReviewSerializer(many=True, read_only=True, required=False)

    class Meta:
        fields = [
            "id",
            "category",
            "teacher",
            "file",
            "image",
            "title",
            "description",
            "price",
            "language",
            "level",
            "platform_status",
            "teacher_course_status",
            "featured",
            "course_id",
            "slug",
            "date",
            "students",
            "curriculum",
            "lectures",
            "average_rating",
            "rating_count",
            "reviews",
        ]
        model = api_models.Course

    def __init__(self, *args, **kwargs):
        super(CourseSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3
