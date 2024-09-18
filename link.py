from playwright.sync_api import sync_playwright #type: ignore
import os
import time

source_urls = [ 
    'https://vneconomy.vn/thue-tai-chhinh.htm',
    'https://vneconomy.vn/kinh-te-so.htm',
]
base_url = 'https://vneconomy.vn'

def get_link(url):
    elasped_time = 0
    start_time = time.time()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  
        page = browser.new_page()

        page.goto(url)

        page.wait_for_timeout(5000)  

        figures = page.locator('figure.story__thumb a')
        figures_count = figures.count()
        if figures_count > 0:
            links = []
            for i in range(figures_count):
                article = figures.nth(i)
                # Lấy giá trị của thuộc tính href
                link = article.get_attribute('href')
                
                if link:
                    if not link.startswith('http'):
                        link = base_url + link
                    links.append(link)

            with open('link.txt', 'w', encoding='utf-8') as file:
                for link in links:
                    file.write(link + '\n')

            print(f"Saved {len(links)} links to link.txt")
        else:
            print("No links found")

        browser.close()
        end_time = time.time()
        elapsed_time = end_time - start_time
    return links


# def get_url():
#     urls = []
#     for source_url in source_urls:
#         links = get_link(source_url)
#         urls.extend(links[:4])
#     for url in urls:
#         print(url)

# get_url()
