from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nomi')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name='Rasm')
    description = models.TextField(blank=True, verbose_name='Tavsif')
    order = models.PositiveIntegerField(default=0, verbose_name='Tartib')
    is_active = models.BooleanField(default=True, verbose_name='Faol')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nomi')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Janr'
        verbose_name_plural = 'Janrlar'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Teg'
        verbose_name_plural = 'Teglar'

    def __str__(self):
        return self.name


class Movie(models.Model):
    QUALITY_CHOICES = [
        ('SD', 'SD'),
        ('HD', 'HD'),
        ('FHD', 'Full HD'),
        ('4K', '4K'),
    ]
    STATUS_CHOICES = [
        ('draft', 'Qoralama'),
        ('published', 'Chop etilgan'),
        ('archived', 'Arxivlangan'),
    ]

    title = models.CharField(max_length=255, verbose_name='Nomi')
    original_title = models.CharField(max_length=255, blank=True, verbose_name='Original nomi')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    description = models.TextField(verbose_name='Tavsif')
    short_description = models.CharField(max_length=300, blank=True, verbose_name='Qisqa tavsif')

    poster = models.ImageField(upload_to='posters/', verbose_name='Poster')
    banner = models.ImageField(upload_to='banners/', null=True, blank=True, verbose_name='Banner')

    video_url = models.CharField(max_length=10000, blank=True)
    trailer_url = models.URLField(blank=True, verbose_name='Treyler URL')

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        related_name='movies', verbose_name='Kategoriya'
    )
    genres = models.ManyToManyField(Genre, blank=True, verbose_name='Janrlar')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Teglar')

    year = models.PositiveIntegerField(verbose_name='Yil')
    duration = models.PositiveIntegerField(null=True, blank=True, verbose_name='Davomiyligi (daqiqa)')
    rating = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name='Reyting'
    )
    imdb_rating = models.FloatField(null=True, blank=True, verbose_name='IMDB reyting')

    language = models.CharField(max_length=50, blank=True, verbose_name='Til')
    country = models.CharField(max_length=100, blank=True, verbose_name='Mamlakat')
    director = models.CharField(max_length=200, blank=True, verbose_name='Rejissyor')
    cast = models.TextField(blank=True, verbose_name='Aktyorlar')

    quality = models.CharField(max_length=5, choices=QUALITY_CHOICES, default='HD', verbose_name='Sifat')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='Holat')
    is_featured = models.BooleanField(default=False, verbose_name='Tanlangan')
    is_premium = models.BooleanField(default=False, verbose_name='Premium')

    views = models.PositiveIntegerField(default=0, verbose_name='Ko\'rishlar')
    likes = models.PositiveIntegerField(default=0, verbose_name='Yoqtirganlar')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Kino'
        verbose_name_plural = 'Kinolar'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} ({self.year})'

    def increment_views(self):
        Movie.objects.filter(pk=self.pk).update(views=models.F('views') + 1)


class Clip(models.Model):
    title = models.CharField(max_length=255, verbose_name='Nomi')
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, verbose_name='Tavsif')
    thumbnail = models.ImageField(upload_to='clip_thumbnails/', verbose_name='Thumbnail')
    video_url = models.URLField(verbose_name='Video URL')
    duration = models.PositiveIntegerField(null=True, blank=True, verbose_name='Davomiylik (soniya)')
    movie = models.ForeignKey(
        Movie, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='clips', verbose_name='Kino'
    )
    views = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Klip'
        verbose_name_plural = 'Kliplar'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class SavedMovie(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='saved_movies', verbose_name='Foydalanuvchi'
    )
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE,
        related_name='saved_by', verbose_name='Kino'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Saqlangan kino'
        verbose_name_plural = 'Saqlangan kinolar'
        unique_together = ['user', 'movie']
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} → {self.movie}'


class MovieView(models.Model):
    """Kino ko'rishlar tarixi"""
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='view_logs')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='viewed_movies'
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    watched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ko'rish"
        verbose_name_plural = "Ko'rishlar"
        ordering = ['-watched_at']


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments', verbose_name='Kino')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(verbose_name='Matn')
    rating = models.PositiveIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Baho'
    )
    is_approved = models.BooleanField(default=False, verbose_name='Tasdiqlangan')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Izoh'
        verbose_name_plural = 'Izohlar'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user} → {self.movie}: {self.text[:40]}'


class Slider(models.Model):
    """Bosh sahifa slider"""
    title = models.CharField(max_length=200, verbose_name='Sarlavha')
    subtitle = models.CharField(max_length=300, blank=True, verbose_name='Kichik sarlavha')
    image = models.ImageField(upload_to='sliders/', verbose_name='Rasm')
    movie = models.ForeignKey(
        Movie, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='sliders', verbose_name='Kino'
    )
    link = models.URLField(blank=True, verbose_name='Havola')
    order = models.PositiveIntegerField(default=0, verbose_name='Tartib')
    is_active = models.BooleanField(default=True, verbose_name='Faol')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Slider'
        verbose_name_plural = 'Sliderlar'
        ordering = ['order']

    def __str__(self):
        return self.title


class Season(models.Model):
    """Serial mavsumlari"""
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='seasons', verbose_name='Serial')
    number = models.PositiveIntegerField(verbose_name='Mavsum raqami')
    title = models.CharField(max_length=200, blank=True, verbose_name='Nomi')
    poster = models.ImageField(upload_to='seasons/', null=True, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Mavsum'
        verbose_name_plural = 'Mavzumlar'
        ordering = ['number']
        unique_together = ['movie', 'number']

    def __str__(self):
        return f'{self.movie.title} — {self.number}-mavsum'


class Episode(models.Model):
    """Qismlar"""
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episodes', verbose_name='Mavsum')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='episodes', verbose_name='Kino')
    number = models.PositiveIntegerField(verbose_name='Qism raqami')
    title = models.CharField(max_length=255, verbose_name='Nomi')
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='episode_thumbs/', null=True, blank=True)
    video_url = models.URLField(verbose_name='Video URL')
    duration = models.PositiveIntegerField(null=True, blank=True, verbose_name='Davomiylik (daqiqa)')
    is_free = models.BooleanField(default=True, verbose_name='Bepul')
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Qism'
        verbose_name_plural = 'Qismlar'
        ordering = ['season__number', 'number']
        unique_together = ['season', 'number']

    def __str__(self):
        return f'{self.movie.title} S{self.season.number}E{self.number} — {self.title}'


class Like(models.Model):
    """Kino like/dislike"""
    LIKE = 'like'
    DISLIKE = 'dislike'
    TYPE_CHOICES = [(LIKE, 'Like'), (DISLIKE, 'Dislike')]

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='user_likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['movie', 'user']
        verbose_name = 'Like'
        verbose_name_plural = 'Likelar'
