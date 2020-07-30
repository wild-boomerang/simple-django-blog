from django.contrib.auth.models import User
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import Client, RequestFactory
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from mixer.backend.django import mixer
import pytest

from blog.tokens import account_activation_token
from blog.models import Comment, Profile, Post, Chat
from blog.views import activate, signup, post_list, post_detail, post_new, post_edit, post_draft_list, post_publish, \
    post_delete, add_comment_to_post, comment_remove, comment_edit, comment_approve, dashboard, profile_edit, \
    like_increment, user_page, DialogsView, CreateDialogView, MessagesView
from taggit.managers import TaggableManager


@pytest.fixture()
def client():
    return Client()


@pytest.fixture
def request_factory():
    return RequestFactory()


@pytest.fixture(autouse=True)
def db_initialisation():
    user = User.objects.create_user('username')
    post = Post.objects.create(author=user, title='title', text='text')
    Comment.objects.create(post=post, text='text', author=user)


def middleware_install(request):
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.save()

    middleware = MessageMiddleware()
    middleware.process_request(request)
    request.session.save()


@pytest.mark.django_db
@pytest.mark.filterwarnings('ignore::Warning')
class TestView:
    def test_post_list_view(self, client):
        path = reverse('post_list')
        assert client.get(path).status_code == 200

    def test_post_detail_view(self, client, request_factory):
        # get method
        user = User.objects.create_user(username='sfda')
        post = Post.objects.create(author=user, title='title', text='text')
        path = reverse('post_detail', kwargs={'pk': post.pk})
        request = request_factory.get(path)
        request.user = user
        view = post_detail(request, user.pk)
        assert view.status_code == 200

        # post method
        request = request_factory.post(path, {'text': 'text'})
        request.user = user
        view = post_detail(request, user.pk)
        assert view.status_code == 200

    def test_post_new_view(self, client, request_factory):
        # get method
        path = reverse('post_new')
        user = User.objects.create_user(username='sfda')
        request = request_factory.get(path)
        request.user = user
        view = post_new(request)
        assert view.status_code == 200

        # post method\
        request = request_factory.post(path, {'title': 'title', 'text': 'text', 'tags': TaggableManager()})
        request.user = user
        view = post_new(request)
        assert view.status_code == 302

    def test_post_edit_view(self, client, request_factory):
        # get method
        user = User.objects.create_user(username='sfda')
        post = Post.objects.create(author=user, title='title', text='text')
        path = reverse('post_edit', kwargs={'pk': post.pk})
        request = request_factory.get(path, {'pk': post.pk})
        request.user = user
        view = post_edit(request, post.pk)
        assert view.status_code == 200

        # post method
        request = request_factory.post(path, {'title': 'title', 'text': 'text', 'tags': TaggableManager()})
        request.user = user
        view = post_edit(request, post.pk)
        assert view.status_code == 302

    def test_post_draft_list_view(self, request_factory):
        path = reverse('post_draft_list')
        request = request_factory.get(path)
        request.user = User.objects.create_user(username='sfda')
        assert post_draft_list(request).status_code == 200

    def test_post_publish_view(self, request_factory):
        user = User.objects.create_user(username='sfda')
        post = Post.objects.create(author=user, title='title', text='text')
        path = reverse('post_publish', kwargs={'pk': post.pk})
        request = request_factory.get(path)
        request.user = user
        assert post_publish(request, post.pk).status_code == 302

    def test_post_delete_view(self, request_factory):
        user = User.objects.create_user(username='sfda')
        post = Post.objects.create(author=user, title='title', text='text')
        path = reverse('post_delete', kwargs={'pk': post.pk})
        request = request_factory.get(path)
        request.user = user
        assert post_delete(request, post.pk).status_code == 302

    def test_add_comment_to_post_view(self, client, request_factory):
        # get method
        user = User.objects.create_user(username='sfda')
        post = Post.objects.create(author=user, title='title', text='text')
        path = reverse('add_comment_to_post', kwargs={'pk': post.pk})
        request = request_factory.get(path)
        request.user = user
        view = add_comment_to_post(request, post.pk)
        assert view.status_code == 200

        # post method
        request = request_factory.post(path, {'text': 'text'})
        request.user = user
        view = add_comment_to_post(request, post.pk)
        assert view.status_code == 302

    def test_comment_remove_view(self, request_factory):
        user = User.objects.create_user(username='sfda')
        post = Post.objects.create(author=user, title='title', text='text')
        comment = Comment.objects.create(post=post, text='text', author=user)
        path = reverse('comment_remove', kwargs={'pk': comment.pk})
        request = request_factory.get(path)
        request.user = user
        assert comment_remove(request, comment.pk).status_code == 302

    def test_comment_edit_view(self, client, request_factory):
        # get method
        user = User.objects.create_user(username='sfda')
        post = Post.objects.create(author=user, title='title', text='text')
        comment = Comment.objects.create(post=post, text='text', author=user)
        path = reverse('comment_edit', kwargs={'pk': comment.pk})
        request = request_factory.get(path)
        request.user = user
        view = comment_edit(request, comment.pk)
        assert view.status_code == 200

        # post method
        request = request_factory.post(path, {'text': 'text'})
        request.user = user
        view = comment_edit(request, comment.pk)
        assert view.status_code == 302

    def test_comment_approve_view(self, request_factory):
        user = User.objects.create_user(username='sfda')
        post = Post.objects.create(author=user, title='title', text='text')
        comment = Comment.objects.create(post=post, text='text', author=user)
        path = reverse('comment_approve', kwargs={'pk': comment.pk})
        request = request_factory.get(path)
        request.user = user
        assert comment_approve(request, comment.pk).status_code == 302

    def test_dashboard_view(self, request_factory):
        user = User.objects.create_user(username='sfda')
        path = reverse('dashboard')
        request = request_factory.get(path)
        request.user = user
        assert dashboard(request).status_code == 200

    def test_profile_edit_view(self, client, request_factory):
        # get method
        user = User.objects.create_user(username='sfda')
        Profile.objects.create(user=user)
        path = reverse('profile_edit')
        request = request_factory.get(path)
        request.user = user
        view = profile_edit(request)
        assert view.status_code == 200

        # post method right
        request = request_factory.post(path, {'username': ['boom'], 'first_name': ['name'], 'last_name': ['surname'],
                                              'email': ['dsfgh@khljn.com'], 'date_of_birth': ['']})
        request.user = user
        middleware_install(request)
        view = profile_edit(request)
        assert view.status_code == 200

        # post method wrong
        request = request_factory.post(path)
        request.user = user
        middleware_install(request)
        view = profile_edit(request)
        assert view.status_code == 200

    def test_like_increment_view(self, request_factory):
        user = User.objects.create_user(username='sfda')
        post = Post.objects.create(author=user, title='title', text='text')
        path = reverse('like_increment', kwargs={'pk': post.pk})
        request = request_factory.get(path)
        request.user = user
        assert like_increment(request, post.pk).status_code == 302

    def test_user_page_view(self, request_factory, client):
        user = User.objects.create_user(username='sfda')
        profile = Profile.objects.create(user=user)
        path = reverse('user_page', kwargs={'pk': profile.pk})
        response = client.get(path)
        assert response.status_code == 200
        # request = request_factory.get(path)
        # request.user = user
        # assert user_page(request, profile.pk).status_code == 200

    def test_DialogsView(self, request_factory):
        user = User.objects.create_user(username='sfda')
        Profile.objects.create(user=user)
        chat = Chat.objects.create()
        path = reverse('dialogs')
        request = request_factory.get(path)
        request.user = user
        dialog = DialogsView()
        dialog.setup(request)
        assert dialog.get(request).status_code == 200

    def test_CreateDialogView(self, request_factory):
        user = User.objects.create_user(username='sfda')
        profile = Profile.objects.create(user=user)
        path = reverse('create_dialog', kwargs={'user_id': profile.pk})
        request = request_factory.get(path)
        request.user = user
        dialog = CreateDialogView()
        dialog.setup(request)
        assert dialog.get(request, profile.pk).status_code == 302

    def test_MessagesView(self, request_factory):
        # get method
        user = User.objects.create_user(username='sfda')
        profile = Profile.objects.create(user=user)
        chat = Chat.objects.create()
        path = reverse('messages', kwargs={'chat_id': chat.pk})
        request = request_factory.get(path)
        request.user = user
        dialog = MessagesView()
        dialog.setup(request)
        assert dialog.get(request, chat.pk).status_code == 200

        # post method
        request = request_factory.post(path, {'content': 'message'})
        request.user = user
        dialog = MessagesView()
        dialog.setup(request)
        assert dialog.post(request, chat.pk).status_code == 302

    def test_signup_view(self, client, request_factory):
        # get method
        path = reverse('signup')
        assert client.get(path).status_code == 200

        # post method
        response = client.post(path, data={'email': 'sdfsadfsdsdgd@gmail.com', 'first_name': 'name',
                                           'last_name': 'name', 'username': 'nick',
                                           'password1': 'asd123qwe', 'password2': 'asd123qwe',
                                           'date_of_birth': timezone.now().date()})
        assert response.status_code == 200
        # request = request_factory.post(path, {'email': 'sdfsadfsdsdgd@gmail.com', 'first_name': 'name',
        #                                       'last_name': 'name', 'username': 'nick',
        #                                       'password1': 'asd123qwe', 'password2': 'asd123qwe',
        #                                       'date_of_birth': timezone.now().date()})
        # request.user = User.objects.create_user(username='sfda')
        # view = signup(request)
        # assert view.status_code == 200

    def test_activate_view(self, request_factory):
        user = mixer.blend(User, username='new_user', password='test_pass123')
        Profile.objects.create(user=user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        path = reverse('activate', kwargs={'uidb64': uid, 'token': token})
        request = request_factory.get(path)
        request.user = user
        assert activate(request, uid, token).status_code == 200

        uid = urlsafe_base64_encode(force_bytes('33'))
        path = reverse('activate', kwargs={'uidb64': uid, 'token': token})
        request = request_factory.get(path)

        assert activate(request, uid, token).status_code == 200
