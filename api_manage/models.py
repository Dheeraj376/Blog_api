from django.db import models
from django.contrib.auth.models import User


class BlogPost(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=255)
    created_date = models.DateField()
    update_date = models.DateField()
    status = models.CharField(max_length=50)
    visibility = models.CharField(max_length=40 , default="public")