from django.urls import path
from app_weather.views import weather_view

urlpatterns = [
    path('weather/', weather_view),
]
