"""LangGraph Workflow - StateGraph for orchestrating AI agents"""

import logging
from typing import Dict, Any, TypedDict
from datetime import datetime

logger = logging.getLogger(__name__)

try:
    from langgraph.graph import StateGraph
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False


class WorkflowState(TypedDict):
    """State definition for the workflow"""
    task_type: str
    input_data: str
    topic: str
    result: Dict[str, Any]
    error: str
    timestamp: str


class AIOperationsWorkflow:
    """LangGraph-based workflow for AI Operations"""
    
    def __init__(self):
        """Initialize the workflow"""
        self.graph = None
        if LANGGRAPH_AVAILABLE:
            self._setup_langgraph()
        logger.info("AI Operations Workflow initialized")
    
    def _setup_langgraph(self):
        """Setup LangGraph StateGraph"""
        try:
            workflow = StateGraph(WorkflowState)
            
            # Define nodes
            workflow.add_node("input_validation", self.validate_input)
            workflow.add_node("task_routing", self.route_task)
            workflow.add_node("meeting_agent", self.run_meeting_agent)
            workflow.add_node("analysis_agent", self.run_analysis_agent)
            workflow.add_node("document_agent", self.run_document_agent)
            workflow.add_node("output_generation", self.generate_output)
            
            # Define edges
            workflow.add_edge("input_validation", "task_routing")
            
            workflow.add_conditional_edges(
                "task_routing",
                self.determine_task,
                {
                    "meeting": "meeting_agent",
                    "analysis": "analysis_agent",
                    "document": "document_agent",
                }
            )
            
            workflow.add_edge("meeting_agent", "output_generation")
            workflow.add_edge("analysis_agent", "output_generation")
            workflow.add_edge("document_agent", "output_generation")
            
            self.graph = workflow.compile()
            logger.info("LangGraph workflow compiled successfully")
            
        except Exception as e:
            logger.error(f"Failed to setup LangGraph: {str(e)}")
            self.graph = None
    
    def validate_input(self, state: WorkflowState) -> WorkflowState:
        """Validate input parameters"""
        logger.info(f"Validating input for task: {state['task_type']}")
        
        if not state['task_type']:
            state['error'] = "Task type is required"
        elif state['task_type'] == 'document' and not state['topic']:
            state['error'] = "Topic is required for document generation"
        elif state['task_type'] in ['meeting', 'analysis'] and not state['input_data']:
            state['error'] = f"Input file is required for {state['task_type']} task"
        
        state['timestamp'] = datetime.now().isoformat()
        return state
    
    def determine_task(self, state: WorkflowState) -> str:
        """Determine which agent to route to"""
        return state['task_type']
    
    def route_task(self, state: WorkflowState) -> WorkflowState:
        """Route task to appropriate handler"""
        logger.info(f"Routing task: {state['task_type']}")
        return state
    
    def run_meeting_agent(self, state: WorkflowState) -> WorkflowState:
        """Run meeting summarizer agent"""
        try:
            from meeting_summarizer import MeetingSummarizer
            agent = MeetingSummarizer()
            result = agent.run(state['input_data'])
            state['result'] = result
        except Exception as e:
            state['error'] = str(e)
        return state
    
    def run_analysis_agent(self, state: WorkflowState) -> WorkflowState:
        """Run data analyzer agent"""
        try:
            from data_analyzer import DataAnalyzer
            agent = DataAnalyzer()
            result = agent.run(state['input_data'])
            state['result'] = result
        except Exception as e:
            state['error'] = str(e)
        return state
    
    def run_document_agent(self, state: WorkflowState) -> WorkflowState:
        """Run document generator agent"""
        try:
            from document_generator import DocumentGenerator
            agent = DocumentGenerator()
            result = agent.run(state['topic'])
            state['result'] = result
        except Exception as e:
            state['error'] = str(e)
        return state
    
    def generate_output(self, state: WorkflowState) -> WorkflowState:
        """Generate final output"""
        logger.info("Generating workflow output")
        
        if state.get('error'):
            logger.error(f"Workflow failed: {state['error']}")
        else:
            logger.info("Workflow completed successfully")
        
        return state
    
    def execute(self, task_type: str, input_data: str = None, topic: str = None) -> Dict[str, Any]:
        """Execute the workflow"""
        initial_state: WorkflowState = {
            'task_type': task_type,
            'input_data': input_data or "",
            'topic': topic or "",
            'result': {},
            'error': "",
            'timestamp': ""
        }
        
        if self.graph:
            try:
                final_state = self.graph.invoke(initial_state)
                return final_state
            except Exception as e:
                logger.error(f"Workflow execution failed: {str(e)}")
                return {'error': str(e), 'task_type': task_type}
        else:
            logger.info("Using fallback workflow execution")
            return self._fallback_execute(task_type, input_data, topic)
    
    def _fallback_execute(self, task_type: str, input_data: str = None, topic: str = None) -> Dict[str, Any]:
        """Fallback execution without LangGraph"""
        try:
            if task_type == 'meeting':
                from meeting_summarizer import MeetingSummarizer
                agent = MeetingSummarizer()
                return agent.run(input_data)
            elif task_type == 'analysis':
                from data_analyzer import DataAnalyzer
                agent = DataAnalyzer()
                return agent.run(input_data)
            elif task_type == 'document':
                from document_generator import DocumentGenerator
                agent = DocumentGenerator()
                return agent.run(topic)
            else:
                return {'error': f'Unknown task type: {task_type}'}
        except Exception as e:
            return {'error': str(e)}
