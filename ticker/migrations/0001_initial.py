# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Ticker'
        db.create_table(u'ticker_ticker', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('symbol', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('industry', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('industry_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'ticker', ['Ticker'])

        # Adding model 'StockRecord'
        db.create_table(u'ticker_stockrecord', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'ticker', ['StockRecord'])

        # Adding model 'Quote'
        db.create_table(u'ticker_quote', (
            (u'stockrecord_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['ticker.StockRecord'], unique=True, primary_key=True)),
            ('ticker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ticker.Ticker'])),
            ('last_trade_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('last_trade_time', self.gf('django.db.models.fields.TimeField')(null=True)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('time', self.gf('django.db.models.fields.TimeField')(auto_now_add=True, blank=True)),
            ('annual_gain', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('book_value', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('change', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('change_inpercent', self.gf('ticker.fields.PercentField')(max_length=10, null=True)),
            ('dividend_share', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('dividend_yield', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('eps_est_current_year', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('eps_est_next_quarter', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('eps_est_next_year', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('earnings_share', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('fifty_day_MA', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('oneyr_target_price', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('peg_ratio', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('pe_ratio', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('ebitda', self.gf('ticker.fields.BigFloatField')(max_length=20, null=True)),
            ('market_cap', self.gf('ticker.fields.BigFloatField')(max_length=20, null=True)),
            ('percent_change_from_year_high', self.gf('ticker.fields.PercentField')(max_length=10, null=True)),
            ('percent_change', self.gf('ticker.fields.PercentField')(max_length=10, null=True)),
            ('percent_change_fifty_MA', self.gf('ticker.fields.PercentField')(max_length=10, null=True)),
            ('percent_change_twohund_MA', self.gf('ticker.fields.PercentField')(max_length=10, null=True)),
            ('percent_change_from_year_low', self.gf('ticker.fields.PercentField')(max_length=10, null=True)),
            ('price_book', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('price_eps_est_current_year', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('price_eps_est_next_year', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('price_sales', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('twohund_MA', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('volume', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('year_high', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('year_low', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('last_trade_price', self.gf('django.db.models.fields.FloatField')(null=True)),
        ))
        db.send_create_signal(u'ticker', ['Quote'])

        # Adding model 'Historical'
        db.create_table(u'ticker_historical', (
            (u'stockrecord_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['ticker.StockRecord'], unique=True, primary_key=True)),
            ('ticker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ticker.Ticker'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('volume', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('open', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('close', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
        ))
        db.send_create_signal(u'ticker', ['Historical'])


    def backwards(self, orm):
        # Deleting model 'Ticker'
        db.delete_table(u'ticker_ticker')

        # Deleting model 'StockRecord'
        db.delete_table(u'ticker_stockrecord')

        # Deleting model 'Quote'
        db.delete_table(u'ticker_quote')

        # Deleting model 'Historical'
        db.delete_table(u'ticker_historical')


    models = {
        u'ticker.historical': {
            'Meta': {'object_name': 'Historical', '_ormbases': [u'ticker.StockRecord']},
            'close': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'open': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            u'stockrecord_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['ticker.StockRecord']", 'unique': 'True', 'primary_key': 'True'}),
            'ticker': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ticker.Ticker']"}),
            'volume': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'ticker.quote': {
            'Meta': {'object_name': 'Quote', '_ormbases': [u'ticker.StockRecord']},
            'annual_gain': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'book_value': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'change': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'change_inpercent': ('ticker.fields.PercentField', [], {'max_length': '10', 'null': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dividend_share': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'dividend_yield': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'earnings_share': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'ebitda': ('ticker.fields.BigFloatField', [], {'max_length': '20', 'null': 'True'}),
            'eps_est_current_year': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'eps_est_next_quarter': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'eps_est_next_year': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'fifty_day_MA': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'last_trade_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'last_trade_price': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'last_trade_time': ('django.db.models.fields.TimeField', [], {'null': 'True'}),
            'market_cap': ('ticker.fields.BigFloatField', [], {'max_length': '20', 'null': 'True'}),
            'oneyr_target_price': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'pe_ratio': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'peg_ratio': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'percent_change': ('ticker.fields.PercentField', [], {'max_length': '10', 'null': 'True'}),
            'percent_change_fifty_MA': ('ticker.fields.PercentField', [], {'max_length': '10', 'null': 'True'}),
            'percent_change_from_year_high': ('ticker.fields.PercentField', [], {'max_length': '10', 'null': 'True'}),
            'percent_change_from_year_low': ('ticker.fields.PercentField', [], {'max_length': '10', 'null': 'True'}),
            'percent_change_twohund_MA': ('ticker.fields.PercentField', [], {'max_length': '10', 'null': 'True'}),
            'price_book': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'price_eps_est_current_year': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'price_eps_est_next_year': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'price_sales': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            u'stockrecord_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['ticker.StockRecord']", 'unique': 'True', 'primary_key': 'True'}),
            'ticker': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ticker.Ticker']"}),
            'time': ('django.db.models.fields.TimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'twohund_MA': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'volume': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'year_high': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'year_low': ('django.db.models.fields.FloatField', [], {'null': 'True'})
        },
        u'ticker.stockrecord': {
            'Meta': {'object_name': 'StockRecord'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'ticker.ticker': {
            'Meta': {'object_name': 'Ticker'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'industry_id': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'symbol': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        }
    }

    complete_apps = ['ticker']