## Scraper for Scripps (Malott) Dining Hall.
## Claremont, CA
## Sean Adler

## Scraped from the Scripps Dining Hall RSS feed,
## which lists all meals in the next week.
## So we scrape once a week, on Monday, to align with other menus.

import feedparser
from pprint import pprint

DATA = feedparser.parse('https://emsweb.claremont.edu/ScrippsMC/RSSFeeds.aspx?d\
ata=3p3oPLk3vPIqlgR7GVicJVEY1uoLxMswNw0YQhkyHqT6cGpSHWhEe5k4c3Exs8yX')

DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

WEEKDAYS = DAYS[:5]
WEEKENDS = DAYS[5:]

WEEKDAY_MEALS = ['breakfast', 'lunch', 'dinner']
WEEKEND_MEALS = ['brunch', 'dinner']


def dayDict(day):
    "Takes a day from the Scripps RSS feed and returns a dict representation."
    day_meals = {entry['title'].lower():
                 formatMeals(entry['summary_detail']['value'])
                 for entry in DATA['entries']
                 if day in entry['published']
                }

    if day in WEEKDAYS:
        for meal in WEEKDAY_MEALS:
            if meal not in day_meals: day_meals[meal] = []

    elif day in WEEKENDS:
        for meal in WEEKEND_MEALS:
            if meal not in day_meals: day_meals[meal] = []

    return day_meals

def formatMeals(meals):
    "Takes a semicolon-delimited string of meals and returns a list of meals."
    meals = filter(None, meals.split(';'))
    return map(lambda s: s.strip(), meals)

def getScrippsMenu():
    return {day.lower() : dayDict(day) for day in DAYS}
