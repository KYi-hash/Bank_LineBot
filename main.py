# Version 3
##########################################################
from selenium import webdriver
from selenium.webdriver.safari.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import requests
import json
import os
from datetime import datetime
##########################################################

### Step 1: Scraped ###
def input_new_bank_data():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Safari()
    driver.get("https://www.nextbank.com.tw/announcement/45c1e31fa40000000285cadc56793797")

    scraped_data = []
    driver.implicitly_wait(5)
    titles = driver.find_elements(By.CLASS_NAME, "itemTitle")
    times = driver.find_elements(By.CLASS_NAME, "date")
    for tit, tim in zip(titles, times):
        content = tit.text.strip()
        publish_time = tim.text.strip()
        if content:
            scraped_data.append({"Title":content, "Time":publish_time})
    
    driver.quit()
    return scraped_data

### Step 2: Data ###
def Clean_Data():
    activity_date = input_new_bank_data()
    today_date = "2026/05/06"

    message_content = []
    for item in activity_date:
        if item['Time'] == today_date:
            message_content.append(item['Title'])
    else:
        same = False
    
    message  = None
    if message_content:
        message_content = "\n".join(message_content)
        message = f"新活動:{message_content}"
        print(message)
    else:
        pass

    return message


### Step 3: Line Bot ###
def send_line_official(message):
    url = "https://api.line.me/v2/bot/message/push"
    
    # 填入你剛剛找到的兩串寶物
    token = os.getenv('LINE_TOKEN')
    user_id = os.getenv('LINE_USER_ID')
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    payload = {
        "to": user_id,
        "messages": [{"type": "text", "text": message}]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.status_code

if __name__ == "__main__":
    # 執行 Step 1, 2
    msg_to_send = Clean_Data()
    
    # 執行 Step 3：只有當 msg 有內容時才發送
    if msg_to_send:
        status = send_line_official(msg_to_send)
        if status == 200:
            print("通知發送成功！")
    else:
        print("沒有新活動。")