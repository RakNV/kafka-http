# Use the official Python image as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Expose the port that FastAPI will run on (adjust as needed)
EXPOSE 8080

# Define the entry point for your FastAPI application
ENTRYPOINT ["python", "main.py"]