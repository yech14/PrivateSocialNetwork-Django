
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages  # ייבוא הספרייה של ההודעות שיעלו למשתמש
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost, FollowersCount, Comment, Message
from .forms import CommentForm, MessageForm
from itertools import chain
from datetime import datetime
from uuid import uuid4
import random

# Create your views here.

@login_required(login_url='signin')  # כדי שרק משתמשים שמחוברים יוכלו להיכנס לדף הזה שמתחת (הראשי)
def index(request):
    user_object = User.objects.get(username=request.user.username)  # קבלת היוזר שמחובר
    user_profile = Profile.objects.filter(user=user_object).first()  # קבלת הפרופיל של היוזר המחובר (שימוש בFILTER כדי שיעבוד, אבל צריך לוודא שלא פוגע - אולי בגלל ריבוי השם USER)

    user_following_list = [] # רשימה של כל היוזרים שהיוזר המחובר עוקב אחריהם
    feed = [] # רשימה של כל הפוסטים של היוזרים שהיוזר המחובר עוקב אחריהם

    user_following = FollowersCount.objects.filter(follower=request.user.username)  # קבלת כל היוזרים שהיוזר המחובר עוקב אחריהם

    for users in user_following:
        user_following_list.append(users.user) # הוספת היוזרים שהיוזר המחובר עוקב אחריהם לרשימה

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames) # קבלת כל הפוסטים של היוזרים שהיוזר המחובר עוקב אחריהם
        feed.append(feed_lists) # הוספת הפוסטים של היוזרים שהיוזר המחובר עוקב אחריהם לרשימה

    feed_list = list(chain(*feed)) # יצירת רשימה חדשה של כל הפוסטים של היוזרים שהיוזר המחובר עוקב אחריהם

    posts_with_comments = []
    for post in feed_list:
        comments = Comment.objects.filter(post=post)
        posts_with_comments.append((post, comments))



    # User suggestions - רשימת היוזרים שהיוזר המחובר לא עוקב אחריהם וזה לא הוא עצמו
    all_users = User.objects.all() # קבלת כל היוזרים
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user) # קבלת כל היוזרים שהיוזר המחובר עוקב אחריהם
        user_following_all.append(user_list) # הוספת היוזרים שהיוזר המחובר עוקב אחריהם לרשימה

    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))] # יצירת רשימה חדשה של כל היוזרים שהיוזר המחובר לא עוקב אחריהם
    current_user = User.objects.filter(username=request.user.username) # קבלת היוזר המחובר
    final_suggestion_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))] # יצירת רשימה חדשה של כל היוזרים שהיוזר המחובר לא עוקב אחריהם וזה לא הוא עצמו
    random.shuffle(final_suggestion_list) # ערבוב הרשימה

    username_profile = []
    username_profile_list = []

    for users in final_suggestion_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))



    messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(
        request,
        'index.html',
        {
            'user_profile': user_profile,
            'posts_with_comments': posts_with_comments,
            'suggestions_username_profile_list': suggestions_username_profile_list[:4],
            'messages': messages[:4]
        }
    )

@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        user = request.user.username  # קבלת היוזר שמחובר
        image = request.FILES.get('image_upload') # קבלת התמונה שהועלתה
        caption = request.POST['caption'] # קבלת הכיתוב שהוזן

        new_post = Post.objects.create(user=user, image=image, caption=caption) # יצירת אובייקט פוסט חדש עם הפרטים שהתקבלו מהPOST
        new_post.save() # שמירת אובייקט הפוסט החדש

        return redirect('/') # חזרה לדף הראשי
    else:
        return redirect('/')

@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)  # קבלת היוזר שמחובר
    user_profile = Profile.objects.get(user=user_object)  # קבלת הפרופיל של היוזר המחובר (שימוש בFILTER כדי שיעבוד, אבל צריך לוודא שלא פוגע - אולי בגלל ריבוי השם USER)

    if request.method == 'POST':
        username = request.POST['username'] # קבלת היוזר שהוזן
        username_object = User.objects.filter(username__icontains=username) # קבלת היוזר שהוזן כאובייקט

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id) # הוספת היוזרים שהוזן לרשימה

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids) # קבלת הפרופילים של היוזרים שהוזןלפי הID
            username_profile_list.append(profile_lists) # הוספת הפרופילים של היוזרים שהוזן לרשימה

        username_profile_list = list(chain(*username_profile_list)) # יצירת רשימה חדשה של כל הפרופילים של היוזרים שהוזן

    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list}) # קובץ הקוד של הדף הראשי של האתר - צריך ליצור קובץ HTML חיצוני מדוייק יותר. והסוגריים המסולסלים שולחים לדף הראשי (לHTML) את היוזר פרופיל לפי השם שנתתי



@login_required(login_url='signin')
def post_detail(request, post_id):
    post = Post.objects.filter(id=post_id)
    comments = post.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'index.html', {'post': post, 'comments': comments, 'form': form})

@login_required(login_url='signin')
def send_message(request):
    user_object = User.objects.get(username=request.user.username)  # קבלת היוזר שמחובר
    user_profile = Profile.objects.filter(user=user_object).first()  # קבלת הפרופיל של היוזר המחובר (שימוש בFILTER כדי שיעבוד, אבל צריך לוודא שלא פוגע - אולי בגלל ריבוי השם USER)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('inbox')
    else:
        form = MessageForm()

    return render(request, 'send_message.html', {'form': form, 'user_profile': user_profile})

@login_required(login_url='signin')
def inbox(request):
    messages = Message.objects.filter(recipient=request.user)
    user_object = User.objects.get(username=request.user.username)  # קבלת היוזר שמחובר
    user_profile = Profile.objects.filter(user=user_object).first()  # קבלת הפרופיל של היוזר המחובר (שימוש בFILTER כדי שיעבוד, אבל צריך לוודא שלא פוגע - אולי בגלל ריבוי השם USER)

    return render(request, 'inbox.html', {'messages': messages, 'user_profile': user_profile})

"""@login_required(login_url='signin')
def search_recipients(request):
    query = request.GET.get('term', '')
    recipients = User.objects.filter(username__icontains=query)
    results = [user.username for user in recipients]
    return JsonResponse(results, safe=False)"""

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username  # קבלת היוזר שמחובר
    post_id = request.GET.get('post_id')  # קבלת הID של הפוסט שהועלה

    post = Post.objects.get(id=post_id)  # קבלת הפוסט לפי הID שהתקבל

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()  # קבלת הלייקים של היוזר המחובר עבור הפוסט שהתקבל

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)  # יצירת אובייקט לייק חדש עבור היוזר המחובר והפוסט שהתקבל
        new_like.save()  # שמירת אובייקט הלייק החדש
        post.no_of_likes += 1  # הוספת לייק אחד לפוסט
        post.save()  # שמירת הפוסט
        return redirect('/') # חזרה לדף הראשי
    else:
        like_filter.delete()  # מחיקת הלייק של היוזר המחובר עבור הפוסט שהתקבל
        post.no_of_likes -= 1  # הורדת לייק אחד מהפוסט
        post.save()  # שמירת הפוסט
        return redirect('/')


@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)  # קבלת היוזר שמחובר
    user_profile = Profile.objects.get(user=user_object)  # קבלת הפרופיל של היוזר המחובר (שימוש בFILTER כדי שיעבוד, אבל צריך לוודא שלא פוגע - אולי בגלל ריבוי השם USER)
    user_posts = Post.objects.filter(user=pk)  # קבלת כל הפוסטים של היוזר המחובר
    user_post_len = len(user_posts)  # קבלת אורך הפוסטים של היוזר המחובר

    follower = request.user.username  # קבלת היוזר שעוקב
    user = pk
    if FollowersCount.objects.filter(follower=follower, user=user).first(): # בדיקה אם היוזר המחובר עוקב אחרי היוזר שהתקבל (בדיקה בדאטה בייס)
        button_text = 'Unfollow' # אם כן, יוצג כפתור הפסקת העקבות
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk)) # קבלת כל העוקבים של היוזר שהתקבל
    user_following = len(FollowersCount.objects.filter(follower=pk)) # קבלת כל היוזרים שהיוזר שהתקבל (pk) עוקב אחריהם

    context = {
        'user_profile': user_profile,
        'user_object': user_object,
        'user_posts': user_posts,
        'user_post_len': user_post_len,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']  # שמירת הערך של FOLLOWER שהתקבל בFORM בPOST
        user = request.POST['user']  # שמירת הערך של USER שהתקבל בFORM בPOST

        if FollowersCount.objects.filter(follower=follower, user=user).first(): # בדיקה אם היוזר המחובר עוקב אחרי היוזר שהתקבל (בדיקה בדאטה בייס)
            delete_follower = FollowersCount.objects.get(follower=follower, user=user) # קבלת העוקב מהדאטה בייס
            delete_follower.delete()  # מחיקת העוקב מהדאטה בייס
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user) # יצירת אובייקט עוקב חדש
            new_follower.save()  # שמירת העוקב בדאטה בייס
            return redirect('/profile/'+user) # חזרה לדף הפרופיל של היוזר שהתקבל
    else:
        return redirect('/')

@login_required(login_url='signin')
def setting(request):
    user_profile = Profile.objects.filter(user=request.user).first()  # קבלת הפרופיל של היוזר המחובר

    if request.method == 'POST':
        # if the user dont enter first and last name it will upload an error
        if request.POST['first_name'] == '' or request.POST['last_name'] == '':
            messages.error(request, 'Please enter your first and last name')
            return redirect('setting')
        elif request.POST['email'] == '':
            messages.error(request, 'Please enter your email')
            return redirect('setting')
        else:
            user_profile.email = request.POST['email']  # שמירת האימייל של היוזר שהתקבל מהPOST לפי השם EMAIL
            user_profile.first_name = request.POST['first_name']
            user_profile.last_name = request.POST['last_name']
            user_profile.save()

        if request.FILES.get('image') == None:  # בדיקה אם המשתמש לא העלה תמונה חדשה
            image = user_profile.profile_img
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profile_img = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profile_img = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect('setting')
    return render(request, 'setting.html', {'user_profile': user_profile})  # קובץ הקוד של דף ההגדרות של היוזר - צריך ליצור קובץ HTML חיצוני מדוייק יותר
def signup(request):
    if request.method == 'POST':  # בדיקה אם המשתמש לחץ על כפתור השליחה שנמצא בHTML של ההרשמה
        username = request.POST['username']  # קבלת הנתונים מהטופס על ידי הNAME שהוספנו
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:  # בדיקה אם הסיסמאות תואמות
            if User.objects.filter(email=email).exists():  # בדיקה אם המייל כבר קיים במערכת
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():  # בדיקה אם השם משתמש כבר קיים במערכת
                messages.info(request, 'Username Taken')
                return redirect('signup') # חזרה לדף ההרשמה
            else:
                user = User.objects.create_user(username=username, email=email, password=password) # יצירת משתמש חדש
                user.save() # שמירת המשתמש

                user_login = auth.authenticate(username=username, password=password) # התחברות אוטומטית לאחר הרשמה
                auth.login(request, user_login) #

                user_model = User.objects.get(username=username) # קבלת המשתמש שנוצר
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id) # יצירת פרופיל חדש למשתמש החדש
                new_profile.save() # שמירת הפרופיל
                return redirect('setting') # מעבר לדף ההגדרות
        else:
            messages.info(request, 'Password not matching')
            return redirect('signup')  # חזרה לדף ההרשמה

    else:
        return render(request, 'signup.html')  # כנל כמו למעלה - רק עם קובץ HTML אחר

def signin(request):
    if request.method == 'POST':  # בדיקה אם המשתמש לחץ על כפתור השליחה שנמצא בHTML של ההתחברות
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)  # בדיקה אם המשתמש קיים במערכת
        if user is not None: # זאת אומרת שיש כזה משתמש
            auth.login(request, user)  # נחבר את המשתמש למערכת
            return redirect('/')  # חזרה לדף הראשי
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('signin')  # חזרה לדף ההתחברות
    return render(request, 'signin.html')  # כנל כמו למעלה - רק עם קובץ HTML של ההתחברות

@login_required(login_url='signin') # כדי שרק משתמשים שמחוברים יוכלו להיכנס לדף ההתנתקות
def logout(request):
    auth.logout(request)  # ניתוק היוזר מהמערכת
    return redirect('/')  # חזרה לדף הראשי

