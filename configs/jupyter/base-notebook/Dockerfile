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

# Update to the latest package version list
RUN apt-get update --yes && \
# Install required OS packages and force yes to any installation prompts
    apt-get install --yes --no-install-recommends \
# List of 
    vim \
    curl \
    emacs && \
# Clear /var/cache/apt directories that contain leftover pacakge files 
    apt-get clean && \
# Remove lists of available packages to save space
    rm -rf /var/lib/apt/lists/*

# Switch to local user for installing user level packages
USER $NB_UID

COPY configs/jupyter/base-notebook/environment.yml /home/$NB_USER/

RUN conda install --quiet --yes \
    'conda-forge::nb_conda_kernels' && \
    conda env update --name cisl-cloud-base -f environment.yml && \
    pip install --no-cache-dir nbgitpuller && \
    conda clean --all -f -y && \
    jupyter lab clean -y && \
    npm cache clean --force && \
    rm -rf /home/$NB_USER/.cache/yarn && \
    rm -rf /home/$NB_USER/.node-gyp && \
    mv environment.yml / && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

COPY configs/jupyter/base-notebook/.condarc /

USER $NB_UID