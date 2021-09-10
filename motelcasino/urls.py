from django.urls import path
from . import views

urlpatterns = [
    path('rooms_available/', views.rooms_available, name="rooms_available")

]
