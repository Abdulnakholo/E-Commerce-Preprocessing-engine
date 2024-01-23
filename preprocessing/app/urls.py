from django.urls import path

from .views import preprocessed


urlpatterns = [
    path('preprocessed/',preprocessed.as_view(), name='preprocessed'),
]