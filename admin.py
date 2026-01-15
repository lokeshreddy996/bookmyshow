from django.contrib import admin
from .models import Movie, Booking


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'language', 'format', 'rating', 'is_now_showing')
    list_filter = ('genre', 'language', 'format', 'is_now_showing')
    search_fields = ('title', 'description')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'customer_name', 'customer_email', 'booked_at', 'seats', 'total_amount')
    list_filter = ('booked_at', 'movie')
    search_fields = ('customer_name', 'customer_email')
