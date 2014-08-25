from django.contrib import admin
from visual.models import Session, Query

class QueryInline(admin.TabularInline):
    model = Query
    extra = 3

class SessionAdmin(admin.ModelAdmin):
    inlines = [QueryInline]
    list_display = ('session_datetime', 'numQueries', 'was_recent')
    list_filter = ['session_datetime']

# Register your models here.
admin.site.register(Session, SessionAdmin)
admin.site.register(Query)
