import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
from io import BytesIO
from typing import List


class ImageEmbedder:
    """Generate image embeddings using CLIP"""

    def __init__(self, model_name: str = "openai/clip-vit-base-patch32"):
        torch.set_num_threads(2);
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = CLIPModel.from_pretrained(model_name).to(self.device)
        self.processor = CLIPProcessor.from_pretrained(model_name)
        self.model.eval()


    def embed_image(self, image_bytes: bytes) -> List[float]:
        """Generate embedding for an image"""
        image = Image.open(BytesIO(image_bytes))

        with torch.no_grad():
            inputs = self.processor(images=image, return_tensors="pt").to(self.device)
            image_features = self.model.get_image_features(**inputs)

            # Normalize embeddings
            image_features = image_features / image_features.norm(dim=-1, keepdim=True)

            return image_features.cpu().numpy()[0].tolist()

