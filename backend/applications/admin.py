from django.contrib import admin
from .models import Application

# Register Application model for admin interface
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    # Columns shown in list view
    list_display = ['id', 'seeker', 'job', 'status', 'applied_at']

    # Filters in right sidebar
    list_filter = ['status', 'applied_at']

    # Search bar functionality
    search_fields = ['seeker__email', 'job__title', 'seeker__username']

    # Fields that cannot be edited
    readonly_fields = ['applied_at', 'seeker', 'job']

    # Date-based drill-down navigation
    date_hierarchy = 'applied_at'

    # Order by most recent first
    ordering = ['-applied_at']
