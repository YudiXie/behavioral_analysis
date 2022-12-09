import json

from make_dataframe import make_df
from extract import extract_trajectories
import plots


if __name__ == '__main__':
    df = make_df()
    # extract_trajectories(df)

    for i_video in range(len(df)):
        # load trajectories from files
        json_path = df.loc[i_video, 'tra_dict_path']
        if json_path is not None:
            f = open(json_path)
            tra_dict = json.load(f)
            plots.plot_trajectories(df.loc[i_video, 'exp_name'],
                                    tra_dict['left_tra'],
                                    tra_dict['right_tra'],
                                    df.loc[i_video, 'center_port'],
                                    df.loc[i_video, 'left_port'],
                                    df.loc[i_video, 'right_port'])
