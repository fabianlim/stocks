import os
from datetime import datetime, timedelta
from random import randint


# copied from the web
def random_date(start, end):
    return start + timedelta(
        seconds=randint(0, int((end - start).total_seconds())))


def populate():
    tformat = '%m/%d/%Y %I:%M %p'
    s = add_session(datetime=random_date(
        datetime.strptime('1/1/2008 1:30 PM', tformat),
        datetime.strptime('1/1/2010 1:30 PM', tformat)))

    q = add_query(session=s,
                  text="""
                       SELECT * FROM yahoo.finance.quote
                       WHERE symbol in ("GOOG", "MSFT")
                       """)

    # Print out what we have added to the user.
    for s in Session.objects.all():
        for q in s.query_set.all():
            print "- {0} - {1}".format(str(s), str(q))


def add_session(datetime):
    s = Session.objects.get_or_create(session_datetime=datetime)[0]
    return s


def add_query(session, text):
    q = Search.objects.get_or_create(session=session, text=text)[0]
    return q

# Start execution here!
if __name__ == '__main__':
    print "Starting Visual population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stocks.settings')
    from visual.models import Session, Search
    populate()
