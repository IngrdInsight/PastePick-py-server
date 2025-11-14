FROM python:3.12
WORKDIR /app


RUN mkdir -p /tmp/numba_cache && chmod -R 777 /tmp/numba_cache
ENV NUMBA_CACHE_DIR=/tmp/numba_cache
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .

# Make app directory group-writable
RUN chmod -R g+rwX /app

EXPOSE 8000

USER 1001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
