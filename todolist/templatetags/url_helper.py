from django import template

register = template.Library()


@register.simple_tag
def relative_url(querystring_key, querystring_value, urlencode=''):
    querystring = f'{querystring_key}={querystring_value}'

    if urlencode:
        querystrings = urlencode.split('&')
        filtered_querystring = []
        to_append_new_querystring = True

        for old_querystring in querystrings:
            if old_querystring.split('=')[0] == querystring_key:
                filtered_querystring.append(querystring)
                to_append_new_querystring = False
                continue
            filtered_querystring.append(old_querystring)

        encoded_querystring = '&'.join(filtered_querystring)

        mapper = {
            True: f'{encoded_querystring}&{querystring}',
            False: f'{encoded_querystring}',
        }

        querystring = mapper[to_append_new_querystring]

    return f'?{querystring}'
