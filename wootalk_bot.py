from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import logging
import time
import random


# 創建自定義日誌器
logger = logging.getLogger('wootalk_bot_log')

# 設置日誌等級
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()  # 控制台處理器
if not os.path.exists(r'.\log'):
    os.makedirs(r'.\log')
file_handler = logging.FileHandler(r'.\log\run.log', encoding='utf-8')  # 文件處理器

# 設置處理器的日誌等級
console_handler.setLevel(logging.WARNING)  # 設置 console terminal 顯示等級
file_handler.setLevel(logging.DEBUG)  # 設置 logfile 顯示等級

# 創建並設置日誌格式器 (Formatter)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# 將處理器添加到日誌器
logger.addHandler(console_handler)
logger.addHandler(file_handler)


def init_browser():
    """
    初始化瀏覽器
    """
    # 自動下載並安裝 ChromeDriver
    try:
        driver_path = ChromeDriverManager().install()
        driver_path = driver_path.replace(
            'THIRD_PARTY_NOTICES.chromedriver', 'chromedriver.exe')
        service = Service(driver_path)
    except Exception as e:
        logger.critical(f'ChromeDriver 取得失敗: \n{e}')

    # 設定 Chrome 瀏覽器的選項
    try:
        options = Options()
        options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('lang=zh-TW')
    except Exception as e:
        logger.warning(f'Chrome 偽裝選項設定錯誤: \n{e}')

    # 初始化 WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    # 設置 JavaScript 屬性
    driver.execute_script("""
        Object.defineProperty(navigator, 'languages', {
            get: function() { return ['zh-TW', 'zh', 'en-US', 'en']; }
        });
        Object.defineProperty(navigator, 'plugins', {
            get: function() { return [
                'PDF Viewer', 'Chrome PDF Viewer', 'Chromium PDF Viewer', 
                'Microsoft Edge PDF Viewer', 'WebKit built-in PDF'
            ]; }
        });
        Object.defineProperty(navigator, 'webdriver', {
            get: function() { return false; }
        });
        Object.defineProperty(window, 'outerHeight', { value: 1040 });
        Object.defineProperty(window, 'outerWidth', { value: 1920 });
        Object.defineProperty(window, 'innerHeight', { value: 919 });
        Object.defineProperty(window, 'innerWidth', { value: 1920 });
        Object.defineProperty(window.screen, 'width', { value: 1920 });
        Object.defineProperty(window.screen, 'height', { value: 1080 });
        Object.defineProperty(window.screen, 'availWidth', { value: 1920 });
        Object.defineProperty(window.screen, 'availHeight', { value: 1040 });
    """)

    return driver


def init_opening():
    """
    初始化開場白列表
    """
    # 定義要發送的開場白列表
    file_path = "opening.txt"
    if os.path.exists(file_path):  # 如果檔案存在
        # 以讀取模式開啟檔案，並指定編碼為 UTF-8
        with open(file_path, 'r', encoding='utf-8') as f:
            # 讀取檔案內容並將其轉換為字符串
            longstr = str(f.read())
            # 將字符串以行為單位分割成列表
            HiMessageList = longstr.splitlines()
    else:  # 如果檔案不存在
        # 使用預設的字符串列表
        HiMessageList = [
            'Hello', 'Hi', '嗨', '純聊不換', '聊嗎'
        ]
        # 初始化空字符串
        longstr = ''

        # 將預設列表中的每個元素添加到字符串中，並在每個元素後加上換行符
        for s in HiMessageList:
            longstr = longstr + s + '\n'
        # 以寫入模式開啟檔案，並將字符串寫入檔案中
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(longstr)
        print('未檢測到開場白檔案，已自動建立 opening.txt')

    return HiMessageList


def antibot_run(link_element):
    """
    處理反機器人驗證的操作
    """
    # 點擊超連結
    time.sleep(random.randint(15, 30)/10)
    link_element.click()

    # 等待驗證時間
    time.sleep(60 + random.randint(0, 3))

    # 獲取當前所有的分頁
    handles = driver.window_handles

    # 切換到第二個分頁
    driver.switch_to.window(handles[1])

    # # 儲存頁面原始碼
    # with open('link_element.txt', 'w', encoding='UTF-8') as f:
    #     f.write(driver.page_source)

    # 定位按鈕
    button = WebDriverWait(driver, 1).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'input.peter-river-flat-button'))
    )
    # 模擬點擊
    print('點擊驗證紐')
    button.click()

    # 關閉當前分頁
    driver.close()

    # 切換回第一個分頁
    driver.switch_to.window(handles[0])

    # 重新整理分頁
    time.sleep(random.randint(0, 30)/10)
    driver.refresh()
    time.sleep(random.randint(0, 3)/10)

    # 點擊開始按鈕
    startButton = driver.find_element(By.ID, 'startButton')
    startButton.click()


def send_message(messageInput, sendButton, message):
    """
    模擬鍵盤輸入並發送消息
    """
    for char in message:
        messageInput.send_keys(char)
        time.sleep(random.uniform(0.15, 0.55))  # 隨機延遲
    sendButton.click()


def send_opening():
    """
    發送開場白
    """
    messageInput = driver.find_element(By.ID, 'messageInput')
    sendButton = driver.find_element(By.ID, 'sendButton')
    send_message(messageInput, sendButton,
                 HiMessageList[random.randint(0, len(HiMessageList) - 1)])


def detect_leave():
    """
    判斷是否有人離開
    """

    systexts = driver.find_elements(
        By.CSS_SELECTOR, "#messages > div.system.text")

    # systext = driver.find_element(
    #     By.CLASS_NAME, ".system.text[value='對方離開了']").text

    # print('Systext ', systexts[-1.text])

    if '對方離開了' in systexts[-1].text:
        strangerleave = 0
        print('對方離開了，開啟下一輪')
        time.sleep(random.randint(1, 4))

        exitButton = driver.find_element(By.ID, 'changeButton')
        exitButton.click()

        try:
            exitConfrim = driver.find_element(By.ID, 'popup-yes')
            exitButton.click()
        except Exception as e:
            a = 1

    return True


def leave():
    """
    主動離開聊天室
    """
    exitButton = driver.find_element(By.ID, 'changeButton')
    exitButton.click()

    try:
        exitConfrim = driver.find_element(By.ID, 'popup-yes')
        exitButton.click()
    except Exception as e:
        a = 1


if __name__ == '__main__':

    chat_round = 1
    antibot = 1

    # 設置瀏覽器偽裝
    driver = init_browser()

    # 打開wootalk
    try:
        driver.get('https://wootalk.today/')
    except Exception as e:
        logger.critical(f'打開 wootalk 失敗: \n{e}')

    # 開場白設定
    HiMessageList = init_opening()

    while chat_round > 0:
        print(f'開始第 {chat_round} 輪聊天')
        startButton = driver.find_element(By.ID, 'startButton')
        startButton.click()

        # 確認系統訊息是否需要人機驗證
        link_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[4]/div[3]/div[1]/blockquote/div[2]/a'))
        )
        systext = link_element.text

        if '開啟此連結' in systext:
            print('需要人機驗證')
            antibot_run(link_element)
            antibot = 0

        time.sleep(random.uniform(1.5, 3.8))

        # 開場白
        print('發送開場白')
        send_opening()

        # 檢測聊天訊息
        second = 1
        while second > 0:
            # try:
            # 檢測是否有人離開
            if detect_leave():
                second = 0

            second += 1
            # except Exception as e:
            #     print(f'錯誤訊息: {e}')

        time.sleep(1)
        chat_round += 1
        # input()
