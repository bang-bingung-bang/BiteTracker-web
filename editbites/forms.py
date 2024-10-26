from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['store', 'name', 'price', 'description', 'calories', 
                 'calorie_tag', 'vegan_tag', 'sugar_tag', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }