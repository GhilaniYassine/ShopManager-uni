from rest_framework import status, generics, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import UserProfile, Product
from .serializers import (
    SignUpSerializer, 
    SignInSerializer, 
    UserSerializer,
    UserProfileSerializer,
    ProductSerializer
)


class SignUpView(generics.CreateAPIView):
    """User registration endpoint"""
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()
        
        # Generate or get auth token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'success': True,
            'message': 'Account created successfully',
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)


class SignInView(generics.GenericAPIView):
    """User login endpoint"""
    serializer_class = SignInSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        # Generate or get auth token
        token, created = Token.objects.get_or_create(user=user)
        
        # Get user profile
        profile = UserProfile.objects.get(user=user)
        
        return Response({
            'success': True,
            'message': 'Login successful',
            'user': UserSerializer(user).data,
            'profile': UserProfileSerializer(profile).data,
            'token': token.key
        }, status=status.HTTP_200_OK)


class SignOutView(generics.GenericAPIView):
    """User logout endpoint"""
    
    def post(self, request, *args, **kwargs):
        try:
            # Delete user token
            request.user.auth_token.delete()
            return Response({
                'success': True,
                'message': 'Logged out successfully'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for user profile operations"""
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    
    def get_queryset(self):
        """Return only the current user's profile"""
        if self.request.user.is_authenticated:
            return UserProfile.objects.filter(user=self.request.user)
        return UserProfile.objects.none()
    
    def retrieve(self, request, *args, **kwargs):
        """Get current user's profile"""
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response({
                'success': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Profile not found'
            }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def check_auth(request):
    """Check if user is authenticated"""
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        return Response({
            'success': True,
            'authenticated': True,
            'user': UserSerializer(request.user).data,
            'profile': UserProfileSerializer(profile).data
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'success': False,
            'authenticated': False,
            'message': 'User not authenticated'
        }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_username(request):
    """Check if username is available"""
    username = request.data.get('username', '')
    
    if not username:
        return Response({
            'success': False,
            'message': 'Username is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    exists = User.objects.filter(username=username).exists()
    
    return Response({
        'success': True,
        'available': not exists
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request):
    """Check if email is available"""
    email = request.data.get('email', '')
    
    if not email:
        return Response({
            'success': False,
            'message': 'Email is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    exists = User.objects.filter(email=email).exists()
    
    return Response({
        'success': True,
        'available': not exists
    }, status=status.HTTP_200_OK)


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for product CRUD operations"""
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return only products for the current user"""
        return Product.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Create product for current user"""
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        """Update product for current user"""
        serializer.save(user=self.request.user)
