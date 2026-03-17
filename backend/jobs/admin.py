from django.contrib import admin
from .models import Job

# Register Job model for admin interface
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'employer', 'location', 'salary_min', 'salary_max', 'job_type', 'posted_at']
    list_filter = ['job_type', 'posted_at', 'location']
    search_fields = ['title', 'description', 'employer__email']
    readonly_fields = ['posted_at']
    date_hierarchy = 'posted_at'
