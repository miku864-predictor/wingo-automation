import time
import gspread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from oauth2client.service_account import ServiceAccountCredentials

# Set up Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1fDsqMmSzI5YCnqRFq4ma3i-SFvuCfHweWBUl3HHS2jM/edit?usp=drivesdk").sheet1

# Set up Selenium headless browser
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)
driver.get("https://damangames.bet/#/home/AllLotteryGames/WinGo?id=1")

# Wait for data to load
time.sleep(10)

# Extract data from page
try:
    results = driver.find_elements(By.CLASS_NAME, "game-result-item")
    if len(results) >= 1:
        latest = results[0].text.split("\n")
        period = latest[0]
        result = latest[1]
        big_small = "Big" if int(result) >= 5 else "Small"
        color = "Red" if int(result) in [3, 6, 9] else "Green" if int(result) % 2 == 0 else "Violet"

        # Add to Google Sheet
        sheet.append_row([period, result, big_small, color])
        print("Data written:", period, result, big_small, color)
    else:
        print("No results found.")
except Exception as e:
    print("Error scraping data:", str(e))

driver.quit()
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheet URL
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1fDsqMmSzI5YCnqRFq4ma3i-SFvuCfHweWBUl3HHS2jM/edit?usp=drivesdk"

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_url(spreadsheet_url).sheet1

# Chrome headless setup
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://damangames.bet/#/home/AllLotteryGames/WinGo?id=1")

time.sleep(10)  # wait for content to load

try:
    period = driver.find_element(By.CLASS_NAME, "period").text.strip()
    result = driver.find_element(By.CLASS_NAME, "lottery-number").text.strip()
    color = driver.find_element(By.CLASS_NAME, "color").text.strip()
    big_small = "big" if int(result) >= 5 else "small"

    sheet.append_row([period, result, color, big_small])
    print(f"Inserted: {period}, {result}, {color}, {big_small}")

except Exception as e:
    print("Error:", e)

driver.quit()
