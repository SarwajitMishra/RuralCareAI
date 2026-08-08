# =============================================================================
# RuralCare AI - container image
#
# Bundles the Streamlit app, trained model artifacts, and Python
# dependencies into a single portable image. The Local LLM (Gemma 3)
# runs in a separate "ollama" container - see docker-compose.yml.
# =============================================================================

FROM python:3.11-slim

# System libraries required by opencv-python (image analysis) and
# faster-whisper/PyAV (voice transcription).
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first so the (large) dependency layer is
# cached across rebuilds that only change application code.
# --timeout/--retries make this resilient to slow/flaky connections
# while downloading large wheels (tensorflow, torch).
COPY requirements.txt .
RUN pip install --no-cache-dir --timeout=120 --retries=10 -r requirements.txt

# Application code.
COPY app.py .
COPY src/ ./src/

# Trained model artifacts and static reference datasets, so the image
# is self-contained and runnable on any machine without a separate
# training/setup step. (Excludes the runtime SQLite DB / ChromaDB
# store / uploaded images / generated reports - those are mounted as
# volumes in docker-compose.yml so they persist and aren't baked into
# the image.)
COPY models/ ./models/
COPY data/Training.csv data/Testing.csv ./data/

# Runtime directories (populated via volumes at container start).
RUN mkdir -p data uploads/images reports logs

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py", \
    "--server.port=8501", \
    "--server.address=0.0.0.0", \
    "--server.headless=true", \
    "--server.fileWatcherType=none"]
