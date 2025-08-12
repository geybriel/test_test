from .indeed import get_indeed_jobs
from .jobbank import get_jobbank_jobs
from .glassdoor import get_glassdoor_jobs
from .linkedin import get_linkedin_jobs
from .monster_ca import get_monster_ca_jobs
from .workopolis import get_workopolis_jobs
import logging

logger = logging.getLogger(__name__)

def aggregate_jobs():
    """Aggregate jobs from all sources with error handling"""
    all_jobs = []
    
    # Define sources with their functions
    sources = [
        ("Indeed", get_indeed_jobs),
        ("JobBank", get_jobbank_jobs),
        ("Glassdoor", get_glassdoor_jobs),
        ("LinkedIn", get_linkedin_jobs),
        ("Monster Canada", get_monster_ca_jobs),
        ("Workopolis", get_workopolis_jobs),
    ]
    
    for source_name, source_func in sources:
        try:
            logger.info(f"Scraping {source_name}...")
            jobs = source_func()
            all_jobs.extend(jobs)
            logger.info(f"Found {len(jobs)} jobs from {source_name}")
        except Exception as e:
            logger.error(f"Error scraping {source_name}: {e}")
            continue
    
    logger.info(f"Total jobs aggregated: {len(all_jobs)}")
    return all_jobs
