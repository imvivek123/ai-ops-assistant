"""Document Generator Agent - Generates professional business documents"""

import logging
import time
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class DocumentGenerator:
    """Agent for generating professional business documents"""
    
    MAX_RETRIES = 3
    RETRY_DELAY = 1
    
    def __init__(self):
        """Initialize the document generator"""
        self.outputs_dir = Path("outputs")
        self.outputs_dir.mkdir(exist_ok=True)
        logger.info("Document Generator initialized")
    
    def run(self, topic: str) -> Dict[str, Any]:
        """Run the document generator with retry logic"""
        start_time = time.time()
        
        for attempt in range(self.MAX_RETRIES):
            try:
                logger.info(f"Document generator attempt {attempt + 1}/{self.MAX_RETRIES}")
                
                # Generate document content
                document = self._generate_document(topic)
                
                # Save the output
                output_file = self._save_document(document, topic)
                
                duration = time.time() - start_time
                logger.info(f"Document generated successfully in {duration:.2f}s")
                
                return {
                    "status": "success",
                    "output_file": str(output_file),
                    "duration": duration,
                    "document": document
                }
                
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < self.MAX_RETRIES - 1:
                    time.sleep(self.RETRY_DELAY * (attempt + 1))
                else:
                    logger.error(f"All {self.MAX_RETRIES} attempts failed")
                    return {"status": "error", "error": str(e)}
    
    def _generate_document(self, topic: str) -> Dict[str, Any]:
        """Generate document structure and content"""
        document = {
            'title': topic,
            'sections': self._create_sections(topic),
            'generated_at': datetime.now().isoformat()
        }
        return document
    
    def _create_sections(self, topic: str) -> list:
        """Create document sections based on topic"""
        sections = [
            {
                'name': 'Executive Summary',
                'content': self._generate_executive_summary(topic)
            },
            {
                'name': 'Key Findings',
                'content': self._generate_key_findings(topic)
            },
            {
                'name': 'Analysis & Recommendations',
                'content': self._generate_analysis(topic)
            },
            {
                'name': 'Implementation Plan',
                'content': self._generate_implementation(topic)
            },
            {
                'name': 'Conclusion',
                'content': self._generate_conclusion(topic)
            }
        ]
        return sections
    
    def _generate_executive_summary(self, topic: str) -> str:
        return f"This report provides comprehensive analysis of {topic}.\n\nKey highlights: strategic assessment, metrics analysis, risk mitigation, and recommendations."
    
    def _generate_key_findings(self, topic: str) -> str:
        return f"Analysis of {topic} reveals: strong performance metrics, competitive positioning, optimized resources, manageable risks, and growth opportunities."
    
    def _generate_analysis(self, topic: str) -> str:
        return f"{topic} shows positive trajectory with challenges and opportunities. Strategic gaps identified with clear mitigation paths."
    
    def _generate_implementation(self, topic: str) -> str:
        return "Phased implementation: Foundation (M1-2), Execution (M3-4), Acceleration (M5-6), Sustainability (M6+)."
    
    def _generate_conclusion(self, topic: str) -> str:
        return f"Clear roadmap for {topic} with commitment to execution and stakeholder alignment."
    
    def _save_document(self, document: Dict[str, Any], topic: str) -> Path:
        """Save document to markdown file"""
        filename = topic.lower().replace(' ', '_').replace('/', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.outputs_dir / f"document_{filename}_{timestamp}.md"
        
        content = self._format_document(document)
        output_file.write_text(content, encoding='utf-8')
        logger.info(f"Document saved to {output_file}")
        
        return output_file
    
    def _format_document(self, document: Dict[str, Any]) -> str:
        """Format document as markdown"""
        md = f"# {document['title']}\n\n"
        md += f"**Generated:** {datetime.now().strftime('%B %d, %Y')}\n\n---\n\n"
        
        for section in document['sections']:
            md += f"## {section['name']}\n\n{section['content']}\n\n---\n\n"
        
        md += "## Document Information\n\n"
        md += f"- **Title:** {document['title']}\n"
        md += f"- **Generated:** {document['generated_at']}\n"
        md += f"- **Status:** Final\n"
        
        return md
