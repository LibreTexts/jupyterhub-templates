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
    def header(self, text, level, raw=None):
        # render and add in an anchor
        anchor = "".join([c if c != ' ' else '-' for c in text.lower() if c in alphanumaspace])
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


if __name__ == "__main__":
    if len(sys.argv) != 2:
        fn = "faq.md"
    else:
        fn = sys.argv[1]
    with open(fn) as f:
        md = f.read()
    html = mistune.Markdown(JupyterHubTemplateRenderer()).parse(md)
    print(START + html + END)
