"""
Housing Market Intelligence
Real-time rental/purchase market analysis for international relocations
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime

class PropertyType(Enum):
    APARTMENT = "apartment"
    HOUSE = "house"
    CONDO = "condo"
    STUDIO = "studio"
    SERVICED_APARTMENT = "serviced_apartment"

class MarketTrend(Enum):
    RISING = "rising"
    FALLING = "falling"
    STABLE = "stable"
    VOLATILE = "volatile"

@dataclass
class PropertyListing:
    id: str
    address: str
    neighborhood: str
    property_type: PropertyType
    bedrooms: int
    bathrooms: float
    square_meters: int
    monthly_rent: Optional[float]
    purchase_price: Optional[float]
    currency: str
    available_date: datetime
    amenities: List[str]
    commute_to_cbd: str
    expat_friendly: bool
    furnishing: str  # furnished, unfurnished, partially furnished

@dataclass
class NeighborhoodInfo:
    name: str
    safety_rating: float  # 1-10 scale
    expat_population: str  # high, medium, low
    avg_rent_per_sqm: float
    avg_purchase_per_sqm: float
    commute_to_cbd: str
    international_schools: List[str]
    restaurants_bars: int
    grocery_stores: int
    public_transport_access: str
    walkability_score: float
    family_friendliness: float
    nightlife_rating: float

@dataclass
class MarketAnalysis:
    city: str
    neighborhood: str
    property_type: PropertyType
    price_trend: MarketTrend
    price_change_3month: float  # percentage
    price_change_12month: float
    median_rent: float
    median_purchase: float
    price_per_sqm: float
    supply_demand_ratio: float
    average_days_on_market: int
    seasonal_patterns: Dict[str, float]
    investment_outlook: str

@dataclass
class CommuteAnalysis:
    from_neighborhood: str
    to_location: str
    transport_modes: List[Dict[str, str]]
    peak_time_duration: str
    off_peak_duration: str
    monthly_transport_cost: float
    reliability_score: float

@dataclass
class HousingRecommendation:
    listings: List[PropertyListing]
    neighborhood_analysis: NeighborhoodInfo
    market_analysis: MarketAnalysis
    commute_analysis: List[CommuteAnalysis]
    total_monthly_cost: float
    pros_cons: Dict[str, List[str]]
    suitability_score: float

class HousingMarketIntelligence:
    def __init__(self):
        self.market_data = self._load_market_data()
        self.neighborhoods = self._load_neighborhood_data()
        self.transport_data = self._load_transport_data()
        self.cost_factors = self._load_cost_factors()
    
    def _load_market_data(self) -> Dict[str, Dict]:
        """Load real estate market data by city"""
        return {
            "Singapore": {
                "median_rent_per_sqm": 45,  # SGD per sqm
                "median_purchase_per_sqm": 15000,
                "market_trend": MarketTrend.STABLE,
                "price_change_3month": 1.2,
                "price_change_12month": 3.5,
                "supply_demand_ratio": 0.95,
                "average_days_on_market": 45,
                "currency": "SGD",
                "seasonal_patterns": {
                    "Q1": 0.98, "Q2": 1.02, "Q3": 0.96, "Q4": 1.04
                }
            },
            "London": {
                "median_rent_per_sqm": 35,  # GBP per sqm
                "median_purchase_per_sqm": 8500,
                "market_trend": MarketTrend.RISING,
                "price_change_3month": 2.1,
                "price_change_12month": 7.8,
                "supply_demand_ratio": 1.15,
                "average_days_on_market": 28,
                "currency": "GBP",
                "seasonal_patterns": {
                    "Q1": 0.95, "Q2": 1.05, "Q3": 0.92, "Q4": 1.08
                }
            },
            "Berlin": {
                "median_rent_per_sqm": 18,  # EUR per sqm
                "median_purchase_per_sqm": 6200,
                "market_trend": MarketTrend.RISING,
                "price_change_3month": 1.8,
                "price_change_12month": 6.2,
                "supply_demand_ratio": 1.25,
                "average_days_on_market": 21,
                "currency": "EUR",
                "seasonal_patterns": {
                    "Q1": 0.96, "Q2": 1.03, "Q3": 0.98, "Q4": 1.03
                }
            },
            "Tokyo": {
                "median_rent_per_sqm": 25,  # USD equivalent
                "median_purchase_per_sqm": 7500,
                "market_trend": MarketTrend.STABLE,
                "price_change_3month": 0.5,
                "price_change_12month": 1.8,
                "supply_demand_ratio": 0.88,
                "average_days_on_market": 35,
                "currency": "JPY",
                "seasonal_patterns": {
                    "Q1": 1.05, "Q2": 0.97, "Q3": 0.95, "Q4": 1.03
                }
            }
        }
    
    def _load_neighborhood_data(self) -> Dict[str, Dict[str, NeighborhoodInfo]]:
        """Load neighborhood information by city"""
        return {
            "Singapore": {
                "Orchard": NeighborhoodInfo(
                    name="Orchard",
                    safety_rating=9.2,
                    expat_population="high",
                    avg_rent_per_sqm=55,
                    avg_purchase_per_sqm=18000,
                    commute_to_cbd="5-15 minutes",
                    international_schools=["Chatsworth International", "ISS International"],
                    restaurants_bars=150,
                    grocery_stores=25,
                    public_transport_access="excellent",
                    walkability_score=9.5,
                    family_friendliness=8.5,
                    nightlife_rating=9.0
                ),
                "East Coast": NeighborhoodInfo(
                    name="East Coast",
                    safety_rating=8.8,
                    expat_population="high",
                    avg_rent_per_sqm=42,
                    avg_purchase_per_sqm=14500,
                    commute_to_cbd="20-30 minutes",
                    international_schools=["East Coast International", "UWC South East Asia"],
                    restaurants_bars=80,
                    grocery_stores=15,
                    public_transport_access="good",
                    walkability_score=7.5,
                    family_friendliness=9.5,
                    nightlife_rating=6.5
                ),
                "Tanjong Pagar": NeighborhoodInfo(
                    name="Tanjong Pagar",
                    safety_rating=9.0,
                    expat_population="medium",
                    avg_rent_per_sqm=48,
                    avg_purchase_per_sqm=16500,
                    commute_to_cbd="5-10 minutes",
                    international_schools=[],
                    restaurants_bars=120,
                    grocery_stores=20,
                    public_transport_access="excellent",
                    walkability_score=9.0,
                    family_friendliness=7.0,
                    nightlife_rating=8.5
                )
            },
            "London": {
                "Canary Wharf": NeighborhoodInfo(
                    name="Canary Wharf",
                    safety_rating=8.5,
                    expat_population="high",
                    avg_rent_per_sqm=48,
                    avg_purchase_per_sqm=12000,
                    commute_to_cbd="direct",
                    international_schools=["International School of London"],
                    restaurants_bars=85,
                    grocery_stores=12,
                    public_transport_access="excellent",
                    walkability_score=8.0,
                    family_friendliness=6.5,
                    nightlife_rating=7.5
                ),
                "Wimbledon": NeighborhoodInfo(
                    name="Wimbledon",
                    safety_rating=9.0,
                    expat_population="medium",
                    avg_rent_per_sqm=32,
                    avg_purchase_per_sqm=8200,
                    commute_to_cbd="25-35 minutes",
                    international_schools=["The American School in London"],
                    restaurants_bars=45,
                    grocery_stores=18,
                    public_transport_access="good",
                    walkability_score=7.5,
                    family_friendliness=9.5,
                    nightlife_rating=5.5
                ),
                "Shoreditch": NeighborhoodInfo(
                    name="Shoreditch",
                    safety_rating=7.5,
                    expat_population="high",
                    avg_rent_per_sqm=38,
                    avg_purchase_per_sqm=9500,
                    commute_to_cbd="15-25 minutes",
                    international_schools=[],
                    restaurants_bars=180,
                    grocery_stores=15,
                    public_transport_access="excellent",
                    walkability_score=9.0,
                    family_friendliness=6.0,
                    nightlife_rating=9.5
                )
            }
        }
    
    def _load_transport_data(self) -> Dict[str, Dict]:
        """Load transportation data by city"""
        return {
            "Singapore": {
                "public_transport": {
                    "monthly_pass": 130,  # SGD
                    "reliability": 9.5,
                    "coverage": "excellent"
                },
                "taxi_uber": {
                    "base_fare": 3.9,
                    "per_km": 0.55,
                    "peak_multiplier": 1.25
                },
                "car_ownership": {
                    "coe_cost": 80000,  # Certificate of Entitlement
                    "monthly_parking": 300,
                    "fuel_per_liter": 2.8
                }
            },
            "London": {
                "public_transport": {
                    "monthly_pass": 160,  # GBP (Zones 1-3)
                    "reliability": 8.2,
                    "coverage": "excellent"
                },
                "taxi_uber": {
                    "base_fare": 3.2,
                    "per_km": 1.8,
                    "peak_multiplier": 1.4
                },
                "car_ownership": {
                    "congestion_charge": 15,  # daily
                    "monthly_parking": 400,
                    "fuel_per_liter": 1.6
                }
            }
        }
    
    def _load_cost_factors(self) -> Dict[str, Dict]:
        """Load additional cost factors by city"""
        return {
            "Singapore": {
                "utilities_monthly": 150,  # SGD
                "internet_monthly": 60,
                "security_deposit_months": 2,
                "agent_fee_percent": 1.0,
                "stamp_duty_percent": 0.4,
                "additional_buyer_stamp_duty": True  # for foreigners
            },
            "London": {
                "utilities_monthly": 180,  # GBP
                "internet_monthly": 35,
                "security_deposit_months": 1.5,
                "agent_fee_percent": 0,  # banned for tenants
                "stamp_duty_percent": 2.0,
                "council_tax_monthly": 150
            },
            "Berlin": {
                "utilities_monthly": 120,  # EUR
                "internet_monthly": 45,
                "security_deposit_months": 3,
                "agent_fee_percent": 2.38,
                "property_transfer_tax": 6.0
            }
        }
    
    def analyze_housing_market(self, city: str, family_size: int, budget_monthly: float,
                             work_location: str, priorities: List[str]) -> List[HousingRecommendation]:
        """Analyze housing market and provide recommendations"""
        
        recommendations = []
        neighborhoods = self.neighborhoods.get(city, {})
        market_data = self.market_data.get(city, {})
        
        for neighborhood_name, neighborhood_info in neighborhoods.items():
            # Check if neighborhood matches budget and requirements
            if self._neighborhood_matches_criteria(neighborhood_info, family_size, budget_monthly, priorities):
                
                # Get sample listings
                listings = self._generate_sample_listings(neighborhood_name, neighborhood_info, family_size, budget_monthly)
                
                # Create market analysis
                market_analysis = self._create_market_analysis(city, neighborhood_name, market_data)
                
                # Analyze commute
                commute_analysis = self._analyze_commute(neighborhood_name, work_location, city)
                
                # Calculate total monthly cost
                total_cost = self._calculate_total_monthly_cost(listings, city)
                
                # Generate pros and cons
                pros_cons = self._generate_pros_cons(neighborhood_info, market_analysis, commute_analysis)
                
                # Calculate suitability score
                suitability_score = self._calculate_suitability_score(
                    neighborhood_info, market_analysis, commute_analysis, priorities, budget_monthly, total_cost)
                
                recommendation = HousingRecommendation(
                    listings=listings,
                    neighborhood_analysis=neighborhood_info,
                    market_analysis=market_analysis,
                    commute_analysis=commute_analysis,
                    total_monthly_cost=total_cost,
                    pros_cons=pros_cons,
                    suitability_score=suitability_score
                )
                
                recommendations.append(recommendation)
        
        # Sort by suitability score
        recommendations.sort(key=lambda x: x.suitability_score, reverse=True)
        return recommendations[:5]  # Top 5 recommendations
    
    def _neighborhood_matches_criteria(self, neighborhood: NeighborhoodInfo, family_size: int,
                                     budget: float, priorities: List[str]) -> bool:
        """Check if neighborhood matches basic criteria"""
        
        # Budget check (rough estimate)
        estimated_monthly = neighborhood.avg_rent_per_sqm * (family_size * 25)  # Rough sqm estimate
        if estimated_monthly > budget * 1.2:  # Allow 20% buffer
            return False
        
        # Family-friendliness for families with children
        if family_size > 2 and neighborhood.family_friendliness < 7.0:
            return False
        
        # Safety requirement
        if "safety" in priorities and neighborhood.safety_rating < 8.0:
            return False
        
        return True
    
    def _generate_sample_listings(self, neighborhood: str, neighborhood_info: NeighborhoodInfo,
                                family_size: int, budget: float) -> List[PropertyListing]:
        """Generate sample property listings for the neighborhood"""
        listings = []
        
        # Determine property requirements based on family size
        if family_size <= 2:
            property_configs = [(PropertyType.APARTMENT, 1, 1, 50), (PropertyType.CONDO, 2, 1, 70)]
        elif family_size <= 4:
            property_configs = [(PropertyType.APARTMENT, 2, 2, 80), (PropertyType.CONDO, 3, 2, 100)]
        else:
            property_configs = [(PropertyType.HOUSE, 3, 2, 120), (PropertyType.CONDO, 4, 3, 150)]
        
        for i, (prop_type, bedrooms, bathrooms, sqm) in enumerate(property_configs):
            monthly_rent = neighborhood_info.avg_rent_per_sqm * sqm
            
            # Only include if within budget
            if monthly_rent <= budget * 1.1:  # Allow 10% over budget
                listing = PropertyListing(
                    id=f"{neighborhood}_{i+1}",
                    address=f"{i+1} {neighborhood} Street",
                    neighborhood=neighborhood,
                    property_type=prop_type,
                    bedrooms=bedrooms,
                    bathrooms=bathrooms,
                    square_meters=sqm,
                    monthly_rent=monthly_rent,
                    purchase_price=neighborhood_info.avg_purchase_per_sqm * sqm,
                    currency="SGD",  # Default, would be dynamic
                    available_date=datetime.now(),
                    amenities=self._get_typical_amenities(prop_type, neighborhood),
                    commute_to_cbd=neighborhood_info.commute_to_cbd,
                    expat_friendly=neighborhood_info.expat_population in ["high", "medium"],
                    furnishing="partially furnished"
                )
                listings.append(listing)
        
        return listings
    
    def _get_typical_amenities(self, property_type: PropertyType, neighborhood: str) -> List[str]:
        """Get typical amenities for property type and location"""
        base_amenities = ["Air conditioning", "Internet ready", "Security"]
        
        if property_type in [PropertyType.CONDO, PropertyType.SERVICED_APARTMENT]:
            base_amenities.extend(["Swimming pool", "Gym", "24/7 security", "Parking"])
        
        if neighborhood in ["Orchard", "Canary Wharf", "Tanjong Pagar"]:
            base_amenities.extend(["Concierge", "Business center"])
        
        return base_amenities
    
    def _create_market_analysis(self, city: str, neighborhood: str, market_data: Dict) -> MarketAnalysis:
        """Create market analysis for specific neighborhood"""
        return MarketAnalysis(
            city=city,
            neighborhood=neighborhood,
            property_type=PropertyType.APARTMENT,  # Default
            price_trend=market_data.get("market_trend", MarketTrend.STABLE),
            price_change_3month=market_data.get("price_change_3month", 0),
            price_change_12month=market_data.get("price_change_12month", 0),
            median_rent=market_data.get("median_rent_per_sqm", 0) * 70,  # Assume 70 sqm
            median_purchase=market_data.get("median_purchase_per_sqm", 0) * 70,
            price_per_sqm=market_data.get("median_rent_per_sqm", 0),
            supply_demand_ratio=market_data.get("supply_demand_ratio", 1.0),
            average_days_on_market=market_data.get("average_days_on_market", 30),
            seasonal_patterns=market_data.get("seasonal_patterns", {}),
            investment_outlook=self._determine_investment_outlook(market_data)
        )
    
    def _determine_investment_outlook(self, market_data: Dict) -> str:
        """Determine investment outlook based on market data"""
        trend = market_data.get("market_trend", MarketTrend.STABLE)
        price_change = market_data.get("price_change_12month", 0)
        
        if trend == MarketTrend.RISING and price_change > 5:
            return "Strong growth expected"
        elif trend == MarketTrend.RISING:
            return "Moderate growth expected"
        elif trend == MarketTrend.STABLE:
            return "Stable market conditions"
        else:
            return "Price corrections possible"
    
    def _analyze_commute(self, neighborhood: str, work_location: str, city: str) -> List[CommuteAnalysis]:
        """Analyze commute options from neighborhood to work location"""
        transport_data = self.transport_data.get(city, {})
        
        # Generate commute analysis based on transport options
        commute_options = []
        
        # Public transport option
        if transport_data.get("public_transport"):
            pt_data = transport_data["public_transport"]
            commute_options.append(CommuteAnalysis(
                from_neighborhood=neighborhood,
                to_location=work_location,
                transport_modes=[{"type": "Public Transport", "details": "MRT/Bus combination"}],
                peak_time_duration="25-40 minutes",
                off_peak_duration="20-30 minutes",
                monthly_transport_cost=pt_data["monthly_pass"],
                reliability_score=pt_data["reliability"]
            ))
        
        # Taxi/Uber option
        if transport_data.get("taxi_uber"):
            taxi_data = transport_data["taxi_uber"]
            daily_cost = (taxi_data["base_fare"] + taxi_data["per_km"] * 10) * 2  # Rough estimate
            commute_options.append(CommuteAnalysis(
                from_neighborhood=neighborhood,
                to_location=work_location,
                transport_modes=[{"type": "Taxi/Uber", "details": "Door-to-door service"}],
                peak_time_duration="20-35 minutes",
                off_peak_duration="15-25 minutes",
                monthly_transport_cost=daily_cost * 22,  # Working days
                reliability_score=8.5
            ))
        
        return commute_options
    
    def _calculate_total_monthly_cost(self, listings: List[PropertyListing], city: str) -> float:
        """Calculate total monthly living cost including rent and utilities"""
        if not listings:
            return 0
        
        avg_rent = sum(listing.monthly_rent or 0 for listing in listings) / len(listings)
        cost_factors = self.cost_factors.get(city, {})
        
        utilities = cost_factors.get("utilities_monthly", 150)
        internet = cost_factors.get("internet_monthly", 50)
        
        return avg_rent + utilities + internet
    
    def _generate_pros_cons(self, neighborhood: NeighborhoodInfo, market: MarketAnalysis,
                          commute: List[CommuteAnalysis]) -> Dict[str, List[str]]:
        """Generate pros and cons for the neighborhood"""
        pros = []
        cons = []
        
        # Safety pros/cons
        if neighborhood.safety_rating >= 9.0:
            pros.append("Excellent safety rating")
        elif neighborhood.safety_rating < 7.0:
            cons.append("Lower safety rating")
        
        # Expat community
        if neighborhood.expat_population == "high":
            pros.append("Large expat community")
        elif neighborhood.expat_population == "low":
            cons.append("Limited expat community")
        
        # Schools
        if neighborhood.international_schools:
            pros.append("Good international school options")
        else:
            cons.append("Limited international school options nearby")
        
        # Market conditions
        if market.price_trend == MarketTrend.STABLE:
            pros.append("Stable property market")
        elif market.price_trend == MarketTrend.RISING:
            cons.append("Rising property prices")
        
        # Commute
        if commute and commute[0].monthly_transport_cost < 200:
            pros.append("Affordable commute options")
        elif commute and commute[0].monthly_transport_cost > 500:
            cons.append("Expensive commute costs")
        
        # Lifestyle
        if neighborhood.walkability_score >= 8.0:
            pros.append("Highly walkable area")
        if neighborhood.restaurants_bars > 100:
            pros.append("Excellent dining and entertainment")
        
        return {"pros": pros, "cons": cons}
    
    def _calculate_suitability_score(self, neighborhood: NeighborhoodInfo, market: MarketAnalysis,
                                   commute: List[CommuteAnalysis], priorities: List[str],
                                   budget: float, total_cost: float) -> float:
        """Calculate overall suitability score"""
        score = 0.0
        
        # Budget fit (25% weight)
        budget_ratio = total_cost / budget if budget > 0 else 1
        if budget_ratio <= 1.0:
            score += 25
        elif budget_ratio <= 1.1:
            score += 20
        elif budget_ratio <= 1.2:
            score += 15
        
        # Safety (20% weight)
        score += neighborhood.safety_rating * 2
        
        # Commute convenience (20% weight)
        if commute:
            avg_reliability = sum(c.reliability_score for c in commute) / len(commute)
            score += avg_reliability * 2
        
        # Expat community (15% weight)
        expat_scores = {"high": 15, "medium": 10, "low": 5}
        score += expat_scores.get(neighborhood.expat_population, 5)
        
        # Priority-based scoring (20% weight)
        priority_score = 0
        if "family" in priorities:
            priority_score += neighborhood.family_friendliness * 2
        if "nightlife" in priorities:
            priority_score += neighborhood.nightlife_rating * 2
        if "walkability" in priorities:
            priority_score += neighborhood.walkability_score * 2
        
        score += min(priority_score, 20)  # Cap at 20 points
        
        return min(score, 100)  # Cap at 100

# Global instance
housing_intelligence = HousingMarketIntelligence()