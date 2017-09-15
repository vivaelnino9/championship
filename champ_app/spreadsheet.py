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
    sheet = gc.open("TagPro Championship Series RAW STATS")
    return sheet

def register_team(team):
    sheet = get_sheet()
    s = sheet.worksheet("Landing Sheet 1")

    column_a = s.col_values(1)
    for cell in column_a:
        row = str(column_a.index(cell)+1)
        if row_is_empty(s,row):
            s.update_acell('A'+row, team.name)
            s.update_acell('B'+row, team.captain)
            s.update_acell('C'+row, team.player1)
            s.update_acell('D'+row, team.player2)
            s.update_acell('E'+row, team.player3)
            s.update_acell('F'+row, team.player4)
            s.update_acell('G'+row, team.get_server_display())
            break

def row_is_empty(sheet,row):
    for cell in sheet.row_values(row):
        if cell != '': return False
    return True
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

def edit_roster(team_name,new_players):
    # make roster changes in spreadsheet
    sheet = get_sheet()
    s = sheet.worksheet("Landing Sheet 1")

    row = str(s.find(team_name).row)
    for field,player in new_players.items():
        if field == 'captain': s.update_acell('B'+row, player)
        elif field == 'player1': s.update_acell('C'+row, player)
        elif field == 'player2': s.update_acell('D'+row, player)
        elif field == 'player3': s.update_acell('E'+row, player)
        elif field == 'player4': s.update_acell('F'+row, player)
        else: pass
