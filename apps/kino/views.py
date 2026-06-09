from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.utils import timezone

from apps.users.permissions import IsAdminUser
from .models import Category, Genre, Tag, Movie, Clip, SavedMovie, Comment, Slider, MovieView, Season, Episode, Like
from .serializers import (
    CategorySerializer, CategoryAdminSerializer,
    GenreSerializer, TagSerializer,
    MovieListSerializer, MovieDetailSerializer, MovieAdminSerializer,
    ClipListSerializer, ClipDetailSerializer, ClipAdminSerializer,
    SavedMovieSerializer,
    CommentSerializer, CommentCreateSerializer, CommentAdminSerializer,
    SliderSerializer, SliderAdminSerializer,
    SeasonSerializer, EpisodeSerializer,
    SeasonAdminSerializer, EpisodeAdminSerializer, LikeSerializer,
)
from django.db import models
from .filters import MovieFilter, ClipFilter, CommentFilter


def get_client_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded.split(',')[0] if x_forwarded else request.META.get('REMOTE_ADDR')


# ─── Category ─────────────────────────────────────────────────────────────────

class CategoryListView(generics.ListAPIView):
    """Faol kategoriyalar ro'yxati (frontend)"""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


# ─── Genre & Tag ──────────────────────────────────────────────────────────────

class GenreListView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.AllowAny]


class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'slug']


# ─── Movie: Public ────────────────────────────────────────────────────────────

class MovieListView(generics.ListAPIView):
    """Chop etilgan kinolar ro'yxati"""
    serializer_class = MovieListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MovieFilter
    search_fields = ['title', 'original_title', 'description', 'director', 'cast']
    ordering_fields = ['created_at', 'views', 'rating', 'year', 'likes']
    ordering = ['-created_at']

    def get_queryset(self):
        return Movie.objects.filter(status='published').select_related('category').prefetch_related('genres', 'tags')


class MovieDetailView(generics.RetrieveAPIView):
    """Kino detali - ko'rishni ham hisoblaydi"""
    serializer_class = MovieDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Movie.objects.filter(status='published').select_related('category').prefetch_related('genres', 'tags')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Ko'rishni hisoblash
        instance.increment_views()
        MovieView.objects.create(
            movie=instance,
            user=request.user if request.user.is_authenticated else None,
            ip_address=get_client_ip(request),
        )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class FeaturedMoviesView(generics.ListAPIView):
    """Tanlangan kinolar (hero banner uchun)"""
    serializer_class = MovieListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Movie.objects.filter(status='published', is_featured=True).order_by('-created_at')[:10]


class TopRatedMoviesView(generics.ListAPIView):
    """Eng yuqori reytingli kinolar"""
    serializer_class = MovieListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Movie.objects.filter(status='published').order_by('-rating')[:20]


class MostViewedMoviesView(generics.ListAPIView):
    """Eng ko'p ko'rilgan kinolar"""
    serializer_class = MovieListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Movie.objects.filter(status='published').order_by('-views')[:20]


class NewReleasesView(generics.ListAPIView):
    """Yangi kinolar"""
    serializer_class = MovieListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Movie.objects.filter(status='published').order_by('-published_at', '-created_at')[:20]


class RelatedMoviesView(generics.ListAPIView):
    """O'xshash kinolar (detail sahifasi uchun)"""
    serializer_class = MovieListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        movie = get_object_or_404(Movie, pk=self.kwargs['pk'], status='published')
        return Movie.objects.filter(
            status='published', category=movie.category
        ).exclude(pk=movie.pk).order_by('-views')[:8]


class MoviesByYearView(generics.ListAPIView):
    """Yil bo'yicha kinolar"""
    serializer_class = MovieListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        year = self.kwargs['year']
        return Movie.objects.filter(status='published', year=year).order_by('-rating')


class MoviesByCategoryView(generics.ListAPIView):
    """Kategoriya bo'yicha kinolar"""
    serializer_class = MovieListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [OrderingFilter]
    ordering_fields = ['views', 'rating', 'year', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Movie.objects.filter(status='published', category__id=category_id)


# ─── Clip: Public ─────────────────────────────────────────────────────────────

class ClipListView(generics.ListAPIView):
    serializer_class = ClipListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ClipFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'views']
    ordering = ['-created_at']

    def get_queryset(self):
        return Clip.objects.filter(is_active=True).select_related('movie')


class ClipDetailView(generics.RetrieveAPIView):
    queryset = Clip.objects.filter(is_active=True)
    serializer_class = ClipDetailSerializer
    permission_classes = [permissions.AllowAny]


class MovieClipsView(generics.ListAPIView):
    """Bitta kinoning barcha kliplari"""
    serializer_class = ClipListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Clip.objects.filter(movie__id=self.kwargs['movie_id'], is_active=True).order_by('order')


# ─── SavedMovies ──────────────────────────────────────────────────────────────

class SavedMovieListView(generics.ListCreateAPIView):
    serializer_class = SavedMovieSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedMovie.objects.filter(user=self.request.user).select_related('movie', 'movie__category')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SavedMovieDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedMovie.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        movie_id = kwargs.get('movie_id')
        obj = get_object_or_404(SavedMovie, user=request.user, movie__id=movie_id)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ─── Comments ─────────────────────────────────────────────────────────────────

class MovieCommentListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Tasdiqlangan barcha sharhlar + foydalanuvchining o‘z tasdiqlanmagan sharhlari
        qs = Comment.objects.filter(movie__id=self.kwargs['movie_id'])
        if self.request.user.is_authenticated:
            return qs.filter(models.Q(is_approved=True) | models.Q(user=self.request.user))
        return qs.filter(is_approved=True)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        movie = get_object_or_404(Movie, pk=self.kwargs['movie_id'])
        serializer.save(user=self.request.user, movie=movie)
        # Agar admin tomonidan tekshiruv shart bo‘lmasa, quyidagi qatorni qo‘shing:
        serializer.instance.is_approved = True
        serializer.instance.save()

class CommentDeleteView(generics.DestroyAPIView):
    """Foydalanuvchi o'z izohini o'chirishi"""
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)


# ─── Slider ───────────────────────────────────────────────────────────────────

class SliderListView(generics.ListAPIView):
    queryset = Slider.objects.filter(is_active=True).order_by('order')
    serializer_class = SliderSerializer
    permission_classes = [permissions.AllowAny]


# ─── Search ───────────────────────────────────────────────────────────────────

class SearchView(APIView):
    """Kino va kliplarni qidirish"""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        q = request.query_params.get('q', '').strip()
        if len(q) < 2:
            return Response({'movies': [], 'clips': [], 'query': q})

        movies = Movie.objects.filter(
            status='published'
        ).filter(
            models.Q(title__icontains=q) |
            models.Q(original_title__icontains=q) |
            models.Q(description__icontains=q) |
            models.Q(director__icontains=q)
        )[:20]

        clips = Clip.objects.filter(
            is_active=True, title__icontains=q
        )[:10]

        return Response({
            'query': q,
            'movies': MovieListSerializer(movies, many=True, context={'request': request}).data,
            'clips': ClipListSerializer(clips, many=True, context={'request': request}).data,
            'total': movies.count() + clips.count(),
        })




# ─── Admin: Category ──────────────────────────────────────────────────────────

class AdminCategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryAdminSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'slug']
    ordering_fields = ['order', 'name', 'created_at']


class AdminCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryAdminSerializer
    permission_classes = [IsAdminUser]


# ─── Admin: Genre & Tag ───────────────────────────────────────────────────────

class AdminGenreListView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUser]


class AdminGenreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUser]


class AdminTagListView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUser]


class AdminTagDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUser]


# ─── Admin: Movies ────────────────────────────────────────────────────────────

class AdminMovieListView(generics.ListCreateAPIView):
    queryset = Movie.objects.all().select_related('category')
    serializer_class = MovieAdminSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MovieFilter
    search_fields = ['title', 'original_title', 'director']
    ordering_fields = ['created_at', 'views', 'rating', 'year', 'status']
    ordering = ['-created_at']


class AdminMovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieAdminSerializer
    permission_classes = [IsAdminUser]


class AdminMoviePublishView(APIView):
    """Admin: kinoni chop etish / arxivlash"""
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        action = request.data.get('action', 'publish')
        if action == 'publish':
            movie.status = 'published'
            movie.published_at = timezone.now()
        elif action == 'draft':
            movie.status = 'draft'
        elif action == 'archive':
            movie.status = 'archived'
        movie.save()
        return Response({'status': movie.status})


class AdminMovieToggleFeaturedView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        movie.is_featured = not movie.is_featured
        movie.save()
        return Response({'is_featured': movie.is_featured})


class AdminMovieStatsView(APIView):
    """Admin: kinolar statistikasi"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        from django.utils import timezone
        from datetime import timedelta
        now = timezone.now()
        qs = Movie.objects.all()
        return Response({
            'total': qs.count(),
            'published': qs.filter(status='published').count(),
            'draft': qs.filter(status='draft').count(),
            'archived': qs.filter(status='archived').count(),
            'featured': qs.filter(is_featured=True).count(),
            'premium': qs.filter(is_premium=True).count(),
            'total_views': qs.aggregate(t=models.Sum('views'))['t'] or 0,
            'new_this_week': qs.filter(created_at__gte=now - timedelta(days=7)).count(),
        })


# ─── Admin: Clips ─────────────────────────────────────────────────────────────

class AdminClipListView(generics.ListCreateAPIView):
    queryset = Clip.objects.all().select_related('movie')
    serializer_class = ClipAdminSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['created_at', 'views', 'order']


class AdminClipDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Clip.objects.all()
    serializer_class = ClipAdminSerializer
    permission_classes = [IsAdminUser]


# ─── Admin: Comments ──────────────────────────────────────────────────────────

class AdminCommentListView(generics.ListAPIView):
    queryset = Comment.objects.all().select_related('user', 'movie')
    serializer_class = CommentAdminSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CommentFilter
    search_fields = ['text', 'user__username', 'movie__title']
    ordering = ['-created_at']


class AdminCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentAdminSerializer
    permission_classes = [IsAdminUser]


class AdminCommentApproveView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.is_approved = not comment.is_approved
        comment.save()
        return Response({'is_approved': comment.is_approved})


# ─── Admin: Slider ────────────────────────────────────────────────────────────

class AdminSliderListView(generics.ListCreateAPIView):
    queryset = Slider.objects.all()
    serializer_class = SliderAdminSerializer
    permission_classes = [IsAdminUser]


class AdminSliderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Slider.objects.all()
    serializer_class = SliderAdminSerializer
    permission_classes = [IsAdminUser]


# ─── Season & Episode: Public ─────────────────────────────────────────────────


class MovieSeasonsView(generics.ListAPIView):
    """Kinoning barcha mavsumlari (episode bilan)"""
    serializer_class = SeasonSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Season.objects.filter(
            movie__id=self.kwargs['movie_id'], movie__status='published'
        ).prefetch_related('episodes')


class SeasonEpisodesView(generics.ListAPIView):
    """Bitta mavzumning qismlari"""
    serializer_class = EpisodeSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Episode.objects.filter(
            season__id=self.kwargs['season_id']
        ).order_by('number')


class EpisodeDetailView(generics.RetrieveAPIView):
    """Bitta qism detali"""
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Episode.objects.filter(pk=instance.pk).update(views=models.F('views') + 1)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# ─── Like/Dislike ─────────────────────────────────────────────────────────────

class MovieLikeView(APIView):
    """Kinoga like yoki dislike"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        like_type = request.data.get('type', 'like')
        if like_type not in ['like', 'dislike']:
            return Response({'detail': 'type: like yoki dislike bo\'lishi kerak'}, status=400)

        like_obj, created = Like.objects.get_or_create(
            movie=movie, user=request.user,
            defaults={'type': like_type}
        )
        if not created:
            if like_obj.type == like_type:
                like_obj.delete()
                action = 'removed'
            else:
                like_obj.type = like_type
                like_obj.save()
                action = 'changed'
        else:
            action = 'added'

        likes = Like.objects.filter(movie=movie, type='like').count()
        dislikes = Like.objects.filter(movie=movie, type='dislike').count()
        Movie.objects.filter(pk=pk).update(likes=likes)

        user_like = Like.objects.filter(movie=movie, user=request.user).first()
        return Response({
            'action': action,
            'likes': likes,
            'dislikes': dislikes,
            'user_type': user_like.type if user_like else None,
        })


class MovieLikeStatusView(APIView):
    """Foydalanuvchining like holati"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        likes = Like.objects.filter(movie=movie, type='like').count()
        dislikes = Like.objects.filter(movie=movie, type='dislike').count()
        user_type = None
        if request.user.is_authenticated:
            like_obj = Like.objects.filter(movie=movie, user=request.user).first()
            user_type = like_obj.type if like_obj else None
        return Response({'likes': likes, 'dislikes': dislikes, 'user_type': user_type})


# ─── Admin: Season & Episode ──────────────────────────────────────────────────

class AdminSeasonListView(generics.ListCreateAPIView):
    serializer_class = SeasonAdminSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['movie']

    def get_queryset(self):
        return Season.objects.all().select_related('movie')


class AdminSeasonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Season.objects.all()
    serializer_class = SeasonAdminSerializer
    permission_classes = [IsAdminUser]


class AdminEpisodeListView(generics.ListCreateAPIView):
    serializer_class = EpisodeAdminSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['season', 'movie', 'is_free']
    search_fields = ['title']

    def get_queryset(self):
        return Episode.objects.all().select_related('season', 'movie')


class AdminEpisodeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Episode.objects.all()
    serializer_class = EpisodeAdminSerializer
    permission_classes = [IsAdminUser]
