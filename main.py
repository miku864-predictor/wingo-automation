import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)

sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1fDsqMmSzI5YCnqRFq4ma3i-SFvuCfHweWBUl3HHS2jM/edit").sheet1

def insert_data(period, number, color, big_small):
    sheet.append_row([period, number, color, big_small])

# Test insert (you can delete this line after testing)
insert_data("20250404123", "9", "green", "big")