from django.db import models
from django.utils.text import slugify
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to="users/images", blank=True)
    def __str__(self):
        return f'Profile of {self.user.username}'

class Tag(models.Model):
    caption = models.CharField(max_length=50)
    def __str__(self):
        return self.caption

class Author(models.Model):
    f_name = models.CharField(max_length=50)
    l_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    def __str__(self):
        return f"{self.f_name} {self.l_name}"


class BlogPost(models.Model):
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=50)
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, related_name='blogpost', null=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    content = models.TextField()
    img_url = models.ImageField(upload_to="images")
    slug = models.CharField(max_length=50, db_index=True, unique=True)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return f"{self.title}"
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Comment(models.Model):
    comment_details = models.CharField(max_length=200)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    comment_author =  models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comments')

    def __str__(self):
        return self.post.title
    








    



