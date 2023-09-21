# Notes for adding these kernels to the base image. 
# These commands were run as part of the base image and worked for installing and displaying the kernel in the launcher. 
# These Dockerfiles currently are mostly for notes and the additional installation of these kernels has not been tested.
# Test build

FROM cislcloudpilot/cisl-cloud-base:latest

USER root

# Bash Kernel
RUN mamba install --yes \
    'bash_kernel'

# C++ kernel
RUN mamba install --yes \
    'xeus-cling'

# Julia kernel
ARG julia_version="1.9.1"

# Julia dependencies
# install Julia packages in /opt/julia instead of ${HOME}
ENV JULIA_DEPOT_PATH=/opt/julia \
    JULIA_PKGDIR=/opt/julia \
    JULIA_VERSION="${julia_version}"

WORKDIR /tmp

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

# Matlab kernel
RUN pip install jupyter-matlab-proxy

# R kernel
# R packages including IRKernel which gets installed globally.
# r-e1071: dependency of the caret R package
RUN mamba install --yes \
    'r-base' \
    'r-caret' \
    'r-crayon' \
    'r-devtools' \
    'r-e1071' \
    'r-forecast' \
    'r-hexbin' \
    'r-htmltools' \
    'r-htmlwidgets' \
    'r-irkernel' \
    'r-nycflights13' \
    'r-randomforest' \
    'r-rcurl' \
    'r-rmarkdown' \
    'r-rodbc' \
    'r-rsqlite' \
    'r-shiny' \
    'r-tidymodels' \
    'r-tidyverse' \
    'rpy2' \
    'unixodbc' && \
    mamba clean --all -f -y

# Scala kernel
# Java required for Scala
RUN apt-get update && \
    apt-get install -y openjdk-8-jdk && \
    apt-get install -y ant && \
    apt-get clean;

# Scala Kernel
RUN curl -Lo coursier https://git.io/coursier-cli && \
    chmod +x coursier && \
    ./coursier launch --fork almond -- --install --force --global && \
    rm -f coursier

USER ${NB_UID}
