from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.dateparse import parse_datetime
import json
from decimal import Decimal

from .models import Movie, Booking


def home(request):
    genre = request.GET.get('genre')
    language = request.GET.get('language')

    movies = Movie.objects.all()

    if genre:
        movies = movies.filter(genre__iexact=genre)

    if language:
        movies = movies.filter(language__iexact=language)

    return render(request, 'home.html', {'movies': movies})


@require_http_methods(["GET", "POST"])
def book_ticket(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        # Accept JSON or form submissions
        try:
            data = json.loads(request.body.decode()) if request.body else request.POST
        except Exception:
            data = request.POST

        customer_name = data.get('customer_name', '')
        customer_email = data.get('customer_email', '')
        seats = data.get('seats', '')
        total_amount = data.get('total_amount', '0.00')
        show_time_raw = data.get('show_time')

        show_time = None
        if show_time_raw:
            show_time = parse_datetime(show_time_raw) or None

        try:
            total_amount = Decimal(str(total_amount))
        except Exception:
            total_amount = Decimal('0.00')

        booking = Booking.objects.create(
            movie=movie,
            customer_name=customer_name,
            customer_email=customer_email,
            seats=seats,
            total_amount=total_amount,
            show_time=show_time,
        )

        # send confirmation email when provided
        if customer_email:
            try:
                send_mail(
                    subject='Ticket Booking Confirmation',
                    message=f'Your ticket for "{movie.title}" has been booked successfully! Seats: {seats}',
                    from_email='noreply@bookmyshow.com',
                    recipient_list=[customer_email],
                    fail_silently=True,
                )
            except Exception:
                pass

        return JsonResponse({'status': 'success', 'booking_id': booking.id})

    # GET fallback: simple text
    return HttpResponse(f"Booking endpoint for {movie.title}")
