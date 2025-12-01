<div align="center">

# PastePick Python Server
**Python image processing server application for PastePick**


![GitHub License](https://img.shields.io/github/license/IngrdInsight/PastePick-py-server)
![GitHub repo size](https://img.shields.io/github/repo-size/IngrdInsight/PastePick-py-server)

</div>

---


## Download and Install

### Clone the Repository

```bash
git clone https://github.com/IngrdInsight/PastePick-py-server.git
cd PastePick-py-server
```

### Create a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration


1. Update environment variables in .env:

```env
ALLAS_ENDPOINT=
ALLAS_ACCESS_KEY=
ALLAS_SECRET_KEY=
ALLAS_BUCKET=

# Database Configuration
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=

# Server Configuration
HOST=0.0.0.0
PORT=8000

```

3. If needed, initialize the database during the first run. Insructions are available here: [link]([https://github.com/IngrdInsight/PastePick-server/README.md](https://github.com/IngrdInsight/PastePick-server/blob/main/README.md))

---

## Run the Server

**Option 1: Simple run**

```bash
python main.py
```

**Option 2: Using uvicorn (recommended for development)**

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

* Server runs by default on `http://0.0.0.0:8000`
* `--reload` automatically reloads the server on code changes (for development)

---

## API Endpoints

* **POST `/api/process-and-upload`**
  Process an image: remove background, resize, generate embedding, upload to S3.
  **Returns:** Image URL and embedding vector.

* **POST `/api/search-by-image`**
  Search for similar images using an uploaded image.
  **Parameters:** `limit` (number of results), `threshold` (similarity threshold)
  **Returns:** List of matching records.

* **GET `/health`**
  Health check endpoint.

---

## Reporting Bugs

Bug reports help improve PastePick:

* Open an issue on GitHub: [New Issue](https://github.com/IngrdInsight/PastePick-py-server/issues/new)

---

## Contributing

We welcome contributions!

1. Fork the repository
2. Create a new branch for your feature or bugfix
3. Make your changes
4. Submit a pull request
