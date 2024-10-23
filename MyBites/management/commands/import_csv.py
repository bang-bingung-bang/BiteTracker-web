import csv
from django.core.management.base import BaseCommand
from MyBites.models import Product

class Command(BaseCommand):
    help = 'Import products from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **options):
        with open(options['file_path'], 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                product = Product(
                    nama_toko_lokasi=row['Nama Toko + Lokasi'].strip(), 
                    nama_product=row['Nama Produk'].strip(),          
                    harga=row['Harga'].strip(),                   
                    deskripsi=row['Deskripsi Produk'].strip(),    
                    kalori=row['Jumlah Kalori'].strip(),           
                    tag_kalori=row['Tag Kalori'].strip(),           
                    tag_vegan=row['Tag Vegan'].strip(),                 
                    tag_gula=row['Tag Gula'].strip(),                      
                )
                product.save()
                self.stdout.write(self.style.SUCCESS(f"Successfully imported {product.nama_product}"))