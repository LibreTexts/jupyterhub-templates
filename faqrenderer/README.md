# FAQ Development

To make changes to faq.html, you should write your changes to `/faqrenderer/faq.md`. To apply these to faq.html which is actually displayed online, navigate to the `/faqrenderer/` directory and run something like `python3 render.py > ../templates/faq.html`. This will update the faq.html file with your changes. Then, you may create a testing docker container to view your changes without having to restart the hub. Using the command below, be sure to replace each instance of `/your-working-directory/` with your actual directory path. The container is viewable at `localhost:8000`. Refresh the page anytime you make changes to the html. To see CSS and image changes, be sure to `shift+f5`. 

```
docker run -it -v /your-working-directory/jupyterhub-templates/static:/usr/local/share/jupyterhub/static/external -v /your-working-directory/jupyterhub-templates/templates:/etc/jupyterhub/templates -v /your-working-directory/jupyterhub-templates/faqrenderer/testrun.py:/srv/jupyterhub/jupyterhub_config.py -p 8000:8000 jupyterhub/jupyterhub jupyterhub --JupyterHub.template_paths=\"['/etc/jupyterhub/templates']\" --debug
```

It is important to use the `render.py` script because it also reads each markdown title (distinguished by `#` characters) and creates a list at the top of the page which contains hyperlinks to each titled section of the FAQ. If the HTML file is edited with changes that are not reflected in `faq.md`, the next person who applies `render.py` to `faq.html` will override the changes made to the HTML. Just be sure to write your changes here in `faq.md`.
