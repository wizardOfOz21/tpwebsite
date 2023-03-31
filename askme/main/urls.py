from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('tag/pog', views.listing, name='taglisting'),
    path('ask', views.ask, name='ask'),
]
