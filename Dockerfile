FROM python:3.8

MAINTAINER netanelkoli@gmail.com

# Set the working directory in the container
WORKDIR /code

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY ricknmorty.py .

# Listen on this port for incoming connections
EXPOSE 5000

# Command to run on container start
CMD [ "python", "./ricknmorty.py" ]
