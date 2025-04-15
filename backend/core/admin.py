from django.contrib import admin
from django.utils.html import format_html
from .models import (Banners , ExerciseVideo , VideoInstruction ,Contact)

class BannersAdmin(admin.ModelAdmin):
    list_display = ('alt_text', 'image_icon')  

    def image_icon(self, obj):
        return format_html('<img src="{}" width="40" />', obj.img.url)

    image_icon.short_description = 'Image'

admin.site.register(Banners, BannersAdmin)

class ExerciseVideosAdmin(admin.ModelAdmin):
    list_display = ('title','video_url')
    
admin.site.register(ExerciseVideo,ExerciseVideosAdmin)

class VideoInstructionAdmin(admin.ModelAdmin):
    list_display = ('video','step_number','instruction_text')
    
admin.site.register(VideoInstruction,VideoInstructionAdmin)

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')
    
admin.site.register(Contact, ContactAdmin)