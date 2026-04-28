from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response

User = get_user_model()


@api_view(['GET', 'POST'])
def user_view(request):
    users = User.objects.all()
    user_list = []

    for user in users:
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        user_list.append(user_data)

    return Response({'users': user_list})



from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, UserSerializer


class RegisterView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]  # Allows anyone to register
    serializer_class = RegisterSerializer


class UserListDetailViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Requires the user to be authenticated





from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status, serializers
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from users.serializers import RegisterSerializer, UserSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from users.serializers import PasswordResetSerializer, PasswordResetConfirmSerializer

class PasswordResetRequestViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = PasswordResetSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = User.objects.get(email=email)

            # Token generation
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Password reset URL generation
            reset_url = request.build_absolute_uri(
                reverse("password-reset-confirm", kwargs={"uidb64": uid, "token": token})
            )

            # Send email
            send_mail(
                "პაროლის აღდგენა",
                f"დააჭირე ბმულს, რომ აღადგინო პაროლი: {reset_url}",
                "noreply@example.com",
                [user.email],
                fail_silently=False,
            )

            return Response(
                {"message": "შეტყობინება გაგზავნილია ელფოსტაზე"},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PasswordResetConfirmViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = PasswordResetConfirmSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'uidb64',
                openapi.IN_PATH,
                description="User ID (Base64 encoded)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'token',
                openapi.IN_PATH,
                description="Password reset token",
                type=openapi.TYPE_STRING
            ),
        ]
    )
    def create(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "პაროლი წარმატებით განახლდა"},
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )