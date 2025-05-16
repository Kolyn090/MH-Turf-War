import os
import csv
import pandas as pd
from game import Game


def get_monsters_concat(db_path):
    return pd.concat(get_monsters_of_games(db_path).values(), axis=0)


def get_monsters_of_games(db_path) -> dict[Game, pd.DataFrame]:
    def get_monster_diff_names(monster_name, all_monster_names) -> list[str]:
        """
        A monster might have more than one name. Here I am referring to things like:
        Alatreon vs. Alatreon (Flight)
        :param monster_name: the monster's name to be searched.
        :param all_monster_names: all possible names across all games, including different names of monsters.
        :return:
        """
        def remove_parenthesis(text):
            return text.split(' (')[0]

        diff_names = []
        for key in all_monster_names:
            if remove_parenthesis(key) == monster_name:
                diff_names.append(key)

        return diff_names

    final_columns = ["monster", "fire_weak", "water_weak", "thunder_weak", "ice_weak", "dragon_weak"]
    result = {}

    for game in list(Game):
        game_name = game.value
        monster_dict = dict()
        # First, look into monster weakness file (because it denotes monsters in different states)
        with open(os.path.join(db_path, f'monster_weak_norm/{game_name}_weak_norm.csv')) as file:
            # monster,fire_weak,water_weak,thunder_weak,ice_weak,dragon_weak
            monsters_weakness = list(csv.reader(file))[1:]
            for monster_weakness in monsters_weakness:
                monster, fire_weak, water_weak, thunder_weak, ice_weak, dragon_weak = monster_weakness
                monster_dict[monster] = {
                    "fire_weak": fire_weak,
                    "water_weak": water_weak,
                    "thunder_weak": thunder_weak,
                    "ice_weak": ice_weak,
                    "dragon_weak": dragon_weak
                }

        # Now get monsters' other attributes
        other_attributes = ["type", "element", "size_pred", "level"]

        for other_attribute in other_attributes:
            with open(os.path.join(db_path, f'monster_{other_attribute}/{game_name}_{other_attribute}.csv')) as file:
                instances = list(csv.reader(file))
                columns = instances[0][1:]  # Exclude 'monster' feature
                final_columns.extend(columns)
                instances = instances[1:]  # Exclude headers

                for instance in instances:
                    monster = instance[0]
                    features = instance[1:]
                    names = get_monster_diff_names(monster, monster_dict.keys())
                    for name in names:
                        for i in range(len(columns)):
                            # This is saying making Alatreon (Flight) to have the same
                            # type, element, size_pred, level as Alatreon.
                            monster_dict[name][columns[i]] = features[i]

        # Convert result
        df = []
        for monster, values in monster_dict.items():
            new_item = {"monster": monster}
            for col in final_columns[1:]:  # Exclude 'monster' feature
                new_item[col] = values[col]
            df.append(new_item)

        result[game] = pd.DataFrame(df)

    return result


if __name__ == '__main__':
    print(get_monsters_concat('../../db'))
