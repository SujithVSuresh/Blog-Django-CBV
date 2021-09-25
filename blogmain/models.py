from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import OneToOneField, RelatedField
from django.utils import timezone
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)  
    category_description = models.TextField(null=True)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    meta_description = models.CharField(max_length=500, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    posted_on = models.DateField(default=timezone.now)
    like = models.ManyToManyField(User, related_name='like', blank=True)
    dislike = models.ManyToManyField(User, related_name='dislike', blank=True)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)      
    name = models.CharField(max_length=50, null=True, blank=True)  
    bio = models.TextField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True,)
    saved_post = models.ManyToManyField(BlogPost, related_name='saved', blank=True)
    follower = models.ManyToManyField(User, related_name='follower', blank=True)
    following = models.ManyToManyField(User, related_name='following', blank=True)

    def __str__(self):
        return str(self.username)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(username=instance)
        print('profile created')   

class Comment(models.Model):
    comment_text = models.CharField(max_length=200, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_commented = models.DateField(default=timezone.now)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment_text

class CommentReply(models.Model):
    comment_reply_text = models.CharField(max_length=180, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_replied = models.DateField(default=timezone.now)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)       



 

           
        


  
