# -*- coding: utf-8 -*-
"""A simple library to handle HTML tags and templates."""
from .tags import TagSingletonError, Node, html_node
from .templates import Placeholder, BaseTemplate, BaseLayout, Tag, placeholder

__all__ = [
    'TagSingletonError', 'Node',
    'Placeholder', 'BaseTemplate', 'BaseLayout', 'Tag', 'placeholder',
    'html_node'
]
