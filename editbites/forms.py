from django import forms
from django.contrib.auth.models import User
from .models import Product

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            }
        )
    )

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            }
        )
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm Password'
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            })
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['store', 'name', 'price', 'description', 'calories', 
                 'calorie_tag', 'vegan_tag', 'sugar_tag', 'image']
        labels = {
            'store': 'Toko',
            'name': 'Nama Produk',
            'price': 'Harga',
            'description': 'Deskripsi',
            'calories': 'Jumlah Kalori',
            'calorie_tag': 'Tag Kalori',
            'vegan_tag': 'Tag Vegan',
            'sugar_tag': 'Tag Gula',
            'image': 'URL Gambar'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'store': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'calories': forms.NumberInput(attrs={'class': 'form-control'}),
            'calorie_tag': forms.Select(attrs={'class': 'form-control'}),
            'vegan_tag': forms.Select(attrs={'class': 'form-control'}),
            'sugar_tag': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/image.jpg'
            })
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise forms.ValidationError("Harga tidak boleh negatif")
        return price

    def clean_calories(self):
        calories = self.cleaned_data.get('calories')
        if calories < 0:
            raise forms.ValidationError("Kalori tidak boleh negatif")
        return calories