from django.contrib import admin
from django.utils.html import format_html
from application.models import RecipeImage


# Register your models here.

class RecipeImageAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'preview')

    def preview(self, obj):
        return format_html('<img src="{}" style="height: 100px;" />', obj.image.url)

    preview.short_description = 'Preview'

admin.site.register(RecipeImage, RecipeImageAdmin)
