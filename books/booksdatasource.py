#!/usr/bin/env python3
'''
    booksdatasource.py
    Jeff Ondich, 21 September 2022

    For use in the "books" assignment at the beginning of Carleton's
    CS 257 Software Design class, Fall 2022.
    Authors: Sydney Nguyen and Kimberly Yip
    Revised by: Sydney Nguyen and Kimberly Yip
'''

import csv

class Author:
    def __init__(self, surname='', given_name='', birth_year=None, death_year=None, books=[]):
        self.surname = surname
        self.given_name = given_name
        self.birth_year = birth_year
        self.death_year = death_year
        self.books = books

    def __eq__(self, other):
        ''' For simplicity, we're going to assume that no two authors have the same name.'''
        return self.surname == other.surname and self.given_name == other.given_name
    
    '''For sorting authors, you could add a "def __lt__(self, other)" method
    to go along with __eq__ to enable you to use the built-in "sorted" function
    to sort a list of Author objects.
    '''

    def __lt__(self, other):
        if self.surname < other.surname:
            return True
        if self.surname == other.surname and self.given_name < other.given_name:
            return True
        return False
    
    def print_authors(self):
        print(self.given_name + " " + self.surname)
        for book in self.books:
            print("\t" + book.title + " " + str(book.publication_year))
        

class Book:
    def __init__(self, title='', publication_year=None, authors=[]):
        ''' Note that the self.authors instance variable is a list of
            references to Author objects. '''
        self.title = title
        self.publication_year = publication_year
        self.authors = authors

    def __eq__(self, other):
        ''' We're going to make the excessively simplifying assumption that
            no two books have the same title, so "same title" is the same
            thing as "same book". '''
        return self.title == other.title
    
    def __lt__(self, other):
        if self.title.strip('"') < other.title.strip('"'):
            return True
        return False

    def print_books(self):
        print(self.title + " " + str(self.publication_year))

class BooksDataSource:
    def __init__(self, books_csv_file_name):
        ''' The books CSV file format looks like this:

                title,publication_year,author_description

            For example:

                All Clear,2010,Connie Willis (1945-)
                "Right Ho, Jeeves",1934,Pelham Grenville Wodehouse (1881-1975)

            This __init__ method parses the specified CSV file and creates
            suitable instance variables for the BooksDataSource object containing
            a collection of Author objects and a collection of Book objects.
        '''
        # All authors and books objects for instance of classes
        self.authors_list = []
        self.book_list = []

        with open(books_csv_file_name) as input_file:
            reader = csv.reader(input_file)
            for column in reader:
                assert len(column) == 3
                book = Book(column[0], int(column[1]), []) # creates a book object
                if book not in self.book_list:
                    self.book_list.append(book) 
                for author_param in column[2].split(" and "): # if more than one author exists per book, separates the two authors
                    author_param = author_param.split(" ") # separates the author's first and last name
                    given_name = author_param[0]
                    if len(author_param) > 3: # if the author has two last names
                        surname = author_param[1] + " " + author_param[2]
                        life = author_param[3]
                        life = life.strip("(").strip(")").split("-")
                        birth_year = life[0]
                        if len(life) < 2:
                            death_year = None
                        else:
                            death_year = life[1]
                    else: # if the author only has one last name
                        surname = author_param[1]
                        life = author_param[2]
                        life = life.strip("(").strip(")").split("-")
                        birth_year = life[0]
                        if len(life) < 2:
                            death_year = None
                        else:
                            death_year = life[1]
                    author = Author(surname, given_name, birth_year, death_year, [book, ]) # creates an author object 
                    book.authors.append(author) # adds the author to the corresponding book
                    if Author(author.surname, author.given_name) not in self.authors_list: # checks if author is already in global list
                        self.authors_list.append(author)
                    else: # adds book to author object if author already in global list
                        index = self.authors_list.index(author) 
                        self.authors_list[index].books.append(book)
                    

    def authors(self, search_text=None):
        ''' Returns a list of all the Author objects in this data source whose names contain
            (case-insensitively) the search text. If search_text is None, then this method
            returns all of the Author objects. In either case, the returned list is sorted
            by surname, breaking ties using given name (e.g. Ann Brontë comes before Charlotte Brontë).
        '''
        author_sorted = []
        if search_text == None: # if there is no specified parameter, returns a sorted list of all authors and their books
            author_sorted = self.authors_list
        else: # if a specified parameter exists, returns a sorted list of all related authors and their books 
            search_text = search_text.lower()
            for author in self.authors_list:
                author_full = author.given_name.lower() + " " + author.surname.lower()
                if search_text in author_full and author not in author_sorted:
                    author_sorted.append(author)
        return sorted(author_sorted)

    def books(self, search_text=None, sort_by='title'):
        ''' Returns a list of all the Book objects in this data source whose
            titles contain (case-insensitively) search_text. If search_text is None,
            then this method returns all of the books objects.

            The list of books is sorted in an order depending on the sort_by parameter:

                'year' -- sorts by publication_year, breaking ties with (case-insenstive) title
                'title' -- sorts by (case-insensitive) title, breaking ties with publication_year
                default -- same as 'title' (that is, if sort_by is anything other than 'year'
                            or 'title', just do the same thing you would do for 'title')
        '''
        book_sorted = []
        if search_text == None: # if there is no specified parameter, returns a sorted list of all books
            book_sorted = self.book_list
        else: # if a specified parameter exists, returns a sorted list of all related books
            search_text = ''.join(filter(str.isalnum, search_text)) # strips the search_string of all punctuation
            for item in self.book_list: 
                search = ''.join(filter(str.isalnum, item.title)) # strips the related books of all punctuation for comparison
                if search_text.lower() in search.lower() and item not in book_sorted:
                    book_sorted.append(item)
        return sorted(book_sorted)
            
            
    def books_between_years(self, start_year=None, end_year=None):
        ''' Returns a list of all the Book objects in this data source whose publication
            years are between start_year and end_year, inclusive. The list is sorted
            by publication year, breaking ties by title (e.g. Neverwhere 1996 should
            come before Thief of Time 1996).

            If start_year is None, then any book published before or during end_year
            should be included. If end_year is None, then any book published after or
            during start_year should be included. If both are None, then all books
            should be included.
        '''
        book_sorted = []
        if start_year == None and end_year == None: # if there is no specified parameter, returns a sorted list of all books
            book_sorted = self.book_list
        else: # if a specified parameter exists, returns a sorted list of all related books
            for item in self.book_list:
                if end_year == None:
                    if int(start_year) <= item.publication_year and item not in book_sorted:
                        book_sorted.append(item)
                elif start_year == None: 
                    if int(end_year) >= item.publication_year and item not in book_sorted:
                        book_sorted.append(item)
                else: # if start_year and end_year are specified
                    if int(start_year) <= item.publication_year and int(end_year) >= item.publication_year:
                        if item not in book_sorted:
                            book_sorted.append(item)
        return sorted(book_sorted, key = lambda book: book.publication_year)
