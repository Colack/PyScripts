#!/usr/bin/env python3

import os
import json
import argparse
from termcolor import colored
from halo import Halo

FAVS_FOLDER = "favs"

def load_favorites():
    favorites = {}
    if not os.path.exists(FAVS_FOLDER):
        os.makedirs(FAVS_FOLDER)
    for filename in os.listdir(FAVS_FOLDER):
        if filename.endswith(".json"):
            genre = filename.split('.')[0]
            filepath = os.path.join(FAVS_FOLDER, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                favorites[genre] = data['favorites']
    return favorites

def display_favorites():
    favorites = load_favorites()
    if not favorites:
        print(colored("No favorite games found. Add some first!", "red"))
        return
    for genre, games in favorites.items():
        print(colored(f"\nGenre: {genre.capitalize()}", "green"))
        for game in games:
            print(colored(f"  - {game}", "cyan"))

def add_favorite_game(genre, game):
    filepath = os.path.join(FAVS_FOLDER, f"{genre}.json")
    spinner = Halo(text='Loading favorites', spinner='dots')
    spinner.start()
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            data = json.load(file)
    else:
        data = {"genre": genre.capitalize(), "favorites": []}

    if game not in data['favorites']:
        data['favorites'].append(game)
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
        spinner.succeed(colored(f"Added {game} to {genre.capitalize()} favorites.", "green"))
    else:
        spinner.fail(colored(f"{game} is already in {genre.capitalize()} favorites.", "red"))

def remove_favorite_game(genre, game):
    filepath = os.path.join(FAVS_FOLDER, f"{genre}.json")
    spinner = Halo(text='Loading favorites', spinner='dots')
    spinner.start()
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            data = json.load(file)
        
        if game in data['favorites']:
            data['favorites'].remove(game)
            with open(filepath, 'w') as file:
                json.dump(data, file, indent=4)
            spinner.succeed(colored(f"Removed {game} from {genre.capitalize()} favorites.", "green"))
        else:
            spinner.fail(colored(f"{game} not found in {genre.capitalize()} favorites.", "red"))
    else:
        spinner.fail(colored(f"No favorites found for genre {genre.capitalize()}.", "red"))

def clear_favorites():
    if os.path.exists(FAVS_FOLDER):
        for filename in os.listdir(FAVS_FOLDER):
            file_path = os.path.join(FAVS_FOLDER, filename)
            os.remove(file_path)
        print(colored("All favorite games cleared.", "yellow"))
    else:
        print(colored("No favorites to clear.", "red"))

def main():
    parser = argparse.ArgumentParser(description="Favorite Games Manager", add_help=False)
    parser.add_argument('--display', action='store_true', help="Display all favorite games")
    parser.add_argument('--add', nargs=2, metavar=('GENRE', 'GAME'), help="Add a game to a genre")
    parser.add_argument('--remove', nargs=2, metavar=('GENRE', 'GAME'), help="Remove a game from a genre")
    parser.add_argument('--clear', action='store_true', help="Clear all favorite games")
    parser.add_argument('--version', action='version', version='Favorite Games Manager 1.0')
    parser.add_argument('--help', action='store_true', help="Show this help message and exit")
    args = parser.parse_args()

    if args.help or not any(vars(args).values()):
        parser.print_help()
    elif args.display:
        display_favorites()
    elif args.add:
        genre, game = args.add
        add_favorite_game(genre.lower(), game)
    elif args.remove:
        genre, game = args.remove
        remove_favorite_game(genre.lower(), game)
    elif args.clear:
        clear_favorites()

if __name__ == "__main__":
    main()
