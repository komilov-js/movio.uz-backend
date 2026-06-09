from django.contrib import admin
from .models import Category, Genre, Tag, Movie, Clip, SavedMovie, Comment, Slider, MovieView


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'year', 'category', 'status', 'is_featured', 'views', 'rating']
    list_filter = ['status', 'category', 'year', 'quality', 'is_featured', 'is_premium']
    search_fields = ['title', 'original_title', 'director']
    list_editable = ['status', 'is_featured']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['genres', 'tags']
    readonly_fields = ['views', 'likes', 'created_at', 'updated_at']


@admin.register(Clip)
class ClipAdmin(admin.ModelAdmin):
    list_display = ['title', 'movie', 'views', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(SavedMovie)
class SavedMovieAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'movie__title']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'text', 'rating', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    list_editable = ['is_approved']
    search_fields = ['user__username', 'movie__title', 'text']


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'movie', 'order', 'is_active']
    list_editable = ['order', 'is_active']


@admin.register(MovieView)
class MovieViewAdmin(admin.ModelAdmin):
    list_display = ['movie', 'user', 'ip_address', 'watched_at']
    list_filter = ['watched_at']

from .models import Season, Episode, Like

class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 1
    fields = ['number', 'title', 'video_url', 'duration', 'is_free']

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ['movie', 'number', 'title', 'year']
    list_filter = ['movie']
    inlines = [EpisodeInline]

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ['movie', 'season', 'number', 'title', 'duration', 'is_free', 'views']
    list_filter = ['movie', 'season', 'is_free']
    search_fields = ['title', 'movie__title']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'type', 'created_at']
    list_filter = ['type']
