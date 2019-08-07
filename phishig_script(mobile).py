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
slack_url = ''
slack_test_url = ''

def compare_image(url):
    grayA = cv2.imread('/home/korbit-users/phishing_scripts/phishing_tmp2/main.png', cv2.IMREAD_GRAYSCALE)
    grayB = cv2.imread('/home/korbit-users/phishing_scripts/phishing_tmp2/tmp.png', cv2.IMREAD_GRAYSCALE)
    grayC = cv2.imread('/home/korbit-users/phishing_scripts/phishing_tmp2/login.png', cv2.IMREAD_GRAYSCALE)

    score = ssim(grayA, grayB)
    m = mse(grayA, grayB)
    score2 = ssim(grayC, grayB)
    m2 = mse(grayC, grayB)
    
    url = urllib.parse.unquote(url)
    ttt = 'https://portal.korbit.co.kr'
    tt = 'https://portal.korbit.co.kr/login'

    if(score*100 >= 95.5 and m <= 300):
        # print(url)
        # print('score:'+str(score*100))
        # print('m:'+str(m))
        message = '*phishing site detected : *' + url + ' (' + str(round((score*100),2)) + '%)'
        payload = {'text': message}
        requests.post(slack_url, json = payload)
        if(ne(str(url), ttt)):
            shutil.copyfile('/home/korbit-users/phishing_scripts/phishing_tmp2/tmp.png', '/home/korbit-users/phishing_scripts/phishing_tmp2/'+str(score)+'.png')

    if(score2*100 >= 95.5 and m2 <= 300):
        # print(url)
        # print('score2:'+str(score2*100))
        # print('m2:'+str(m2))
        message = '*phishing site detected : *' + url + ' (' + str(round((score2*100),2)) + '%)'
        payload = {'text': message}
        requests.post(slack_url, json = payload)
        if(ne(str(url), tt)):
            shutil.copyfile('/home/korbit-users/phishing_scripts/phishing_tmp2/tmp.png', '/home/korbit-users/phishing_scripts/phishing_tmp2/'+str(score2)+'.png')


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
        if '...' in u[0]:
            continue
        if '/' not in u[0]:
            continue
        # urlencoded = urllib.parse.quote(i.text)
        urls_tmp.append(u[0])
        
    r2 = requests.get('https://www.google.co.kr/search?num=50&cr=countryKR&q=%EC%BD%94%EB%B9%97')
    time.sleep(3)
    html2 = r2.text
    # print(html2)
    html2 = urllib.parse.unquote(html2)
    soup2 = bs(html2, 'html.parser')
    tmp2 = soup.find_all(class_='BNeawe UPmit AP7Wnd')
    # tmp2 = soup2.select('div > cite')
    for k in tmp2:
        # print(k.text)
        u = k.text.split(' ')
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
    options.add_argument('--headless')
    options.add_argument('--no-sandbox') # for linux environment
    options.add_argument('--disable-dev-shm-usage')  # for linux environment
    options.add_argument('--incognito')
    mobile_emulation = { 'deviceName': 'Nexus 5' }
    options.add_experimental_option('mobileEmulation', mobile_emulation)
    browser = webdriver.Chrome(executable_path='/home/korbit-users/phishing_scripts/chromedriver', options=options)
    browser.get('https://portal.korbit.co.kr')
    time.sleep(10)
    browser.save_screenshot('/home/korbit-users/phishing_scripts/phishing_tmp2/main.png')

    browser.get('https://portal.korbit.co.kr/login')
    time.sleep(5)
    browser.save_screenshot('/home/korbit-users/phishing_scripts/phishing_tmp2/login.png')
    browser.quit()

    http = 'http://'
    https = 'https://'
    num = 0
    
    for i in urls:
        i = urllib.parse.unquote(i)
        if not(http in i or https in i):
            i = 'http://'+i

        browser = webdriver.Chrome(executable_path='/home/korbit-users/phishing_scripts/chromedriver', options=options)
        browser.set_page_load_timeout(10) # timeout
        time.sleep(2)
        try:
            browser.get(i)
            res = requests.get(i)
            if not res.status_code == 200:
                continue
            time.sleep(10)                
            browser.save_screenshot('/home/korbit-users/phishing_scripts/phishing_tmp2/tmp.png')
            browser.quit()
            compare_image(i)
        except:
            browser.quit()
            continue

if __name__=='__main__':
    try:
        search()
        urls_tmp = set(urls_tmp)
        urls = list(urls_tmp)
        save_screenshot()
        
    except Exception as e:
        print(str(e))
        payload = {'text': str(e)}
        requests.post(slack_test_url, json = payload)
