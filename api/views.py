from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from .serializers import (
    MemberSerializer,
    RegisterSerializer,
    LoginSerializer,
    MessageSerializer
)
from .models import Member
from .authentication import MemberTokenAuthentication


class RegisterView(APIView):
    """User registration endpoint"""

    @extend_schema(
        request=RegisterSerializer,
        responses={201: MemberSerializer},
        description="Register a new user"
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            member = serializer.save()
            token, created = Token.objects.get_or_create(user_id=member.id)
            member_serializer = MemberSerializer(member)
            return Response(
                {
                    'token': token.key,
                    'user': member_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """User login endpoint"""

    @extend_schema(
        request=LoginSerializer,
        responses={200: MemberSerializer},
        description="Login user and return token"
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            try:
                member = Member.objects.get(username=username)
                if member.check_password(password):
                    token, created = Token.objects.get_or_create(user_id=member.id)
                    member_serializer = MemberSerializer(member)
                    return Response(
                        {
                            'token': token.key,
                            'user': member_serializer.data
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {'error': 'Invalid credentials'},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            except Member.DoesNotExist:
                return Response(
                    {'error': 'Invalid credentials'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):
    """Get current authenticated user"""
    authentication_classes = [MemberTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: MemberSerializer},
        description="Get current user information"
    )
    def get(self, request):
        serializer = MemberSerializer(request.user)
        return Response(serializer.data)


class ProfileView(APIView):
    """Get and update user profile"""
    authentication_classes = [MemberTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: MemberSerializer},
        description="Get user profile"
    )
    def get(self, request):
        serializer = MemberSerializer(request.user)
        return Response(serializer.data)

    @extend_schema(
        request=MemberSerializer,
        responses={200: MemberSerializer},
        description="Update user profile (full_name only)"
    )
    def put(self, request):
        member = request.user
        if 'full_name' in request.data:
            member.full_name = request.data['full_name']
            member.save()
        serializer = MemberSerializer(member)
        return Response(serializer.data)


class HelloView(APIView):
    """
    A simple API endpoint that returns a greeting message.
    """

    @extend_schema(
        responses={200: MessageSerializer},
        description="Get a hello world message"
    )
    def get(self, request):
        data = {"message": "Hello!", "timestamp": timezone.now()}
        return Response(data)
