## How do I access RStudio?

To open an RStudio interface, you can select the RStudio notebook from the Jupyter Launcher (ctrl+shift+L).

![RStudio Launcher icon](RStudio-launcher.png)

## What do I need to know about the new environment?

Most of the packages are at their latest version as of August 2020.

Most notably, all supported languages except for Octave and C++ have been upgraded. Depending on the language, some syntax might have changed, so be sure to test your code to see if it works on a newer version. Here's a list of all the languages we support and the version changes:

| Language | Old version | New version |
| - | - | - |
| Python | 3.6 | 3.7.8 |
| R | 3.6.1 | 4.0.2 |
| Julia | 1.1.0 | 1.5.0 |
| Octave | 4.2.2 | 4.2.2 |
| C++ (cling) | 0.6 | 0.6 |
| SageMath | 8.1 | 9.1 |

In addition, almost all Python packages have been upgraded to a newer version. They should be backwards compatible, but you should still test your existing code to make sure they work with the newer packages.

Several packages have been removed in our new image, which are listed below. Also see [How can I permanently install additional packages?]().

- pymol and ipymol: Requires extra conda channels and is not free software. Can be installed manually in a new conda environment.
- opty: Requires Python <=3.6. Can be installed manually in a new conda environment with Python 3.6.
- rpy2: Requires R <= 4.0. Can be installed manually in a new conda environemt with R 3.6.

To ease this transition, our old image will still be listed as an option when you login to JupyterHub, and it will be supported until December 31st, 2020 (?). Please email us at [jupyterteam@ucdavis.edu](mailto:jupyterteam@ucdavis.edu) if you have concerns or issues with the new environment.

## How do I restart my JupyterLab server?

Go to File -> Hub Control Panel: TODO

## Can I install additional packages?

You are free to install any additional packages available through conda by [creating a conda environment](#how-do-i-create-a-persistent-conda-environment). These packages will persist for you. You may also use `conda install` directly without creating an environment, but these packages won't be permanent and will be wiped anytime your server restarts.

TODO: Add documentation on how octave, sagemath, julia pkg managers work. Note that `pip install --user` would persist.

You may also request packages to be installed for everyone in the default environment. This is useful if you think most LibreTexts users would benefit from a package, or if you're running a class with many students who need the package by default. In that case, please [email us](mailto:jupyterteam@ucdavis.edu).

## How do I create a persistent Conda environment?

The best way to permanently install new packages onto your account is through conda environments. Using conda environments, you may also build Jupyter notebooks and consoles which contain only the programming language and packages that you need. Follow the steps below to create one.

1. In the top left corner, open a terminal by going to File->New->Terminal or open a New Launcher (ctrl+shift+L) and select terminal from the 'other' section.

![Finding the Terminal](terminal.png)

2. Within the terminal, use the command `conda create -n 'your_env_name' 'kernel' 'packages'` to create your environment.
  Below is an example that creates an environment called `scipkg`, which contains the `ipykernel` kernel along with the python packages `numpy`, `pandas` and `matplotlib`. In general, you may include any packages which are available through conda.

  ![Conda Create command](conda-create.png)

  *Do not worry if you recieve a warning about newer versions of conda when running the `conda create` command. Just proceed through the installation by pressing `y` or by initially running `conda create` with a `-y` flag at the end.*

3. Activate your environment using `conda activate your_env_name`. You should now see `(your_env_name)` at the beginning of the terminal prompt. This indicates that the environment is active. Note that the environment will only be active within that specific terminal session. To deactivate, run `conda deactivate`.

  ![Conda Activate command](conda-activate.png)

4. If you specified a Jupyter kernel then you may run your environment as a Jupyter notebook or console. Open the launcher (Ctrl+Shift+L) and select your environment from there. Using the `scipkg` example, the environment will appear as `Python [conda env:.conda-scipkg]`. You may have to wait a little bit for the icon to appear; refresh the webpage if needed.

  ![Launch the conda environment](env-launcher.png)
  
  Once the notebook opens, you can verify that you are using the proper environment by looking in the top right corner;

  ![Notebook environment](notebook.png) 

5. Now your conda environment is created! You may access it in the terminal by `conda activate 'your_env_name'` or as a notebook from the launcher at any time. 

Note that if you want to use your environment with a Jupyter notebook, you must install a [Jupyter kernel](#what-is-a-jupyter-kernel) along with your packages. Here's a list of common languages and their kernels:

| Language | Jupyter kernel |
| - | - |
| Python | ipykernel |
| R | r-irkernel |
| C++ | xeus-cling |
| Octave | octave_kernel |

You may view all your created conda environments using `conda env list`. To remove an environment, use `conda env remove -n your_env_name`. For reference, all of your created environments are stored in `/home/jovyan/.conda/envs/`. You can learn more about [managing environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) and [more conda commands](https://docs.conda.io/projects/conda/en/latest/commands.html) from the linked documentation.

## What is a Jupyter kernel?

Jupyter kernels are language specific [managing kernels](https://jupyterlab.readthedocs.io/en/stable/user/running.html)

TODO finish

## Can I recieve accouncements for downtime and other critical information about jupyter.libretexts.org?

If you wish to recieve updates from the JupyterTeam about possible downtime for jupyter.libretexts.org, you can subscribe to our [mailing list](https://lists.ucdavis.edu/sympa/subscribe/flock-announce). Just enter your email and you will recieve emails whenever we notify Hub users about downtime and maintenance.

# For Instructors

## How do I distribute files to students?

You can distribute files using [nbgitpuller](https://jupyterhub.github.io/nbgitpuller/index.html). Please store your files in a GitHub repository and we can set up a custom environment that will update the files whenever a student spawns a server. This is a good option since students don't need to understand git, but keep in mind that nbgitpuller does have [some limitations](https://jupyterhub.github.io/nbgitpuller/topic/automatic-merging.html). Other options include hosting your files on an external site, like GitHub or Google Drive, where students can download them.

## How do I set up custom environments for my class?

If you are an instructor who wants to set up an environment with custom packages and kernels for your course, please let us know by emailing us at jupyterteam@ucdavis.edu. It would also help if you can create one of the following to let us know your exact needs:

- A repository supported by [repo2docker](https://repo2docker.readthedocs.io/) that lists your desired packages. Supported configuration files are listed [here](https://repo2docker.readthedocs.io/en/latest/config_files.html).
- A [Dockerfile](https://docs.docker.com/engine/reference/builder/) to build your custom image, if you have advanced needs. We recommend using or building on top of an existing [Jupyter Docker Stack](https://jupyter-docker-stacks.readthedocs.io/en/latest/index.html).
