from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse
# from django.contrib.auth import authenticate, login
from django.contrib import messages
import logging
import logging.config
from django.views import View

from BlogSite.settings import LOGGING
from .models import Post, Comment, Profile, Likes, Message, Chat
from .forms import PostForm, CommentForm, UserRegistrationForm, UserEditForm, ProfileEditForm, MessageForm


def post_list(request):
    logging.config.dictConfig(LOGGING)
    logger = logging.getLogger("my_logger")
    logger.info("Test logging, post_list view before ")
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    logger.info("Test logging, post_list view after")
    return render(request, "blog/post_list.html", {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # comments = post.approved_comments()
    comments = post.comments
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Likes.objects.create(post=post, user=request.user)
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def post_delete(request, pk):
    # post = get_object_or_404(Post, pk=pk)
    Post.objects.get(pk=pk).delete()
    return redirect('post_list')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = get_object_or_404(Post, pk=comment.post.pk)
    comments = post.approved_comments()
    if request.method == 'POST':
        comment_form = CommentForm(instance=comment, data=request.POST)
        if comment_form.is_valid():
            comment_form.save()
            # created_data = timezone.now()
            return redirect('post_detail', pk=comment.post.pk)
    else:
        comment_form = CommentForm(instance=comment)
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(username=cd['username'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('Authenticated successfully!')
#                 else:
#                     return HttpResponse('Disabled account!')
#             else:
#                 return HttpResponse('Invalid login!')
#     else:
#         form = LoginForm()
#     return render(request, 'registration/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'blog/dashboard.html', {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'blog/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'blog/register.html', {'user_form': user_form})


@login_required
def profile_edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'blog/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def like_increment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like = Likes.objects.get_or_create(post=post, user=request.user)[0]
    if like.already_liked:
        post.like_quantity -= 1
        like.invert_like()
    else:
        post.like_quantity += 1
        like.invert_like()
    post.save()
    like.save()
    # print(request.user.is_superuser)
    print(request)
    return redirect('post_list')  # todo redirect to right page


def user_page(request, pk):
    user_profile = get_object_or_404(Profile, pk=pk)
    user = user_profile.user
    profile_form = ProfileEditForm(instance=user_profile)
    user_form = UserEditForm(instance=user)
    return render(request, 'blog/user_page.html', {'user': user, 'user_form': user_form,
                                                   'profile_form': profile_form})


class DialogsView(View):
    def get(self, request):
        chats = Chat.objects.filter(members__in=[request.user.id])
        return render(request, 'blog/dialogs.html', {'user_profile': request.user, 'chats': chats})


class MessagesView(View):
    def get(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id)
            if request.user.profile in chat.members.all():
                chat.content_set.filter(is_read=False).exclude(sender=request.user.profile).update(is_read=True)
            else:
                chat = None
        except Chat.DoesNotExist:
            chat = None

        return render(request, 'blog/messages.html', {'user': request.user, 'chat': chat,
                                                      'message_form': MessageForm()})

    def post(self, request, chat_id):
        message_form = MessageForm(data=request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.chat_id = chat_id
            message.sender = request.user.profile
            message.save()
        return redirect(reverse('blog:messages', kwargs={'chat_id': chat_id}))


class CreateDialogView(View):
    def get(self, request, user_id):
        chats = Chat.objects.filter(members__in=[request.user.id, user_id], type=Chat.DIALOG).annotate(c=Count('members')).filter(c=2)
        if chats.count() == 0:
            chat = Chat.objects.create()
            chat.members.add(request.user.profile)
            chat.members.add(user_id)
        else:
            chat = chats.first()
        # return redirect(reverse('blog:messages', kwargs={'chat_id': chat.id}))
        return redirect('messages', chat.id)
