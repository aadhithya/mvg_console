# coding=utf-8
from mvg_console.mvg_api.mvg_api_requests import *
from mvg_console.history_manager import HistoryManager

from colr import color
from texttable import Texttable

import os
import sys
from pprint import pprint

MVG_BG = "#2a4779"
MVG_FG = "#ffffff"

######
# Types of Transports
# 1. UBAHN
# 2. BUS
# 3. REGIONAL_BUS
# 4. TRAM
# 5. SBAHN
# 5. NACHT_BUSs
#######

__package_name__ = "mvg_console"
__version__ = "2018.11.2"
__description__ = "A Command Line Tool to get the MVG departures for a station."

class Departure:
    
    def __init__( self, json ):
        self.label = json["label"]
        self.destination = json["destination"]
        self.departure_time_minutes = json["departureTimeMinutes"]
        self.line_background_color = json["lineBackgroundColor"]
        self.product = json["product"]


    def get_label_colored(self):
        return color(self.label, fore="#fff", back=self.line_background_color)
    
    def __str__(self):
        label = self.get_label_colored()
        direction = self.destination
        departure_min = self.departure_time_minutes

        return label + "\t" + direction + "\t" + str(departure_min)
        

def display_title_bar():
    """ Print a title bar. """

    color_it_mvg = lambda x: color(x, fore=MVG_FG, back=MVG_BG)
    bar_mvg_colored = color_it_mvg("*" * 48)
    fifteen_stars = "*" * 15

    print(bar_mvg_colored)
    print(color_it_mvg(fifteen_stars + " MVG - Departures " + fifteen_stars))
    print(bar_mvg_colored + "\n")


def display_departures(station_name, limit=10, mode=None):
    station_name = get_station_name(station_name)
    departuresJSON = get_departures_by_name(station_name)
    departures = []
    if mode is not None:
        for d in departuresJSON:
            if mode.upper() in d['product']:
                departures += [Departure(d)]
    else:
        departures = [ Departure(i) for i in departuresJSON ]

    departures = departures[:limit]
    
    print('\nStation: '+station_name+'\n')
    
    
    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.set_cols_dtype( ['t', 't', 'i'])
    table.set_cols_align( ['l', 'l', 'r'] )
    
    rows = []
    rows.append(['\x1b[38;5;231m\x1b[48;5;23mline\x1b[0m', 'destination', 'departure (min)'])
    for dep in departures:
        rows.append( [dep.get_label_colored(), dep.destination, dep.departure_time_minutes] )
    table.add_rows(rows)
    print( color(table.draw(), fore=MVG_FG, back=MVG_BG) )
    
def get_nearest_stations(address):
    location = get_locations(address)
    lat = location[0]['latitude']
    lng = location[0]['longitude']

    stations_json = get_nearby_stations(lat,lng)[:5]

    #print(len(stations_json))

    print('Nearest Stations to '+address+' :')
    print(''.join([str(idx+1)+". "+station['name']+": "+', '.join(station['products'])+'\n' for idx,station in enumerate(stations_json)]))
    return


def main():
    import argparse

    parser = argparse.ArgumentParser(prog="mvg")
    #print(parser)
    #args_group = parser.add_mutually_exclusive_group()
    args_group = parser
    args_group.add_argument("--version", "-v", help="Version Info.", action="store_true")
    args_group.add_argument("--recent", "-r", action="store_true", help="fetch the most recent search.")
    args_group.add_argument("--departures", "-d", help="Departures at Station/Stop", nargs='+')
    args_group.add_argument("--limit", "-l", help="# results to fetch")
    args_group.add_argument("--mode", "-m", help="Transportation Mode: bus, ubahn, sbahn, tram.")
    args_group.add_argument("--search", "-s", help="Gets stations closest to the address.", nargs='+')


    args = parser.parse_args()
    #print(args)
    recents_file_path = os.path.join(os.getcwd(), "recent.txt")
    history = HistoryManager(recents_file_path)
    result, latest_departure = history.get_latest()

    if args.recent:      
        print(args.recent)
        if not result:
            print(latest_departure)
        else:
            display_departures(latest_departure, mode=args.mode)
    elif args.departures: 
        if args.limit:
            display_departures(' '.join(args.departures), int(args.limit), args.mode)
        else:
            display_departures(' '.join(args.departures), mode=args.mode)
        with open(recents_file_path, "w") as recent:
            recent.write(' '.join(args.departures))
    elif args.search:
        get_nearest_stations(' '.join(args.search))
    elif args.version:
        print(__package_name__ +' version '+__version__+'\n'+__description__)
        sys.exit()
    else:
        top5 = history.get_top(5)
        # spaghetti cleanup pls
        if result:
            print("Your most recent stations:")
            print( "  ".join([str(idx+1)+". "+str(station) for idx, station in enumerate(top5)]) )
            display_departures(latest_departure, mode=args.mode)
        else:
            print('No recent stations.')

     

if __name__ == "__main__":
    main()