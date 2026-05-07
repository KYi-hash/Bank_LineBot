# Version 2
##########################################################
from selenium import webdriver
from selenium.webdriver.safari.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import requests
import json
import os
##########################################################

### Step 1: Scraped ###
def input_new_bank_data():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Safari()
    driver.get("https://www.nextbank.com.tw/announcement/45c1e31fa40000000285cadc56793797")

    scraped_data = []
    titles = driver.find_elements(By.CLASS_NAME, "itemTitle")
    for t in titles:
        content = t.text.strip()
        if content:
            scraped_data.append(content)

    df = pd.DataFrame(scraped_data, columns = ["Title"])
    df.to_csv("/Users/kai/Desktop/My_Project/Bank_line/Data/bank_news.csv", index=False, encoding="utf-8-sig")
    
    driver.quit()

### Step 2: Data ###
def Clean_Data():
    new = pd.read_csv("/Users/kai/Desktop/My_Project/Bank_line/Data/bank_news.csv")
    old  = pd.read_csv("/Users/kai/Desktop/My_Project/Bank_line/Data/bank_olds.csv")
    update = set(new["Title"]) - set(old["Title"])
    if update:
        clean_data = "\n".join(update)
        message = f"新活動:\n{clean_data}"
    else:
        pass
    new.to_csv("/Users/kai/Desktop/My_Project/Bank_line/Data/bank_olds.csv", index=False, encoding="utf-8-sig")
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
    # 執行 Step 1
    input_new_bank_data()
    
    # 執行 Step 2
    msg_to_send = Clean_Data()
    
    # 執行 Step 3：只有當 msg 有內容時才發送
    if msg_to_send:
        status = send_line_official(msg_to_send)
        if status == 200:
            print("通知發送成功！")
    else:
        print("沒有新活動。")