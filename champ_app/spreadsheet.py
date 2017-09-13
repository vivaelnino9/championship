import gspread
import os
import json
from oauth2client.client import SignedJwtAssertionCredentials

def get_sheet():
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds']
    try:
        client_secret = json.loads(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    except KeyError:
        client_secret = json.load(open('client_secret.json'))
    client_email = client_secret['client_email']
    private_key = client_secret['private_key']

    creds = SignedJwtAssertionCredentials(client_email, private_key, scope)
    gc = gspread.authorize(creds)
    sheet = gc.open("TP Championship league RAW STATS")
    return sheet

def enter_signup(team_name,tournament):
    # find landing sheet 2 and place team name and tournament in next available cells
    sheet = get_sheet()
    s = sheet.worksheet("Landing Sheet 2")
    column_a = s.col_values(1)
    column_b = s.col_values(2)
    for cell in column_a:
        if cell == '':
            s.update_acell('A'+str(column_a.index(cell)+1), tournament)
            break
    for cell in column_b:
        if cell == '':
            s.update_acell('B'+str(column_a.index(cell)+1), team_name)
            break
def check_for_signup(team_name,tournament):
    sheet = get_sheet()
    s = sheet.worksheet("Landing Sheet 2")
    column_a = s.col_values(1)
    column_b = s.col_values(2)
    matched_cells = s.findall(team_name)
    for cell in matched_cells:
        tour = s.acell('B'+str(cell.row)).value
        if tour == tournament:
            return True
    return False
