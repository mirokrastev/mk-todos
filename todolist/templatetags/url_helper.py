from django import template

register = template.Library()


@register.simple_tag
def relative_url(field_name, value, urlencode=''):
    url = f'?{field_name}={value}'
    if urlencode:
        querystrings = urlencode.split('&')
        filtered_querystring = [querystring for querystring in querystrings
                                if querystring.split('=')[0] != field_name]
        encoded_querystring = '&'.join(filtered_querystring)
        if encoded_querystring:
            url = f'?{encoded_querystring}&{url.replace("?", "")}'
    return url
