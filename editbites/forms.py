from django import forms
from .models import Product

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
            'image': 'Foto Produk'
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