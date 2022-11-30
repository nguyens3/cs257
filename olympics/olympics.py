'''
   CS.257 Software Design
   Professor Jeff Ondich
   Author: Sydney Nguyen 

   This program works with a populated olympics database to implement certain queries. A copy of the databased used
   to model this program is in olympics.sql. This program also borrows some code from Jeff's psycopg2-sample.py 
   provided with the "LAB: POSTGRES AND PYTHON USING PSYCOPG2".
'''

import sys
import psycopg2
import config

def get_connection():
    '''Returns a database connection object with which you can create cursors,
    issue SQL queries, etc. This function is extremely aggressive about
    failed connections--it just prints an error message and kills the whole
    program. Sometimes that's the right choice, but it depends on your error-handling needs.'''
    try:
        return psycopg2.connect(database=config.database, user=config.user, password=config.password)
    except Exception as e:
        print (e, file=sys.stderr)
        exit()

def get_athletes(search_text):
    '''Returns a list of the full names of all athletes in the database whose NOC are equal to the specified search string.'''
    athletes = []
    try:
        query = '''SELECT DISTINCT athletes.name 
                FROM athletes, NOC, olympic_games_events
                WHERE athletes.id = olympic_games_events.athletes_id
                AND noc.id = olympic_games_events.noc_id
                AND noc.abbreviation = %s'''
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (search_text,))
        for row in cursor:
            given_name = row[0]
            athletes.append(given_name)
    except Exception as e:
        print(e, file=sys.stderr)
    
    connection.close()
    return athletes

def get_noc_medals():
    '''Returns a list of all the NOCs and the number of gold medals they have won, in decreasing order of the number of gold medals.'''
    noc_medals =[]
    noc_list=[]
    try:
        connection = get_connection()
        cursor = connection.cursor()
        #Gathers all countries that won gold medals
        query_gold = '''SELECT noc.abbreviation, olympic_games_events.medal, COUNT(olympic_games_events.medal)
                    FROM noc, olympic_games_events
                    WHERE noc.id = olympic_games_events.noc_id
                    AND olympic_games_events.medal = 'Gold'
                    GROUP BY noc.abbreviation, olympic_games_events.medal
                    ORDER BY COUNT(olympic_games_events.medal) DESC'''
        cursor.execute(query_gold)
        for row in cursor:
            noc = row[0]
            count = row[2]
            noc_medals.append([noc, count])
            noc_list.append(noc)
        #Takes into account all the countries that won no gold medals
        query_noc = '''SELECT noc.abbreviation
                FROM NOC
                ORDER BY noc.abbreviation'''
        cursor.execute(query_noc)
        for row in cursor:
            noc = row[0]
            zero_count = '0'
            if noc not in noc_list:
                noc_medals.append([noc, zero_count])
    except Exception as e:
        print(e, file=sys.stderr)
    
    connection.close()
    return noc_medals

def get_athlete_medals(search_text):
    '''Returns a list of all the medals won by a specified athlete listed in chronological order of games competed.'''
    athlete_medals=[]
    #Takes into account if the search string is not given exactly as the names in the database
    search_text=search_text.replace(" ", "%%")
    try:
        query = '''SELECT olympic_games_events.medal, olympic_games.year, olympic_games.season, events.name, noc.abbreviation
        FROM athletes, olympic_games, events, noc,  olympic_games_events
        WHERE athletes.id = olympic_games_events.athletes_id
        AND olympic_games.id = olympic_games_events.olympic_games_id
        AND events.id = olympic_games_events.events_id
        AND noc.id = olympic_games_events.noc_id
        AND athletes.name ILIKE CONCAT('%%', %s, '%%')
        ORDER BY olympic_games.year'''
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (search_text,))
        for row in cursor:
            medal = str(row[0])
            year = str(row[1])
            season = str(row[2])
            event = str(row[3])
            noc = str(row[4])
            #For formatting printing later
            athlete_medals.append([medal, year, season, event, noc])
    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return athlete_medals

def print_usage():
    usage = open('usage.txt')
    print(usage.read())
    usage.close()

def extra_instances():
    print("Amount of inputs cannot be handled. Refer to usage statement below.")
    print_usage()

def main():
    if("-h" in sys.argv or "--help" in sys.argv):
        print_usage()
    
    elif(len(sys.argv) == 1): #If no method is specified
        print("Not a valid method. Refer to usage statement below.")
        print_usage()

    elif(sys.argv[1] == "gold"):
        if len(sys.argv) == 2: #No extra instances given
            noc_gold = get_noc_medals()
            print('===== The Number of Gold Medals Won by all NOCs in Decreasing Order =====')
            for noc in noc_gold:
                print(noc[0] + ':' + str(noc[1]))
            print()
        else:
            extra_instances()
    
    elif(sys.argv[1] == "medals"):
        if len(sys.argv) == 3: #No extra instances given
            name = sys.argv[2]
            athlete_medals = get_athlete_medals(name)
            if athlete_medals == []:
                print("No athlete found. Refer to usage statement below.")
                print_usage()
            else:
                print(f'========== ALl Medals Won by "{name}"==========')
                for athlete in athlete_medals:
                    print(athlete[0] + ' ' + athlete[1] + ' ' + athlete[2] + ' ' + athlete[3] + ' ' + athlete[4])
                print()
        else:
            if len(sys.argv) < 3:
                print("Not enought inputs: Specify an athlete in quotes. Ex: \"Greg Louganis\". Refer to the usage statement below for more information.")
                print_usage()
            else:
                extra_instances()
    
    elif(sys.argv[1] == "athletes"):
        if len(sys.argv) == 3: #No extra instances given
            noc = sys.argv[2]
            athletes = get_athletes(noc)
            if athletes == []:
                print("No NOC found. Refer to usage statement below.")
                print_usage()
            else:
                print(f'========== All Athletes from "{noc}" ==========')
                for athlete in athletes:
                    print(athlete)
                print()
        else:
            if len(sys.argv) < 3:
                print("Not enough inputs: Specify a NOC in quotes (Ex. \"SGP\"). Refer to the usage statement below for more information.")
                print_usage()
            else:
                extra_instances()
    
    else:
        print("Not a valid method. Refer to usage statement below.")
        print_usage()

if __name__ == '__main__':
    main()