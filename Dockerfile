# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app 

# Copy the current directory contents into the container at /app
# Install any needed packages specified in requirements.txt
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Run the serverless function when the container launches
CMD ["python3", "app.py"]