# JupyterHub Templates

This repository contains templates and files specific to our LibreTexts JupyterHub, whih customizes our login page and adds About and FAQ pages.

# Directory structure

The `templates` folder contains Jinja templates to be rendered by JupyterHub. This should be mounted in `/etc/jupyterhub/templates`.

The `static` folder contains CSS files and images used by the pages. This should be mounted in `/usr/local/share/jupyterhub/static/external`. Note that `/usr/local/share/jupyterhub/static` is already occupied and shouldn't be overwritten, and our mounted folder corresponds to `/hub/static/external/` in the URL, not `/hub/static`.

The `faqrenderer` folder contains the FAQ markdown file and a Python script that generates `templates/faq.html`, so we don't have to write HTML by hand for the FAQ.

# Usage

A couple of things need to be setup for this to work:

1. Custom handlers for `/hub/about` and `/hub/faq`. Add this to JupyterHub's config:
```python
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
```

If you're using Z2JH, you can add this to the helm values like this:
```yaml
hub:
  extraConfig:
    customtemplates: |
      from jupyterhub.handlers.base import BaseHandler
      ... (rest of the config file)
```

2. Mount the right folders in the right places. We're using the `alpine/git` image as an initContainer to clone the repo and move the right folders to the right places, like this in Z2JH config.yaml:
```yaml
hub:
  initContainers:
    - name: git-clone-templates
      image: alpine/git
      command: /bin/sh 
      args:
        - -c
        - |
          git clone --branch=master https://github.com/LibreTexts/jupyterhub-templates.git &&
          cp -r jupyterhub-templates/templates /templates &&
          cp -r jupyterhub-templates/static /static
      volumeMounts:
        - name: custom-templates
          mountPath: /templates
        - name: custom-templates-static
          mountPath: /static
  extraVolumes:
    - name: custom-templates
      emptyDir: {}
    - name: custom-templates-static
      emptyDir: {}
  extraVolumeMounts:
    - name: custom-templates
      mountPath: /etc/jupyterhub/templates
    - name: custom-templates-static
      mountPath: /usr/local/share/jupyterhub/static/external
```
