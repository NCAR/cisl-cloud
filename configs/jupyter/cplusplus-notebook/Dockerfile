# Notes for adding these kernels to the base image. 
# These commands were run as part of the base image and worked for installing and displaying the kernel in the launcher. 
# These Dockerfiles currently are mostly for notes and the additional installation of these kernels has not been tested.

FROM ncote/cisl-cloud-base:latest

COPY configs/cplusplus-notebook/environment.yml /home/jovyan

# C++ Kernel
RUN mamba env create -f environment.yml

USER ${NB_UID}
