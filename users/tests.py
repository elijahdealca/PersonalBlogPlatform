from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import BlogPost

class BlogPostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.blog_post = BlogPost.objects.create(
            title="Test Post",
            content="This is a test blog post.",
            author=self.user
        )

    def test_blog_post_content(self):
        self.assertEqual(self.blog_post.title, "Test Post")
        self.assertEqual(self.blog_post.content, "This is a test blog post.")
        self.assertEqual(self.blog_post.author.username, "testuser")