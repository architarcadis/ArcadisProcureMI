import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

class DataProcessor:
    """Utility class for processing procurement data"""
    
    @staticmethod
    def validate_data(df):
        """Validate uploaded procurement data"""
        if df is None or df.empty:
            return False, "No data available"
        
        required_patterns = [
            'requisition', 'approval', 'contract', 'supplier', 
            'invoice', 'payment', 'date', 'timestamp'
        ]
        
        columns_lower = [col.lower() for col in df.columns]
        found_patterns = []
        
        for pattern in required_patterns:
            if any(pattern in col for col in columns_lower):
                found_patterns.append(pattern)
        
        if len(found_patterns) < 3:
            return False, f"Insufficient procurement data columns. Found: {found_patterns}"
        
        return True, f"Valid procurement data with {len(found_patterns)} relevant columns"
    
    @staticmethod
    def extract_date_columns(df):
        """Extract date/timestamp columns from dataframe"""
        if df is None:
            return []
        
        date_columns = []
        for col in df.columns:
            if any(keyword in col.lower() for keyword in ['date', 'time', 'timestamp', 'created', 'updated']):
                date_columns.append(col)
        
        return date_columns
    
    @staticmethod
    def calculate_cycle_times(df, start_col, end_col):
        """Calculate cycle times between two date columns"""
        try:
            if start_col not in df.columns or end_col not in df.columns:
                return None
            
            start_dates = pd.to_datetime(df[start_col], errors='coerce')
            end_dates = pd.to_datetime(df[end_col], errors='coerce')
            
            cycle_times = (end_dates - start_dates).dt.days
            return cycle_times.dropna()
        
        except Exception as e:
            st.error(f"Error calculating cycle times: {str(e)}")
            return None
    
    @staticmethod
    def get_numeric_columns(df):
        """Get numeric columns from dataframe"""
        if df is None:
            return []
        
        return df.select_dtypes(include=[np.number]).columns.tolist()
    
    @staticmethod
    def get_categorical_columns(df):
        """Get categorical columns from dataframe"""
        if df is None:
            return []
        
        return df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    @staticmethod
    def create_summary_stats(df):
        """Create summary statistics for the dataset"""
        if df is None or df.empty:
            return None
        
        stats = {
            'total_records': len(df),
            'numeric_columns': len(DataProcessor.get_numeric_columns(df)),
            'categorical_columns': len(DataProcessor.get_categorical_columns(df)),
            'date_columns': len(DataProcessor.extract_date_columns(df)),
            'missing_values': df.isnull().sum().sum(),
            'completeness': (1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        }
        
        return stats
