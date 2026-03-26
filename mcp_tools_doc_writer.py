"""Document Writer Tool - Write markdown documents to outputs/"""

import logging
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


def write_document(
    filename: str,
    content: str,
    output_dir: str = "outputs"
) -> Dict[str, Any]:
    """Write markdown document to outputs/ folder"""
    try:
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        if not filename.endswith('.md'):
            filename = f"{filename}.md"
        
        file_path = output_path / filename
        file_path.write_text(content, encoding='utf-8')
        
        result = {
            'status': 'success',
            'file_path': str(file_path.absolute()),
            'file_size_bytes': len(content.encode('utf-8')),
            'written_at': datetime.now().isoformat()
        }
        
        logger.info(f"Successfully wrote document: {file_path}")
        return result
        
    except Exception as e:
        logger.error(f"Error writing document {filename}: {str(e)}")
        return {
            'status': 'error',
            'error': str(e),
            'filename': filename
        }


def append_to_document(
    filename: str,
    content: str,
    output_dir: str = "outputs"
) -> Dict[str, Any]:
    """Append content to an existing document"""
    try:
        output_path = Path(output_dir)
        
        if not filename.endswith('.md'):
            filename = f"{filename}.md"
        
        file_path = output_path / filename
        
        existing_content = ""
        if file_path.exists():
            existing_content = file_path.read_text(encoding='utf-8')
        
        new_content = existing_content + "\n\n" + content
        file_path.write_text(new_content, encoding='utf-8')
        
        result = {
            'status': 'success',
            'file_path': str(file_path.absolute()),
            'file_size_bytes': len(new_content.encode('utf-8')),
            'appended_at': datetime.now().isoformat()
        }
        
        logger.info(f"Successfully appended to document: {file_path}")
        return result
        
    except Exception as e:
        logger.error(f"Error appending to document {filename}: {str(e)}")
        return {
            'status': 'error',
            'error': str(e),
            'filename': filename
        }
