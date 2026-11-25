from django.contrib import admin

from .models import Comment, Community, Like, Post, Report

admin.site.register(Community)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'community', 'created_at')
    list_filter = ('community',)
    search_fields = ('title', 'body')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('post', 'reporter', 'short_reason', 'is_handled', 'created_at')
    list_filter = ('is_handled',)
    actions = ['mark_handled', 'delete_reported_posts']

    @admin.display(description='Reason')
    def short_reason(self, obj):
        return obj.reason[:60]

    @admin.action(description='Mark selected reports as handled')
    def mark_handled(self, request, queryset):
        updated = queryset.update(is_handled=True)
        self.message_user(request, f'{updated} report(s) marked as handled.')

    @admin.action(description='Delete the posts of the selected reports')
    def delete_reported_posts(self, request, queryset):
        posts = Post.objects.filter(reports__in=queryset).distinct()
        count = posts.count()
        posts.delete()
        self.message_user(request, f'{count} post(s) deleted.')    