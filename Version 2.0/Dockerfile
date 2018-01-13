# Start out with the same node image
FROM node:8.9.1-alpine

RUN mkdir /usr/lab5

# Copy all local files to VM
# Hint: add a .dockerignore file to ignore certain files on COPY
COPY . /usr/lab5

# Set the working directory
WORKDIR /usr/lab5

# Retrieve all dependencies
RUN npm install

# Expose port 3000
EXPOSE 3000

# What gets called when VM launches
CMD node app.js
