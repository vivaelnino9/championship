import gspread
import os
import json
import time
from oauth2client.client import SignedJwtAssertionCredentials

def get_sheet(s):
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
    sheet = gc.open(s)
    return sheet

# Leaderboards

def get_season_leaders():
    sheet = get_sheet("Championship Series Stock Sheet")
    s = sheet.worksheet("Season 1 Leader Board")

    leaders = {}

    leaders['Capture Leaders'] = get_leaders(s,'C4:C23','E4:E23')
    leaders['Hold Leaders'] = get_leaders(s,'I4:I23','K4:K23')
    leaders['Return Leaders'] = get_leaders(s,'C28:C47','E28:E47')
    leaders['Prevent Leaders'] = get_leaders(s,'I28:I47','K28:K47')

    return leaders

def get_leaders(s,names_range,stats_range):
    names = s.range(names_range)
    stats = s.range(stats_range)
    players = []
    for cell in names:
        if cell.value == '': continue
        player = {'name':cell.value,'stat':stats[names.index(cell)].value}
        players.append(player)
    return players

# Team Register/ Tournament Signup

def register_team(team):
    sheet = get_sheet("TagPro Championship Series RAW STATS")
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
    sheet = get_sheet("TagPro Championship Series RAW STATS")
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
    sheet = get_sheet("TagPro Championship Series RAW STATS")
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
    sheet = get_sheet("TagPro Championship Series RAW STATS")
    s = sheet.worksheet("Landing Sheet 1")

    row = str(s.find(team_name).row)
    for field,player in new_players.items():
        if field == 'captain': s.update_acell('B'+row, player)
        elif field == 'player1': s.update_acell('C'+row, player)
        elif field == 'player2': s.update_acell('D'+row, player)
        elif field == 'player3': s.update_acell('E'+row, player)
        elif field == 'player4': s.update_acell('F'+row, player)
        else: pass

# Process games

def process_games(games):
    # main function for processing games after submission
    sheet = get_sheet("Championship Series TagPro.eu Extractor")
    s = sheet.worksheet("Copy")
    clear_first_copy_row(s)
    fill_copy_cells(s,games)
    time.sleep(2)
    rows = get_copy_rows(s)
    s = sheet.worksheet("Export")
    fill_export_rows(s,rows)
    sheet = get_sheet("TagPro Championship Series RAW STATS")
    s = sheet.worksheet("RADIUS")
    fill_winner_loser(s,games)

def clear_first_copy_row(s):
    # clear first row of cells on copy sheet
    first_row = s.range('B1:M1')
    for cell in first_row:
        cell.value = ''
    s.update_cells(first_row)

def fill_copy_cells(s,games):
    # fill top row cells in copy sheet to produce rows to copy
    s.update_acell('B1',split_link(games['g1h1']))
    if 'g1h1time' in games: s.update_acell('C1',split_link(games['g1h1time']))
    s.update_acell('D1',split_link(games['g1h2']))
    if 'g1h2time' in games: s.update_acell('E1',split_link(games['g1h2time']))
    if 'g1ot1' in games: s.update_acell('F1',split_link(games['g1ot1']))
    if 'g1ot2' in games: s.update_acell('G1',split_link(games['g1ot2']))
    s.update_acell('H1',split_link(games['g2h1']))
    if 'g2h1time' in games: s.update_acell('I1',split_link(games['g2h1time']))
    s.update_acell('J1',split_link(games['g2h2']))
    if 'g2h2time' in games: s.update_acell('K1',split_link(games['g2h2time']))
    if 'g2ot1' in games: s.update_acell('L1',split_link(games['g2ot1']))
    if 'g2ot2' in games: s.update_acell('M1',split_link(games['g2ot2']))


def get_copy_rows(s):
    # get rows to copy to export page
    rows = []
    for i in range(5,31):
        if s.acell('C'+str(i)).value == '': break
        else: rows.append(s.row_values(i))
    return rows

def fill_export_rows(s,rows):
    # fill rows on export page
    current_row = find_open_row(s)
    for row in rows:
        fill_row(s,row,current_row)
        current_row += 1

def fill_winner_loser(s,games):
    # fill winner and loser cells
    winner_row, winner_col = int(games['winner_row']), int(games['winner_col'])
    loser_row, loser_col = int(games['loser_row']), int(games['loser_col'])
    s.update_cell(winner_row, winner_col, games['winner'])
    s.update_cell(loser_row, loser_col, games['loser'])

def fill_row(s,row,row_number):
    # helper for fill_export_rows
    cell_range = 'A' + str(row_number) + ':' + 'X' + str(row_number)
    cell_list = s.range(cell_range)
    for cell in cell_list:
        cell.value = row[cell_list.index(cell)]
    s.update_cells(cell_list)

def find_open_row(s):
    # find first open row to copy rows into
    vals = s.col_values(5)
    for cell in vals:
        if cell == '': return (vals.index(cell) + 1)

def find_game(tournament_abv,team):
    # find game info for submit page
    sheet = get_sheet("TagPro Championship Series RAW STATS")
    s = sheet.worksheet(get_server_sheet(tournament_abv))
    teams = {}
    cell_list = get_cell_list(s,tournament_abv,team)
    for cell in cell_list:
        winner_loser = get_winner_loser(s,cell.row,cell.col)
        if winner_loser['winner'].value == '' and winner_loser['loser'].value == '':
            teams = get_teams(s,cell)
            if teams['team1'] == '' or teams['team2'] == '': teams = {}
    return teams

def get_cell_list(s,tournament_abv,team):
    # based on tournament, find team name in team1 and team2 columns
    tour_cell = s.find(tournament_abv)
    start_row = tour_cell.row + 4
    start_col = tour_cell.col + 4
    finish_row = start_row + 28
    finish_col = start_col + 1
    cell_range = s.range(start_row,start_col,finish_row,finish_col)
    cell_list = [cell for cell in cell_range if cell.value == team.name]
    return cell_list

def get_winner_loser(s,row,col):
    is_t1 = is_team1(s,s.cell(row,col))
    winner_col = col + 2 if is_t1 else col + 1
    loser_col = col + 3 if is_t1 else col + 2
    winner, loser = s.cell(row,winner_col),s.cell(row,loser_col)
    return {'winner':winner,'loser':loser}

def get_teams(s,cell):
    # helper for getting both team names and game number
    is_t1 = is_team1(s,cell)
    row = cell.row
    col = cell.col
    game = s.cell(row,col-1).value if is_t1 else s.cell(row,col-2).value
    team1 = cell.value if is_t1 else s.cell(row,col-1).value
    team2 = s.cell(row,col+1).value if is_t1 else cell.value
    teams = {'game':game,'team1':team1,'team2':team2}
    winner_loser = get_winner_loser(s,row,col)
    teams.update(winner_loser)
    return teams

def is_team1(s,cell):
    # check if team is in team1 column or team2
    if s.cell(4,cell.col).value == 'Team 1': return True
    else: return False

def get_server_sheet(abv):
    # get specific sheet for certain server tournament
    if abv[0] == 'R' or abv[0] == 'T': return "RADIUS"
    elif abv[0] == 'S': return "Sphere"
    elif abv[0] == 'C': return "Centra"
    else: return ''

def split_link(link):
    # get eu id from end of eu link
    return link.split('match=')[1]
