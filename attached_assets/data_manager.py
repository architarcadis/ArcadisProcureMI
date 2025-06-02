import json
import os
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import threading

logger = logging.getLogger(__name__)

class DataManager:
    """Service for managing market intelligence data storage and retrieval"""
    
    def __init__(self, data_file: str = "market_intelligence_data_PROD.json"):
        self.data_file = data_file
        self.lock = threading.Lock()
        self._ensure_data_file_exists()
    
    def _ensure_data_file_exists(self):
        """Ensure the data file exists with proper structure"""
        if not os.path.exists(self.data_file):
            initial_data = {
                "metadata": {
                    "created_timestamp": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat(),
                    "version": "1.0"
                },
                "companies": {}
            }
            self.save_data(initial_data)
    
    def load_data(self) -> Dict[str, Any]:
        """Load data from JSON file with error handling"""
        try:
            with self.lock:
                with open(self.data_file, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    return data
        except FileNotFoundError:
            logger.warning(f"Data file {self.data_file} not found, creating new one")
            self._ensure_data_file_exists()
            return self.load_data()
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from {self.data_file}: {e}")
            return {"metadata": {}, "companies": {}}
        except Exception as e:
            logger.error(f"Unexpected error loading data: {e}")
            return {"metadata": {}, "companies": {}}
    
    def save_data(self, data: Dict[str, Any]) -> bool:
        """Save data to JSON file with error handling"""
        try:
            with self.lock:
                # Update metadata
                if "metadata" not in data:
                    data["metadata"] = {}
                data["metadata"]["last_updated"] = datetime.now().isoformat()
                
                # Write to file
                with open(self.data_file, 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=2, ensure_ascii=False)
                
                logger.info(f"Data saved successfully to {self.data_file}")
                return True
                
        except Exception as e:
            logger.error(f"Error saving data to {self.data_file}: {e}")
            return False
    
    def save_company_analysis(self, company_name: str, analysis_data: Dict[str, Any]) -> bool:
        """Save complete company analysis to storage"""
        try:
            data = self.load_data()
            
            # Ensure companies section exists
            if "companies" not in data:
                data["companies"] = {}
            
            # Add timestamp to analysis
            analysis_data["analysis_timestamp"] = datetime.now().isoformat()
            analysis_data["company_name"] = company_name
            
            # Store under company name
            data["companies"][company_name] = analysis_data
            
            return self.save_data(data)
            
        except Exception as e:
            logger.error(f"Error saving company analysis for {company_name}: {e}")
            return False
    
    def get_company_analysis(self, company_name: str) -> Optional[Dict[str, Any]]:
        """Retrieve company analysis from storage"""
        try:
            data = self.load_data()
            return data.get("companies", {}).get(company_name)
        except Exception as e:
            logger.error(f"Error retrieving company analysis for {company_name}: {e}")
            return None
    
    def list_analyzed_companies(self) -> List[str]:
        """Get list of all analyzed companies"""
        try:
            data = self.load_data()
            return list(data.get("companies", {}).keys())
        except Exception as e:
            logger.error(f"Error listing analyzed companies: {e}")
            return []
    
    def delete_company_analysis(self, company_name: str) -> bool:
        """Delete company analysis from storage"""
        try:
            data = self.load_data()
            if company_name in data.get("companies", {}):
                del data["companies"][company_name]
                return self.save_data(data)
            return True
        except Exception as e:
            logger.error(f"Error deleting company analysis for {company_name}: {e}")
            return False
    
    def export_company_data_csv(self, company_name: str) -> Optional[str]:
        """Export company supplier data to CSV format"""
        try:
            analysis = self.get_company_analysis(company_name)
            if not analysis:
                return None
            
            import io
            import csv
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write header
            writer.writerow([
                'Market Segment', 'Company Name', 'Relevance Score', 
                'Innovation Index', 'ESG Rating', 'Domain', 'Technologies'
            ])
            
            # Write supplier data
            market_segments = analysis.get("market_segments", {})
            for segment_name, segment_data in market_segments.items():
                suppliers = segment_data.get("suppliers", [])
                for supplier in suppliers:
                    writer.writerow([
                        segment_name,
                        supplier.get("company_name", ""),
                        supplier.get("relevance_score", ""),
                        supplier.get("innovation_index", ""),
                        supplier.get("esg_rating", ""),
                        supplier.get("domain", ""),
                        ", ".join(supplier.get("technological_differentiators", []))
                    ])
            
            csv_content = output.getvalue()
            output.close()
            
            logger.info(f"Exported CSV data for company: {company_name}")
            return csv_content
            
        except Exception as e:
            logger.error(f"Error exporting CSV for {company_name}: {e}")
            return None
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """Get statistics about stored data"""
        try:
            data = self.load_data()
            companies = data.get("companies", {})
            
            stats = {
                "total_companies": len(companies),
                "total_market_segments": 0,
                "total_suppliers": 0,
                "file_size_mb": 0,
                "last_updated": data.get("metadata", {}).get("last_updated", "Unknown")
            }
            
            # Calculate detailed stats
            for company_data in companies.values():
                segments = company_data.get("market_segments", {})
                stats["total_market_segments"] += len(segments)
                
                for segment_data in segments.values():
                    suppliers = segment_data.get("suppliers", [])
                    stats["total_suppliers"] += len(suppliers)
            
            # File size
            if os.path.exists(self.data_file):
                file_size = os.path.getsize(self.data_file)
                stats["file_size_mb"] = round(file_size / (1024 * 1024), 2)
            
            return stats
            
        except Exception as e:
            logger.error(f"Error calculating storage stats: {e}")
            return {"error": str(e)}
    
    def cleanup_old_analyses(self, days_old: int = 30) -> int:
        """Remove analyses older than specified days"""
        try:
            from datetime import timedelta
            
            cutoff_date = datetime.now() - timedelta(days=days_old)
            data = self.load_data()
            companies = data.get("companies", {})
            
            removed_count = 0
            companies_to_remove = []
            
            for company_name, company_data in companies.items():
                timestamp_str = company_data.get("analysis_timestamp")
                if timestamp_str:
                    try:
                        analysis_date = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                        if analysis_date < cutoff_date:
                            companies_to_remove.append(company_name)
                    except ValueError:
                        continue
            
            # Remove old analyses
            for company_name in companies_to_remove:
                del companies[company_name]
                removed_count += 1
            
            if removed_count > 0:
                self.save_data(data)
                logger.info(f"Cleaned up {removed_count} old analyses")
            
            return removed_count
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            return 0
