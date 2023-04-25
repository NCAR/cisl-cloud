# CISL Cloud Pilot Documentation

[MkDocs](https://www.mkdocs.org/getting-started/) has an easy to use implementation to create professional documentation pages. <br/>
We can host this documentation on the on-prem cloud. <br/>

## Running MkDocs from this repo

* `git clone https://github.com/NCAR/cisl-cloud.git` - Clone the github repo.
* `cd cisl-cloud/docs/` - Change to the cisl-cloud docs directory.
* `mkdocs serve` - Start the live-reloading docs server on http://127.0.0.1:8000

## MkDocs Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

# Project layout

    mkdocs.yml    # The configuration file.
    docs/
        about.md # The project about page
        features.md # A list of potential features for the project
        index.md  # The documentation homepage.
        layout.md # Outline of site directories and files
        services.md # An initial list of services we will offer