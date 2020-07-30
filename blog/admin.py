from django.contrib import admin
from django.db.models import QuerySet

from .models import Post, Comment, Profile, Likes, Message, Chat, Feedback
from django.core.mail import send_mail, BadHeaderError
from .email import send_email_multiproc


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'created_date', 'like_quantity')
    list_filter = ('published_date', 'created_date', 'author', 'like_quantity')
    search_fields = ('title', 'text')
    # prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'published_date'
    ordering = ['created_date', 'published_date']


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_date', 'like_quantity', 'approved_comment')
    list_filter = ('post', 'created_date', 'author', 'like_quantity', 'approved_comment')
    search_fields = ('post', 'author')
    # prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_date'
    ordering = ['created_date', 'post']


admin.site.register(Comment, CommentAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'verified']
    list_filter = ('user', 'date_of_birth', 'verified')
    search_fields = ('user', 'date_of_birth', )
    # prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date_of_birth'
    ordering = ['user', 'date_of_birth', 'verified']


admin.site.register(Profile, ProfileAdmin)


class LikesAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'already_liked']
    list_filter = ('user', 'post', 'already_liked')
    search_fields = ('user', 'date_of_birth', )
    # prepopulated_fields = {'slug': ('title',)}
    # date_hierarchy = 'date_of_birth'
    ordering = ['user', 'post', ]


admin.site.register(Likes, LikesAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'content', 'is_read', 'departure_date', 'chat']
    list_filter = ('sender', 'content', 'is_read', 'departure_date', 'chat')
    search_fields = ('sender', 'content', 'is_read', 'departure_date', 'chat')
    # prepopulated_fields = {'slug': ('title',)}
    # date_hierarchy = 'date_of_birth'
    ordering = ['sender', 'content', 'is_read', 'departure_date', 'chat']


admin.site.register(Message, MessageAdmin)


class ChatAdmin(admin.ModelAdmin):
    list_display = ['type']
    list_filter = ('members', 'type', )
    search_fields = ('members', 'type', )
    # prepopulated_fields = {'slug': ('title',)}
    # date_hierarchy = 'date_of_birth'
    ordering = ['members', 'type']


admin.site.register(Chat, ChatAdmin)


class EmailReply(admin.ModelAdmin):
    list_display = ['email_address', 'email_reply_capt', 'email_reply_text', 'email_reply']
    list_filter = ('email_reply', 'email_address', 'email_reply_capt', 'email_reply_text', )
    search_fields = ('email_reply', 'email_address', 'email_reply_capt', 'email_reply_text', )
    # prepopulated_fields = {'slug': ('title',)}
    # date_hierarchy = 'date_of_birth'
    ordering = ['email_reply', 'email_address', 'email_reply_capt', 'email_reply_text']
    actions = ['save_model']

    def save_model(self, request, obj, form=None, change=None):
        if isinstance(obj, QuerySet):
            for o in obj.all():
                o.email_reply = True
                self.test(request, o, form, change)
        else:
            self.test(request, obj, form, change)

    def test(self, request, obj, form=None, change=None):
        if not obj.email_reply:
            super().save_model(request, obj, form, change)
            return
        if not obj.email_reply_text:
            return
        if not obj.email_address:
            return

        recipients = [
            obj.email_address,
        ]

        for mail in recipients:
            try:
                send_email_multiproc(mail, obj.email_reply_capt, obj.email_reply_text)
            except BadHeaderError:
                pass

        obj.email_reply = False
        # obj.email_reply_capt = ''
        # obj.email_reply_text = None
        super().save_model(request, obj, form, change)


admin.site.register(Feedback, EmailReply)
