from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    KALORI_CHOICES = [
        ('tinggi', 'Tinggi Kalori'),
        ('rendah', 'Rendah Kalori'),
    ]
    
    VEGAN_CHOICES = [
        ('vegan', 'Vegan'),
        ('non-vegan', 'Non-Vegan'),
    ]
    
    GULA_CHOICES = [
        ('tinggi', 'Tinggi Gula'),
        ('rendah', 'Rendah Gula'),
    ]

    # Store details
    nama_toko = models.CharField(max_length=255)
    nama_product = models.CharField(max_length=255)
    harga = models.IntegerField()
    deskripsi = models.TextField()
    
    # Tags with choices
    tag_kalori = models.CharField(max_length=6, choices=KALORI_CHOICES)
    tag_vegan = models.CharField(max_length=9, choices=VEGAN_CHOICES)
    tag_gula = models.CharField(max_length=6, choices=GULA_CHOICES)

    def __str__(self):
        return f"{self.nama_product} from {self.nama_toko}"

class MyBites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s wishlist: {self.product.nama_product}"
