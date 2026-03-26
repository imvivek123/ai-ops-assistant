#!/usr/bin/env python3
"""Quick validation - Test core imports and functionality"""

import sys
from pathlib import Path


def validate_imports():
    """Check if core modules can be imported"""
    print("\n" + "="*60)
    print("VALIDATING CORE IMPORTS")
    print("="*60)
    
    modules = [
        ("Orchestrator", "orchestrator", "Orchestrator"),
        ("Meeting Summarizer", "meeting_summarizer", "MeetingSummarizer"),
        ("Data Analyzer", "data_analyzer", "DataAnalyzer"),
        ("Document Generator", "document_generator", "DocumentGenerator"),
        ("Workflow", "workflow", "AIOperationsWorkflow"),
        ("MCP Server", "mcp_server", "MCPServer"),
    ]
    
    passed = 0
    failed = 0
    
    for display_name, module_name, class_name in modules:
        try:
            module = __import__(module_name)
            obj = getattr(module, class_name)
            print(f"✓ {display_name}")
            passed += 1
        except Exception as e:
            print(f"✗ {display_name}: {type(e).__name__}")
            failed += 1
    
    return passed, failed


def validate_syntax():
    """Check Python syntax of all modules"""
    print("\n" + "="*60)
    print("VALIDATING PYTHON SYNTAX")
    print("="*60)
    
    import py_compile
    
    python_files = list(Path(".").glob("*.py"))
    passed = 0
    failed = 0
    
    for file_path in python_files:
        try:
            py_compile.compile(str(file_path), doraise=True)
            print(f"✓ {file_path.name}")
            passed += 1
        except py_compile.PyCompileError:
            print(f"✗ {file_path.name}")
            failed += 1
    
    return passed, failed


def main():
    """Run all validations"""
    print("\n" + "="*60)
    print("AI-OPERATIONS-ASSISTANT VALIDATION")
    print("="*60)
    
    results = []
    
    p, f = validate_syntax()
    results.append(("Python Syntax", p, f))
    
    p, f = validate_imports()
    results.append(("Module Imports", p, f))
    
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)
    
    total_passed = 0
    total_failed = 0
    
    for section, passed, failed in results:
        total_passed += passed
        total_failed += failed
        total = passed + failed
        status = "✓" if failed == 0 else "✗"
        print(f"{status} {section}: {passed}/{total} passed")
    
    print("-" * 60)
    print(f"TOTAL: {total_passed}/{total_passed + total_failed} checks passed")
    
    if total_failed == 0:
        print("\n✓ ALL VALIDATIONS PASSED!")
        return 0
    else:
        print(f"\n✗ {total_failed} validations failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
