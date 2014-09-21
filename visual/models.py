from django.db import models
# import datetime
# from django.utils import timezone

# Create your models here.
# class Session(models.Model):
#     session_datetime = models.DateTimeField('datetime started')
#
#     def numSearches(self):
#         return self.query_set.count()
#
#         return self.session_datetime >= (timezone.now() -
#             datetime.timedelta(days=1))
#
#     def __unicode__(self):
#         return self.session_datetime.strftime('%m/%d/%Y %I:%M %p')


class Search(models.Model):
    """ Model that holds a search query """

    # session = models.ForeignKey(Session)
    datetime = models.DateTimeField('datetime started')
    text = models.CharField(max_length=200)

    def __unicode__(self):
        # return self.text
        return self.datetime.strftime('%m/%d/%Y %I:%M %p') + ": " + self.text
