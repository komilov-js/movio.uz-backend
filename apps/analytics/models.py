from django.db import models
from django.conf import settings


class DailyStats(models.Model):
    """Kunlik statistika"""
    date = models.DateField(unique=True)
    total_views = models.PositiveIntegerField(default=0)
    unique_visitors = models.PositiveIntegerField(default=0)
    new_users = models.PositiveIntegerField(default=0)
    total_searches = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Kunlik statistika'
        verbose_name_plural = 'Kunlik statistikalar'
        ordering = ['-date']

    def __str__(self):
        return str(self.date)


class SearchLog(models.Model):
    query = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    results_count = models.PositiveIntegerField(default=0)
    searched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-searched_at']
