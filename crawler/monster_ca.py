import requests
from bs4 import BeautifulSoup
import time
import logging
from config import Config

def get_monster_ca_jobs():
    """Scrape Monster Canada for relevant jobs"""
    jobs = []
    try:
        for term in Config.ADDITIONAL_SOURCES['monster_ca']:
            url = f"https://www.monster.ca/jobs/search?q={term.replace(' ', '+')}&where=Canada"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            }
            
            response = requests.get(url, headers=headers, timeout=Config.REQUEST_TIMEOUT)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract job listings from Monster
                job_cards = soup.find_all('div', class_='job-cardstyle__JobCardComponent')
                
                for card in job_cards[:Config.MAX_JOBS_PER_SOURCE]:
                    try:
                        title_elem = card.find('h2', class_='title')
                        company_elem = card.find('div', class_='company')
                        location_elem = card.find('div', class_='location')
                        link_elem = card.find('a', class_='job-link')
                        
                        if title_elem and company_elem:
                            job = {
                                'title': title_elem.get_text(strip=True),
                                'company': company_elem.get_text(strip=True),
                                'location': location_elem.get_text(strip=True) if location_elem else '',
                                'url': 'https://www.monster.ca' + link_elem['href'] if link_elem and link_elem.get('href') else '',
                                'description': '',
                                'source': 'Monster Canada'
                            }
                            jobs.append(job)
                    except Exception as e:
                        logging.warning(f"Error parsing Monster job card: {e}")
                        continue
                        
            time.sleep(Config.REQUEST_DELAY)
            
    except Exception as e:
        logging.error(f"Error scraping Monster Canada: {e}")
    
    return jobs 