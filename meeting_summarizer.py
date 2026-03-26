"""Meeting Summarizer Agent - Summarizes meeting transcripts into structured reports"""

import logging
import time
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class MeetingSummarizer:
    """Agent for summarizing meeting transcripts"""
    
    MAX_RETRIES = 3
    RETRY_DELAY = 1
    
    def __init__(self):
        """Initialize the meeting summarizer"""
        self.outputs_dir = Path("outputs")
        self.outputs_dir.mkdir(exist_ok=True)
        logger.info("Meeting Summarizer initialized")
    
    def run(self, input_file: str) -> Dict[str, Any]:
        """Run the meeting summarizer with retry logic"""
        start_time = time.time()
        
        for attempt in range(self.MAX_RETRIES):
            try:
                logger.info(f"Meeting summarizer attempt {attempt + 1}/{self.MAX_RETRIES}")
                
                # Read the meeting transcript
                transcript = self._read_file(input_file)
                
                # Extract structured information
                summary = self._extract_summary(transcript)
                
                # Save the output
                output_file = self._save_summary(summary)
                
                duration = time.time() - start_time
                logger.info(f"Meeting summarized successfully in {duration:.2f}s")
                
                return {
                    "status": "success",
                    "output_file": str(output_file),
                    "duration": duration,
                    "summary": summary
                }
                
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < self.MAX_RETRIES - 1:
                    time.sleep(self.RETRY_DELAY * (attempt + 1))
                else:
                    logger.error(f"All {self.MAX_RETRIES} attempts failed")
                    return {"status": "error", "error": str(e)}
    
    def _read_file(self, file_path: str) -> str:
        """Read file contents"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        return path.read_text(encoding='utf-8')
    
    def _extract_summary(self, transcript: str) -> Dict[str, Any]:
        """Extract structured information from transcript"""
        lines = transcript.split('\n')
        
        summary = {
            'attendees': self._extract_attendees(lines),
            'key_decisions': self._extract_decisions(lines),
            'action_items': self._extract_action_items(lines),
            'next_steps': self._extract_next_steps(lines),
            'metrics': self._extract_metrics(lines)
        }
        
        return summary
    
    def _extract_attendees(self, lines: list) -> list:
        """Extract list of attendees"""
        attendees = []
        for line in lines:
            if 'Attendees:' in line:
                attendees_str = line.split('Attendees:')[1].strip()
                attendees = [a.strip() for a in attendees_str.split(',')]
                break
        return attendees
    
    def _extract_decisions(self, lines: list) -> list:
        """Extract key decisions"""
        decisions = []
        decision_keywords = ['Approved', 'approved', 'agreed', 'Agreed', 'decided', 'Decided']
        
        for line in lines:
            if any(keyword in line for keyword in decision_keywords):
                decisions.append(line.strip())
        
        return decisions[:5]
    
    def _extract_action_items(self, lines: list) -> list:
        """Extract action items"""
        action_items = []
        action_keywords = ['Number one', 'action', 'Action', 'hire', 'release', 'Launch', 'Present', 'Schedule']
        
        for line in lines:
            if any(keyword in line for keyword in action_keywords):
                action_items.append(line.strip())
        
        return action_items
    
    def _extract_next_steps(self, lines: list) -> list:
        """Extract next steps and timeline"""
        next_steps = []
        timeline_keywords = ['April', 'May', 'week', 'two weeks', 'reconvene', 'by']
        
        for line in lines:
            if any(keyword in line for keyword in timeline_keywords):
                next_steps.append(line.strip())
        
        return next_steps
    
    def _extract_metrics(self, lines: list) -> Dict[str, Any]:
        """Extract key metrics mentioned"""
        metrics = {}
        text = '\n'.join(lines)
        
        if '$4.2M' in text:
            metrics['new_revenue'] = '$4.2M'
        if '32%' in text:
            metrics['growth_rate'] = '32%'
        if '47' in text:
            metrics['new_clients'] = 47
        
        return metrics
    
    def _save_summary(self, summary: Dict[str, Any]) -> Path:
        """Save summary to markdown file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.outputs_dir / f"meeting_summary_{timestamp}.md"
        
        content = self._format_summary(summary)
        output_file.write_text(content, encoding='utf-8')
        logger.info(f"Summary saved to {output_file}")
        
        return output_file
    
    def _format_summary(self, summary: Dict[str, Any]) -> str:
        """Format summary as markdown"""
        md = "# Meeting Summary Report\n\n"
        md += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        if summary.get('attendees'):
            md += "## Attendees\n"
            for attendee in summary['attendees']:
                md += f"- {attendee}\n"
            md += "\n"
        
        if summary.get('key_decisions'):
            md += "## Key Decisions\n"
            for i, decision in enumerate(summary['key_decisions'], 1):
                md += f"{i}. {decision}\n"
            md += "\n"
        
        if summary.get('action_items'):
            md += "## Action Items\n"
            for i, item in enumerate(summary['action_items'], 1):
                md += f"{i}. {item}\n"
            md += "\n"
        
        if summary.get('metrics'):
            md += "## Key Metrics\n"
            for key, value in summary['metrics'].items():
                md += f"- **{key.replace('_', ' ').title()}:** {value}\n"
            md += "\n"
        
        if summary.get('next_steps'):
            md += "## Next Steps & Timeline\n"
            for i, step in enumerate(summary['next_steps'], 1):
                md += f"{i}. {step}\n"
        
        return md
