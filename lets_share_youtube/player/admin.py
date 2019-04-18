from django.contrib import admin
from .models import PlayList, Video


class PlayListAdmin(admin.ModelAdmin):
    pass


class VideoAdmin(admin.ModelAdmin):
    pass


admin.site.register(PlayList, PlayListAdmin)
admin.site.register(Video, VideoAdmin)
