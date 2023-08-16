# Borrowed heavily from the base-notebook Dockerfile by Jupyter
# https://github.com/jupyter/docker-stacks/blob/main/base-notebook/Dockerfile
# The shell scripts and python modules were developed by the Jupyter Development Team
# This image provides a custom environment.yml and requirements.txt as well as
# having some customizations injected into this Dockerfile 
# The base image used is the docker-stacks-foundation by Jupyter
# https://github.com/jupyter/docker-stacks/blob/main/docker-stacks-foundation/Dockerfile

FROM jupyter/docker-stacks-foundation:latest

# Update version here and on the .github/workflow/build-push-basenb.yaml before pushing changes to the repo
LABEL maintainer="CISL Cloud Pilot Team <cisl-cloud-pilot@ucar.edu>" version="v1-stable"

ENV CONDA_ENV=cisl-cloud-base

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
# Fix: https://github.com/koalaman/shellcheck/wiki/SC3014
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

# Install all OS dependencies for notebook server that starts but lacks all
# features (e.g., download as all possible file formats)
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    curl \
    cmake \
    csh \
    emacs \
    fonts-dejavu \
    fonts-liberation \
    g++ \
    gcc \
    gfortran \
    git \
    # R pre-requisites
    libperl-dev \
    libsnappy-dev \
    libstdc++-12-dev \
    make \
    nodejs \
    npm \
    pandoc \
    vim \
    # - pandoc is used to convert notebooks to html files
    #   it's not present in aarch64 ubuntu image, so we install it here
    # - run-one - a wrapper script that runs no more
    #   than one unique  instance  of  some  command with a unique set of arguments,
    #   we use `run-one-constantly` to support `RESTARTABLE` option
    run-one && \
    apt-get clean && rm -rf /var/lib/apt/lists/* 

USER ${NB_UID}

# Install Jupyter Notebook, Lab, and Hub
# Generate a notebook server config
# Cleanup temporary files
# Correct permissions
# Do all this in a single RUN command to avoid duplicating all of the
# files across image layers when the permissions change

###
# GitHub Build
###
COPY configs/jupyter/base-notebook/environment.yml configs/jupyter/base-notebook/requirements.txt /tmp/

###
# Local Build
###
#COPY environment.yml requirements.txt /tmp/

WORKDIR /tmp

RUN mamba install --quiet --yes \
    # NodeJS >= 18.0 is required for `jupyter lab build` command
    # https://github.com/jupyter/docker-stacks/issues/1901
    'nodejs>=18.0' \
    'notebook' \
    'jupyterhub' \
    'jupyterlab==3.6.3' \
    'conda-forge::nb_conda_kernels' && \
    # Pin NodeJS
    echo 'nodejs >=18.0' >> "${CONDA_DIR}/conda-meta/pinned" && \
    # nb_conda_kernels is required to save user environments as custom user notebook kernels that persist
    # Create a kernel named cisl-cloud-base from the environment.yml file
    mamba env update --name "${CONDA_ENV}" -f environment.yml && \
    pip install -r requirements.txt && \
    jupyter notebook --generate-config && \
    mamba clean --all -f -y && \
    npm cache clean --force && \
    jupyter lab clean && \
    rm -rf "/home/${NB_USER}/.cache/yarn" && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Ask dask to read config from ${CONDA_DIR}/etc rather than
# the default of /etc, since the non-root jovyan user can write
# to ${CONDA_DIR}/etc but not to /etc
ENV DASK_ROOT_CONFIG=${CONDA_DIR}/etc

ENV JUPYTER_PORT=8888
EXPOSE $JUPYTER_PORT

###
# GitHub Actions Build
###
# Copy local files as late as possible to avoid cache busting
COPY configs/jupyter/base-notebook/scripts/start-notebook.sh configs/jupyter/base-notebook/scripts/start-singleuser.sh /usr/local/bin/
# Currently need to have both jupyter_notebook_config and jupyter_server_config to support classic and lab
COPY configs/jupyter/base-notebook/scripts/jupyter_server_config.py configs/jupyter/base-notebook/scripts/docker_healthcheck.py /etc/jupyter/

###
# Local Build
###
#COPY scripts/start-notebook.sh scripts/start-singleuser.sh /usr/local/bin/
#COPY scripts/jupyter_server_config.py scripts/docker_healthcheck.py /etc/jupyter/

# Fix permissions on /etc/jupyter as root
USER root

RUN rm -rf /tmp/environment.yml && \
    rm -rf /tmp/requirements.txt 
    
# Legacy for Jupyter Notebook Server, see: [#1205](https://github.com/jupyter/docker-stacks/issues/1205)
RUN sed -re "s/c.ServerApp/c.NotebookApp/g" \
    /etc/jupyter/jupyter_server_config.py > /etc/jupyter/jupyter_notebook_config.py && \
    fix-permissions /etc/jupyter/

# Used to allow folder deletions
RUN sed -i 's/c.FileContentsManager.delete_to_trash = False/c.FileContentsManager.always_delete_dir = True/g' /etc/jupyter/jupyter_server_config.py

# HEALTHCHECK documentation: https://docs.docker.com/engine/reference/builder/#healthcheck
# This healtcheck works well for `lab`, `notebook`, `nbclassic`, `server` and `retro` jupyter commands
# https://github.com/jupyter/docker-stacks/issues/915#issuecomment-1068528799
HEALTHCHECK --interval=5s --timeout=3s --start-period=5s --retries=3 \
    CMD /etc/jupyter/docker_healthcheck.py || exit 1

###
# GitHub Build
###
# Copy the .condarc file to allow for saving of user custom conda environments
COPY configs/jupyter/base-notebook/config/.condarc /opt/conda/
COPY configs/jupyter/base-notebook/config/.profile /.bash_profile
COPY configs/jupyter/base-notebook/config/.bashrc /etc/bash.bashrc

###
# Local Build
###
#COPY config/.condarc /opt/conda/
#COPY config/.profile /.bash_profile
#COPY config/.bashrc /etc/bash.bashrc

# Switch back to jovyan to avoid accidental container runs as root
USER ${NB_UID}

WORKDIR "${HOME}"

# Configure container startup
ENTRYPOINT ["start-notebook.sh"]