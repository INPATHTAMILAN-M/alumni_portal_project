from django.db import models
from django.contrib.auth.models import User

class PostCategory(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    blog = models.CharField(max_length=255, blank=True, null=True)
    post_category = models.ForeignKey(PostCategory, on_delete=models.CASCADE)
    content = models.TextField( blank=True, null=True)
    published = models.BooleanField(default=False)
    visible_to_public = models.BooleanField(default=False)
    featured_image = models.ImageField(upload_to='posts/featured_images/', blank=True, null=True)
    posted_on = models.DateField(auto_now=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

class PostFiles(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.FileField(upload_to='posts/files/')

class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    comment_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.comment_by.username} on {self.post.title}"

class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.liked_by.username} liked {self.post.title}"

class Album(models.Model):
    album_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    album_location = models.CharField(max_length=225, blank=True, null=True)
    album_date = models.DateField()
    public_view = models.BooleanField(default=True)
    created_on = models.DateField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.album_name

class AlbumPhotos(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='albums/photos/')
    uploaded_on = models.DateField(auto_now_add=True)
    approved = models.BooleanField(default=False)

class AlbumComment(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='album_comments')
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    
    def __str__(self):
        return f"{self.comment_by.username} liked {self.album.album_name}"

class AlbumLike(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='album_likes')
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.liked_by.username} liked {self.album.album_name}"
    
class Video(models.Model):
    video_title = models.CharField(max_length=225)
    video_url = models.CharField(max_length=225)
    uploaded_on = models.DateField(auto_now=True)
    approved = models.BooleanField(default=False)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

class VideoComment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()

class Memories(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    created_on = models.DateField(auto_now=True)
    approved = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class MemoryComment(models.Model):
    memory = models.ForeignKey(Memories, on_delete=models.CASCADE)
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()

class MemoryTags(models.Model):
    memory = models.ForeignKey(Memories, on_delete=models.CASCADE)
    tag = models.CharField(max_length=55)

class MemoryPhotos(models.Model):
    memory = models.ForeignKey(Memories, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='memories/photos/')
