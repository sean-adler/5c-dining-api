## Scraper for Collins dining hall.
## Claremont, CA
## Sean Adler

import requests
import feedparser
from bs4 import BeautifulSoup
from collections import defaultdict
from pprint import pprint

rss = feedparser.parse('http://legacy.cafebonappetit.com/rss/menu/50')


def collinsDayDict(day_index):
    entry = BeautifulSoup(rss.entries[day_index].summary)
    date = rss.entries[day_index].title[:4]
    tm = titles_and_meals = entry.findAll(['h3', 'h4'])

    meal_dict = defaultdict(list)

    for m in tm:
        if m.name == 'h3':
            meal_title = m.text
        elif m.name == 'h4':
            food = m.text.strip().split(', ')
            for f in food:
                station_and_food = f.split('] ')
                if len(station_and_food) > 1:
                    station = station_and_food[0]
                    food = station_and_food[1]
                    meal_dict[meal_title].append(food)
                else:
                    food = station_and_food[0]
                    meal_dict[meal_title].append(food)

    meal_dict = dict(meal_dict)
    return {key.lower(): value for key,value in meal_dict.iteritems()}


day_range = range(7)

days = ['monday', 'tuesday', 'wednesday', 'thursday',
        'friday', 'saturday', 'sunday']


def getCollinsMenu():
    return {days[i][:3] : collinsDayDict(i) for i in day_range}
