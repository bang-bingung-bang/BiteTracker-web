# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'category', 'image', 'excerpt']  # Tambahkan kolom 'image' sebagai URLField

    # Opsi untuk mengubah label 'image' menjadi 'Image URL' jika diinginkan
    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['image'].label = 'Image URL'

# Custom Form untuk User Registration
class CustomUserCreationForm(UserCreationForm):
    is_staff = forms.BooleanField(required=False, label="Daftar sebagai Admin", initial=False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'is_staff']
