# https://pythonspeed.com/articles/base-image-python-docker-images/
FROM python:3.7.6-slim-buster

# PHASE 1 - Install general development nice-to-haves
RUN apt-get update; apt-get clean
RUN apt-get upgrade -y
RUN apt-get install apt-utils -y
RUN apt-get install git -y
RUN apt-get install build-essential -y
RUN apt-get install cython3 -y

# PHASE 2 - Install dependencies for bootstrap.sh
# Using a virtual network computing (VNC) screen:
# https://medium.com/dot-debug/running-chrome-in-a-docker-container-a55e7f4da4a8
RUN apt-get install -y x11vnc
RUN apt-get install -y xvfb
RUN apt-get install -y fluxbox
RUN apt-get install -y wget
RUN apt-get install -y wmctrl

# PHASE 3 - upgrade pip
RUN pip install --upgrade pip

# PHASE 4 - pip install requirements (Python project dependencies)
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

# PHASE 5 - copy bootstrap.sh to root and run it within the Docker container
COPY bootstrap.sh /app
CMD 'dos2unix bootstrap.sh'
CMD './bootstrap.sh'
