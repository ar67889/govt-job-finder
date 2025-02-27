from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.cache import cache
from .scraper import scrape_data
from .scraper1 import scrape_allgovernmentjobs_selenium, format_state_name

def job_listings(request):
    search_query = str(request.GET.get('search', '')).strip()
    page_no = request.GET.get('page_no', '1')
    filter_type = request.GET.get('filter', 'all')
    category = request.GET.get('category', '').strip()

    try:
        page_no = int(page_no)
        if page_no < 1:
            page_no = 1
    except ValueError:
        page_no = 1

    # Create a unique cache key based on the query parameters
    cache_key = f"jobs_{search_query}_{category}_{filter_type}"
    # Try to get the data from cache first
    scraped_data = cache.get(cache_key)
    
    if scraped_data is None:
        scraped_data_1, scraped_data_2 = [], []
    
        if category:
            # Fetch jobs from the selected category (always get multiple pages)
            scraped_data_2 = scrape_allgovernmentjobs_selenium(category=category, max_pages=10)
        elif search_query:
            formatted_state = format_state_name(search_query)
            if filter_type in ('all', 'services'):
                scraped_data_1 = scrape_data(search_query)
            if filter_type in ('all', 'jobs'):
                scraped_data_2 = scrape_allgovernmentjobs_selenium(state_name=formatted_state, max_pages=10)
    
        # Combine results with source labels
        scraped_data = (
            [{**job, 'source': 'Government Services'} for job in scraped_data_1] +
            [{**job, 'source': 'All Government Jobs'} for job in scraped_data_2]
        )
        # Store the scraped data in the cache for 1 hour (3600 seconds)
        cache.set(cache_key, scraped_data, timeout=3600)
    
    # Apply Django pagination on the cached data
    paginator = Paginator(scraped_data, 20)
    page = paginator.get_page(page_no)

    context = {
        'scraped_data': page.object_list,
        'search_query': search_query,
        'filter_type': filter_type,
        'category': category,
        'page_no': page_no,
        'paginator': paginator,
        'page': page,
    }

    return render(request, 'home.html', context)
