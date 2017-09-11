import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
# creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
# creds = ServiceAccountCredentials.from_json_keyfile_name(os.environ['GOOGLE_APPLICATION_CREDENTIALS'], scope)
creds = ServiceAccountCredentials.make_creds(
  scope: 'https://www.googleapis.com/auth/drive',
  json_key_io: StringIO.new(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Team Form (Responses)").sheet1

# Extract and print all of the values
list_of_hashes = sheet.get_all_records()
# print(list_of_hashes)
cell = sheet.find("Rattpack")
print("Found something at Row:%s Col:%s" % (cell.row, cell.col))
