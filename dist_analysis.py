import os
import json
import numpy as np
from group_analysis import interpolate_tra, pixel_per_m
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
            exp_name = df.loc[i_video, 'exp_name']
            f = open(json_path)
            tra_dict = json.load(f)
            left_tra = [np.array(tra) for tra in tra_dict['left_tra']]
            right_tra = [np.array(tra) for tra in tra_dict['right_tra']]

            # interpolate trajectories and calculate distance to averaged trajectory
            num_p = 11
            left_tra_interpld = np.array([interpolate_tra(tra, num_p) for tra in left_tra])
            left_diff2avg_square = (left_tra_interpld - left_tra_interpld.mean(axis=0)) ** 2
            left_dist2avg = np.sqrt(left_diff2avg_square[:, :, 0] + left_diff2avg_square[:, :, 1])

            right_tra_interpld = np.array([interpolate_tra(tra, num_p) for tra in right_tra])
            right_diff2avg_square = (right_tra_interpld - right_tra_interpld.mean(axis=0)) ** 2
            right_dist2avg = np.sqrt(right_diff2avg_square[:, :, 0] + right_diff2avg_square[:, :, 1])

            left_dist2avg = (left_dist2avg / pixel_per_m) * 1000  # convert to mm
            right_dist2avg = (right_dist2avg / pixel_per_m) * 1000  # convert to mm
            left_tra_dis = left_dist2avg.mean(axis=1)
            right_tra_dis = right_dist2avg.mean(axis=1)

            plt.figure()
            plt.scatter(np.arange(len(left_tra_dis)), left_tra_dis, label='left tra.')
            plt.scatter(np.arange(len(right_tra_dis)), right_tra_dis, label='right tra.')
            plt.ylabel("Distance from avg. tra. (mm)")
            plt.xlabel("Trial number")
            plt.legend()
            plt.title("Distance from averaged trajectory \n"
                      + exp_name)
            plt.ylim([0, 5])
            adjust_figure()
            plt.savefig(os.path.join('./figures/', exp_name + '_dist.pdf'), transparent=True, bbox_inches="tight")
            plt.close()
