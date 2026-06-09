from django.urls import path
from . import views

urlpatterns = [
    # ─── Public: Categories ───────────────────────────────────────────────────
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:category_id>/movies/', views.MoviesByCategoryView.as_view(), name='category-movies'),

    # ─── Public: Genres & Tags ────────────────────────────────────────────────
    path('genres/', views.GenreListView.as_view(), name='genre-list'),
    path('tags/', views.TagListView.as_view(), name='tag-list'),

    # ─── Public: Movies ───────────────────────────────────────────────────────
    path('movie-list/', views.MovieListView.as_view(), name='movie-list'),
    path('movie-list/featured/', views.FeaturedMoviesView.as_view(), name='featured-movies'),
    path('movie-list/top-rated/', views.TopRatedMoviesView.as_view(), name='top-rated'),
    path('movie-list/most-viewed/', views.MostViewedMoviesView.as_view(), name='most-viewed'),
    path('movie-list/new-releases/', views.NewReleasesView.as_view(), name='new-releases'),
    path('movie-list/year/<int:year>/', views.MoviesByYearView.as_view(), name='movies-by-year'),
    path('movie-list/<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),
    path('movie-list/<int:pk>/related/', views.RelatedMoviesView.as_view(), name='related-movies'),
    path('movie-list/<int:movie_id>/clips/', views.MovieClipsView.as_view(), name='movie-clips'),
    path('movie-list/<int:movie_id>/comments/', views.MovieCommentListView.as_view(), name='movie-comments'),
    path('movie-list/<int:movie_id>/seasons/', views.MovieSeasonsView.as_view(), name='movie-seasons'),
    path('movie-list/<int:pk>/like/', views.MovieLikeView.as_view(), name='movie-like'),
    path('movie-list/<int:pk>/like-status/', views.MovieLikeStatusView.as_view(), name='movie-like-status'),

    # ─── Public: Clips ────────────────────────────────────────────────────────
    path('clips/', views.ClipListView.as_view(), name='clip-list'),
    path('clips/<int:pk>/', views.ClipDetailView.as_view(), name='clip-detail'),

    # ─── Public: Seasons & Episodes ───────────────────────────────────────────
    path('seasons/<int:season_id>/episodes/', views.SeasonEpisodesView.as_view(), name='season-episodes'),
    path('episodes/<int:pk>/', views.EpisodeDetailView.as_view(), name='episode-detail'),

    # ─── Public: Comments ─────────────────────────────────────────────────────
    path('comments/<int:pk>/', views.CommentDeleteView.as_view(), name='comment-delete'),

    # ─── Public: SavedMovies ──────────────────────────────────────────────────
    path('saved-movies/', views.SavedMovieListView.as_view(), name='saved-movie-list'),
    path('saved-movies/<int:movie_id>/', views.SavedMovieDeleteView.as_view(), name='saved-movie-delete'),

    # ─── Public: Sliders ──────────────────────────────────────────────────────
    path('sliders/', views.SliderListView.as_view(), name='slider-list'),

    # ─── Public: Search ───────────────────────────────────────────────────────
    path('search/', views.SearchView.as_view(), name='search'),

    # ─── Admin: Categories ────────────────────────────────────────────────────
    path('admin/categories/', views.AdminCategoryListView.as_view(), name='admin-category-list'),
    path('admin/categories/<int:pk>/', views.AdminCategoryDetailView.as_view(), name='admin-category-detail'),

    # ─── Admin: Genres & Tags ─────────────────────────────────────────────────
    path('admin/genres/', views.AdminGenreListView.as_view(), name='admin-genre-list'),
    path('admin/genres/<int:pk>/', views.AdminGenreDetailView.as_view(), name='admin-genre-detail'),
    path('admin/tags/', views.AdminTagListView.as_view(), name='admin-tag-list'),
    path('admin/tags/<int:pk>/', views.AdminTagDetailView.as_view(), name='admin-tag-detail'),

    # ─── Admin: Movies ────────────────────────────────────────────────────────
    path('admin/movies/', views.AdminMovieListView.as_view(), name='admin-movie-list'),
    path('admin/movies/stats/', views.AdminMovieStatsView.as_view(), name='admin-movie-stats'),
    path('admin/movies/<int:pk>/', views.AdminMovieDetailView.as_view(), name='admin-movie-detail'),
    path('admin/movies/<int:pk>/publish/', views.AdminMoviePublishView.as_view(), name='admin-movie-publish'),
    path('admin/movies/<int:pk>/toggle-featured/', views.AdminMovieToggleFeaturedView.as_view(), name='admin-movie-featured'),

    # ─── Admin: Clips ─────────────────────────────────────────────────────────
    path('admin/clips/', views.AdminClipListView.as_view(), name='admin-clip-list'),
    path('admin/clips/<int:pk>/', views.AdminClipDetailView.as_view(), name='admin-clip-detail'),

    # ─── Admin: Comments ──────────────────────────────────────────────────────
    path('admin/comments/', views.AdminCommentListView.as_view(), name='admin-comment-list'),
    path('admin/comments/<int:pk>/', views.AdminCommentDetailView.as_view(), name='admin-comment-detail'),
    path('admin/comments/<int:pk>/approve/', views.AdminCommentApproveView.as_view(), name='admin-comment-approve'),

    # ─── Admin: Sliders ───────────────────────────────────────────────────────
    path('admin/sliders/', views.AdminSliderListView.as_view(), name='admin-slider-list'),
    path('admin/sliders/<int:pk>/', views.AdminSliderDetailView.as_view(), name='admin-slider-detail'),

    # ─── Admin: Seasons & Episodes ────────────────────────────────────────────
    path('admin/seasons/', views.AdminSeasonListView.as_view(), name='admin-season-list'),
    path('admin/seasons/<int:pk>/', views.AdminSeasonDetailView.as_view(), name='admin-season-detail'),
    path('admin/episodes/', views.AdminEpisodeListView.as_view(), name='admin-episode-list'),
    path('admin/episodes/<int:pk>/', views.AdminEpisodeDetailView.as_view(), name='admin-episode-detail'),
]
