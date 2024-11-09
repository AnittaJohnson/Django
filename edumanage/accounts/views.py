from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import RegisterForm
from .models import User, SchoolRegistration
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Student
from .forms import StudentForm  # Create this form for the Student model
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.http import JsonResponse
import openpyxl, os
from django.http import HttpResponse
from datetime import datetime
from .models import Faculty  # Ensure this import is correct
from .forms import FacultyForm
from .models import Event
from .forms import EventForm, FeeForm
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from .models import Fee
from django.utils import timezone
from datetime import datetime, timedelta
from django.views import View

User = get_user_model()

# Store OTPs temporarily in session or another method
def send_otp(email):
    otp = get_random_string(length=6, allowed_chars='0123456789')
    subject = "Password Reset OTP"
    message = f"Your OTP for password reset is {otp}"
    send_mail(subject, message, 'no-reply@edumanage.com', [email])
    return otp

def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            otp = send_otp(user.email)
            request.session['otp'] = otp
            request.session['email'] = email
            return JsonResponse({'status': 'otp_sent'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Email does not exist'})
    return render(request, 'accounts/forget_password.html')

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if entered_otp == request.session.get('otp'):
            return JsonResponse({'status': 'otp_verified'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid OTP'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def reset_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password == confirm_password:
            email = request.session.get('email')
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                return JsonResponse({'status': 'password_reset'})
            except User.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'User not found'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Passwords do not match'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def login_view(request):
    return render(request, 'accounts/login.html')

def school_login(request):
    if request.method == 'POST':
        email = request.POST.get('school_id').lower()
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('school_details')
        else:
            # Add an error message to be displayed in the template
            messages.error(request, 'Please check your email or password')
            return redirect('login')  # Redirect to login page to display the error message
    return render(request, 'accounts/login.html')

@login_required
def school_details(request):
    return render(request, 'accounts/school_login.html', {'user': request.user})
def student_login(request):
    if request.method == 'POST':
        # Process form data here
        pass
    return render(request, 'accounts/student_login.html')  


def register_school(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Extract cleaned data from form
            school_name = form.cleaned_data['school_name']
            email = form.cleaned_data['email'].lower()
            phone = form.cleaned_data['phone']
            address_area = form.cleaned_data['address_area']
            address_landmark = form.cleaned_data['address_landmark']
            address_city = form.cleaned_data['address_city']
            address_state = form.cleaned_data['address_state']
            address_country = form.cleaned_data['address_country']
            address_pincode = form.cleaned_data['address_pincode']
            password = form.cleaned_data['password']
            organization_type = form.cleaned_data['organization_type']

            # Check if the user already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'User already registered with this email!')
                return redirect('register_school')

            # Create a new user with additional fields
            user = User.objects.create_user(
                email=email,
                school_name=school_name,
                password=password
            )
            user.phone = phone
            user.address_area = address_area
            user.address_landmark = address_landmark
            user.address_city = address_city
            user.address_state = address_state
            user.address_country = address_country
            user.address_pincode = address_pincode
            user.organization_type = organization_type
            user.save()

            # Register school
            SchoolRegistration.objects.create(user=user)

            # Add a success message
            messages.success(request, 'Registered successfully!!')

           
    else:
        form = RegisterForm()

    return render(request, 'accounts/register_school.html', {'form': form})

@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect('login')



@login_required
def student_list(request):
    search_query = request.GET.get('search', '')
    students = Student.objects.filter(school=request.user)  # Filter by the logged-in school
    
    if search_query:
        students = students.filter(name__icontains=search_query)
        
    paginator = Paginator(students, 10)  
    page = request.GET.get('page')
    students_page = paginator.get_page(page)
    
    return render(request, 'accounts/student_list.html', {
        'students': students_page,
        'search_query': search_query
    })

@login_required
def student_add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.school = request.user  # Associate the student with the logged-in school
            student.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'accounts/student_form.html', {'form': form})

@login_required
def student_edit(request, student_id):
    student = get_object_or_404(Student, id=student_id, school=request.user)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'accounts/student_form.html', {'form': form})


@login_required
def student_delete(request, student_id):
    student = get_object_or_404(Student, id=student_id, school=request.user)
    student.delete()
    return redirect('student_list')



@login_required
def export_students(request):
    students = Student.objects.filter(school=request.user)
    school_name = request.user.school_name
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M")  # Use underscores for the filename

    # Create an in-memory workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f'Students_List_{school_name}'

    # Add the header row
    ws.append(['ID', 'Name', 'Email', 'Roll No.', 'Class', 'Section', 'Fee'])

    # Add student data rows
    for student in students:
        ws.append([
            student.id,
            student.name,
            student.email,
            student.roll_no,
            student.student_class,
            student.section,
            student.fee,
        ])

    # Prepare response to download the file
    file_name = f'Student_List_{school_name}_{current_datetime}.xlsx'  # Create the desired file name
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={file_name}'  # Set the filename in the response header

    wb.save(response)  # Save the workbook to the response
    return response


@login_required
def faculty_list(request):
    search_query = request.GET.get('search', '')
    
    if search_query:
        faculties = Faculty.objects.filter(name__icontains=search_query)
    else:
        faculties = Faculty.objects.all()

    # Pagination
    paginator = Paginator(faculties, 10)  # Show 10 faculties per page
    page_number = request.GET.get('page')
    faculties_page = paginator.get_page(page_number)

    return render(request, 'accounts/faculty_list.html', {
        'faculties': faculties_page,
        'search_query': search_query,
    })
    
    
@login_required
def faculty_add(request):
    if request.method == 'POST':
        form = FacultyForm(request.POST)
        if form.is_valid():
            faculty = form.save(commit=False)
            faculty.school = request.user
            faculty.save()
            return redirect('faculty_list')
    else:
        form = FacultyForm()
    return render(request, 'accounts/faculty_form.html', {'form': form})

@login_required
def faculty_edit(request, faculty_id):
    faculty = get_object_or_404(Faculty, id=faculty_id, school=request.user)
    if request.method == 'POST':
        form = FacultyForm(request.POST, instance=faculty)
        if form.is_valid():
            form.save()
            return redirect('faculty_list')
    else:
        form = FacultyForm(instance=faculty)
    return render(request, 'accounts/faculty_form.html', {'form': form, 'faculty': faculty})

@login_required
def faculty_delete(request, faculty_id):
    faculty = get_object_or_404(Faculty, id=faculty_id, school=request.user)
    faculty.delete()
    return redirect('faculty_list')


@login_required
def export_faculties(request):
    faculties = Faculty.objects.filter(school=request.user)
    school_name = request.user.school_name
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M")  # Use underscores for the filename

    # Create an in-memory workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f'Faculty_List_{school_name}'

    # Add the header row
    ws.append(['Employee ID', 'Name', 'Email', 'Contact', 'Subject', 'Salary'])

    # Add faculty data rows
    for faculty in faculties:
        ws.append([
            faculty.emp_id,
            faculty.name,
            faculty.email,
            faculty.contact,
            faculty.subject,
            faculty.salary,
        ])

    # Prepare response to download the file
    file_name = f'Faculty_List_{school_name}_{current_datetime}.xlsx'  # Create the desired file name
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={file_name}'  # Set the filename in the response header

    wb.save(response)  # Save the workbook to the response
    return response


@login_required
def event_list(request):
    search_query = request.GET.get('search', '')
    events = Event.objects.filter(school=request.user)

    if search_query:
        events = Event.objects.filter(details__icontains=search_query).order_by('-time')
    else:
        events = Event.objects.all().order_by('-time')
    
    paginator = Paginator(events, 5)
    page = request.GET.get('page')
    events_page = paginator.get_page(page)

    return render(request, 'accounts/event_list.html', {
        'events': events_page,
        'search_query': search_query,
    })

@login_required
def event_add(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.school = request.user
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'accounts/event_form.html', {'form': form})

@login_required
def event_edit(request, event_id):
    event = get_object_or_404(Event, id=event_id, school=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'accounts/event_form.html', {'form': form})

@login_required
def event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id, school=request.user)
    event.delete()
    return redirect('event_list')


@login_required
def fee_list(request):
    fees = Fee.objects.filter(student__school=request.user)  # Filter by the logged-in school
    return render(request, 'accounts/fee.html', {'fees': fees})

@login_required
@csrf_exempt
def fee_add(request):
    if request.method == 'POST':
        form = FeeForm(request.POST)
        if form.is_valid():
            fee = form.save(commit=False)
            fee.student.school = request.user  # Associate the fee with the logged-in school
            fee.save()
            return redirect('fee')
    else:
        form = FeeForm()
    return render(request, 'accounts/fee_form.html', {'form': form})

@login_required
def fee_edit(request, fee_id):
    fee = get_object_or_404(Fee, id=fee_id, student__school=request.user)
    if request.method == 'POST':
        form = FeeForm(request.POST, instance=fee)
        if form.is_valid():
            form.save()
            return redirect('fee')
    else:
        form = FeeForm(instance=fee)
    return render(request, 'accounts/fee_form.html', {'form': form})

@login_required
def fee_delete(request, fee_id):
    fee = get_object_or_404(Fee, id=fee_id, student__school=request.user)
    fee.delete()
    return redirect('fee')

def get_due_date():
    today = timezone.now()
    next_month = today.month % 12 + 1
    due_date = datetime(today.year + (today.month // 12), next_month, 5)
    return due_date

# In your view where you fetch the fees
fees = Fee.objects.all()
for fee in fees:
    fee.due_date = get_due_date()  # Set due date for each fee