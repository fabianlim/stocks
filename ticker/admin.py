from django.contrib import admin
from ticker.models import Ticker, Quote

# admin
class QuoteAdmin(admin.ModelAdmin):
    fieldsets=[
        ("Basic Infomation", {'fields': ['ticker', 'date', 'time']}),
        ("Pricing", {'fields': ['change', 'ask']}),
    ]
    list_display = ('time', 'date', 'ticker')
    list_filter = ['time', 'date']
    search_fields = ['ticker__name']

# admin
class QuoteInline(admin.StackedInline):
    model = Quote
    extra = 10

# admin
class TickerAdmin(admin.ModelAdmin):
    inlines= [QuoteInline]

# Register your models here.
admin.site.register(Ticker, TickerAdmin)
admin.site.register(Quote, QuoteAdmin)
