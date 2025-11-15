FROM python:3.12

# working directory
WORKDIR /app

# cache directories
RUN mkdir -p /tmp/numba_cache /tmp/huggingface_cache && \
    chmod -R 777 /tmp/numba_cache /tmp/huggingface_cache

# Environment variables
ENV NUMBA_CACHE_DIR=/tmp/numba_cache
ENV HF_HOME=/tmp/huggingface_cache
ENV TRANSFORMERS_CACHE=/tmp/huggingface_cache
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download CLIP model & processor
RUN python - <<'EOF'
from transformers import CLIPModel, CLIPProcessor
CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
EOF

# Copy code
COPY . .

# write permissions
RUN chmod -R g+rwX /app && \
    chmod -R 777 /tmp/huggingface_cache /tmp/numba_cache

# Expose port
EXPOSE 8000
