from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import RegisterForm
from .models import User, SchoolRegistration
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Student
from .forms import StudentForm  # Create this form for the Student model
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.http import JsonResponse

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


