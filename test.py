# from airflow import DAG # type: ignore
# from airflow.operators.python_operator import PythonOperator # type: ignore
# from datetime import datetime, timedelta
# import time
# from playwright.sync_api import sync_playwright # type: ignore
# from pymongo import MongoClient # type: ignore

# default_args = {
#     'owner': 'airflow',
#     'depends_on_past': False,
#     'start_date': datetime(2024, 9, 13),  # Điều chỉnh thời gian bắt đầu
#     'email_on_failure': False,
#     'email_on_retry': False,
#     'retries': 1,
#     'retry_delay': timedelta(minutes=5),
# }

# dag = DAG(
#     'test1',  # Tên DAG
#     default_args=default_args,
#     description='A pipeline to crawl news articles and store them in MongoDB',
#     schedule_interval=timedelta(days=1),  # Lịch chạy hàng ngày
#     max_active_runs=1,
#     concurrency=16,
# )

# def get_article(url, **kwargs):
#     start_time = time.time()
#     print(f"Fetching article from {url}")

#     with sync_playwright() as p:
#         # Use Chromium browser
#         browser = p.chromium.launch(headless=True)
#         page = browser.new_page()
#         page.goto(url)
#         client = MongoClient('localhost', 27017)
        
#         db = client['news3']
#         collection = db['newscrawl']

#         newscrawl = {
#             'url': url
#         }

#         if collection.find_one({'url': url}) != None:
#             print(f"Article from {url} already exists")
#             return 0
#         else:
#         # Wait for page to load content (adjust timeout as needed)
#             page.wait_for_timeout(3000)



#             # Take category
#             category_element = page.locator('h1.category-main a')
#             category = category_element.text_content().strip() if category_element else 'No category'
#             #category_html = category_element.inner_html() if category_element else 'No category HTML'

#             # Take meta
#             meta_element = page.locator('div.detail__meta')
#             meta = meta_element.text_content().strip() if meta_element else 'No meta'
#             #meta_html = meta_element.inner_html() if meta_element else 'No meta HTML'

#             # Take title
#             title_element = page.locator('h1.detail__title')
#             title = title_element.text_content().strip() if title_element else 'No title'
#             #title_html = title_element.inner_html() if title_element else 'No title HTML'

#             # Take content
#             content_element = page.locator('div.detail__content')
#             content_html = content_element.inner_html() if content_element else 'No content HTML'
#             paragraph_elements = content_element.locator('p, h4').all_text_contents() if content_element else []
#             content = '\n'.join([p.strip() for p in paragraph_elements])

#             # Process and save data
#             newscrawl = {
#                 'url': url,
#                 'category': category,
#                 'meta': meta,
#                 'title': title,
#                 'content': content,
#                 'content_html': content_html
#             }
#             collection.insert_one(newscrawl)
#             print(f"Saved article from {url} to MongoDB")
#         browser.close()

#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     print(f"Elapsed time for {url}: {elapsed_time} seconds")
#     kwargs['ti'].xcom_push(key=f'elapsed_time_{url}', value=elapsed_time)

# def record_time(**kwargs):
#     ti = kwargs['ti']
    
#     for url in url_list:
#         elapsed_time = ti.xcom_pull(key=f'elapsed_time_{url}', task_ids=f'crawl_{url_list.index(url)}')
#         if elapsed_time is not None:
#             with open('/home/hgf/airflow/dags/total_elapsed_time2.txt', 'a', encoding='utf-8') as file:
#                 file.write(f'{url}: {elapsed_time}\n')

# url_list = [
#     'https://vneconomy.vn/10-thien-duong-thue-lon-nhat-the-gioi.htm',
#     'https://vneconomy.vn/thong-tin-ve-gan-9-000-ho-so-thue-dat-bi-tac-tai-tp-hcm.htm',
#     'https://vneconomy.vn/gan-100-doanh-nghiep-rat-hai-long-va-hai-long-doi-voi-hai-quan.htm',
#     'https://vneconomy.vn/nganh-hai-quan-xu-ly-11-555-vu-vi-pham-tap-trung-ra-soat-nhieu-mat-hang-rui-ro-cuoi-nam.htm',
#     'https://vneconomy.vn/ha-tinh-nganh-cong-nghiep-khai-khoang-len-ngoi.htm',
#     'https://vneconomy.vn/thu-tien-su-dung-dat-dat-thap-thu-tuong-yeu-cau-nghien-cuu-hoan-thien-thue-nha-dat.htm',
#     'https://vneconomy.vn/bo-cong-an-dua-ra-kien-nghi-de-phong-tranh-mua-ban-hoa-don-khong.htm',
#     'https://vneconomy.vn/vu-mua-ban-hoa-don-khong-nhieu-giam-doc-huong-loi-trung-gian-hang-chuc-ty-dong.htm',
#     'https://vneconomy.vn/tang-thue-tieu-thu-dac-biet-can-nhac-muc-thue-va-lo-trinh-phu-hop.htm',
#     'https://vneconomy.vn/du-giam-va-gia-han-thue-gan-90-nghin-ty-dong-nhung-ngan-sach-van-som-can-dich.htm'
# ]

# # Tạo các task crawl bài viết
# crawl_tasks = []
# for i, url in enumerate(url_list):
#     task = PythonOperator(
#         task_id=f'crawl_{i}',
#         python_callable=get_article,
#         op_args=[url],
#         provide_context=True,
#         dag=dag,
#     )
#     crawl_tasks.append(task)

# # Task ghi lại thời gian thực thi
# record_time_task = PythonOperator(
#     task_id='record_time',
#     python_callable=record_time,
#     provide_context=True,
#     dag=dag,
# )

# # Liên kết các task
# for task in crawl_tasks:
#     task >> record_time_task