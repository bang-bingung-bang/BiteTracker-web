from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product

class EditbitesTests(TestCase):
    def setUp(self):
        # Create test users
        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpass123',
            is_staff=True
        )
        self.member_user = User.objects.create_user(
            username='member',
            password='memberpass123',
            is_staff=False
        )
        
        # Create test product
        self.product = Product.objects.create(
            store='Test Store',
            name='Test Product',
            price=10000,
            description='Test Description',
            calories=100,
            calorie_tag='LOW',
            vegan_tag='VEGAN',
            sugar_tag='LOW',
            image='https://example.com/image.jpg'
        )
        
        self.client = Client()

    def test_product_list_view(self):
        # Test member access
        self.client.login(username='member', password='memberpass123')
        response = self.client.get(reverse('editbites:product_list'))
        self.assertEqual(response.status_code, 200)
        
        # Test admin access
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('editbites:product_list'))
        self.assertEqual(response.status_code, 200)

    def test_create_product(self):
        # Test member access (should be denied)
        self.client.login(username='member', password='memberpass123')
        response = self.client.get(reverse('editbites:create_product'))
        self.assertEqual(response.status_code, 403)
        
        # Test admin access
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('editbites:create_product'))
        self.assertEqual(response.status_code, 200)