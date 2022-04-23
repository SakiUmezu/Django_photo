from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static 
from django.contrib.auth import views as auth_views


app_name = 'app'
urlpatterns = [
    path('', views.index, name='index'),
    path('users/<int:pk>/', views.users_detail, name='users_detail'),
    path('photos/new/', views.photos_new, name='photos_new'),#投稿画面
    path('photos/<int:pk>/', views.photos_detail, name='photos_detail'),
    path('photos/<int:pk>/delete/',
         views.photos_delete, name='photos_delete'),
    path('photos/<str:category>/', views.photos_category, name='photos_category'),#カテゴリー
    path('signup/', views.signup, name='signup'),#ユーザー新規登録画面
    path('login/',
         auth_views.LoginView.as_view(template_name='app/login.html'),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

# MEDIA_ROOT を公開する(アクセス可能にする) 
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)







