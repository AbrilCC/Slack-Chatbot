from django.contrib import admin
from django.urls import path
from events.views import Events

# Here we define the url endpoints and what handler they use
urlpatterns = [
    path('', Events.as_view()), #as_view translates Django classes into an http function
]
