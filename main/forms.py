from django import forms  
from django.contrib.auth.models import User  
from django.contrib.auth.forms import UserCreationForm  
from django.core.exceptions import ValidationError  

class UserRegisterForm(UserCreationForm):
    role_choice = (
        ('admin', 'Admin'),
        ('user', 'Member'),
    )

    role = forms.ChoiceField(choices=role_choice, widget=forms.Select())
    username = forms.CharField(max_length=30, required=True, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    
    class Meta:
        model = User
        fields = ['username', 'role', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists')
        return username
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Passwords do not match')

        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)  # Create a user instance without saving
        user.is_staff = (self.cleaned_data['role'] == 'admin')
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user
