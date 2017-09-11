import gspread
import os
import json
# from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.client import SignedJwtAssertionCredentials
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
client_email = os.environ['CLIENT_EMAIL']
client_secret = json.loads(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
private_key = client_secret['private_key']
creds = SignedJwtAssertionCredentials(client_email, private_key, scope)
gc = gspread.authorize(creds)
sheet = gc.open("Team Form (Responses)").sheet1
client = gspread.authorize(creds)

list_of_hashes = sheet.get_all_records()
cell = sheet.find("Rattpack")
print("Found something at Row:%s Col:%s" % (cell.row, cell.col))
