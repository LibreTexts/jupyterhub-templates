#!/usr/bin/python
import mistune
import sys

START = '''{% extends "page.html" %}

{% block main %}
<h1>Frequently Asked Questions</h1>
<section id="faq" class="container">
'''
END = '''</section>
{% endblock main %}

{% block stylesheet %}
{{ super() }}
<link rel="stylesheet" href="{{ static_url("external/css/faq.css") }}" type="text/css"/>
{% endblock stylesheet %}
'''
alphanumaspace="abcdefghijklmnopqrstuvwxyz0123456789 "

class JupyterHubTemplateRenderer(mistune.Renderer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.toc = "<h1>On this page:</h1>\n"

    def header(self, text, level, raw=None):
        # render and add in an anchor
        anchor = "".join([c if c != ' ' else '-' for c in text.lower() if c in alphanumaspace])
        if level == 1:
            self.toc += '<h2>%s</h2>\n'%text
        elif level == 2:
            self.toc += '<li><a href="#%s">%s</a></li>\n'%(anchor, text)
        return '<h%d id="%s">%s</h%d>\n'%(level, anchor, text, level)

    def image(self, src, title, text):
        # if not an external image, use the static_url template function
        # doing it the lazy way and just checking if / is in the name
        # if not, it probably is image.png or sth similar
        # not doing proper escaping of quotes, but good enough
        if '/' not in src:
            src = '{{ static_url("external/images/faq/%s") }}' % src
        else:
            src = mistune.escape_link(src)
        # the rest is the same as the original function
        text = mistune.escape(text, quote=True)
        if title:
            title = mistune.escape(title, quote=True)
            html = '<img src="%s" alt="%s" title="%s"' % (src, text, title)
        else:
            html = '<img src="%s" alt="%s"' % (src, text)
        if self.options.get('use_xhtml'):
            return '%s />' % html
        return '%s>' % html

    def table_of_contents(self):
        return "<ul>\n%s\n</ul>\n"%self.toc

if __name__ == "__main__":
    if len(sys.argv) != 2:
        fn = "faq.md"
    else:
        fn = sys.argv[1]
    with open(fn) as f:
        md = f.read()
    renderer = JupyterHubTemplateRenderer()
    html = mistune.Markdown(renderer).parse(md)
    toc = renderer.table_of_contents()
    print(START + toc + html + END)
