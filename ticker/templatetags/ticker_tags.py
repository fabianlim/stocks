from django import template

register = template.Library()


@register.simple_tag
def ticker(symbol):
    """ to watch a ticker """

    # return {"ticker": {"symbol": symbol}}
    # return {"symbol": [symbol]}
    import json
    return json.dumps({"symbol": [symbol]})
