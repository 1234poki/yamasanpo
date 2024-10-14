from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # ログインしていないユーザー向けのホームページ
    path('login/', views.login_view, name='login'),  # ログインページ
    path('register/', views.register_view, name='register'),  # 新規登録ページ
    path('logout/', views.logout_view, name='logout'),  # ログアウト
    path('posts/', views.post_list, name='post_list'),  # 投稿一覧
    path('posts/create/', views.create_post, name='create_post'),  # 新規投稿
    path('posts/delete/<int:post_id>/', views.delete_post, name='delete_post'),  # 投稿削除
    path('user/', views.user_page, name='user_page'),  # ユーザーページ
    path('user/edit/', views.edit_user, name='edit_user'),
    path('user/change_password/', views.change_password, name='change_password'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),  # 投稿詳細
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),# コメント削除
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),  # 投稿編集用のURL
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),  # コメント編集用のURL
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'), # コメント削除
]
