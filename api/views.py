from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.utils import timezone
from datetime import timedelta
from drf_spectacular.utils import extend_schema
from .serializers import (
    MemberSerializer,
    RegisterSerializer,
    LoginSerializer,
    MessageSerializer
)
from .models import Member, Message
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


class MessagesListView(APIView):
    """Get all chat messages and create new messages"""
    authentication_classes = [MemberTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: MessageSerializer(many=True)},
        description="Get all messages sorted by time with author info"
    )
    def get(self, request):
        messages = Message.objects.all().select_related('author').order_by('created_at')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=MessageSerializer,
        responses={201: MessageSerializer},
        description="Create new message from current user"
    )
    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save(author=request.user)
            response_serializer = MessageSerializer(message)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OnlineUsersView(APIView):
    """Get list of online users"""
    authentication_classes = [MemberTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: MemberSerializer(many=True)},
        description="Get list of users active in last 5 minutes"
    )
    def get(self, request):
        time_threshold = timezone.now() - timedelta(minutes=5)
        online_members = Member.objects.filter(last_seen__gte=time_threshold).order_by('username')
        serializer = MemberSerializer(online_members, many=True)
        return Response(serializer.data)


class HeartbeatView(APIView):
    """Update user last seen timestamp"""
    authentication_classes = [MemberTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: dict},
        description="Update current user's last_seen to current time"
    )
    def post(self, request):
        request.user.update_last_seen()
        return Response({'status': 'online'}, status=status.HTTP_200_OK)


class HelloView(APIView):
    """
    A simple API endpoint that returns a greeting message.
    """

    @extend_schema(
        responses={200: dict},
        description="Get a hello world message"
    )
    def get(self, request):
        data = {"message": "Hello!", "timestamp": timezone.now()}
        return Response(data)
