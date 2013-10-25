# -*- coding: utf-8 -*-
from nose.tools import raises, eq_, ok_
from .tags import TagSingletonError, Tag, html_node as h
from .templates import BaseLayout


class Sample(Tag):
    tagname = 'test'

def test_tag_should_generate_simple_valid_html_element():
    tag = Sample()
    eq_(unicode(tag), u'<test></test>')

def test_tag_should_generate_element_with_classes():
    tag = Sample(class_='hello')
    eq_(unicode(tag), u'<test class="hello"></test>')

def test_tag_should_be_able_to_be_nested():
    tag1 = Sample()
    tag2 = Sample()
    tag3 = Sample(tag1, tag2, 'This is Tag 3.')
    eq_(unicode(tag3), u'<test><test></test><test></test>This is Tag 3.</test>')

def test_tag_should_escape_harmful_attribute_values():
    tag = Sample(attr1='<script>alert("Crack the hell!")</script>')
    eq_(unicode(tag), u'<test attr1="&lt;script&gt;alert(&quot;Crack the hell!&quot;)&lt;/script&gt;"></test>')

def test_tag_can_contain_text():
    tag = h.a('inner', href="http://hello/world")
    eq_(unicode(tag), u'<a href="http://hello/world">inner</a>')

def test_tag_should_escape_text_node_by_default():
    tag = Sample('<hello />')
    eq_(unicode(tag), u'<test>&lt;hello /&gt;</test>')

def test_tag_should_extract_list_of_classes():
    tag = Sample(class_=['happy', 'good', 'safe'])
    eq_(unicode(tag), u'<test class="happy good safe"></test>')

@raises(TagSingletonError)
def test_singleton_tag_cannot_have_children():
    tag = h.img(Sample(), src="something.png")

@raises(KeyError)
def test_tag_cannot_miss_required_attributes():
    tag = h.img()

def test_tag_should_remove_trailing_underscore_on_attributes_name():
    tag = Sample(hello_='world')
    eq_(unicode(tag), u'<test hello="world"></test>')

def test_safe_tag_should_not_escape_text_node():
    class SafeTag(Sample): safe = True
    tag = SafeTag('<hello />')
    eq_(unicode(tag), u'<test><hello /></test>')

def test_html5_tag():
    tag = h.Html5()
    ok_('HTML' in unicode(tag))

def test_simple_layout_using_tags():
    layout = h.Html5(
        h.head(
            h.title('Test Page'),
            h.link(href='abc.css')
            )
        )
    ok_(unicode(layout).startswith(u'<!DOCTYPE HTML><html><head><title>Test Page</title><link '))

def test_base_layout_should_work():
    layout = BaseLayout(title='Hello World')
    ok_('DOCTYPE' in unicode(layout))


def test_tag_children_clause_comes_after_arg_list():
    template = Sample(Sample('hello'), children=[Sample('a'), Sample('b')])
    eq_(unicode(template), u'<test><test>hello</test><test>a</test><test>b</test></test>')

def test_tag_default_classes_work():
    class SampleWithDefaultClasses(Sample):
        default_classes = ['hello', 'world']

    template = SampleWithDefaultClasses(class_=['hello', 'abc'])
    eq_(unicode(template), u'<test class="hello world abc"></test>')

def test_tag_should_accept_dictionary_as_classes():
    template = Sample(class_={'hello': True, 'world': False})
    eq_(unicode(template), u'<test class="hello"></test>')

def test_tag_should_accept_string_with_multiple_classes():
    template = Sample(class_='hello world sweet')
    eq_(unicode(template), u'<test class="hello world sweet"></test>')

def test_tag_should_accept_true_as_simple_attribute():
    template = Sample(an_attribute=True)
    eq_(unicode(template), u'<test an-attribute="an-attribute"></test>')

def test_tag_with_none_attribute_value():
    template = Sample(empty_attribute=None)
    eq_(unicode(template), u'<test empty-attribute></test>')

def test_tag_with_falsy_attribute_value():
    template = Sample(falsy_attribute=False)
    eq_(unicode(template), u'<test></test>')

def test_tag_attribute_should_accept_number():
    template = Sample(d=15, f=17.58)
    eq_(unicode(template), u'<test d="15" f="17.58"></test>')

def test_tag_can_be_called_to_include_a_single_child():
    template = Sample()(Sample())
    eq_(unicode(template), u'<test><test></test></test>')

def test_tag_can_be_called_to_include_several_child():
    template = Sample()(Sample(), Sample())
    eq_(unicode(template), u'<test><test></test><test></test></test>')

def test_tag_can_be_called_to_include_list_of_childs():
    template = Sample()([Sample(), Sample()])
    eq_(unicode(template), u'<test><test></test><test></test></test>')

def test_tag_can_flatten_childs():
    template = Sample()(Sample(), [Sample(), Sample()], Sample())
    eq_(unicode(template), u'<test><test></test><test></test><test></test><test></test></test>')

def test_tag_name_automatically_inherit_from_class_name():
    class Auto(h.tag):
        pass
    eq_(unicode(Auto()), u'<auto></auto>')

def test_tag_dynamically_created():
    eq_(unicode(h.abc()), u'<abc></abc>')

def test_tag_dynamically_created_should_be_same_class():
    tag1 = h.dtag
    tag2 = h.dtag
    eq_(tag1, tag2)
