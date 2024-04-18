from django.conf import settings
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from random import randint
from decimal import Decimal

from api import models as api_models
from userauths.models import User, Profile
from api import serializer as api_serializer


class MyTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for obtaining token pairs.

    Args:
        TokenObtainPairView (type): Base class for token obtain views.
    """

    serializer_class = api_serializer.MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    """
    Custom view for user registration.

    Args:
        generics (type): Base class for generic views.
    """

    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = api_serializer.RegisterSerializer


def generate_random_otp(length=7):
    """
    Generates a random one-time password (OTP).

    Args:
        length (int, optional): Length of the OTP. Defaults to 7.

    Returns:
        str: A randomly generated OTP.
    """
    otp = "".join([str(randint(0, 9)) for _ in range(length)])

    return otp


class PasswordResetEmailVerifyAPIView(generics.RetrieveAPIView):
    """
    Custom view for verifying password reset email.

    Args:
        generics (type): Base class for generic views.
    """

    permission_classes = [AllowAny]
    serializer_class = api_serializer.UserSerializer

    def get_object(self):
        email = self.kwargs["email"]
        user = User.objects.filter(email=email).first()

        if user:
            uuidb64 = user.pk
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh.access_token)

            user.refresh_token = refresh_token
            user.otp = generate_random_otp()
            user.save()

            link = f"http://localhost:5173/create-new-password/?otp={user.otp}&uuidb64={uuidb64}&refresh_token={refresh_token}"

            context = {"link": link, "username": user.username}

            html_body = render_to_string("email/password_reset.html", context)

            msg = EmailMultiAlternatives(
                subject="Password Rest Email",
                body="",
                from_email=settings.FROM_EMAIL,
                to=[user.email],
            )

            msg.attach_alternative(html_body, "text/html")
            msg.send()

        return user


class PasswordChangeAPIView(generics.CreateAPIView):
    """
    Custom view for changing user passwords.

    Args:
        generics (type): Base class for generic views.

    Returns:
        Response: A response indicating success or failure.
    """

    serializer_class = api_serializer.UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        otp = request.data["otp"]
        uuidb64 = request.data["uuidb64"]
        password = request.data["password"]

        user = User.objects.get(id=uuidb64, otp=otp)

        if user:
            user.set_password(password)
            user.otp = ""
            user.save()

            return Response(
                {"message": "Password Changed Successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"message": "User Does Not Exists"}, status=status.HTTP_404_NOT_FOUND
            )


class CategoryListAPIView(generics.ListAPIView):
    """
    API view for listing categories.

    Args:
        generics (type): The base class for generic views.
    """

    queryset = api_models.Category.objects.filter(active=True)
    serializer_class = api_serializer.CategorySerializer
    permission_classes = [AllowAny]


class CourseListAPIView(generics.ListAPIView):
    """
    API view for listing published courses.

    Args:
        generics (type): The base class for generic views.
    """

    queryset = api_models.Course.objects.filter(
        platform_status="Published", teacher_course_status="Published"
    )
    serializer_class = api_serializer.CourseSerializer
    permission_classes = [AllowAny]


class CourseDetailAPIView(generics.RetrieveAPIView):
    """
    API view for retrieving details of a published course.

    Args:
        generics (type): The base class for generic views.

    Returns:
        type: The serialized course details.
    """

    serializer_class = api_serializer.CourseSerializer
    permission_classes = [AllowAny]
    queryset = api_models.Course.objects.filter(
        platform_status="Published", teacher_course_status="Published"
    )

    def get_object(self):
        slug = self.kwargs["slug"]
        course = api_models.Course.objects.get(
            slug=slug, platform_status="Published", teacher_course_status="Published"
        )
        return course


class CartAPIView(generics.CreateAPIView):
    """
    API view for managing shopping carts.

    Args:
        generics (Type[generics.CreateAPIView]): The base class for creating a new cart.

    Returns:
        Response: A response indicating the success or failure of cart creation/update.
    """

    queryset = api_models.Cart.objects.all()
    serializer_class = api_serializer.CartSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        course_id = request.data["course_id"]
        user_id = request.data["user_id"]
        price = request.data["price"]
        country_name = request.data["country_name"]
        cart_id = request.data["cart_id"]

        course = api_models.Course.objects.filter(id=course_id).first()
        user = User.objects.get(id=user_id) if user_id != "undefined" else None

        try:
            country_object = api_models.Country.objects.get(name=country_name)
            country = country_object.name
            tax_rate = country_object.tax_rate / 100
        except api_models.Country.DoesNotExist:
            country = "United Kingdom"
            tax_rate = 0

        cart = api_models.Cart.objects.filter(cart_id=cart_id, course=course).first()

        if cart:
            cart.course = course
            cart.user = user
            cart.price = price
            cart.tax_fee = Decimal(price) * Decimal(tax_rate)
            cart.country = country
            cart.cart_id = cart_id
            cart.total = Decimal(cart.price) + Decimal(cart.tax_fee)
            cart.save()

            return Response(
                {"message": "Cart Updated Successfully"}, status=status.HTTP_200_OK
            )

        else:
            cart = api_models.Cart()

            cart.course = course
            cart.user = user
            cart.price = price
            cart.tax_fee = Decimal(price) * Decimal(tax_rate)
            cart.country = country
            cart.cart_id = cart_id
            cart.total = Decimal(cart.price) + Decimal(cart.tax_fee)
            cart.save()

            return Response(
                {"message": "Cart Created Successfully"}, status=status.HTTP_201_CREATED
            )


class CartListAPIView(generics.ListAPIView):
    serializer_class = api_serializer.CartSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        cart_id = self.kwargs["cart_id"]
        queryset = api_models.Cart.objects.filter(cart_id=cart_id)

        return queryset


class CartItemDeleteAPIView(generics.DestroyAPIView):
    serializer_class = api_serializer.CartSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        cart_id = self.kwargs["cart_id"]
        item_id = self.kwargs["item_id"]

        return api_models.Cart.objects.filter(cart_id=cart_id, id=item_id).first()


class CartStatsAPIView(generics.RetrieveAPIView):
    serializer_class = api_serializer.CartSerializer
    permission_classes = [AllowAny]
    lookup_field = "cart_id"

    def get_queryset(self):
        cart_id = self.kwargs["cart_id"]
        return api_models.Cart.objects.filter(cart_id=cart_id)

    def retrieve_cart_statistics(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        total_price = 0.00
        total_tax = 0.00
        total_total = 0.00

        for cart_item in queryset:
            total_price += float(self.calculate_price(cart_item))
            total_tax += float(self.calculate_tax(cart_item))
            total_total += round(float(self.calculate_total(cart_item)), 2)

        data = {
            "price": total_price,
            "tax": total_tax,
            "total": total_total,
        }

        return Response(data)

    def calculate_price(self, cart_item: api_models.Cart) -> float:
        return cart_item.price

    def calculate_tax(self, cart_item: api_models.Cart) -> float:
        return cart_item.tax_fee

    def calculate_total(self, cart_item: api_models.Cart) -> float:
        return cart_item.total
