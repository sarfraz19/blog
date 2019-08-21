from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published = models.DateTimeField(auto_now_add=True)
    lastmodified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('module1:post-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class images(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_pics", blank=True)

    def __str__(self):
        return self.user.username + " " + "Profile"

    def save(self):
        super().save()
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
