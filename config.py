import os
from typing import List

class Config:
    # Email Configuration
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    EMAIL_FROM = os.getenv("EMAIL_FROM", "alerts@example.com")
    TARGET_EMAIL = os.getenv("TARGET_EMAIL", "geybriel71@gmail.com")
    
    # Database Configuration
    DB_PATH = os.getenv("DB_PATH", "./db/jobs.db")
    
    # Job Matching Configuration
    MIN_MATCH_SCORE = float(os.getenv("MIN_MATCH_SCORE", "70"))
    
    # Comprehensive Skills Keywords (expanded for your profile)
    SKILLS_KEYWORDS = [
        # Core Technical Skills
        "Prisma Access", "PanOS", "DLP", "DataDog", "Kibana", "Grafana",
        "AWS", "Azure", "GCP", "SRE", "Linux", "Kubernetes", "Python", "API",
        "Docker", "Terraform", "Ansible", "Jenkins", "GitLab CI",
        "Monitoring", "Observability", "Security", "Networking",
        
        # Cloud & Infrastructure
        "Cloud Engineer", "DevOps", "Infrastructure", "CI/CD", "Microservices",
        "Serverless", "Containerization", "Orchestration", "Load Balancing",
        
        # Cybersecurity & IAM
        "Cybersecurity", "IAM", "Identity Management", "Zero Trust", "SSO",
        "MFA", "RBAC", "Security Compliance", "SOC", "SIEM", "Threat Detection",
        
        # Data & Analytics
        "Data Engineer", "Data Analyst", "ETL", "Data Pipeline", "SQL", "NoSQL",
        "Data Warehouse", "Big Data", "Machine Learning", "Business Intelligence",
        "Database Admin", "DBA", "PostgreSQL", "MySQL", "MongoDB", "Redis",
        
        # Customer-Facing Technical Roles
        "Customer Success Engineer", "Technical Account Manager", "Solutions Engineer",
        "Customer Support Engineer", "Senior Support Engineer", "Customer Service Specialist",
        "Technical Support", "Implementation Engineer", "Professional Services",
        
        # Additional Technical Skills
        "JavaScript", "React", "Node.js", "Java", "Go", "Rust", "Shell Scripting",
        "Git", "REST API", "GraphQL", "Web Services", "System Administration"
    ]
    
    # Enhanced Relocation Keywords with International Focus
    RELOCATION_PHRASES = [
        # Direct Immigration Terms
        "visa sponsorship", "lmia", "work permit", "permanent residence", "pr application",
        "express entry", "provincial nominee", "temporary foreign worker", "skilled worker",
        "canada immigration", "canadian permanent resident", "immigration support",
        "china work visa", "z visa", "china residence permit", "foreign expert",
        "china relocation", "expat package", "international assignment",
        
        # Relocation Benefits
        "relocation package", "relocation assistance", "relocation support", "relocation bonus",
        "relocation provided", "relocation offered", "moving assistance", "sign-on bonus for relocation",
        "flight", "housing", "housing allowance", "accommodation", "dependent documentation",
        "family sponsorship", "dependent visa", "spouse work permit",
        "expat benefits", "international relocation", "overseas assignment",
        
        # Canadian-Specific Terms
        "canada", "canadian", "toronto", "vancouver", "montreal", "calgary", "ottawa",
        "edmonton", "winnipeg", "halifax", "victoria", "quebec", "alberta", "ontario",
        "british columbia", "manitoba", "nova scotia", "saskatchewan", "new brunswick",
        
        # Chinese-Specific Terms
        "china", "chinese", "beijing", "shanghai", "shenzhen", "guangzhou", "hangzhou",
        "chengdu", "xian", "tianjin", "chongqing", "suzhou", "nanjing", "wuhan",
        "english speaking", "english required", "international team", "multinational",
        
        # Immigration Programs
        "federal skilled worker", "federal skilled trades", "canadian experience class",
        "atlantic immigration", "rural and northern immigration", "startup visa",
        "self-employed", "investor", "entrepreneur", "family class",
        
        # Work Authorization
        "open work permit", "closed work permit", "post-graduate work permit",
        "global talent stream", "intra-company transfer", "nafta work permit",
        "comprehensive economic and trade agreement", "ceta"
    ]
    
    # Enhanced Relocation Detection Keywords (for scoring)
    RELOCATION_SCORING_KEYWORDS = {
        'high_confidence': [
            'visa sponsorship', 'lmia', 'work permit', 'relocation package',
            'permanent residence', 'express entry', 'immigration support',
            'relocation provided', 'relocation offered', 'china work visa',
            'z visa', 'expat package', 'international assignment'
        ],
        'medium_confidence': [
            'canada', 'canadian', 'relocation assistance', 'housing allowance',
            'dependent documentation', 'family sponsorship', 'moving assistance',
            'relocation support', 'relocation bonus', 'china', 'chinese',
            'english speaking', 'international team', 'expat benefits'
        ],
        'low_confidence': [
            'toronto', 'vancouver', 'montreal', 'calgary', 'ottawa',
            'beijing', 'shanghai', 'shenzhen', 'guangzhou'
        ]
    }
    
    # Crawler Configuration
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
    REQUEST_DELAY = float(os.getenv("REQUEST_DELAY", "1.0"))
    MAX_JOBS_PER_SOURCE = int(os.getenv("MAX_JOBS_PER_SOURCE", "5"))

    # Search locations to include (order matters for preference)
    SEARCH_LOCATIONS = [
        loc.strip() for loc in os.getenv("SEARCH_LOCATIONS", "Canada,United States,China").split(",") if loc.strip()
    ]
    
    # Comprehensive Search Terms for Different Sources
    INDEED_SEARCH_TERMS = [
        "software engineer relocation canada",
        "devops engineer visa sponsorship",
        "sre canada work permit",
        "python developer relocation package",
        "cloud engineer canada immigration",
        "cybersecurity engineer relocation",
        "data engineer canada work permit",
        "customer success engineer relocation",
        "senior support engineer canada",
        "iam engineer visa sponsorship",
        "software engineer china english",
        "devops engineer china expat",
        "cloud engineer china international",
        "cybersecurity engineer china english speaking"
    ]
    
    JOBBANK_SEARCH_TERMS = [
        "software developer",
        "devops engineer", 
        "site reliability engineer",
        "python developer",
        "cloud engineer",
        "cybersecurity engineer",
        "data engineer",
        "customer success engineer",
        "senior support engineer",
        "iam engineer"
    ]
    
    GLASSDOOR_SEARCH_TERMS = [
        "software engineer canada",
        "devops engineer canada",
        "sre canada",
        "python developer canada",
        "cloud engineer canada",
        "cybersecurity engineer canada",
        "data engineer canada",
        "customer success engineer canada",
        "senior support engineer canada",
        "iam engineer canada",
        "software engineer china english",
        "devops engineer china expat",
        "cloud engineer china international"
    ]
    
    LINKEDIN_SEARCH_TERMS = [
        "software engineer canada relocation",
        "devops engineer canada visa",
        "cloud engineer canada immigration",
        "cybersecurity engineer canada sponsorship",
        "data engineer canada work permit",
        "customer success engineer canada relocation",
        "senior support engineer canada immigration",
        "iam engineer canada sponsorship",
        "software engineer china english speaking",
        "devops engineer china expat package",
        "cloud engineer china international team",
        "cybersecurity engineer china english required"
    ]
    
    # Additional Job Sources
    ADDITIONAL_SOURCES = {
        'monster_ca': [
            "software engineer canada",
            "devops engineer canada",
            "cloud engineer canada",
            "cybersecurity engineer canada"
        ],
        'workopolis': [
            "software engineer",
            "devops engineer",
            "cloud engineer",
            "cybersecurity engineer"
        ],
        'eluta_ca': [
            "software engineer",
            "devops engineer",
            "cloud engineer",
            "cybersecurity engineer"
        ],
        'careerbeacon': [
            "software engineer",
            "devops engineer",
            "cloud engineer",
            "cybersecurity engineer"
        ]
    }
    
    @classmethod
    def validate(cls) -> List[str]:
        """Validate configuration and return list of issues"""
        issues = []
        
        if not cls.SENDGRID_API_KEY:
            issues.append("SENDGRID_API_KEY is required")
        
        if not cls.TARGET_EMAIL:
            issues.append("TARGET_EMAIL is required")
            
        if cls.MIN_MATCH_SCORE < 0 or cls.MIN_MATCH_SCORE > 100:
            issues.append("MIN_MATCH_SCORE must be between 0 and 100")
            
        return issues 