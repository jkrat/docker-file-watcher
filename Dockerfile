# Use an official Python runtime as a parent image
FROM python:3.9-slim

ENV INCOMING_DIR="/home/containeruser/src/incomingFiles" \
    NEXT_DIR="/home/containeruser/src/nextFiles"

# # Install system dependencies
RUN apt-get update && apt-get install -y

# Set the working directory in the container
RUN useradd --create-home containeruser
USER containeruser
WORKDIR /home/containeruser

ENV VIRTUALENV=/home/containeruser/venv
RUN python3 -m venv $VIRTUALENV
ENV PATH="$VIRTUALENV/bin:$PATH"

# Copy the src directory contents into the container at /src
COPY --chown=containeruser src/ src/

RUN mkdir $NEXT_DIR 
RUN chown -R containeruser:containeruser $NEXT_DIR
RUN chmod -R 755 $NEXT_DIR

# Run the application
ENTRYPOINT ["python", "-m", "src.file_access.app"]