from django.urls import resolve
from blog.views import *


class TestUrls:
    def test_post_list_url(self):
        path = reverse('post_list')
        assert resolve(path).view_name == 'post_list'
        assert resolve(path).func == post_list

    def test_post_list_by_tag_url(self):
        path = reverse('post_list_by_tag', kwargs={'tag_slug': 'slug'})
        assert resolve(path).view_name == 'post_list_by_tag'
        assert resolve(path).func == post_list

    def test_post_detail_url(self):
        path = reverse('post_detail', kwargs={'pk': 1})
        assert resolve(path).view_name == 'post_detail'
        assert resolve(path).func == post_detail

    def test_dialogs_url(self):
        path = reverse('dialogs')
        assert resolve(path).view_name == 'dialogs'
        assert resolve(path).func.view_class == DialogsView

    def test_activate_url(self):
        path = reverse('activate', kwargs={'uidb64': 'Njc', 'token': '5gg-0cb3b3b4f111ed7029fa'})
        assert resolve(path).view_name == 'activate'
        assert resolve(path).func == activate
