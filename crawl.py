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
        client = MongoClient('localhost', 27017)
        
        db = client['news4']
        collection = db['newscrawl']

        newscrawl = {
            'url': url
        }

        if collection.find_one({'url': url}) != None:
            print(f"Article from {url} already exists")
            return 0
        else:
        # Wait for page to load content (adjust timeout as needed)
            page.wait_for_timeout(3000)



            # Take category
            category_element = page.locator('h1.category-main a')
            category = category_element.text_content().strip() if category_element else 'No category'
            #category_html = category_element.inner_html() if category_element else 'No category HTML'

            # Take meta
            meta_element = page.locator('div.detail__meta')
            meta = meta_element.text_content().strip() if meta_element else 'No meta'
            #meta_html = meta_element.inner_html() if meta_element else 'No meta HTML'

            # Take title
            title_element = page.locator('h1.detail__title')
            title = title_element.text_content().strip() if title_element else 'No title'
            #title_html = title_element.inner_html() if title_element else 'No title HTML'

            # Take content
            content_element = page.locator('div.detail__content')
            content_html = content_element.inner_html() if content_element else 'No content HTML'
            paragraph_elements = content_element.locator('p, h4').all_text_contents() if content_element else []
            content = '\n'.join([p.strip() for p in paragraph_elements])

            # Process and save data
            newscrawl = {
                'url': url,
                'category': category,
                'meta': meta,
                'title': title,
                'content': content,
                'content_html': content_html
            }
            collection.insert_one(newscrawl)
        browser.close()
        end_time = time.time()
        elasped_time += end_time - start_time
        
    return elasped_time

# url_list = [
#         'https://vneconomy.vn/10-thien-duong-thue-lon-nhat-the-gioi.htm',
#         'https://vneconomy.vn/thong-tin-ve-gan-9-000-ho-so-thue-dat-bi-tac-tai-tp-hcm.htm',
#         'https://vneconomy.vn/gan-100-doanh-nghiep-rat-hai-long-va-hai-long-doi-voi-hai-quan.htm',
#         'https://vneconomy.vn/nganh-hai-quan-xu-ly-11-555-vu-vi-pham-tap-trung-ra-soat-nhieu-mat-hang-rui-ro-cuoi-nam.htm',
#         'https://vneconomy.vn/ha-tinh-nganh-cong-nghiep-khai-khoang-len-ngoi.htm',
#         'https://vneconomy.vn/du-giam-va-gia-han-thue-gan-90-nghin-ty-dong-nhung-ngan-sach-van-som-can-dich.htm'
# ]

