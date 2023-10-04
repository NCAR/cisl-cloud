# Use the Apache HTTP server image
FROM httpd:2.4

# Copy HTML files created by `jupyter-book build .` in to directory apache serves out of
COPY docs/_build/html/. /usr/local/apache2/htdocs/