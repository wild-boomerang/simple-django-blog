from django.contrib import admin
from .models import Post, Comment, Profile, Likes


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