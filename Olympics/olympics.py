#!/usr/bin/env python3
'''

    Author: Sydney Nguyen 
    
    Used code from: psycopg2-sample.py
    Jeff Ondich, 23 April 2016
    A very short, demo of how to use psycopg2 to connect to
    and query a PostgreSQL database. This demo assumes a "books"
    database like the one I've used in CS257 for the past few years,
    including an authors table with fields
        (id, given_name, surname, birth_year, death_year)
    You might also want to consult the official psycopg2 tutorial
    at https://wiki.postgresql.org/wiki/Psycopg2_Tutorial.
    Also, SEE THE NOTE BELOW ABOUT config.py. It's important.
'''
import sys
import psycopg2
import config


def get_connection():
    ''' Returns a database connection object with which you can create cursors,
        issue SQL queries, etc. This function is extremely aggressive about
        failed connections--it just prints an error message and kills the whole
        program. Sometimes that's the right choice, but it depends on your
        error-handling needs. '''
    try:
        return psycopg2.connect(database=config.database,
                                user=config.user,
                                password=config.password)
    except Exception as e:
        print(e, file=sys.stderr)
        exit()

def get_noc(search_text):
    ''' Returns a list of the full names of athletes from the given searchstring (noc). '''
    athletes = []

    try:
        # Create a "cursor", which is an object with which you can iterate
        # over query results.
        connection = get_connection()
        cursor = connection.cursor()

        # Execute the query
        query = '''SELECT DISTINCT athletes.athlete_name
                    FROM athletes, noc, results
                    WHERE athletes.id = results.athlete_id
                    AND noc.id = results.noc_id
                    AND noc.noc_region = %s
                    ORDER BY athletes.athlete_name ASC;'''       
        cursor.execute(query, (search_text,))

        for row in cursor:
            given_name = row[0]
            athletes.append(given_name)
    except Exception as e:
        print(e, file=sys.stderr)
    
    connection.close()
    return athletes

def get_athletes_by_name(search_text):
    athletes = []
    try:
        query = '''SELECT DISTINCT athletes.athlete_name, events.event_name, games.game_year, games.season, results.medal
                    FROM athletes, events, games, results
                    WHERE athletes.id = results.athlete_id
                    AND events.id = results.event_id
                    AND games.id = results.games_id
                    AND athletes.athlete_name ILIKE CONCAT('%%', %s, '%%')
                    AND results.medal IN ('Gold','Silver','Bronze')
                    ORDER BY games.game_year;'''
        
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (search_text,))
        for row in cursor:
            name = row[0]
            event = row[1]
            game_year = row[2]
            season = row[3] 
            medal = row[4]
            #appended as a list to make the printing pretty
            athletes.append([name,event,game_year,season,medal])
    
    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return athletes

def get_noc_medals():
    ''' Returns a list of medals won by noc in decreasing order '''
    noc = []
    noc_list = []
    try:
        query = '''SELECT noc.noc_abreviation, results.medal, COUNT(results.medal)
                    FROM noc, results
                    WHERE noc.id = results.noc_id
                    AND results.medal = 'Gold'
                    GROUP BY noc.noc_abreviation, results.medal
                    ORDER BY COUNT(results.medal) DESC;'''
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query,)
        for row in cursor:
            nocs = row[0]
            count = row[2]
            #appended as a list to make the printing pretty
            noc.append([nocs,count])
            noc_list.append(nocs)
        #for nocs with 0 gold medals 
        query ='''SELECT noc_abreviation
                FROM NOC
                ORDER BY noc_abreviation ASC;'''
        cursor = connection.cursor()
        cursor.execute(query,)
        for row in cursor:
            if row[0] not in noc_list:
                noc.append([row[0], 0])
    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return noc

def usage():
    usage = open('usage.txt')
    print(usage.read())
    usage.close()

def main():
    
    if("-h" in sys.argv or "--help" in sys.argv):
    # prints usage statement
        usage()
    elif(sys.argv[1] == 'athletes'):
        if(len(sys.argv) != 3):
            usage()
        else:
            output =  get_noc(sys.argv[2])
            if len(output) == 0:
                print(sys.argv[2] + ' : Does not exist in the dataset')
            else:
                for athlete in output:
                    print(athlete + '\n')
                
    elif(sys.argv[1] == 'medals'):
        if(len(sys.argv) != 2):
            usage()
        else:
            
            output = get_noc_medals()
            for noc in output:
                print(noc[0] + ' ' + str(noc[1]) + '\n' )
                
    elif(sys.argv[1] == 'search_athlete'):
        
        if(len(sys.argv) != 3):
            usage()
            
        else:
            output =  get_athletes_by_name(sys.argv[2])
            
            if len(output) == 0:
                print(sys.argv[2] + ' : Does not exist in the dataset')
            else:
                for athlete in output:
                    print(athlete[0] + ' ' + athlete[1] + ' ' + str(athlete[2]) + ' ' + athlete[3]+ ' ' +athlete[4] + '\n')
            
    else: 
        usage()


if __name__ == '__main__':
    main()
