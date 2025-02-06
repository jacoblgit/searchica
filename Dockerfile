FROM python:3.12

# Set working directory
WORKDIR /app/backend

# Set production environment
ENV FLASK_ENV=production

# Copy requirements from root directory
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy backend and data directories
COPY backend/ .
COPY data/ ../data/

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]