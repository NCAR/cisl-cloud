# User requested use cases

## Running Tutorials
An on-premise cloud would allow hosting of user tutorials in an environment controlled by the organization. Access to systems would be controlled by administrators and tutorial leaders in a programmatic way speeding up the on-boarding and off-boarding process. Golden images that allow an identical starting point for each tutorial would be hosted on shared storage. These images would be deployed and assigned to users in a programmatic way by administrators and tutorial leaders. Remote viewing access for users and administrators simultaneously would also create an environment where it was easier to help troubleshoot issues during the tutorials.  

## Jupyter Services
JupyterHub is running on a bare metal kubernetes (k8s) cluster deployed with Rancher RKE2. This instance will have authentication for individual users. A user will be able to select from a few different sized environments, some offering GPU capabilities, and a new instance will be spun up with KubeSpawner from a base image. The base image will contain a few common kernels and packages but users will be able to customize their instance with the packages they require. Shared storage will be provided with a unique directory for each user to keep their files. GLADE read-only access will also be provided to each instance so datasets can be accessed from an internal nearby location. Dask services will also be provided in the form of dask.distributed, dask-kubernetes, dask-gateway, and dask-jobqueue for running against HPC resources. Web based visualization capabilities will also be provided but access to these websites hosted via JupyterHub will be limited to authorized users of the JupyterHub instance. 

## Data Access
#### GLADE Access
GLADE Access will be provided to JupyterHub instances for users to read GLADE datasets in a close location. An NFS mount to other resources hosted on CISL on-prem cloud hardware may be made available as well. 

#### Object Storage
CISL provides an Object Storage system named STRATUS with an API available to access S3 buckets in the same fashion as AWS. STRATUS will be utilized to provide API access to required datasets as well as possibly hosting terraform state files used in creating other user resources. Administrators on our STRATUS implementation will be responsible for user management and the creation and maintenance of new buckets. An elastic and flexible catalog for datasets will be implemented with preview or thumbnail methods to ensure access to the correct datasets. Uncoupling large datasets in to individual components will be part of the implementation process. 

#### Shared Storage
Shared Storage will be provided to JupyterHub instances via the NFS protocol. Access to these mounts from other resources hosted on CISL on-prem cloud hardware may be made available as well.

#### Local Transfers
A method to allow for quick and easy data & output transfers to local systems will be provided with detailed instructions. 

## Web Visualization Hosting
Real time interactive and customizable web visualizations will be hosted in various methods on CISL infrastructure. Applications such as Bokeh, Panel, Viola, etc. can host interactive visualizations from Jupyter Notebooks or Python applications. Users will be provided with a programmatic way to deploy these applications with public or private URLs in a stable highly available environment.

## File Sharing
The CISL on-prem infrastrucutre provides a location that is easier to access and share information and files. Applications like NextCloud can be provisioned to host file sharing services. 

## Creating k8s clusters
Rancher is part of the on-prem software stack and can be utilized to provision users their own k8s cluster for development or production use cases. Access to most storage resources can also be provided in these deployments. 

## Hosting Containerized Applications
Users will be able to deploy their containerized applications in to the k8s cluster which provides a highly available and accessible hosting location. Smaller individual JupyterLab containers can be provisioned with the ability to host public facing web visualizations via notebooks and code running in the JupyterLab containers.

## Hosting Virtual Machines (VMs)
If needed, VM's can also be provided either from pre configured templates or as bare instances and will be hosted either in a VMware cluster or the k8s cluster.