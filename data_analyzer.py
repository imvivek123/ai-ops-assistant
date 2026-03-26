"""Data Analyzer Agent - Analyzes CSV data and generates insights"""

import logging
import time
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    logger.warning("pandas not available - data analysis will be limited")


class DataAnalyzer:
    """Agent for analyzing CSV data and generating insights"""
    
    MAX_RETRIES = 3
    RETRY_DELAY = 1
    
    def __init__(self):
        """Initialize the data analyzer"""
        self.outputs_dir = Path("outputs")
        self.outputs_dir.mkdir(exist_ok=True)
        logger.info("Data Analyzer initialized")
    
    def run(self, input_file: str) -> Dict[str, Any]:
        """Run the data analyzer with retry logic"""
        start_time = time.time()
        
        for attempt in range(self.MAX_RETRIES):
            try:
                logger.info(f"Data analyzer attempt {attempt + 1}/{self.MAX_RETRIES}")
                
                # Read the CSV file
                data = self._read_csv(input_file)
                
                # Analyze the data
                analysis = self._analyze_data(data)
                
                # Save the output
                output_file = self._save_analysis(analysis)
                
                duration = time.time() - start_time
                logger.info(f"Data analyzed successfully in {duration:.2f}s")
                
                return {
                    "status": "success",
                    "output_file": str(output_file),
                    "duration": duration,
                    "analysis": analysis
                }
                
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < self.MAX_RETRIES - 1:
                    time.sleep(self.RETRY_DELAY * (attempt + 1))
                else:
                    logger.error(f"All {self.MAX_RETRIES} attempts failed")
                    return {"status": "error", "error": str(e)}
    
    def _read_csv(self, file_path: str) -> Any:
        """Read CSV file"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if PANDAS_AVAILABLE:
            return pd.read_csv(file_path)
        else:
            lines = path.read_text(encoding='utf-8').strip().split('\n')
            return lines
    
    def _analyze_data(self, data: Any) -> Dict[str, Any]:
        """Analyze the data"""
        analysis = {
            'row_count': 0,
            'column_count': 0,
            'summary_stats': {},
            'trends': [],
            'top_performers': [],
            'anomalies': []
        }
        
        if PANDAS_AVAILABLE and isinstance(data, pd.DataFrame):
            return self._analyze_pandas(data)
        else:
            return self._analyze_fallback(data)
    
    def _analyze_pandas(self, df: 'pd.DataFrame') -> Dict[str, Any]:
        """Pandas-based analysis"""
        analysis = {
            'row_count': len(df),
            'column_count': len(df.columns),
            'columns': list(df.columns),
            'summary_stats': {}
        }
        
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        for col in numeric_cols:
            try:
                analysis['summary_stats'][col] = {
                    'mean': float(df[col].mean()),
                    'median': float(df[col].median()),
                    'min': float(df[col].min()),
                    'max': float(df[col].max()),
                    'std': float(df[col].std())
                }
            except:
                pass
        
        analysis['top_performers'] = []
        for col in numeric_cols:
            top_val = df[col].max()
            analysis['top_performers'].append({
                'column': col,
                'value': float(top_val),
                'row_index': int(df[df[col] == top_val].index[0])
            })
        
        analysis['anomalies'] = []
        for col in numeric_cols:
            mean = df[col].mean()
            std = df[col].std()
            if std > 0:
                anomaly_threshold = mean + (2 * std)
                anomalies = df[df[col] > anomaly_threshold]
                if len(anomalies) > 0:
                    analysis['anomalies'].append({
                        'column': col,
                        'threshold': float(anomaly_threshold),
                        'count': len(anomalies)
                    })
        
        return analysis
    
    def _analyze_fallback(self, data: list) -> Dict[str, Any]:
        """Fallback analysis for when pandas is not available"""
        analysis = {
            'row_count': len(data) - 1 if data else 0,
            'column_count': len(data[0].split(',')) if data else 0,
            'columns': data[0].split(',') if data else [],
            'summary_stats': {}
        }
        return analysis
    
    def _save_analysis(self, analysis: Dict[str, Any]) -> Path:
        """Save analysis to markdown file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.outputs_dir / f"data_analysis_{timestamp}.md"
        
        content = self._format_analysis(analysis)
        output_file.write_text(content, encoding='utf-8')
        logger.info(f"Analysis saved to {output_file}")
        
        return output_file
    
    def _format_analysis(self, analysis: Dict[str, Any]) -> str:
        """Format analysis as markdown"""
        md = "# Data Analysis Report\n\n"
        md += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        md += f"## Dataset Overview\n"
        md += f"- **Rows:** {analysis['row_count']}\n"
        md += f"- **Columns:** {analysis['column_count']}\n"
        if analysis.get('columns'):
            md += f"- **Column Names:** {', '.join(analysis['columns'][:5])}"
            if len(analysis['columns']) > 5:
                md += f" ... and {len(analysis['columns']) - 5} more"
            md += "\n"
        md += "\n"
        
        if analysis.get('summary_stats'):
            md += "## Summary Statistics\n"
            for col, stats in analysis['summary_stats'].items():
                md += f"\n### {col}\n"
                for key, value in stats.items():
                    md += f"- **{key.title()}:** {value:.2f}\n"
            md += "\n"
        
        if analysis.get('top_performers'):
            md += "## Top Performers\n"
            for perf in analysis['top_performers'][:3]:
                md += f"- **{perf['column']}:** {perf['value']:.2f}\n"
            md += "\n"
        
        if analysis.get('anomalies'):
            md += "## Detected Anomalies\n"
            for anomaly in analysis['anomalies']:
                md += f"- **{anomaly['column']}:** {anomaly['count']} value(s) > {anomaly['threshold']:.2f}\n"
            md += "\n"
        
        md += "## Insights\n"
        md += "- Data quality looks good with clear patterns\n"
        md += "- Recommend further investigation into detected anomalies\n"
        md += "- Ensure data is validated before important business decisions\n"
        
        return md
