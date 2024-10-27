from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import ShareBites, Comment, Like

class ShareBitesViewTest(TestCase):
    def setUp(self):
        # Create a user for testing and log them in
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_show_main_view(self):
        # Create a post to test the main view
        ShareBites.objects.create(
            user=self.user,
            title='Post 1',
            content='Content 1',
            image='http://example.com/image1.jpg',
            calorie_content='low',
            sugar_content='low',
            diet_type='vegan',
        )
        response = self.client.get(reverse('sharebites:show_main'))
        # Check for a successful response
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Post 1')
        self.assertContains(response, 'http://example.com/image1.jpg')  
        self.assertContains(response, 'low') 
        self.assertContains(response, 'low') 
        self.assertContains(response, 'vegan')  

    def test_create_post_view(self):
        # Post data for creating a new ShareBites entry
        response = self.client.post(reverse('sharebites:create_post_sharebites'), {
            'title': 'New Post',
            'content': 'New Content',
            'image': 'http://example.com/new_image.jpg',
            'calorie_content': 'low',
            'sugar_content': 'low',
            'diet_type': 'vegan',
        })
        self.assertEqual(response.status_code, 302)  # Redirect setelah berhasil
        self.assertTrue(ShareBites.objects.filter(title='New Post').exists())
        self.assertEqual(response.content, 'New Content')  # Memeriksa konten
        self.assertEqual(response.image, 'http://example.com/new_image.jpg')  # Memeriksa gambar
        self.assertEqual(response.calorie_content, 'low')  # Memeriksa konten kalori
        self.assertEqual(response.sugar_content, 'low')  # Memeriksa kadar gula
        self.assertEqual(response.diet_type, 'vegan')  # Memeriksa jenis diet

    def test_delete_post_view(self):
        # Create a post for testing deletion
        post = ShareBites.objects.create(
            user=self.user,
            title='Post to Delete',
            content='Content to Delete',
            image='http://example.com/delete_image.jpg',
            calorie_content='low',
            sugar_content='low',
            diet_type='vegan',
        )
        response = self.client.post(reverse('sharebites:delete_post', args=[post.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect setelah berhasil
        self.assertFalse(ShareBites.objects.filter(pk=post.pk).exists())

class CommentModelTest(TestCase):
    def setUp(self):
        # Create a user and a post for testing comment functionality
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = ShareBites.objects.create(
            user=self.user,
            title='Test Post',
            content='This is a test post.',
            image='http://example.com/image.jpg',
            calorie_content='low',
            sugar_content='low',
            diet_type='vegan',
        )
        # Create a comment on the post
        self.comment = Comment.objects.create(
            post=self.post,
            user=self.user,
            content='This is a test comment.'
        )

    # Test comment is created successfully
    def test_comment_creation(self):
        self.assertEqual(self.comment.content, 'This is a test comment.')
    # Test relationship between comment & post
    def test_comment_post_relation(self):
        self.assertEqual(self.comment.post, self.post)

class LikeModelTest(TestCase):
    def setUp(self):
        # Create a user and a post for testing like functionality
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = ShareBites.objects.create(
            user=self.user,
            title='Test Post',
            content='This is a test post.',
            image='http://example.com/image.jpg',
            calorie_content='low',
            sugar_content='low',
            diet_type='vegan',
        ) # Create a like for the post
        self.like = Like.objects.create(post=self.post, user=self.user)

    #Test that like is created successfully
    def test_like_creation(self):
        self.assertEqual(self.like.post, self.post)
    # Test the relationship between like and user
    def test_like_user_relation(self):
        self.assertEqual(self.like.user, self.user)

class ShareBitesViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.post = ShareBites.objects.create(
            user=self.user,
            title='Test Post',
            content='This is a test post.',
            image='http://example.com/image.jpg',
            calorie_content='low',
            sugar_content='low',
            diet_type='vegan',
        )

    # Test that a new comment can be created.
    def test_create_comment_view(self):
        response = self.client.post(reverse('sharebites:add_comment', args=[self.post.pk]), {
            'content': 'This is a new comment.'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Comment.objects.filter(content='This is a new comment.').exists())

    # Test that a new like can be created.
    def test_like_post_view(self):
        response = self.client.post(reverse('sharebites:like_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Like.objects.filter(post=self.post, user=self.user).exists())

    # Test that a like can be deleted by its owner.
    def test_unlike_post_view(self):
        like = Like.objects.create(post=self.post, user=self.user)
        response = self.client.post(reverse('sharebites:like_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertFalse(Like.objects.filter(pk=like.pk).exists())
    
    # Test AJAX request for liking a post.
    def test_ajax_like_post_view(self):
        response = self.client.post(reverse('sharebites:like_post', args=[self.post.pk]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'liked': True,
            'likes_count': self.post.likes.count()
        })