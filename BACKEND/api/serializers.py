from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'shop_name', 'phone', 'address', 'city', 'country', 'created_at', 'updated_at']


class SignUpSerializer(serializers.Serializer):
    """Serializer for user registration"""
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    shop_name = serializers.CharField(max_length=200, required=False, allow_blank=True)

    def validate(self, data):
        """Validate that passwords match"""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError(
                {"password": "Passwords must match"}
            )
        return data

    def validate_username(self, value):
        """Check if username already exists"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Username already exists"
            )
        return value

    def validate_email(self, value):
        """Check if email already exists"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Email already registered"
            )
        return value

    def create(self, validated_data):
        """Create new user"""
        validated_data.pop('password_confirm')
        shop_name = validated_data.pop('shop_name', '')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        # Update user profile with shop_name (profile is auto-created by signal)
        profile = UserProfile.objects.get(user=user)
        if shop_name:
            profile.shop_name = shop_name
            profile.save()
        
        return user


class SignInSerializer(serializers.Serializer):
    """Serializer for user login"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Authenticate user"""
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError(
                "Username and password are required"
            )

        user = authenticate(username=username, password=password)
        
        if not user:
            raise serializers.ValidationError(
                "Invalid credentials"
            )

        data['user'] = user
        return data
