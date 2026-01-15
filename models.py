from django.db import models
from decimal import Decimal
from django.utils import timezone


class Movie(models.Model):
    GENRE_CHOICES = [
        ('Action', 'Action'),
        ('Comedy', 'Comedy'),
        ('Drama', 'Drama'),
        ('Thriller', 'Thriller'),
        ('Sci-Fi', 'Sci-Fi'),
        ('Horror', 'Horror'),
        ('Romance', 'Romance'),
        ('Adventure', 'Adventure'),
    ]

    LANGUAGE_CHOICES = [
        ('English', 'English'),
        ('Hindi', 'Hindi'),
        ('Telugu', 'Telugu'),
        ('Tamil', 'Tamil'),
        ('Kannada', 'Kannada'),
        ('Malayalam', 'Malayalam'),
    ]

    FORMAT_CHOICES = [
        ('2D', '2D'),
        ('3D', '3D'),
        ('IMAX', 'IMAX'),
        ('4DX', '4DX'),
    ]

    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, blank=True)
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, blank=True)
    duration = models.IntegerField(help_text="Duration in minutes", null=True, blank=True)
    rating = models.FloatField(default=0.0)
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='2D')
    trailer_url = models.URLField(blank=True)
    poster_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    release_date = models.DateField(null=True, blank=True)
    is_now_showing = models.BooleanField(default=True)

    class Meta:
        ordering = ['-release_date']

    def __str__(self):
        return self.title


class Booking(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100, blank=True, default='')
    customer_email = models.EmailField(blank=True, default='')
    booked_at = models.DateTimeField(auto_now_add=True)
    show_time = models.DateTimeField(null=True, blank=True)
    seats = models.CharField(max_length=100, blank=True, default='')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        display = self.customer_name or 'Guest'
        return f"{display} - {self.movie.title}"
