# 🎬 Movio Backend — Django REST API

## Ishga tushirish

```bash
# 1. Virtual muhit yaratish
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 2. Kutubxonalarni o'rnatish
pip install -r requirements.txt

# 3. .env fayl yaratish
cp .env.example .env

# 4. Migratsiyalar
python manage.py makemigrations users kino analytics
python manage.py migrate

# 5. Superuser yaratish
python manage.py createsuperuser

# 6. Server ishga tushirish
python manage.py runserver
```

## API Endpointlar

### Auth (Ochiq)
| Method | URL | Vazifa |
|--------|-----|--------|
| POST | `/api/users/register/` | Ro'yxat |
| POST | `/api/users/login/` | Kirish (JWT) |
| POST | `/api/users/logout/` | Chiqish |
| POST | `/api/users/token/refresh/` | Token yangilash |
| GET/PATCH | `/api/users/profile/` | Profil |
| POST | `/api/users/change-password/` | Parol o'zgartirish |

### Kinolar (Ochiq)
| Method | URL | Vazifa |
|--------|-----|--------|
| GET | `/api/kino/categories/` | Kategoriyalar |
| GET | `/api/kino/movie-list/` | Kinolar ro'yxati |
| GET | `/api/kino/movie-list/{id}/` | Kino detali |
| GET | `/api/kino/movie-list/featured/` | Tanlangan kinolar |
| GET | `/api/kino/movie-list/top-rated/` | Top reyting |
| GET | `/api/kino/movie-list/most-viewed/` | Ko'p ko'rilgan |
| GET | `/api/kino/movie-list/new-releases/` | Yangi kinolar |
| GET | `/api/kino/movie-list/{id}/related/` | O'xshash kinolar |
| GET | `/api/kino/movie-list/year/{year}/` | Yil bo'yicha |
| GET | `/api/kino/categories/{id}/movies/` | Kategoriya kinolari |
| GET | `/api/kino/clips/` | Kliplar |
| GET | `/api/kino/clips/{id}/` | Klip detali |
| GET | `/api/kino/movie-list/{id}/clips/` | Kino kliplari |
| GET | `/api/kino/sliders/` | Sliderlar |
| GET | `/api/kino/search/?q=...` | Qidirish |
| GET | `/api/kino/genres/` | Janrlar |
| GET | `/api/kino/tags/` | Teglar |

### Saqlangan (Auth kerak)
| Method | URL | Vazifa |
|--------|-----|--------|
| GET/POST | `/api/kino/saved-movies/` | Saqlangan kinolar |
| DELETE | `/api/kino/saved-movies/{movie_id}/` | O'chirish |

### Izohlar (Auth kerak)
| Method | URL | Vazifa |
|--------|-----|--------|
| GET/POST | `/api/kino/movie-list/{id}/comments/` | Izohlar |
| DELETE | `/api/kino/comments/{id}/` | Izoh o'chirish |

### Admin — Kinolar (Staff kerak)
| Method | URL | Vazifa |
|--------|-----|--------|
| GET/POST | `/api/kino/admin/movies/` | CRUD |
| GET/PATCH/DELETE | `/api/kino/admin/movies/{id}/` | Detail |
| POST | `/api/kino/admin/movies/{id}/publish/` | Nashr |
| POST | `/api/kino/admin/movies/{id}/toggle-featured/` | Featured |
| GET | `/api/kino/admin/movies/stats/` | Statistika |
| GET/POST | `/api/kino/admin/categories/` | Kategoriyalar |
| GET/POST | `/api/kino/admin/clips/` | Kliplar |
| GET/POST | `/api/kino/admin/comments/` | Izohlar |
| POST | `/api/kino/admin/comments/{id}/approve/` | Tasdiqlash |
| GET/POST | `/api/kino/admin/sliders/` | Sliderlar |
| GET/POST | `/api/kino/admin/genres/` | Janrlar |
| GET/POST | `/api/kino/admin/tags/` | Teglar |

### Admin — Foydalanuvchilar (Staff kerak)
| Method | URL | Vazifa |
|--------|-----|--------|
| GET | `/api/users/admin/users/stats/` | Statistika |
| GET/POST | `/api/users/admin/users/` | Ro'yxat |
| GET/PATCH/DELETE | `/api/users/admin/users/{id}/` | Detail |
| POST | `/api/users/admin/users/{id}/toggle-active/` | Faol/Blok |
| POST | `/api/users/admin/users/{id}/toggle-premium/` | Premium |

### Analitika (Staff kerak)
| Method | URL | Vazifa |
|--------|-----|--------|
| GET | `/api/analytics/dashboard/` | Dashboard stats |
| GET | `/api/analytics/views-chart/?days=30` | Ko'rishlar grafigi |
| GET | `/api/analytics/top-movies/` | Top kinolar |
| GET | `/api/analytics/user-growth/` | User o'sishi |
| GET | `/api/analytics/category-stats/` | Kategoriya stats |

## API Docs
- Swagger UI: `http://127.0.0.1:8000/api/docs/`
- ReDoc: `http://127.0.0.1:8000/api/redoc/`

## Filter parametrlar (kinolar)
```
?search=avatar         # Qidirish
?category=1            # Kategoriya ID
?status=published      # Holat
?year_min=2020         # Yil (min)
?year_max=2024         # Yil (max)
?rating_min=7          # Reyting (min)
?quality=HD            # Sifat
?ordering=-views       # Saralash
?page=2                # Sahifa
```
