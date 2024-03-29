# Borrowed heavily from the base-notebook Dockerfile by Jupyter
# https://github.com/jupyter/docker-stacks/blob/main/base-notebook/Dockerfile
# The shell scripts and python modules were developed by the Jupyter Development Team
# This image provides a custom cisl-cloud-base.yml and requirements.txt as well as
# having some customizations injected into this Dockerfile 
# The base image used is the docker-stacks-foundation by Jupyter
# https://github.com/jupyter/docker-stacks/blob/main/images/docker-stacks-foundation/Dockerfile

ARG ROOT_CONTAINER=ubuntu:22.04

FROM $ROOT_CONTAINER

LABEL maintainer="CISL Cloud Pilot Team <cisl-cloud-pilot@ucar.edu>"
ARG NB_USER="jovyan"
ARG NB_UID="1000"
ARG NB_GID="100"

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
# Fix: https://github.com/koalaman/shellcheck/wiki/SC3014
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

# Install all OS dependencies for Server that starts
# but lacks all features (e.g., download as all possible file formats)
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update --yes && \
    # - apt-get upgrade is run to patch known vulnerabilities in apt-get packages as
    #   the ubuntu base image is rebuilt too seldom sometimes (less than once a month)
    apt-get upgrade --yes && \
    apt-get install --yes --no-install-recommends \
    # - bzip2 is necessary to extract the micromamba executable.
    bzip2 \
    ca-certificates \
    curl \
    # Build C++
    cmake \
    # C shell
    csh \
    # text editor for POSIX
    emacs \
    fonts-dejavu \
    fonts-liberation \
    # GNU C++ compiler
    g++ \
    # Set of GNU compilers
    gcc \
    # GNU Fortan
    gfortran \
    git \
    graphviz \
    # R pre-requisites
    # Perl library development files
    libperl-dev \
    # compression/decompression library
    libsnappy-dev \
    # GNU Standard C++ Library development files
    libstdc++-12-dev \
    locales \
    # Build executable programs
    make \
    # SSH for Git 
    openssh-client \
    # - pandoc is used to convert notebooks to html files
    pandoc \
    # - run-one - a wrapper script that runs no more
    run-one \
    sudo \
    # - tini is installed as a helpful container entrypoint that reaps zombie
    #   processes and such of the actual executable we want to start, see
    #   https://github.com/krallin/tini#why-tini for details.
    tini \
    vim \
    # Remote Desktop packages
    dbus-x11 \
    firefox \
    xfce4 \
    xfce4-panel \
    xfce4-session \
    xfce4-settings \
    xorg \
    xubuntu-icon-theme \
    tigervnc-standalone-server \
    tigervnc-xorg-extension \
    websockify \
    # End of packages required for RDP
    wget && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

# Configure environment
ENV CONDA_DIR=/opt/conda \
    SHELL=/bin/bash \
    NB_USER="${NB_USER}" \
    NB_UID=${NB_UID} \
    NB_GID=${NB_GID} \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8
ENV PATH="${CONDA_DIR}/bin:${PATH}" \
    HOME="/home/${NB_USER}"

###
# Copy a script that we will use to correct permissions after running certain commands
###
COPY fix-permissions /usr/local/bin/fix-permissions

RUN chmod a+rx /usr/local/bin/fix-permissions

# Enable prompt color in the skeleton .bashrc before creating the default NB_USER
# hadolint ignore=SC2016
RUN sed -i 's/^#force_color_prompt=yes/force_color_prompt=yes/' /etc/skel/.bashrc && \
   # Add call to conda init script see https://stackoverflow.com/a/58081608/4413446
   echo 'eval "$(command conda shell.bash hook 2> /dev/null)"' >> /etc/skel/.bashrc

# Create NB_USER with name jovyan user with UID=1000 and in the 'users' group
# and make sure these dirs are writable by the `users` group.
RUN echo "auth requisite pam_deny.so" >> /etc/pam.d/su && \
    sed -i.bak -e 's/^%admin/#%admin/' /etc/sudoers && \
    sed -i.bak -e 's/^%sudo/#%sudo/' /etc/sudoers && \
    useradd --no-log-init --create-home --shell /bin/bash --uid "${NB_UID}" --no-user-group "${NB_USER}" && \
    mkdir -p "${CONDA_DIR}" && \
    chown "${NB_USER}:${NB_GID}" "${CONDA_DIR}" && \
    chmod g+w /etc/passwd && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Pin python version here, or set it to "default"
ARG PYTHON_VERSION=3.10.12

# Setup work directory for backward-compatibility
RUN mkdir "/home/${NB_USER}/work" && \
    fix-permissions "/home/${NB_USER}"

# Download and install Micromamba, and initialize Conda prefix.
#   <https://github.com/mamba-org/mamba#micromamba>
#   Similar projects using Micromamba:
#     - Micromamba-Docker: <https://github.com/mamba-org/micromamba-docker>
#     - repo2docker: <https://github.com/jupyterhub/repo2docker>
# Install Python, Mamba and jupyter_core
# Cleanup temporary files and remove Micromamba
# Correct permissions
# Do all this in a single RUN command to avoid duplicating all of the
# files across image layers when the permissions change

###
# Copy the first condarc file to install preconfigured envs to /opt/conda
###
COPY --chown="${NB_UID}:${NB_GID}" initial-condarc "${CONDA_DIR}/.condarc"

WORKDIR /tmp

RUN set -x && \
    arch=$(uname -m) && \
    if [ "${arch}" = "x86_64" ]; then \
        # Should be simpler, see <https://github.com/mamba-org/mamba/issues/1437>
        arch="64"; \
    fi && \
    wget --progress=dot:giga -O /tmp/micromamba.tar.bz2 \
        "https://micromamba.snakepit.net/api/micromamba/linux-${arch}/latest" && \
    tar -xvjf /tmp/micromamba.tar.bz2 --strip-components=1 bin/micromamba && \
    rm /tmp/micromamba.tar.bz2 && \
    PYTHON_SPECIFIER="python=${PYTHON_VERSION}" && \
    if [[ "${PYTHON_VERSION}" == "default" ]]; then PYTHON_SPECIFIER="python"; fi && \
    # Install the packages
    ./micromamba install \
        --root-prefix="${CONDA_DIR}" \
        --prefix="${CONDA_DIR}" \
        --yes \
        "${PYTHON_SPECIFIER}" \
        'mamba' \
        'jupyter_core' && \
    rm micromamba && \
    # Pin major.minor version of python
    mamba list python | grep '^python ' | tr -s ' ' | cut -d ' ' -f 1,2 >> "${CONDA_DIR}/conda-meta/pinned" && \
    # Changed to conda clean due to : https://github.com/mamba-org/mamba/issues/3044
    conda clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

ENV CONDA_ENV=cisl-cloud-base \
    NB_PYTHON_PREFIX=${HOME}/.jupyter \
    PATH=${NB_PYTHON_PREFIX}/bin:${PATH}

WORKDIR /tmp

###
# Python Package Installation
###
# Copy package list for base OS and Kernels
###
COPY requirements.txt conda-envs/cisl-cloud-base.yml /tmp/

# Install required Python packages
RUN mamba install --quiet --yes \
    # NodeJS >= 18.0 is required for `jupyter lab build` command
    # https://github.com/jupyter/docker-stacks/issues/1901
    'notebook' \
    'jupyterhub' \
    'r-irkernel' \
    'conda-forge::nb_conda_kernels' && \
    # Pin NodeJS
    # nb_conda_kernels is required to save user environments as custom user notebook kernels that persist
    # Create a kernel named cisl-cloud-base from the cisl-cloud-base.yml file
    mamba env create -f cisl-cloud-base.yml && \
    # Install extensions in to OS Python env
    pip install -r requirements.txt && \
    # Build Jupyter Config
    jupyter notebook --generate-config && \
    # Cleanup files no longer needed to reduce image size
    # Changed to conda clean due to : https://github.com/mamba-org/mamba/issues/3044
    conda clean --all -f -y && \
    npm cache clean --force && \
    jupyter lab clean && \
    rm -rf "/home/${NB_USER}/.cache/yarn" && \
    # Fix permissions
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Run conda activate each time a bash shell starts, so users don't have to manually type conda activate
# Note this is only read by shell, but not by the jupyter notebook - that relies
# on us starting the correct `python` process, which we do by adding the notebook conda environment's
# bin to PATH earlier ($NB_PYTHON_PREFIX/bin)
RUN echo ". ${CONDA_DIR}/etc/profile.d/conda.sh ; conda activate ${CONDA_ENV}" > /etc/profile.d/init_conda.sh

# Ask dask to read config from ${CONDA_DIR}/etc rather than
# the default of /etc, since the non-root jovyan user can write
# to ${CONDA_DIR}/etc but not to /etc
ENV DASK_ROOT_CONFIG=/opt/base-conda/cisl-cloud-base/etc

###
# Change the .condarc file now so user envs are created in ~/my-conda-envs
###
COPY config/.condarc /opt/conda/

# Expose the application on the port JupyterHub listens on
ENV JUPYTER_PORT=8888
EXPOSE $JUPYTER_PORT

# Configure container startup. Dask gateway requires ENTRYPOINT
ENTRYPOINT ["/srv/start"]

###
# Copy startup/healthcheck scripts & custom user profile
###
# Copy local files as late as possible to avoid cache busting
# Currently need to have both jupyter_notebook_config and jupyter_server_config to support classic and lab
###
COPY scripts/start /srv/start
COPY scripts/jupyter_server_config.py scripts/docker_healthcheck.py /etc/jupyter/

###
# Copy the bash profile to autoload conda envs
###
COPY config/.profile /.bash_profile
COPY config/.bashrc /etc/bash.bashrc

# Cleanup files that were already installed
RUN rm -rf /tmp/cisl-cloud-base.yml && \
    rm -rf /tmp/requirements.txt 
    
# Legacy for Jupyter Notebook Server, see: [#1205](https://github.com/jupyter/docker-stacks/issues/1205)
RUN sed -re "s/c.ServerApp/c.NotebookApp/g" \
    /etc/jupyter/jupyter_server_config.py > /etc/jupyter/jupyter_notebook_config.py && \
    fix-permissions /etc/jupyter/ && \
# Used to allow user deletions of folders and contents
    sed -i 's/c.FileContentsManager.delete_to_trash = False/c.FileContentsManager.always_delete_dir = True/g' \
    /etc/jupyter/jupyter_server_config.py

# HEALTHCHECK documentation: https://docs.docker.com/engine/reference/builder/#healthcheck
# This healtcheck works well for `lab`, `notebook`, `nbclassic`, `server` and `retro` jupyter commands
# https://github.com/jupyter/docker-stacks/issues/915#issuecomment-1068528799
HEALTHCHECK --interval=5s --timeout=3s --start-period=5s --retries=3 \
    CMD /etc/jupyter/docker_healthcheck.py || exit 1

# Make the conda environments we install read only and executable for the user
# They can run the environments but will get permission denied when trying to make changes
# New environments are installed to /home/jovyan/.jupyter with write permissions for the users
RUN chmod 755 /opt/base-conda/cisl-cloud-base/* && \
    chown root:root /opt/*   

# Switch back to jovyan to avoid accidental container runs as root
USER ${NB_UID}

WORKDIR "${HOME}"
