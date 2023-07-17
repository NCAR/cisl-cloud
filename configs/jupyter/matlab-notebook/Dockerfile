# Notes for adding these kernels to the base image. 
# These commands were run as part of the base image and worked for installing and displaying the kernel in the launcher. 
# These Dockerfiles currently are mostly for notes and the additional installation of these kernels has not been tested.

FROM ncote/cisl-cloud-base:latest

COPY configs/jupyter/matlab-notebook/requirements.txt /tmp/

# MatLab Kernel
RUN pip install -r /tmp/requirements.txt \
    rm /tmp/requirements.txt

USER ${NB_UID}
