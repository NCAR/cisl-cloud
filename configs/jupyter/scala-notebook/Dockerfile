# Notes for adding these kernels to the base image. 
# These commands were run as part of the base image and worked for installing and displaying the kernel in the launcher. 
# These Dockerfiles currently are mostly for notes and the additional installation of these kernels has not been tested.

FROM ncote/cisl-cloud-base:latest

USER root

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
