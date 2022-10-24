'''
   booksdatasourcetest.py
   Jeff Ondich, 24 September 2021
   Authors: Sydney Nguyen and Kimberly Yip
   Revised by: Sydney Nguyen and Kimberly Yip
'''

from booksdatasource import Author, Book, BooksDataSource
import unittest

class BooksDataSourceTester(unittest.TestCase):
    def setUp(self):
        self.data_source = BooksDataSource('books1.csv')

    def tearDown(self):
        pass

    def test_unique_author(self):
        authors = self.data_source.authors('Pratchett')
        self.assertTrue(authors[0] == Author('Pratchett', 'Terry'))

    def test_search_author_two_lastname(self):
        authors = self.data_source.authors('Grenville Wodehouse')
        self.assertTrue(authors[0] == Author('Grenville Wodehouse', 'Pelham'))

    def test_search_author_special_character(self):
        authors = self.data_source.authors('García Márquez')
        self.assertTrue(authors[0] == Author('García Márquez', 'Gabriel'))
  
    def test_search_author_multiple_lastname(self):
        authors = self.data_source.authors('Brontë')
        self.assertTrue(authors[0] == Author('Brontë', 'Ann'))
        self.assertTrue(authors[1] == Author('Brontë', 'Charlotte'))
        self.assertTrue(authors[2] == Author('Brontë', 'Emily'))
	
    def test_search_year_begginning(self):
        titles = self.data_source.books_between_years(2020, None)
        self.assertTrue(titles[0] == Book('Boys and Sex')) 
        self.assertTrue(titles[1] == Book('The Invisible Life of Addie LaRue')) 
	
    def test_search_year_end(self):
        titles = self.data_source.books_between_years(None, 1813)
        self.assertTrue(titles[0] == Book('The Life and Opinions of Tristram Shandy, Gentleman'))
        self.assertTrue(titles[1] == Book('Pride and Prejudice')) 
        self.assertTrue(titles[2] == Book('Sense and Sensibility')) 
	
    def test_search_year_range(self):
        titles = self.data_source.books_between_years(1813, 1847)
        self.assertTrue(titles[0] == Book('Pride and Prejudice'))
        self.assertTrue(titles[1] == Book('Sense and Sensibility')) 
        self.assertTrue(titles[2] == Book('Emma')) 
        self.assertTrue(titles[3] == Book('Jane Eyre')) 
	
    def test_search_title_special_char(self):
        titles = self.data_source.books('\"There, There\"')
        self.assertTrue(titles[0] == Book('There, There'))

    def test_search_title_multiple(self):
        titles = self.data_source.books('and')
        self.assertTrue(titles[0] == Book('And Then There Were None'))
        self.assertTrue(titles[1] == Book('Boys and Sex'))
        self.assertTrue(titles[2] == Book('Girls and Sex'))
        self.assertTrue(titles[3] == Book('Hard-Boiled Wonderland and the End of the World'))
        self.assertTrue(titles[4] == Book('Pride and Prejudice'))
        self.assertTrue(titles[5] == Book('Sense and Sensibility'))
        self.assertTrue(titles[6] == Book('The Life and Opinions of Tristram Shandy, Gentleman'))

    def test_search_title_numbers(self):
        titles = self.data_source.books('1Q84')
        self.assertTrue(titles[0] == Book('1Q84'))

    def test_sort_author(self):
        authors_list = self.data_source.authors()
        self.assertTrue(authors_list[0] == Author('Austen', 'Jane'))
        self.assertTrue(authors_list[1] == Author('Baldwin', 'James'))
        self.assertTrue(authors_list[2] == Author('Brontë', 'Ann')) 
        self.assertTrue(authors_list[3] == Author('Brontë', 'Charlotte')) 
        self.assertTrue(authors_list[4] == Author('Brontë', 'Emily'))
			
    def test_sort_title(self):
        title_list = self.data_source.books()
        self.assertTrue(title_list[0] == Book('1Q84'))
        self.assertTrue(title_list[1] == Book('A Wild Sheep Chase'))
        self.assertTrue(title_list[2] == Book('All Clear'))
        self.assertTrue(title_list[3] == Book('And Then There Were None')) 
        self.assertTrue(title_list[4] == Book('Beloved')) 
        self.assertTrue(title_list[5] == Book('Blackout'))

#assuming that it sorts from past to present
    def test_sort_year(self):
        title_list = self.data_source.books_between_years()
        self.assertTrue(title_list[0] == Book('The Life and Opinions of Tristram Shandy, Gentleman'))
        self.assertTrue(title_list[1] == Book('Pride and Prejudice'))
        self.assertTrue(title_list[2] == Book('Sense and Sensibility')) 
        self.assertTrue(title_list[3] == Book('Emma')) 
        self.assertTrue(title_list[4] == Book('Jane Eyre'))

if __name__ == '__main__':
    unittest.main()
