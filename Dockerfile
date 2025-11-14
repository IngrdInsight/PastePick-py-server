FROM python:3.12
WORKDIR /app

# cache directories
RUN mkdir -p /tmp/numba_cache /tmp/huggingface_cache && \
    chmod -R 777 /tmp/numba_cache /tmp/huggingface_cache

# env vars
ENV NUMBA_CACHE_DIR=/tmp/numba_cache
ENV HF_HOME=/tmp/huggingface_cache
ENV TRANSFORMERS_CACHE=/tmp/huggingface_cache
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download the CLIP
RUN python -c "from transformers import CLIPModel, CLIPProcessor; \
    CLIPModel.from_pretrained('openai/clip-vit-base-patch32'); \
    CLIPProcessor.from_pretrained('openai/clip-vit-base-patch32')"

# Copy code
COPY . .

# Make directories accessible
RUN chmod -R g+rwX /app && \
    chmod -R 777 /tmp/huggingface_cache /tmp/numba_cache

EXPOSE 8000

USER 1001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
