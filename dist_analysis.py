import os
import json
import numpy as np
from group_analysis import get_tra_dis
import matplotlib.pyplot as plt

from plots import adjust_figure


def dist_ana(df):
    """
    analyze the distance between the trajectories and the optimal trajectories
    """
    for i_video in range(len(df)):
        # extract trajectories from files
        json_path = df.loc[i_video, 'tra_dict_path']
        if json_path is not None:
            f = open(json_path)
            tra_dict = json.load(f)
            all_tra = tra_dict['all_tra']
            all_tra_array = [np.array(tra) for tra in all_tra]
            left_tra = tra_dict['left_tra']
            left_tra_array = [np.array(tra) for tra in left_tra]
            right_tra = tra_dict['right_tra']
            right_tra_array = [np.array(tra) for tra in right_tra]

            # calculate distance from optimal trajectories
            center_port = df.loc[i_video, 'center_port']
            left_port = df.loc[i_video, 'left_port']
            right_port = df.loc[i_video, 'right_port']

            exp_name = df.loc[i_video, 'exp_name']

            left_tra_dis = [get_tra_dis(tra, center_port, left_port) for tra in left_tra_array]
            right_tra_dis = [get_tra_dis(tra, center_port, right_port) for tra in right_tra_array]
            all_dis = left_tra_dis + right_tra_dis
            mean_dis = np.array(all_dis).mean()
            df.loc[i_video, 'avg_tra_dis'] = mean_dis  # log

            plt.figure()
            plt.scatter(np.arange(len(left_tra_dis)), left_tra_dis, label='left tra.')
            plt.scatter(np.arange(len(right_tra_dis)), right_tra_dis, label='right tra.')
            plt.ylabel("Distance from optimal tra. (mm)")
            plt.xlabel("Trial number")
            plt.legend()
            plt.title("Distance from optimal trajectory \n"
                      + exp_name)
            plt.ylim([0, 5])
            adjust_figure()
            plt.savefig(os.path.join('./figures/', exp_name + '_dist.pdf'), transparent=True, bbox_inches="tight")
            plt.close()
