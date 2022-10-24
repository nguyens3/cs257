'''
    books.py
    Jeff Ondich, 21 September 2022
    For use in the "books" assignment at the beginning of Carleton's
    CS 257 Software Design class, Fall 2022.
    
    Authors: Kimberly Yip and Sydney Nguyen
    Revised by: Sydney Nguyen and Kimberly Yip
'''

import csv 
import sys
import booksdatasource

def dne_authors():
  '''If an author does not exist, prints an error and usage statement.'''
  print("No authors found. Refer to usage statement below.")
  usage = open('usage.txt')
  print(usage.read())
  usage.close()

def dne_books():
  '''If an author does not exist, prints an error and usage statement.'''
  print("No books found. Refer to usage statement below.")
  usage = open('usage.txt')
  print(usage.read())
  usage.close()


def main():
  file = booksdatasource.BooksDataSource('books1.csv')
  output = ''
  if("-h" in sys.argv or "--help" in sys.argv):
  # prints usage statement
     usage = open('usage.txt')
     print(usage.read())
     usage.close()

  elif(sys.argv[1] == "author"):
  # When author parameter is given, runs author method with specified instances. 
    if len(sys.argv) == 2: # no instances given
      output = file.authors()
      for item in output:
        item.print_authors()
    elif len(sys.argv) == 3: # one instance given
      output = file.authors(sys.argv[2])
      if output == []:
        dne_authors()
      else:
        for item in output:
          item.print_authors()
    else:
      raise SyntaxError("Amount of inputs can not be handled")

  elif(sys.argv[1] == "books"):
  # When book parameter is given, runs book method with specified instances.
    if len(sys.argv) == 2: # no instances given
      output = file.books()
      for item in output:
        item.print_books()
    elif len(sys.argv) == 3: # no instance given (specified sorting)
      if sys.argv[2] == '-t': # sorting by title (default)
        output = file.books()
        if output == []:
          dne_books()
        else:
          for item in output:
            item.print_books()
      elif sys.argv[2] == '-y': # sorting by year
        output = file.books()
        if output == []:
          dne_books()
        else:
          years_sorted = sorted(output, key = lambda book: book.publication_year)
          for item in years_sorted:
            item.print_books()
      else:
        output = file.books(sys.argv[2]) # one instance given with no specified sorting (sorted by title default)
        if output == []:
          dne_books()
        else:
          for item in output:
            item.print_books()
    elif len(sys.argv) == 4: # one instance given (specified sorting)
      if sys.argv[3] == '-t': # sorting by title (default)
        output = file.books(sys.argv[2])
        if output == []:
          dne_books()
        else:
          for item in output:
            item.print_books()
      elif sys.argv[3] == '-y': # sorting by year
        output = file.books(sys.argv[2])
        if output == []:
          dne_books()
        else:
          years_sorted = sorted(output, key = lambda book: book.publication_year)
          for item in years_sorted:
            item.print_books()
    else:
      raise SyntaxError("Amount of inputs can not be handled")

  elif(sys.argv[1] == "range"):
  # When range parameter is given, runs books_between_years method with specified instances
    if len(sys.argv) == 2: # no parameters given
      output = file.books_between_years()
      for item in output:
        item.print_books()
    elif len(sys.argv) == 3: # one parameter given (start year)
      if sys.argv[2].isalpha():
        print("Input must be an integer. Refer to usage statement below")
        usage = open('usage.txt')
        print(usage.read())
        usage.close()
      else:
        output = file.books_between_years(sys.argv[2])
      if output == []:
        dne_books()
      else:
        for item in output:
          item.print_books()
    elif len(sys.argv) == 4: # two parameters given (start and end year)
      if sys.argv[2].isalpha() and sys.argv[3].isalpha():
        print("Input must be an integer. Refer to usage statement below")
        usage = open('usage.txt')
        print(usage.read())
        usage.close()
      else:
        output = file.books_between_years(sys.argv[2],sys.argv[3])
      if output == []:
        dne_books()
      else:
        for item in output:
          item.print_books()
    else:
      raise SyntaxError("Amount of inputs can not be handled")
  else:
    # If no parameter is given, prints error and usage statement.
    print("Not a valid method. Refer to usage statement below.")
    usage = open('usage.txt')
    print(usage.read())
    usage.close()
    
main()
