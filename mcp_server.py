"""MCP Server - Tool protocol server for AI Operations Assistant"""

import logging
from typing import Any, Dict, Callable
from pathlib import Path

logger = logging.getLogger(__name__)


class MCPServer:
    """MCP Protocol Server for tool registration and execution"""
    
    def __init__(self):
        """Initialize MCP server"""
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.outputs_dir = Path("outputs")
        self.outputs_dir.mkdir(exist_ok=True)
        logger.info(f"MCP Server initialized. Output dir: {self.outputs_dir}")
    
    def register_tool(self, name: str, tool_func: Callable, description: str) -> None:
        """Register a tool with the server"""
        self.tools[name] = {
            'func': tool_func,
            'description': description
        }
        logger.info(f"Tool registered: {name}")
    
    def execute_tool(self, tool_name: str, **kwargs) -> Any:
        """Execute a registered tool"""
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found")
        
        try:
            result = self.tools[tool_name]['func'](**kwargs)
            logger.info(f"Tool executed successfully: {tool_name}")
            return result
        except Exception as e:
            logger.error(f"Tool execution failed for {tool_name}: {str(e)}")
            raise
    
    def list_tools(self) -> Dict[str, str]:
        """List all registered tools"""
        return {name: info['description'] for name, info in self.tools.items()}
    
    def initialize_tools(self) -> None:
        """Initialize all standard tools"""
        try:
            from mcp_tools_file_reader import read_file
            from mcp_tools_doc_writer import write_document
            from mcp_tools_analyzer import analyze_dataframe
            
            self.register_tool(
                'file_reader',
                read_file,
                'Read text or CSV files from disk'
            )
            
            self.register_tool(
                'doc_writer',
                write_document,
                'Write markdown documents to outputs/ folder'
            )
            
            self.register_tool(
                'analyzer',
                analyze_dataframe,
                'Analyze pandas DataFrames and extract insights'
            )
            
            logger.info(f"Initialized {len(self.tools)} tools")
        except ImportError as e:
            logger.warning(f"Could not initialize all tools: {str(e)}")
            logger.warning("Some tools may not be available")
