from playwright.sync_api import sync_playwright # type: ignore
import re
import time

source_url = 'https://cafef.vn/tai-chinh-quoc-te.chn'
base_url = 'https://cafef.vn'

def get_links(url):
    start_time = time.time()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Truy cập trang web
        page.goto(url)

        # Đợi trang web tải hoàn tất
        page.wait_for_timeout(5000)
        regex = re.compile(r'\d+(?=\.chn)')
        # Tìm phần tử list-main (giới hạn phạm vi tìm kiếm link)
        list_main = page.locator('div.list-main')
        links = []
        
        # Tìm tất cả các thẻ <a> có thuộc tính href bên trong list-main
        link_elements = list_main.locator('a[href]')

        # Lấy tất cả các đường dẫn từ thuộc tính href
        for i in range(link_elements.count()):
            link = link_elements.nth(i).get_attribute('href')
            if link and link != '#':  # Bỏ qua link trống hoặc chứa '#'
                if not link.startswith('http'):  # Thêm base_url nếu link không có http
                    link = base_url + link
                if link not in links and link != url and 'adx.admicro' not in link and regex.search(link):
                    links.append(link)

        # Lưu các đường dẫn vào file links_list_main.txt
        with open('links_list_main.txt', 'w', encoding='utf-8') as file:
            for link in links:
                file.write(link + '\n')

        print(f"Saved {len(links)} links to links_list_main.txt")

        # Đóng trình duyệt
        browser.close()
        
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time} seconds")
    return links


get_links(source_url)