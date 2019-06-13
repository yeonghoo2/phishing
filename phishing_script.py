# encoding=utf8
from skimage.measure import compare_ssim as ssim
from skimage.measure import compare_mse as mse
import cv2
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import shutil
import time
import websocket
import urllib.parse
import sys
from operator import ne

'''
python36 -m pip install --upgrade pip setuptools wheel
python36 -m pip install opencv-python
python36 -m pip install scikit-image
python36 -m pip install imutils
python36 -m pip install selenium
python36 -m pip install requests
python36 -m pip install scipy
python36 -m pip install bs4
python36 -m pip install websocket

'''
urls = []
urls_tmp = []
slack_url = 'https://hooks.slack.com/services/-'
slack_test_url = 'https://hooks.slack.com/services/-'
popup = False
popup2 = False

def compare_image(url):
    grayA = cv2.imread('/home/korbit-users/phishing_scripts/phishing_tmp/origin1.png', cv2.IMREAD_GRAYSCALE)
    grayB = cv2.imread('/home/korbit-users/phishing_scripts/phishing_tmp/tmp.png', cv2.IMREAD_GRAYSCALE)
    grayC = cv2.imread('/home/korbit-users/phishing_scripts/phishing_tmp/login.png', cv2.IMREAD_GRAYSCALE)

    score = ssim(grayA, grayB)
    m = mse(grayA, grayB)
    score2 = ssim(grayC, grayB)
    m2 = mse(grayC, grayB)
    score3 = 0
    m3 = 400
    score4 = 0
    m4 = 400

    if(popup):
        grayD = cv2.imread('/home/korbit-users/phishing_scripts/phishing_tmp/origin2.png', cv2.IMREAD_GRAYSCALE)
        score3 = ssim(grayD, grayB)
        m3 = mse(grayD, grayB)

    if(popup2):
        grayD = cv2.imread('/home/korbit-users/phishing_scripts/phishing_tmp/origin3.png', cv2.IMREAD_GRAYSCALE)
        score4 = ssim(grayD, grayB)
        m4 = mse(grayD, grayB)

    url = urllib.parse.unquote(url)
    ttt = 'https://www.korbit.co.kr/'
    tt = 'https://www.korbit.co.kr/sign-in/'

    if(score*100 >= 95.5 and m <= 300):
        # print(url)
        # print('score:'+str(score*100))
        # print('m:'+str(m))
        message = '*phishing site detected : *' + url + ' (' + str(round((score*100),2)) + '%)'
        payload = {'text': message}
        requests.post(slack_url, json = payload)
        if(ne(str(url), ttt)):
            shutil.copyfile('/home/korbit-users/phishing_scripts/phishing_tmp/tmp.png', '/home/korbit-users/phishing_scripts/phishing_tmp/'+str(score)+'.png')

    if(score2*100 >= 95.5 and m2 <= 300):
        # print(url)
        # print('score2:'+str(score2*100))
        # print('m2:'+str(m2))
        message = '*phishing site detected : *' + url + ' (' + str(round((score2*100),2)) + '%)'
        payload = {'text': message}
        requests.post(slack_url, json = payload)
        if(ne(str(url), tt)):
            shutil.copyfile('/home/korbit-users/phishing_scripts/phishing_tmp/tmp.png', '/home/korbit-users/phishing_scripts/phishing_tmp/'+str(score2)+'.png')

    if(score3*100 >= 95.5 and m3 <=300):
        message = '*phishing site deteced : *' + url + ' (' + str(round((score3*100),2)) + '%)'
        payload = {'text': message}
        requests.post(slack_url, json = payload)
        if(ne(str(url), ttt)):
            shutil.copyfile('/home/korbit-users/phishing_scripts/phishing_tmp/tmp.png', '/home/korbit-users/phishing_scripts/phishing_tmp/'+str(score3)+'.png')

    if(score4*100 >= 95.5 and m4 <=300):
        message = '*phishing site deteced : *' + url + ' (' + str(round((score4*100),2)) + '%)'
        payload = {'text': message}
        requests.post(slack_url, json = payload)
        if(ne(str(url), ttt)):
            shutil.copyfile('/home/korbit-users/phishing_scripts/phishing_tmp/tmp.png', '/home/korbit-users/phishing_scripts/phishing_tmp/'+str(score4)+'.png')


def search():
    r = requests.get('https://www.google.co.kr/search?num=50&q=korbit&cr=countryKR')
    # r = requests.get('https://www.google.co.kr/search?num=60&q=korbit')
    # print(r.status_code)
    time.sleep(2)
    html = r.text
    html = urllib.parse.unquote(html)
    # print(html)
    soup = bs(html, 'html.parser')
    tmp = soup.find_all(class_='BNeawe UPmit AP7Wnd') # 2019.5.29 update
    # tmp = soup.select('div > cite') # 2018.11.1

    for i in tmp:
        u = i.text.split(' ')
        if 'blockmedia' in u[0]:
            continue
        if 'bokim' in u[0]:
            continue
        if 'wanted' in u[0]:
            continue
        if '...' in u[0]:
            continue
        if '/' not in u[0]:
            continue
        # urlencoded = urllib.parse.quote(i.text)
        urls_tmp.append(u[0])

    r3 = requests.get('https://www.google.co.kr/search?num=50&cr=countryKR&q=%EC%BD%94%EB%B9%97')
    time.sleep(3)
    html3 = r3.text
    # print(html3)
    html3 = urllib.parse.unquote(html3)
    soup3 = bs(html3, 'html.parser') 
    tmp3 = soup.find_all(class_='BNeawe UPmit AP7Wnd')
    # tmp3 = soup3.select('div > cite')
    for k in tmp3:
        # print(k.text)
        u = k.text.split(' ')
        if 'blockmedia' in u[0]:
            continue
        if 'bokim' in u[0]:
            continue
        if 'wanted' in u[0]:
            continue
        if '...' in u[0]:
            continue
        if '/' not in u[0]:
            continue
        # print(k.text)
        urls_tmp.append(u[0])

    # print(urls_tmp)
    # urls.remove(urllib.parse.quote('https://www.korbit.co.kr/'))

def save_screenshot():
    options = Options()
    # options.add_argument('--start-fullscreen')
    # options.add_argument('--disable-notifications')
    options.add_argument('--window-size=1300x1500')
    options.add_argument('--headless')
    options.add_argument('--disable-infobars')
    options.add_argument('--hide-scrollbar')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--user-agent = Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')

    chrome_prefs = {}
    options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = { "popups" : 1 }
    browser = webdriver.Chrome(executable_path='/home/korbit-users/phishing_scripts/chromedriver', options=options)
    browser.get('https://www.korbit.co.kr/')
    time.sleep(10)
    browser.save_screenshot('/home/korbit-users/phishing_scripts/phishing_tmp/origin1.png')


    for i in range(9,0,-1):
        for j in range(5,0,-1):
            try:
                browser.find_element_by_xpath('/html/body/div['+str(i)+']/div/div/div/footer/table/tbody/tr/td['+str(j)+']/button').click()
                time.sleep(10)
                browser.save_screenshot('/home/korbit-users/phishing_scripts/phishing_tmp/origin2.png')
                popup = True
                break
            except:
                continue


    for i in range(9,0,-1):
        for j in range(5,0,-1):
            try:
                browser.find_element_by_xpath('/html/body/div['+str(i)+']/div/div/div/footer/table/tbody/tr/td['+str(j)+']/button').click()
                time.sleep(10)
                browser.save_screenshot('/home/korbit-users/phishing_scripts/phishing_tmp/origin3.png')
                popup2 = True
                break
            except:
                continue

    for i in range(9,0,-1):
        for j in range(5,0,-1):
            try:
                browser.find_element_by_xpath('/html/body/div['+str(i)+']/div/div/footer/table/tbody/tr/td['+str(j)+']/button').click()
                time.sleep(10)
                browser.save_screenshot('/home/korbit-users/phishing_scripts/phishing_tmp/origin3.png')
                popup2 = True
                break
            except:
                continue

    # browser.save_screenshot('/home/korbit-users/phishing_scripts/phishing_tmp/origin.png')
    # time.sleep(2)
    browser.get('https://www.korbit.co.kr/sign-in/')
    time.sleep(5)
    browser.save_screenshot('/home/korbit-users/phishing_scripts/phishing_tmp/login.png')
    browser.quit()

    http = 'http://'
    https = 'https://'
    num = 0

    for i in urls:
        # num = num + 1
        # print(num)
        i = urllib.parse.unquote(i)
        # print(i)
        if not(http in i or https in i):
            i = 'http://'+i

        browser = webdriver.Chrome(executable_path='/home/korbit-users/phishing_scripts/chromedriver', options=options)
        browser.set_page_load_timeout(10) # timeout
        # print(i)
        time.sleep(2)
        try:
            browser.get(i)
            time.sleep(10)
            browser.save_screenshot('/home/korbit-users/phishing_scripts/phishing_tmp/tmp.png')
            browser.quit()
            compare_image(i)
        except:
            browser.quit()
            continue

if __name__=='__main__':
    # try:
        # shutil.rmtree('/home/korbit-users/phishing_scripts/phishing_tmp')
        # os.mkdir('/home/korbit-users/phishing_scripts/phishing_tmp')
    # except:
        # pass

    try:
        # print('go')
        search()
    # f = open('/home/korbit-users/phishing_scripts/pre_urls.txt','r')
    # pre_urls = f.read().split('\n')
    # urls = urls + pre_urls
        urls_tmp = set(urls_tmp)
        urls = list(urls_tmp)
        # print(urls)
    # print(urls)
        save_screenshot()
    except Exception as e:
        print(str(e))
        payload = {'text': str(e)}
        requests.post(slack_test_url, json = payload)
