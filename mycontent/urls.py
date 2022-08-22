from django.urls import path

# import myauth
from . import views

app_name = 'mycontent'
urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('newpost/', views.post_create, name='newpost'),
    # path('profile/', myauth.views.profile, name='profile'),
    path('post-list/', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    # <str:new_answer>
    path('tag_list/', views.tag_list, name='tag_list'),
    path('tag_detail/<slug:tag>/', views.tag_detail, name='tag_detail')

]
