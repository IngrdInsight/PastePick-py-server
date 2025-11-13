from PIL import Image
from rembg import remove
from io import BytesIO
from typing import Tuple
from config import config


class ImageProcessor:
    """Handle image background removal and formatting"""

    @staticmethod
    def remove_background(image_bytes: bytes) -> Image.Image:
        """Remove background from image"""
        input_image = Image.open(BytesIO(image_bytes))
        output_image = remove(input_image)
        return output_image

    @staticmethod
    def resize_and_format(
            image: Image.Image,
            size: Tuple[int, int] = (800, 800),
            format: str = "webp",
            quality: int = 85
    ) -> bytes:
        """Resize and convert image to specified format"""
        # Convert to RGB if image has alpha channel
        if image.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
            image = background

        # Create new image and center the resized image
        image.thumbnail(size, Image.Resampling.LANCZOS)
        final_image = Image.new('RGB', size, (255, 255, 255))
        offset = ((size[0] - image.size[0]) // 2, (size[1] - image.size[1]) // 2)
        final_image.paste(image, offset)

        # Convert to bytes
        output_buffer = BytesIO()
        final_image.save(output_buffer, format=format.upper(), quality=quality, optimize=True)
        output_buffer.seek(0)
        return output_buffer.read()

    @staticmethod
    def process_image(image_bytes: bytes) -> bytes:
        """Complete image processing pipeline"""
        # Remove background
        no_bg_image = ImageProcessor.remove_background(image_bytes)

        # Resize and format
        processed_bytes = ImageProcessor.resize_and_format(
            no_bg_image,
            size=config.TARGET_SIZE,
            format=config.IMAGE_FORMAT,
            quality=config.IMAGE_QUALITY
        )

        return processed_bytes