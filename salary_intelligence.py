"""
Global Salary Intelligence System
Advanced salary comparison with cost of living, taxes, and negotiation insights
"""

import requests
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SalaryData:
    base_salary: float
    currency: str
    location: str
    cost_of_living_index: float
    tax_rate: float
    net_salary: float
    purchasing_power: float
    job_title: str
    experience_level: str

@dataclass
class CostOfLivingData:
    location: str
    overall_index: float
    housing_index: float
    food_index: float
    transportation_index: float
    healthcare_index: float
    utilities_index: float

class SalaryIntelligence:
    def __init__(self):
        # Real cost of living data (this would connect to APIs in production)
        self.cost_of_living_data = {
            "New York, NY": {"index": 100, "housing": 100, "food": 100, "transport": 100},
            "San Francisco, CA": {"index": 92.4, "housing": 102.3, "food": 95.8, "transport": 88.7},
            "London, UK": {"index": 82.3, "housing": 75.2, "food": 68.9, "transport": 45.3},
            "Toronto, Canada": {"index": 71.2, "housing": 55.8, "food": 72.1, "transport": 67.4},
            "Berlin, Germany": {"index": 65.4, "housing": 42.1, "food": 58.7, "transport": 55.2},
            "Amsterdam, Netherlands": {"index": 78.9, "housing": 68.4, "food": 75.3, "transport": 62.1},
            "Sydney, Australia": {"index": 83.7, "housing": 78.9, "food": 89.2, "transport": 71.5},
            "Singapore": {"index": 84.3, "housing": 89.7, "food": 65.4, "transport": 43.2},
            "Tokyo, Japan": {"index": 88.1, "housing": 85.6, "food": 78.9, "transport": 69.7},
            "Dubai, UAE": {"index": 67.8, "housing": 58.9, "food": 52.3, "transport": 34.1}
        }
        
        # Tax rates by country (simplified)
        self.tax_rates = {
            "United States": 0.25,
            "United Kingdom": 0.32,
            "Canada": 0.28,
            "Germany": 0.35,
            "Netherlands": 0.37,
            "Australia": 0.30,
            "Singapore": 0.15,
            "Japan": 0.33,
            "UAE": 0.0
        }
        
        # Currency conversion rates (would be live in production)
        self.exchange_rates = {
            "USD": 1.0,
            "GBP": 1.27,
            "CAD": 0.74,
            "EUR": 1.08,
            "AUD": 0.65,
            "SGD": 0.74,
            "JPY": 0.0067,
            "AED": 0.27
        }

    def get_salary_comparison(self, job_title: str, experience_level: str, 
                            locations: List[str]) -> List[SalaryData]:
        """Get comprehensive salary comparison across multiple locations"""
        
        # Base salary ranges by job title and experience (would come from real API)
        salary_ranges = {
            "Software Engineer": {
                "Entry": {"min": 70000, "max": 95000},
                "Mid": {"min": 95000, "max": 140000},
                "Senior": {"min": 140000, "max": 200000},
                "Lead": {"min": 180000, "max": 280000}
            },
            "Data Scientist": {
                "Entry": {"min": 80000, "max": 110000},
                "Mid": {"min": 110000, "max": 150000},
                "Senior": {"min": 150000, "max": 220000},
                "Lead": {"min": 200000, "max": 300000}
            },
            "Product Manager": {
                "Entry": {"min": 90000, "max": 120000},
                "Mid": {"min": 120000, "max": 170000},
                "Senior": {"min": 170000, "max": 250000},
                "Lead": {"min": 220000, "max": 350000}
            },
            "DevOps Engineer": {
                "Entry": {"min": 75000, "max": 100000},
                "Mid": {"min": 100000, "max": 145000},
                "Senior": {"min": 145000, "max": 210000},
                "Lead": {"min": 190000, "max": 290000}
            }
        }
        
        results = []
        base_range = salary_ranges.get(job_title, salary_ranges["Software Engineer"])
        base_salary = (base_range[experience_level]["min"] + base_range[experience_level]["max"]) / 2
        
        for location in locations:
            # Adjust salary based on location
            city_data = self.cost_of_living_data.get(location, {"index": 70})
            location_multiplier = city_data["index"] / 100
            adjusted_salary = base_salary * location_multiplier
            
            # Get country from location (simplified)
            country = self._get_country_from_location(location)
            tax_rate = self.tax_rates.get(country, 0.25)
            net_salary = adjusted_salary * (1 - tax_rate)
            
            # Calculate purchasing power
            purchasing_power = net_salary / (city_data["index"] / 100)
            
            salary_data = SalaryData(
                base_salary=adjusted_salary,
                currency="USD",  # Would be location-specific in production
                location=location,
                cost_of_living_index=city_data["index"],
                tax_rate=tax_rate,
                net_salary=net_salary,
                purchasing_power=purchasing_power,
                job_title=job_title,
                experience_level=experience_level
            )
            results.append(salary_data)
        
        # Sort by purchasing power (highest first)
        results.sort(key=lambda x: x.purchasing_power, reverse=True)
        return results

    def get_negotiation_insights(self, job_title: str, experience_level: str, 
                               location: str, current_offer: float) -> Dict:
        """Get salary negotiation insights and recommendations"""
        
        # Get market data for the position
        comparisons = self.get_salary_comparison(job_title, experience_level, [location])
        if not comparisons:
            return {"error": "No data available for this location"}
        
        market_data = comparisons[0]
        
        # Calculate percentiles
        market_salary = market_data.base_salary
        percentile = (current_offer / market_salary) * 100
        
        # Generate insights
        insights = {
            "current_offer": current_offer,
            "market_average": market_salary,
            "percentile": percentile,
            "recommendation": "",
            "negotiation_range": {
                "conservative": market_salary * 1.05,
                "target": market_salary * 1.15,
                "aggressive": market_salary * 1.25
            },
            "supporting_points": []
        }
        
        if percentile < 75:
            insights["recommendation"] = "Strong negotiation opportunity"
            insights["supporting_points"] = [
                f"Offer is {100-percentile:.1f}% below market average",
                f"Cost of living in {location} is {market_data.cost_of_living_index}% of NYC baseline",
                f"Your experience level ({experience_level}) commands premium pricing"
            ]
        elif percentile < 90:
            insights["recommendation"] = "Moderate negotiation potential"
            insights["supporting_points"] = [
                f"Offer is competitive but room for improvement",
                f"Market average is ${market_salary:,.0f}",
                f"Consider negotiating benefits and equity"
            ]
        else:
            insights["recommendation"] = "Excellent offer"
            insights["supporting_points"] = [
                f"Offer exceeds market average by {percentile-100:.1f}%",
                f"Focus on non-salary benefits",
                f"Consider accepting with minor adjustments"
            ]
        
        return insights

    def get_relocation_cost_analysis(self, from_location: str, to_location: str, 
                                   family_size: int = 1) -> Dict:
        """Calculate comprehensive relocation costs"""
        
        # Base relocation costs (would be from real APIs)
        base_costs = {
            "moving_services": 5000 + (family_size * 1000),
            "flights": 1500 * family_size,
            "temporary_accommodation": 3000,
            "visa_fees": 2000,
            "security_deposits": 4000,
            "initial_setup": 2000
        }
        
        # Location-specific adjustments
        from_data = self.cost_of_living_data.get(from_location, {"index": 70})
        to_data = self.cost_of_living_data.get(to_location, {"index": 70})
        
        # Adjust costs based on destination
        cost_multiplier = to_data["index"] / 100
        adjusted_costs = {k: v * cost_multiplier for k, v in base_costs.items()}
        
        total_cost = sum(adjusted_costs.values())
        
        # Monthly cost comparison
        monthly_diff = (to_data["index"] - from_data["index"]) * 50  # $50 per index point
        
        analysis = {
            "one_time_costs": adjusted_costs,
            "total_relocation_cost": total_cost,
            "monthly_cost_difference": monthly_diff,
            "breakeven_salary_increase": total_cost + (monthly_diff * 12),
            "cost_breakdown": {
                "housing_change": f"{((to_data.get('housing', 70) / from_data.get('housing', 70)) - 1) * 100:+.1f}%",
                "food_change": f"{((to_data.get('food', 70) / from_data.get('food', 70)) - 1) * 100:+.1f}%",
                "transport_change": f"{((to_data.get('transport', 70) / from_data.get('transport', 70)) - 1) * 100:+.1f}%"
            }
        }
        
        return analysis

    def _get_country_from_location(self, location: str) -> str:
        """Extract country from location string"""
        location_to_country = {
            "New York, NY": "United States",
            "San Francisco, CA": "United States",
            "London, UK": "United Kingdom",
            "Toronto, Canada": "Canada",
            "Berlin, Germany": "Germany",
            "Amsterdam, Netherlands": "Netherlands",
            "Sydney, Australia": "Australia",
            "Singapore": "Singapore",
            "Tokyo, Japan": "Japan",
            "Dubai, UAE": "UAE"
        }
        return location_to_country.get(location, "United States")

    def get_tax_optimization_tips(self, salary: float, location: str) -> List[str]:
        """Get location-specific tax optimization advice"""
        
        country = self._get_country_from_location(location)
        tax_rate = self.tax_rates.get(country, 0.25)
        
        tips = [
            f"Current effective tax rate: {tax_rate*100:.1f}%",
            f"Annual tax burden: ${salary * tax_rate:,.0f}"
        ]
        
        if country == "United States":
            tips.extend([
                "Maximize 401(k) contributions ($23,000 limit)",
                "Consider Health Savings Account (HSA)",
                "Look into stock option tax strategies"
            ])
        elif country == "United Kingdom":
            tips.extend([
                "Utilize pension contributions for tax relief",
                "Consider salary sacrifice schemes",
                "ISA allowance for tax-free savings"
            ])
        elif country == "Germany":
            tips.extend([
                "Church tax may apply (8-9% additional)",
                "Professional expenses are deductible",
                "Consider private pension schemes"
            ])
        elif country == "UAE":
            tips.extend([
                "No personal income tax",
                "Maximize savings and investments",
                "Consider offshore banking options"
            ])
        
        return tips

# Example usage
if __name__ == "__main__":
    salary_intel = SalaryIntelligence()
    
    # Example: Compare Software Engineer salaries
    locations = ["New York, NY", "London, UK", "Berlin, Germany", "Singapore"]
    comparisons = salary_intel.get_salary_comparison("Software Engineer", "Senior", locations)
    
    print("Salary Comparison Results:")
    for comp in comparisons:
        print(f"{comp.location}: ${comp.base_salary:,.0f} gross, ${comp.net_salary:,.0f} net, Purchasing Power: ${comp.purchasing_power:,.0f}")
    
    # Example: Negotiation insights
    insights = salary_intel.get_negotiation_insights("Software Engineer", "Senior", "New York, NY", 160000)
    print(f"\nNegotiation Recommendation: {insights['recommendation']}")