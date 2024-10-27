# Generated by Django 5.1.2 on 2024-10-23 07:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sharebites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store', models.CharField(choices=[('QITA_MART', 'QITA MART, Jl. K.H.M. Usman No.38, Kukusan, Kecamatan Beji, Kota Depok, Jawa Barat 16425'), ('TUTUL_V_MARKET', 'Tutul V Market, Jl. Margonda No.358, Kemiri Muka, Kecamatan Beji, Kota Depok, Jawa Barat 16423'), ('AL_HIKAM_MART', 'Al Hikam Mart, Jl. H. Amat No.21, Kukusan, Kecamatan Beji, Kota Depok, Jawa Barat 16425'), ('SNACK_JAYA_MARKET', 'Snack Jaya Market, Jl. Cagar Alam Sel. No.60, RT.01/RW.02, Pancoran MAS, Kec. Pancoran Mas, Kota Depok, Jawa Barat 16436'), ('BELANDA_MART', 'Belanda Mart, Jl. Tole Iskandar No.3, Mekar Jaya, Kec. Sukmajaya, Kota Depok, Jawa Barat 16411')], max_length=20)),
                ('name', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
                ('description', models.TextField()),
                ('calories', models.IntegerField()),
                ('calorie_tag', models.CharField(choices=[('HIGH', 'Tinggi'), ('LOW', 'Rendah')], max_length=4)),
                ('vegan_tag', models.CharField(choices=[('VEGAN', 'Vegan'), ('NON_VEGAN', 'Non-vegan')], max_length=9)),
                ('sugar_tag', models.CharField(choices=[('HIGH', 'Tinggi'), ('LOW', 'Rendah')], max_length=4)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['store', 'name'],
            },
        ),
        migrations.AddField(
            model_name='sharebites',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sharebites.product'),
            preserve_default=False,
        ),
    ]
