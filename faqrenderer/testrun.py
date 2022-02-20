import jupyterhub.auth
c.JupyterHub.authenticator_class=jupyterhub.auth.DummyAuthenticator

from jupyterhub.handlers.base import BaseHandler
class AboutHandler(BaseHandler):
    def get(self):
        self.write(self.render_template("about.html"))
class FAQHandler(BaseHandler):
    def get(self):
        self.write(self.render_template("faq.html"))
c.JupyterHub.extra_handlers.extend([
    (r"about", AboutHandler),
    (r"faq", FAQHandler),
])

