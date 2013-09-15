## Serves JSON API for CMC, Frary, Frank, Mudd, Scripps, & Pitzer Dining Halls
## Claremont, CA
## Sean Adler

from flask import Flask, jsonify
import json
import os
import time
import threading
import mongoengine
from flask.ext.mongoengine import MongoEngine
from ConfigParser import ConfigParser
import sqlite3


from collins import *
from pitzer import *
from mudd import *
from frary import *
from frank import *
from scripps import *


APP = Flask(__name__)  # global app object

LAST_UPDATE = 0  # Update menus immediately, and then 1x per day afterwards


##############
## DATABASE ##
##############

parser = ConfigParser()
parser.read('mongo.cfg')
DB_NAME = parser.get('mongo', 'DB_NAME')
DB_USERNAME = parser.get('mongo', 'DB_USERNAME')
DB_PASSWORD = parser.get('mongo', 'DB_PASSWORD')
DB_HOST_ADDRESS = parser.get('mongo', 'DB_HOST_ADDRESS')

APP.config["MONGODB_DB"] = DB_NAME
mongoengine.connect(DB_NAME, host='mongodb://' + DB_USERNAME + ':'
        + DB_PASSWORD + '@' + DB_HOST_ADDRESS)

DB = MongoEngine(APP)

## Schema ##

class Menu(DB.DynamicDocument):
    name = DB.StringField(max_length=16)
    menu = DB.DictField()


######################
## Helper functions ##
######################

#@APP.before_request
def updateMenusIfNecessary():
    "Calls `updateMenus()` every 24 hours, and once on app boot-up."
    global LAST_UPDATE
    if time.time() > LAST_UPDATE + 24*60*60:
        t = threading.Thread(target=updateMenus)
        t.start()
        LAST_UPDATE = time.time()

def updateMenus():
    "Scrapes all menus and updates them in MongoDB."

    print "Updating menus..."
    
    collins_menu = Menu.objects(name='collins').get()
    collins_menu.menu = getCollinsMenu()
    collins_menu.save()

    pitzer_menu = Menu.objects(name='pitzer').get()
    pitzer_menu.menu = getPitzerMenu()
    pitzer_menu.save()

    frary_menu = Menu.objects(name='frary').get()
    frary_menu.menu = getFraryMenu()
    frary_menu.save()

    frank_menu = Menu.objects(name='frank').get()
    frank_menu.menu = getFrankMenu()
    frank_menu.save()

    scripps_menu = Menu.objects(name='scripps').get()
    scripps_menu.menu = getScrippsMenu()
    scripps_menu.save()

    mudd_menu = Menu.objects(name='mudd').get()
    mudd_menu.menu = getMuddMenu()
    mudd_menu.save()

    all_menus = Menu.objects(name='all').get()
    all_menus.menu = {'collins': collins_menu.menu,
                      'pitzer': pitzer_menu.menu,
                      'frank': frank_menu.menu,
                      'frary': frary_menu.menu,
                      'scripps': scripps_menu.menu,
                      'mudd': mudd_menu.menu
                     }
    all_menus.save()

    print "Done updating."


############
## ROUTES ##
############


@APP.route('/')
def index():
    updateMenusIfNecessary()
    return jsonify({'routes':
                    ['/collins',
                     '/pitzer',
                     '/frary',
                     '/frank',
                     '/scripps',
                     '/mudd',
                     '/all']
                  })

@APP.route('/collins')
def collins():
    updateMenusIfNecessary()
    collins_menu = Menu.objects(name='collins').get().menu
    return jsonify(collins_menu)

@APP.route('/frank')
def frank():
    updateMenusIfNecessary()
    frank_menu = Menu.objects(name='frank').get().menu
    return jsonify(frank_menu)

@APP.route('/frary')
def frary():
    updateMenusIfNecessary()
    frary_menu = Menu.objects(name='frary').get().menu
    return jsonify(frary_menu)

@APP.route('/pitzer')
def pitzer():
    updateMenusIfNecessary()
    pitzer_menu = Menu.objects(name='pitzer').get().menu
    return jsonify(pitzer_menu)

@APP.route('/scripps')
def scripps():
    updateMenusIfNecessary()
    scripps_menu = Menu.objects(name='scripps').get().menu
    return jsonify(scripps_menu)

@APP.route('/mudd')
def mudd():
    updateMenusIfNecessary()
    mudd_menu = Menu.objects(name='mudd').get().menu
    return jsonify(mudd_menu)

@APP.route('/all')
def all():
    updateMenusIfNecessary()
    all_menus = Menu.objects(name='all').get().menu
    return jsonify(all_menus)


############
## Deploy ##
############

def deploy(heroku=True):
    """Simple deploy script -- we use different host/port values depending on
       if we want to test this locally, or actually push to Heroku."""
    if heroku:
        if __name__ == '__main__':
            ## Bind to PORT if defined, otherwise default to 5000.
            port = int(os.environ.get('PORT', 5000))
            APP.run(host='0.0.0.0', port=port)
    else:
        ## We run the APP locally:  
        if __name__ == '__main__':
            APP.run(port=5001)

deploy(heroku=True)


