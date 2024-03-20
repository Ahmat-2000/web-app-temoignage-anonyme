from django.contrib import admin
from .models import TemoignesModel

class TemoinsAdmin(admin.ModelAdmin):
    list_display = ["agresseur", "message", "victime"]

admin.site.register(TemoignesModel,TemoinsAdmin)