from django.urls import path, include
from myauth import views

urlpatterns = [
    path('', views.register, name='register'),
    path('django/', include("django.contrib.auth.urls")),
    # path('profile', views.profile, name='profile')
]
