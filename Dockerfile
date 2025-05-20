# Use official Python image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy backend folder into container
COPY backend/ .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose Railway port
ENV PORT=5000
EXPOSE 5000

# Run app
CMD ["python", "app.py"]
