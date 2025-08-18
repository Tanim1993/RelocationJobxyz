"""
AI Resume Localizer
Automatically adapt resumes for different country standards and cultural formatting
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class ResumeFormat(Enum):
    US_STANDARD = "us_standard"
    EU_STANDARD = "eu_standard"
    UK_STANDARD = "uk_standard"
    APAC_STANDARD = "apac_standard"
    GERMAN_STANDARD = "german_standard"
    CANADIAN_STANDARD = "canadian_standard"

class Industry(Enum):
    TECHNOLOGY = "technology"
    FINANCE = "finance"
    CONSULTING = "consulting"
    HEALTHCARE = "healthcare"
    ENGINEERING = "engineering"
    MARKETING = "marketing"

@dataclass
class ResumeSection:
    title: str
    content: str
    order: int
    required: bool
    format_notes: List[str]

@dataclass
class LocalizedResume:
    format_type: ResumeFormat
    country: str
    industry: Industry
    sections: List[ResumeSection]
    formatting_guidelines: Dict[str, str]
    cultural_adaptations: List[str]
    keyword_optimizations: List[str]
    length_recommendation: str
    photo_requirement: Optional[str]

class ResumeLocalizer:
    def __init__(self):
        self.country_standards = self._load_country_standards()
        self.industry_keywords = self._load_industry_keywords()
        self.cultural_guidelines = self._load_cultural_guidelines()
    
    def _load_country_standards(self) -> Dict[str, Dict]:
        """Load resume standards by country"""
        return {
            "United States": {
                "format": ResumeFormat.US_STANDARD,
                "length": "1-2 pages",
                "photo": "Not recommended",
                "personal_info": "Minimal (no age, marital status)",
                "date_format": "MM/DD/YYYY",
                "sections_order": ["Contact", "Summary", "Experience", "Education", "Skills"],
                "required_sections": ["Contact", "Experience", "Education"],
                "optional_sections": ["Summary", "Skills", "Projects", "Certifications"],
                "formatting": {
                    "font": "Professional (Arial, Calibri, Times New Roman)",
                    "font_size": "10-12pt",
                    "margins": "0.5-1 inch",
                    "bullet_points": "Required for experience",
                    "colors": "Black text preferred, minimal color"
                },
                "cultural_notes": [
                    "Focus on achievements and quantifiable results",
                    "Use action verbs to start bullet points",
                    "Tailor to specific job descriptions",
                    "Include relevant keywords for ATS",
                    "No personal references unless requested"
                ]
            },
            "United Kingdom": {
                "format": ResumeFormat.UK_STANDARD,
                "length": "2 pages maximum",
                "photo": "Not recommended",
                "personal_info": "Minimal (no age, marital status)",
                "date_format": "DD/MM/YYYY",
                "sections_order": ["Personal Details", "Personal Statement", "Employment History", "Education", "Skills"],
                "required_sections": ["Personal Details", "Employment History", "Education"],
                "optional_sections": ["Personal Statement", "Skills", "Interests", "References"],
                "formatting": {
                    "font": "Professional fonts",
                    "font_size": "10-12pt",
                    "margins": "2.5cm",
                    "bullet_points": "Preferred for experience",
                    "colors": "Conservative, minimal color"
                },
                "cultural_notes": [
                    "Include brief personal statement",
                    "Use British English spelling",
                    "Focus on responsibilities and achievements",
                    "Include 'References available upon request'",
                    "Hobbies section acceptable if relevant"
                ]
            },
            "Germany": {
                "format": ResumeFormat.GERMAN_STANDARD,
                "length": "1-2 pages (Lebenslauf)",
                "photo": "Recommended (professional headshot)",
                "personal_info": "Comprehensive (age, marital status, nationality)",
                "date_format": "DD.MM.YYYY",
                "sections_order": ["Persönliche Daten", "Berufserfahrung", "Ausbildung", "Kenntnisse", "Sonstiges"],
                "required_sections": ["Persönliche Daten", "Berufserfahrung", "Ausbildung"],
                "optional_sections": ["Kenntnisse", "Sprachen", "Ehrenamtliche Tätigkeiten"],
                "formatting": {
                    "font": "Conservative fonts",
                    "font_size": "10-12pt",
                    "margins": "2.5cm",
                    "bullet_points": "Less common, paragraph format preferred",
                    "colors": "Very conservative, minimal color"
                },
                "cultural_notes": [
                    "Include professional photo",
                    "Reverse chronological order strongly preferred",
                    "Include detailed personal information",
                    "Very formal tone and structure",
                    "Hand-written signature may be expected"
                ]
            },
            "Canada": {
                "format": ResumeFormat.CANADIAN_STANDARD,
                "length": "1-2 pages",
                "photo": "Not recommended",
                "personal_info": "Minimal (similar to US)",
                "date_format": "MM/DD/YYYY or DD/MM/YYYY",
                "sections_order": ["Contact Information", "Professional Summary", "Work Experience", "Education", "Skills"],
                "required_sections": ["Contact Information", "Work Experience", "Education"],
                "optional_sections": ["Professional Summary", "Skills", "Certifications", "Languages"],
                "formatting": {
                    "font": "Professional fonts",
                    "font_size": "10-12pt", 
                    "margins": "1 inch",
                    "bullet_points": "Required for experience",
                    "colors": "Conservative use of color"
                },
                "cultural_notes": [
                    "Bilingual capabilities (English/French) valuable",
                    "Focus on achievements and metrics",
                    "Similar to US style but slightly more formal",
                    "Include relevant volunteer work",
                    "References available upon request"
                ]
            },
            "Japan": {
                "format": ResumeFormat.APAC_STANDARD,
                "length": "1-2 pages (Rirekisho format)",
                "photo": "Required (formal business photo)",
                "personal_info": "Very comprehensive (age, gender, family status)",
                "date_format": "Japanese era year format",
                "sections_order": ["基本情報", "学歴", "職歴", "資格", "志望動機"],
                "required_sections": ["基本情報", "学歴", "職歴"],
                "optional_sections": ["資格", "志望動機", "特技"],
                "formatting": {
                    "font": "MS Gothic or similar",
                    "font_size": "10-11pt",
                    "margins": "Standard A4",
                    "bullet_points": "Not common, paragraph format",
                    "colors": "Black and white only"
                },
                "cultural_notes": [
                    "Very formal and structured approach",
                    "Include formal business photo",
                    "Comprehensive personal details required",
                    "Hand-written versions may be preferred",
                    "Demonstrate long-term commitment intention"
                ]
            },
            "Singapore": {
                "format": ResumeFormat.APAC_STANDARD,
                "length": "2-3 pages acceptable",
                "photo": "Optional but common",
                "personal_info": "Moderate (nationality important for work pass)",
                "date_format": "DD/MM/YYYY",
                "sections_order": ["Personal Particulars", "Career Objective", "Work Experience", "Education", "Skills"],
                "required_sections": ["Personal Particulars", "Work Experience", "Education"],
                "optional_sections": ["Career Objective", "Skills", "Languages", "References"],
                "formatting": {
                    "font": "Professional fonts",
                    "font_size": "10-12pt",
                    "margins": "2.5cm",
                    "bullet_points": "Widely used",
                    "colors": "Professional use of color acceptable"
                },
                "cultural_notes": [
                    "Include nationality and work pass eligibility",
                    "Multicultural awareness valued",
                    "Language skills very important",
                    "International experience highlighted",
                    "Professional references preferred"
                ]
            }
        }
    
    def _load_industry_keywords(self) -> Dict[Industry, Dict[str, List[str]]]:
        """Load industry-specific keywords by country"""
        return {
            Industry.TECHNOLOGY: {
                "universal": ["software development", "programming", "agile", "cloud computing", "API"],
                "United States": ["full-stack", "DevOps", "machine learning", "scalability", "microservices"],
                "Germany": ["softwareentwicklung", "programmierung", "digitalisierung", "innovation"],
                "Singapore": ["fintech", "digital transformation", "emerging technologies", "innovation hub"],
                "Japan": ["digital transformation", "AI", "IoT", "robotics", "innovation"]
            },
            Industry.FINANCE: {
                "universal": ["financial analysis", "risk management", "portfolio management", "compliance"],
                "United States": ["investment banking", "private equity", "hedge funds", "derivatives"],
                "United Kingdom": ["financial services", "asset management", "regulatory compliance", "FSA"],
                "Germany": ["banken", "finanzdienstleistungen", "risikomanagement", "compliance"],
                "Singapore": ["wealth management", "private banking", "regulatory compliance", "MAS"]
            },
            Industry.CONSULTING: {
                "universal": ["strategy", "business analysis", "project management", "client management"],
                "United States": ["management consulting", "business transformation", "operational excellence"],
                "United Kingdom": ["business consulting", "change management", "process improvement"],
                "Germany": ["unternehmensberatung", "strategieberatung", "prozessoptimierung"],
                "Japan": ["business consulting", "kaizen", "process improvement", "corporate strategy"]
            }
        }
    
    def _load_cultural_guidelines(self) -> Dict[str, List[str]]:
        """Load cultural adaptation guidelines"""
        return {
            "United States": [
                "Emphasize individual achievements and quantifiable results",
                "Use confident, action-oriented language",
                "Highlight innovation and problem-solving abilities",
                "Include leadership experience and initiative",
                "Focus on value delivered to previous employers"
            ],
            "Germany": [
                "Demonstrate thoroughness and attention to detail",
                "Include comprehensive educational background",
                "Emphasize technical expertise and qualifications",
                "Show stability and long-term commitment",
                "Use formal, conservative language throughout"
            ],
            "Japan": [
                "Demonstrate respect for hierarchy and teamwork",
                "Show long-term career progression and stability",
                "Emphasize continuous learning and development",
                "Include any experience with Japanese companies/culture",
                "Use humble, respectful tone throughout"
            ],
            "United Kingdom": [
                "Balance confidence with modesty",
                "Include diverse experiences and well-roundedness",
                "Demonstrate cultural awareness and adaptability",
                "Show collaborative working style",
                "Use proper British English spelling and terminology"
            ]
        }
    
    def localize_resume(self, resume_content: str, target_country: str, 
                       target_industry: Industry, target_role: str) -> LocalizedResume:
        """Localize resume for specific country, industry, and role"""
        
        if target_country not in self.country_standards:
            raise ValueError(f"Country standards not available for {target_country}")
        
        standards = self.country_standards[target_country]
        
        # Extract and restructure sections
        sections = self._restructure_sections(resume_content, standards)
        
        # Apply cultural adaptations
        cultural_adaptations = self._apply_cultural_adaptations(
            resume_content, target_country, target_industry)
        
        # Optimize keywords
        keyword_optimizations = self._optimize_keywords(
            resume_content, target_country, target_industry, target_role)
        
        # Generate formatting guidelines
        formatting_guidelines = self._generate_formatting_guidelines(standards)
        
        return LocalizedResume(
            format_type=standards["format"],
            country=target_country,
            industry=target_industry,
            sections=sections,
            formatting_guidelines=formatting_guidelines,
            cultural_adaptations=cultural_adaptations,
            keyword_optimizations=keyword_optimizations,
            length_recommendation=standards["length"],
            photo_requirement=standards["photo"]
        )
    
    def _restructure_sections(self, resume_content: str, standards: Dict) -> List[ResumeSection]:
        """Restructure resume sections according to country standards"""
        sections = []
        section_order = standards["sections_order"]
        required_sections = standards["required_sections"]
        
        # Map common sections
        section_mapping = {
            "Contact": ["contact", "personal", "details"],
            "Summary": ["summary", "objective", "profile"],
            "Experience": ["experience", "work", "employment", "career"],
            "Education": ["education", "academic", "qualifications"],
            "Skills": ["skills", "competencies", "technical"],
            "Projects": ["projects", "portfolio"],
            "Certifications": ["certifications", "licenses"]
        }
        
        for i, section_name in enumerate(section_order):
            # Determine if section exists in resume
            section_content = self._extract_section_content(resume_content, section_name, section_mapping)
            
            is_required = section_name in required_sections
            format_notes = self._get_section_format_notes(section_name, standards)
            
            section = ResumeSection(
                title=section_name,
                content=section_content,
                order=i + 1,
                required=is_required,
                format_notes=format_notes
            )
            sections.append(section)
        
        return sections
    
    def _extract_section_content(self, resume_content: str, section_name: str, 
                                section_mapping: Dict) -> str:
        """Extract content for a specific section"""
        # This is a simplified version - in reality would use NLP to parse resume
        content_lines = resume_content.split('\n')
        section_content = []
        
        keywords = section_mapping.get(section_name, [section_name.lower()])
        in_section = False
        
        for line in content_lines:
            line_lower = line.lower()
            
            # Check if we're entering the section
            if any(keyword in line_lower for keyword in keywords):
                in_section = True
                continue
            
            # Check if we're leaving the section (next section starts)
            if in_section and line.strip() and line[0].isupper() and ':' in line:
                # Likely next section header
                for other_section, other_keywords in section_mapping.items():
                    if other_section != section_name and any(kw in line_lower for kw in other_keywords):
                        in_section = False
                        break
            
            if in_section and line.strip():
                section_content.append(line)
        
        return '\n'.join(section_content) if section_content else f"[Content for {section_name} section]"
    
    def _get_section_format_notes(self, section_name: str, standards: Dict) -> List[str]:
        """Get formatting notes for specific sections"""
        notes = []
        
        if section_name in ["Contact", "Personal Details", "Persönliche Daten"]:
            if standards["photo"] != "Not recommended":
                notes.append("Include professional photo")
            if standards["personal_info"] == "Comprehensive":
                notes.append("Include age, marital status, nationality")
            notes.append(f"Use date format: {standards['date_format']}")
        
        elif section_name in ["Experience", "Work Experience", "Employment History"]:
            if standards["formatting"]["bullet_points"] == "Required for experience":
                notes.append("Use bullet points for achievements")
            elif standards["formatting"]["bullet_points"] == "Less common":
                notes.append("Use paragraph format instead of bullets")
            notes.append("Include quantifiable achievements")
        
        elif section_name in ["Education", "Ausbildung"]:
            notes.append("List in reverse chronological order")
            if standards["country"] == "Germany":
                notes.append("Include detailed academic records")
        
        return notes
    
    def _apply_cultural_adaptations(self, resume_content: str, target_country: str,
                                  target_industry: Industry) -> List[str]:
        """Apply cultural adaptations for the target country"""
        adaptations = []
        guidelines = self.cultural_guidelines.get(target_country, [])
        
        for guideline in guidelines:
            adaptation = self._generate_specific_adaptation(guideline, resume_content, target_industry)
            if adaptation:
                adaptations.append(adaptation)
        
        # Add country-specific adaptations
        if target_country == "Germany":
            adaptations.extend([
                "Replace casual language with formal German business terminology",
                "Emphasize educational credentials and certifications",
                "Include detailed company information and roles"
            ])
        elif target_country == "Japan":
            adaptations.extend([
                "Demonstrate cultural sensitivity and respect for hierarchy",
                "Include any Japanese language skills or cultural training",
                "Emphasize team collaboration over individual achievements"
            ])
        elif target_country == "United States":
            adaptations.extend([
                "Quantify all achievements with specific numbers and percentages",
                "Use strong action verbs to begin all bullet points",
                "Tailor content specifically to job description keywords"
            ])
        
        return adaptations
    
    def _generate_specific_adaptation(self, guideline: str, resume_content: str,
                                    industry: Industry) -> Optional[str]:
        """Generate specific adaptation based on guideline and content"""
        if "quantifiable results" in guideline:
            return "Add specific metrics: increased sales by X%, reduced costs by $Y, managed team of Z people"
        elif "technical expertise" in guideline:
            return "List specific certifications, software proficiencies, and technical qualifications"
        elif "teamwork" in guideline:
            return "Reframe individual achievements to highlight team collaboration and group success"
        elif "formal" in guideline:
            return "Replace informal language with professional, business-appropriate terminology"
        
        return None
    
    def _optimize_keywords(self, resume_content: str, target_country: str,
                          target_industry: Industry, target_role: str) -> List[str]:
        """Optimize keywords for country, industry, and role"""
        optimizations = []
        
        # Get industry keywords
        industry_keywords = self.industry_keywords.get(target_industry, {})
        universal_keywords = industry_keywords.get("universal", [])
        country_keywords = industry_keywords.get(target_country, [])
        
        # Role-specific keywords
        role_keywords = self._extract_role_keywords(target_role)
        
        # Generate optimization suggestions
        all_keywords = universal_keywords + country_keywords + role_keywords
        
        for keyword in all_keywords[:10]:  # Top 10 most relevant
            if keyword.lower() not in resume_content.lower():
                optimizations.append(f"Consider adding '{keyword}' if relevant to your experience")
        
        # Country-specific optimizations
        if target_country == "Germany" and target_industry == Industry.TECHNOLOGY:
            optimizations.append("Include German technical terms where appropriate")
        elif target_country == "Singapore":
            optimizations.append("Emphasize multicultural and international experience")
        elif target_country == "Japan":
            optimizations.append("Highlight any experience with Japanese companies or methodologies")
        
        return optimizations
    
    def _extract_role_keywords(self, target_role: str) -> List[str]:
        """Extract relevant keywords from target role"""
        role_lower = target_role.lower()
        keywords = []
        
        # Common role keywords
        role_mappings = {
            "software engineer": ["programming", "coding", "development", "algorithms", "debugging"],
            "product manager": ["product strategy", "roadmap", "stakeholder management", "user research"],
            "data scientist": ["machine learning", "statistics", "data analysis", "python", "SQL"],
            "marketing manager": ["campaign management", "brand strategy", "digital marketing", "analytics"],
            "sales manager": ["sales strategy", "customer acquisition", "revenue growth", "CRM"]
        }
        
        for role_key, role_keywords in role_mappings.items():
            if role_key in role_lower:
                keywords.extend(role_keywords)
        
        return keywords
    
    def _generate_formatting_guidelines(self, standards: Dict) -> Dict[str, str]:
        """Generate detailed formatting guidelines"""
        formatting = standards["formatting"]
        
        guidelines = {
            "Font": formatting["font"],
            "Font Size": formatting["font_size"],
            "Margins": formatting["margins"],
            "Length": standards["length"],
            "Date Format": standards["date_format"],
            "Bullet Points": formatting["bullet_points"],
            "Colors": formatting["colors"]
        }
        
        if standards["photo"] != "Not recommended":
            guidelines["Photo"] = f"{standards['photo']} - {self._get_photo_guidelines(standards)}"
        
        return guidelines
    
    def _get_photo_guidelines(self, standards: Dict) -> str:
        """Get photo guidelines for countries that require them"""
        if standards["format"] == ResumeFormat.GERMAN_STANDARD:
            return "Professional headshot, business attire, neutral background, 4x5cm size"
        elif standards["format"] == ResumeFormat.APAC_STANDARD:
            return "Formal business photo, professional attire, clear quality"
        else:
            return "Professional photo if required"
    
    def get_localization_checklist(self, target_country: str) -> List[Dict[str, str]]:
        """Get a checklist for resume localization"""
        checklist = [
            {"item": "Review length requirements", "description": f"Ensure resume meets {target_country} length standards"},
            {"item": "Check photo requirements", "description": "Add or remove photo as appropriate"},
            {"item": "Verify personal information", "description": "Include appropriate level of personal details"},
            {"item": "Update date format", "description": "Use correct date format for country"},
            {"item": "Optimize keywords", "description": "Include relevant industry and country keywords"},
            {"item": "Cultural tone adjustment", "description": "Adjust language tone for cultural appropriateness"},
            {"item": "Section restructuring", "description": "Reorder sections according to country preferences"},
            {"item": "Language localization", "description": "Use appropriate terminology and spelling"}
        ]
        
        # Add country-specific checklist items
        if target_country == "Germany":
            checklist.extend([
                {"item": "Add formal signature", "description": "Include handwritten signature if submitting physically"},
                {"item": "Include detailed education", "description": "List all educational qualifications comprehensively"}
            ])
        elif target_country == "United States":
            checklist.extend([
                {"item": "Remove personal information", "description": "Remove age, marital status, and photo"},
                {"item": "Quantify achievements", "description": "Add specific numbers and percentages to all accomplishments"}
            ])
        
        return checklist

# Global instance
resume_localizer = ResumeLocalizer()