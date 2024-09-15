from airflow.decorators import task # type: ignore
from airflow import DAG # type: ignore
from datetime import datetime, timedelta
import link
import crawl

source_urls = [ 
    'https://vneconomy.vn/thue-tai-chhinh.htm',
    'https://vneconomy.vn/kinh-te-so.htm',
]

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 9, 14),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'dynamic_tasks_example4',
    default_args=default_args,
    description='A pipeline to crawl news articles and store them in MongoDB',
    schedule_interval=timedelta(days=1),
    max_active_runs=1,
    concurrency=16,
)

@task
def get_url():
    urls = []
    for source_url in source_urls:
        urls.extend(link.get_link(source_url))
    return urls

@task
def get_articles(url):
    elapsed_time = crawl.get_article(url)
    return {'url': url, 'elapsed_time': elapsed_time}

@task
def record_time(results):
    with open('/home/hgf/airflow/dags/total_elapsed_time3.txt', 'a', encoding='utf-8') as file:
        for result in results:
            file.write(f"{result['url']}: {result['elapsed_time']}\n")

# Tạo DAG
with dag:
    # Task lấy danh sách URL
    url_list = get_url()

    # Task crawl các bài viết dựa trên danh sách URL
    crawl_results = get_articles.expand(url=url_list)

    # Task ghi lại thời gian crawl
    record_time(crawl_results)
