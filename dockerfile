FROM python:3.11-slim

# Set working directory
WORKDIR /data-analysis-copilot

# Copy requirements file if you have one
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Python program
COPY . .

# Run the program
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.fileWatcherType=poll"]