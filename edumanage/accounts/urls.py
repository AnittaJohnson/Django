from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # Existing route
    path('school_login/', views.school_login, name='school_login'),  # Route for school login
    path('student_login/', views.student_login, name='student_login'),  # Add this route for student login
    path('forget-password/', views.forget_password, name='forget_password'),
    path('register/', views.register_school, name='register_school'),
    path('logout/', views.logout_view, name='logout'),
    path('school-details/', views.school_details, name='school_details'),
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_add, name='student_add'),
    path('students/edit/<int:student_id>/', views.student_edit, name='student_edit'),
    path('students/delete/<int:student_id>/', views.student_delete, name='student_delete'),

]