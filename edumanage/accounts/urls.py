from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

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
    path('events/', views.event_list, name='event_list'),
    path('events/add/', views.event_add, name='event_add'),
    path('events/edit/<int:event_id>/', views.event_edit, name='event_edit'),
    path('events/delete/<int:event_id>/', views.event_delete, name='event_delete'),
    path('fee/', views.fee_list, name='fee'),
    path('fee/add/', views.fee_add, name='fee_add'),
    path('fee/edit/<int:fee_id>/', views.fee_edit, name='fee_edit'),
    path('fee/delete/<int:fee_id>/', views.fee_delete, name='fee_delete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
