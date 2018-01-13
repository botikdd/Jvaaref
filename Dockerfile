# Start out with the same node image
FROM python:3

# installing pip3 and necessary module for subprocess
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip
RUN pip3 install pylint
RUN pip3 install numpy
RUN pip3 install matplotlib
RUN pip3 install opencv-python

RUN mkdir -p /usr/team/Jvaaref/lab5

# Copy all local files to VM
# Hint: add a .dockerignore file to ignore certain files on COPY
COPY . /usr/team/Jvaaref/lab5

# Set the working directory
WORKDIR /usr/team/Jvaaref/lab5

# What gets called when VM launches
CMD python ./AngleDetection.py