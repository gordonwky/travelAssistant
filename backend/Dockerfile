# ----------------------
# Base image
# ----------------------
FROM python:3.13-slim

# ----------------------
# Environment variables
# ----------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ----------------------
# Set working directory inside container
# ----------------------
WORKDIR /app





# ----------------------
# Install system dependencies
# ----------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv
# ----------------------
# Install Python dependencies
# ----------------------

COPY pyproject.toml  uv.lock ./

RUN uv sync --frozen --no-cache

# ----------------------
# Copy backend project files
# ----------------------
COPY . .

# ----------------------
# Expose port for FastAPI
# ----------------------
EXPOSE 8000

# ----------------------
# Run FastAPI app using Uvicorn
# ----------------------
CMD ["uv", "run",  "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]