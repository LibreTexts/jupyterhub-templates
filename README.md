# JupyterHub Templates

This repository contains templates and files specific to our LibreTexts JupyterHub, whih customizes our login page and adds About and FAQ pages.

## Directory structure

The `templates` folder contains Jinja templates to be rendered by JupyterHub. This should be mounted in `/etc/jupyterhub/templates`.

The `static` folder contains CSS files and images used by the pages. This should be mounted in `/usr/local/share/jupyterhub/static/external`. Note that `/usr/local/share/jupyterhub/static` is already occupied and shouldn't be overwritten, and our mounted folder corresponds to `/hub/static/external/` in the URL, not `/hub/static`.

The `faqrenderer` folder contains the FAQ markdown file and a Python script that generates `templates/faq.html`, so we don't have to write HTML by hand for the FAQ.

## Making Changes

Assuming all the JupyterHub configuration is set up on the cluster, making changes is as simple as:
1. Make your changes and get them on the master branch. This can be done by either committing straight to the branch or by making a new branch and merging.
1. While on a management node, restart the jhub hub pod. The easiest way to do this would be to delete the pod and let k8s respawn it on its own.

To test things first through staging JupyterHub, the above steps could be repeated with slight alterations. Instead of pushing to master branch, push to the staging branch. Likewise, instead of restarting the jhub hub pod, restart the staging-jhub hub pod.

## Usage

Two things need to be setup for this to work:

1. Custom handlers for `/hub/about` and `/hub/faq`, along with setting `template_paths` to point JupyterHub to our custom templates. Add this to JupyterHub's config:
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
c.JupyterHub.template_paths = ['/etc/jupyterhub/templates']
```

If you're using Z2JH, you can add this to the helm values like this:
```yaml
hub:
  extraConfig:
    templates: |
      from jupyterhub.handlers.base import BaseHandler
      ... (rest of the config file)
```

2. Mount the right folders in the right places. We're using the `alpine/git` image as an initContainer to clone the repo and move the right folders to the right places, like this in Z2JH config.yaml:
```yaml
hub:
  initContainers:
    - name: git-clone-templates
      image: alpine/git
      command:
        - /bin/sh
        - -c
      args:
        - >-
            git clone --branch=master https://github.com/LibreTexts/jupyterhub-templates.git &&
            cp -r jupyterhub-templates/templates/* /templates &&
            cp -r jupyterhub-templates/static/* /static
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

## FAQ Development

To make changes to faq.html, you may write your changes to `/faqrenderer/faq.md`. To apply these to faq.html which is actually displayed online, navigate to the `/faqrenderer/` directory and run something like `python3 render.py > ../templates/faq.html`. This will update the faq.html file with your changes. Then, you may create a testing docker container to view your changes without having to restart the hub. Using the command below, be sure to replace each instance of `/your-working-directory/` with your actual directory path. The container is viewable at `localhost:8000`. Refresh the page anytime you make changes to the html. To see CSS and image changes, be sure to `shift+f5`. 

```
docker run -it -v /your-working-directory/jupyterhub-templates/static:/usr/local/share/jupyterhub/static/external -v /your-working-directory/jupyterhub-templates/templates:/etc/jupyterhub/templates -v /your-working-directory/jupyterhub-templates/faqrenderer/testrun.py:/srv/jupyterhub/jupyterhub_config.py -p 8000:8000 jupyterhub/jupyterhub jupyterhub --JupyterHub.template_paths=\"['/etc/jupyterhub/templates']\" --debug
```
