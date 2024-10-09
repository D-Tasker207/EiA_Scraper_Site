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
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app 

# Set working directory for the backend
WORKDIR /webserver

COPY requirements.txt ./

# Install backend build dependencies
RUN apt-get update && apt-get install -y \
    firefox-esr \
    xvfb \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn

# Copy backend source code & resources
COPY app/ ./app/

# Copy the frontend build from the frontend-build stage
COPY --from=frontend-build /app/client/static/dist ./app/static/dist/

# Copy the entrypoint script
COPY run.py ./

# Expose the port Flask will run on (container's internal port)
EXPOSE 5000

# Start the Flask app using Gunicorn
CMD ["gunicorn", "--worker-class", "gthread", "--bind", "0.0.0.0:5000", "--threads", "2", "run:app"]