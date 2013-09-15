## Scraper for Frary dining hall.

from selenium import webdriver
from bs4 import BeautifulSoup

## Open page with PhantomJS (headless browser)
browser = webdriver.PhantomJS('./vendor/phantomjs-1.9.0-linux-x86_64/bin/phantomjs')
#browser = webdriver.PhantomJS('/usr/local/bin/phantomjs')
browser.get('http://www.pomona.edu/administration/dining/menus/frary.aspx')
content = browser.page_source
browser.quit()

## BeautifulSoup lets us parse the DOM
soup = BeautifulSoup(content)
tables = soup.findAll('table', class_='menu')

days = ['monday', 'tuesday', 'wednesday', 'thursday',
        'friday', 'saturday', 'sunday']


#####  NOTES:
## monday = tables[0]
## tuesday = tables[1]
## wednesday = tables[2]
## thursday = tables[3]
## friday = tables[4]
## saturday = tables[5]
## sunday = tables[6]
#####


def splitOnPattern(meal_list, pattern):
    meal_list = map(lambda s: s.split(pattern), meal_list)
    return [m for sublist in meal_list for m in sublist]

def getMeals(day_id):
    print "day_id: ", day_id
    if day_id in [0,1,2,3,4]:
        return getWeekdayMeals(day_id)
    elif day_id in [5,6]:
        return getWeekendMeals(day_id)
    else:
        raise ValueError("Day_ID must be in range [0-6].")

def getWeekdayMeals(day_id):
    "Takes an int in range [0-4] and returns a dict of all meals that day."

    breakfast = tables[day_id].findAll('td', class_='breakfast')
    lunch = tables[day_id].findAll('td', class_='lunch')
    dinner = tables[day_id].findAll('td', class_='dinner')

    breakfast = filter(None, [f.text for f in breakfast])
    lunch = filter(None, [f.text for f in lunch])
    dinner = filter(None, [f.text for f in dinner])
    
    splitComma = lambda s: s.split(', ')
    strStrip = lambda s: s.encode('ascii', 'ignore').strip()

    
    
    breakfast = map(splitComma, breakfast)
    breakfast = [b for sublist in breakfast for b in sublist]
    breakfast = map(strStrip, breakfast)

    lunch = map(splitComma, lunch)
    lunch = [b for sublist in lunch for b in sublist]
    lunch = map(strStrip, lunch)

    dinner = map(splitComma, dinner)
    dinner = [b for sublist in dinner for b in sublist]
    dinner = map(strStrip, dinner)

    meals_dict = {'breakfast': breakfast,
                  'lunch': lunch,
                  'dinner': dinner}

    return meals_dict

def getWeekendMeals(day_id):
    "Takes an int in range [5-6] and returns a dict of all meals that day."
    brunch = tables[day_id].findAll('td', class_='brunch')
    dinner = tables[day_id].findAll('td', class_='dinner')

    brunch = filter(None, [f.text for f in brunch])
    dinner = filter(None, [f.text for f in dinner])

    ## Split on commas, and flatten into one list
    splitComma = lambda s: s.split(', ')
    strStrip = lambda s: s.encode('ascii', 'ignore').strip()

    brunch = map(splitComma, brunch)
    brunch = [b for sublist in brunch for b in sublist]
    brunch = map(strStrip, brunch)

    dinner = map(splitComma, dinner)
    dinner = [b for sublist in dinner for b in sublist]
    dinner = map(strStrip, dinner)

    meals_dict = {'brunch': brunch,
                  'dinner': dinner}

    return meals_dict


def getFraryMenu():
    ## Common format --> keep days abbreviated to first 3 letters
    return {days[i][:3] : getMeals(i) for i in range(len(days))}
