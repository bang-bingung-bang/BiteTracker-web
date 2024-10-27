from django.test import TestCase
from django.contrib.auth.models import User
from MyBites.models import Product, MyBites
from django.urls import reverse

class MyBitesTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.product = Product.objects.create(
            store='QITA_MART',  
            name='Test Product',
            price=10000,
            description='Test Description',
            calories=200,
            calorie_tag='LOW',  
            vegan_tag='VEGAN', 
            sugar_tag='LOW'     
        )

        self.client.login(username='testuser', password='testpassword')


    def test_add_to_wishlist_logged_in(self):
        response = self.client.post(reverse('MyBites:add_to_wishlist', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after adding
        self.assertTrue(MyBites.objects.filter(user=self.user, product=self.product).exists())

    def test_view_wishlist_logged_in(self):
        MyBites.objects.create(user=self.user, product=self.product)
        response = self.client.get(reverse('MyBites:wishlist'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')

    def test_remove_from_wishlist(self):
        MyBites.objects.create(user=self.user, product=self.product)
        response = self.client.post(reverse('MyBites:remove_from_wishlist', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(MyBites.objects.filter(user=self.user, product=self.product).exists())

    def test_show_main(self):
        response = self.client.get(reverse('main:show_main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')

    def test_show_json(self):
        response = self.client.get(reverse('MyBites:show_json'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')

    def test_show_xml(self):
        response = self.client.get(reverse('MyBites:show_xml'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
