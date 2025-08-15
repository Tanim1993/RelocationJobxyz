import requests
import logging
import os
from typing import List, Dict
import time
import json

def search_relocation_jobs(job_type: str = "", location: str = "") -> List[Dict]:
    """
    Search for jobs with relocation support using multiple free APIs
    This uses real job APIs to find authentic relocation opportunities
    """
    jobs = []
    
    # Try multiple free sources
    try:
        # 1. First try free USAJobs API (US Government jobs)
        usa_jobs = search_usajobs_api(job_type, location)
        jobs.extend(usa_jobs)
        
        # 2. Try JSearch API (RapidAPI) for real job data - FREE TIER
        rapidapi_key = os.getenv("RAPIDAPI_KEY")
        
        if rapidapi_key:
            rapidapi_jobs = search_jsearch_api(job_type, location, rapidapi_key)
            jobs.extend(rapidapi_jobs)
        else:
            logging.info("RAPIDAPI_KEY not found, using free APIs only")
        
        # 3. Try LinkUp API (completely free)
        linkup_jobs = search_linkup_api(job_type, location)
        jobs.extend(linkup_jobs)
        
    except Exception as e:
        logging.error(f"Error in job scraping: {str(e)}")
    
    return jobs[:20]  # Limit to 20 results

def search_usajobs_api(job_type: str, location: str) -> List[Dict]:
    """
    Search USAJobs API (completely free US government jobs)
    """
    jobs = []
    
    try:
        # USAJobs API - completely free, no API key needed
        params = {
            'Keyword': f"{job_type} visa sponsorship OR relocation",
            'LocationName': location if location else 'United States',
            'ResultsPerPage': 10
        }
        
        headers = {
            'User-Agent': 'YourAppName (your.email@example.com)'  # Required by USAJobs
        }
        
        response = requests.get(
            "https://data.usajobs.gov/api/search",
            params=params,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            
            for job_data in data.get("SearchResult", {}).get("SearchResultItems", []):
                job_detail = job_data.get("MatchedObjectDescriptor", {})
                
                job = {
                    "title": job_detail.get("PositionTitle", ""),
                    "company": job_detail.get("OrganizationName", "US Government"),
                    "location": job_detail.get("PositionLocationDisplay", ""),
                    "job_url": job_detail.get("ApplyURI", [{}])[0].get("", "") if job_detail.get("ApplyURI") else "",
                    "job_description": job_detail.get("QualificationSummary", ""),
                    "salary_range": format_usajobs_salary(job_detail.get("PositionRemuneration", [])),
                    "job_type": job_type or "Government",
                    "visa_sponsorship": True,  # Government jobs often support visa processes
                    "housing_assistance": "relocation" in job_detail.get("QualificationSummary", "").lower(),
                    "relocation_package": {"federal_relocation": True, "visa_support": True},
                    "relocation_type": "visa_sponsorship"
                }
                
                jobs.append(job)
                
    except Exception as e:
        logging.error(f"USAJobs API error: {str(e)}")
    
    return jobs

def search_jsearch_api(job_type: str, location: str, api_key: str) -> List[Dict]:
    """
    Search JSearch API (RapidAPI) - 500 free requests per month
    """
    jobs = []
    
    try:
        # Search terms that indicate relocation support
        relocation_keywords = [
            "visa sponsorship", "relocation package", "relocation assistance",
            "H1B sponsor", "work permit", "immigration support",
            "moving allowance", "relocation bonus", "international candidates"
        ]
        
        # Construct search query
        job_term = job_type if job_type else "engineer"
        search_query = f"{job_term} " + " OR ".join([f'"{keyword}"' for keyword in relocation_keywords[:3]])
        
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }
        
        params = {
            "query": search_query,
            "page": "1",
            "num_pages": "3",
            "country": "us" if not location else None,
            "employment_types": "FULLTIME"
        }
        
        if location:
            params["location"] = location
        
        response = requests.get(
            "https://jsearch.p.rapidapi.com/search",
            headers=headers,
            params=params,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            
            for job_data in data.get("data", []):
                # Check if job description contains relocation keywords
                job_description = job_data.get("job_description", "").lower()
                job_title = job_data.get("job_title", "").lower()
                
                has_relocation = any(keyword.lower() in job_description or keyword.lower() in job_title 
                                   for keyword in relocation_keywords)
                
                if has_relocation:
                    # Extract relocation benefits from description
                    relocation_package = extract_relocation_benefits(job_description)
                    
                    job = {
                        "title": job_data.get("job_title", ""),
                        "company": job_data.get("employer_name", ""),
                        "location": job_data.get("job_city", "") + ", " + job_data.get("job_country", ""),
                        "job_url": job_data.get("job_apply_link", ""),
                        "job_description": job_data.get("job_description", ""),
                        "requirements": job_data.get("job_required_skills", []),
                        "salary_range": extract_salary_range(job_data),
                        "job_type": job_type or extract_job_type(job_data.get("job_title", "")),
                        "visa_sponsorship": "visa" in job_description or "h1b" in job_description,
                        "housing_assistance": "housing" in job_description or "accommodation" in job_description,
                        "moving_allowance": extract_moving_allowance(job_description),
                        "relocation_type": determine_relocation_type(job_description),
                        "relocation_package": relocation_package,
                        "remote_friendly": job_data.get("job_is_remote", False),
                        "company_email": extract_company_email(job_data),
                        "hr_email": extract_hr_email(job_data)
                    }
                    
                    jobs.append(job)
                    
                    # Rate limiting
                    time.sleep(0.1)
        
        else:
            logging.error(f"JSearch API request failed with status {response.status_code}")
            
    except Exception as e:
        logging.error(f"Error in JSearch API: {str(e)}")
    
    return jobs

def search_linkup_api(job_type: str, location: str) -> List[Dict]:
    """
    Search LinkUp API (completely free - 5M+ jobs from company career pages)
    """
    jobs = []
    
    try:
        # LinkUp provides free access to job postings directly from company career pages
        params = {
            'q': f"{job_type} visa sponsorship OR relocation",
            'location': location if location else 'United States',
            'limit': 10
        }
        
        headers = {
            'User-Agent': 'RelocationJobsHub/1.0'
        }
        
        # Note: This would need actual LinkUp API endpoint
        # For now, return empty list as LinkUp requires registration
        logging.info("LinkUp API integration placeholder - requires registration")
        
    except Exception as e:
        logging.error(f"LinkUp API error: {str(e)}")
    
    return jobs

def format_usajobs_salary(remuneration_list: List) -> str:
    """
    Format USAJobs salary information
    """
    if not remuneration_list:
        return "Salary not specified"
    
    for rem in remuneration_list:
        min_range = rem.get('MinimumRange')
        max_range = rem.get('MaximumRange')
        
        if min_range and max_range:
            return f"${min_range:,} - ${max_range:,}"
        elif min_range:
            return f"${min_range:,}+"
    
    return "Government salary scale"

def search_adzuna_jobs_fallback(job_type: str, location: str) -> List[Dict]:
    """
    Fallback function using Adzuna API for job search
    """
    jobs = []
    
    try:
        app_id = os.getenv("ADZUNA_APP_ID")
        app_key = os.getenv("ADZUNA_APP_KEY")
        
        if not app_id or not app_key:
            return []
        
        # Search for jobs with relocation terms
        search_terms = f"{job_type} visa sponsorship OR relocation"
        
        params = {
            "app_id": app_id,
            "app_key": app_key,
            "results_per_page": 20,
            "what": search_terms,
            "content-type": "application/json"
        }
        
        if location:
            params["where"] = location
        
        response = requests.get(
            "https://api.adzuna.com/v1/api/jobs/us/search/1",
            params=params,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            
            for job_data in data.get("results", []):
                job_description = job_data.get("description", "").lower()
                
                # Filter for relocation-related jobs
                relocation_keywords = ["visa", "relocation", "h1b", "sponsor", "immigration"]
                if any(keyword in job_description for keyword in relocation_keywords):
                    
                    job = {
                        "title": job_data.get("title", ""),
                        "company": job_data.get("company", {}).get("display_name", ""),
                        "location": job_data.get("location", {}).get("display_name", ""),
                        "job_url": job_data.get("redirect_url", ""),
                        "job_description": job_data.get("description", ""),
                        "salary_range": extract_salary_from_adzuna(job_data),
                        "job_type": job_type,
                        "visa_sponsorship": "visa" in job_description or "h1b" in job_description,
                        "housing_assistance": "housing" in job_description,
                        "relocation_package": extract_relocation_benefits(job_description),
                        "relocation_type": determine_relocation_type(job_description)
                    }
                    
                    jobs.append(job)
    
    except Exception as e:
        logging.error(f"Adzuna API error: {str(e)}")
    
    return jobs

def extract_relocation_benefits(job_description: str) -> Dict:
    """Extract specific relocation benefits from job description"""
    benefits = {}
    description_lower = job_description.lower()
    
    if "visa sponsorship" in description_lower or "h1b" in description_lower:
        benefits["visa_sponsorship"] = True
    
    if "relocation package" in description_lower or "moving allowance" in description_lower:
        benefits["moving_allowance"] = True
    
    if "housing assistance" in description_lower or "temporary accommodation" in description_lower:
        benefits["housing_assistance"] = True
    
    if "immigration support" in description_lower:
        benefits["immigration_support"] = True
    
    if "relocation bonus" in description_lower:
        benefits["relocation_bonus"] = True
    
    return benefits

def extract_salary_range(job_data: Dict) -> str:
    """Extract salary information from job data"""
    salary_min = job_data.get("job_min_salary")
    salary_max = job_data.get("job_max_salary")
    
    if salary_min and salary_max:
        return f"${salary_min:,} - ${salary_max:,}"
    elif salary_min:
        return f"${salary_min:,}+"
    else:
        return "Salary not specified"

def extract_salary_from_adzuna(job_data: Dict) -> str:
    """Extract salary from Adzuna job data"""
    salary_min = job_data.get("salary_min")
    salary_max = job_data.get("salary_max")
    
    if salary_min and salary_max:
        return f"${salary_min:,} - ${salary_max:,}"
    return "Salary not specified"

def extract_job_type(job_title: str) -> str:
    """Extract job type from job title"""
    title_lower = job_title.lower()
    
    if "qa" in title_lower or "quality assurance" in title_lower:
        return "QA Engineer"
    elif "software engineer" in title_lower or "developer" in title_lower:
        return "Software Engineer"
    elif "data scientist" in title_lower:
        return "Data Scientist"
    elif "devops" in title_lower:
        return "DevOps Engineer"
    elif "product manager" in title_lower:
        return "Product Manager"
    else:
        return "Technology"

def extract_moving_allowance(job_description: str) -> str:
    """Extract moving allowance information"""
    description_lower = job_description.lower()
    
    if "moving allowance" in description_lower or "relocation bonus" in description_lower:
        return "Provided"
    elif "relocation package" in description_lower:
        return "Package available"
    else:
        return ""

def determine_relocation_type(job_description: str) -> str:
    """Determine the type of relocation support offered"""
    description_lower = job_description.lower()
    
    if "visa sponsorship" in description_lower or "h1b" in description_lower:
        return "visa_sponsorship"
    elif "internal transfer" in description_lower:
        return "internal_transfer"
    elif "remote" in description_lower and "office" in description_lower:
        return "remote_to_office"
    else:
        return "general_relocation"

def extract_company_email(job_data: Dict) -> str:
    """Extract company email if available"""
    # This would be implemented based on the specific job data structure
    # Most APIs don't provide direct email access for privacy reasons
    return ""

def extract_hr_email(job_data: Dict) -> str:
    """Extract HR email if available"""
    # This would be implemented based on the specific job data structure
    # Most APIs don't provide direct email access for privacy reasons
    return ""
