from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from django.db import models

from apps.users.permissions import IsAdminUser
from apps.users.models import User
from apps.kino.models import Movie, Clip, Comment, MovieView, SavedMovie


class AdminDashboardStatsView(APIView):
    """Admin dashboard - bosh sahifa statistikasi"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        now = timezone.now()
        today = now.date()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)

        # Movies
        movies_qs = Movie.objects.all()
        # Users
        users_qs = User.objects.all()
        # Views
        views_qs = MovieView.objects.all()

        data = {
            # ─── Overview ───────────────────────────
            'overview': {
                'total_movies': movies_qs.count(),
                'total_users': users_qs.count(),
                'total_clips': Clip.objects.count(),
                'total_views': movies_qs.aggregate(t=models.Sum('views'))['t'] or 0,
                'total_comments': Comment.objects.count(),
                'pending_comments': Comment.objects.filter(is_approved=False).count(),
                'total_saved': SavedMovie.objects.count(),
            },
            # ─── Today ──────────────────────────────
            'today': {
                'views': views_qs.filter(watched_at__date=today).count(),
                'new_users': users_qs.filter(date_joined__date=today).count(),
                'new_movies': movies_qs.filter(created_at__date=today).count(),
            },
            # ─── This Week ──────────────────────────
            'this_week': {
                'views': views_qs.filter(watched_at__gte=week_ago).count(),
                'new_users': users_qs.filter(date_joined__gte=week_ago).count(),
                'new_movies': movies_qs.filter(created_at__gte=week_ago).count(),
            },
            # ─── This Month ─────────────────────────
            'this_month': {
                'views': views_qs.filter(watched_at__gte=month_ago).count(),
                'new_users': users_qs.filter(date_joined__gte=month_ago).count(),
                'new_movies': movies_qs.filter(created_at__gte=month_ago).count(),
            },
            # ─── Movies Status ──────────────────────
            'movies_status': {
                'published': movies_qs.filter(status='published').count(),
                'draft': movies_qs.filter(status='draft').count(),
                'archived': movies_qs.filter(status='archived').count(),
            },
            # ─── Top Movies ─────────────────────────
            'top_movies': list(
                movies_qs.order_by('-views').values('id', 'title', 'views', 'rating')[:5]
            ),
            # ─── Recent Users ───────────────────────
            'recent_users': list(
                users_qs.order_by('-date_joined').values('id', 'username', 'email', 'date_joined')[:5]
            ),
        }
        return Response(data)


class AdminViewsChartView(APIView):
    """Ko'rishlar grafigi (oxirgi 30 kun)"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        days = int(request.query_params.get('days', 30))
        now = timezone.now()
        data = []
        for i in range(days - 1, -1, -1):
            day = (now - timedelta(days=i)).date()
            count = MovieView.objects.filter(watched_at__date=day).count()
            data.append({'date': str(day), 'views': count})
        return Response(data)


class AdminTopMoviesView(APIView):
    """Eng ko'p ko'rilgan kinolar"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        limit = int(request.query_params.get('limit', 10))
        movies = Movie.objects.order_by('-views').values(
            'id', 'title', 'views', 'rating', 'year', 'status'
        )[:limit]
        return Response(list(movies))


class AdminUserGrowthView(APIView):
    """Foydalanuvchilar o'sish grafigi"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        days = int(request.query_params.get('days', 30))
        now = timezone.now()
        data = []
        for i in range(days - 1, -1, -1):
            day = (now - timedelta(days=i)).date()
            count = User.objects.filter(date_joined__date=day).count()
            data.append({'date': str(day), 'users': count})
        return Response(data)


class AdminCategoryStatsView(APIView):
    """Kategoriyalar bo'yicha statistika"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        from apps.kino.models import Category
        categories = Category.objects.annotate(
            movie_count=models.Count('movies'),
            total_views=models.Sum('movies__views'),
        ).values('id', 'name', 'movie_count', 'total_views').order_by('-movie_count')
        return Response(list(categories))
