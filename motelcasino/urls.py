from django.urls import path
from . import views

urlpatterns = [
    path('rooms_available/', views.rooms_available, name="rooms_available"),
    path('book/', views.book, name="book"),
    path('rooms_booked/', views.rooms_booked, name="rooms_booked")
]
