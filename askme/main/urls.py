from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('hot/', views.hot, name='hot'),
    path('tag/<str:tname>/', views.tag, name='tag'),
    path('question/<int:qid>', views.question, name='question'),
    path('ask', views.ask, name='ask'),
    path('settings', views.settings, name='settings'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
]
