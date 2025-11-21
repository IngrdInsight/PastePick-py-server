FROM python:3.12
WORKDIR /app

# cache directories
RUN mkdir -p /tmp/numba_cache /tmp/huggingface_cache /tmp/u2net_cache && \
    chmod -R 777 /tmp/numba_cache /tmp/huggingface_cache /tmp/u2net_cache

# env vars
ENV NUMBA_CACHE_DIR=/tmp/numba_cache
ENV HF_HOME=/tmp/huggingface_cache
ENV TRANSFORMERS_CACHE=/tmp/huggingface_cache
ENV U2NET_HOME=/tmp/u2net_cache
ENV HOME=/tmp
ENV PYTHONUNBUFFERED=1


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copy code
COPY . .

# Make directories accessible
RUN chmod -R g+rwX /app && \
    chmod -R 777 /tmp/huggingface_cache /tmp/numba_cache

EXPOSE 8000

USER 1001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
