from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    name=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateTimeField(default=timezone.now)
    likes=models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog-home")

class LikedPost(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    
class Comment(models.Model):
    comment=models.TextField()
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
        
