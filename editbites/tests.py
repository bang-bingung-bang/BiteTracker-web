from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product
import json

class EditBitesTest(TestCase):
    def setUp(self):
        # Create admin user
        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpass123',
            is_staff=True
        )
        
        # Create regular user
        self.regular_user = User.objects.create_user(
            username='regular',
            password='userpass123',
            is_staff=False
        )
        
        # Create test product
        self.product = Product.objects.create(
            store='QITA_MART',
            name='Test Product',
            price=10000,
            description='Test Description',
            calories=100,
            calorie_tag='HIGH',
            sugar_tag='LOW',
            vegan_tag='VEGAN'
        )
        
        self.client = Client()

    def test_product_list_admin(self):
        # Login as admin
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('editbites:product_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'editbites/product_list.html')
        self.assertTrue(response.context['is_admin'])
        self.assertContains(response, 'Add Product')

    def test_product_list_user(self):
        # Login as regular user
        self.client.login(username='regular', password='userpass123')
        response = self.client.get(reverse('editbites:product_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'editbites/product_list.html')
        self.assertFalse(response.context['is_admin'])
        self.assertNotContains(response, 'Add Product')

    def test_product_list_filter(self):
        self.client.login(username='regular', password='userpass123')
        
        # Test each filter
        filters = ['high_calories', 'high_sugar', 'low_calorie', 
                  'low_sugar', 'non_vegan', 'vegan']
        
        for filter_param in filters:
            response = self.client.get(f"{reverse('editbites:product_list')}?filter={filter_param}")
            self.assertEqual(response.status_code, 200)

    def test_product_detail(self):
        self.client.login(username='regular', password='userpass123')
        response = self.client.get(
            reverse('editbites:product_detail', args=[self.product.pk])
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'editbites/product_detail.html')
        self.assertEqual(response.context['product'], self.product)

    def test_create_product_admin(self):
        self.client.login(username='admin', password='adminpass123')
        
        data = {
            'store': 'QITA_MART',
            'name': 'New Product',
            'price': '15000',
            'description': 'New Description',
            'calories': '150',
            'calorie_tag': 'HIGH',
            'sugar_tag': 'LOW',
            'vegan_tag': 'VEGAN',
            'image': 'https://example.com/image.jpg'
        }
        
        response = self.client.post(reverse('editbites:create_product'), data, follow=True)
        messages = list(response.context.get('messages', []))
        
        self.assertTrue(Product.objects.filter(name='New Product').exists())
        self.assertTrue(any(message.message == 'Product created successfully!' for message in messages))
        new_product = Product.objects.get(name='New Product')
        self.assertEqual(new_product.price, 15000)
        self.assertEqual(new_product.calories, 150)

    def test_create_product_invalid_data(self):
        self.client.login(username='admin', password='adminpass123')
        
        data = {
            'name': 'Invalid Product',
            # Missing required fields
        }
        
        response = self.client.post(reverse('editbites:create_product'), data)
        self.assertEqual(response.status_code, 200)  # Stays on same page
        self.assertFalse(Product.objects.filter(name='Invalid Product').exists())

    def test_create_product_user(self):
        self.client.login(username='regular', password='userpass123')
        response = self.client.get(reverse('editbites:create_product'))
        self.assertEqual(response.status_code, 302)  # Redirect non-admin users

    def test_edit_product_admin(self):
        self.client.login(username='admin', password='adminpass123')
        
        data = {
            'store': 'AL_HIKAM_MART',
            'name': 'Updated Product',
            'price': '20000',
            'description': 'Updated Description',
            'calories': '200',
            'calorie_tag': 'HIGH',
            'sugar_tag': 'HIGH',
            'vegan_tag': 'VEGAN',
            'image': 'https://example.com/updated-image.jpg'
        }
        
        response = self.client.post(
            reverse('editbites:edit_product', args=[self.product.pk]),
            data,
            follow=True
        )
        
        messages = list(response.context.get('messages', []))
        updated_product = Product.objects.get(pk=self.product.pk)
        
        self.assertEqual(updated_product.name, 'Updated Product')
        self.assertEqual(updated_product.price, 20000)
        self.assertEqual(updated_product.calories, 200)
        self.assertTrue(any(message.message == 'Product updated successfully!' for message in messages))

    def test_edit_product_invalid_data(self):
        self.client.login(username='admin', password='adminpass123')
        
        data = {
            'name': 'Invalid Update',
            # Missing required fields
        }
        
        response = self.client.post(
            reverse('editbites:edit_product', args=[self.product.pk]),
            data
        )
        self.assertEqual(response.status_code, 200)  # Stays on same page
        updated_product = Product.objects.get(pk=self.product.pk)
        self.assertNotEqual(updated_product.name, 'Invalid Update')

    def test_edit_product_user(self):
        self.client.login(username='regular', password='userpass123')
        response = self.client.get(
            reverse('editbites:edit_product', args=[self.product.pk])
        )
        self.assertEqual(response.status_code, 302)  # Redirect non-admin users

    def test_delete_product_admin(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.post(
            reverse('editbites:delete_product', args=[self.product.pk])
        )
        
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

    def test_delete_product_user(self):
        self.client.login(username='regular', password='userpass123')
        response = self.client.post(
            reverse('editbites:delete_product', args=[self.product.pk])
        )
        self.assertEqual(response.status_code, 302)  # Redirect non-admin users
        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())  # Product should still exist

    def test_get_product_json(self):
        self.client.login(username='regular', password='userpass123')
        response = self.client.get(reverse('editbites:get_product_json'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content)
        self.assertTrue(len(data) > 0)

    def test_product_model_methods(self):
        product = Product.objects.get(pk=self.product.pk)
        
        # Test get_store_display
        self.assertEqual(
            product.get_store_display(),
            'QITA MART, Jl. K.H.M. Usman No.38, Kukusan, Kecamatan Beji, Kota Depok, Jawa Barat 16425'
        )
        
        # Test get_image_url with default image
        self.assertTrue(product.get_image_url().startswith('http'))
        
        # Test string representation
        self.assertEqual(
            str(product),
            f"{product.name} - {product.get_store_display()}"
        )

    def test_product_model_ordering(self):
        Product.objects.create(
            store='BELANDA_MART',
            name='AAA Product',
            price=5000,
            description='Test',
            calories=50,
            calorie_tag='LOW',
            sugar_tag='LOW',
            vegan_tag='VEGAN'
        )
        
        products = Product.objects.all()
        self.assertEqual(products[0].store, 'BELANDA_MART')  # Should come first alphabetically