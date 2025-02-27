from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Category-to-URL mapping
CATEGORY_URLS = {
    "Medical": "medical-jobs",
    "Engineering": "engineering-jobs",
    "Law": "llb-jobs",
    "Finance": "mba-jobs",
    "Nurse": "staff-nurse-jobs",
    "Pharmacy": "pharmacy-jobs",
    "Dental": "bds-jobs",
    "Aviation": "aeronautical-engineering-jobs",
    "Naval": "indian-navy-recruitment",
    "Hotel Management": "hotel-management-jobs",
    "Sports Quota": "sports-quota-jobs",
    "Architecture": "architectural-engineering-jobs",
    "ITI/Diploma": "iti-jobs",
    "Arts": "m-a-jobs",
    "Agriculture": "agricultural-engineering-job",
    "Teacher Training": "b-ed-jobs",
    "Any Degree": "any-degree-jobs"
}

def format_state_name(state_name):
    """Converts state name into URL-friendly format (e.g., 'Tamil Nadu' → 'tamil-nadu')."""
    if not isinstance(state_name, str):  
        state_name = str(state_name)  
    return state_name.lower().replace(" ", "-")


def scrape_allgovernmentjobs_selenium(category=None, state_name=None, start_page=1, max_pages=10):
    """Scrapes job listings based on category selection or state-based search, starting from the given page."""
    
    if category and category in CATEGORY_URLS:
        base_url = f"https://allgovernmentjobs.in/{CATEGORY_URLS[category]}"
        pagination_format = f"https://allgovernmentjobs.in/{CATEGORY_URLS[category]}/page/{{}}"  # Category pagination
    elif state_name:
        formatted_state = format_state_name(state_name)
        base_url = f"https://allgovernmentjobs.in/govt-jobs-in-{formatted_state}"
        pagination_format = f"https://allgovernmentjobs.in/govt-jobs-in-{formatted_state}/page/{{}}"  # State-based pagination
    else:
        return []  # No valid category or state provided

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    all_jobs = []

    # Start scraping from the provided start_page number
    for page_num in range(start_page, start_page + max_pages):
        url = base_url if page_num == 1 else pagination_format.format(page_num)
        print(f"Scraping: {url}")  # Debugging output

        driver.get(url)
        time.sleep(3)  # Wait for page to load

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        job_cards = soup.find_all('div', class_='card-body p-3')

        if not job_cards:
            print(f"No jobs found on page {page_num}. Stopping pagination.")
            break

        for job_card in job_cards:
            title_tag = job_card.find('div', class_='card-title h6 mb-0')
            title = title_tag.text.strip() if title_tag else 'No title available'

            date_tag = job_card.find('div', class_='mb-1 text-secondary _ln')
            job_date = date_tag.text.strip() if date_tag else 'No date available'

            description_tag = job_card.find('div', class_='content')
            description = description_tag.text.strip() if description_tag else 'No description available'

            apply_tag = job_card.find('div', class_='mt-3').find('a', href=True) if job_card.find('div', class_='mt-3') else None
            apply_link = apply_tag['href'] if apply_tag else 'No link available'

            all_jobs.append({
                'title': title,
                'date': job_date,
                'description': description,
                'apply_link': apply_link
            })

        print(f"Scraped {len(job_cards)} jobs from page {page_num}")

    driver.quit()
    return all_jobs
