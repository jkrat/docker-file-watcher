# Use an official Python runtime as a parent image
FROM python:3.9-slim

ENV INCOMING_DIR="/home/containeruser/src/incomingFiles" \
    NEXT_DIR="/home/containeruser/src/nextFiles"

# # Install system dependencies
RUN apt-get update && apt-get install -y

# Set the working directory in the container
# RUN useradd --create-home containeruser
# USER containeruser
WORKDIR /home/containeruser

# Copy the current directory contents into the container at /app
# COPY --chown=containeruser src/ src/
COPY src/ src/

# RUN mkdir $INCOMING_DIR 
# RUN chown -R containeruser:containeruser $INCOMING_DIR
# RUN chmod -R 755 $INCOMING_DIR

RUN mkdir $NEXT_DIR 
# RUN chown -R containeruser:containeruser $NEXT_DIR
# RUN chmod -R 755 $NEXT_DIR

# Run the application
ENTRYPOINT ["python", "-m", "src.file_access.app"]