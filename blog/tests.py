import email
from urllib import response
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from blog.models import Post

# Create your tests here.

class BlogTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='ukeme',
            email='ukeme@company.com',
            password='password'
        )
        self.post = Post.objects.create(
            title='my blog title',
            body='my blog content',
            author=self.user
        )

    def test_string_representation(self):
        self.assertEqual(str(self.post), 'my blog title')

    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), '/post/1/')

    def test_post_content(self):
        self.assertEqual(str(self.post.title), 'my blog title')
        self.assertEqual(str(self.post.body), 'my blog content')
        self.assertEqual(str(self.post.author), str(self.user))

    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'my blog content')
        self.assertTemplateUsed(response, 'home.html')

    def test_post_detail_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/100/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'my blog content')
        self.assertTemplateUsed(response, 'post_detail.html')

    def test_post_create_view(self):
        response = self.client.post(reverse('post_new'), {
            'title': 'New title',
            'author': self.user,
            'body': 'New content',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New title')
        self.assertContains(response, 'New content')

    def test_post_update_view(self):
        response = self.client.post(reverse('post_edit', args='1'), {
            'title': 'Updated title',
            'body': 'Updated body',
        })
        self.assertEqual(response.status_code, 302)

    def test_post_delete_view(self):
        response = self.client.post(reverse('post_delete', args='1'))
        self.assertEqual(response.status_code, 302)