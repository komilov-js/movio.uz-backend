from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """Faqat staff/admin foydalanuvchilar uchun"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)
