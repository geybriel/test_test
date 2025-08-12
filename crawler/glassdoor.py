import requests
from bs4 import BeautifulSoup
import time
import logging

def get_glassdoor_jobs():
    """Scrape Glassdoor Canada for relevant jobs"""
    jobs = []
    try:
        # Glassdoor search for tech jobs in Canada
        search_terms = [
            "software engineer canada",
            "devops engineer canada",
            "sre canada",
            "python developer canada"
        ]
        
        for term in search_terms:
            url = f"https://www.glassdoor.ca/Job/canada-{term.replace(' ', '-')}-jobs-SRCH_IL.0,6_IN3_KO7,{len(term.split()) + 7}.htm"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract job listings from Glassdoor
                job_cards = soup.find_all('li', class_='react-job-listing')
                
                for card in job_cards[:5]:  # Limit to 5 jobs per search term
                    try:
                        title_elem = card.find('a', class_='jobLink')
                        company_elem = card.find('a', class_='job-search-key-l2wjgv')
                        location_elem = card.find('span', class_='job-search-key-iiw14i')
                        
                        if title_elem:
                            job = {
                                'title': title_elem.get_text(strip=True),
                                'company': company_elem.get_text(strip=True) if company_elem else 'Unknown',
                                'location': location_elem.get_text(strip=True) if location_elem else '',
                                'url': 'https://www.glassdoor.ca' + title_elem['href'] if title_elem.get('href') else '',
                                'description': '',  # Would need to scrape individual job pages
                                'source': 'Glassdoor'
                            }
                            jobs.append(job)
                    except Exception as e:
                        logging.warning(f"Error parsing Glassdoor job card: {e}")
                        continue
                        
            time.sleep(1)  # Be respectful to the server
            
    except Exception as e:
        logging.error(f"Error scraping Glassdoor: {e}")
    
    return jobs 