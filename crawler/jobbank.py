import requests
from bs4 import BeautifulSoup
import time
import logging

def get_jobbank_jobs():
    """Scrape JobBank Canada for relevant jobs"""
    jobs = []
    try:
        # JobBank Canada search for tech jobs
        search_terms = [
            "software developer",
            "devops engineer", 
            "site reliability engineer",
            "python developer"
        ]
        
        for term in search_terms:
            url = f"https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring={term.replace(' ', '+')}&locationstring=Canada"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract job listings from JobBank
                job_cards = soup.find_all('article', class_='result')
                
                for card in job_cards[:5]:  # Limit to 5 jobs per search term
                    try:
                        title_elem = card.find('a', class_='resultJobItem')
                        company_elem = card.find('li', class_='business')
                        location_elem = card.find('li', class_='location')
                        
                        if title_elem:
                            job = {
                                'title': title_elem.get_text(strip=True),
                                'company': company_elem.get_text(strip=True) if company_elem else 'Unknown',
                                'location': location_elem.get_text(strip=True) if location_elem else '',
                                'url': 'https://www.jobbank.gc.ca' + title_elem['href'] if title_elem.get('href') else '',
                                'description': '',  # Would need to scrape individual job pages
                                'source': 'JobBank'
                            }
                            jobs.append(job)
                    except Exception as e:
                        logging.warning(f"Error parsing JobBank job card: {e}")
                        continue
                        
            time.sleep(1)  # Be respectful to the server
            
    except Exception as e:
        logging.error(f"Error scraping JobBank: {e}")
    
    return jobs 