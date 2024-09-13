from playwright.sync_api import sync_playwright # type: ignore
from pymongo import MongoClient # type: ignore
import time

def get_article(url):
    elasped_time = 0
    start_time = time.time()
    print(f"Fetching article from {url}")

    with sync_playwright() as p:
        # Use Chromium browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        
        # Wait for page to load content (adjust timeout as needed)
        page.wait_for_timeout(3000)

        # Take category
        category_element = page.locator('h1.category-main a')
        category = category_element.text_content().strip() if category_element else 'No category'
        category_html = category_element.inner_html() if category_element else 'No category HTML'

        # Take meta
        meta_element = page.locator('div.detail__meta')
        meta = meta_element.text_content().strip() if meta_element else 'No meta'
        meta_html = meta_element.inner_html() if meta_element else 'No meta HTML'

        # Take title
        title_element = page.locator('h1.detail__title')
        title = title_element.text_content().strip() if title_element else 'No title'
        title_html = title_element.inner_html() if title_element else 'No title HTML'

        # Take content
        content_element = page.locator('div.detail__content')
        content_html = content_element.inner_html() if content_element else 'No content HTML'
        paragraph_elements = content_element.locator('p, h4').all_text_contents() if content_element else []
        content = '\n'.join([p.strip() for p in paragraph_elements])

        # Process and save data
        client = MongoClient('localhost', 27017)
        db = client['news']
        collection = db['newscrawl']

        newscrawl = {
            'url': url,
            'category': category,
            'meta': meta,
            'title': title,
            'content': content,
            'content_html': content_html
        }

        if collection.find_one({'url': url}) is None:
            collection.insert_one(newscrawl)
            print(f"Saved article from {url}")
        else:
            print(f"Article from {url} already exists")
            
        browser.close()
        end_time = time.time()
        elasped_time += end_time - start_time
        
    return elasped_time
        
