'''
    Author: Sydney Nguyen 
    Collaborator: Kimberly and Quoc 
    
    convert.py
    Jeff Ondich, 15 Oct 2021
    Started in class, polished later
    Illustrating how to use Python dictionaries, etc. to
    start converting the data. This is based on the Kaggle
    Olympics data, and assumes you have a copy of the
    athlete_events.csv file.
    In this small example, I am imagining three tables as shown
    below. The point of this code sample is to illustrate how you
    could connect the event_results table's ID fields to the
    appropriate IDs in the athletes and events tables.
    # Like "Simone Arianne Biles"
    CREATE TABLE athletes (
        id INTEGER,
        name TEXT
    );
    # Like "Gymnastics Women's Individual All-Around"
    CREATE TABLE events (
        id INTEGER,
        name TEXT
    );
    # One row represents one athlete competing in one event
    # at one time.
    CREATE TABLE event_results (
        athlete_id INTEGER,
        event_id INTEGER,
        medal TEXT
    );
    When I run this code, I end up with three new files: athletes.csv,
    events.csv, and event_results.csv. One of the lines of athletes.csv is:
        11495,Simone Arianne Biles
    One of the rows in events.csv is:
        213,Gymnastics Women's Individual All-Around
    And one of the rows in event_results.csv is:
        11495,213,Gold
    When you combine those three rows from three different tables, you can
    conclude that Simone Biles won the Gold medal in the
    Gymnastics Women's Individual All-Around. This sample program hasn't
    included year information or city information or anything like that.
    But I hope this code helps you understand one way to approach converting
    raw data into structured tabular data.
'''

import csv

# Strategy:
# (1) Create a dictionary that maps athlete IDs to athlete names
#       and then save the results in athletes.csv
# (2) Create a dictionary that maps event names to event IDs
#       and then save the results in events.csv
# (3) For each row in the original athlete_events.csv file, build a row
#       for our new event_results.csv table
#
# NOTE: I'm doing these three things in three different passes through
# the athlete_events.csv files. This is not necessary--you can do it all
# in a single pass.


# Create a dictionary that maps athlete_id -> athlete_name
#       and then save the results in athletes.csv
athletes = {}
with open('athlete_events.csv') as original_data_file,\
        open('athletes.csv', 'w',newline = '') as athletes_file:
    reader = csv.reader(original_data_file)
    writer = csv.writer(athletes_file)
    heading_row = next(reader) # eat up and ignore the heading row of the data file
    for row in reader:
        athlete_id = row[0]
        athlete_name = row[1]
        athlete_sex = row[2]
        if athlete_id not in athletes:
            athletes[athlete_id] = athlete_name
            writer.writerow([athlete_id, athlete_name,athlete_sex])



# Create a dictionary that maps event_name -> event_id
#    and then save the results in events.csv
events = {}
with open('athlete_events.csv') as original_data_file,\
        open('events.csv', 'w',newline = '') as events_file:
    reader = csv.reader(original_data_file)
    writer = csv.writer(events_file)
    heading_row = next(reader) # eat up and ignore the heading row of the data file
    for row in reader:
        category_name = row[12]
        event_name = row[13]
        if event_name not in events:
            event_id = len(events) + 1
            events[event_name] = event_id
            writer.writerow([event_id, event_name, category_name])


# Create a dictionary that maps games_year & games_season -> game_id
#       and then save the results in games.csv
games = {}
with open('athlete_events.csv') as original_data_file,\
        open('games.csv', 'w',newline = '') as games_file:
    reader = csv.reader(original_data_file)
    writer = csv.writer(games_file)
    heading_row = next(reader) # eat up and ignore the heading row of the data file
    for row in reader:
        game_id = len(games) + 1
        game_games = row[8]
        game_year = row[9]
        game_season = row[10]
        game_city = row[11]
        if game_games not in games:
            game_id = len(games) + 1
            games[game_games] = game_id        
            writer.writerow([game_id, game_year, game_season, game_city])


# Create a dictionary that maps athletes_noc -> noc_id
#       and then save the results in noc.csv
noc = {}
with open('noc_regions.csv') as original_data_file,\
    open('noc.csv', 'w',newline = '') as noc_file:
    reader = csv.reader(original_data_file)
    writer = csv.writer(noc_file)
    heading_row = next(reader)
    for row in reader:
        noc_abbreviation = row[0]
        region = row[1]
        #there is an issue with singapore when creating the keys and abreviations (only affects the event_results creation)
        if noc_abbreviation == 'SIN':
            noc_abbreviation = 'SGP' 
        if noc_abbreviation not in noc:
            noc_id = len(noc) + 1
            noc[noc_abbreviation] = noc_id
            writer.writerow([noc_id, noc_abbreviation, region])

        
# For each row in the original athlete_events.csv file, build a row
#       for our new event_results.csv table
with open('athlete_events.csv') as original_data_file,\
        open('event_results.csv', 'w',newline = '') as event_results_file:
    reader = csv.reader(original_data_file)
    writer = csv.writer(event_results_file)
    heading_row = next(reader) # eat up and ignore the heading row of the data file
    for row in reader:
        athlete_id = row[0]
        event_name = row[13]
        event_id = events[event_name] # this is guaranteed to work by section (2)
        game_name = row[8]
        game_id = games[game_name]
        noc_name = row[7]
        noc_id = noc[noc_name]
        medal = row[14]
        writer.writerow([athlete_id,noc_id, event_id, game_id, medal])
    