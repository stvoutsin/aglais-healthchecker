FROM python:3
WORKDIR /project
ADD src/ /project
VOLUME src/data /project/data
RUN pip install requests
RUN python3 setup.py install
CMD [ "python3", "aglais_healthchecker/healthcheck.py", "-c", "/project/data/sample-config-docker.json"]
