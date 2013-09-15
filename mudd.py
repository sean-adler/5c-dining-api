## Mudd scraper
## Green Pod, CA
## Sean Adler


###  This one is by far the worst to scrape.
###    Have fun!!

import requests
from bs4 import BeautifulSoup
from copy import deepcopy
from pprint import pprint


##  Annoyingly, the correct suffix changes from week to week.
URL_SUFFIX = 'week_2.html'


resp = requests.get('http://hmcdining.com/dining/menus/'+URL_SUFFIX)
soup = BeautifulSoup(resp.text)

DAYS = ['friday', 'saturday', 'sunday', 'monday',
        'tuesday', 'wednesday', 'thursday']
WEEKDAYS = [1,4,5,6,7]
WEEKENDS = [2,3]

## Get tr tags
## FRIDAY is second-from-left column (first is header column)

TRS = soup.findAll('tr')

def validMeal(string):
    return string != u'\xa0' and string != u''

def mealList(day_index):
    meals = []  ## Group of meals for a given day
    meal = []   ## Individual meal (e.g., lunch)
    for t in TRS:
        try:
            food = t.findAll('td')[day_index].text.strip()
            if food.upper() in ['BREAKFAST', 'LUNCH', 'DINNER']:
                ## We hit the end of a section (meal).
                ## Append to meals and start a new list of meals
                meals.append(filter(validMeal, meal))
                meal = []
            else:
                if food.lower() in DAYS or food.lower() == 'brunch':
                    pass
                else:
                    meal.append(food)
        except Exception:
            pass
    ## Append last meal (dinner) to meals list
    meals.append(filter(validMeal, meal))
    return meals

def mealDict(day_index, meals):
    if day_index in WEEKDAYS:
        return {'breakfast': meals[1],
                'lunch': meals[2],
                'dinner': meals[3]}
    elif day_index in WEEKENDS:
        return {'brunch': meals[0][1:],  ## First element of brunch is the date...
                'dinner': meals[1]}
    else:
        raise ValueError("`day_index` must be in range [1,2,3,4,5,6,7].")

def getMuddMenu():
    ## Common format --> keep days abbreviated to first 3 letters
    return {DAYS[i][:3] : mealDict(i+1, mealList(i+1))
            for i in range(len(DAYS))}

