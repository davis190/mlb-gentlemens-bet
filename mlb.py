#!/usr/bin/python
# http://panz.io/mlbgame
import mlbgame
import datetime

##############
### INPUTS ###
##############
team = 'Cardinals'
year = 2017

########################
### Global Variables ###
########################
## Create list of oposing teams we care about
opposingTeams = {}
opposingTeams['Cardinals'] = ['Brewers','Cubs']
opposingTeams['Brewers'] = ['Cardinals','Cubs']
opposingTeams['Cubs'] = ['Brewers','Cardinals']

## Create array to store payouts by team
payout = {}
payout['Cardinals'] = 0
payout['Brewers'] = 0
payout['Cubs'] = 0

## Variables to track the current series
seriesPreviousDate = datetime.datetime(2010,1,1)
seriesPreviousTeam = ""
seriesWin = 0
seriesLoss = 0

## Main function. Loops through games
def main():
    month = getGames()
    print('----------------')

    # Loop through games and determine wether team won/lost or home/away
    for m in month:
        if m[0].away_team in opposingTeams[team]:
            if m[0].away_team_runs < m[0].home_team_runs:
                gameSummary = team + " beat " + m[0].away_team + " " + str(m[0].home_team_runs) + "-" + str(m[0].away_team_runs) + " on " + str(m[0].date.date())
                game_payout('win', m[0].away_team, m[0].date, gameSummary)
            else:
                gameSummary = team + " lost to " + m[0].away_team + " " + str(m[0].home_team_runs) + "-" + str(m[0].away_team_runs) + " on " + str(m[0].date.date())
                game_payout('lose', m[0].away_team, m[0].date, gameSummary)
        elif m[0].home_team in opposingTeams[team]:
            if m[0].away_team_runs > m[0].home_team_runs:
                gameSummary = team + " beat " + m[0].home_team + " " + str(m[0].away_team_runs) + "-" + str(m[0].home_team_runs) + " on " + str(m[0].date.date())
                game_payout('win', m[0].home_team, m[0].date, gameSummary)
            else:
                gameSummary = team + " lost to " + m[0].home_team + " " + str(m[0].away_team_runs) + "-" + str(m[0].home_team_runs) + " on " + str(m[0].date.date())
                game_payout('lose', m[0].home_team, m[0].date, gameSummary)

    is_series_game(seriesPreviousDate, datetime.datetime(2020,1,1), "No One")

    print("PAYOUT TOTALS")
    print("Kurtz: "+str(payout['Cubs']))
    print("Clayton: "+str(payout['Cardinals']))
    print("Casey: "+str(payout['Brewers']))

## Function to pull all games where team is question played
def getGames():
    print('Fetching January games...')
    month = mlbgame.games(year, 1, home=team, away=team)
    for i in range(2,12):
        dateMonth = datetime.datetime(year, i, 1)
        print("Fetching "+dateMonth.strftime("%B")+" games...")
        month = month + mlbgame.games(year, i, home=team, away=team)
    return month

## Determine if part of current series
def is_series_game(previous, current, opponent):
    global seriesLoss
    global seriesWin
    global seriesPreviousTeam

    dateDiff = current.date() - previous.date()
    # If the first pass - ignore the series
    if seriesPreviousTeam == "" and seriesPreviousDate == datetime.datetime(2010,1,1):
        return True
    # If still part of current series (same team, less than 2 days apart)
    elif dateDiff.days < 3 and opponent == seriesPreviousTeam:
        return True
    # Else means that a series ended. Process results
    else:
        if seriesWin > 0 or seriesLoss > 0:
            # If the team swept the oponent
            if seriesLoss == 0 and seriesWin > 0:
                payout[team] = payout[team] + 2
                payout[seriesPreviousTeam] = payout[seriesPreviousTeam] - 2
                print "SERIES: " + team + " SWEPT " + seriesPreviousTeam + " in series " + str(seriesWin) + "-" + str(seriesLoss)
            # If the team got swept by the oponent
            elif seriesWin == 0 and seriesLoss > 0:
                payout[team] = payout[team] - 2
                payout[seriesPreviousTeam] = payout[seriesPreviousTeam] + 2
                print "SERIES: " + team + " WAS SWEPT BY " + seriesPreviousTeam + " in series " + str(seriesLoss) + "-" + str(seriesWin)
            # If the team won the series
            elif seriesWin > seriesLoss:
                payout[team] = payout[team] + 1
                payout[seriesPreviousTeam] = payout[seriesPreviousTeam] - 1
                print "SERIES: " + team + " beat " + seriesPreviousTeam + " in series " + str(seriesWin) + "-" + str(seriesLoss)
            # If the team lost the series
            elif seriesWin < seriesLoss:
                payout[team] = payout[team] - 1
                payout[seriesPreviousTeam] = payout[seriesPreviousTeam] + 1
                print "SERIES: " + team + " lost to " + seriesPreviousTeam + " in series " + str(seriesLoss) + "-" + str(seriesWin)
            # If the series was tied
            else:
                print "series was tied " + str(seriesLoss) + "-" + str(seriesWin)
            print "---------------"
        # Reset series count
        seriesWin = 0
        seriesLoss = 0
        return False

# Function to determine game payout
def game_payout(outcome, opponent, currentDate, gameSummary):
    global seriesLoss
    global seriesWin
    global seriesPreviousDate
    global seriesPreviousTeam

    is_series_game(seriesPreviousDate, currentDate, opponent)
    print gameSummary
    if outcome == 'win':
        payout[team] = payout[team] + 1
        payout[opponent] = payout[opponent] - 1
        seriesWin = seriesWin + 1
    elif outcome == 'lose':
        payout[team] = payout[team] - 1
        payout[opponent] = payout[opponent] + 1
        seriesLoss = seriesLoss + 1
        
    seriesPreviousDate = currentDate
    seriesPreviousTeam = opponent

main()