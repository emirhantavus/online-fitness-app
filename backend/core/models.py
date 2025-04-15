from django.db import models
from django.utils.html import mark_safe
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils.text import slugify

class Banners(models.Model):
	img=models.ImageField(upload_to="banners/")
	alt_text=models.CharField(max_length=150)

	class Meta:
		verbose_name_plural='Banners'

	def __str__(self):
		return self.alt_text

	def image_tag(self):
            if self.img:
                  return mark_safe(f'<a href="{self.img.url}" target="_blank"><img src="{self.img.url}" width="40" /></a>')
            else:
                  return "No image found"
            
   
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
  
  
class ExerciseVideo(models.Model):
    title = models.CharField(max_length=100)
    video_url = models.URLField()
    slug = models.SlugField(unique=True, max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.title
  
  
class VideoInstruction(models.Model):
    video = models.ForeignKey(ExerciseVideo, on_delete=models.CASCADE, related_name='instructions')
    step_number = models.PositiveIntegerField()
    instruction_text = models.TextField()

    class Meta:
        unique_together = ('video', 'step_number')

    def __str__(self):
        return f"{self.video.title} - Step {self.step_number}"
    
@receiver(pre_save, sender=ExerciseVideo)
def add_slug_to_exercise_video(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)