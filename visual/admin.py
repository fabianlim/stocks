from django.contrib import admin
from models import Search


# class SearchInline(admin.TabularInline):
#     model = Search
#     extra = 3

# class SessionAdmin(admin.ModelAdmin):
#     inlines = [SearchInline]
#     list_display = ('session_datetime', 'numSearches', 'was_recent')
#     list_filter = ['session_datetime']

# Register your models here.
# admin.site.register(Session, SessionAdmin)
admin.site.register(Search)
