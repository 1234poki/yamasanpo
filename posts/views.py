from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash
from .models import Post, User, Comment
from .forms import CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserRegistrationForm, UserLoginForm, PostForm, UserEditForm


User = get_user_model()

def home(request):
    if request.user.is_authenticated:
        return redirect('post_list')
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'メールアドレスまたはパスワードが正しくありません。')
            except User.DoesNotExist:
                messages.error(request, 'そのメールアドレスは存在しません。')
            except Exception as e:
                messages.error(request, f"ログイン中にエラーが発生しました: {e}")
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def post_list(request):
    posts = Post.objects.all().order_by('-created_at') 
    return render(request, 'post_list.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def user_page(request):
    user_posts = Post.objects.filter(user=request.user)

    user_comments = Comment.objects.filter(user=request.user)
    commented_posts = Post.objects.filter(comments__in=user_comments).distinct()

    return render(request, 'user_page.html', {
        'user_posts': user_posts,
        'commented_posts': commented_posts
    })

@login_required
def edit_user(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_page')
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'edit_user.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            messages.success(request, "パスワードが正常に変更されました。")
            return redirect('user_page')
        else:
            messages.error(request, "パスワードの変更に失敗しました。もう一度お試しください。")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id) 

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            try:
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.user = request.user
                comment.save()
                return redirect('post_detail', post_id=post.id)
            except Exception as e:
                pass
    else:
        comment_form = CommentForm()


    return render(request, 'post_detail.html', {
        'post': post,
        'comment_form': comment_form
    })



@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('user_page')
    return render(request, 'delete_post.html', {'post': post})

def logout_view(request):
    logout(request)
    messages.info(request, 'ログアウトしました。')
    return redirect('home')

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    
    if request.method == 'POST':
        comment.delete()
        return redirect('post_detail', post_id=comment.post.id)
    
    return render(request, 'comment_confirm_delete.html', {'comment': comment})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user) 
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = PostForm(instance=post)

    return render(request, 'edit_post.html', {'form': form, 'post': post})

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user) 
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'edit_comment.html', {'form': form, 'comment': comment})
