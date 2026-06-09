from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import User
from .serializers import (
    UserRegisterSerializer, UserLoginSerializer, UserProfileSerializer,
    UserListSerializer, UserAdminSerializer, ChangePasswordSerializer,
)
from .permissions import IsAdminUser


# ─── Public Auth ──────────────────────────────────────────────────────────────

class RegisterView(generics.CreateAPIView):
    """Yangi foydalanuvchi ro'yxatdan o'tishi"""
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserProfileSerializer(user, context={'request': request}).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """Foydalanuvchi kirishi - JWT token qaytaradi"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
        )
        if not user:
            return Response({'detail': 'Login yoki parol noto\'g\'ri'}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_active:
            return Response({'detail': 'Akkaunt faol emas'}, status=status.HTTP_403_FORBIDDEN)
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserProfileSerializer(user, context={'request': request}).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })


class LogoutView(APIView):
    """Foydalanuvchi chiqishi - refresh tokenni blacklist qiladi"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({'detail': 'Muvaffaqiyatli chiqildi'})
        except TokenError:
            return Response({'detail': 'Token noto\'g\'ri'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    """Joriy foydalanuvchi profili"""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    """Parol o'zgartirish"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'old_password': 'Eski parol noto\'g\'ri'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'detail': 'Parol muvaffaqiyatli o\'zgartirildi'})


# ─── Admin User Management ────────────────────────────────────────────────────

class AdminUserListView(generics.ListCreateAPIView):
    """Admin: barcha foydalanuvchilar ro'yxati"""
    queryset = User.objects.all().order_by('-date_joined')
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'is_staff', 'is_premium']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['date_joined', 'username', 'email']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserListSerializer
        return UserAdminSerializer


class AdminUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin: bitta foydalanuvchi CRUD"""
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = [IsAdminUser]


class AdminUserToggleActiveView(APIView):
    """Admin: foydalanuvchini faol/nofaol qilish"""
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.is_active = not user.is_active
            user.save()
            return Response({'is_active': user.is_active})
        except User.DoesNotExist:
            return Response({'detail': 'Topilmadi'}, status=status.HTTP_404_NOT_FOUND)


class AdminUserTogglePremiumView(APIView):
    """Admin: premium status o'zgartirish"""
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.is_premium = not user.is_premium
            user.save()
            return Response({'is_premium': user.is_premium})
        except User.DoesNotExist:
            return Response({'detail': 'Topilmadi'}, status=status.HTTP_404_NOT_FOUND)


class AdminUserStatsView(APIView):
    """Admin: foydalanuvchilar statistikasi"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        from django.utils import timezone
        from datetime import timedelta
        now = timezone.now()
        return Response({
            'total': User.objects.count(),
            'active': User.objects.filter(is_active=True).count(),
            'premium': User.objects.filter(is_premium=True).count(),
            'staff': User.objects.filter(is_staff=True).count(),
            'new_today': User.objects.filter(date_joined__date=now.date()).count(),
            'new_this_week': User.objects.filter(date_joined__gte=now - timedelta(days=7)).count(),
            'new_this_month': User.objects.filter(date_joined__gte=now - timedelta(days=30)).count(),
        })
