from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='home'),
    path('hot/', views.hot, name='hot'),
    path('tag/<str:tag_name>/', views.tag, name='tag'),
    path('question/<int:q_id>', views.question, name='question'),
    path('ask', views.ask, name='ask'),
    path('settings', views.settings, name='settings'),
    path('signup', views.signup, name='signup'),
    path('login', views.log_in, name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('vote/', views.vote, name='vote'),
]
