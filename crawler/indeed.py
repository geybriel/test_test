import requests
from bs4 import BeautifulSoup
import time
import logging

def get_indeed_jobs():
    """Scrape Indeed Canada for relevant jobs"""
    jobs = []
    try:
        # Search for tech jobs with relocation keywords
        search_terms = [
            "software engineer relocation canada",
            "devops engineer visa sponsorship",
            "sre canada work permit",
            "python developer relocation package"
        ]
        
        for term in search_terms:
            url = f"https://ca.indeed.com/jobs?q={term.replace(' ', '+')}&l=Canada"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract job listings (this is a simplified version)
                job_cards = soup.find_all('div', class_='job_seen_beacon')
                
                for card in job_cards[:5]:  # Limit to 5 jobs per search term
                    try:
                        title_elem = card.find('h2', class_='jobTitle')
                        company_elem = card.find('span', class_='companyName')
                        location_elem = card.find('div', class_='companyLocation')
                        link_elem = card.find('a', class_='jcs-JobTitle')
                        
                        if title_elem and company_elem:
                            job = {
                                'title': title_elem.get_text(strip=True),
                                'company': company_elem.get_text(strip=True),
                                'location': location_elem.get_text(strip=True) if location_elem else '',
                                'url': 'https://ca.indeed.com' + link_elem['href'] if link_elem else '',
                                'description': '',  # Would need to scrape individual job pages
                                'source': 'Indeed'
                            }
                            jobs.append(job)
                    except Exception as e:
                        logging.warning(f"Error parsing job card: {e}")
                        continue
                        
            time.sleep(1)  # Be respectful to the server
            
    except Exception as e:
        logging.error(f"Error scraping Indeed: {e}")
    
    return jobs 