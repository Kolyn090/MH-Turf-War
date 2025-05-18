import os
import csv
import pandas as pd
from game import Game


def get_monster_fights_df(db_path) -> pd.DataFrame:
    """
    Join monsters data with fights data
    :return:
    """

    def has_parenthesis(monster_name):
        return ' (' in monster_name

    def remove_parenthesis(monster_name):
        return monster_name.split(' (')[0]

    def find_same_monster(monster_name, same_monsters_dict) -> list:
        same_monsters = []
        for key, value in same_monsters_dict.items():
            if value == monster_name:
                same_monsters.append(key)
        return same_monsters

    # Search for all monsters across games
    monsters_columns = None
    monsters = []
    for game in list(Game):
        game_name = game.value
        with open(os.path.join(db_path, f'monster/{game_name}.csv')) as file:
            content = list(csv.reader(file))
            if monsters_columns is None:
                monsters_columns = content[0]
            content = content[1:]
            monsters.extend(content)

    # Make a dict to recognize a monster that is in a different state:
    # E.g. Alatreon (Flight)
    same_monsters_dict = dict()
    for monster in monsters:
        name = monster[0]
        if has_parenthesis(name):
            same_monsters_dict[name] = remove_parenthesis(name)

    fights = pd.read_csv(os.path.join(db_path, 'fights.csv')).values.tolist()
    monsters_columns_initiator = ['I_' + mc for mc in monsters_columns]
    monsters_columns_opponent = ['O_' + mc for mc in monsters_columns]
    csv_columns = []
    csv_columns.extend(monsters_columns_initiator[1:])
    csv_columns.extend(monsters_columns_opponent[1:])
    csv_columns.append("Outcome")

    monster_dict = {monster[0]: monster[1:] for monster in monsters}

    result = []
    for fight in fights:
        initiator, opponent, outcome = fight
        initiator_data = []
        opponent_data = []

        # Both monsters are in their original state
        if initiator in monster_dict and opponent in monster_dict:
            initiator_data = monster_dict[initiator]
            opponent_data = monster_dict[opponent]
            row_data = []
            row_data.extend(initiator_data)
            row_data.extend(opponent_data)
            row = {column: data for data, column in zip(row_data, csv_columns[:-1])}
            row["Outcome"] = outcome
            result.append(row)
        else:  # At least one is not in original state
            same_initiators = [initiator]
            same_opponents = [opponent]
            if initiator not in monster_dict:
                same_initiators = find_same_monster(initiator, same_monsters_dict)
            if opponent not in monster_dict:
                same_opponents = find_same_monster(opponent, same_monsters_dict)
            battles = []
            for same_initiator in same_initiators:
                for same_opponent in same_opponents:
                    battles.append((same_initiator, same_opponent))

            for battle in battles:
                initiator_data = monster_dict[battle[0]]
                opponent_data = monster_dict[battle[1]]
                row_data = []
                row_data.extend(initiator_data)
                row_data.extend(opponent_data)
                row = {column: data for data, column in zip(row_data, csv_columns[:-1])}
                row["Outcome"] = outcome
                result.append(row)
    return pd.DataFrame(result)


if __name__ == '__main__':
    print(get_monster_fights_df('../../db'))
