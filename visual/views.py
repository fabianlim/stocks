from django.shortcuts import render
from visual.forms import SessionForm
from visual.models import Query

# index view with the query searchbar
def index(request):

     # A HTTP POST?
    if request.method == 'POST':
        form = SessionForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():

            # Save the new category to the database.
            session = form.save(commit=True)

            # query text
            qtext = form.cleaned_data['query']

            # creates the query
            Query.objects.get_or_create(session=session,
                    text=qtext)

            # Now call the visual view
            # The user will be shown the plot
            return visual(request, qtext)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = SessionForm()

    context = {'form': form}
    return render(request, 'visual/index.html', context)

from ticker.models import Ticker, Quote
from ticker.query import QueryInterface
from django.http import HttpResponse

# visualize view
def visual(request, qtext):

    quote = QueryInterface.query_quote(','.join(Quote.get_fields()),
            qtext)

    if quote.count > 0:
        # will create the entries
        tick = Ticker.query_to_models(qtext, quote.results)

        # get the plot (in string format)
        plt_str = tick.plot()

        # save will handle duplicate entries
        # quote.save()
        #context = {'plt_str': plt_str}
        #return render(request, 'visual/plot.html', context)

        return HttpResponse(plt_str, content_type='image/png')
    else:
        print "did not get any query result with qtext={}".format(qtext)


