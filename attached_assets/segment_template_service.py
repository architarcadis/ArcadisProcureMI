import json
import os
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class SegmentTemplateService:
    """Service for managing predefined market segment templates and keywords"""
    
    def __init__(self, template_file: str = "market_segments_template.json"):
        self.template_file = template_file
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, Any]:
        """Load predefined market segment templates"""
        try:
            if os.path.exists(self.template_file):
                with open(self.template_file, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    logger.info(f"Loaded {len(data.get('market_segments_templates', {}))} industry templates")
                    return data.get('market_segments_templates', {})
            else:
                logger.warning(f"Template file {self.template_file} not found")
                return {}
        except Exception as e:
            logger.error(f"Error loading templates: {e}")
            return {}
    
    def identify_industry_template(self, company_name: str, identified_industry: str) -> Optional[str]:
        """Identify the best matching industry template based on company and industry"""
        industry_lower = identified_industry.lower()
        
        # Industry matching patterns
        industry_mappings = {
            'technology_companies': [
                'software', 'technology', 'tech', 'cloud', 'saas', 'ai', 'artificial intelligence',
                'machine learning', 'data', 'analytics', 'platform', 'digital', 'internet',
                'cybersecurity', 'security', 'fintech', 'edtech'
            ],
            'utility_companies': [
                'utility', 'utilities', 'water', 'wastewater', 'electric', 'electricity',
                'power', 'energy', 'gas', 'municipal', 'infrastructure', 'grid'
            ],
            'manufacturing_companies': [
                'manufacturing', 'industrial', 'automotive', 'aerospace', 'chemicals',
                'materials', 'construction', 'machinery', 'equipment', 'production'
            ],
            'financial_services': [
                'financial', 'finance', 'banking', 'insurance', 'investment', 'capital',
                'asset management', 'wealth', 'trading', 'payments', 'fintech'
            ],
            'healthcare_companies': [
                'healthcare', 'health', 'medical', 'pharmaceutical', 'pharma', 'biotech',
                'biotechnology', 'hospital', 'clinical', 'diagnostic', 'therapeutics'
            ]
        }
        
        # Find best matching template
        for template_key, keywords in industry_mappings.items():
            if any(keyword in industry_lower for keyword in keywords):
                logger.info(f"Matched industry template: {template_key}")
                return template_key
        
        # Default fallback based on common company patterns
        company_lower = company_name.lower()
        if any(word in company_lower for word in ['tech', 'soft', 'data', 'cloud', 'ai']):
            return 'technology_companies'
        elif any(word in company_lower for word in ['water', 'electric', 'power', 'energy']):
            return 'utility_companies'
        elif any(word in company_lower for word in ['manufacturing', 'industrial', 'auto']):
            return 'manufacturing_companies'
        elif any(word in company_lower for word in ['bank', 'financial', 'capital', 'invest']):
            return 'financial_services'
        elif any(word in company_lower for word in ['health', 'medical', 'pharma', 'bio']):
            return 'healthcare_companies'
        
        logger.info("No specific template match found, will use custom analysis")
        return None
    
    def get_template_segments(self, template_key: str) -> List[Dict[str, Any]]:
        """Get predefined segments for a specific industry template"""
        if template_key in self.templates:
            segments = self.templates[template_key].get('segments', [])
            logger.info(f"Retrieved {len(segments)} segments for template: {template_key}")
            return segments
        return []
    
    def enhance_segments_with_template(self, ai_segments: List[Dict[str, Any]], 
                                     template_key: Optional[str]) -> List[Dict[str, Any]]:
        """Enhance AI-generated segments with template data"""
        if not template_key or template_key not in self.templates:
            return ai_segments
        
        template_segments = self.get_template_segments(template_key)
        enhanced_segments = []
        
        # Try to match AI segments with template segments
        for ai_segment in ai_segments:
            ai_name = ai_segment.get('segment_name', '').lower()
            
            # Find best matching template segment
            best_match = None
            best_score = 0
            
            for template_segment in template_segments:
                template_name = template_segment.get('segment_name', '').lower()
                
                # Simple keyword matching score
                ai_keywords = set(ai_name.split())
                template_keywords = set(template_name.split())
                overlap = len(ai_keywords.intersection(template_keywords))
                
                if overlap > best_score:
                    best_score = overlap
                    best_match = template_segment
            
            # Enhance with template data if good match found
            if best_match and best_score > 0:
                enhanced_segment = ai_segment.copy()
                
                # Add template keywords to AI keywords
                ai_keywords = enhanced_segment.get('intelligence_gathering_keywords', [])
                template_keywords = best_match.get('intelligence_keywords', [])
                
                # Combine and deduplicate keywords
                combined_keywords = list(set(ai_keywords + template_keywords))
                enhanced_segment['intelligence_gathering_keywords'] = combined_keywords[:8]  # Limit to 8 keywords
                
                # Add template metadata
                enhanced_segment['template_enhanced'] = True
                enhanced_segment['template_source'] = template_key
                
                enhanced_segments.append(enhanced_segment)
                logger.info(f"Enhanced segment '{ai_segment.get('segment_name')}' with template data")
            else:
                enhanced_segments.append(ai_segment)
        
        # Add any unmatched template segments as additional opportunities
        used_template_names = set()
        for segment in enhanced_segments:
            if segment.get('template_enhanced'):
                # This is rough matching, but helps avoid duplicates
                segment_name_keywords = set(segment.get('segment_name', '').lower().split())
                for template_segment in template_segments:
                    template_keywords = set(template_segment.get('segment_name', '').lower().split())
                    if len(segment_name_keywords.intersection(template_keywords)) > 0:
                        used_template_names.add(template_segment.get('segment_name'))
        
        # Add unused template segments as additional analysis areas
        for template_segment in template_segments:
            if template_segment.get('segment_name') not in used_template_names:
                segment_def = template_segment.get('segment_definition', '') or ''
                strategic_rel = template_segment.get('strategic_relevance', '') or ''
                combined_definition = f"{segment_def} {strategic_rel}".strip()
                
                additional_segment = {
                    'segment_name': template_segment.get('segment_name'),
                    'segment_definition_and_strategic_relevance': combined_definition,
                    'intelligence_gathering_keywords': template_segment.get('intelligence_keywords', []),
                    'template_enhanced': True,
                    'template_source': template_key,
                    'additional_opportunity': True
                }
                enhanced_segments.append(additional_segment)
                logger.info(f"Added additional template segment: {template_segment.get('segment_name')}")
        
        logger.info(f"Enhanced {len(ai_segments)} AI segments to {len(enhanced_segments)} total segments")
        return enhanced_segments
    
    def get_industry_insights(self, template_key: str) -> Dict[str, Any]:
        """Get general industry insights for dashboard storytelling"""
        industry_insights = {
            'technology_companies': {
                'key_trends': [
                    'Cloud-first digital transformation',
                    'AI/ML integration across all sectors',
                    'Zero-trust security architecture adoption',
                    'Low-code/no-code platform proliferation',
                    'Edge computing and 5G enablement'
                ],
                'market_drivers': [
                    'Remote work digitalization',
                    'Data privacy regulations',
                    'Sustainability requirements',
                    'Customer experience demands',
                    'Operational efficiency needs'
                ],
                'competitive_dynamics': 'Rapid innovation cycles, platform ecosystems, and strategic partnerships drive competitive advantage',
                'outlook': 'Strong growth expected in AI, cybersecurity, and cloud infrastructure segments'
            },
            'utility_companies': {
                'key_trends': [
                    'Smart grid modernization initiatives',
                    'Renewable energy integration',
                    'IoT-enabled infrastructure monitoring',
                    'Predictive maintenance adoption',
                    'Customer engagement digitalization'
                ],
                'market_drivers': [
                    'Regulatory compliance requirements',
                    'Infrastructure aging concerns',
                    'Environmental sustainability goals',
                    'Operational cost pressures',
                    'Grid reliability demands'
                ],
                'competitive_dynamics': 'Technology adoption for operational efficiency and regulatory compliance creates supplier selection pressures',
                'outlook': 'Significant investment in grid modernization and smart infrastructure technologies'
            },
            'manufacturing_companies': {
                'key_trends': [
                    'Industry 4.0 smart factory adoption',
                    'Supply chain digitalization',
                    'Predictive quality control systems',
                    'Sustainable manufacturing practices',
                    'Robotics and automation expansion'
                ],
                'market_drivers': [
                    'Supply chain resilience needs',
                    'Quality and compliance requirements',
                    'Labor shortage challenges',
                    'Cost optimization pressures',
                    'Customer customization demands'
                ],
                'competitive_dynamics': 'Technology integration for operational excellence and supply chain agility drives vendor partnerships',
                'outlook': 'Growth in IIoT, automation, and supply chain technologies'
            },
            'financial_services': {
                'key_trends': [
                    'Digital banking transformation',
                    'Open banking API adoption',
                    'RegTech compliance automation',
                    'AI-powered risk management',
                    'Cryptocurrency integration'
                ],
                'market_drivers': [
                    'Customer experience expectations',
                    'Regulatory compliance complexity',
                    'Fraud prevention needs',
                    'Operational cost reduction',
                    'Market volatility management'
                ],
                'competitive_dynamics': 'Technology innovation for customer experience and regulatory compliance creates fintech partnerships',
                'outlook': 'Continued investment in digital platforms and risk management technologies'
            },
            'healthcare_companies': {
                'key_trends': [
                    'Telemedicine platform expansion',
                    'AI-assisted diagnostics',
                    'Electronic health record integration',
                    'Precision medicine development',
                    'Remote patient monitoring'
                ],
                'market_drivers': [
                    'Patient care quality improvement',
                    'Healthcare cost containment',
                    'Regulatory compliance requirements',
                    'Population health management',
                    'Clinical efficiency needs'
                ],
                'competitive_dynamics': 'Technology adoption for patient outcomes and operational efficiency drives healthcare IT partnerships',
                'outlook': 'Strong growth in digital health and AI-powered medical technologies'
            }
        }
        
        return industry_insights.get(template_key, {
            'key_trends': ['Industry-specific technology adoption'],
            'market_drivers': ['Operational efficiency and compliance'],
            'competitive_dynamics': 'Technology partnerships drive competitive advantage',
            'outlook': 'Growth expected in digital transformation technologies'
        })