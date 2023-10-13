# Borrowed heavily from the base-notebook Dockerfile by Jupyter
# https://github.com/jupyter/docker-stacks/blob/main/base-notebook/Dockerfile
# The shell scripts and python modules were developed by the Jupyter Development Team
# This image provides a custom environment.yml and requirements.txt as well as
# having some customizations injected into this Dockerfile 
# The base image used is the docker-stacks-foundation by Jupyter
# https://github.com/jupyter/docker-stacks/blob/main/docker-stacks-foundation/Dockerfile

FROM jupyter/docker-stacks-foundation:latest

# Update version here and on the .github/workflow/build-push-basenb.yaml before pushing changes to the repo
LABEL maintainer="CISL Cloud Pilot Team <cisl-cloud-pilot@ucar.edu>"

ENV CONDA_ENV=cisl-cloud-base

# Add User conda directory to path
ENV NB_PYTHON_PREFIX=${HOME}/.conda
ENV PATH=${NB_PYTHON_PREFIX}/bin:${PATH}

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
# Fix: https://github.com/koalaman/shellcheck/wiki/SC3014
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

###
# OS Package Install
###

# Install all OS dependencies for notebook server that starts but lacks all
# features (e.g., download as all possible file formats)
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
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
    # R pre-requisites
    # Perl library development files
    libperl-dev \
    # compression/decompression library
    libsnappy-dev \
    # GNU Standard C++ Library development files
    libstdc++-12-dev \
    # Build executable programs
    make \
    # Javascript runtime
    nodejs \
    # Javascript Package manager
    npm \
    # - pandoc is used to convert notebooks to html files
    pandoc \
    vim \
    # - run-one - a wrapper script that runs no more
    run-one && \
    apt-get clean && rm -rf /var/lib/apt/lists/* 

###
# Copy the .condarc file now so envs are created in ~/.conda
###
# GitHub Build
###
COPY configs/jupyter/base-notebook/config/.condarc /opt/conda/

###
# Local Build
###
#COPY config/.condarc /opt/conda/

WORKDIR /tmp

###
# Python Package Installation
###
# Copy package list for base OS and Kernels
###
# GitHub Build
###
COPY configs/jupyter/base-notebook/environment.yml configs/jupyter/base-notebook/requirements.txt configs/jupyter/base-notebook/npl-2023b.yml configs/jupyter/base-notebook/r-4.3.yml /tmp/

###
# Local Build
###
#COPY environment.yml requirements.txt npl-2023b.yml r-4.3.yml /tmp/

# Install required Python packages
RUN mamba install --quiet --yes \
    # NodeJS >= 18.0 is required for `jupyter lab build` command
    # https://github.com/jupyter/docker-stacks/issues/1901
    'nodejs>=18.0' \
    'notebook' \
    'jupyterhub' \
    'r-irkernel' \
    'conda-forge::nb_conda_kernels' && \
    # Pin NodeJS
    echo 'nodejs >=18.0' >> "${CONDA_DIR}/conda-meta/pinned" && \
    # nb_conda_kernels is required to save user environments as custom user notebook kernels that persist
    # Create a kernel named cisl-cloud-base from the environment.yml file
    mamba env create --name "${CONDA_ENV}" -f environment.yml && \
    # Create a kernel named NPL-2023b from the environment.yml file
    mamba env create --name "NPL-2023b" -f npl-2023b.yml && \
    # Create a kernel named R-4.3 from the r-4.3.yml file
    mamba env create --name "R-4.3" -f r-4.3.yml && \
    # Install extensions in to OS Python env
    pip install -r requirements.txt && \
    # Build Jupyter Config
    jupyter notebook --generate-config && \
    # Cleanup files no longer needed to reduce image size
    mamba clean --all -f -y && \
    npm cache clean --force && \
    jupyter lab clean && \
    rm -rf "/home/${NB_USER}/.cache/yarn" && \
    # Fix permissions
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Ask dask to read config from ${CONDA_DIR}/etc rather than
# the default of /etc, since the non-root jovyan user can write
# to ${CONDA_DIR}/etc but not to /etc
ENV DASK_ROOT_CONFIG=${CONDA_DIR}/etc

###
# Julia Install
###

ARG julia_version="1.9.1"

# Julia dependencies
# install Julia packages in /opt/julia instead of ${HOME}
ENV JULIA_DEPOT_PATH=/opt/julia \
    JULIA_PKGDIR=/opt/julia \
    JULIA_VERSION="${julia_version}"

# hadolint ignore=SC2046
RUN set -x && \
    julia_arch=$(uname -m) && \
    julia_short_arch="${julia_arch}" && \
    if [ "${julia_short_arch}" == "x86_64" ]; then \
      julia_short_arch="x64"; \
    fi; \
    julia_installer="julia-${JULIA_VERSION}-linux-${julia_arch}.tar.gz" && \
    julia_major_minor=$(echo "${JULIA_VERSION}" | cut -d. -f 1,2) && \
    mkdir "/opt/julia-${JULIA_VERSION}" && \
    wget -q "https://julialang-s3.julialang.org/bin/linux/${julia_short_arch}/${julia_major_minor}/${julia_installer}" && \
    tar xzf "${julia_installer}" -C "/opt/julia-${JULIA_VERSION}" --strip-components=1 && \
    rm "${julia_installer}" && \
    ln -fs /opt/julia-*/bin/julia /usr/local/bin/julia

# Show Julia where conda libraries are \
RUN mkdir /etc/julia && \
    echo "push!(Libdl.DL_LOAD_PATH, \"${CONDA_DIR}/lib\")" >> /etc/julia/juliarc.jl && \
    # Create JULIA_PKGDIR \
    mkdir "${JULIA_PKGDIR}" && \
    chown "${NB_USER}" "${JULIA_PKGDIR}" && \
    fix-permissions "${JULIA_PKGDIR}"

# Add Julia packages.
# Install IJulia as jovyan and then move the kernelspec out
# to the system share location. Avoids problems with runtime UID change not
# taking effect properly on the .local folder in the jovyan home dir.
RUN julia -e 'import Pkg; Pkg.update()' && \
    julia -e 'import Pkg; Pkg.add("HDF5")' && \
    julia -e 'using Pkg; pkg"add IJulia"; pkg"precompile"' && \
    # move kernelspec out of home \
    mv "${HOME}/.local/share/jupyter/kernels/julia"* "${CONDA_DIR}/share/jupyter/kernels/" && \
    chmod -R go+rx "${CONDA_DIR}/share/jupyter" && \
    rm -rf "${HOME}/.local" && \
    fix-permissions "${JULIA_PKGDIR}" "${CONDA_DIR}/share/jupyter"

# Expose the application on the port JupyterHub listens on
ENV JUPYTER_PORT=8888
EXPOSE $JUPYTER_PORT

# Configure container startup. Dask gateway requires ENTRYPOINT
ENTRYPOINT ["/srv/start"]

###
# Copy startup/healthcheck scripts & custom user profile
###
# GitHub Actions Build
###
# Copy local files as late as possible to avoid cache busting
COPY configs/jupyter/base-notebook/scripts/start /srv/start
# Currently need to have both jupyter_notebook_config and jupyter_server_config to support classic and lab
COPY configs/jupyter/base-notebook/scripts/jupyter_server_config.py configs/jupyter/base-notebook/scripts/docker_healthcheck.py /etc/jupyter/

###
# Local Build
###
#COPY scripts/start /srv/start
#COPY scripts/jupyter_server_config.py scripts/docker_healthcheck.py /etc/jupyter/

###
# GitHub Build
###
# Copy the bash profile to autoload conda envs
COPY configs/jupyter/base-notebook/config/.profile /.bash_profile
COPY configs/jupyter/base-notebook/config/.bashrc /etc/bash.bashrc

###
# Local Build
###
#COPY config/.profile /.bash_profile
#COPY config/.bashrc /etc/bash.bashrc

# Cleanup files that were already installed
RUN rm -rf /tmp/environment.yml && \
    rm -rf /tmp/requirements.txt && \
    rm -rf /tmp/npl-2023b.yml && \
    rm -rf /tmp/r-4.3.yml 
    
# Legacy for Jupyter Notebook Server, see: [#1205](https://github.com/jupyter/docker-stacks/issues/1205)
RUN sed -re "s/c.ServerApp/c.NotebookApp/g" \
    /etc/jupyter/jupyter_server_config.py > /etc/jupyter/jupyter_notebook_config.py && \
    fix-permissions /etc/jupyter/ 

# Used to allow folder deletions from user
RUN sed -i 's/c.FileContentsManager.delete_to_trash = False/c.FileContentsManager.always_delete_dir = True/g' /etc/jupyter/jupyter_server_config.py

# HEALTHCHECK documentation: https://docs.docker.com/engine/reference/builder/#healthcheck
# This healtcheck works well for `lab`, `notebook`, `nbclassic`, `server` and `retro` jupyter commands
# https://github.com/jupyter/docker-stacks/issues/915#issuecomment-1068528799
HEALTHCHECK --interval=5s --timeout=3s --start-period=5s --retries=3 \
    CMD /etc/jupyter/docker_healthcheck.py || exit 1

# Switch back to jovyan to avoid accidental container runs as root
USER ${NB_UID}

WORKDIR "${HOME}"

