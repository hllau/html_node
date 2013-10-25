# -*- coding: utf-8 -*-
import datetime
from cgi import escape


TAG_TYPE_OPEN = 1
TAG_TYPE_CLOSE = 2
TAG_TYPE_SINGLETON = 3


def render_tag(*args, **kwargs):
    """Wrap one or more strings with tag format, larger-then and smaller-then sign.
    >>> render_tag('hello')
    u'<hello>'
    >>> render_tag('hello', type_=TAG_TYPE_SINGLETON)
    u'<hello />'
    >>> render_tag('a', 'b', 'c', type_=TAG_TYPE_OPEN)
    u'<a b c>'
    """
    args = filter(lambda x: not (x is None or (isinstance(x, basestring) and x.strip()==u'')), args)
    if len(args) == 0:
        raise NameError("Tag must have at least one string input!")

    type_ = kwargs.get('type_', TAG_TYPE_OPEN)
    if type_ == TAG_TYPE_OPEN:
        template = u'<{}>'
    elif type_ == TAG_TYPE_CLOSE:
        template = u'</{}>'
    elif type_ == TAG_TYPE_SINGLETON:
        template = u'<{} />'
    else:
        raise ValueError('{} is not a valid type of tag.'.format(type_))
    return template.format(u' '.join(args))


def html_param(k, v):
    """Provide a very flexible way to create a pair of attribute-vlaue pair or just attribute."""
    partial = lambda key, value: u'{}="{}"'.format(key, escape(value, quote=True))
    if v is None:
        return k
    elif v is True:
        return partial(k, k)
    elif isinstance(v, basestring):
        return partial(k, v)
    elif isinstance(v, list):
        return partial(k, u' '.join(v))
    elif isinstance(v, dict):
        return partial(k, u' '.join([key for key, value in v.items() if value]))
    elif isinstance(v, (int, float, long)):
        return partial(k, unicode(v))
    elif isinstance(v, datetime.datetime):
        return partial(k, v.isoformat())
    else:
        raise ValueError('Unknown value is used in html parameters.')


def html_params(attributes):
    return u' '.join([html_param(k, v) for k, v in attributes.items() if v is not False])
