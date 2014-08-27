# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Ticker.symbol'
        db.alter_column(u'ticker_ticker', 'symbol', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20))

    def backwards(self, orm):

        # Changing field 'Ticker.symbol'
        db.alter_column(u'ticker_ticker', 'symbol', self.gf('django.db.models.fields.CharField')(max_length=10, unique=True))

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
            'ask': ('django.db.models.fields.FloatField', [], {}),
            'change': ('django.db.models.fields.FloatField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'stockrecord_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['ticker.StockRecord']", 'unique': 'True', 'primary_key': 'True'}),
            'ticker': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ticker.Ticker']"}),
            'time': ('django.db.models.fields.TimeField', [], {})
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