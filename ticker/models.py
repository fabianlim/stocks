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
    name = models.CharField(max_length=4, unique=True)

    def __unicode__(self):
        return self.name

    # to go from yql to models
    # the query_result is a dict with keys in the field.name
    # format. This is necessary for the models get_or_create
    # API
    @staticmethod
    def query_to_models(ticker_name, query_result):
        # this returns a tuple, so need to index first elem
        tick = Ticker.objects.get_or_create(name=ticker_name)[0]

        # query_result is a dict with keys according to field.name
        for q in query_result:
            try:
                parsed = Quote.parse_query_result(q)
                tick.quote_set.get_or_create(**parsed)
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
    def get_fields():
        return [f.verbose_name for f in Quote._meta.fields]

    # the query result passed in is a dictionary d
    # d.keyvalues() will be those used in the
    # external database (these are captured in f.verbose_name)
    # need to convert the keys to f.name
    @staticmethod
    def parse_query_result(d):
        p = dict()
        for f in Quote._meta.fields:
            if f.verbose_name in d:
                # TODO : I should list out all the formats when I have time
                if isinstance(f,models.DateField):
                    p[f.name] = datetime.datetime.strptime(d[f.verbose_name], '%m/%d/%Y')
                else:
                    p[f.name] = d[f.verbose_name]
        return p

class Quote(StockRecord):
    ticker = models.ForeignKey(Ticker)
    date = models.DateField(verbose_name='LastTradeDate')
    time = models.TimeField(verbose_name='LastTradeTime')

    change = models.FloatField(verbose_name='Change')
    ask    = models.FloatField(verbose_name='Ask') # maybe should use Decimal
    #open   = models.DecimalField(max_digits=6,
    #            decimal_places=2,
    #            verbose_name='Open')

    def __unicode__(self):
        return self.time.strftime('%H:%M:%S') + ' ' + self.date.strftime('%Y-%m-%d')


