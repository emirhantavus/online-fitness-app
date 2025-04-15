from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils.text import slugify

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = CKEditor5Field('Content', config_name='extends')
    image = models.ImageField(upload_to='posts/', null=True, blank=True,default='\posts\headerlogo.jpg')
    slug = models.SlugField(unique=True, max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

@receiver(pre_save, sender=Post)
def add_slug_to_post(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Comment by {self.author} on {self.post}'