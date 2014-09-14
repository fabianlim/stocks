from django.shortcuts import render
from visual.forms import SearchForm
from visual.models import Search

from ticker.models import Ticker, Quote
# index view with the query searchbar
def index(request):

     # A HTTP POST?
    if request.method == 'POST':
        form = SearchForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():

            # Save the new category to the database.
            search = form.save(commit=True)

            # search text
            #qtext = form.cleaned_data['query']

            ## creates the search
            #Search.objects.get_or_create(session=session,
            #        text=qtext)
            Ticker.objects.get(symbol=search.text)

            # Now call the visual view
            # The user will be shown the plot
            return visual(request, search.text)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = SearchForm()

    context = {'form': form}
    return render(request, 'visual/index.html', context)

from ticker.query import QueryInterface
from django.http import HttpResponse

# visualize view
def visual(request, qtext):

    # query the quote with fields set in the model
    quote = QueryInterface.query_quote(','.join(Quote.get_fields()),
            qtext)

    if quote.count > 0:
        # will create the quote entry in the database, and return
        quote_entry = Ticker.query_to_models(qtext, quote.results, Quote)

        # get the plot (in string format)
        plt_str = tick.plot()

        # save will handle duplicate entries
        # quote.save()
        #context = {'plt_str': plt_str}
        #return render(request, 'visual/plot.html', context)

        return HttpResponse(plt_str, content_type='image/png')
    else:
        print "did not get any query result with qtext={}".format(qtext)


