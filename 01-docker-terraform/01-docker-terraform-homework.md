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
