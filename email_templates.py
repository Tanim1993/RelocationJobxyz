from models import Job
import json

def generate_email_content(job: Job) -> dict:
    """
    Generate personalized email content for relocation job applications
    """
    # Parse relocation package
    relocation_package = {}
    if job.relocation_package:
        try:
            relocation_package = json.loads(job.relocation_package)
        except json.JSONDecodeError:
            relocation_package = {'details': job.relocation_package}
    
    # Generate subject line
    subject = f"Application for {job.title} - Experienced Professional Seeking Relocation Opportunity"
    
    # Generate email body
    body = f"""Dear Hiring Manager / HR Team,

I hope this email finds you well. I am writing to express my strong interest in the {job.title} position at {job.company}. As a professional actively seeking relocation opportunities, I am particularly drawn to this role due to your company's support for international talent and relocation assistance.

**Why I'm Interested in This Relocation Opportunity:**

• Your commitment to supporting international professionals aligns perfectly with my career goals
• The {job.title} role represents an excellent opportunity to contribute my expertise while building a new life in {job.location}
"""

    # Add relocation-specific content based on available benefits
    if job.visa_sponsorship:
        body += """• I greatly appreciate your company's visa sponsorship program, which demonstrates a commitment to global talent acquisition
"""

    if job.housing_assistance:
        body += """• The housing assistance offered would be invaluable during my relocation transition
"""

    if job.moving_allowance:
        body += """• The relocation package support would significantly ease the financial aspects of international relocation
"""

    body += f"""
**My Background and Relocation Readiness:**

I am a skilled professional with extensive experience in {job.job_type or 'technology'} and am fully prepared for international relocation. My qualifications include:

• Strong technical background with proven track record in similar roles
• Experience working in diverse, multicultural environments
• Full legal authorization to work upon visa approval
• Flexibility and adaptability essential for successful international relocation
• Commitment to long-term growth with companies that invest in their international employees

**Relocation Timeline and Logistics:**

I am prepared to begin the relocation process immediately upon offer acceptance and can:
• Start the visa application process without delay
• Coordinate with your relocation support team for smooth transition
• Commit to long-term employment in appreciation of the relocation investment
• Adapt quickly to new cultural and professional environments

**Next Steps:**

I would welcome the opportunity to discuss how my background aligns with your needs and to learn more about your relocation support process. I am available for interviews via video call across different time zones and can provide any additional documentation required for the visa sponsorship process.

Thank you for considering international candidates and for your commitment to supporting global talent. I look forward to the possibility of contributing to {job.company}'s success while building my career in {job.location}.

Best regards,
[Your Name]
[Your Contact Information]
[Your Current Location]

---
**Attachments:**
• Resume/CV
• Portfolio (if applicable)
• References upon request

**Note:** I am specifically interested in this position due to the relocation support offered and am prepared for all aspects of international relocation including visa processes, cultural adaptation, and long-term commitment to your organization."""

    # Add specific relocation package details if available
    if relocation_package:
        body += f"\n\n**Regarding Your Relocation Package:**\n"
        for benefit, value in relocation_package.items():
            if value:
                body += f"• I understand you offer {benefit.replace('_', ' ').title()}: {value}\n"

    return {
        'subject': subject,
        'body': body,
        'recipient_email': job.hr_email or job.company_email or 'hr@company.com',
        'relocation_focused': True
    }

def generate_followup_email(job: Job) -> dict:
    """Generate follow-up email for relocation applications"""
    
    subject = f"Following up on {job.title} Application - Relocation Candidate"
    
    body = f"""Dear Hiring Team,

I hope this email finds you well. I wanted to follow up on my application for the {job.title} position at {job.company}, submitted [DATE].

As a candidate specifically seeking relocation opportunities, I remain very interested in this role and wanted to reiterate my enthusiasm for the position and your relocation support program.

**Quick Recap of My Interest:**
• Actively seeking international relocation with visa sponsorship
• Ready to commit long-term in appreciation of relocation investment
• Prepared for immediate visa application process upon offer

I understand that reviewing applications, especially for international candidates, takes time. I wanted to confirm that:

1. My application and documents were received successfully
2. I remain available for interviews across time zones
3. I can provide any additional documentation needed for visa processing

Please let me know if there are any updates on the hiring timeline or if you need any additional information from me.

Thank you again for your time and consideration. I look forward to hearing from you.

Best regards,
[Your Name]"""

    return {
        'subject': subject,
        'body': body,
        'recipient_email': job.hr_email or job.company_email or 'hr@company.com',
        'relocation_focused': True
    }

# Predefined email templates for different scenarios
EMAIL_TEMPLATES = {
    'initial_application': {
        'subject': 'Application for {job_title} - International Candidate Seeking Relocation',
        'template': 'relocation_application_template'
    },
    'follow_up': {
        'subject': 'Following up on {job_title} Application - Relocation Candidate', 
        'template': 'relocation_followup_template'
    },
    'visa_inquiry': {
        'subject': 'Inquiry about Visa Sponsorship Process for {job_title}',
        'template': 'visa_inquiry_template'
    },
    'relocation_package_inquiry': {
        'subject': 'Questions about Relocation Package for {job_title}',
        'template': 'relocation_package_template'
    }
}
