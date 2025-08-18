"""
Global Benefits Comparison Engine
Compare healthcare, retirement, and social benefits across countries with total compensation analysis
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class BenefitCategory(Enum):
    HEALTHCARE = "healthcare"
    RETIREMENT = "retirement"
    SOCIAL_SECURITY = "social_security"
    FAMILY_SUPPORT = "family_support"
    VACATION_LEAVE = "vacation_leave"
    PROFESSIONAL_DEVELOPMENT = "professional_development"

class CoverageLevel(Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    MODERATE = "moderate"
    BASIC = "basic"
    MINIMAL = "minimal"

@dataclass
class BenefitDetail:
    category: BenefitCategory
    coverage_level: CoverageLevel
    annual_value: float  # Estimated annual value in USD
    employer_contribution: float  # Percentage paid by employer
    employee_contribution: float  # Percentage paid by employee
    waiting_period: Optional[str]
    key_features: List[str]
    limitations: List[str]

@dataclass
class CountryBenefits:
    country: str
    healthcare: BenefitDetail
    retirement: BenefitDetail
    social_security: BenefitDetail
    family_support: BenefitDetail
    vacation_leave: BenefitDetail
    professional_development: BenefitDetail
    total_annual_value: float
    quality_of_life_index: float
    work_life_balance_score: float

@dataclass
class BenefitsComparison:
    countries: List[str]
    salary_level: str
    family_situation: str
    benefits_breakdown: List[CountryBenefits]
    key_differences: Dict[str, List[str]]
    recommendations: List[str]
    total_compensation_analysis: Dict[str, float]
    long_term_projections: Dict[str, Dict[str, float]]

class GlobalBenefitsComparison:
    def __init__(self):
        self.benefits_data = self._load_benefits_data()
        self.quality_metrics = self._load_quality_metrics()
        self.exchange_rates = self._load_exchange_rates()
    
    def _load_benefits_data(self) -> Dict[str, Dict]:
        """Load comprehensive benefits data by country"""
        return {
            "Germany": {
                "healthcare": {
                    "coverage_level": CoverageLevel.EXCELLENT,
                    "annual_value": 6500,
                    "employer_contribution": 7.3,
                    "employee_contribution": 7.3,
                    "waiting_period": "None",
                    "key_features": [
                        "Universal coverage for all residents",
                        "Comprehensive medical, dental, and mental health",
                        "Prescription drug coverage",
                        "Rehabilitation and long-term care",
                        "Sick leave compensation (up to 78 weeks)"
                    ],
                    "limitations": [
                        "Some specialists may have waiting periods",
                        "Dental coverage basic for adults"
                    ]
                },
                "retirement": {
                    "coverage_level": CoverageLevel.EXCELLENT,
                    "annual_value": 8200,
                    "employer_contribution": 9.3,
                    "employee_contribution": 9.3,
                    "waiting_period": "5 years vesting",
                    "key_features": [
                        "Statutory pension scheme",
                        "Occupational pension (Betriebsrente)",
                        "Private pension (Riester/Rürup) with tax benefits",
                        "Early retirement options",
                        "Survivor benefits"
                    ],
                    "limitations": [
                        "Pension level depends on contribution years",
                        "Early retirement reduces benefits"
                    ]
                },
                "social_security": {
                    "coverage_level": CoverageLevel.EXCELLENT,
                    "annual_value": 4500,
                    "employer_contribution": 2.6,
                    "employee_contribution": 2.6,
                    "waiting_period": "None",
                    "key_features": [
                        "Unemployment insurance (12-24 months)",
                        "Job training and placement services",
                        "Disability insurance",
                        "Long-term care insurance"
                    ],
                    "limitations": [
                        "Unemployment benefits decrease over time",
                        "Strict job search requirements"
                    ]
                },
                "family_support": {
                    "coverage_level": CoverageLevel.EXCELLENT,
                    "annual_value": 5800,
                    "employer_contribution": 0,
                    "employee_contribution": 0,
                    "waiting_period": "None",
                    "key_features": [
                        "Child benefit (€250/month per child)",
                        "Parental leave (14 months paid)",
                        "Childcare support and subsidies",
                        "Free education including university",
                        "Family tax benefits"
                    ],
                    "limitations": [
                        "Childcare availability varies by region",
                        "University may require local language"
                    ]
                },
                "vacation_leave": {
                    "coverage_level": CoverageLevel.EXCELLENT,
                    "annual_value": 3200,
                    "employer_contribution": 100,
                    "employee_contribution": 0,
                    "waiting_period": "6 months",
                    "key_features": [
                        "Minimum 20 days annual leave",
                        "Typical 25-30 days in practice",
                        "Public holidays (9-13 per year)",
                        "Sick leave separate from vacation",
                        "Vacation pay protection"
                    ],
                    "limitations": [
                        "Must take minimum vacation time",
                        "Advance planning required"
                    ]
                },
                "professional_development": {
                    "coverage_level": CoverageLevel.GOOD,
                    "annual_value": 2500,
                    "employer_contribution": 80,
                    "employee_contribution": 20,
                    "waiting_period": "1 year",
                    "key_features": [
                        "Training and education support",
                        "Professional certification funding",
                        "Career development programs",
                        "Language learning support"
                    ],
                    "limitations": [
                        "Employer discretion on funding",
                        "May require commitment periods"
                    ]
                }
            },
            "United States": {
                "healthcare": {
                    "coverage_level": CoverageLevel.MODERATE,
                    "annual_value": 8500,
                    "employer_contribution": 70,
                    "employee_contribution": 30,
                    "waiting_period": "30-90 days",
                    "key_features": [
                        "Employer-sponsored health insurance",
                        "Medical, dental, vision options",
                        "Health Savings Account (HSA) option",
                        "Prescription drug coverage",
                        "Preventive care coverage"
                    ],
                    "limitations": [
                        "High deductibles and co-pays common",
                        "Network restrictions",
                        "Coverage varies significantly by employer",
                        "Pre-existing condition limitations"
                    ]
                },
                "retirement": {
                    "coverage_level": CoverageLevel.MODERATE,
                    "annual_value": 7800,
                    "employer_contribution": 50,
                    "employee_contribution": 50,
                    "waiting_period": "1 year typical",
                    "key_features": [
                        "401(k) with employer matching",
                        "Social Security benefits",
                        "Individual Retirement Accounts (IRA)",
                        "Some pension plans remaining",
                        "Roth IRA tax advantages"
                    ],
                    "limitations": [
                        "401(k) depends on employee contributions",
                        "Social Security provides basic income only",
                        "Vesting schedules vary",
                        "Limited employer matching"
                    ]
                },
                "social_security": {
                    "coverage_level": CoverageLevel.BASIC,
                    "annual_value": 2800,
                    "employer_contribution": 50,
                    "employee_contribution": 50,
                    "waiting_period": "None",
                    "key_features": [
                        "Social Security disability",
                        "Unemployment insurance (state-based)",
                        "Workers' compensation",
                        "Medicare (age 65+)"
                    ],
                    "limitations": [
                        "Unemployment benefits limited duration",
                        "Low replacement income ratios",
                        "Means testing for some benefits"
                    ]
                },
                "family_support": {
                    "coverage_level": CoverageLevel.BASIC,
                    "annual_value": 1200,
                    "employer_contribution": 0,
                    "employee_contribution": 0,
                    "waiting_period": "Varies",
                    "key_features": [
                        "Family and Medical Leave Act (unpaid)",
                        "Child tax credits",
                        "Some state family leave programs",
                        "Dependent care assistance"
                    ],
                    "limitations": [
                        "No federal paid parental leave",
                        "FMLA is unpaid leave only",
                        "Benefits vary significantly by state",
                        "Limited childcare support"
                    ]
                },
                "vacation_leave": {
                    "coverage_level": CoverageLevel.BASIC,
                    "annual_value": 2000,
                    "employer_contribution": 100,
                    "employee_contribution": 0,
                    "waiting_period": "Varies",
                    "key_features": [
                        "Employer discretion (typically 10-20 days)",
                        "Federal holidays (10 per year)",
                        "Sick leave policies vary",
                        "PTO (Paid Time Off) common"
                    ],
                    "limitations": [
                        "No legal minimum vacation requirement",
                        "\"Use it or lose it\" policies common",
                        "Limited vacation time compared to other countries"
                    ]
                },
                "professional_development": {
                    "coverage_level": CoverageLevel.GOOD,
                    "annual_value": 3000,
                    "employer_contribution": 90,
                    "employee_contribution": 10,
                    "waiting_period": "Varies",
                    "key_features": [
                        "Tuition reimbursement programs",
                        "Professional certification support",
                        "Conference and training funding",
                        "Mentorship programs"
                    ],
                    "limitations": [
                        "Varies significantly by employer",
                        "May require repayment if leaving company",
                        "Budget limitations"
                    ]
                }
            },
            "Singapore": {
                "healthcare": {
                    "coverage_level": CoverageLevel.EXCELLENT,
                    "annual_value": 3500,
                    "employer_contribution": 60,
                    "employee_contribution": 40,
                    "waiting_period": "None",
                    "key_features": [
                        "Medisave (mandatory health savings)",
                        "Medishield (basic insurance)",
                        "Employer group insurance",
                        "World-class healthcare facilities",
                        "Preventive care emphasis"
                    ],
                    "limitations": [
                        "High out-of-pocket costs for premium care",
                        "Foreign worker levy for some procedures"
                    ]
                },
                "retirement": {
                    "coverage_level": CoverageLevel.EXCELLENT,
                    "annual_value": 9500,
                    "employer_contribution": 17,
                    "employee_contribution": 20,
                    "waiting_period": "None",
                    "key_features": [
                        "Central Provident Fund (CPF)",
                        "Mandatory savings for retirement",
                        "Housing and healthcare accounts",
                        "Employer contributions",
                        "Investment options within CPF"
                    ],
                    "limitations": [
                        "Withdrawal restrictions until retirement age",
                        "Currency risk for expatriates",
                        "Complex withdrawal rules"
                    ]
                },
                "social_security": {
                    "coverage_level": CoverageLevel.MODERATE,
                    "annual_value": 1800,
                    "employer_contribution": 0,
                    "employee_contribution": 0,
                    "waiting_period": "None",
                    "key_features": [
                        "Work injury compensation",
                        "Foreign worker protection",
                        "Employment protection schemes",
                        "Skills development programs"
                    ],
                    "limitations": [
                        "Limited unemployment benefits",
                        "Benefits mainly for citizens/PR"
                    ]
                },
                "family_support": {
                    "coverage_level": CoverageLevel.GOOD,
                    "annual_value": 2800,
                    "employer_contribution": 100,
                    "employee_contribution": 0,
                    "waiting_period": "None",
                    "key_features": [
                        "Maternity/paternity leave (16 weeks)",
                        "Childcare subsidies",
                        "Baby bonus schemes",
                        "Education savings schemes",
                        "Tax relief for children"
                    ],
                    "limitations": [
                        "Benefits primarily for citizens",
                        "Childcare costs still high",
                        "Work permit restrictions for spouses"
                    ]
                },
                "vacation_leave": {
                    "coverage_level": CoverageLevel.GOOD,
                    "annual_value": 2200,
                    "employer_contribution": 100,
                    "employee_contribution": 0,
                    "waiting_period": "3 months",
                    "key_features": [
                        "Minimum 7 days annual leave",
                        "Additional days based on service",
                        "Public holidays (11 per year)",
                        "Sick leave entitlements",
                        "Flexible work arrangements"
                    ],
                    "limitations": [
                        "Lower minimum compared to Europe",
                        "High work intensity culture"
                    ]
                },
                "professional_development": {
                    "coverage_level": CoverageLevel.EXCELLENT,
                    "annual_value": 4000,
                    "employer_contribution": 75,
                    "employee_contribution": 25,
                    "waiting_period": "None",
                    "key_features": [
                        "SkillsFuture credits for all citizens",
                        "Workforce development programs",
                        "Government co-funding for training",
                        "Professional certification support",
                        "Career guidance services"
                    ],
                    "limitations": [
                        "Some programs for citizens only",
                        "Industry-specific limitations"
                    ]
                }
            },
            "United Kingdom": {
                "healthcare": {
                    "coverage_level": CoverageLevel.EXCELLENT,
                    "annual_value": 4200,
                    "employer_contribution": 0,
                    "employee_contribution": 0,
                    "waiting_period": "None for emergency, 6 months for non-urgent",
                    "key_features": [
                        "National Health Service (NHS) - free at point of use",
                        "Comprehensive medical coverage",
                        "Prescription drug coverage",
                        "Mental health services",
                        "Emergency care for all"
                    ],
                    "limitations": [
                        "Waiting times for non-urgent procedures",
                        "Limited dental and optical coverage",
                        "Private insurance common for faster access"
                    ]
                },
                "retirement": {
                    "coverage_level": CoverageLevel.GOOD,
                    "annual_value": 6800,
                    "employer_contribution": 3,
                    "employee_contribution": 5,
                    "waiting_period": "Auto-enrollment after 3 months",
                    "key_features": [
                        "State pension for all residents",
                        "Workplace pension auto-enrollment",
                        "Personal pension options",
                        "Tax relief on contributions",
                        "Protected minimum pension amount"
                    ],
                    "limitations": [
                        "State pension provides basic income only",
                        "Full state pension requires 35 years contributions",
                        "Workplace pension depends on employer"
                    ]
                },
                "social_security": {
                    "coverage_level": CoverageLevel.GOOD,
                    "annual_value": 3200,
                    "employer_contribution": 0,
                    "employee_contribution": 0,
                    "waiting_period": "Varies by benefit",
                    "key_features": [
                        "Universal Credit system",
                        "Jobseeker's Allowance",
                        "Employment and Support Allowance",
                        "Disability benefits",
                        "Housing benefit"
                    ],
                    "limitations": [
                        "Means-tested benefits",
                        "Strict eligibility requirements",
                        "Benefit cap limitations"
                    ]
                },
                "family_support": {
                    "coverage_level": CoverageLevel.EXCELLENT,
                    "annual_value": 4500,
                    "employer_contribution": 0,
                    "employee_contribution": 0,
                    "waiting_period": "None",
                    "key_features": [
                        "Child benefit for all children",
                        "Statutory maternity/paternity pay",
                        "Shared parental leave",
                        "Free childcare hours (30 hours/week)",
                        "Free education including university for EU students"
                    ],
                    "limitations": [
                        "University fees for non-EU students",
                        "Childcare costs high before free hours",
                        "Income thresholds for some benefits"
                    ]
                },
                "vacation_leave": {
                    "coverage_level": CoverageLevel.EXCELLENT,
                    "annual_value": 2800,
                    "employer_contribution": 100,
                    "employee_contribution": 0,
                    "waiting_period": "Accrued from start date",
                    "key_features": [
                        "Minimum 28 days annual leave (including public holidays)",
                        "Public holidays (8 per year)",
                        "Statutory sick pay",
                        "Flexible working rights",
                        "Enhanced leave policies common"
                    ],
                    "limitations": [
                        "Includes public holidays in minimum",
                        "Sick pay limited amount and duration"
                    ]
                },
                "professional_development": {
                    "coverage_level": CoverageLevel.GOOD,
                    "annual_value": 2800,
                    "employer_contribution": 80,
                    "employee_contribution": 20,
                    "waiting_period": "Varies",
                    "key_features": [
                        "Apprenticeship levy funding",
                        "Professional development programs",
                        "Government skills initiatives",
                        "Industry certification support",
                        "Career guidance services"
                    ],
                    "limitations": [
                        "Funding depends on employer size",
                        "Limited individual training accounts",
                        "Sector-specific variations"
                    ]
                }
            }
        }
    
    def _load_quality_metrics(self) -> Dict[str, Dict[str, float]]:
        """Load quality of life and work-life balance metrics"""
        return {
            "Germany": {
                "quality_of_life_index": 8.2,
                "work_life_balance_score": 8.8,
                "social_progress_index": 8.6,
                "happiness_index": 7.5
            },
            "United States": {
                "quality_of_life_index": 7.8,
                "work_life_balance_score": 6.5,
                "social_progress_index": 7.9,
                "happiness_index": 7.0
            },
            "Singapore": {
                "quality_of_life_index": 8.0,
                "work_life_balance_score": 6.8,
                "social_progress_index": 8.3,
                "happiness_index": 6.8
            },
            "United Kingdom": {
                "quality_of_life_index": 7.9,
                "work_life_balance_score": 7.8,
                "social_progress_index": 8.4,
                "happiness_index": 7.2
            }
        }
    
    def _load_exchange_rates(self) -> Dict[str, float]:
        """Load exchange rates to USD for value calculations"""
        return {
            "EUR": 1.08,
            "GBP": 1.27,
            "SGD": 0.74,
            "USD": 1.0
        }
    
    def compare_benefits(self, countries: List[str], salary_usd: float,
                        family_situation: str, priorities: List[str]) -> BenefitsComparison:
        """Compare benefits across multiple countries"""
        
        benefits_breakdown = []
        
        for country in countries:
            if country in self.benefits_data:
                country_benefits = self._create_country_benefits(country, salary_usd, family_situation)
                benefits_breakdown.append(country_benefits)
        
        # Generate key differences
        key_differences = self._identify_key_differences(benefits_breakdown)
        
        # Create recommendations
        recommendations = self._generate_recommendations(benefits_breakdown, priorities, family_situation)
        
        # Total compensation analysis
        total_comp_analysis = self._analyze_total_compensation(benefits_breakdown, salary_usd)
        
        # Long-term projections
        long_term_proj = self._calculate_long_term_projections(benefits_breakdown, salary_usd)
        
        return BenefitsComparison(
            countries=countries,
            salary_level=self._categorize_salary(salary_usd),
            family_situation=family_situation,
            benefits_breakdown=benefits_breakdown,
            key_differences=key_differences,
            recommendations=recommendations,
            total_compensation_analysis=total_comp_analysis,
            long_term_projections=long_term_proj
        )
    
    def _create_country_benefits(self, country: str, salary: float, family_situation: str) -> CountryBenefits:
        """Create benefits breakdown for a specific country"""
        data = self.benefits_data[country]
        quality_metrics = self.quality_metrics[country]
        
        # Create benefit details for each category
        healthcare = self._create_benefit_detail(BenefitCategory.HEALTHCARE, data["healthcare"], salary)
        retirement = self._create_benefit_detail(BenefitCategory.RETIREMENT, data["retirement"], salary)
        social_security = self._create_benefit_detail(BenefitCategory.SOCIAL_SECURITY, data["social_security"], salary)
        family_support = self._create_benefit_detail(BenefitCategory.FAMILY_SUPPORT, data["family_support"], salary)
        vacation_leave = self._create_benefit_detail(BenefitCategory.VACATION_LEAVE, data["vacation_leave"], salary)
        professional_dev = self._create_benefit_detail(BenefitCategory.PROFESSIONAL_DEVELOPMENT, data["professional_development"], salary)
        
        # Calculate total annual value
        total_value = sum([
            healthcare.annual_value,
            retirement.annual_value,
            social_security.annual_value,
            family_support.annual_value if "children" in family_situation.lower() else 0,
            vacation_leave.annual_value,
            professional_dev.annual_value
        ])
        
        return CountryBenefits(
            country=country,
            healthcare=healthcare,
            retirement=retirement,
            social_security=social_security,
            family_support=family_support,
            vacation_leave=vacation_leave,
            professional_development=professional_dev,
            total_annual_value=total_value,
            quality_of_life_index=quality_metrics["quality_of_life_index"],
            work_life_balance_score=quality_metrics["work_life_balance_score"]
        )
    
    def _create_benefit_detail(self, category: BenefitCategory, data: Dict, salary: float) -> BenefitDetail:
        """Create benefit detail from raw data"""
        return BenefitDetail(
            category=category,
            coverage_level=data["coverage_level"],
            annual_value=data["annual_value"],
            employer_contribution=data["employer_contribution"],
            employee_contribution=data["employee_contribution"],
            waiting_period=data.get("waiting_period"),
            key_features=data["key_features"],
            limitations=data["limitations"]
        )
    
    def _categorize_salary(self, salary: float) -> str:
        """Categorize salary level"""
        if salary < 50000:
            return "Entry Level"
        elif salary < 100000:
            return "Mid Level"
        elif salary < 200000:
            return "Senior Level"
        else:
            return "Executive Level"
    
    def _identify_key_differences(self, benefits: List[CountryBenefits]) -> Dict[str, List[str]]:
        """Identify key differences between countries"""
        differences = {
            "Healthcare": [],
            "Retirement": [],
            "Family Support": [],
            "Work-Life Balance": []
        }
        
        # Healthcare differences
        healthcare_levels = [(b.country, b.healthcare.coverage_level) for b in benefits]
        if len(set(level for _, level in healthcare_levels)) > 1:
            for country, level in healthcare_levels:
                differences["Healthcare"].append(f"{country}: {level.value} coverage")
        
        # Retirement contribution differences
        for benefit in benefits:
            total_retirement = benefit.retirement.employer_contribution + benefit.retirement.employee_contribution
            differences["Retirement"].append(f"{benefit.country}: {total_retirement}% total contributions")
        
        # Family support differences
        family_values = [(b.country, b.family_support.annual_value) for b in benefits]
        family_values.sort(key=lambda x: x[1], reverse=True)
        for country, value in family_values:
            differences["Family Support"].append(f"{country}: ${value:,.0f} annual value")
        
        # Work-life balance
        for benefit in benefits:
            differences["Work-Life Balance"].append(
                f"{benefit.country}: {benefit.work_life_balance_score}/10 score, "
                f"{benefit.vacation_leave.annual_value/160:.0f} vacation days equivalent"
            )
        
        return differences
    
    def _generate_recommendations(self, benefits: List[CountryBenefits], 
                                priorities: List[str], family_situation: str) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Find best healthcare
        best_healthcare = max(benefits, key=lambda x: x.healthcare.annual_value)
        recommendations.append(f"Best healthcare value: {best_healthcare.country} "
                             f"(${best_healthcare.healthcare.annual_value:,.0f} annual value)")
        
        # Find best retirement benefits
        best_retirement = max(benefits, key=lambda x: x.retirement.annual_value)
        recommendations.append(f"Best retirement benefits: {best_retirement.country} "
                             f"(${best_retirement.retirement.annual_value:,.0f} annual value)")
        
        # Family-specific recommendations
        if "children" in family_situation.lower():
            best_family = max(benefits, key=lambda x: x.family_support.annual_value)
            recommendations.append(f"Best for families: {best_family.country} "
                                 f"(${best_family.family_support.annual_value:,.0f} family support)")
        
        # Work-life balance
        if "work_life_balance" in priorities:
            best_balance = max(benefits, key=lambda x: x.work_life_balance_score)
            recommendations.append(f"Best work-life balance: {best_balance.country} "
                                 f"({best_balance.work_life_balance_score}/10 score)")
        
        # Total value recommendation
        best_total = max(benefits, key=lambda x: x.total_annual_value)
        recommendations.append(f"Highest total benefits value: {best_total.country} "
                             f"(${best_total.total_annual_value:,.0f} annual)")
        
        return recommendations
    
    def _analyze_total_compensation(self, benefits: List[CountryBenefits], 
                                  base_salary: float) -> Dict[str, float]:
        """Analyze total compensation including benefits"""
        total_comp = {}
        
        for benefit in benefits:
            total_compensation = base_salary + benefit.total_annual_value
            total_comp[benefit.country] = total_compensation
        
        return total_comp
    
    def _calculate_long_term_projections(self, benefits: List[CountryBenefits], 
                                       salary: float) -> Dict[str, Dict[str, float]]:
        """Calculate 10-year and 30-year benefit projections"""
        projections = {}
        
        for benefit in benefits:
            # 10-year projection
            ten_year_benefits = benefit.total_annual_value * 10
            ten_year_retirement = benefit.retirement.annual_value * 10 * 1.05  # Assume 5% growth
            
            # 30-year projection (retirement focus)
            thirty_year_retirement = benefit.retirement.annual_value * 30 * 1.07  # Assume 7% growth
            thirty_year_healthcare = benefit.healthcare.annual_value * 30 * 1.04  # Assume 4% growth
            
            projections[benefit.country] = {
                "10_year_total_benefits": ten_year_benefits,
                "10_year_retirement_value": ten_year_retirement,
                "30_year_retirement_value": thirty_year_retirement,
                "30_year_healthcare_value": thirty_year_healthcare,
                "lifetime_value_estimate": thirty_year_retirement + thirty_year_healthcare
            }
        
        return projections

# Global instance
benefits_comparator = GlobalBenefitsComparison()