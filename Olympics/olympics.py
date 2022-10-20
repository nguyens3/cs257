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

def get_athletes_by_noc(search_text):
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

        # Iterate over the query results to produce the list of author names.
        for row in cursor:
            name = row[0]
            athletes.append(name)

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
                    AND athletes.athlete_name LIKE %s
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
            athletes.append(f'{name} {event} {game_year} {season} {medal}')
    
    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return athletes

def get_noc_medals():
    ''' Returns a list of medals won by noc in decreasing order '''
    athletes = []
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
            noc = row[0]
            medal = row[1]
            count = row[2]
            athletes.append(f'{noc} {medal} {count}')

    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return athletes

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
            print( get_athletes_by_name(sys.argv[2]))
    elif(sys.argv[1] == 'medals'):
        if(len(sys.argv) != 2):
            usage()
        else:
            print(get_noc_medals())
    elif(sys.argv[1] == 'search_athlete'):
        if(len(sys.argv) != 3):
            usage()
        else:
            print( get_athletes_by_noc(sys.argv[2]))
    else: 
        usage()


if __name__ == '__main__':
    main()
