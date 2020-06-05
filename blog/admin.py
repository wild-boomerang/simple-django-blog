from django.contrib import admin
from .models import Post, Comment, Profile, Likes, Message, Chat, Feedback
from django.core.mail import send_mail, BadHeaderError


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
    list_display = ['email_reply', 'email_address', 'email_reply_capt', 'email_reply_text']
    list_filter = ('email_reply', 'email_address', 'email_reply_capt', 'email_reply_text', )
    search_fields = ('email_reply', 'email_address', 'email_reply_capt', 'email_reply_text', )
    # prepopulated_fields = {'slug': ('title',)}
    # date_hierarchy = 'date_of_birth'
    ordering = ['email_reply', 'email_address', 'email_reply_capt', 'email_reply_text']

    def save_model(self, request, obj, form, change):
        if not obj.email_reply:
            return
        if not obj.email_reply_text:
            return
        # если для хранения e-mail используется не поле email_address, а другое - заменяем название. Если оно не
        # строкового типа - приводим к строке
        if not obj.email_address:
            return

        # сюда можно ещё дописать алгорит проверки, правильно ли введен e-mail
        # впрочем, если адрес окажется некорректным, ничего не сломается. Письмо просто не будет отправлено

        # список получателей (получатели не видят чужие e-mail)
        # если нужно отправлять кому-то ещё, дописываем адреса в этот список через запятую
        # желательно добавить свой адрес электронной почты, чтобы видеть, что вы отправили
        recipients = [
            obj.email_address,
        ]

        for mail in recipients:
            try:
                send_mail(obj.email_reply_capt, obj.email_reply_text, 'skyblogsender@gmail.com', [mail])
            except BadHeaderError:
                # если есть какие-либо предпочтения в обработке случаев, когда e-mail указан неправильно - описываем
                # обработку таких случаев тут. В моём примере такие адреса просто пропускаются, сообщения отправлены
                # не будут
                pass

        # сбрасываем поля, чтобы при следующем сохранении модели случайно не отправить письмо ещё раз
        # поле адреса электронной почты я не сбрасываю. Вдруг пригодится ещё
        obj.email_reply = False
        # obj.email_reply_capt = ''
        # obj.email_reply_text = None
        super().save_model(request, obj, form, change)


admin.site.register(Feedback, EmailReply)
