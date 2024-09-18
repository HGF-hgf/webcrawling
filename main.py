# from airflow.decorators import task, dag # type: ignore
# from airflow import DAG # type: ignore
# from datetime import datetime, timedelta
# import link_cafef as link
# import crawl_cafef as crawls
# import random

# source_urls = [ 
#     'https://cafef.vn/thi-truong-chung-khoan.chn',
#     'https://cafef.vn/bat-dong-san.chn',
#     'https://cafef.vn/tai-chinh-ngan-hang.chn',
#     'https://cafef.vn/smart-money.chn',
#     'https://cafef.vn/tai-chinh-quoc-te.chn',
# ]

# default_args = {
#     'owner': 'airflow',
#     'depends_on_past': False,
#     'start_date': datetime(2024, 9, 14),
#     'email_on_failure': False,
#     'email_on_retry': False,
#     'retries': 1,
#     'retry_delay': timedelta(minutes=5),
# }

# dag = DAG(
#     'example11',
#     default_args=default_args,
#     description='A pipeline to crawl news articles and store them in MongoDB',
#     schedule_interval=timedelta(minutes=10),
#     max_active_runs=1,
#     concurrency=16,
#     start_date=datetime(2024, 9, 14),
# )
    
# @task
# def get_url():
#     if not source_urls:
#         return []
#     else:
#         source_url = random.choice(source_urls)
#         links = link.get_links(source_url)
#         source_urls[:] = [url for url in source_urls if url != source_url]
#         return links[7:14]

# @task
# def get_articles(url):
#     elapsed_time = crawls.get_article(url)
#     return {'url': url, 'elapsed_time': elapsed_time}

# @task
# def record_time(results):
#     if not results:
#         with open('/home/hgf/airflow/dags/total_elapsed_time3.txt', 'a', encoding='utf-8') as file:
#             file.write("No articles crawled today.\n")
#     else:
#         with open('/home/hgf/airflow/dags/total_elapsed_time3.txt', 'a', encoding='utf-8') as file:
#             for result in results:
#                 file.write(f"{result['url']}: {result['elapsed_time']}\n")

#     # Tạo các task
# with dag:
#     url_list = get_url()
#     crawl_results = get_articles.expand(url=url_list)
#     record_time(crawl_results)

