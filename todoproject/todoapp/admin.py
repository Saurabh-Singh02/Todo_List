from django.contrib import admin
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'completed', 'priority', 'created_at']
    list_filter = ['completed', 'priority', 'created_at']
    search_fields = ['title', 'description', 'user__username']
    date_hierarchy = 'created_at'

    # admin
    # Test@1234



admin.site.site_header = "TodoApp Admin"
admin.site.site_title = "TodoApp Admin Portal"      