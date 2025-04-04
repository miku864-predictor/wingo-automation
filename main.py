import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)

sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1fDsqMmSzI5YCnqRFq4ma3i-SFvuCfHweWBUl3HHS2jM/edit").sheet1

def get_game_data():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://damangames.bet/#/home/AllLotteryGames/WinGo?id=1")
    
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    period = soup.select_one(".number-wrap .number-info .period").text.strip()
    result = soup.select_one(".number-wrap .number-info .number").text.strip()
    
    number = result.split("+")[0].strip()
    color = soup.select_one(".number-wrap .number-color").text.strip().lower()
    big_small = "big" if int(number) >= 5 else "small"
    
    return period, number, color, big_small

def update_sheet():
    period, number, color, big_small = get_game_data()
    existing = sheet.col_values(1)
    
    if period not in existing:
        sheet.append_row([period, number, color, big_small])
        print("Row added:", period, number, color, big_small)
    else:
        print("Already exists:", period)

update_sheet()
