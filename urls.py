from django.urls import path
from .views import home, book_ticket

urlpatterns = [
    path('', home, name='home'),
    path('book/<int:movie_id>/', book_ticket, name='book_ticket'),
]
