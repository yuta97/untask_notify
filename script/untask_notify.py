#!/usr/local/bin/python3
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
import datetime
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import settings

def execSearch(browser: webdriver):
    """
    京大の課題サイトにアクセスし、未実行の課題を教える。
    """
    browser.get('https://cas.ecs.kyoto-u.ac.jp/cas/login?service=https%3A%2F%2Fpanda.ecs.kyoto-u.ac.jp%2Fsakai-login-tool%2Fcontainer')
    sleep(1)

    #ログイン
    user_id = browser.find_element_by_name("username")
    user_id.clear()
    user_id.send_keys(settings.USN)

    password = browser.find_element_by_name("password")
    password.clear()
    password.send_keys(settings.PWD)

    login = browser.find_element_by_class_name("btn-submit")
    login.click()
    sleep(1)

    #各科目のページに遷移
    base_url = browser.current_url
    
    
    links = {
    "弾性体の力学解析":"2020-110-3200-000",
    "流体力学":"2020-110-3165-000",
    "一般力学":"2020-110-3010-100",
    "基礎有機化学I":"2020-888-N347-014",
    "地球環境学のすすめ":"2020-888-Y201-001",
    "社会基盤デザインＩ":"2020-110-3181-000",
    "工業数学B2":"2020-110-3174-000",
    "確率統計解析及び演習":"2020-110-3003-000",
    "水文学基礎":"2020-110-3030-000",
    "地球工学基礎数理":"2020-110-3005-000",
    }
    
    # nav = browser.find_element_by_id("2020-110-3165-000")
    for subject,link_id in links.items():
        unkadai(base_url,subject,link_id)
    # return tasks

def unkadai(base_url,subject,link_id):
    browser.get(base_url)
    other_link = browser.find_element_by_xpath("//*[@id='topnav']/li[6]/a")
    other_link.click()
    sleep(1)
    nav = browser.find_element_by_id(link_id)
    nav.click()
    
    other_link = browser.find_element_by_xpath("//*[@id='toolMenu']/ul/li[5]/a")
    other_link.click()

    sleep(1)
    # url = browser.find_element_by_xpath("//*[@id='Main73d01739xf8bdx4a24xbf5dx88f92ab7f547']").get_attribute("src")
    # browser.get(url)
    # sleep(1)

    url = browser.find_element_by_xpath("//*[@id='col1']/div[1]/div/div[1]/a").get_attribute("href")
    browser.get(url)
    sleep(1)
    # print(url)
    html = browser.page_source.encode('utf-8')

    # html = requests.get(url)
    soup = BeautifulSoup(html, "html.parser")
    # print(soup)
    base = soup.select("tr")
    # print(base)
    for k in base:
        status =k.select_one("td:nth-child(3)")
        if status is not None:
            if "未開始" in status.text :
                # print(status.text)
                dt = datetime.today()
                highlightday = k.select_one("td:nth-child(5) > span")
                if highlightday is not None:
                    highlightday = highlightday.text
                    highlightday = datetime.strptime(highlightday,'%Y/%m/%d %H:%M')
                    if highlightday >dt:
                        a =  k.select_one("td:nth-child(2)>h4>a")
                        if a is not None:
                            task = (subject+':'+a.text)
                            line_notify(task)


def line_notify(message):
    line_notify_token = settings.LAK
    line_notify_api = 'https://notify-api.line.me/api/notify'
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}
    requests.post(line_notify_api, data=payload, headers=headers)



if __name__ == '__main__':
    try:
        #browser = webdriver.Firefox()  # 普通のFilefoxを制御する場合
        #browser = webdriver.Chrome()   # 普通のChromeを制御する場合


        # HEADLESSブラウザに接続
        browser = webdriver.Remote(
            command_executor='http://selenium-hub:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)

        execSearch(browser)
        
    finally:
        # 終了
        browser.close()
        browser.quit()

