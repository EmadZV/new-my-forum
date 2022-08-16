from django.urls import path

# import myauth
from . import views

app_name = 'mycontent'
urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('newpost/', views.post_create, name='newpost'),
    # path('profile/', myauth.views.profile, name='profile'),
    path('post-list/', views.post_list, name='post_list'),
    path('post-detail', views.post_detail, name='post_detail')
    # <str:new_answer>
]
