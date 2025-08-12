import requests
from bs4 import BeautifulSoup
import time
import logging
from config import Config

def get_linkedin_jobs():
    """Scrape LinkedIn for relevant jobs with relocation focus across configured locations"""
    jobs = []
    try:
        for term in Config.LINKEDIN_SEARCH_TERMS:
            for location in Config.SEARCH_LOCATIONS:
                url = (
                    "https://www.linkedin.com/jobs/search/?"
                    f"keywords={term.replace(' ', '%20')}&"
                    f"location={location.replace(' ', '%20')}&"
                    "f_LF=f_AL&f_E=2%2C3%2C4"
                )
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                }

                response = requests.get(url, headers=headers, timeout=Config.REQUEST_TIMEOUT)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    job_cards = soup.find_all('div', class_='base-card')

                    for card in job_cards[:Config.MAX_JOBS_PER_SOURCE]:
                        try:
                            title_elem = card.find('h3', class_='base-search-card__title')
                            title = title_elem.get_text(strip=True) if title_elem else ''

                            company_elem = card.find('h4', class_='base-search-card__subtitle')
                            company = company_elem.get_text(strip=True) if company_elem else 'Unknown'

                            location_elem = card.find('span', class_='job-search-card__location')
                            loc_text = location_elem.get_text(strip=True) if location_elem else location

                            link_elem = card.find('a', class_='base-card__full-link')
                            job_url = link_elem['href'] if link_elem and link_elem.get('href') else ''

                            description_elem = card.find('div', class_='base-search-card__metadata')
                            description = description_elem.get_text(strip=True) if description_elem else ''

                            if title and company:
                                job = {
                                    'title': title,
                                    'company': company,
                                    'location': loc_text,
                                    'url': job_url,
                                    'description': description,
                                    'source': 'LinkedIn'
                                }
                                jobs.append(job)

                        except Exception as e:
                            logging.warning(f"Error parsing LinkedIn job card: {e}")
                            continue

                time.sleep(Config.REQUEST_DELAY)

    except Exception as e:
        logging.error(f"Error scraping LinkedIn: {e}")

    return jobs 