#!/usr/bin/env python3
"""
AI Operations Assistant - Main CLI Entry Point
Multi-agent system for automating internal business operations
"""

import argparse
import logging
import sys
import json
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_environment():
    """Setup environment and create necessary directories"""
    Path("outputs").mkdir(exist_ok=True)
    Path("sample_data").mkdir(exist_ok=True)
    logger.info("Environment setup complete")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='AI Operations Assistant - Automate business operations'
    )
    parser.add_argument(
        '--task',
        choices=['meeting', 'analyze', 'document'],
        required=True,
        help='Type of task to execute'
    )
    parser.add_argument(
        '--input',
        type=str,
        help='Input file path'
    )
    parser.add_argument(
        '--topic',
        type=str,
        help='Topic for document generation'
    )
    parser.add_argument(
        '--use-workflow',
        action='store_true',
        help='Use LangGraph workflow (if available)'
    )
    
    args = parser.parse_args()
    
    setup_environment()
    
    logger.info(f"Starting AI-Ops-Assistant")
    logger.info(f"Task: {args.task}")
    if args.input:
        logger.info(f"Input: {args.input}")
    if args.topic:
        logger.info(f"Topic: {args.topic}")
    
    try:
        if args.use_workflow:
            # Use LangGraph workflow
            from workflow import AIOperationsWorkflow
            workflow = AIOperationsWorkflow()
            result = workflow.execute(args.task, args.input, args.topic)
        else:
            # Use direct agent execution
            from orchestrator import Orchestrator
            orchestrator = Orchestrator()
            result = orchestrator.route_task(args.task, args.input, args.topic)
        
        # Display results
        if result.get('status') == 'success':
            logger.info(f"✓ Task completed successfully")
            logger.info(f"  Duration: {result.get('duration', 'N/A'):.2f}s")
            logger.info(f"  Output: {result.get('output_file', 'outputs/')}")
            return 0
        else:
            logger.error(f"✗ Task failed: {result.get('error', 'Unknown error')}")
            return 1
            
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
