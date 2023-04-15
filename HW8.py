# Your name: Liam Kendall
# Your student id: 6069 5995
# Your email: liamkend@umich.edu
# List who you have worked with on this homework: Zack Eisman

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
    d = {}
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    curCategory = conn.cursor()
    curBuilding = conn.cursor()

    cur.execute("SELECT * FROM restaurants")
    for row in cur:
        nest = {}
        name = row[1]
        category_id = row[2]
        building_id = row[3]
        rating = row[4]

        categories = curCategory.execute("SELECT * FROM categories")
        for row in categories:
            if category_id == row[0]:
                category = row[1]

        buildings = curBuilding.execute("SELECT * FROM buildings")
        for row in buildings:
            if building_id == row[0]:
                building = row[1]

        nest['category'] = category
        nest['building'] = building
        nest['rating'] = rating
        
        d[name] = nest
    
    cur.close()
    curCategory.close()
    curBuilding.close()
    return d

def plot_rest_categories(db):
    d = {}
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    curCategory = conn.cursor()

    categories = curCategory.execute("SELECT * FROM categories")
    for row in categories:
        d[row[1]] = 0

    cur.execute("SELECT * FROM restaurants")
    for row in cur:
        category_id = row[2]

        categories = curCategory.execute("SELECT * FROM categories")
        for row in categories:
            if category_id == row[0]:
                category = row[1]
        
        d[category] += 1
    
    cur.close()
    curCategory.close()

    x = list(d.keys())
    y = list(d.values())
    plt.bar(range(len(x)), y, tick_label=x)
    plt.show()

    return d

def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    l = []
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()

    cur.execute(f"SELECT buildings.building, restaurants.name, restaurants.rating FROM restaurants JOIN buildings ON restaurants.building_id = buildings.id WHERE buildings.building = {building_num} ORDER BY restaurants.rating DESC")
    for row in cur:
        l.append(row[1])

    return l

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    pass

#Try calling your functions here
def main():
    db = 'South_U_Restaurants.db'
    load_rest_data(db)
    plot_rest_categories(db)
    find_rest_in_building(1300, db)
    get_highest_rating(db)

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
