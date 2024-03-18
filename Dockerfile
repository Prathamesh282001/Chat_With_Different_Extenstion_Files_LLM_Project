# Use the official Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app


# Install required Python packages
#RUN pip install --no-cache-dir -r requirements.txt
COPY requirements.txt .

# Install required Python packages
RUN pip install -r requirements.txt --default-timeout=100 future


# Copy the rest of the application files to the container's working directory
COPY . .

EXPOSE 80

# Command to run your Streamlit application
CMD ["chainlit", "run", "app.py", "--host=0.0.0.0", "--port=80", "--headless"]