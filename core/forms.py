from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Booking, Service


class SignUpForm(UserCreationForm):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('provider', 'Service Provider'),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )   

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'avatar']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }
        
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_date']
        widgets = {
            # This widget creates the date/time picker input
            'booking_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local', 
                'class': 'form-control',
                'placeholder': 'dd-mm-yyyy --:-- --'
            }),
        }
        labels = {
            'booking_date': 'Select Date and Time',
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'category', 'price', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control glass-input', 'placeholder': 'e.g. AC Gas Refilling'}),
            'price': forms.NumberInput(attrs={'class': 'form-control glass-input', 'placeholder': 'Price in ₹'}),
            'description': forms.Textarea(attrs={'class': 'form-control glass-input', 'rows': 4}),
        }