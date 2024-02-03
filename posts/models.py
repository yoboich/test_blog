from django.db import models

# Create your models here.

from users.models import CustomUser


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    context = models.TextField(blank=True, null=True)
    publish_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(CustomUser, related_name='like_user', blank=True, null=True)


    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return f"{self.title} / {self.publish_date}"

    def num_likes(self):
        return self.likes.count()

    
    def like(self, user):
        self.likes.add(user)

    def unlike(self, user):
        self.likes.remove(user)