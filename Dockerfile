# Use an official lightweight Python image.
FROM python:3.8-slim

# Set environment variables to prevent Python from writing pyc files to disc (which isn't necessary)
ENV PYTHONDONTWRITEBYTECODE 1

# Set environment variables to prevent Python from buffering stdout and stderr (which isn't necessary)
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define the command to run the app using gunicorn as the web server
#CMD gunicorn --workers=2 --threads=4 --bind 0.0.0.0:$PORT app:app
CMD exec gunicorn --workers=2 --threads=4 --bind 0.0.0.0:${PORT} app:app

