import json
import os
import logging
from openai import OpenAI
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class OpenAIService:
    """Service for OpenAI API interactions"""
    
    def __init__(self):
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        self.model = "gpt-4o"
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        if not self.api_key:
            logger.error("OpenAI API key not found in environment variables")
            raise ValueError("OpenAI API key is required")
        
        self.client = OpenAI(api_key=self.api_key)
    
    def analyze_company_context(self, company_name: str, template_service=None) -> Optional[Dict[str, Any]]:
        """
        Phase 1: Analyze company context and identify market segments
        Returns structured JSON with industry analysis and supplier segments
        """
        try:
            prompt = self._get_phase1_prompt(company_name)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a Principal Market Intelligence Strategist. Provide detailed, accurate market analysis in valid JSON format only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=4000,
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            if not content:
                raise ValueError("Empty response from OpenAI")
            result = json.loads(content)
            
            # Enhance with template data if available
            if template_service:
                identified_industry = result.get("identified_industry", "")
                template_key = template_service.identify_industry_template(company_name, identified_industry)
                
                if template_key:
                    ai_segments = result.get("critical_supplier_market_segments", [])
                    enhanced_segments = template_service.enhance_segments_with_template(ai_segments, template_key)
                    result["critical_supplier_market_segments"] = enhanced_segments
                    result["template_enhanced"] = True
                    result["template_key"] = template_key
                    logger.info(f"Enhanced analysis with template: {template_key}")
            
            logger.info(f"Successfully analyzed context for company: {company_name}")
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse OpenAI JSON response: {e}")
            return None
        except Exception as e:
            logger.error(f"Error in company context analysis: {e}")
            return None
    
    def analyze_supplier_content(self, content: str, segment_name: str) -> Optional[Dict[str, Any]]:
        """
        Analyze scraped content to generate detailed supplier profile
        """
        try:
            prompt = f"""
            You are an expert market analyst. Analyze the following content from a potential supplier website 
            in the "{segment_name}" market segment. Generate a comprehensive supplier profile in JSON format.
            
            Content to analyze:
            {content[:8000]}  # Limit content length
            
            Provide your analysis as a valid JSON object with the following structure:
            {{
                "company_name": "Extracted company name",
                "overview": "Company overview and mission (2-3 sentences)",
                "market_positioning": "Market position and value proposition",
                "products_services": ["List of key products/services relevant to segment"],
                "technological_differentiators": ["Key technologies and innovations"],
                "market_traction": {{
                    "key_clients": ["Notable clients mentioned"],
                    "partnerships": ["Strategic partnerships"],
                    "case_studies": ["Brief descriptions of success stories"]
                }},
                "esg_profile": {{
                    "environmental": "Environmental initiatives and commitments",
                    "social": "Social responsibility programs",
                    "governance": "Governance practices mentioned"
                }},
                "innovation_indicators": {{
                    "rd_focus": "R&D focus areas",
                    "patents_mentioned": "Any patent or IP mentions",
                    "new_products": "Recent product launches or pipeline"
                }},
                "relevance_score": "Score from 1-10 indicating relevance to segment",
                "innovation_index": "Score from 1-10 indicating innovation level",
                "esg_rating": "Score from 1-10 based on ESG mentions"
            }}
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                max_tokens=2000,
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            logger.info(f"Successfully analyzed supplier content for segment: {segment_name}")
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing supplier content: {e}")
            return None
    
    def analyze_market_content(self, content: str, segment_name: str) -> Optional[Dict[str, Any]]:
        """
        Analyze market research content to generate segment insights
        """
        try:
            prompt = f"""
            You are a senior market research analyst. Analyze the following content about the "{segment_name}" market segment.
            Generate comprehensive market insights in JSON format.
            
            Content to analyze:
            {content[:8000]}  # Limit content length
            
            Provide your analysis as a valid JSON object with the following structure:
            {{
                "segment_overview": "Comprehensive overview of the market segment",
                "market_trends": ["Key trends and developments"],
                "technological_disruptions": ["Major tech disruptions and innovations"],
                "competitive_landscape": "Overview of competitive dynamics",
                "market_drivers": ["Primary growth drivers"],
                "market_restraints": ["Key challenges and barriers"],
                "future_outlook": "Future projections and growth prospects",
                "regulatory_impacts": ["Regulatory changes affecting the market"],
                "key_statistics": {{
                    "market_size": "Market size if mentioned",
                    "growth_rate": "Growth rate if mentioned",
                    "key_metrics": ["Other relevant metrics"]
                }}
            }}
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                max_tokens=2000,
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            logger.info(f"Successfully analyzed market content for segment: {segment_name}")
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing market content: {e}")
            return None
    
    def generate_executive_summary(self, analysis_data: Dict[str, Any]) -> str:
        """
        Generate executive summary from complete analysis data
        """
        try:
            prompt = f"""
            Generate a comprehensive executive summary for a market intelligence report based on the following analysis data.
            Focus on key insights, opportunities, and strategic recommendations.
            
            Analysis Data:
            {json.dumps(analysis_data, indent=2)}
            
            Provide a professional executive summary (3-5 paragraphs) that highlights:
            1. Key market opportunities across all segments
            2. Major technological trends and disruptions
            3. Most promising supplier relationships
            4. Strategic recommendations for competitive advantage
            5. Potential risks and mitigation strategies
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1500,
                temperature=0.4
            )
            
            summary = response.choices[0].message.content
            logger.info("Successfully generated executive summary")
            return summary
            
        except Exception as e:
            logger.error(f"Error generating executive summary: {e}")
            return "Executive summary generation failed. Please review individual segment analyses."
    
    def enhance_supplier_profile(self, supplier_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance supplier profile with AI analysis"""
        try:
            supplier_name = supplier_data.get('name', 'Unknown Supplier')
            description = supplier_data.get('description', '')
            
            prompt = f"""
            Analyze this supplier and provide enhanced insights:
            
            Supplier: {supplier_name}
            Description: {description}
            
            Provide analysis in JSON format with these fields:
            - "market_positioning": Brief market position analysis
            - "innovation_index": Score 0-100 for innovation capability  
            - "esg_rating": Score 0-100 for ESG performance
            - "products_services": List of key products/services
            - "technological_differentiators": List of key tech advantages
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                max_tokens=1000,
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            if content:
                enhanced_data = json.loads(content)
                supplier_data.update(enhanced_data)
                
            return supplier_data
            
        except Exception as e:
            logger.error(f"Error enhancing supplier profile: {e}")
            return supplier_data
    
    def generate_executive_summary(self, analysis_data: Dict[str, Any], company_name: str) -> str:
        """Generate executive summary from analysis data"""
        try:
            segments_info = ""
            if "market_segments" in analysis_data:
                for segment_name, segment_data in analysis_data["market_segments"].items():
                    suppliers_count = len(segment_data.get("suppliers", []))
                    segments_info += f"- {segment_name}: {suppliers_count} suppliers analyzed\n"
            
            prompt = f"""
            Create an executive summary for market intelligence analysis of {company_name}.
            
            Analysis includes:
            {segments_info}
            
            Provide a concise 3-4 paragraph executive summary covering:
            1. Key market insights discovered
            2. Notable supplier trends and opportunities
            3. Strategic recommendations
            
            Keep it professional and actionable.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.4
            )
            
            return response.choices[0].message.content or "Executive summary generated successfully."
            
        except Exception as e:
            logger.error(f"Error generating executive summary: {e}")
            return "Unable to generate executive summary at this time."
    
    def _get_phase1_prompt(self, company_name: str) -> str:
        """Generate the Phase 1 prompt for company context analysis"""
        return f"""
        You are a Principal Market Intelligence Strategist. Your mandate is to conduct a thorough market analysis to identify strategic supplier market segments and key intelligence gathering vectors relevant to the company: '{company_name}'. The output will drive a comprehensive market intelligence report.

        Given the company name: '{company_name}'

        Provide your analysis as a meticulously structured VALID JSON object adhering to the following schema:

        1. "context_company_name": The exact company name provided.
        2. "identified_industry": A precise identification of the company's primary industry and sub-sector (e.g., "UK Regulated Water & Wastewater Services," "Global Automotive OEM - Electric Vehicles," "International E-commerce & Digital Marketplace Platforms").
        3. "strategic_industry_overview": A concise (3-4 sentences) executive overview of this industry, detailing its core operational imperatives, prevailing strategic challenges, key growth drivers, and significant regulatory considerations. This sets the strategic context for market intelligence.
        4. "critical_supplier_market_segments": A list of 6 to 8 critical and distinct supplier market segments. These segments are vital for the operational continuity, innovation, and strategic advantage of companies like '{company_name}'. Each item in this list must be an object with:
           a. "segment_name": A formal and descriptive name for the supplier market segment (e.g., "Next-Generation SCADA & Industrial Control Systems Security Market," "Advanced Water Purification & Desalination Technologies Market," "AI-Driven Predictive Analytics for Utility Operations Market," "Sustainable & Circular Economy Solutions for Industrial Waste Market").
           b. "segment_definition_and_strategic_relevance": A detailed 2-3 sentence description defining the scope of this market segment and explaining its strategic importance to the '{company_name}'s industry, including how it addresses key challenges or enables opportunities.
           c. "intelligence_gathering_keywords": A list of 4 to 6 highly specific and effective Google search keywords. These keywords must be crafted to uncover:
              i. Leading, emerging, and innovative companies (potential suppliers and key players) within this market segment.
              ii. Authoritative market research reports, in-depth industry analyses, news articles discussing significant technological advancements, M&A activities, competitive shifts, or regulatory changes impacting this segment, especially in relation to the '{company_name}'s industry.
              (Example keywords for a sophisticated search: "Frost & Sullivan report predictive analytics utilities market share", "innovative SCADA cybersecurity solutions critical infrastructure vendors", "venture capital funding sustainable industrial waste technologies Europe", "case studies AI water purification municipal")

        Ensure every response is a valid JSON object that can be parsed without errors. Focus on strategic depth, business relevance, and actionable intelligence gathering capabilities.
        """