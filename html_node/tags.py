# -*- coding: utf-8 -*-
import copy
from cgi import escape
from .utils import TAG_TYPE_OPEN, TAG_TYPE_CLOSE, TAG_TYPE_SINGLETON
from .utils import render_tag, html_params


__all__ = ['TagSingletonError', 'Node', 'Tag', 'html_node']


class TagSingletonError(Exception):
    """Raised when a tag is not allowed to have children."""
    pass


class Node(object):
    """Base type for all node objects."""
    pass


class Tag(Node):
    tagname = None
    default_attributes = {}
    default_classes = []
    required_attributes = []
    singleton = False
    children_delimiter = u''
    safe = False

    def __init__(self, *args, **kwargs):
        # Guess tagname if not provided
        if self.tagname is None:
            self.tagname = self.__class__.__name__.lower()

        # Append children if not singleton
        self.children = []
        self.children.extend(list(args))
        self.children.extend(kwargs.get('children', []))
        if 'children' in kwargs:
            del kwargs['children']
        if len(self.children) > 0 and self.singleton:
            raise TagSingletonError

        # Assigning tag attributes, override defaults
        self.attributes = self.default_attributes.copy()
        if 'name' in kwargs:
            self.name = kwargs.get('name')
        self._classes = None
        if 'class_' in kwargs:
            self.classes = kwargs['class_']
            del kwargs['class_']
        if 'safe' in kwargs:
            self.safe = kwargs['safe']
            del kwargs['safe']
        if 'children_delimiter' in kwargs:
            self.children_delimiter = kwargs['children_delimiter']
            del kwargs['children_delimiter']

        for key in kwargs:
            escaped_key = key[:-1] if key.endswith('_') else key
            escaped_key = escaped_key.replace('_', '-')
            self.attributes[escaped_key] = kwargs[key]

        # Check if all required attributes are set
        for key in self.required_attributes:
            if key not in self.attributes:
                raise KeyError

    @property
    def classes(self):
        if self._classes is not None:
            return ' '.join(self._classes)
        else:
            return ' '.join(self.default_classes)

    def append(self, *args):
        if not self.singleton:
            for elm in args:
                self.children.append(elm)
        return self

    def prepend(self, *args):
        if not self.singleton:
            for elm in args[::-1]:
                self.children.insert(0, elm)
        return self

    @classes.setter
    def classes(self, value):
        self._classes = []
        self._classes.extend(self.default_classes)
        if isinstance(value, basestring):
            self._classes.extend(value.split(' '))
        elif isinstance(value, list):
            for c in value:
                if c not in self._classes:
                    self._classes.append(c)
        elif isinstance(value, dict):
            for key in value:
                if value[key]:
                    self._classes.append(key)

    def render(self):
        return self.__unicode__()

    def __call__(self, *args):
        for item in args:
            if isinstance(item, list) or isinstance(item, tuple):
                for nested_item in item:
                    self.children.append(nested_item)
            else:
                self.children.append(item)
        return self

    def __unicode__(self):
        attributes = copy.copy(self.attributes)
        inner_nodes = map(lambda x: x if isinstance(x, Node) or self.safe else escape(unicode(x)), self.children)
        inner_html = self.children_delimiter.join([unicode(n) for n in inner_nodes])
        if self.classes:
            attributes['class'] = self.classes
        attribute_partial = html_params(attributes)
        if self.singleton:
            return render_tag(self.tagname, attribute_partial, type_=TAG_TYPE_SINGLETON)
        else:
            return u'{open}{inner}{close}'.format(
                open=render_tag(self.tagname, attribute_partial, type_=TAG_TYPE_OPEN),
                inner=inner_html,
                close=render_tag(self.tagname, type_=TAG_TYPE_CLOSE)
            )

    def __str__(self):
        return self.__unicode__()


# Tags with special behaviors
# ===========================
class Html5(Tag):
    tagname = 'html'

    def __unicode__(self):
        return u'<!DOCTYPE HTML>{}'.format(super(Html5, self).__unicode__())

class Link(Tag):
    singleton = True
    default_attributes = {'rel': 'text/css'}
    required_attributes = ['href']

class Script(Tag):
    safe = True
    default_attributes = {'type': 'text/javascript'}

class A(Tag):
    default_attributes = {'href': 'javascript:void(0)'}

class Img(Tag):
    singleton = True
    required_attributes = ['src']

class Input(Tag):
    singleton = True

class Br(Tag):
    singleton = True

class Base(Tag):
    singleton = True

class Area(Tag):
    singleton = True

class Col(Tag):
    singleton = True

class Command(Tag):
    singleton = True

class Embed(Tag):
    singleton = True

class Hr(Tag):
    singleton = True

class Keygen(Tag):
    singleton = True

class Meta(Tag):
    singleton = True

class Param(Tag):
    singleton = True

class Source(Tag):
    singleton = True

class Track(Tag):
    singleton = True

class Wbr(Tag):
    singleton = True


# Factory to provide DSL shorthand in creating HTML elements
# ======================================================
class _HtmlFactory(object):
    """Provide HTML5 elements.

    A new tag class can be created using the factory dynamically. Common and valid
    elements are created here for introspection and autocompletion."""
    def __init__(self):
        self.__cache = {}
        self.__load_default_elements()

    def __load_default_elements(self):
        """Create here for IDE to introspect. Make autocomplete possible."""
        # Extracted from http://www.quackit.com/html_5/tags/
        self.a = self.__get_tag('a')
        self.abbr = self.__get_tag('abbr')
        self.address = self.__get_tag('address')
        self.area = self.__get_tag('area')
        self.article = self.__get_tag('article')
        self.aside = self.__get_tag('aside')
        self.audio = self.__get_tag('audio')
        self.b = self.__get_tag('b')
        self.base = self.__get_tag('base')
        self.bdi = self.__get_tag('bdi')
        self.bdo = self.__get_tag('bdo')
        self.blockquote = self.__get_tag('blockquote')
        self.body = self.__get_tag('body')
        self.br = self.__get_tag('br')
        self.button = self.__get_tag('button')
        self.canvas = self.__get_tag('canvas')
        self.caption = self.__get_tag('caption')
        self.cite = self.__get_tag('cite')
        self.code = self.__get_tag('code')
        self.col = self.__get_tag('col')
        self.colgroup = self.__get_tag('colgroup')
        self.command = self.__get_tag('command')
        self.data = self.__get_tag('data')
        self.datagrid = self.__get_tag('datagrid')
        self.datalist = self.__get_tag('datalist')
        self.dd = self.__get_tag('dd')
        self.details = self.__get_tag('details')
        self.dfn = self.__get_tag('dfn')
        self.div = self.__get_tag('div')
        self.dl = self.__get_tag('dl')
        self.dt = self.__get_tag('dt')
        self.em = self.__get_tag('em')
        self.embed = self.__get_tag('embed')
        self.eventsource = self.__get_tag('eventsource')
        self.fieldset = self.__get_tag('fieldset')
        self.figcaption = self.__get_tag('figcaption')
        self.figure = self.__get_tag('figure')
        self.footer = self.__get_tag('footer')
        self.form = self.__get_tag('form')
        self.h1 = self.__get_tag('h1')
        self.h2 = self.__get_tag('h2')
        self.h3 = self.__get_tag('h3')
        self.h4 = self.__get_tag('h4')
        self.h5 = self.__get_tag('h5')
        self.h6 = self.__get_tag('h6')
        self.head = self.__get_tag('head')
        self.header = self.__get_tag('header')
        self.hgroup = self.__get_tag('hgroup')
        self.hr = self.__get_tag('hr')
        self.html = self.__get_tag('html')
        self.i = self.__get_tag('i')
        self.iframe = self.__get_tag('iframe')
        self.img = self.__get_tag('img')
        self.input = self.__get_tag('input')
        self.ins = self.__get_tag('ins')
        self.kbd = self.__get_tag('kbd')
        self.keygen = self.__get_tag('keygen')
        self.label = self.__get_tag('label')
        self.legend = self.__get_tag('legend')
        self.li = self.__get_tag('li')
        self.link = self.__get_tag('link')
        self.mark = self.__get_tag('mark')
        self.map = self.__get_tag('map')
        self.menu = self.__get_tag('menu')
        self.meta = self.__get_tag('meta')
        self.meter = self.__get_tag('meter')
        self.nav = self.__get_tag('nav')
        self.noscript = self.__get_tag('noscript')
        self.object = self.__get_tag('object')
        self.ol = self.__get_tag('ol')
        self.optgroup = self.__get_tag('optgroup')
        self.option = self.__get_tag('option')
        self.output = self.__get_tag('output')
        self.p = self.__get_tag('p')
        self.param = self.__get_tag('param')
        self.pre = self.__get_tag('pre')
        self.progress = self.__get_tag('progress')
        self.q = self.__get_tag('q')
        self.ruby = self.__get_tag('ruby')
        self.rp = self.__get_tag('rp')
        self.rt = self.__get_tag('rt')
        self.s = self.__get_tag('s')
        self.samp = self.__get_tag('samp')
        self.script = self.__get_tag('script')
        self.section = self.__get_tag('section')
        self.select = self.__get_tag('select')
        self.small = self.__get_tag('small')
        self.source = self.__get_tag('source')
        self.span = self.__get_tag('span')
        self.strong = self.__get_tag('strong')
        self.style = self.__get_tag('style')
        self.sub = self.__get_tag('sub')
        self.summary = self.__get_tag('summary')
        self.sup = self.__get_tag('sup')
        self.table = self.__get_tag('table')
        self.tbody = self.__get_tag('tbody')
        self.td = self.__get_tag('td')
        self.textarea = self.__get_tag('textarea')
        self.tfoot = self.__get_tag('tfoot')
        self.th = self.__get_tag('th')
        self.thead = self.__get_tag('thead')
        self.time = self.__get_tag('time')
        self.title = self.__get_tag('title')
        self.tr = self.__get_tag('tr')
        self.track = self.__get_tag('track')
        self.u = self.__get_tag('u')
        self.ul = self.__get_tag('ul')
        self.var = self.__get_tag('var')
        self.video = self.__get_tag('video')
        self.wbr = self.__get_tag('wbr')

    def __get_tag(self, item):
        key = item.lower()
        if key in self.__cache:
            return self.__cache[key]
        else:
            # If found in special tags, use it
            class_name = key.lower().capitalize()
            if class_name in globals():
                tag_class = globals()[class_name]
                if issubclass(tag_class, Tag):
                    rv = tag_class
            else:
                rv = type(key, (Tag,), {})
            self.__cache[key] = rv
            return rv

    def __getattr__(self, item):
        """Case insensitive matching for HTML element."""
        return self.__get_tag(item)


html_node = _HtmlFactory()
