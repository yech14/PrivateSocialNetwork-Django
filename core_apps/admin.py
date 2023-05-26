from django.contrib import admin
from .models import Profile, Post, LikePost, FollowersCount, Comment, Message
from .forms import CommentForm

# Register your models here.
admin.site.register(Profile) # רישום המודל לאדמין של פרופילים עבור המחלקה PROFILE
admin.site.register(Post) # רישום המודל לאדמין עבור המחלקה POST
admin.site.register(LikePost) # רישום המודל לאדמין עבור המחלקה LIKEPOST
admin.site.register(FollowersCount) # רישום המודל לאדמין עבור המחלקה FOLLOWERSCOUNT
admin.site.register(Comment) # רישום המודל לאדמין עבור המחלקה COMMENT
admin.site.register(Message) # רישום המודל לאדמין עבור המחלקה MESSAGE



