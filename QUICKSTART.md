# Quick Start Guide for AI-Ops-Assistant

## ⚡ 5-Minute Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Create Environment Config
```bash
cp .env.example .env
```

### Step 3: Generate Sample Data
```bash
python setup_samples.py
```

This creates:
- `sample_data/meeting_transcript.txt` (Q1 2024 business review)
- `sample_data/sales_data.csv` (20 rows of sales data)
- `sample_data/doc_request.txt` (document generation request)

## 🚀 Running Examples

### Meeting Summarization
```bash
python main.py --task meeting --input sample_data/meeting_transcript.txt
```

Expected output:
- Extracts 5 attendees
- Identifies 5+ key decisions
- Lists 3+ action items with deadlines
- Captures metrics ($4.2M revenue, 32% growth)
- Saves to `outputs/meeting_summary_*.md`

### Data Analysis
```bash
python main.py --task analyze --input sample_data/sales_data.csv
```

Expected output:
- Shows 20 rows x 9 columns
- Summary statistics (mean, median, std dev)
- Top performers in revenue
- Detects outliers if any
- Saves to `outputs/data_analysis_*.md`

### Document Generation
```bash
python main.py --task document --topic "Q1 Performance Report"
```

Expected output:
- 5-section professional document
- Executive Summary, Key Findings, Analysis, Implementation, Conclusion
- Saves to `outputs/document_q1_performance_report_*.md`

## 🧪 Full System Test

Run the comprehensive test suite:
```bash
python test_system.py
```

This tests:
1. Sample data creation
2. Meeting Summarizer
3. Data Analyzer
4. Document Generator
5. Orchestrator routing
6. CLI interface

## 📊 Exploring Generated Reports

After running any task, check the `outputs/` folder:

```bash
# List all generated reports
ls outputs/

# View a meeting summary
cat outputs/meeting_summary_*.md

# View analysis report
cat outputs/data_analysis_*.md

# View generated document
cat outputs/document_*.md
```

## 🔄 Advanced Usage

### Use LangGraph Workflow (if available)
```bash
python main.py --task meeting --input sample_data/meeting_transcript.txt --use-workflow
```

### Chain Tasks
```bash
# Create a meeting summary, then generate a document about it
python main.py --task meeting --input sample_data/meeting_transcript.txt
python main.py --task document --topic "Q1 Meeting Summary Report"
```

### Enable Detailed Logging
Edit `main.py` and change:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 🐛 Troubleshooting

### ImportError: No module named 'X'
```bash
pip install --upgrade -r requirements.txt
```

### FileNotFoundError: sample_data not found
```bash
python setup_samples.py
```

### Permission denied writing to outputs/
```bash
chmod 755 outputs/
```

### OPENAI_API_KEY not set
- Document generation works without it
- Meeting summarization and analysis work standalone
- LLM-enhanced features require the key in `.env`

## ✅ Verification Checklist

- [ ] All dependencies installed
- [ ] `.env` file created from `.env.example`
- [ ] Sample data created (`ls sample_data/`)
- [ ] All three main tasks run successfully
- [ ] Output files generated in `outputs/`
- [ ] Test suite passes (`python test_system.py`)

## 📚 Next Steps

1. **Customize Agents**: Edit agent files to adjust extraction logic
2. **Add New Agents**: Follow the same pattern for new task types
3. **Integrate Tools**: Add MCP tools in `mcp_tools_*.py`
4. **Production Deployment**: Use the workflow.py with LangGraph

---

**Ready?** Start with: `python setup_samples.py` then `python test_system.py`
