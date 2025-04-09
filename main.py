import time
import random
import gspread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from google.oauth2.service_account import Credentials
from selenium.webdriver.common.by import By
from datetime import datetime

# Setup Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("service_account.json", scopes=scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1fDsqMmSzI5YCnqRFq4ma3i-SFvuCfHweWBUl3HHS2jM/edit").worksheet("Miku wingo automation")

# Setup Selenium headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=chrome_options)

def get_live_result():
    driver.get("https://damangames.bet/#/home/AllLotteryGames/WinGo?id=1")
    time.sleep(5)

    try:
        # Update with latest working selectors if needed
        period = driver.find_element(By.CLASS_NAME, "game-title").text.strip().split()[-1]
        result = driver.find_element(By.CLASS_NAME, "lottery-number").text.strip()

        return period, int(result)
    except Exception as e:
        print("Error getting result:", e)
        return None, None

def predict(number):
    big_small = "Big" if number >= 5 else "Small"

    if number in [0, 5]:
        color = "Violet"
    elif number in [1, 3, 7, 9]:
        color = "Green"
    elif number in [2, 4, 6, 8]:
        color = "Red"
    else:
        color = "Unknown"

    return big_small, color

while True:
    period, number = get_live_result()
    if period and number is not None:
        big_small, color = predict(number)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{now} | Period: {period}, Number: {number}, {big_small}, {color}")
        sheet.append_row([period, str(number), big_small, color])
    else:
        print("Failed to get result.")
    
    time.sleep(60)
