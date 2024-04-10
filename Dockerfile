# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 80 for the API server
EXPOSE 80

# Run the command to start the API server
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
CMD ["sh", "-c", "tail -f /dev/null"]