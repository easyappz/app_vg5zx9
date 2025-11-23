from rest_framework import serializers
from .models import Member, Message


class MemberSerializer(serializers.ModelSerializer):
    """Serializer for Member model without password_hash"""
    class Meta:
        model = Member
        fields = ['id', 'username', 'full_name', 'created_at', 'last_seen']
        read_only_fields = ['id', 'created_at', 'last_seen']


class RegisterSerializer(serializers.Serializer):
    """Serializer for user registration"""
    username = serializers.CharField(max_length=150)
    full_name = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True, min_length=6)

    def validate_username(self, value):
        """Check if username already exists"""
        if Member.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def create(self, validated_data):
        """Create new member with hashed password"""
        member = Member(
            username=validated_data['username'],
            full_name=validated_data['full_name']
        )
        member.set_password(validated_data['password'])
        member.save()
        return member


class LoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)


class MessageAuthorSerializer(serializers.ModelSerializer):
    """Nested serializer for message author"""
    class Meta:
        model = Member
        fields = ['id', 'username', 'full_name']


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model with nested author"""
    author = MessageAuthorSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'author', 'text', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']
