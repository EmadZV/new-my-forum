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
    path('tag_detail/<slug:tag>/', views.tag_detail, name='tag_detail'),

    path('post-status/<int:post_id>/<int:status_value>', views.post_status, name='post_status'),
    # path('answer_status/<int:answer_id>/<int:answer_status_value>', views.answer_status, name='answer_status'),
    path('post-vote/<int:post_id>/<int:vote_value>/', views.vote_post, name='vote_post'),
    path('user-vote/<int:user_id>/<int:vote_value>/', views.vote_user, name='vote_user'),
    path('answer-vote/<int:answer_id>/<int:vote_value>/', views.vote_answer, name='vote_answer'),
]
