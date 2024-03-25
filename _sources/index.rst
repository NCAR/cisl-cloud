NSF NCAR | CISL Cloud
=======================

.. banner::
   :image: images/cirrus.png
   :caption: Photo by Nick Cote
   :class: dark-banner


This is the NSF NCAR | CISL Cloud Gateway. We host dependable storage, compute, and networking resources operated 
and maintained by CISL staff that are highly available to the NSF NCAR community. This project and the services run on it
are still in a introductory pilot phase. As such, there are currently no well defined SLAs as active development is ongoing. 

.. raw:: html

   <span class="d-flex justify-content-center py-4">
     <a href="overview/getting-started.html" role="button" class="btn btn-light btn-lg">
       Getting Started on the Cloud
     </a>
   </span>

Information
------------------------

Built with |jbook|

NSF NCAR received one-time funding to evaluate an on-premise (on-prem) cloud. An on-prem cloud offers the ability to tailor the environment
to meet the needs of the scientific community while being fully in control of access and security. Initial use cases were gathered
from the scientific community. The services provided are tailored to address those use cases. Agile product management methods
are also being utilized to provide users an interface to the team via a Product Owner while prioritizing and accomplishing work
on a Kanban board.

This project is still in a pre-production stage and user data stored on our services is not guaranteed, even with robust architecture. 
Ensuring the safety of important work is paramount, and one effective strategy is to back up crucial data on production 
storage or in code repositories. Leveraging tools such as Git, coupled with our on-prem storage options, not only minimizes 
the risk of loss but also provides a structured approach to version control, collaborative efforts, and efficient tracking of 
changes. This proactive approach becomes particularly valuable in mitigating potential disruptions, allowing for the seamless 
reproduction of work in the event of an outage in our pre-production services. 

Resources
------------------------

NSF UCAR Network Access Required
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. raw:: html

    <span class="d-flex justify-content-center py-4">
      <a href="https://hub.k8s.ucar.edu/">
      <figure>
        <img src="_static/harbor.png">
        <figcaption style="text-align:center">Harbor Container Registry</figcaption>
        <figcaption style="text-align:center"><a href="how-to/K8s/harbor/harbor-intro.html">Link to Docs</a></figcaption>
      </figure>
      </a>
      <a href="how-to/K8s/Hosting/deploy">
      <figure>
        <img src="_static/argo.png">
        <figcaption style="text-align:center">Argo CD Docs</figcaption>
      </figure>
      </a>
      <a href="https://stratus-admin.ucar.edu:10443/asview">
      <figure>
        <img src="_static/stratus.png">
        <figcaption style="text-align:center">Stratus Object Storage</figcaption>
        <figcaption style="text-align:center"><a href="how-to/Stratus/stratus-intro.html">Link to Docs</a></figcaption>
      </figure>
      </a>
    </span>
    <span class="d-flex justify-content-center py-4">
      <a href="https://jupyter.k8s.ucar.edu/">
      <figure>
        <img src="_static/jhub-logo.png">
        <figcaption style="text-align:center">K8s JupyterHub</figcaption>
        <figcaption style="text-align:center"><a href="how-to/k8sJH/k8sJH-intro.html">Link to Docs</a></figcaption>
      </figure>
      </a>
      <a href="https://binder.k8s.ucar.edu/">
      <figure>
        <img src="_static/binder/binder-logo.png">
        <figcaption style="text-align:center">K8s Binder</figcaption>
        <figcaption style="text-align:center"><a href="how-to/binderhub/binderhub.html">Link to Docs</a></figcaption>
      </figure>
      </a>
      <a href="https://jupyterhub.hpc.ucar.edu/">
      <figure>
        <img src="_static/jhub-logo.png">
        <figcaption style="text-align:center">HPC JupyterHub</figcaption>
        <figcaption style="text-align:center"><a href="https://arc.ucar.edu/knowledge_base/70549913">Link to Docs</a></figcaption>
      </figure>
      </a>
    </span>
   
Publicly Accessible
^^^^^^^^^^^^^^^^^^^^^^

.. raw:: html

   <span class="d-flex justify-content-center py-4">
     <a href="https://ncar-cisl.2i2c.cloud/">
     <figure>
       <img src="_static/jhub-logo.png">
       <figcaption style="text-align:center">2i2c JupyterHub</figcaption>
       <figcaption style="text-align:center"><a href="how-to/2i2cJH/2i2cJH-intro.html">Link to Docs</a></figcaption>
      </figure>
     </a>
   </span>

Documentation
-------------

.. rst-class:: text-center

   Click the button below to read the CISL Cloud documentation.

.. raw:: html

   <span class="d-flex justify-content-center py-4">
     <a href="main.html" role="button" class="btn btn-primary btn-lg">
       Read the documentation
     </a>
   </span>

.. |jbook| image:: images/jupyterbook.svg
   :target: https://jupyterbook.org
