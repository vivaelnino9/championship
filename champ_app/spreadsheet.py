import gspread
import os
import json
# from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.client import SignedJwtAssertionCredentials
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
private_key = os.environ['PRIVATE_KEY']
print(os.environ['GOOGLE_APPLICATION_CREDENTIALS']['private_key'])
# creds = SignedJwtAssertionCredentials(client_email, private_key.encode(), scope)
# gc = gspread.authorize(creds)
# sheet = gc.open("Team Form (Responses)").sheet1
# client = gspread.authorize(creds)
#
# sheet = client.open("Team Form (Responses)").sheet1
#
# list_of_hashes = sheet.get_all_records()
# cell = sheet.find("Rattpack")
# print("Found something at Row:%s Col:%s" % (cell.row, cell.col))
