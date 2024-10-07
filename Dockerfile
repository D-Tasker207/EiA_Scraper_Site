# =========================
# Stage 1: Build React Frontend
# =========================
FROM node:18-alpine AS frontend-build

# Set working directory for the frontend, and copy package.json and package-lock.json
# and install dependencies
WORKDIR /app/client
COPY client/package*.json ./
RUN npm install

# Copy the frontend source code
COPY client/ ./ 

# Build the frontend for production
RUN npm run build

# =========================
# Stage 2: Final Production Image with Frontend
# =========================
FROM python:3.11-slim AS final

# Set environment variables for Flask
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app 

# Set working directory for the backend
WORKDIR /webserver

# Install backend build dependencies
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy backend source code & resources
COPY app/ ./app/

# Copy the frontend build from the frontend-build stage
COPY --from=frontend-build /app/client/static/dist ./app/static/dist/

# Copy the entrypoint script
COPY run.py ./

# Install Gunicorn to run the Flask app
RUN pip install gunicorn

# Expose the port Flask will run on (container's internal port)
EXPOSE 5000

# Start the Flask app using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]