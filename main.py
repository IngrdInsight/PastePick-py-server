from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import logging

from services.allas_uploader import S3Uploader
from services.database import Database
from services.embedder import ImageEmbedder
from services.image_processor import ImageProcessor


app = FastAPI(title="Image Processing Service", version="1.0.0")
image_processor = ImageProcessor()
embedder = ImageEmbedder()
s3_uploader = S3Uploader()
database = Database()

# Configure CORS and logging
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.post("/api/process-and-upload")
async def process_and_upload(file: UploadFile = File(...)):
    """
    Process image: remove background, resize, embed, upload to S3
    Returns: URL and embedding vector
    """
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")

        # Read file
        image_bytes = await file.read()
        logger.info(f"Processing image: {file.filename}")

        # Process image, generate embedding and upload
        processed_bytes = image_processor.process_image(image_bytes)
        logger.info("Image processed successfully")

        embedding = embedder.embed_image(processed_bytes)
        logger.info(f"Embedding generated (dimension: {len(embedding)})")
        logger.info(f"Type of processed_bytes before upload: {type(processed_bytes)}")
        upload_url = s3_uploader.upload_image(processed_bytes, file.filename)
        logger.info(f"Image uploaded: {upload_url}")

        return JSONResponse(content={
            "success": True,
            "url": upload_url,
            "embedding": embedding,
        })

    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/search-by-image")
async def search_by_image(
        file: UploadFile = File(...),
        limit: int = 1,
        threshold: float = 0.7
):
    """
    Search for similar images in database
    Returns: List of matching toothpaste records
    """
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")

        # Read file
        image_bytes = await file.read()
        logger.info(f"Searching with image: {file.filename}")

        # Process image, generate embedding and search
        processed_bytes = image_processor.process_image(image_bytes)
        logger.info("Image processed successfully")

        embedding = embedder.embed_image(processed_bytes)
        logger.info(f"Embedding generated (dimension: {len(embedding)})")

        results = await database.search_by_embedding(embedding, limit, threshold)
        logger.info(f"Found {len(results)} matching records")

        return JSONResponse(content={
            "success": True,
            "results": results
        })

    except Exception as e:
        logger.error(f"Error searching image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check"""
    return {"status": "healthy", "service": "image-processing"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
