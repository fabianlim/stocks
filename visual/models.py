from django.db import models
import datetime
from django.utils import timezone

# Create your models here.
class Session(models.Model):
    session_datetime = models.DateTimeField('datetime started')

    def numQueries(self):
        return self.query_set.count()

    def was_recent(self):
        return self.session_datetime >= timezone.now() - datetime.timedelta(days=1)

    def __unicode__(self):
        return self.session_datetime.strftime('%m/%d/%Y %I:%M %p')

class Query(models.Model):
    session = models.ForeignKey(Session)
    text = models.CharField(max_length=200)

    def __unicode__(self):
        return self.text

