# CISL Cloud Pilot Project
| GitHub Pages |  ![GitHub Pages Status](https://github.com/NCAR/cisl-cloud/actions/workflows/pages/pages-build-deployment/badge.svg) | |
|---|---|---|
| Documentation Website Builds | ![Documentation Test Build Status](https://github.com/NCAR/cisl-cloud/actions/workflows/docs-cicd-test.yaml/badge.svg) | ![Documentation CI/CD Status](https://github.com/NCAR/cisl-cloud/actions/workflows/docs-cicd.yaml/badge.svg) |
| **Jupyter Singleuser CPU image build** | ![CPU Image Test Build Status](https://github.com/NCAR/cisl-cloud/actions/workflows/build-basenb-test.yaml/badge.svg) | ![CPU Image Build Status](https://github.com/NCAR/cisl-cloud/actions/workflows/build-push-basenb.yaml/badge.svg) |
| **Jupyter Singleuser GPU image builds** | ![Tensorflow Image Build Status](https://github.com/NCAR/cisl-cloud/actions/workflows/build-push-tfgpu.yaml/badge.svg) | ![PyTorch Image Build Status](https://github.com/NCAR/cisl-cloud/actions/workflows/build-push-pytgpu.yaml/badge.svg) |

* ***Note*** - The TensorFlow build does not work on GitHub hosted runners


Follow our up to date [Kanban](https://jira.ucar.edu/secure/RapidBoard.jspa?rapidView=220&projectKey=CCPP).

## This Repository

This repository is a place for the CCPP team to push code for configurations and documentation.

## Repo Overview

    .github/    # GitHub Actions and Workflows
    cluster/    # Kubernetes cluster & JupyterHub deployment config files
    configs/    # Configuration files for different services implemented
    docs/       # Potential Documentation website information
    README.md   # The file you are reading now

## Goals
* Improve understanding of how scientific community might use and benefit from an on-prem cloud
    * Which services fit on-prem better than traditional HPC and/or public cloud
* Gain experience within CISL deploying and operating an on-prem cloud and associated services
* Improve CISL ability to support interactive analysis workflows in environment where data is globally distributed
* Increase user visibility in to on-prem cloud offerings
* Develop metrics to showcase project value & feasibility
* Gain experience with Agile Project Management