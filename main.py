import crawl
import link
import removedup
import time

url_list, get_link_time = link.get_link('https://vneconomy.vn/thue-tai-chhinh.htm')

temp = url_list = [
        'https://vneconomy.vn/10-thien-duong-thue-lon-nhat-the-gioi.htm',
        'https://vneconomy.vn/thong-tin-ve-gan-9-000-ho-so-thue-dat-bi-tac-tai-tp-hcm.htm',
        'https://vneconomy.vn/gan-100-doanh-nghiep-rat-hai-long-va-hai-long-doi-voi-hai-quan.htm',
        'https://vneconomy.vn/nganh-hai-quan-xu-ly-11-555-vu-vi-pham-tap-trung-ra-soat-nhieu-mat-hang-rui-ro-cuoi-nam.htm',
        'https://vneconomy.vn/ha-tinh-nganh-cong-nghiep-khai-khoang-len-ngoi.htm',
        'https://vneconomy.vn/du-giam-va-gia-han-thue-gan-90-nghin-ty-dong-nhung-ngan-sach-van-som-can-dich.htm'
]
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
