from airflow import DAG # type: ignore
from airflow.operators.python_operator import PythonOperator # type: ignore
from datetime import datetime, timedelta
import time
from playwright.sync_api import sync_playwright # type: ignore
from pymongo import MongoClient # type: ignore

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 9, 1),  # Điều chỉnh thời gian bắt đầu
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'news_crawl_pipeline',  # Tên DAG
    default_args=default_args,
    description='A pipeline to crawl news articles and store them in MongoDB',
    schedule_interval=timedelta(days=1),  # Lịch chạy hàng ngày
)

def get_article(url):
    elasped_time = 0
    start_time = time.time()
    print(f"Fetching article from {url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(3000)

        # Take category
        category_element = page.locator('h1.category-main a')
        category = category_element.text_content().strip() if category_element else 'No category'
        
        # Take meta
        meta_element = page.locator('div.detail__meta')
        meta = meta_element.text_content().strip() if meta_element else 'No meta'
        
        # Take title
        title_element = page.locator('h1.detail__title')
        title = title_element.text_content().strip() if title_element else 'No title'
        
        # Take content
        content_element = page.locator('div.detail__content')
        content_html = content_element.inner_html() if content_element else 'No content HTML'
        paragraph_elements = content_element.locator('p, h4').all_text_contents() if content_element else []
        content = '\n'.join([p.strip() for p in paragraph_elements])

        # Save to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
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
        collection.insert_one(newscrawl)

        browser.close()
        end_time = time.time()
        elasped_time += end_time - start_time
        print(f"Saved article from {url}")
    return elasped_time

# Task để chạy hàm crawl
def crawl_task():
    url_list = [
        'https://vneconomy.vn/10-thien-duong-thue-lon-nhat-the-gioi.htm',
        'https://vneconomy.vn/thong-tin-ve-gan-9-000-ho-so-thue-dat-bi-tac-tai-tp-hcm.htm',
        'https://vneconomy.vn/gan-100-doanh-nghiep-rat-hai-long-va-hai-long-doi-voi-hai-quan.htm',
        'https://vneconomy.vn/nganh-hai-quan-xu-ly-11-555-vu-vi-pham-tap-trung-ra-soat-nhieu-mat-hang-rui-ro-cuoi-nam.htm',
        'https://vneconomy.vn/ha-tinh-nganh-cong-nghiep-khai-khoang-len-ngoi.htm',
        'https://vneconomy.vn/du-giam-va-gia-han-thue-gan-90-nghin-ty-dong-nhung-ngan-sach-van-som-can-dich.htm'
    ]
    for url in url_list:
        get_article(url)

# Tạo PythonOperator
crawl_operator = PythonOperator(
    task_id='crawl_news_task',
    python_callable=crawl_task,
    dag=dag,
)

crawl_operator
