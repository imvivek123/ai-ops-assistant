"""Analyzer Tool - Pandas-based data analysis"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


def analyze_dataframe(df_data: Any) -> Dict[str, Any]:
    """Analyze a pandas DataFrame and extract insights"""
    if not PANDAS_AVAILABLE:
        return {'status': 'error', 'error': 'pandas not installed'}
    
    try:
        if isinstance(df_data, dict):
            df = pd.DataFrame(df_data)
        else:
            df = df_data
        
        analysis = {
            'status': 'success',
            'shape': {'rows': len(df), 'columns': len(df.columns)},
            'columns': list(df.columns),
            'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
            'summary_stats': {},
            'missing_values': {},
            'correlations': {}
        }
        
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        for col in numeric_cols:
            try:
                analysis['summary_stats'][col] = {
                    'count': int(df[col].count()),
                    'mean': float(df[col].mean()),
                    'median': float(df[col].median()),
                    'std': float(df[col].std()),
                    'min': float(df[col].min()),
                    'max': float(df[col].max()),
                    'q25': float(df[col].quantile(0.25)),
                    'q75': float(df[col].quantile(0.75))
                }
            except Exception as e:
                logger.warning(f"Could not calculate stats for {col}: {str(e)}")
        
        missing = df.isnull().sum()
        for col in df.columns:
            if missing[col] > 0:
                analysis['missing_values'][col] = int(missing[col])
        
        if len(numeric_cols) > 1:
            try:
                corr_matrix = df[numeric_cols].corr()
                analysis['correlations'] = corr_matrix.to_dict()
            except Exception as e:
                logger.warning(f"Could not calculate correlations: {str(e)}")
        
        logger.info(f"Successfully analyzed DataFrame: {analysis['shape']}")
        return analysis
        
    except Exception as e:
        logger.error(f"Error analyzing DataFrame: {str(e)}")
        return {'status': 'error', 'error': str(e)}


def detect_outliers(df_data: Any, column: str, std_threshold: float = 2.0) -> Dict[str, Any]:
    """Detect outliers in a column using standard deviation"""
    if not PANDAS_AVAILABLE:
        return {'status': 'error', 'error': 'pandas not installed'}
    
    try:
        if isinstance(df_data, dict):
            df = pd.DataFrame(df_data)
        else:
            df = df_data
        
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found")
        
        mean = df[column].mean()
        std = df[column].std()
        threshold = std_threshold * std
        
        outliers = df[
            (df[column] > mean + threshold) | (df[column] < mean - threshold)
        ]
        
        result = {
            'status': 'success',
            'column': column,
            'mean': float(mean),
            'std': float(std),
            'threshold': float(threshold),
            'outlier_count': len(outliers),
            'outlier_percentage': float((len(outliers) / len(df)) * 100),
            'outlier_indices': outliers.index.tolist() if len(outliers) > 0 else []
        }
        
        logger.info(f"Detected {len(outliers)} outliers in {column}")
        return result
        
    except Exception as e:
        logger.error(f"Error detecting outliers: {str(e)}")
        return {'status': 'error', 'error': str(e)}
