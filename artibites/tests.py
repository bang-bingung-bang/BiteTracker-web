from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Article

class ArtibitesTestCase(TestCase):
    def setUp(self):
        # Membuat pengguna admin
        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpass123',
            is_staff=True
        )

        # Membuat pengguna biasa
        self.regular_user = User.objects.create_user(
            username='user',
            password='userpass123',
            is_staff=False
        )

        # Membuat artikel untuk pengujian
        self.article = Article.objects.create(
            title="Test Article",
            content="This is a test article.",
            excerpt="Test excerpt",
        )

        self.client = Client()

    def test_article_list_access_admin(self):
        # Login sebagai admin
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('artibites:article_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'article_list.html')  # Perbaikan nama template
        # Memastikan teks "Tambah Artikel Baru" muncul untuk admin
        self.assertContains(response, 'Tambah Artikel Baru', msg_prefix="Admin tidak melihat tombol 'Tambah Artikel Baru'")

    def test_article_list_access_user(self):
        # Login sebagai pengguna biasa
        self.client.login(username='user', password='userpass123')
        response = self.client.get(reverse('artibites:article_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'article_list.html')  # Perbaikan nama template
        # Memastikan tombol "Tambah Artikel Baru" tidak muncul untuk pengguna biasa
        self.assertNotContains(response, 'Tambah Artikel Baru', msg_prefix="Pengguna biasa dapat melihat tombol 'Tambah Artikel Baru'")

    def test_article_detail_view(self):
        # Mengakses detail artikel
        response = self.client.get(reverse('artibites:article_detail', args=[self.article.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'article_detail.html')  # Perbaikan nama template
        # Memastikan judul artikel muncul di halaman detail
        self.assertContains(response, self.article.title, msg_prefix="Detail artikel tidak memuat judul yang benar")

    def test_add_article_admin(self):
        # Login sebagai admin
        self.client.login(username='admin', password='adminpass123')
        
        # Data untuk artikel baru
        data = {
            'title': 'New Article',
            'content': 'This is new content',
            'excerpt': 'New excerpt',
        }
        
        # Mengirimkan permintaan POST untuk menambah artikel
        response = self.client.post(reverse('artibites:add_article'), data, follow=True)
        
        # Periksa apakah respons statusnya 200
        self.assertEqual(response.status_code, 200, "Respons tidak berhasil dengan status 200")
 
