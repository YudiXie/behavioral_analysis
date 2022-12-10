import json
import numpy as np

from make_dataframe import make_df
from extract import extract_trajectories
import plots
from group_analysis import group_ana, interpolate_tra
from dist_analysis import dist_ana


def plot_all_tra(df):
    # plot trajectories
    for i_video in range(len(df)):
        # load trajectories from files
        json_path = df.loc[i_video, 'tra_dict_path']
        if json_path is not None:
            f = open(json_path)
            tra_dict = json.load(f)

            left_tra = [np.array(tra) for tra in tra_dict['left_tra']]
            right_tra = [np.array(tra) for tra in tra_dict['right_tra']]
            # interpolate trajectories
            num_p = 50
            left_tra_interpld = np.array([interpolate_tra(tra, num_p) for tra in left_tra])
            right_tra_interpld = np.array([interpolate_tra(tra, num_p) for tra in right_tra])

            plots.plot_trajectories(df.loc[i_video, 'exp_name'],
                                    tra_dict['left_tra'],
                                    tra_dict['right_tra'],
                                    df.loc[i_video, 'center_port'],
                                    df.loc[i_video, 'left_port'],
                                    df.loc[i_video, 'right_port'],
                                    left_tra_interpld.mean(axis=0),
                                    right_tra_interpld.mean(axis=0))


if __name__ == '__main__':
    df = make_df()
    # extract_trajectories(df)
    plot_all_tra(df)
    group_ana(df)
    dist_ana(df)
