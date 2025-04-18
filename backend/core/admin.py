from django.contrib import admin
from django.utils.html import format_html
from .models import Banners, Contact, ExerciseVideo, VideoInstruction

@admin.register(Banners)
class BannersAdmin(admin.ModelAdmin):
    list_display = ('alt_text', 'image_icon')

    def image_icon(self, obj):
        if obj.img:
            return format_html('<img src="{}" width="40" />', obj.img.url)
        return "No image"

@admin.register(ExerciseVideo)
class ExerciseVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_url')

@admin.register(VideoInstruction)
class VideoInstructionAdmin(admin.ModelAdmin):
    list_display = ('video', 'step_number', 'instruction_text')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')
