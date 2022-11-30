'''
   CS.257 Software Design
   Professor Jeff Ondich
   Author: Sydney Ngueyn 

   This program borrows data from kaggle to populate the csv files created here. 
   Go to https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results for the source data.
   This program assumes you have a copy of the athlete_events.csv and noc_regions.csv.
'''

import csv

def dictionary_map():
   noc = {}
   with open('noc_regions.csv') as original_data_file,\
      open('noc.csv', 'w') as noc_file:
      reader = csv.reader(original_data_file)
      writer = csv.writer(noc_file)
      heading_row = next(reader) # skips the first line
      for row in reader:
         noc_abbreviation = row[0]
         region = row[1]
         if noc_abbreviation not in noc:
            noc_id = len(noc) + 1
            noc[noc_abbreviation] = noc_id
            writer.writerow([noc_id, noc_abbreviation, region])

   athletes = {}
   with open('athlete_events.csv') as original_data_file,\
      open ('athletes.csv', 'w') as athletes_file:
      reader = csv.reader(original_data_file)
      writer = csv.writer(athletes_file)
      heading_row = next(reader) # skips the first line
      for row in reader:
         athlete_id = row[0]
         athlete_name = row[1]
         athlete_sex = row[2]
         if athlete_id not in athletes:
            athletes[athlete_id] = athlete_name
            writer.writerow([athlete_id, athlete_name, athlete_sex])
   
   games = {}
   with open('athlete_events.csv') as original_data_file,\
      open ('olympic_games.csv', 'w') as games_file:
      reader = csv.reader(original_data_file)
      writer = csv.writer(games_file)
      heading_row = next(reader) # skips the first line
      for row in reader:
         game_year = row[9]
         game_season = row[10]
         game_year_season = row[8]
         game_city = row[11]
         if game_year_season not in games:
            game_id = len(games) + 1
            games[game_year_season] = game_id
            writer.writerow([game_id, game_year, game_season, game_city])
         

   event_categories = {}
   with open('athlete_events.csv') as original_data_file,\
      open('event_categories.csv', 'w') as category_file:
      reader = csv.reader(original_data_file)
      writer = csv.writer(category_file)
      heading_row = next(reader) # skips the first line
      for row in reader:
         category_name = row[12]
         if category_name not in event_categories:
            category_id = len(event_categories) + 1
            event_categories[category_name] = category_id
            writer.writerow([category_id, category_name])

   events = {}
   with open('athlete_events.csv') as original_data_file,\
      open('events.csv', 'w') as events_file:
      reader = csv.reader(original_data_file)
      writer = csv.writer(events_file)
      heading_row = next(reader) # skips the first line
      for row in reader:
         event_name = row[13]
         if event_name not in events:
            event_id = len(events) + 1
            events[event_name] = event_id
            category_name = row[12]
            category_id = event_categories[category_name]
            writer.writerow([event_id, category_id, event_name])
   
   with open('athlete_events.csv') as original_data_file,\
      open('olympic_games_events.csv', 'w') as olympic_games_events:
      reader = csv.reader(original_data_file)
      writer = csv.writer(olympic_games_events)
      heading_row = next(reader) # skips the first line
      for row in reader:
         olympic_games_id = games[row[8]]
         events_id = events[row[13]]
         noc_id = noc[row[7]]
         athletes_id = row[0]
         athlete_age = row[3]
         athlete_height = row[4]
         athlete_weight = row[5]
         medal = row[14]
         writer.writerow([olympic_games_id, events_id, noc_id, athletes_id, athlete_height, athlete_weight, athlete_age, medal])


if __name__ == '__main__':
   dictionary_map()
   
