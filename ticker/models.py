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

class Quote(StockRecord):
    ticker = models.ForeignKey(Ticker)
    date = models.DateField(verbose_name='LastTradeDate')
    time = models.TimeField(verbose_name='LastTradeTime')

    change = models.FloatField(verbose_name='Change')
    change_realtime = models.FloatField(verbose_name='ChangeRealtime',
            default=0.0)
    ask    = models.FloatField(verbose_name='Ask') # maybe should use Decimal
    volume = models.IntegerField(verbose_name='Volume',
            default=0)
    last_trade_price = models.FloatField(verbose_name='LastTradePriceOnly',
            default=0.00)
    #open   = models.DecimalField(max_digits=6,
    #            decimal_places=2,
    #            verbose_name='Open')

    _dateformat = '%m/%d/%Y'

    def __unicode__(self):
        return self.time.strftime('%H:%M:%S') + ' ' + self.date.strftime('%Y-%m-%d')

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
        return self.ticker__name + ' ' + self.date.strftime('%Y-%m-%d')

