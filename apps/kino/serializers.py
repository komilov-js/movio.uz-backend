from rest_framework import serializers
from .models import Category, Genre, Tag, Movie, Clip, SavedMovie, Comment, Slider, Season, Episode, Like


# ─── Category ─────────────────────────────────────────────────────────────────

class CategorySerializer(serializers.ModelSerializer):
    movie_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image', 'description', 'order', 'movie_count']

    def get_movie_count(self, obj):
        return obj.movies.filter(status='published').count()


class CategoryAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# ─── Genre & Tag ──────────────────────────────────────────────────────────────

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'slug']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


# ─── Movie ────────────────────────────────────────────────────────────────────

class MovieListSerializer(serializers.ModelSerializer):
    """Ro'yxat uchun yengil serializer"""
    category = CategorySerializer(read_only=True)
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'slug', 'poster', 'year', 'rating',
            'duration', 'category', 'quality', 'is_featured',
            'is_premium', 'views', 'is_saved',
        ]

    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return SavedMovie.objects.filter(user=request.user, movie=obj).exists()
        return False


class MovieDetailSerializer(serializers.ModelSerializer):
    """Detail uchun to'liq serializer"""
    category = CategorySerializer(read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    is_saved = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'original_title', 'slug', 'description', 'short_description',
            'poster', 'banner', 'video_url', 'trailer_url',
            'category', 'genres', 'tags',
            'year', 'duration', 'rating', 'imdb_rating',
            'language', 'country', 'director', 'cast',
            'quality', 'is_featured', 'is_premium',
            'views', 'likes', 'is_saved', 'comment_count',
            'created_at', 'published_at',
        ]

    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return SavedMovie.objects.filter(user=request.user, movie=obj).exists()
        return False

    def get_comment_count(self, obj):
        return obj.comments.filter(is_approved=True).count()


class MovieAdminSerializer(serializers.ModelSerializer):
    """Admin uchun to'liq CRUD serializer"""
    class Meta:
        model = Movie
        fields = '__all__'


# ─── Clip ─────────────────────────────────────────────────────────────────────

class ClipListSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True, allow_null=True)

    class Meta:
        model = Clip
        fields = ['id', 'title', 'slug', 'thumbnail', 'video_url', 'duration', 'movie', 'movie_title', 'views']


class ClipDetailSerializer(serializers.ModelSerializer):
    movie = MovieListSerializer(read_only=True)

    class Meta:
        model = Clip
        fields = '__all__'


class ClipAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clip
        fields = '__all__'


# ─── SavedMovie ───────────────────────────────────────────────────────────────

class SavedMovieSerializer(serializers.ModelSerializer):
    movie = MovieListSerializer(read_only=True)
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(), source='movie', write_only=True
    )

    class Meta:
        model = SavedMovie
        fields = ['id', 'movie', 'movie_id', 'created_at']


# ─── Comment ──────────────────────────────────────────────────────────────────

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'username', 'avatar', 'text', 'rating', 'created_at']
        read_only_fields = ['id', 'username', 'created_at']

    def get_avatar(self, obj):
        request = self.context.get('request')
        if obj.user.avatar and request:
            return request.build_absolute_uri(obj.user.avatar.url)
        return None


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text', 'rating']


class CommentAdminSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    movie_title = serializers.CharField(source='movie.title', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'username', 'movie_title', 'movie', 'user', 'text', 'rating', 'is_approved', 'created_at']


# ─── Slider ───────────────────────────────────────────────────────────────────


class SliderMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'year', 'rating', 'duration']

class SliderSerializer(serializers.ModelSerializer):
    movie = SliderMovieSerializer(read_only=True)

    class Meta:
        model = Slider
        fields = ['id', 'title', 'subtitle', 'image', 'movie', 'link', 'order']

class SliderAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = '__all__'


# ─── Episode & Season ─────────────────────────────────────────────────────────

class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ['id', 'number', 'title', 'description', 'thumbnail',
                  'video_url', 'duration', 'is_free', 'views', 'created_at']


class SeasonSerializer(serializers.ModelSerializer):
    episodes = EpisodeSerializer(many=True, read_only=True)
    episode_count = serializers.SerializerMethodField()

    class Meta:
        model = Season
        fields = ['id', 'number', 'title', 'poster', 'year',
                  'description', 'episode_count', 'episodes']

    def get_episode_count(self, obj):
        return obj.episodes.count()


class SeasonAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = '__all__'


class EpisodeAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = '__all__'


# ─── Like ─────────────────────────────────────────────────────────────────────

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'type', 'created_at']
