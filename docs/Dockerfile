FROM python:3
RUN pip install mkdocs
COPY /docs /docs/docs
COPY mkdocs.yml /docs
EXPOSE 8000
WORKDIR /docs
ENTRYPOINT ["mkdocs"]
CMD ["serve", "--dev-addr=0.0.0.0:8000"]