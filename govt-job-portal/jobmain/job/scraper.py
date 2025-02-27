import requests
from bs4 import BeautifulSoup

def scrape_data(search_term, max_pages=10):
    """Scrape government services from services.india.gov.in across multiple pages"""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    job_listings = []
    for page_no in range(1, max_pages + 1):  # Loop through multiple pages
        url = f"https://services.india.gov.in/service/search?kw={search_term}&page_no={page_no}"
        try:
            response = requests.get(url, headers=headers, timeout=20)
            if response.status_code != 200:
                print(f"Failed to retrieve the page: {response.status_code}")
                break

            soup = BeautifulSoup(response.content, 'html.parser')

            page_jobs = []
            for job in soup.find_all('div', class_='edu-lern-con'):
                job_link = job.find('a', class_='ext-link')
                job_description = job.find('p')

                if job_link:
                    title = job_link.text.strip()
                    apply_link = job_link['href']
                    description = job_description.text.strip() if job_description else 'No description available'

                    page_jobs.append({
                        'title': title,
                        'apply_link': apply_link,
                        'description': description,
                    })

            if not page_jobs:
                break  # Stop when no more results are found
            job_listings.extend(page_jobs)

        except requests.RequestException as e:
            print(f"Error fetching page {page_no}: {e}")
            break

    return job_listings
