from django.db import models

import datetime

from ticker.fields import PercentField, BigFloatField

# for south migrations
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^ticker\.fields\.PercentField"])
add_introspection_rules([], ["^ticker\.fields\.BigFloatField"])


def get_fields(model, name_filter_list=None):
    """ helper function to return model fields """
    if name_filter_list is None:
        return model._meta.fields
    else:
        return [f for f in get_fields(model) if
                f.verbose_name in name_filter_list]


def get_field_verbose_names(model, name_filter_list=None):
    """ helper function to return model fields verbose names """

    return [f.verbose_name for f in get_fields(model, name_filter_list)]


def get_dateformat(model):
    """ helper function to return datetime format """
    return model._dateformat


class Ticker(models.Model):
    """ model for stock ticker """

    symbol = models.CharField(
        max_length=20,
        unique=True)

    name = models.CharField(
        max_length=200)

    industry = models.CharField(
        max_length=40)

    industry_id = models.IntegerField()

    def __unicode__(self):
        return self.name

    @staticmethod
    def query_to_models(ticker_name, query, model):
        """
        to parse the yql query_result into a format acceptable
        by some django StockRecord model and stores it.
        ticker_name: foreign key for the StockRecord
        query_result: from the yql (or external DB query)
        model: StockRecord model
        """
        # this returns a tuple, so need to index first elem
        tick = Ticker.objects.get_or_create(symbol=ticker_name)[0]
        # call the to_model method of Query object and link to ticker
        query.to_model(model, ticker=tick)
        # return tick
        return tick


def parse_query_result(d, fields, dateformat):
    """
    parse the query result into a dict
    dict is essentially the kwargs needed for model creation
    """

    # TODO : can be made alot simpler
    # basically its just swapping keys of the dict

    p = dict()
    for f in fields:
        # TODO : I should list out all the formats when I have time
        if isinstance(f, models.DateField):
            p[f.name] = datetime.datetime.strptime(d[f.verbose_name],
                                                   dateformat)
        else:
            p[f.name] = d[f.verbose_name]

    return p


class Quote(models.Model):
    """ model for quote record """
    ticker = models.ForeignKey(Ticker)

    last_trade_date = models.DateField(
        verbose_name='LastTradeDate',
        null=True)

    last_trade_time = models.TimeField(
        verbose_name='LastTradeTime',
        null=True)

    date = models.DateField(
        verbose_name='Date',
        auto_now_add=True)

    time = models.TimeField(
        verbose_name='Time',
        auto_now_add=True)

    annual_gain = models.FloatField(
        verbose_name='AnnualizedGain',
        null=True)

    book_value = models.FloatField(
        verbose_name='BookValue',
        null=True)

    change = models.FloatField(
        verbose_name='Change',
        null=True)

    change_inpercent = PercentField(
        verbose_name='ChangeinPercent',
        null=True)

    dividend_share = models.FloatField(
        verbose_name='DividendShare',
        null=True)

    dividend_yield = models.FloatField(
        verbose_name='DividendYield',
        null=True)

    eps_est_current_year = models.FloatField(
        verbose_name='EPSEstimateCurrentYear',
        null=True)

    eps_est_next_quarter = models.FloatField(
        verbose_name='EPSEstimateNextQuarter',
        null=True)

    eps_est_next_year = models.FloatField(
        verbose_name='EPSEstimateNextYear',
        null=True)

    earnings_share = models.FloatField(
        verbose_name='EarningsShare',
        null=True)

    fifty_day_MA = models.FloatField(
        verbose_name='FiftydayMovingAverage',
        null=True)

    oneyr_target_price = models.FloatField(
        verbose_name='OneyrTargetPrice',
        null=True)

    peg_ratio = models.FloatField(
        verbose_name='PEGRatio',
        null=True)

    pe_ratio = models.FloatField(
        verbose_name='PERatio',
        null=True)

    ebitda = BigFloatField(
        verbose_name='EBITDA',
        null=True)

    market_cap = BigFloatField(
        verbose_name='MarketCapitalization',
        null=True)

    percent_change_from_year_high = PercentField(
        verbose_name='PercebtChangeFromYearHigh',
        null=True)

    percent_change = PercentField(
        verbose_name='PercentChange',
        null=True)

    percent_change_fifty_MA = PercentField(
        verbose_name='PercentChangeFromFiftydayMovingAverage',
        null=True)

    percent_change_twohund_MA = PercentField(
        verbose_name='PercentChangeFromTwoHundreddayMovingAverage',
        null=True)

    percent_change_from_year_low = PercentField(
        verbose_name='PercentChangeFromYearLow',
        null=True)

    price_book = models.FloatField(
        verbose_name='PriceBook',
        null=True)

    price_eps_est_current_year = models.FloatField(
        verbose_name='PriceEPSEstimateCurrentYear',
        null=True)

    price_eps_est_next_year = models.FloatField(
        verbose_name='PriceEPSEstimateNextYear',
        null=True)

    price_sales = models.FloatField(
        verbose_name='PriceSales',
        null=True)

    twohund_MA = models.FloatField(
        verbose_name='TwoHundreddayMovingAverage',
        null=True)

    volume = models.IntegerField(
        verbose_name='Volume',
        null=True)

    year_high = models.FloatField(
        verbose_name='YearHigh',
        null=True)

    year_low = models.FloatField(
        verbose_name='YearLow',
        null=True)

    last_trade_price = models.FloatField(
        verbose_name='LastTradePriceOnly',
        null=True)

    _dateformat = '%m/%d/%Y'

    def __unicode__(self):
        return (self.ticker.name +
                ' ' +
                self.time.strftime('%H:%M:%S') +
                ' ' +
                self.date.strftime('%Y-%m-%d'))


class Historical(models.Model):
    """
    class to store the historical record.
    Not sure if we will be using this forward
    """
    ticker = models.ForeignKey(Ticker)
    date = models.DateField(
        verbose_name='Date')

    volume = models.IntegerField(
        verbose_name='Volume',
        default=0)

    open = models.DecimalField(
        verbose_name='Open',
        max_digits=6,
        decimal_places=2)

    close = models.DecimalField(
        verbose_name='Close',
        max_digits=6,
        decimal_places=2)

    _dateformat = '%Y-%m-%d'

    def __unicode__(self):
        return self.ticker.name + ' ' + self.date.strftime('%Y-%m-%d')
