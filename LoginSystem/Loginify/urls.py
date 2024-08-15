from django.urls import path

from . import views

urlpatterns = [
    path('hello/', views.print),
    path('login/', views.login, name='login'),
    path('signup/', views.signup,  name='signup'),
    path('login/success', views.login_success,  name='login_success'),
    path('all-user-data/',views.all_user_data),
    path('single-user-data/<str:email>/',views.single_user_data),  
  
]