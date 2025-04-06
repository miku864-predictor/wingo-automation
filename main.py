import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Setup Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1fDsqMmSzI5YCnqRFq4ma3i-SFvuCfHweWBUl3HHS2jM/edit").sheet1

# Setup Chrome options
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

# Setup WebDriver
driver = webdriver.Chrome(options=options)
driver.get("https://damangames.bet/#/home/AllLotteryGames/WinGo?id=1")

time.sleep(10)  # Wait for page to load fully

try:
    period = driver.find_element(By.CLASS_NAME, "period").text
    result = driver.find_element(By.CLASS_NAME, "lottery-number").text
    color = driver.find_element(By.CLASS_NAME, "color").text
    big_small = "big" if int(result) >= 5 else "small"

    # Insert into Google Sheet
    sheet.append_row([period, result, color, big_small])
    print(f"Inserted: {period}, {result}, {color}, {big_small}")

except Exception as e:
    print("Error:", e)

driver.quit()
