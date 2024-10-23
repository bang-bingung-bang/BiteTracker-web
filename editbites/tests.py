from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product

class EditBitesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.product = Product.objects.create(
            store='QITA_MART',
            name='Test Product',
            price=10000,
            description='Test Description',
            calories=100,
            calorie_tag='LOW',
            vegan_tag='VEGAN',
            sugar_tag='LOW'
        )

    def test_main_page(self):
        response = self.client.get(reverse('editbites:main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')

    def test_admin_dashboard_requires_login(self):
        response = self.client.get(reverse('editbites:admin_dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_admin_dashboard_with_login(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('editbites:admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'editbites/admin_dashboard.html')