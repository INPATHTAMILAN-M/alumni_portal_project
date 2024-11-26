from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(PostCategory)
admin.site.register(Post)
admin.site.register(PostFiles)
admin.site.register(PostComment)
admin.site.register(PostLike)
admin.site.register(Album)
admin.site.register(AlbumPhotos)
admin.site.register(AlbumComment)
admin.site.register(AlbumLike)
admin.site.register(Video)
admin.site.register(VideoComment)
admin.site.register(Memories)
admin.site.register(MemoryComment)
admin.site.register(MemoryTags)
admin.site.register(MemoryPhotos)