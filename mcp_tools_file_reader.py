"""File Reader Tool - Read text and CSV files"""

import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)


def read_file(file_path: str, encoding: str = 'utf-8') -> Dict[str, Any]:
    """Read text or CSV files from disk"""
    try:
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        content = path.read_text(encoding=encoding)
        
        result = {
            'status': 'success',
            'file_path': str(path.absolute()),
            'content': content,
            'file_size_bytes': path.stat().st_size,
            'lines': len(content.split('\n'))
        }
        
        logger.info(f"Successfully read file: {file_path}")
        return result
        
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {str(e)}")
        return {
            'status': 'error',
            'error': str(e),
            'file_path': file_path
        }


def read_csv(file_path: str) -> Dict[str, Any]:
    """Read CSV file and return rows"""
    try:
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        content = path.read_text(encoding='utf-8')
        lines = content.strip().split('\n')
        
        if not lines:
            raise ValueError("CSV file is empty")
        
        header = lines[0].split(',')
        rows = []
        for line in lines[1:]:
            values = line.split(',')
            row = dict(zip(header, values))
            rows.append(row)
        
        result = {
            'status': 'success',
            'file_path': str(path.absolute()),
            'headers': header,
            'row_count': len(rows),
            'rows': rows
        }
        
        logger.info(f"Successfully read CSV file: {file_path} ({len(rows)} rows)")
        return result
        
    except Exception as e:
        logger.error(f"Error reading CSV file {file_path}: {str(e)}")
        return {
            'status': 'error',
            'error': str(e),
            'file_path': file_path
        }
