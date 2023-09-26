from django.urls import path

from user import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
<<<<<<< Updated upstream
=======
    path('logout/', views.user_logout, name='logout'),
    path('detail/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
>>>>>>> Stashed changes
]
