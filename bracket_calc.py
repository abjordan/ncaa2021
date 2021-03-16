#!/usr/bin/env python3

import csv
import sys

class Game:

    # Need them to set LEFT, RIGHT, and METRIC
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return f"GAME({self.left} VS. {self.right})"

    def __repr__(self):
        return f"{self.left} vs {self.right}"

    def play(self, metric, use_max=True):
        if type(self.left) is Game:
            self.left = self.left.play(metric, use_max)
        if type(self.right) is Game:
            self.right = self.right.play(metric, use_max)

        print(f"{self.left} is playing {self.right}...", end='')

        if use_max:
            if metric[self.left] > metric[self.right]:
                print(f"{self.left} win!")
                return self.left
            else:
                print(f"{self.right} win!")
                return self.right
        else:
            if metric[self.left] < metric[self.right]:
                print(f"{self.left} win!")
                return self.left
            else:
                print(f"{self.right} win!")
                return self.right

class Tournament:

    games = {}

    def __init__(self, seeding):

        def do_region(region): 
            round_64 = []
            for pairing in seeding[region]:
                round_64.append( Game(pairing[0], pairing[1]) )

            round_32 = []
            while len(round_64) > 0:
                round_32.append( Game(round_64.pop(), round_64.pop()) )

            round_16 = []
            while len(round_32) > 0:
                round_16.append( Game(round_32.pop(), round_32.pop()) )

            round_8 = []
            while len(round_16) > 0:
                round_8.append( Game(round_16.pop(), round_16.pop()) )
            # Winner of round_8 is the Final Four candidate from our region
            return round_8[0]

        west = do_region("west")
        east = do_region("east")
        midwest = do_region("midwest")
        south = do_region("south")

        ff_1 = Game( west, east )
        ff_2 = Game( south, midwest )

        final = Game( ff_1, ff_2 )
        self.root = final

    def play(self, metric, use_max=True):
        game = self.root
        return game.play(metric, use_max)

if __name__=="__main__":

    with open("NCAA-2021.csv", "r") as datafile:
        reader = csv.DictReader(datafile)
        metric = {}
        for row in reader:
            key = row['Team']
            value = float(row['incidence'])
            metric[key] = value

    #metric = {'A': 1, 'B': 2, 'C': 3, 'D': 4}
    #g = Game('A', 'B')
    #print(g.play(metric))
    #
    #g = Game('C', 'D')
    #print(g.play(metric, use_max=False))
    from seeding import seeding

    t = Tournament(seeding)
    t.play(metric, use_max=False)