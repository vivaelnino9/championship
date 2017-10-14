import gspread
import os
import json
import time
from oauth2client.client import SignedJwtAssertionCredentials

from .models import *

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

###############################################
################# Leaderboard #################
###############################################

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

###############################################
######### Team Register/ Tour. Signup #########
###############################################

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

def enter_signup(team,tournament):
    # find landing sheet 2 and place team name and tournament in next available cells
    sheet = get_sheet("TagPro Championship Series RAW STATS")
    s = sheet.worksheet("Landing Sheet 2")
    column_a = s.col_values(1)
    for cell in column_a:
        row = str(column_a.index(cell)+1)
        if cell == '' and s.acell('B'+row).value == '':
            s.update_acell('A'+row, tournament.abv)
            s.update_acell('B'+row, team.name)
            break

def remove_signup(team,tournament):
    # find signup for tournament and remove it
    sheet = get_sheet("TagPro Championship Series RAW STATS")
    s = sheet.worksheet("Landing Sheet 2")

    team_matches = s.findall(team.name)
    for team in team_matches:
        row = str(team.row)
        tour = s.acell('A'+row).value
        if tour == tournament.abv:
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

###############################################
########## Activate/End Tournament ############
###############################################

def activate_tournament(tournament):
    # activate tournament, set all the first games
    sheet = get_sheet("TagPro Championship Series RAW STATS")
    s = sheet.worksheet(get_server_sheet(tournament.abv))
    for team in tournament.team_set.all():
        set_new_game(s,team,tournament)
    tournament.active = True
    tournament.save()

def set_new_game(s,team,tournament):
    # create new game, set status according to if both teams are present
    game_cell = get_cell_list(s,team,tournament)[-1]
    game_row = game_cell.row
    game_col = game_cell.col
    game_number = s.cell(game_row,game_col-1).value if is_team1(s,game_cell) else s.cell(game_row,game_col-2).value
    teams = get_teams(s,game_cell)
    winner_loser = get_winner_loser_cols(s,tournament)
    winner_col,loser_col = winner_loser['winner_col'],winner_loser['loser_col']
    winner_val, loser_val = s.cell(game_row,winner_col).value, s.cell(game_row,loser_col).value
    status = 1 if teams['team1'] is None or teams['team2'] is None else 2
    if not (winner_val == '' and loser_val == ''): return
    if Game.objects.filter(number=game_number,tournament=tournament).exists(): return
    game = Game.objects.create(
        number=game_number,
        team1=teams['team1'],
        team2=teams['team2'],
        row=game_row,
        winner_col=winner_col,
        loser_col=loser_col,
        tournament=tournament,
        status=status
    )
    return game

def get_teams(s,game_cell):
    # get team1 and team2, if empty value return None
    game_row = game_cell.row
    game_col = game_cell.col
    team1_name = game_cell.value if is_team1(s,game_cell) else s.cell(game_row,game_col-1).value
    team2_name = s.cell(game_row,game_col+1).value if is_team1(s,game_cell) else game_cell.value
    team1 = Team.objects.get(name=team1_name) if team1_name != '' else None
    team2 = Team.objects.get(name=team2_name) if team2_name != '' else None
    return {'team1':team1,'team2':team2}


def get_winner_loser_cols(s,tournament):
    # Get winner and loser columns based on tournament
    tour_cell = s.find(tournament.abv)
    winner_col = tour_cell.col + 6
    loser_col = tour_cell.col + 7
    return {'winner_col':winner_col,'loser_col':loser_col}

def is_team1(s,cell):
    # check if team is in team1 column or team2
    if s.cell(4,cell.col).value == 'Team 1': return True
    else: return False

def end_tournament(tournament):
    # end tournament
    tournament.active = False
    tournament.save()

###############################################
############# Check For Game ##################
###############################################

def check_for_game(team,tournament):
    # check for latest unsubmitted game, if game is looking
    # then look for next opponent, if set return so user can submit
    game = team.get_unsubmitted_game(tournament)
    if not game.exists(): return False
    game = game.latest('id')
    if game.status == 1: return look_for_opponent(team,tournament,game)
    return game

def look_for_opponent(team,tournament,game):
    # looking for next opponent, if none return False, if there is then set the teams
    sheet = get_sheet("TagPro Championship Series RAW STATS")
    s = sheet.worksheet(get_server_sheet(tournament.abv))
    opp_col = get_team2_col(s,tournament) if game.team2 is None else get_team1_col(s,tournament)
    opp = s.cell(game.row,opp_col)
    if opp.value == '': return False
    else: return set_looking_game(game,opp.value)

def set_looking_game(game,new_team_name):
    # set other team in game waiting for second opponent
    new_team = Team.objects.get(name=new_team_name)
    if game.team1 is None: game.team1 = new_team
    else: game.team2 = new_team
    game.status = 2
    game.save()
    return game

def get_team1_col(s,tournament):
    # get the team1 column number based on the tournament
    tour_col = s.find(tournament.abv).col
    return tour_col + 4

def get_team2_col(s,tournament):
    # get the team2 column number based on the tournament
    tour_col = s.find(tournament.abv).col
    return tour_col + 5

###############################################
############# Submit Game #####################
###############################################

def submit_game(game,game_links):
    # get stats from eus and fill in winner/loser
    sheet = get_sheet("Championship Series TagPro.eu Extractor")
    s = sheet.worksheet("Copy")
    clear_first_copy_row(s)
    fill_copy_cells(s,game_links)
    rows = get_copy_rows(s)
    s = sheet.worksheet("Export")
    fill_export_rows(s,rows)
    fill_winner_loser(game)

def clear_first_copy_row(s):
    # clear first row of cells on copy sheet
    first_row = s.range('B1:M1')
    for cell in first_row:
        cell.value = ''
    s.update_cells(first_row)

def fill_copy_cells(s,game_links):
    # fill top row cells in copy sheet to produce rows to copy
    s.update_cell(1,2,split_link(game_links['g1h1']))
    if 'g1h1time' in game_links: s.update_cell(1,3,split_link(game_links['g1h1time']))
    s.update_cell(1,4,split_link(game_links['g1h2']))
    if 'g1h2time' in game_links: s.update_cell(1,5,split_link(game_links['g1h2time']))
    if 'g1ot1' in game_links: s.update_cell(1,6,split_link(game_links['g1ot1']))
    if 'g1ot2' in game_links: s.update_cell(1,7,split_link(game_links['g1ot2']))
    s.update_cell(1,8,split_link(game_links['g2h1']))
    if 'g2h1time' in game_links: s.update_cell(1,9,split_link(game_links['g2h1time']))
    s.update_cell(1,10,split_link(game_links['g2h2']))
    if 'g2h2time' in game_links: s.update_cell(1,11,split_link(game_links['g2h2time']))
    if 'g2ot1' in game_links: s.update_cell(1,12,split_link(game_links['g2ot1']))
    if 'g2ot2' in game_links: s.update_cell(1,13,split_link(game_links['g2ot2']))

def split_link(link):
    # get eu id from end of eu link
    return link.split('match=')[1]

def get_copy_rows(s):
    return [cell for cell in s.range(5,3,31,24) if cell.value != '']

def fill_export_rows(s,rows):
    row = find_open_row(s)
    num_rows = rows[-1].row - rows[0].row
    new_cells = s.range(row,3,row+num_rows,24)
    for i,cell in enumerate(new_cells):
        cell.value = rows[i].value
    s.update_cells(new_cells)

def find_open_row(s):
    # find first open row to copy rows into
    vals = s.col_values(5)
    for cell in vals:
        if cell == '': return (vals.index(cell) + 1)

def fill_winner_loser(game):
    sheet = get_sheet("TagPro Championship Series RAW STATS")
    s = sheet.worksheet(get_server_sheet(game.tournament.abv))
    s.update_cell(game.row, game.winner_col, game.winner.name)
    s.update_cell(game.row, game.loser_col, game.loser.name)
    game.status = 3
    game.save()
    if game.number == 'FINALS': return end_tournament(game.tournament)
    set_new_game(s,game.winner,game.tournament)
    set_new_game(s,game.loser,game.tournament)

def get_cell_list(s,team,tournament):
    # Get team name in team1 and team2 columns based on tournament
    tour_cell = s.find(tournament.abv)
    start_row = tour_cell.row + 4
    start_col = tour_cell.col + 4
    finish_row = start_row + 29
    finish_col = start_col + 1
    cell_range = s.range(start_row,start_col,finish_row,finish_col)
    cell_list = [cell for cell in cell_range if cell.value == team.name]
    return cell_list

###############################################

def get_server_sheet(abv):
    # get specific sheet for certain server tournament
    if abv[0] == 'R' or abv[0] == 'T': return "RADIUS"
    elif abv[0] == 'S': return "Sphere"
    elif abv[0] == 'C': return "Centra"
    else: return ''
