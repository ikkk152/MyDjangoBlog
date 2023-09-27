from django.urls import path

from user import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('register/code/', views.SendCode.as_view(), name='send_code'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('detail/<int:pk>/', views.UserProfile.as_view(), name='user_detail'),
]
