import csv
from django.core.management.base import BaseCommand
from MyBites.models import Product

class Command(BaseCommand):
    help = 'Import CSV data into the database'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **options):
        file_path = options['file_path']
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if not row['Nama Toko + Lokasi']:
                    self.stdout.write(self.style.WARNING(f"Skipping entry due to empty 'Nama Toko + Lokasi': {row['Nama Produk']}"))
                    continue

                price = row['Harga'].replace('Rp', '').replace('£', '').replace('.', '').strip()
                try:
                    price = int(price)
                except ValueError:
                    self.stdout.write(self.style.ERROR(f"Invalid price format for {row['Nama Produk']}: {row['Harga']}"))
                    continue

                Product.objects.create(
                    nama_toko=row['Nama Toko + Lokasi'],
                    nama_product=row['Nama Produk'],
                    harga=price,
                    deskripsi=row['Deskripsi Produk'],
                    tag_kalori=row['Tag Kalori'],
                    tag_vegan=row['Tag Vegan'],
                    tag_gula=row['Tag Gula'],
                )
                self.stdout.write(self.style.SUCCESS(f"Imported {row['Nama Produk']}"))
