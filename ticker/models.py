from django.db import models

from matplotlib import pylab
from pylab import *
import PIL
import PIL.Image
import StringIO

# sample view to plot a graph
def dummpy_graph():
    x = [1,2,3,4,5,6]
    y = [5, 2, 6, 1, -1, 0]
    plot(x,y, linewidth=2)

    xlabel('x axis')
    ylabel('y axis')
    title('my graph')

    buffer = StringIO.StringIO()
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()
    graphIMG = PIL.Image.frombytes("RGB", canvas.get_width_height(),
            canvas.tostring_rgb())
    graphIMG.save(buffer, 'PNG')
    pylab.close()

    return buffer.getvalue()

# Create your models here.
class Ticker(models.Model):
    symbol = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    industry = models.CharField(max_length=40)
    industry_id = models.IntegerField()

    def __unicode__(self):
        return self.name

    # to go from yql to models
    # the query_result is a dict with keys in the field.name
    # format. This is necessary for the models get_or_create
    # API
    @staticmethod
    def query_to_models(ticker_name, query_result, model):
        # this returns a tuple, so need to index first elem
        tick = Ticker.objects.get_or_create(symbol=ticker_name)[0]

        # query_result is a dict with keys according to field.name
        for q in query_result:
            parsed = model.parse_query_result(q)
            try:
                model.objects.get_or_create(ticker=tick, **parsed)
            except Exception as e:
                print """add quote {} failed:
                    parsed as {}""".format(q, parsed)
                print e

        return tick

    # method to plot
    def plot(self):
        return dummpy_graph()

# parent class for a single entry
class StockRecord(models.Model):
    # have to use the _meta tag to get fields
    # returns the verbose names (database key names)
    @staticmethod
    def _get_fields():
        return [f.verbose_name for f in Quote._meta.fields]

    @classmethod
    def get_fields(cls):
        return cls._get_fields()

    # the query result passed in is a dictionary d
    # d.keyvalues() will be those used in the
    # external database (these are captured in f.verbose_name)
    # need to convert the keys to f.name
    @staticmethod
    def _parse_query_result(fields, dateformat, d):
        p = dict()
        for f in fields:
            if f.verbose_name in d:
                # TODO : I should list out all the formats when I have time
                if isinstance(f,models.DateField):
                    p[f.name] = datetime.datetime.strptime(d[f.verbose_name],
                            dateformat)
                else:
                    p[f.name] = d[f.verbose_name]
        return p

    @classmethod
    def parse_query_result(cls, d):
        return cls._parse_query_result(cls._meta.fields, cls._dateformat, d)

from ticker.fields import PercentField, BigFloatField
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^ticker\.fields\.FloatWithModifierField"])
add_introspection_rules([], ["^ticker\.fields\.PercentField"])
add_introspection_rules([], ["^ticker\.fields\.BigFloatField"])

class Quote(StockRecord):
    ticker = models.ForeignKey(Ticker)
    last_trade_date = models.DateField(verbose_name='LastTradeDate', null=True)
    last_trade_time = models.TimeField(verbose_name='LastTradeTime', null=True)

    date = models.DateField(auto_now_add=True, verbose_name='Date')
    time = models.TimeField(auto_now_add=True, verbose_name='Time')

    annual_gain = models.FloatField(verbose_name='AnnualizedGain', null=True)
    book_value = models.FloatField(verbose_name='BookValue', null=True)

    change = models.FloatField(verbose_name='Change', null=True)
    change_inpercent = PercentField(verbose_name='ChangeinPercent', null=True)

    dividend_share = models.FloatField(verbose_name='DividendShare', null=True)
    dividend_yield = models.FloatField(verbose_name='DividendYield', null=True)

    eps_est_current_year = models.FloatField(verbose_name='EPSEstimateCurrentYear', null=True)
    eps_est_next_quarter = models.FloatField(verbose_name='EPSEstimateNextQuarter', null=True)
    eps_est_next_year = models.FloatField(verbose_name='EPSEstimateNextYear', null=True)
    earnings_share = models.FloatField(verbose_name='EarningsShare', null=True)

    fifty_day_MA = models.FloatField(verbose_name='FiftydayMovingAverage', null=True)

    oneyr_target_price = models.FloatField(verbose_name='OneyrTargetPrice', null=True)

    peg_ratio = models.FloatField(verbose_name='PEGRatio', null=True)
    pe_ratio = models.FloatField(verbose_name='PERatio', null=True)

    ebitda = BigFloatField(verbose_name='EBITDA', null=True)
    market_cap = BigFloatField(verbose_name='MarketCapitalization', null=True)
    percent_change_from_year_high = PercentField(verbose_name='PercebtChangeFromYearHigh', null=True)
    percent_change = PercentField(verbose_name='PercentChange', null=True)
    percent_change_fifty_MA = PercentField(verbose_name='PercentChangeFromFiftydayMovingAverage', null=True)
    percent_change_twohund_MA = PercentField(verbose_name='PercentChangeFromTwoHundreddayMovingAverage', null=True)
    percent_change_from_year_low = PercentField(verbose_name='PercentChangeFromYearLow', null=True)

    price_book = models.FloatField(verbose_name='PriceBook', null=True)
    price_eps_est_current_year = models.FloatField(verbose_name='PriceEPSEstimateCurrentYear', null=True)
    price_eps_est_next_year = models.FloatField(verbose_name='PriceEPSEstimateNextYear', null=True)
    price_sales = models.FloatField(verbose_name='PriceSales', null=True)

    twohund_MA = models.FloatField(verbose_name='TwoHundreddayMovingAverage', null=True)

    volume = models.IntegerField(verbose_name='Volume', null=True)
    year_high = models.FloatField(verbose_name='YearHigh', null=True)
    year_low = models.FloatField(verbose_name='YearLow', null=True)

    last_trade_price = models.FloatField(verbose_name='LastTradePriceOnly', null=True)

    _dateformat = '%m/%d/%Y'

    def __unicode__(self):
        return self.ticker.name + ' ' + self.time.strftime('%H:%M:%S') + ' ' + self.date.strftime('%Y-%m-%d')

"""add quote {u'Volume': u'984100', u'Symbol': u'GOOG', u'Adj_Close': u'590.60', u'High': u'592.50', u'Low': u'584.75', u'Date': u'2014-07-28', u'Close': u'590.60', u'Open': u'588.07'} failed:
"""
class Historical(StockRecord):
    ticker = models.ForeignKey(Ticker)
    date = models.DateField(verbose_name='Date')

    volume = models.IntegerField(default=0)

    open   = models.DecimalField(max_digits=6,
                decimal_places=2,
                verbose_name='Open')

    close  = models.DecimalField(max_digits=6,
                decimal_places=2,
                verbose_name='Close')

    _dateformat = '%Y-%m-%d'

    def __unicode__(self):
        return self.ticker.name + ' ' + self.date.strftime('%Y-%m-%d')

