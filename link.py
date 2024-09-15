from playwright.sync_api import sync_playwright #type: ignore
import os
import time

url = 'https://vneconomy.vn/thue-tai-chhinh.htm'
base_url = 'https://vneconomy.vn'

def get_link(url):
    elasped_time = 0
    start_time = time.time()
    with sync_playwright() as p:
        # Mở trình duyệt
        browser = p.chromium.launch(headless=True)  # headless=True để chạy ngầm, không hiện cửa sổ trình duyệt
        page = browser.new_page()

        # Điều hướng đến URL
        page.goto(url)

        # Đợi trang web tải và nội dung JavaScript được render (nếu có)
        page.wait_for_timeout(5000)  # Đợi 5 giây để chắc chắn nội dung được tải xong (bạn có thể tinh chỉnh thời gian)

        # Tìm tất cả các thẻ <a> bên trong <figure> có class 'story__thumb'
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

            # Lưu các link vào file 'link2.txt'
            with open('link.txt', 'w', encoding='utf-8') as file:
                for link in links:
                    file.write(link + '\n')

            print(f"Saved {len(links)} links to link.txt")
        else:
            print("No links found")

        # Đóng trình duyệt
        browser.close()
        end_time = time.time()
        elapsed_time = end_time - start_time
    return links