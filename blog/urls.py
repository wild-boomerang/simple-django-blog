from django.contrib.auth.decorators import login_required
from django.urls import path
from django.conf.urls import url
import django.contrib.auth.views

from blog.views import DialogsView
from . import views


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    path('comment/<int:pk>/edit/', views.comment_edit, name='comment_edit'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('post/<int:pk>/like/', views.like_increment, name='like_increment'),

    # url(r'^login/$', views.user_login, name='login'),
    # url(r'^logout-then-login/$', 'django.contrib.auth.views.logout_then_login', name='logout_then_login'),
    url(r'^login/$', django.contrib.auth.views.LoginView.as_view(), name='login'),
    url(r'^logout$', django.contrib.auth.views.LogoutView.as_view(next_page='/'), name='logout'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    # change password urls
    url(r'^password_change/$', django.contrib.auth.views.PasswordChangeView.as_view(), name='password_change'),
    url(r'^password_change/done/$', django.contrib.auth.views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # restore password urls
    url(r'^password-reset/$', django.contrib.auth.views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password-reset/done/$', django.contrib.auth.views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', django.contrib.auth.views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^password-reset/complete/$', django.contrib.auth.views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # register
    url(r'^register/$', views.register, name='register'),
    url(r'^profile_edit/$', views.profile_edit, name='profile_edit'),
    # messages & chats
    path('user/<int:pk>/profile/', views.user_page, name='user_page'),
    url(r'^dialogs/$', login_required(views.DialogsView.as_view()), name='dialogs'),
    url(r'^dialogs/create/(?P<user_id>\d+)/$', login_required(views.CreateDialogView.as_view()), name='create_dialog'),
    url(r'^dialogs/(?P<chat_id>\d+)/$', login_required(views.MessagesView.as_view()), name='messages'),
]
