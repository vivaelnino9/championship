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
    for cell in column_a:
        row = str(column_a.index(cell)+1)
        if cell == '' and s.acell('B'+row).value == '':
            s.update_acell('A'+row, tournament)
            s.update_acell('B'+row, team_name)
            break

def remove_signup(team_name,tournament):
    # find signup for tournament and remove it
    sheet = get_sheet()
    s = sheet.worksheet("Landing Sheet 2")

    team_matches = s.findall(team_name)
    for team in team_matches:
        row = str(team.row)
        tour = s.acell('A'+row).value
        if tour == tournament:
            s.update_acell('A'+row, '')
            s.update_acell('B'+row, '')
            break
