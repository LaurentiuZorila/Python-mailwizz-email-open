# Importing packages
import time
import requests
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor


def main():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    login(driver)
    run_urls(driver)


def wait_for_id(web_browser, div_id):
    wait = WebDriverWait(web_browser, 10)
    wait.until(EC.presence_of_element_located((By.ID, div_id)))


def login(web_browser):
    login_url = 'http://mailwizz.test/customer/index.php/guest/index'
    username = 'laurentiu.zorila@onetwist.com'
    password = 'laurentiu.zorila@onetwist.com'
    main_url = 'customer/index.php'

    web_browser.get(login_url)
    username_input = web_browser.find_element_by_id('CustomerLogin_email')
    password_input = web_browser.find_element_by_id('CustomerLogin_password')
    login_button = web_browser.find_element_by_css_selector(
        '#yw0 > div > div.login-form.login-flex-col > div > div:nth-child(4) > div > div.pull-right > button > i')

    username_input.clear()
    username_input.send_keys(username)
    password_input.clear()
    password_input.send_keys(password)
    login_button.click()

    current_url = web_browser.current_url

    if main_url in current_url:
        print('-> You are successfully logged in!')
    else:
        print('-> Login failed! Please check your credentials and try again!')
        web_browser.close()


def run_urls(web_browser):
    loop = asyncio.get_event_loop()
    url_to_open_one = ' http://mailwizz.test/index.php/campaigns/bl550t3dgdec2/track-url/'
    url_to_open_two = '/55325aad95abbdf2045d4a1955c88c7174d5020b'
    list_url = 'http://mailwizz.test/customer/index.php/lists/jw056e6r3c5c3/subscribers'
    web_browser.get(list_url)

    # wait until id is visible
    wait_for_id(web_browser, 'subscribers-form')

    # Grab all subscribers id to make url
    rows = web_browser.find_element_by_xpath('//*[@id="subscribers-form"]/table/tbody').find_elements_by_tag_name('tr')
    subscribers_id = []
    for row in rows:
        cells = row.find_elements_by_tag_name('td')
        subscriber_id = cells[2].text
        subscribers_id.append(subscriber_id)

    urls = []
    for s_id in subscribers_id:
        url = url_to_open_one + s_id + url_to_open_two
        urls.append(url)

    for url_ in urls:
        print(url_)
        # req = requests.get(url)
        start = time.time()
        loop.run_until_complete(make_requests(loop, url_))
        print(time.time() - start)


async def make_requests(loop_, url_):
    executor = ThreadPoolExecutor(max_workers=5)
    futures = [loop_.run_in_executor(executor, requests.get, url_) for _ in range(5)]
    await asyncio.wait(futures)


if __name__ == "__main__":
    main()
