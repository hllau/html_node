HtmlNode - Python HTML Generator
=====================================

**HtmlNode** is an internal Domain Specific Language (DSL) using Python to generate HTML templates. 
It is designed to be really easy and flexible to use. By using DSL instead of a specific
templating language, you can write Python code to render HTML directly, so you can debug
your presentation logics easily. Also, you get the full power of Python in writing 
presentation logic, without the hassle to learn another templating language.

An overview for using interal DSL vs external template languages can be found 
`here <http://bitbucket.org/tavisrudd/throw-out-your-templates/src/tip/throw_out_your_templates.py>`_.


Features
--------

* Very simple syntax and natural way to generate HTML
* Unicode support
* Auto-escape dangerous characters
* Template inheritance support
* Context variables insertion into templates
* Auto-completion support for IDEs which can introspect
* Custom HTML elements can be created on the fly
* Flexible ways to include attributes for HTML element


Usage Example
-------------

**Example 1 - Simple HTML:**

Code snippet::

    from html_node import html_node as h
    
    template = h.div(class_='container')(
                    h.span('Hello World!', style='color: pink; font-weight: bold;')
               )
    print template


Output::

    <div class="container">
        <span style="color: pink; font-weight: bold;">
            Hello World!
        </span>
    </div>

*By default, the actual output is concatenated without space or line feeds.*


**Example 2 - Simple reusable layout**

You can use `placeholder` to mark different block section to replace with. You give the
placeholder a name, and provide a method with the same name that returns a unicode string.
You can inherit the layout just like how you normally do in Python.

Code snippet::

    from html_node import html_node as h, BaseTemplate, placeholder
    

    class MyLayout(BaseTemplate):
        """My customized layout which other templates can inherit from."""

        title = 'HtmlNode'
        
        def template(self):
            return h.html5(placeholder('head'), placeholder('body'))
        
        @placeholder
        def head(self):
            return h.head(
                       h.title(self.title),
                       h.link(rel="stylesheet", type="text/css", href="default.css"),
                   )
        
        @placeholder
        def body(self):
            return h.body(
                       h.div(class_=['container', 'expand'])(
                           placeholder('content')
                       )
                   )

        @placeholder
        def content(self):
            raise NotImplementedError


    class MyViewTemplate(MyLayout):
        """This template will provide the content block for the layout."""

        @placeholder
        def content(self):
            return u'HTML Node is a flexible and easy-to-use HTML generator!'


    template = MyViewTemplate()
    print template


Output::

    <!DOCTYPE HTML>
    <html>
        <head>
            <title>HtmlNode</title>
            <link href="default.css" type="text/css" rel="stylesheet" />
        </head>
        <body>
            <div class="container expand">
                HtmlNode is a flexible and easy-to-use HTML generator!
            </div>
        </body>
    </html>

