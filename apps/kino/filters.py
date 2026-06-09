import django_filters
from .models import Movie, Clip, Comment


class MovieFilter(django_filters.FilterSet):
    year_min = django_filters.NumberFilter(field_name='year', lookup_expr='gte')
    year_max = django_filters.NumberFilter(field_name='year', lookup_expr='lte')
    rating_min = django_filters.NumberFilter(field_name='rating', lookup_expr='gte')
    duration_max = django_filters.NumberFilter(field_name='duration', lookup_expr='lte')
    category = django_filters.NumberFilter(field_name='category__id')
    genre = django_filters.NumberFilter(field_name='genres__id')
    tag = django_filters.CharFilter(field_name='tags__slug')

    class Meta:
        model = Movie
        fields = ['category', 'year_min', 'year_max', 'rating_min', 'duration_max',
                  'language', 'country', 'quality', 'is_featured', 'is_premium', 'status']


class ClipFilter(django_filters.FilterSet):
    movie = django_filters.NumberFilter(field_name='movie__id')

    class Meta:
        model = Clip
        fields = ['movie', 'is_active']


class CommentFilter(django_filters.FilterSet):
    movie = django_filters.NumberFilter(field_name='movie__id')

    class Meta:
        model = Comment
        fields = ['movie', 'is_approved', 'user']
