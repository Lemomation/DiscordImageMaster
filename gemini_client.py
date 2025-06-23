import asyncio
import logging
import os
from typing import Optional

from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

class GeminiImageGenerator:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.0-flash-preview-image-generation"
        
    async def generate_image_async(self, prompt: str) -> Optional[bytes]:
        """
        Generate an image asynchronously using Gemini 2.0 Flash Preview.
        
        Args:
            prompt: Text description for image generation
            
        Returns:
            Image data as bytes or None if generation failed
        """
        try:
            # Run the synchronous API call in a thread pool
            loop = asyncio.get_event_loop()
            image_data = await loop.run_in_executor(None, self._generate_image_sync, prompt)
            return image_data
            
        except Exception as e:
            logger.error(f"Async image generation failed: {e}")
            return None
    
    def _generate_image_sync(self, prompt: str) -> Optional[bytes]:
        """
        Synchronous image generation method.
        
        Args:
            prompt: Text description for image generation
            
        Returns:
            Image data as bytes or None if generation failed
        """
        try:
            logger.info(f"Generating image with prompt: {prompt[:100]}...")
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=['TEXT', 'IMAGE']
                )
            )
            
            if not response.candidates:
                logger.error("No candidates in response")
                return None
                
            content = response.candidates[0].content
            if not content or not content.parts:
                logger.error("No content or parts in response")
                return None
            
            # Look for image data in response parts
            for part in content.parts:
                if part.text:
                    logger.info(f"Response text: {part.text}")
                elif part.inline_data and part.inline_data.data:
                    logger.info("Found image data in response")
                    return part.inline_data.data
            
            logger.error("No image data found in response")
            return None
            
        except Exception as e:
            logger.error(f"Image generation failed: {e}")
            return None
    
    def generate_image(self, prompt: str, image_path: str) -> bool:
        """
        Generate an image and save it to a file.
        
        Args:
            prompt: Text description for image generation
            image_path: Path to save the generated image
            
        Returns:
            True if successful, False otherwise
        """
        try:
            image_data = self._generate_image_sync(prompt)
            if image_data:
                with open(image_path, 'wb') as f:
                    f.write(image_data)
                logger.info(f"Image saved to {image_path}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Failed to save image: {e}")
            return False
