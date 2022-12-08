from make_dataframe import make_df
from extract import extract_trajectories


if __name__ == '__main__':
    df = make_df()
    extract_trajectories(df)
    print(df)

