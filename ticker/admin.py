from django.contrib import admin
from models import Ticker, Quote, Historical
from models import Search


# admin
class QuoteAdmin(admin.ModelAdmin):
    fieldsets = [
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
class HistoricalAdmin(admin.ModelAdmin):
    list_display = ('date', 'open', 'close', 'ticker')
    search_fields = ['ticker__name']


# admin
class TickerAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'name', 'industry', 'industry_id')
    # list_filter = ('symbol', 'name', 'industry', 'industry_id')
    # search_fields = ['symbol', 'name']
    inlines = [QuoteInline]

# Register your models here.
admin.site.register(Ticker, TickerAdmin)
admin.site.register(Quote, QuoteAdmin)
admin.site.register(Historical, HistoricalAdmin)
admin.site.register(Search)
