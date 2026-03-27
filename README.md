🤖 AI Ops Assistant

An internal operations AI assistant that automates repetitive business workflows — meeting summarization, document generation, and data analysis — using a multi-agent architecture powered by LangGraph and MCP (Model Context Protocol).


📌 Problem It Solves
Business teams waste hours every week on:

✍️ Writing meeting summaries manually
📄 Drafting repetitive internal documents
📊 Analyzing spreadsheets for insights

AI Ops Assistant automates all three — give it a file or topic, it handles the rest.

🏗️ Architecture
┌─────────────────────────────────────────────────────────────┐
│                      User Input (CLI)                        │
│         --task meeting / analyze / document                  │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   Orchestrator Agent                         │
│         Detects task type → Routes to correct agent          │
│         Handles errors → Retries up to 3 times               │
└──────────┬──────────────────┬──────────────────┬────────────┘
           │                  │                  │
           ▼                  ▼                  ▼
┌─────────────────┐  ┌────────────────┐  ┌──────────────────┐
│    Meeting      │  │   Document     │  │      Data        │
│   Summarizer    │  │   Generator    │  │    Analyzer      │
│     Agent       │  │     Agent      │  │     Agent        │
│                 │  │                │  │                  │
│ → Key decisions │  │ → Professional │  │ → Trends         │
│ → Action items  │  │   business doc │  │ → Averages       │
│ → Next steps    │  │ → Structured   │  │ → Anomalies      │
│ → Attendees     │  │   sections     │  │ → Top performers │
└────────┬────────┘  └───────┬────────┘  └────────┬─────────┘
         └───────────────────┴─────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                     MCP Server Layer                         │
│  ┌───────────────┐ ┌──────────────┐ ┌───────────────────┐  │
│  │ file_reader   │ │  doc_writer  │ │     analyzer      │  │
│  │ (txt/csv)     │ │ (markdown)   │ │  (pandas-based)   │  │
│  └───────────────┘ └──────────────┘ └───────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│               outputs/ (all generated reports)               │
└─────────────────────────────────────────────────────────────┘

🧠 Agent Responsibilities
AgentInputOutputTools UsedOrchestratorAny user requestRouted resultLangGraph StateGraphMeeting Summarizer.txt transcriptStructured summaryfile_reader, doc_writerDocument GeneratorTopic stringBusiness documentdoc_writerData Analyzer.csv fileInsights reportfile_reader, analyzer

📁 Project Structure
ai-ops-assistant/
├── agents/
│   ├── orchestrator.py        # Task detection & agent routing
│   ├── meeting_summarizer.py  # Meeting transcript processing
│   ├── document_generator.py  # Business document creation
│   └── data_analyzer.py       # CSV data analysis & insights
├── mcp_server/
│   ├── server.py              # MCP server with tool registration
│   └── tools/
│       ├── file_reader.py     # Read txt/csv files from disk
│       ├── doc_writer.py      # Write markdown reports to outputs/
│       └── analyzer.py        # Pandas-based statistical analysis
├── graph/
│   └── workflow.py            # LangGraph StateGraph wiring
├── sample_data/
│   ├── meeting_transcript.txt # Sample Q1 review meeting transcript
│   ├── sales_data.csv         # Sample sales data (20+ rows)
│   └── doc_request.txt        # Sample document request
├── outputs/                   # Auto-created — all reports saved here
├── main.py                    # CLI entry point
├── requirements.txt
└── README.md

⚡ Key Technical Features
1. Multi-Agent Orchestration with LangGraph

StateGraph manages typed state between agents
Each agent receives state, transforms it, passes forward
Conditional routing based on task type detection
Clean separation — each agent independently testable

2. MCP (Model Context Protocol) Server

Standardized tool exposure following Anthropic's open protocol
Tools decoupled from agents — swap tools without touching agent logic
Three production tools: file_reader, doc_writer, analyzer
Any MCP-compatible client can consume these tools

3. Intelligent Error Recovery

Every agent wrapped in try/except with 3 automatic retries
Failed agents return graceful error state — pipeline never crashes
Performance logging with timestamps for every operation

4. Extensible Design

Add new agent: create file in agents/, register in workflow.py
Add new tool: create file in mcp_server/tools/, register in server.py
No changes needed to existing agents or orchestrator


🚀 Quick Start
Prerequisites

Python 3.11+
pip

Installation
bash# Clone the repository
git clone https://github.com/imvivek123/ai-ops-assistant.git
cd ai-ops-assistant

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Copy environment config
cp .env.example .env
# Add your Anthropic API key in .env (optional)

💻 Usage
Meeting Summarizer
bashpython main.py --task meeting --input sample_data/meeting_transcript.txt
🎯 Orchestrator: Detected task → meeting_summarizer
📋 Meeting Summarizer: Processing transcript...
   ✓ Extracted 4 key decisions
   ✓ Identified 6 action items
   ✓ Found 5 attendees
✅ Report saved → outputs/meeting_summary_20250325_143022.md
⏱  Completed in 2.3s
Data Analyzer
bashpython main.py --task analyze --input sample_data/sales_data.csv
🎯 Orchestrator: Detected task → data_analyzer
📊 Data Analyzer: Processing 20 rows × 6 columns...
   ✓ Calculated trends across Q1-Q4
   ✓ Identified top 3 performers
   ✓ Flagged 2 anomalies
✅ Report saved → outputs/analysis_report_20250325_143156.md
⏱  Completed in 1.8s
Document Generator
bashpython main.py --task document --topic "Q1 Performance Report"
🎯 Orchestrator: Detected task → document_generator
📄 Document Generator: Creating 'Q1 Performance Report'...
   ✓ Generated executive summary
   ✓ Created 4 structured sections
   ✓ Added recommendations
✅ Report saved → outputs/Q1_Performance_Report_20250325_143301.md
⏱  Completed in 3.1s

🛠️ Tech Stack
TechnologyPurposePython 3.11+Core languageLangGraphMulti-agent workflow orchestrationMCP (Model Context Protocol)Standardized tool/agent communicationAnthropic SDKLLM-powered agent intelligencePandasData analysis and CSV processingasyncioAsync execution pipelinepython-dotenvEnvironment configuration
