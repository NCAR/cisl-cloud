# CISL Cloud Pilot Project


| GitHub Action Name | Action Status | Action Status |
|---|---|---|
| Documentation Website Builds | ![GitHub Pages Status](https://github.com/NCAR/cisl-cloud/actions/workflows/pages/pages-build-deployment/badge.svg) | ![Documentation CI/CD Status](https://github.com/NCAR/cisl-cloud/actions/workflows/docs-cicd.yaml/badge.svg) |

Jupyter Image builds have been moved to the [ccpp-jhub-images repository](https://github.com/NCAR/ccpp-jhub-images)

Follow our up to date [Kanban](https://jira.ucar.edu/secure/RapidBoard.jspa?rapidView=220&projectKey=CCPP).

## This Repository

This repository is a place for the CCPP team to push code for configurations and documentation.

## Dev/Main branch Overview

    .github/    # GitHub Actions and Workflows
    cluster/    # Kubernetes cluster & JupyterHub deployment config files
    README.md   # The file you are reading now

We utilize a GitFlow development strategy where changes are made to feature branches, typically dev for this repository, and pull requests are made to merge changes back in to the main branch. 

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