from django.db import models

# Create your models here.
class Session(models.Model):
    session_datetime = models.DateTimeField('datetime started')

    def __unicode__(self):
        return self.session_datetime.strftime('%m/%d/%Y %I:%M %p')

class Query(models.Model):
    session = models.ForeignKey(Session)
    text = models.CharField(max_length=200)

    def __unicode__(self):
        return self.text

