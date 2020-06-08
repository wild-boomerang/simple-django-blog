from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest
from django.test import Client, RequestFactory
from django.urls import reverse, resolve
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from mixer.backend.django import mixer
import pytest

from blog.tokens import account_activation_token
# from blog.admin import CustomUserAdmin
from blog.models import Comment, Profile
from blog.views import activate, signup


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def request_factory():
    return RequestFactory()


@pytest.fixture
def anonymous_user():
    return AnonymousUser()


@pytest.fixture
def not_staff_user(db):
    user = mixer.blend(User, is_staff=False, password='test123')
    user.profile.verified = True
    return user


@pytest.fixture
def staff_user(db):
    user = mixer.blend(User, is_staff=True, password='test123')
    user.profile.verified = True
    return user


@pytest.fixture
def test_type(db):
    return mixer.blend('archbucket_index_core.ItemType', name='test_type', url='test_type_url')


def middleware_anotate(request):
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.save()

    middleware = MessageMiddleware()
    middleware.process_request(request)
    request.session.save()


@pytest.mark.django_db
@pytest.mark.filterwarnings('ignore::Warning')
class TestView:
    # def test_game_view(self, client):
    #     path = reverse('game')
    #
    #     assert client.get(path).status_code == 200

    def test_activation_email_sent(self, client):
        path = reverse('activate')

        assert client.get(path).status_code == 200

    def test_signup_view_not_authenticated_post(self, request_factory, anonymous_user):
        path = reverse('signup')
        request = request_factory.post(path, {'username': 'test_user', 'email': 'test@test.com', 'password1': 'gt54regtf', 'password2': 'gt54regtf'})
        request.user = anonymous_user

        view = signup(request)

        assert view.status_code == 302

        request = request_factory.post(path, {'email': 'test@test.com', 'password1': 'gt54regtf', 'password2': 'gt54regtf'})
        request.user = anonymous_user

        assert view.status_code == 302

    def test_signup_view_not_authenticated_get(self, request_factory, anonymous_user):
        path = reverse('signup')
        request = request_factory.get(path)
        request.user = anonymous_user

        view = signup(request)

        assert view.status_code == 200

    # def test_send_email_view(self, request_factory, not_staff_user, staff_user):
    #     path = reverse('email')
    #     request = request_factory.post(path, {'subject': 'test', 'message': 'test', 'users': [not_staff_user.pk]})
    #     request.user = staff_user
    #     middleware_anotate(request)
    #     view = SendEmailView()
    #     view.setup(request)
    #
    #     assert view.post(request).status_code == 302
    #
    #     request = request_factory.post(path, {'message': 'test', 'users': [not_staff_user.pk]})
    #     request.user = staff_user
    #     view.setup(request)
    #
    #     assert view.post(request).status_code == 302

    def test_profile_view_authenticated_get(self, request_factory, not_staff_user):
        path = reverse('signup')
        request = request_factory.get(path)
        request.user = not_staff_user

        view = signup(request)

        assert view.status_code == 200

    def test_profile_view_authenticated_post(self, request_factory, not_staff_user, staff_user):
        path = reverse('signup')
        request = request_factory.post(path, {'user': not_staff_user, 'current_password': 'test_pass123', 'new_password1': 'fefsa6d54fd5', 'new_password2': 'fefsa6d54fd5'})
        request.user = not_staff_user

        view = signup(request)

        assert view.status_code == 200

    def test_activate(self, request_factory):
        user = mixer.blend(User, username='new_user', password='test_pass123')
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        path = reverse('activate', kwargs={'uidb64': uid, 'token': token})
        request = request_factory.get(path)
        request.user = user

        uid = urlsafe_base64_encode(force_bytes('33'))
        path = reverse('activate', kwargs={'uidb64': uid, 'token': token})
        request = request_factory.get(path)

        assert activate(request, uid, token).status_code == 200
