from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.models import User #ユーザーモデルを使えるようにする
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import PhotoForm
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Photo, Category



def index(request):
    photos = Photo.objects.all().order_by('-created_at')
    return render(request, 'app/index.html', {'photos': photos})


def users_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    photos = user.photo_set.all().order_by('-created_at')
    return render(request, 'app/users_detail.html', {'user': user,'photos': photos})


def signup(request): #ユーザー新規登録
    if request.method == 'POST':
        form = UserCreationForm(request.POST)     # 入力情報（ユーザー情報）を持ったフォームをformに代入？
        if form.is_valid():
            new_user = form.save()     # ユーザー情報を保存
            input_username = form.cleaned_data['username']       #cleaned_dataでform に入力された値を取得
            input_password = form.cleaned_data['password1']
            new_user = authenticate(username=input_username, password=input_password)#ユーザーネームとパスワードが一致したらUserオブジェクトを返す
            if new_user is not None:
                login(request, new_user)        #request情報と上で返されたUserオブジェクトを引数に取り、ユーザーをログインさせる
                # return redirect('app:index')
                return redirect('app:users_detail', pk=request.user.pk)#????userとは？
    else:   # Postじゃない場合、つまり/signupでアクセスされた場合
        form = UserCreationForm()
    return render(request, 'app/signup.html', {'form': form})


#投稿画面
@login_required #①ユーザーがログイン状態ならphotos_new 関数を実行
def photos_new(request):
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES) #② 入力された情報からフォーム情報を生成
        if form.is_valid():
            photo = form.save(commit=False) #③入力された情報から、Photo インスタンスを生成
            photo.user = request.user #④③で一時的に生成した Photo インスタンスのuserフィールドに、request.user を代入
            photo.save() #⑤userフィールドが入り、全てのフィールドに値が入ったのでデータベースに保存
            messages.success(request, "投稿が完了しました!")
            return redirect('app:users_detail', pk=request.user.pk)
    else:
       form = PhotoForm()
    return render(request, 'app/photos_new.html', {'form': form})


def photos_detail(request, pk):
        photo = get_object_or_404(Photo, pk=pk)
        return render(request, 'app/photos_detail.html', {'photo': photo})


@require_POST
def photos_delete(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    photo.delete()
    return redirect('app:users_detail', request.user.id)


def photos_category(request, category):
# title が URL の文字列と一致する Category インスタンスを取得
    category = Category.objects.get(title=category)
# 取得した Category に属する Photo 一覧を取得
    photos = Photo.objects.filter(category=category).order_by('-created_at')

    return render(request, 'app/index.html', {'photos': photos,'category':category})






