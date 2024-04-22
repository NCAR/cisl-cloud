# CISL Cloud Pilot Project
| Documentation Website Builds | ![GitHub Pages Status](https://github.com/NCAR/cisl-cloud/actions/workflows/pages/pages-build-deployment/badge.svg) | ![Documentation CI/CD Status](https://github.com/NCAR/cisl-cloud/actions/workflows/docs-cicd.yaml/badge.svg) |
|---|---|---|
| **Jupyter Singleuser CPU image build** | ![CPU Image Test Build Status](https://github.com/NCAR/cisl-cloud/actions/workflows/build-basenb-test.yaml/badge.svg) | ![CPU Image Build Status](https://github.com/NCAR/cisl-cloud/actions/workflows/build-push-basenb.yaml/badge.svg) |
| **Jupyter Tensorflow GPU image builds** | ![Tensorflow Test Build Status](https://github.com/NCAR/cisl-cloud/actions/workflows/tensorflow-build-test.yaml/badge.svg) | ![Tensorflow Image Build & Push](https://github.com/NCAR/cisl-cloud/actions/workflows/build-push-tfgpu.yaml/badge.svg) |
| **Jupyter PyTorch GPU image builds** | ![PyTorch Test Build Status](https://github.com/NCAR/cisl-cloud/actions/workflows/pytorch-build-test.yaml/badge.svg) | ![PyTorch Image Build & Push](https://github.com/NCAR/cisl-cloud/actions/workflows/build-push-pytgpu.yaml/badge.svg) |


Follow our up to date [Kanban](https://jira.ucar.edu/secure/RapidBoard.jspa?rapidView=220&projectKey=CCPP).

## This Repository

This repository is a place for the CCPP team to push code for configurations and documentation.

## Dev/Main branch Overview

    .github/    # GitHub Actions and Workflows
    cluster/    # Kubernetes cluster & JupyterHub deployment config files
    images/     # Custom container image files and build instructions
    README.md   # The file you are reading now

We utilize a GitFlow development strategy where changes are made to feature branches, typically dev for this repository, and pull requests are made to merge changes back in to the main branch. 

## Workflow

GitHub Action Workflows are in place and triggered to build images when changes are made to specific paths in the dev or main branches. These paths are currently:

    configs/argocd/**
    configs/jupyter/base-notebook/**
    configs/jupyter/gpu-pyt-notebook/**
    configs/jupyter/gpu-tf-notebook/**
    configs/jupyter/rdp-notebook/**

Any changes made to the docs branch will also kick of a GitHub Action workflow. 

## Docs Branch

All the documentation is hosted out of the docs branch of the repository. Changes made to that branch will trigger a rebuild of the JupyterBook files and a GitHub pages rebuild, in to the gh-pages branch. A new container image will also be created, the associated Helm chart for the cloud hosted version will be updated, and the github-actions bot will open a PR to merge dev in to main on a successful Action run. 

## Goals
* Improve understanding of how scientific community might use and benefit from an on-prem cloud
    * Which services fit on-prem better than traditional HPC and/or public cloud
* Gain experience within CISL deploying and operating an on-prem cloud and associated services
* Improve CISL ability to support interactive analysis workflows in environment where data is globally distributed
* Increase user visibility in to on-prem cloud offerings
* Develop metrics to showcase project value & feasibility
* Gain experience with Agile Project Management