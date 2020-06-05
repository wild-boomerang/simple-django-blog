from django.conf import settings
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    like_quantity = models.BigIntegerField(default=0)

    class Meta:
        ordering = ('-published_date', )

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    like_quantity = models.BigIntegerField(default=0)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(blank=True, null=True)
    verified = models.BooleanField(default=False)
    # photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

    # def like(self, post_pk):
    #     post = get_object_or_404(Post, pk=post_pk)


class Likes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='like')
    already_liked = models.BooleanField(default=False)

    def invert_like(self):
        if self.already_liked:
            self.already_liked = False
        else:
            self.already_liked = True

    def __str__(self):
        return self.already_liked


class Chat(models.Model):
    members = models.ManyToManyField(Profile)
    CHAT = 'C'
    DIALOG = 'D'
    CHAT_TYPE_CHOICES = ((DIALOG, 'Dialog'), (CHAT, 'Chat'))
    type = models.CharField(max_length=1, choices=CHAT_TYPE_CHOICES, default=DIALOG)

    def get_absolute_url(self):
        return 'users:messages', (), {'chat_id': self.pk}


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    content = models.TextField()
    departure_date = models.DateTimeField(blank=True, null=True, default=timezone.now)
    is_read = models.BooleanField(default=False)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat')

    class Meta:
        ordering = ['departure_date']

    def __str__(self):
        return self.content


class Feedback(models.Model):
    email_reply = models.BooleanField('Отправить ответ на e-mail')
    email_address = models.CharField('e-mail адрес для ответа', blank=True, max_length=500)  # если email передаёт
    # пользователь, это поле необязательно. Вместо него можно использовать то, которое уже предназначено для email
    email_reply_capt = models.CharField('Заголовок ответа на e-mail', blank=True, max_length=500)
    email_reply_text = models.TextField('Текст ответа на e-mail', null=True, blank=True)
