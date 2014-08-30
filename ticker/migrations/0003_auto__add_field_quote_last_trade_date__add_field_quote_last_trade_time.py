# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Quote.last_trade_date'
        db.add_column(u'ticker_quote', 'last_trade_date',
                      self.gf('django.db.models.fields.DateField')(null=True),
                      keep_default=False)

        # Adding field 'Quote.last_trade_time'
        db.add_column(u'ticker_quote', 'last_trade_time',
                      self.gf('django.db.models.fields.TimeField')(null=True),
                      keep_default=False)


        # Changing field 'Quote.date'
        db.alter_column(u'ticker_quote', 'date', self.gf('django.db.models.fields.DateField')(auto_now_add=True))

        # Changing field 'Quote.time'
        db.alter_column(u'ticker_quote', 'time', self.gf('django.db.models.fields.TimeField')(auto_now_add=True))

    def backwards(self, orm):
        # Deleting field 'Quote.last_trade_date'
        db.delete_column(u'ticker_quote', 'last_trade_date')

        # Deleting field 'Quote.last_trade_time'
        db.delete_column(u'ticker_quote', 'last_trade_time')


        # Changing field 'Quote.date'
        db.alter_column(u'ticker_quote', 'date', self.gf('django.db.models.fields.DateField')())

        # Changing field 'Quote.time'
        db.alter_column(u'ticker_quote', 'time', self.gf('django.db.models.fields.TimeField')())

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