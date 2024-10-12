from django import forms
from .models import Student
from .models import Faculty


class RegisterForm(forms.Form):
    ORGANIZATION_CHOICES = [
        ('school', 'School'),
        ('college', 'College'),
    ]
    
    COUNTRY_CHOICES = [
        ('', 'Select Country'),
        ('us', 'United States'),
        ('uk', 'United Kingdom'),
        ('in', 'India'),
        # Add more countries as needed
    ]
    
    school_name = forms.CharField(label='School/College Name', max_length=100)
    email = forms.EmailField(label='Email')
    phone = forms.CharField(label='Phone', max_length=15)
    address_area = forms.CharField(label='Area', max_length=100)
    address_landmark = forms.CharField(label='Landmark', max_length=100, required=False)
    address_city = forms.CharField(label='City', max_length=50)
    address_state = forms.CharField(label='State', max_length=50)
    address_country = forms.ChoiceField(label='Country', choices=COUNTRY_CHOICES)
    address_pincode = forms.CharField(label='Pincode', max_length=10)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    organization_type = forms.ChoiceField(label='Organization Type', choices=ORGANIZATION_CHOICES)
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match')

def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            return email.lower()  # Convert email to lowercase
        return email
    
    
class StudentForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))  # Input type=date for DOB

    class Meta:
        model = Student
        fields = ['name', 'email', 'number', 'fathers_name', 'dob', 'roll_no', 'student_class', 'section', 'fee']
        
        
class FacultyForm(forms.ModelForm):
    joining_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Faculty
        fields = ['emp_id', 'name', 'email', 'contact', 'subject', 'joining_date', 'salary']