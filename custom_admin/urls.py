from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.admin_login, name="admin-login"),
    path("logout/", views.admin_logout, name="admin-logout"),
    path('admin_reset_password', views.admin_reset_password, name='admin_reset_password'),
    path("dashboard/", views.dashboard, name="admin-dashboard"),
    path('admin/profile/', views.admin_profile, name='admin_profile'),
    path("admin/change-password/", views.admin_change_password, name="admin_change_password"),
    path("students/", views.student_list, name="student-list"),
    path('admin/student/<int:pk>/delete/', views.delete_student, name='admin-delete-student'),
    path('admin/student/<int:pk>/', views.view_student, name='admin-view-student'),
    path('admin/student/<int:pk>/predict/', views.predict_student, name='admin-predict-student'),
    path('predictions/<str:period>/', views.prediction_list, name='predictions-list'),
    path('prediction/<int:pk>/', views.prediction_detail, name='prediction-detail'),
    path("courses/", views.course_list, name="course-list"),
    path("courses/add/", views.add_course, name="add-course"),
    path("courses/edit/<int:course_id>/", views.edit_course, name="edit-course"),
    path("courses/delete/<int:course_id>/", views.delete_course, name="delete-course"),
]
