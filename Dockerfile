# ---------------------------
# Dockerfile for Streamlit App
# ---------------------------

# 1. Use lightweight Python base
FROM python:3.10-slim

# 2. Set working directory
WORKDIR /app

# 3. Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy requirements file first (to leverage Docker cache)
COPY requirements.txt .

# 5. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the entire project into container
COPY . .

# 7. Expose Streamlit default port
EXPOSE 8501

# 8. Set environment variables for Streamlit
ENV STREAMLIT_PORT=8501
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# 9. Run Streamlit when container starts
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

