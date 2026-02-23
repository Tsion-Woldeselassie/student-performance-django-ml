from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='student_register'),
    path('login/', views.student_login, name='student_login'),
    path('logout/', views.student_logout, name='student_logout'),
    path('profile/', views.student_profile, name='student_profile'),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path('predict/', views.predict_view, name='student_predict'),
    path("change-password/", views.change_password, name="change_password"),
    path('reset-password', views.reset_password, name='reset_password'),
     path("student/prediction-history/", views.student_prediction_history, name="student_prediction_history"),
    ]
    

  
