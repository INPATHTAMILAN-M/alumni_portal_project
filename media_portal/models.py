from django.db import models
from django.contrib.auth.models import User
from event_portal.models import Event
from job_portal.models import JobPost

class PostCategory(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Memories(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    created_on = models.DateField(auto_now=True)
    approved = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Memories of {self.year}-{self.month} by {self.created_by.username}"
class Post(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    blog = models.CharField(max_length=255, blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True)
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, blank=True, null=True)
    memories = models.ForeignKey(Memories, on_delete=models.CASCADE, blank=True, null=True)
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

    def __str__(self):
        return f"Photo in {self.album.album_name} by {self.album.created_by.username}"
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

# class MemoryLike(models.Model):
#     memory = models.ForeignKey(Memories, on_delete=models.CASCADE, related_name='album_likes')
#     liked_by = models.ForeignKey(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.liked_by.username} liked {self.album.album_name}"
    
class MemoryComment(models.Model):
    memory = models.ForeignKey(Memories, on_delete=models.CASCADE)
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()

class MemoryTags(models.Model):
    memory = models.ForeignKey(Memories, on_delete=models.CASCADE,related_name='memorytags')
    tag = models.CharField(max_length=255)

    def __str__(self):
        return f"Tag {self.tag} in {self.memory.year}-{self.memory.month} by {self.memory.created_by.username}"
class MemoryPhotos(models.Model):
    memory = models.ForeignKey(Memories, on_delete=models.CASCADE,related_name='memoryphoto')
    photo = models.ImageField(upload_to='memories/photos/')

    def __str__(self):
        return f"Photo in {self.memory.year}-{self.memory.month} by {self.memory.created_by.username}"