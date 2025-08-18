"""
International Tax Optimizer
Compare tax implications of working in different countries
Calculate take-home pay after taxes, social security, and mandatory contributions
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum

class TaxResidency(Enum):
    RESIDENT = "resident"
    NON_RESIDENT = "non_resident"
    TEMPORARY_RESIDENT = "temporary_resident"

class DeductionType(Enum):
    STANDARD = "standard"
    ITEMIZED = "itemized"
    PROFESSIONAL = "professional"

@dataclass
class TaxBracket:
    min_income: float
    max_income: float
    rate: float

@dataclass
class TaxCalculation:
    country: str
    gross_salary: float
    currency: str
    income_tax: float
    social_security: float
    mandatory_contributions: float
    net_salary: float
    effective_tax_rate: float
    marginal_tax_rate: float
    deductions_applied: Dict[str, float]
    take_home_monthly: float
    tax_residency: TaxResidency

@dataclass
class TaxComparison:
    base_country: str
    comparison_countries: List[str]
    calculations: List[TaxCalculation]
    recommendations: List[str]
    treaty_benefits: Dict[str, List[str]]
    optimal_structures: List[Dict]

class InternationalTaxOptimizer:
    def __init__(self):
        self.tax_systems = self._load_tax_systems()
        self.treaty_networks = self._load_treaty_networks()
        self.exchange_rates = self._load_exchange_rates()
        self.social_security_rates = self._load_social_security_rates()
    
    def _load_tax_systems(self) -> Dict[str, Dict]:
        """Load tax system data for different countries"""
        return {
            "United States": {
                "currency": "USD",
                "tax_brackets": [
                    TaxBracket(0, 11000, 0.10),
                    TaxBracket(11001, 44725, 0.12),
                    TaxBracket(44726, 95375, 0.22),
                    TaxBracket(95376, 182050, 0.24),
                    TaxBracket(182051, 231250, 0.32),
                    TaxBracket(231251, 578125, 0.35),
                    TaxBracket(578126, float('inf'), 0.37)
                ],
                "standard_deduction": 13850,
                "state_tax_avg": 0.05,  # Average state tax
                "payroll_tax": 0.0765,  # Social Security + Medicare
                "residency_threshold_days": 183,
                "special_deductions": {
                    "401k_max": 22500,
                    "health_insurance": 0,  # Often pre-tax
                    "foreign_earned_income_exclusion": 120000
                }
            },
            "United Kingdom": {
                "currency": "GBP",
                "tax_brackets": [
                    TaxBracket(0, 12570, 0.0),
                    TaxBracket(12571, 50270, 0.20),
                    TaxBracket(50271, 125140, 0.40),
                    TaxBracket(125141, float('inf'), 0.45)
                ],
                "national_insurance": {
                    "employee_rate": 0.12,
                    "threshold": 12570
                },
                "pension_contribution": 0.08,  # Auto-enrollment
                "residency_threshold_days": 183,
                "special_deductions": {
                    "pension_annual_allowance": 40000,
                    "isa_allowance": 20000
                }
            },
            "Germany": {
                "currency": "EUR", 
                "tax_brackets": [
                    TaxBracket(0, 10908, 0.0),
                    TaxBracket(10909, 62809, 0.14),  # Progressive from 14% to 42%
                    TaxBracket(62810, 277825, 0.42),
                    TaxBracket(277826, float('inf'), 0.45)
                ],
                "social_security_rate": 0.195,  # Employee portion
                "solidarity_surcharge": 0.055,  # 5.5% on income tax
                "church_tax": 0.08,  # Optional, 8-9% of income tax
                "residency_threshold_days": 183,
                "special_deductions": {
                    "basic_allowance": 10908,
                    "work_related_expenses": 1230,
                    "riester_pension": 2100
                }
            },
            "Canada": {
                "currency": "CAD",
                "federal_brackets": [
                    TaxBracket(0, 53359, 0.15),
                    TaxBracket(53360, 106717, 0.205),
                    TaxBracket(106718, 165430, 0.26),
                    TaxBracket(165431, 235675, 0.29),
                    TaxBracket(235676, float('inf'), 0.33)
                ],
                "provincial_tax_avg": 0.10,  # Average across provinces
                "cpp_rate": 0.0595,  # Canada Pension Plan
                "ei_rate": 0.0229,   # Employment Insurance
                "residency_threshold_days": 183,
                "special_deductions": {
                    "rrsp_limit": 30780,
                    "basic_personal_amount": 15000,
                    "tfsa_limit": 6500
                }
            },
            "Australia": {
                "currency": "AUD",
                "tax_brackets": [
                    TaxBracket(0, 18200, 0.0),
                    TaxBracket(18201, 45000, 0.19),
                    TaxBracket(45001, 120000, 0.325),
                    TaxBracket(120001, 180000, 0.37),
                    TaxBracket(180001, float('inf'), 0.45)
                ],
                "medicare_levy": 0.02,
                "superannuation": 0.105,  # Employer contribution
                "residency_threshold_days": 183,
                "special_deductions": {
                    "concessional_super": 27500,
                    "work_related_deductions": 3000
                }
            },
            "Singapore": {
                "currency": "SGD",
                "tax_brackets": [
                    TaxBracket(0, 20000, 0.0),
                    TaxBracket(20001, 30000, 0.02),
                    TaxBracket(30001, 40000, 0.035),
                    TaxBracket(40001, 80000, 0.07),
                    TaxBracket(80001, 120000, 0.115),
                    TaxBracket(120001, 160000, 0.15),
                    TaxBracket(160001, 200000, 0.18),
                    TaxBracket(200001, 240000, 0.19),
                    TaxBracket(240001, 280000, 0.195),
                    TaxBracket(280001, 320000, 0.20),
                    TaxBracket(320001, float('inf'), 0.22)
                ],
                "cpf_rate": 0.20,  # Employee CPF contribution
                "residency_threshold_days": 183,
                "special_deductions": {
                    "cpf_ordinary_account": 37740,
                    "course_fee_relief": 5500,
                    "parent_relief": 9000
                }
            },
            "Netherlands": {
                "currency": "EUR",
                "tax_brackets": [
                    TaxBracket(0, 73031, 0.3693),  # Combined income tax + social security
                    TaxBracket(73032, float('inf'), 0.495)
                ],
                "social_security_included": True,  # Included in brackets above
                "residency_threshold_days": 183,
                "special_deductions": {
                    "employment_deduction": 4260,
                    "general_tax_credit": 3070,
                    "labour_tax_credit": 4209
                }
            },
            "Switzerland": {
                "currency": "CHF",
                "federal_tax_max": 0.115,  # Max federal rate
                "cantonal_tax_avg": 0.08,   # Average cantonal tax
                "municipal_tax_avg": 0.03,  # Average municipal tax
                "social_security_rate": 0.0525,  # AHV/IV/EO
                "unemployment_insurance": 0.011,
                "residency_threshold_days": 90,  # Lower threshold
                "special_deductions": {
                    "pillar_3a": 7056,  # Tax-deferred savings
                    "professional_expenses": 2000
                }
            }
        }
    
    def _load_treaty_networks(self) -> Dict[str, Dict[str, List[str]]]:
        """Load tax treaty information"""
        return {
            "double_taxation_agreements": {
                "United States": ["United Kingdom", "Germany", "Canada", "Australia", "Singapore", "Netherlands", "Switzerland"],
                "United Kingdom": ["United States", "Germany", "Canada", "Australia", "Singapore", "Netherlands", "Switzerland"],
                "Germany": ["United States", "United Kingdom", "Canada", "Australia", "Singapore", "Netherlands", "Switzerland"],
                "Canada": ["United States", "United Kingdom", "Germany", "Australia", "Singapore", "Netherlands", "Switzerland"]
            },
            "totalization_agreements": {
                "United States": ["United Kingdom", "Germany", "Canada", "Australia", "Netherlands", "Switzerland"],
                "Canada": ["United States", "United Kingdom", "Germany", "Australia", "Netherlands"]
            }
        }
    
    def _load_exchange_rates(self) -> Dict[str, float]:
        """Load current exchange rates to USD"""
        return {
            "USD": 1.0,
            "GBP": 1.27,
            "EUR": 1.08,
            "CAD": 0.74,
            "AUD": 0.67,
            "SGD": 0.74,
            "CHF": 1.11
        }
    
    def _load_social_security_rates(self) -> Dict[str, Dict]:
        """Load social security contribution rates"""
        return {
            "United States": {
                "social_security": 0.062,
                "medicare": 0.0145,
                "unemployment": 0.006,
                "total": 0.0765
            },
            "United Kingdom": {
                "national_insurance": 0.12,
                "total": 0.12
            },
            "Germany": {
                "pension": 0.093,
                "unemployment": 0.012,
                "health": 0.073,
                "care": 0.017,
                "total": 0.195
            },
            "Canada": {
                "cpp": 0.0595,
                "ei": 0.0229,
                "total": 0.0824
            }
        }
    
    def calculate_taxes(self, gross_salary: float, country: str, 
                       tax_residency: TaxResidency = TaxResidency.RESIDENT,
                       deduction_type: DeductionType = DeductionType.STANDARD,
                       custom_deductions: Optional[Dict[str, float]] = None) -> TaxCalculation:
        """Calculate comprehensive tax liability for a given salary and country"""
        
        if country not in self.tax_systems:
            raise ValueError(f"Tax system data not available for {country}")
        
        tax_system = self.tax_systems[country]
        currency = tax_system["currency"]
        
        # Calculate income tax
        income_tax = self._calculate_income_tax(gross_salary, country, tax_residency, deduction_type, custom_deductions)
        
        # Calculate social security
        social_security = self._calculate_social_security(gross_salary, country)
        
        # Calculate mandatory contributions
        mandatory_contributions = self._calculate_mandatory_contributions(gross_salary, country)
        
        # Calculate net salary
        net_salary = gross_salary - income_tax - social_security - mandatory_contributions
        
        # Calculate tax rates
        total_tax = income_tax + social_security + mandatory_contributions
        effective_tax_rate = (total_tax / gross_salary) * 100 if gross_salary > 0 else 0
        marginal_tax_rate = self._calculate_marginal_rate(gross_salary, country) * 100
        
        # Deductions applied
        deductions_applied = self._get_applied_deductions(gross_salary, country, deduction_type, custom_deductions)
        
        return TaxCalculation(
            country=country,
            gross_salary=gross_salary,
            currency=currency,
            income_tax=income_tax,
            social_security=social_security,
            mandatory_contributions=mandatory_contributions,
            net_salary=net_salary,
            effective_tax_rate=effective_tax_rate,
            marginal_tax_rate=marginal_tax_rate,
            deductions_applied=deductions_applied,
            take_home_monthly=net_salary / 12,
            tax_residency=tax_residency
        )
    
    def _calculate_income_tax(self, gross_salary: float, country: str, 
                            tax_residency: TaxResidency, deduction_type: DeductionType,
                            custom_deductions: Optional[Dict[str, float]]) -> float:
        """Calculate income tax based on tax brackets"""
        tax_system = self.tax_systems[country]
        
        # Apply deductions
        taxable_income = self._apply_deductions(gross_salary, country, deduction_type, custom_deductions)
        
        # Non-residents may have different rules
        if tax_residency == TaxResidency.NON_RESIDENT and country == "United States":
            # Flat 30% for non-residents (simplified)
            return max(0, taxable_income * 0.30)
        
        if country == "Switzerland":
            # Special calculation for Switzerland (combined rates)
            federal_rate = min(0.115, taxable_income / 1000000 * 0.115) if taxable_income > 31300 else 0
            cantonal_rate = tax_system["cantonal_tax_avg"]
            municipal_rate = tax_system["municipal_tax_avg"]
            return taxable_income * (federal_rate + cantonal_rate + municipal_rate)
        
        # Progressive tax calculation
        if "tax_brackets" in tax_system:
            return self._calculate_progressive_tax(taxable_income, tax_system["tax_brackets"])
        elif "federal_brackets" in tax_system:  # Canada
            federal_tax = self._calculate_progressive_tax(taxable_income, tax_system["federal_brackets"])
            provincial_tax = taxable_income * tax_system["provincial_tax_avg"]
            return federal_tax + provincial_tax
        
        return 0
    
    def _calculate_progressive_tax(self, taxable_income: float, brackets: List[TaxBracket]) -> float:
        """Calculate tax using progressive brackets"""
        total_tax = 0
        remaining_income = taxable_income
        
        for bracket in brackets:
            if remaining_income <= 0:
                break
            
            bracket_income = min(remaining_income, bracket.max_income - bracket.min_income)
            if bracket_income > 0:
                total_tax += bracket_income * bracket.rate
                remaining_income -= bracket_income
        
        return total_tax
    
    def _apply_deductions(self, gross_salary: float, country: str, 
                         deduction_type: DeductionType,
                         custom_deductions: Optional[Dict[str, float]]) -> float:
        """Apply tax deductions to reduce taxable income"""
        tax_system = self.tax_systems[country]
        total_deductions = 0
        
        # Standard deduction
        if deduction_type == DeductionType.STANDARD and "standard_deduction" in tax_system:
            total_deductions = tax_system["standard_deduction"]
        
        # Basic allowance (for countries like Germany)
        if "basic_allowance" in tax_system.get("special_deductions", {}):
            total_deductions = max(total_deductions, tax_system["special_deductions"]["basic_allowance"])
        
        # Custom deductions
        if custom_deductions:
            for deduction_name, amount in custom_deductions.items():
                if deduction_name in tax_system.get("special_deductions", {}):
                    max_allowed = tax_system["special_deductions"][deduction_name]
                    total_deductions += min(amount, max_allowed)
                else:
                    total_deductions += amount
        
        return max(0, gross_salary - total_deductions)
    
    def _calculate_social_security(self, gross_salary: float, country: str) -> float:
        """Calculate social security contributions"""
        if country not in self.social_security_rates:
            return 0
        
        rates = self.social_security_rates[country]
        tax_system = self.tax_systems[country]
        
        # Some countries have caps on social security
        if country == "United States":
            # Social Security cap (2024: $160,200)
            ss_cap = 160200
            social_security_wage = min(gross_salary, ss_cap)
            medicare_wage = gross_salary  # No cap on Medicare
            
            return (social_security_wage * 0.062) + (medicare_wage * 0.0145)
        
        elif country == "Germany":
            # Contribution ceiling
            contribution_ceiling = 87600  # 2024 amount
            capped_salary = min(gross_salary, contribution_ceiling)
            return capped_salary * rates["total"]
        
        else:
            return gross_salary * rates["total"]
    
    def _calculate_mandatory_contributions(self, gross_salary: float, country: str) -> float:
        """Calculate mandatory contributions (pension, unemployment insurance, etc.)"""
        tax_system = self.tax_systems[country]
        
        if country == "Australia":
            # Superannuation is paid by employer, not deducted from salary
            return 0
        
        elif country == "Singapore":
            # CPF contributions
            cpf_rate = tax_system["cpf_rate"]
            # Ordinary wage ceiling
            ordinary_wage_ceiling = 72000  # Annual ceiling
            capped_salary = min(gross_salary, ordinary_wage_ceiling)
            return capped_salary * cpf_rate
        
        elif country == "United Kingdom":
            # Pension auto-enrollment
            pension_rate = tax_system["pension_contribution"]
            qualifying_earnings = max(0, gross_salary - 6240)  # Above lower threshold
            return min(qualifying_earnings, 50270) * pension_rate  # Up to upper threshold
        
        return 0
    
    def _calculate_marginal_rate(self, gross_salary: float, country: str) -> float:
        """Calculate marginal tax rate"""
        current_calc = self.calculate_taxes(gross_salary, country)
        higher_calc = self.calculate_taxes(gross_salary + 1000, country)
        
        marginal_rate = (higher_calc.income_tax + higher_calc.social_security - 
                        current_calc.income_tax - current_calc.social_security) / 1000
        
        return marginal_rate
    
    def _get_applied_deductions(self, gross_salary: float, country: str,
                              deduction_type: DeductionType,
                              custom_deductions: Optional[Dict[str, float]]) -> Dict[str, float]:
        """Get breakdown of applied deductions"""
        deductions = {}
        tax_system = self.tax_systems[country]
        
        if deduction_type == DeductionType.STANDARD and "standard_deduction" in tax_system:
            deductions["Standard Deduction"] = tax_system["standard_deduction"]
        
        if custom_deductions:
            for name, amount in custom_deductions.items():
                deductions[name] = amount
        
        return deductions
    
    def compare_countries(self, gross_salary: float, countries: List[str],
                         base_country: str = "United States") -> TaxComparison:
        """Compare tax implications across multiple countries"""
        calculations = []
        
        # Convert salary to local currency for each country
        for country in countries:
            local_salary = self._convert_salary(gross_salary, "USD", self.tax_systems[country]["currency"])
            calc = self.calculate_taxes(local_salary, country)
            calculations.append(calc)
        
        # Generate recommendations
        recommendations = self._generate_tax_recommendations(calculations)
        
        # Get treaty benefits
        treaty_benefits = self._get_treaty_benefits(base_country, countries)
        
        # Suggest optimal structures
        optimal_structures = self._suggest_optimal_structures(calculations, base_country)
        
        return TaxComparison(
            base_country=base_country,
            comparison_countries=countries,
            calculations=calculations,
            recommendations=recommendations,
            treaty_benefits=treaty_benefits,
            optimal_structures=optimal_structures
        )
    
    def _convert_salary(self, amount: float, from_currency: str, to_currency: str) -> float:
        """Convert salary between currencies"""
        if from_currency == to_currency:
            return amount
        
        # Convert to USD first, then to target currency
        usd_amount = amount / self.exchange_rates.get(from_currency, 1.0)
        return usd_amount * self.exchange_rates.get(to_currency, 1.0)
    
    def _generate_tax_recommendations(self, calculations: List[TaxCalculation]) -> List[str]:
        """Generate tax optimization recommendations"""
        recommendations = []
        
        # Find most tax-efficient country
        best_net = max(calculations, key=lambda x: x.net_salary)
        recommendations.append(f"Highest net income: {best_net.country} ({best_net.currency} {best_net.net_salary:,.0f})")
        
        # Find lowest effective tax rate
        lowest_tax = min(calculations, key=lambda x: x.effective_tax_rate)
        recommendations.append(f"Lowest tax rate: {lowest_tax.country} ({lowest_tax.effective_tax_rate:.1f}%)")
        
        # Social security considerations
        for calc in calculations:
            if calc.social_security / calc.gross_salary > 0.15:
                recommendations.append(f"High social security in {calc.country} - consider totalization agreements")
        
        # Specific recommendations by country
        for calc in calculations:
            if calc.country == "Singapore" and calc.effective_tax_rate < 15:
                recommendations.append("Singapore: Low tax rate, consider CPF benefits for retirement")
            elif calc.country == "Germany" and calc.effective_tax_rate > 40:
                recommendations.append("Germany: High tax rate, but excellent social benefits included")
            elif calc.country == "United States" and calc.marginal_tax_rate > 30:
                recommendations.append("US: Consider maximizing 401(k) and health insurance deductions")
        
        return recommendations
    
    def _get_treaty_benefits(self, base_country: str, countries: List[str]) -> Dict[str, List[str]]:
        """Get applicable tax treaty benefits"""
        benefits = {}
        
        dta_countries = self.treaty_networks.get("double_taxation_agreements", {}).get(base_country, [])
        totalization_countries = self.treaty_networks.get("totalization_agreements", {}).get(base_country, [])
        
        for country in countries:
            country_benefits = []
            
            if country in dta_countries:
                country_benefits.append("Double taxation agreement - avoid paying tax in both countries")
                country_benefits.append("Reduced withholding tax rates")
                
            if country in totalization_countries:
                country_benefits.append("Social security totalization - avoid double social security payments")
                country_benefits.append("Coordination of benefits between countries")
            
            if country_benefits:
                benefits[country] = country_benefits
        
        return benefits
    
    def _suggest_optimal_structures(self, calculations: List[TaxCalculation], 
                                  base_country: str) -> List[Dict]:
        """Suggest optimal tax structures"""
        structures = []
        
        # Foreign Earned Income Exclusion for US citizens abroad
        us_calc = next((c for c in calculations if c.country == "United States"), None)
        if us_calc and base_country == "United States":
            structures.append({
                "structure": "Foreign Earned Income Exclusion",
                "description": "Exclude up to $120,000 of foreign earned income from US taxes",
                "requirements": ["Physical presence test (330 days abroad)", "Bona fide residence test"],
                "savings": "Up to $30,000+ in tax savings annually"
            })
        
        # For high earners, consider countries with territorial tax systems
        high_earner_countries = [c for c in calculations if c.gross_salary > 200000]
        if high_earner_countries:
            structures.append({
                "structure": "Territorial Tax Planning",
                "description": "Relocate to countries that don't tax foreign-sourced income",
                "countries": ["Singapore", "Hong Kong", "Malaysia"],
                "savings": "Significant for foreign investment income"
            })
        
        return structures

# Global instance
tax_optimizer = InternationalTaxOptimizer()