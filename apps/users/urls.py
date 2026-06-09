from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # ─── Auth ────────────────────────────────────────────────────────────────
    path('register/', views.RegisterView.as_view(), name='user-register'),
    path('login/', views.LoginView.as_view(), name='user-login'),
    path('logout/', views.LogoutView.as_view(), name='user-logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # ─── Profile ─────────────────────────────────────────────────────────────
    path('profile/', views.ProfileView.as_view(), name='user-profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),

    # ─── Admin: Users ─────────────────────────────────────────────────────────
    path('admin/users/', views.AdminUserListView.as_view(), name='admin-user-list'),
    path('admin/users/stats/', views.AdminUserStatsView.as_view(), name='admin-user-stats'),
    path('admin/users/<int:pk>/', views.AdminUserDetailView.as_view(), name='admin-user-detail'),
    path('admin/users/<int:pk>/toggle-active/', views.AdminUserToggleActiveView.as_view(), name='admin-user-toggle-active'),
    path('admin/users/<int:pk>/toggle-premium/', views.AdminUserTogglePremiumView.as_view(), name='admin-user-toggle-premium'),
]
