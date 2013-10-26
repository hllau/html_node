# -*- coding: utf-8 -*-
from .tags import Node, Tag, html_node as n


__all__ = ['Placeholder', 'placeholder', 'BaseTemplate', 'BaseLayout']


class Placeholder(Node):
    """Stub to fill in other template."""
    def __init__(self, name):
        self.name = name

def fill(tag, placeholders):
    """Recursively fill in the placeholders of descendents of any Tag in place."""
    if isinstance(tag, Tag):
        for index in range(0, len(tag.children)):
            if isinstance(tag.children[index], Placeholder):
                tag.children[index] = fill(placeholders[tag.children[index].name], placeholders=placeholders)
            else:
                tag.children[index] = fill(tag.children[index], placeholders=placeholders)
    return tag


def placeholder(arg):
    """Decorate a class method to create a placeholder with the same name as the method name.

    ... 2013-07-07 - add ability to be use as Placeholder anchor in the template also
    """
    if isinstance(arg, basestring):
        # put an anchor
        return Placeholder(arg)
    elif hasattr(arg, '__call__'):
        # register the function to relate to the anchor
        arg.is_placeholder = True
        return arg


class BaseTemplate(Node):
    default_context = {}

    def __init__(self, context={}, **kwargs):
        """The most basic template, which uses placeholder for rendering.

        :param context: A dictionary of Context to bring into the template
        :param kwargs: Key word argument which overrides the value in the context
        """
        self.__placeholders = {}
        self.context = {}
        self.context.update(self.default_context)
        self.context.update(context)
        self.context.update(kwargs)

        # Make shorthand available
        self.c = self.context.get

        self.__extract_placeholders()

    def __extract_placeholders(self):
        """Get placeholders from its declared methods which decorated as `placeholder`."""
        for key in dir(self):
            method = getattr(self, key)
            if getattr(method, 'is_placeholder', False):
                self.__placeholders[method.__name__] = method()

    def template(self):
        raise NotImplementedError

    def render(self):
        return self.__unicode__()

    def __unicode__(self):
        return fill(self.template(), self.__placeholders).render()

    def __str__(self):
        return self.__unicode__()


class BaseLayout(BaseTemplate):
    title = 'Welcome!'

    def template(self):
        return n.html5(n.head(Placeholder('head')), n.body(Placeholder('body')))

    @placeholder
    def head(self):
        return n.title(self.title)

    @placeholder
    def body(self):
        return n.div(class_="container")
