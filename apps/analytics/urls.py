from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.AdminDashboardStatsView.as_view(), name='admin-dashboard'),
    path('views-chart/', views.AdminViewsChartView.as_view(), name='admin-views-chart'),
    path('top-movies/', views.AdminTopMoviesView.as_view(), name='admin-top-movies'),
    path('user-growth/', views.AdminUserGrowthView.as_view(), name='admin-user-growth'),
    path('category-stats/', views.AdminCategoryStatsView.as_view(), name='admin-category-stats'),
]
