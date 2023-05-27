# NCAR CISL Customized version of the Jupyter scipy-notebook Docker image
# https://github.com/jupyter/docker-stacks/blob/main/scipy-notebook/
# This is built on a collection of Docker images from jupyter but the base image is ubuntu:22.04
# https://github.com/jupyter/docker-stacks/blob/main/docker-stacks-foundation/Dockerfile

ARG BASE_CONTAINER=jupyter/scipy-notebook:latest
FROM $BASE_CONTAINER

# Replace with team name and email
LABEL maintainer="Nick Cote <ncote@ucar.edu>"

# Set to root user for apt-get commands to follow
USER root

# Used to allow folder deletions
# RUN sed -i 's/c.FileContentsManager.delete_to_trash = False/c.FileContentsManager.always_delete_dir = True/g' /etc/jupyter/jupyter_server_config.py

# Update to the latest package version list
RUN apt-get update --yes && \
# Install required OS packages and force yes to any installation prompts
    apt-get install --yes --no-install-recommends \
# List of OS packages to be installed
    vim \
    curl \
    emacs && \
# Clear /var/cache/apt directories that contain leftover pacakge files 
    apt-get clean && \
# Remove lists of available packages to save space
    rm -rf /var/lib/apt/lists/* 

# Copy environment.yml file with list of python packages to be installed to the user home directory
COPY configs/jupyter/base-notebook/environment.yml /home/$NB_USER/

# Switch to local user for installing user level packages
USER $NB_UID

# Run a list of commands in user space to install packages and clean up environment
# mamba is used instead of conda to speed up the installation
RUN mamba uninstall jupyterlab --yes && \
    mamba install --quiet --yes \
# nb_conda_kernels is required to save user environments as custom user notebook kernels that persist
    'conda-forge::nb_conda_kernels' && \
# Create a kernel named cisl-cloud-base from the environment.yml file
    mamba env update --name cisl-cloud-base -f environment.yml && \
# Install nbgitpuller via pip 
    pip install --no-cache-dir nbgitpuller && \
    pip install --no-cache-dir jupyter-server-proxy && \
    pip install --no-cache-dir dask-labextension && \
# Use mamba to remove unused packages and caches including writable packages and do no ask to confirm
    mamba clean --all -f -y && \
# Use jupyter lab to remove unused packages and caches and do no ask to confirm
    jupyter lab clean -y && \
# Use npm to remove data in cache and do no ask to confirm
    npm cache clean --force && \
# Remove unneeded cache files
    rm -rf /home/$NB_USER/.cache/yarn && \
    rm -rf /home/$NB_USER/.node-gyp && \
# Remove the environment.yml file to allow permissions to be correct
    rm environment.yml && \
# Run jupyter fix-permissions script to make sure all files are writable
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

# Copy the .condarc file to allow for saving of user custom conda environments
COPY configs/jupyter/base-notebook/.condarc /
COPY configs/jupyter/base-notebook/.bash_profile /
COPY configs/jupyter/base-notebook/distributed.yml /

# Make sure the notebook user is set to be the default
USER $NB_UID