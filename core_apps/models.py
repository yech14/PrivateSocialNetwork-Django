from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime

# Create your models here - יצירת מודל לפרופילים עם שימוש בדאטה בייס (זאת אומרת יכולת להוסיף פרופילים חדשים ולערוך אותם)
class Profile(models.Model):
     user = models.OneToOneField(User, on_delete=models.CASCADE) # קשר חד צדדי עם דאטה בייס של יוזר
     id_user = models.IntegerField(default=0) # מספר זיהוי של היוזר
     first_name = models.CharField(max_length=100, blank=True, null=True, default='') # שם פרטי של היוזר
     last_name = models.CharField(max_length=100, blank=True, null=True, default='') # שם משפחה של היוזר
     email = models.EmailField(max_length=150, blank=True, null=True, default='') # אימייל של היוזר
     bio = models.TextField(max_length=500, blank=True) # תיאור קצר של היוזר
     profile_img = models.ImageField(upload_to='profile_images', default='blank_profile.png') # תמונת פרופיל שיאוחסנו בתקייה, עם תמונת ברירת המחדל
     location = models.CharField(max_length=30, blank=True) # מיקום של היוזר

     def __str__(self):
         return self.user.username



class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user # הצגת שם הפוסט בפורמט של סטרינג


class LikePost(models.Model):
    post_id = models.CharField(max_length=200, null=True)
    username = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.username

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.user



class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender


















