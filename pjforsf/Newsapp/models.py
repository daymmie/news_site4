
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


article = 'AR'
news = 'NW'

POSITIONS = [
    (article, 'Article'),
    (news, 'News')
]


class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        self.author_rating = 0
        for post in Post.post_rating.validators:
            self.author_rating += post * 3
        for comment in Comment.comment_rating.validators:
            self.author_rating += comment
        self.save()

    def __str__(self):
        return f'{self.author_user}'


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.category_name}'


class Post(models.Model):
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_choice = models.CharField(max_length=2,
                                   choices=POSITIONS,
                                   default=news)
    post_date = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    post_title = models.CharField(max_length=30)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)

    def preview(self):
        post_preview = self.post_text[0:125] + '...'
        return f'{post_preview}'

    def like(self, amount=1):
        self.post_rating += amount
        self.save()

    def dislike(self, amount=1):
        self.post_rating -= amount
        self.save()

    def __str__(self):
        return f'Title: {self.post_title}\nDate: {self.post_date}\n' \
               f'article preview: {self.preview()}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self, amount=1):
        self.comment_rating += amount
        self.save()

    def dislike(self, amount=1):
        self.comment_rating -= amount
        self.save()
