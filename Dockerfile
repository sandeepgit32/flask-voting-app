FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY src/requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY src/ .

# Expose port 5000
EXPOSE 5000

# Make the run.sh file executable
RUN chmod +x run.sh

# Run the application
ENTRYPOINT ["bash", "run.sh"]