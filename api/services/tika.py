import requests
from typing import Tuple, Dict, Any
from fastapi import HTTPException

from core.config import get_settings

settings = get_settings()


class TikaService:
    def __init__(self):
        self.tika_url = settings.TIKA_URL

    async def process_file(self, file_content: bytes, content_type: str) -> Tuple[str, Dict[str, Any]]:
        """Process file content with Apache Tika"""
        try:
            # Extract text content
            content_response = requests.put(
                f"{self.tika_url}/tika",
                data=file_content,
                headers={
                    'Accept': 'text/plain; charset=UTF-8',
                    'Content-Type': content_type
                }
            )
            content_response.raise_for_status()
            content = content_response.text


            # Extract metadata
            metadata_response = requests.put(
                f"{self.tika_url}/meta",
                data=file_content,
                headers={'Accept': 'application/json'}
            )
            metadata_response.raise_for_status()
            metadata = metadata_response.json()

            return content, metadata
        except requests.RequestException as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error processing file with Tika: {str(e)}"
            )
