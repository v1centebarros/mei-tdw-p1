import io

import requests
from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter
from typing import Tuple, Dict, Any
from fastapi import HTTPException


class DocumentService:
    def __init__(self):
        self.converter = DocumentConverter(
            allowed_formats=[
                InputFormat.PDF,
                InputFormat.IMAGE,
                InputFormat.DOCX,
                InputFormat.HTML,
                InputFormat.PPTX,
                InputFormat.ASCIIDOC,
                InputFormat.MD,
            ]
        )

    async def process_file(self, source: str) -> Tuple[str, Dict[str, Any]]:
        """Process file content with Docling"""
        try:

            # Convert document
            result = self.converter.convert(source)

            # Get markdown content and metadata
            markdown_content = result.document.export_to_markdown()
            # metadata = result.document.metadata

            return markdown_content, dict()
        except Exception as e:
            request = requests.get(source)
            if request.status_code != 200 or request.headers.get("Content-Type", None) != "text/plain":
                raise HTTPException(
                    status_code=500,
                    detail=f"Error processing file with Docling: {str(e)}"
                )

            file_content = request.content.decode()
            return file_content, dict()
