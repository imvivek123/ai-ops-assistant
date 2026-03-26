"""Orchestrator Agent - Routes tasks to appropriate agents"""

import logging
import time
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class Orchestrator:
    """Orchestrator that auto-detects task type and routes to appropriate agent"""
    
    def __init__(self):
        """Initialize the orchestrator"""
        self.outputs_dir = Path("outputs")
        self.outputs_dir.mkdir(exist_ok=True)
        logger.info("Orchestrator initialized")
        self.meeting_summarizer = None
        self.data_analyzer = None
        self.document_generator = None
    
    def detect_task_type(self, input_data: str, task_hint: str = None) -> str:
        """Auto-detect task type from input"""
        if task_hint:
            return task_hint
        
        if input_data.endswith('.csv'):
            return 'analyze'
        elif input_data.endswith('.txt'):
            try:
                content = Path(input_data).read_text(encoding='utf-8')
                if any(word in content.lower() for word in ['meeting', 'attendees', 'agenda', 'discussed']):
                    return 'meeting'
            except:
                pass
            return 'unknown'
        
        return 'unknown'
    
    def execute_task(self, task_type: str, input_data: str = None, topic: str = None) -> Dict[str, Any]:
        """Execute task based on detected type"""
        logger.info(f"Orchestrator executing task: {task_type}")
        start_time = time.time()
        
        try:
            if task_type == 'meeting':
                if not self.meeting_summarizer:
                    from meeting_summarizer import MeetingSummarizer
                    self.meeting_summarizer = MeetingSummarizer()
                result = self.meeting_summarizer.run(input_data)
            elif task_type == 'analyze':
                if not self.data_analyzer:
                    from data_analyzer import DataAnalyzer
                    self.data_analyzer = DataAnalyzer()
                result = self.data_analyzer.run(input_data)
            elif task_type == 'document':
                if not self.document_generator:
                    from document_generator import DocumentGenerator
                    self.document_generator = DocumentGenerator()
                result = self.document_generator.run(topic)
            else:
                raise ValueError(f"Unknown task type: {task_type}")
            
            result['orchestrator_duration'] = time.time() - start_time
            result['task_type'] = task_type
            result['executed_at'] = datetime.now().isoformat()
            
            return result
            
        except Exception as e:
            logger.error(f"Task execution failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "task_type": task_type,
                "executed_at": datetime.now().isoformat()
            }
    
    def route_task(self, task_type: str, input_data: str = None, topic: str = None) -> Dict[str, Any]:
        """Route task to appropriate agent with error handling"""
        logger.info(f"Routing task: {task_type}")
        
        if task_type not in ['meeting', 'analyze', 'document']:
            logger.error(f"Unknown task type: {task_type}")
            raise ValueError(f"Unknown task type: {task_type}. Must be 'meeting', 'analyze', or 'document'")
        
        return self.execute_task(task_type, input_data, topic)
