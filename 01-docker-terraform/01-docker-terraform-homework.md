# QUESTION 1 - Understanding docker images


* get the image automatically and run the python:3.13 container

`docker run -it --rm --entrypoint bash python:3.13`

* inside the container find the version of pip

`pip --version`

OUTPUT:
```
/# pip --version
pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)
```

# QUESTION 2 - Understanding docker networking and docker-compose

* the hostport:internalport of the 'db' service is ports: - '5433:5432'
* which means any internal services within the docker network will use port 5432 to connect to the 'db' service 

* So, the hostname and port that pgadmin should use to connect to the postgres database is `db:5432`
