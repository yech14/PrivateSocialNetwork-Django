import debug_toolbar
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('setting', views.setting, name='setting'),
    path('upload', views.upload, name='upload'),
    path('follow', views.follow, name='follow'),
    path('search', views.search, name='search'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('like-post', views.like_post, name='like-post'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),  # יצירת נתיב לדף ההתחברות, ואז הוא קורא להתחברות מוויוז, ומגדירים לו את השם התחברות
    path('logout', views.logout, name='logout'), # כשאני רושם לוג אווט בHTML בקישור (HERF) זה מפנה לפונקצית לוג אווט שבוויוז, ומגדירים לו את השם התנתקות
    path('__debug__/', include(debug_toolbar.urls)),
    path('send_message', views.send_message, name='send_message'),
    #path('search_recipients', views.search_recipients, name='search_recipients'),
    path('inbox', views.inbox, name='inbox'),



]# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)