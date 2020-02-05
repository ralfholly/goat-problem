#! /usr/bin/env python3

# Goat problem (Monty-Hall problem) simulator.
#
# Why does it make sense to pick another door?
#
# 1. If you switch but initially picked a goat, you'll win.
# 2. If you switch but initially picked a car, you'll lose.
# 3. It's twice as likely to initially pick a goat.
# => It's twice as likely to win when you switch!
#

import random
import sys
import re
import enum

class Choice(enum.Enum):
    goat = 100
    car = 200

def new_game():
    game = [Choice.goat for _ in range(0, 3)]
    game[random.randint(0, len(game) - 1)] = Choice.car
    return game

def disclose_goat(game, choice_index):
    for i, _ in enumerate(game):
        if game[i] == Choice.goat and i != choice_index:
            return i
    return None

def pick_alternative(game, choice_index, goat_index):
    all_indices = range(len(game))
    remaining_alternatives = (set(all_indices) - set([choice_index, goat_index]))
    return random.choice(list(remaining_alternatives))

def run(games_to_play_count):
    games_won_stay = 0
    games_won_change = 0

    for i in range(games_to_play_count):
        game = new_game()
        # Our inital pick.
        choice_index = random.randint(0, len(game) - 1)

        # In case we stick with original choice.
        if game[choice_index] == Choice.car:
            games_won_stay += 1

        # In case we change our mind.
        goat_index = disclose_goat(game, choice_index)
        alternative_index = pick_alternative(game, choice_index, goat_index)

        if game[alternative_index] == Choice.car:
            games_won_change += 1

        games_played = i + 1

        print("\rgames played:%5d, games won (stayed): %.2f%%, games won (switched):%1.2f%%" % \
            (games_played, 100.0 * games_won_stay / games_played, 100.0 * games_won_change / games_played), end="")

    print()

if __name__ == '__main__':
    if len(sys.argv) != 2 or not re.match(r"\d+$", sys.argv[1]):
        print("Usage: %s <number of games to play>" % sys.argv[0])
        sys.exit(1)
    run(int(sys.argv[1]))
