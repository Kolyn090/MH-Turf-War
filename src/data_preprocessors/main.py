import os
from mon_weak_norm import get_mon_weak_norm_of_games
from monsters import get_monsters_of_games
from monster_fights import get_monster_fights_df
from mon_size_pred import get_mon_size_pred_of_games, get_mon_size_pred_concat, get_size_concat
from game import Game


"""
Run this script after you have modified anything in db folder.
"""


def main(db_path):
    # Step 1: Make monster weakness data normalized within its own game
    mon_weak_norm_of_games = get_mon_weak_norm_of_games(db_path)
    weak_norm_path = os.path.join(db_path, 'monster_weak_norm')
    os.makedirs(weak_norm_path, exist_ok=True)
    for game in list(Game):
        game_name = game.value
        mon_weak_norm_df = mon_weak_norm_of_games[game]
        mon_weak_norm_df.to_csv(os.path.join(weak_norm_path, f'{game_name}_weak_norm.csv'), index=False)

    # Step 2: Predict, combine monster size
    size_concat = get_size_concat(db_path)
    mon_size_pred_of_games = get_mon_size_pred_of_games(db_path)
    mon_size_pred_concat = get_mon_size_pred_concat(db_path)
    monster_size_pred_path = os.path.join(db_path, 'monster_size_pred')
    os.makedirs(monster_size_pred_path, exist_ok=True)
    for game in list(Game):
        game_name = game.value
        mon_size_pred_df = mon_size_pred_of_games[game]
        mon_size_pred_df.to_csv(os.path.join(monster_size_pred_path, f'{game_name}_size_pred.csv'), index=False)
    size_concat.to_csv(os.path.join(db_path, 'monster_size/size_concat.csv'), index=False)
    mon_size_pred_concat.to_csv(os.path.join(monster_size_pred_path, 'size_pred_concat.csv'), index=False)

    # Step 3: Join monster data according to its game version
    monsters_of_games = get_monsters_of_games(db_path)
    monster_path = os.path.join(db_path, 'monster')
    for game in list(Game):
        game_name = game.value
        monsters_df = monsters_of_games[game]
        monsters_df.to_csv(os.path.join(monster_path, f'{game_name}.csv'), index=False)

    # Step 4: Join monster fights data (monster + fights)
    monster_fights = get_monster_fights_df(db_path)
    monster_fights.to_csv(os.path.join(db_path, 'monster_fights.csv'), index=False)


if __name__ == '__main__':
    db_path = '../../db'
    main(db_path)
