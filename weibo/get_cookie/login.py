import os
import pymongo
from pymongo.errors import DuplicateKeyError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

sys.path.append(os.getcwd())

LOCAL_MONGO_HOST = '127.0.0.1'
LOCAL_MONGO_PORT = 27017
DB_NAME = 'Sina'

TEMPLATES_FOLDER = os.getcwd() + '/sina/account_build/templates/'


class WeiboLogin():
    def __init__(self, username, password):
        os.system('pkill -f phantom')
        self.url = 'https://passport.weibo.cn/signin/login?entry=mweibo&r=https://weibo.cn/'
        self.browser = webdriver.Chrome()
        self.browser.set_window_size(1050, 840)
        self.wait = WebDriverWait(self.browser, 20)
        self.username = username
        self.password = password

    def open(self):
        """
        使用自动化工具打开网页输入用户名密码并点击
        :return: None
        """
        self.browser.get(self.url)
        username = self.wait.until(EC.presence_of_element_located((By.ID, 'loginName')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'loginPassword')))
        submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'loginAction')))
        username.send_keys(self.username)
        password.send_keys(self.password)
        submit.click()

    def run(self):
        """
        获取cookie
        :return:
        """
        self.open()
        WebDriverWait(self.browser, 30).until(
            EC.title_is('我的首页')
        )
        cookies = self.browser.get_cookies()
        cookie = [item["name"] + "=" + item["value"] for item in cookies]
        cookie_str = '; '.join(item for item in cookie)
        self.browser.quit()
        return cookie_str


if __name__ == '__main__':
    # 在目录account.txt中添加更多的微博账号 以'----'分隔开
    #file_path = os.getcwd() + r'\weibo\get_cookie\account.txt'
    file_path = 'E:/project/weibo/weibo/get_cookie/account.txt'
    with open(file_path, 'r') as f:
        lines = f.readlines()
    mongo_client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
    collection = mongo_client[DB_NAME]["account.txt"]
    for line in lines:
        line = line.strip()
        username = line.split('----')[0]
        password = line.split('----')[1]
        print('=' * 10 + username + '=' * 10)
        try:
            cookie_str = WeiboLogin(username, password).run()
        except Exception as e:
            print(e)
            continue
        print('获取cookie成功')
        print('Cookie:', cookie_str)
        try:
            collection.insert(
                {"_id": username, "password": password, "cookie": cookie_str, "status": "success"})
        except DuplicateKeyError as e:
            collection.find_one_and_update({'_id': username}, {'$set': {'cookie': cookie_str, "status": "success"}})