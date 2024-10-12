from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # Existing route
    path('school_login/', views.school_login, name='school_login'),  # Route for school login
    path('student_login/', views.student_login, name='student_login'),  # Add this route for student login
    path('register/', views.register_school, name='register_school'),
    path('logout/', views.logout_view, name='logout'),
    path('school-details/', views.school_details, name='school_details'),
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_add, name='student_add'),
    path('students/edit/<int:student_id>/', views.student_edit, name='student_edit'),
    path('students/delete/<int:student_id>/', views.student_delete, name='student_delete'),
    path('forget-password/', views.forget_password, name='forget_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('export_students/', views.export_students, name='export_students'),
    path('faculty/', views.faculty_list, name='faculty_list'),
    path('faculty/add/', views.faculty_add, name='faculty_add'),
    path('faculty/<int:faculty_id>/edit/', views.faculty_edit, name='faculty_edit'),
    path('faculty/<int:faculty_id>/delete/', views.faculty_delete, name='faculty_delete'),
    path('export_faculties/', views.export_faculties, name='export_faculties'),

]
