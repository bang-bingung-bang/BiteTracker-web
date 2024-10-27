from django.db import models

class Product(models.Model):
    CALORIE_CHOICES = [
        ('HIGH', 'Tinggi'),
        ('LOW', 'Rendah'),
    ]
    
    VEGAN_CHOICES = [
        ('VEGAN', 'Vegan'),
        ('NON_VEGAN', 'Non-vegan'),
    ]
    
    SUGAR_CHOICES = [
        ('HIGH', 'Tinggi'),
        ('LOW', 'Rendah'),
    ]

    STORE_CHOICES = [
        ('QITA_MART', 'QITA MART, Jl. K.H.M. Usman No.38, Kukusan, Kecamatan Beji, Kota Depok, Jawa Barat 16425'),
        ('TUTUL_V_MARKET', 'Tutul V Market, Jl. Margonda No.358, Kemiri Muka, Kecamatan Beji, Kota Depok, Jawa Barat 16423'),
        ('AL_HIKAM_MART', 'Al Hikam Mart, Jl. H. Amat No.21, Kukusan, Kecamatan Beji, Kota Depok, Jawa Barat 16425'),
        ('SNACK_JAYA_MARKET', 'Snack Jaya Market, Jl. Cagar Alam Sel. No.60, RT.01/RW.02, Pancoran MAS, Kec. Pancoran Mas, Kota Depok, Jawa Barat 16436'),
        ('BELANDA_MART', 'Belanda Mart, Jl. Tole Iskandar No.3, Mekar Jaya, Kec. Sukmajaya, Kota Depok, Jawa Barat 16411'),
    ]

    store = models.CharField(max_length=20, choices=STORE_CHOICES)
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.TextField()
    calories = models.IntegerField()
    calorie_tag = models.CharField(max_length=4, choices=CALORIE_CHOICES)
    vegan_tag = models.CharField(max_length=9, choices=VEGAN_CHOICES)
    sugar_tag = models.CharField(max_length=4, choices=SUGAR_CHOICES)
    image = models.URLField(max_length=500, default="https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_store_display(self):
        return dict(self.STORE_CHOICES)[self.store]

    def get_image_url(self):
        if self.image:
            return self.image
        return f"https://placehold.co/400x300?text={self.name.replace(' ', '+')}"
    
    def __str__(self):
        return f"{self.name} - {self.get_store_display()}"

    class Meta:
        ordering = ['store', 'name']