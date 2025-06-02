import os
import logging
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from typing import Dict, Any, List, Optional
import json

logger = logging.getLogger(__name__)

Base = declarative_base()

class CompanyAnalysis(Base):
    """Database model for company analysis data"""
    __tablename__ = 'company_analyses'
    
    id = Column(Integer, primary_key=True)
    company_name = Column(String(255), nullable=False, index=True)
    industry = Column(String(255))
    context_analysis = Column(JSON)
    market_segments = Column(JSON)
    executive_summary = Column(Text)
    analysis_settings = Column(JSON)
    template_enhanced = Column(Boolean, default=False)
    template_key = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MarketSegment(Base):
    """Database model for market segment data"""
    __tablename__ = 'market_segments'
    
    id = Column(Integer, primary_key=True)
    company_name = Column(String(255), nullable=False, index=True)
    segment_name = Column(String(255), nullable=False)
    segment_definition = Column(Text)
    strategic_relevance = Column(Text)
    keywords = Column(JSON)
    suppliers = Column(JSON)
    market_insights = Column(JSON)
    total_urls_processed = Column(Integer, default=0)
    processing_timestamp = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

class SupplierProfile(Base):
    """Database model for supplier profiles"""
    __tablename__ = 'supplier_profiles'
    
    id = Column(Integer, primary_key=True)
    company_name = Column(String(255), nullable=False, index=True)
    segment_name = Column(String(255), nullable=False)
    supplier_name = Column(String(255), nullable=False)
    domain = Column(String(255))
    source_url = Column(String(500))
    overview = Column(Text)
    market_positioning = Column(Text)
    products_services = Column(JSON)
    technological_differentiators = Column(JSON)
    market_traction = Column(JSON)
    esg_profile = Column(JSON)
    innovation_indicators = Column(JSON)
    relevance_score = Column(Float)
    innovation_index = Column(Float)
    esg_rating = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class DatabaseService:
    """Service for managing market intelligence data with PostgreSQL database"""
    
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL')
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable not found")
        
        # Create engine and session
        self.engine = create_engine(self.database_url, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Create tables
        self._create_tables()
        
        logger.info("Database service initialized successfully")
    
    def _create_tables(self):
        """Create database tables if they don't exist"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {e}")
            raise
    
    def get_session(self) -> Session:
        """Get database session"""
        return self.SessionLocal()
    
    def save_company_analysis(self, company_name: str, analysis_data: Dict[str, Any]) -> bool:
        """Save complete company analysis to database"""
        session = self.get_session()
        try:
            # Check if analysis already exists
            existing = session.query(CompanyAnalysis).filter(
                CompanyAnalysis.company_name == company_name
            ).first()
            
            context = analysis_data.get("context_analysis", {})
            
            if existing:
                # Update existing analysis
                existing.industry = context.get("identified_industry")
                existing.context_analysis = context
                existing.market_segments = analysis_data.get("market_segments", {})
                existing.executive_summary = analysis_data.get("executive_summary", "")
                existing.analysis_settings = analysis_data.get("analysis_settings", {})
                existing.template_enhanced = context.get("template_enhanced", False)
                existing.template_key = context.get("template_key")
                # Updated timestamp is handled automatically by onupdate
                
                logger.info(f"Updated existing analysis for company: {company_name}")
            else:
                # Create new analysis
                new_analysis = CompanyAnalysis(
                    company_name=company_name,
                    industry=context.get("identified_industry"),
                    context_analysis=context,
                    market_segments=analysis_data.get("market_segments", {}),
                    executive_summary=analysis_data.get("executive_summary", ""),
                    analysis_settings=analysis_data.get("analysis_settings", {}),
                    template_enhanced=context.get("template_enhanced", False),
                    template_key=context.get("template_key")
                )
                session.add(new_analysis)
                logger.info(f"Created new analysis for company: {company_name}")
            
            # Save market segments separately for better querying
            self._save_market_segments(session, company_name, analysis_data.get("market_segments", {}))
            
            session.commit()
            return True
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving company analysis: {e}")
            return False
        finally:
            session.close()
    
    def _save_market_segments(self, session: Session, company_name: str, segments_data: Dict[str, Any]):
        """Save market segments data separately"""
        try:
            # Delete existing segments for this company
            session.query(MarketSegment).filter(
                MarketSegment.company_name == company_name
            ).delete()
            
            session.query(SupplierProfile).filter(
                SupplierProfile.company_name == company_name
            ).delete()
            
            # Save new segments and suppliers
            for segment_name, segment_info in segments_data.items():
                segment = MarketSegment(
                    company_name=company_name,
                    segment_name=segment_name,
                    segment_definition=segment_info.get("segment_info", {}).get("segment_definition_and_strategic_relevance", ""),
                    keywords=segment_info.get("segment_info", {}).get("intelligence_gathering_keywords", []),
                    suppliers=segment_info.get("suppliers", []),
                    market_insights=segment_info.get("market_insights", []),
                    total_urls_processed=segment_info.get("total_urls_processed", 0),
                    processing_timestamp=datetime.fromtimestamp(segment_info.get("processing_timestamp", 0)) if segment_info.get("processing_timestamp") else None
                )
                session.add(segment)
                
                # Save individual supplier profiles
                for supplier_data in segment_info.get("suppliers", []):
                    supplier = SupplierProfile(
                        company_name=company_name,
                        segment_name=segment_name,
                        supplier_name=supplier_data.get("company_name", ""),
                        domain=supplier_data.get("domain", ""),
                        source_url=supplier_data.get("source_url", ""),
                        overview=supplier_data.get("overview", ""),
                        market_positioning=supplier_data.get("market_positioning", ""),
                        products_services=supplier_data.get("products_services", []),
                        technological_differentiators=supplier_data.get("technological_differentiators", []),
                        market_traction=supplier_data.get("market_traction", {}),
                        esg_profile=supplier_data.get("esg_profile", {}),
                        innovation_indicators=supplier_data.get("innovation_indicators", {}),
                        relevance_score=supplier_data.get("relevance_score", 0),
                        innovation_index=supplier_data.get("innovation_index", 0),
                        esg_rating=supplier_data.get("esg_rating", 0)
                    )
                    session.add(supplier)
            
        except Exception as e:
            logger.error(f"Error saving market segments: {e}")
            raise
    
    def get_company_analysis(self, company_name: str) -> Optional[Dict[str, Any]]:
        """Retrieve company analysis from database"""
        session = self.get_session()
        try:
            analysis = session.query(CompanyAnalysis).filter(
                CompanyAnalysis.company_name == company_name
            ).first()
            
            if not analysis:
                return None
            
            # Convert to dict format expected by the application
            result = {
                "context_analysis": analysis.context_analysis,
                "market_segments": analysis.market_segments,
                "executive_summary": analysis.executive_summary,
                "analysis_settings": analysis.analysis_settings,
                "analysis_timestamp": analysis.created_at.isoformat(),
                "company_name": analysis.company_name
            }
            
            logger.info(f"Retrieved analysis for company: {company_name}")
            return result
            
        except Exception as e:
            logger.error(f"Error retrieving company analysis: {e}")
            return None
        finally:
            session.close()
    
    def list_analyzed_companies(self) -> List[str]:
        """Get list of all analyzed companies"""
        session = self.get_session()
        try:
            companies = session.query(CompanyAnalysis.company_name).distinct().all()
            return [company[0] for company in companies]
        except Exception as e:
            logger.error(f"Error listing companies: {e}")
            return []
        finally:
            session.close()
    
    def delete_company_analysis(self, company_name: str) -> bool:
        """Delete company analysis from database"""
        session = self.get_session()
        try:
            # Delete related data
            session.query(SupplierProfile).filter(
                SupplierProfile.company_name == company_name
            ).delete()
            
            session.query(MarketSegment).filter(
                MarketSegment.company_name == company_name
            ).delete()
            
            session.query(CompanyAnalysis).filter(
                CompanyAnalysis.company_name == company_name
            ).delete()
            
            session.commit()
            logger.info(f"Deleted analysis for company: {company_name}")
            return True
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error deleting company analysis: {e}")
            return False
        finally:
            session.close()
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """Get statistics about stored data"""
        session = self.get_session()
        try:
            total_companies = session.query(CompanyAnalysis).count()
            total_segments = session.query(MarketSegment).count()
            total_suppliers = session.query(SupplierProfile).count()
            
            # Get most recent analysis timestamp
            latest_analysis = session.query(CompanyAnalysis).order_by(
                CompanyAnalysis.created_at.desc()
            ).first()
            
            last_updated = latest_analysis.created_at.isoformat() if latest_analysis else "No data"
            
            return {
                "total_companies": total_companies,
                "total_market_segments": total_segments,
                "total_suppliers": total_suppliers,
                "database_type": "PostgreSQL",
                "last_updated": last_updated
            }
            
        except Exception as e:
            logger.error(f"Error getting storage stats: {e}")
            return {"error": str(e)}
        finally:
            session.close()