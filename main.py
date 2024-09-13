import crawl
import link
import removedup
import time

url_list, get_link_time = link.get_link('https://vneconomy.vn/thue-tai-chhinh.htm')

temp = url_list[6:]
crawl_time = 0
elapsed_time = 0
time_start = time.time()
for url in temp:
    crawl_time += crawl.get_article(url)
time_end = time.time()
elapsed_time += time_end - time_start
with open('time.txt', 'w', encoding='utf-8') as file:
    file.write(f"Total time main: {elapsed_time} seconds) \n")
    file.write(f"Total time crawl: {crawl_time} seconds) \n")
    file.write(f"Total time link: {get_link_time} seconds) \n")
