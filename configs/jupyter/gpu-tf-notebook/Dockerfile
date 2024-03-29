# Currently copied directly from https://github.com/zonca/jupyterhub-deploy-kubernetes-jetstream/blob/master/gpu/nvidia-tensorflow-jupyterhub/Dockerfile
# We will start with this and go through testing to determine where this needs to be customized

ARG ROOT_CONTAINER=ubuntu:22.04

FROM $ROOT_CONTAINER

LABEL maintainer="CISL Cloud Pilot Team <cisl-cloud-pilot@ucar.edu>"
ARG NB_USER="jovyan"
ARG NB_UID="1000"
ARG NB_GID="100"

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
# Fix: https://github.com/koalaman/shellcheck/wiki/SC3014
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

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
    # Required for NVIDIA OpenGL Possibly
    libglu1-mesa-dev \
    libglvnd-dev \
    mesa-common-dev \
    # End of OpenGL
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
    LANGUAGE=en_US.UTF-8 \
    PIP_EXTRA_INDEX_URL='https://pypi.nvidia.com'

ENV PATH="${CONDA_DIR}/bin:${PATH}" \
    HOME="/home/${NB_USER}"

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
    conda clean --all -f -y

ENV CONDA_ENV=cisl-gpu-base \
    NB_PYTHON_PREFIX=${HOME}/.jupyter \
    PATH=${NB_PYTHON_PREFIX}/bin:${PATH}

COPY requirements.txt cisl-gpu-base.yaml /tmp/

RUN mamba install --quiet --yes \
    'notebook' \
    'jupyterhub' \
    'conda-forge::nb_conda_kernels' && \
    CONDA_OVERRIDE_CUDA="12.3" mamba env create -f /tmp/cisl-gpu-base.yaml && \
    pip install -r /tmp/requirements.txt && \
    # Install Nvidia extension for Jupyterlab>=4
    pip install --extra-index-url https://pypi.anaconda.org/rapidsai-wheels-nightly/simple --pre jupyterlab_nvdashboard && \
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

# Set the conda prefix and update the path to include shared libraries for nvidia and cuda
ENV CONDA_PREFIX=/opt/base-conda/${CONDA_ENV} \
    LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:$CONDA_PREFIX/lib/:/opt/conda/lib/:/usr/lib/

# Run conda activate each time a bash shell starts, so users don't have to manually type conda activate
# Note this is only read by shell, but not by the jupyter notebook - that relies
# on us starting the correct `python` process, which we do by adding the notebook conda environment's
# bin to PATH earlier ($NB_PYTHON_PREFIX/bin)
RUN echo ". ${CONDA_DIR}/etc/profile.d/conda.sh ; conda activate ${CONDA_ENV}" > /etc/profile.d/init_conda.sh && \
    mkdir -p $CONDA_PREFIX/etc/conda/activate.d && \
    echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/' > $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh

# GPU TensorFlow config based on https://github.com/tensorflow/tensorflow/issues/58681
RUN printf 'export XLA_FLAGS=--xla_gpu_cuda_data_dir=$CONDA_PREFIX/lib/\n' >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh && \
    mkdir -p $CONDA_PREFIX/lib/nvvm/libdevice && \
    cp $CONDA_PREFIX/lib/libdevice.10.bc $CONDA_PREFIX/lib/nvvm/libdevice/

# Ask dask to read config from ${CONDA_DIR}/etc rather than
# the default of /etc, since the non-root jovyan user can write
# to ${CONDA_DIR}/etc but not to /etc
ENV DASK_ROOT_CONFIG=${CONDA_DIR}/etc

COPY config/.condarc /opt/conda

# Expose the application on the port JupyterHub listens on
ENV JUPYTER_PORT=8888
EXPOSE $JUPYTER_PORT

# Configure container startup. Dask gateway requires ENTRYPOINT
ENTRYPOINT ["/srv/start"]

COPY scripts/jupyter_server_config.py scripts/docker_healthcheck.py /etc/jupyter/
COPY start /srv/start
COPY config/.profile /.bash_profile
COPY config/.bashrc /etc/bash.bashrc

RUN rm -rf /tmp/requirements.txt /tmp/cisl-gpu-base.yaml

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

RUN chmod 755 /opt/base-conda/cisl-gpu-base/*

USER ${NB_UID}

WORKDIR "${HOME}"