import os
import pandas as pd
from game import Game


def get_mon_weak_norm_concat(db_path):
    return pd.concat(get_mon_weak_norm_of_games(db_path).values(), axis=0)


def get_mon_weak_norm_of_games(db_path) -> dict[Game, pd.DataFrame]:
    def normalize_within_rows(df, features_to_normalize, min_val=0):
        df_normalized = df.copy()
        
        # Select only the columns to normalize
        features_df = df_normalized[features_to_normalize]
        
        # Min-max normalization: (x - min) / (max - min)
        row_min = min_val
        row_max = features_df.max(axis=1)
        df_normalized[features_to_normalize] = features_df.sub(row_min, axis=0).div(row_max - row_min, axis=0)
            
        # Replace NaN values with 0 (occurs when std=0 or max=min)
        df_normalized[features_to_normalize] = df_normalized[features_to_normalize].fillna(0)
        
        return df_normalized

    def normalize_columns(df, features_to_normalize):
        df_normalized = df.copy()
        
        # Min-max normalization: (x - min) / (max - min)
        for feature in features_to_normalize:
            col_min = df[feature].min()
            col_max = df[feature].max()
            df_normalized[feature] = (df[feature] - col_min) / (col_max - col_min)

        # Replace NaN values with 0 (occurs when std=0 or max=min)
        df_normalized[features_to_normalize] = df_normalized[features_to_normalize].fillna(0)
        
        return df_normalized
    
    def multiply_dataframes(df1, df2, features_to_multiply):
        # Verify DataFrames have same shape
        if df1.shape != df2.shape:
            raise ValueError("DataFrames must have the same dimensions")
        
        # Verify specified columns exist in both DataFrames
        for col in features_to_multiply:
            if col not in df1.columns or col not in df2.columns:
                raise ValueError(f"Column '{col}' not found in both DataFrames")
        
        # Create a copy of df1 to store results
        result_df = df1.copy()
        
        # Multiply specified features
        for col in features_to_multiply:
            result_df[col] = df1[col] * df2[col]
        
        return result_df
    
    def normalize_combined(df, features_to_normalize):
        normalized_by_rows = normalize_within_rows(df, features_to_normalize)
        normalized_by_columns = normalize_columns(df, features_to_normalize)
        return multiply_dataframes(normalized_by_rows, normalized_by_columns, features_to_normalize)

    features_to_normalize = ['fire_weak', 'water_weak', 'thunder_weak', 'ice_weak', 'dragon_weak']
    result = {}

    for game in list(Game):
        game_name = game.value
        df = pd.read_csv(os.path.join(db_path, f'monster_weak/{game_name}_weak.csv'))
        normalized_df = normalize_combined(df, features_to_normalize).round(2)
        result[game] = normalized_df
    
    return result


if __name__ == '__main__':
    print(get_mon_weak_norm_concat('../../db/'))
