import json
import numpy as np

from plots import two_set_scatter_plot

pixel_per_m = 325 / 0.320
fps = 84


def interpolate_tra(trajectory, num_points=10):
    """
    interpolate the trajectories to the same length by linear method
    :param trajectory: the first two cols of trajectory is x and y positions in pixels
    :param num_points: number of points to interpolate
    :return: interpolated trajectory, size (num_points, 2)
    """
    time = np.linspace(0.0, 1.0, len(trajectory))
    new_time = np.linspace(0.0, 1.0, num_points)

    x = np.interp(new_time, time, trajectory[:, 0])
    y = np.interp(new_time, time, trajectory[:, 1])

    return np.stack((x, y), axis=1)


def get_tra_avg_speed(trajectory):
    """
    get the averaged velocity of a single trajectory
    :param trajectory: the first two cols of trajectory is x and y positions in pixels
    :return: mean_vel: averaged velocity of trajectory, in m/s
    """
    squared_vel = np.diff(trajectory, axis=0)**2
    mean_vel = (np.sqrt(squared_vel[:, 0] + squared_vel[:, 1]).mean() * fps) / pixel_per_m
    return mean_vel


def get_tra_dis(trajectory, p1, p2):
    """
    get the averaged distance of the trajectory from the line defined by p1 and p2
    :param trajectory: the first two cols of trajectory is x and y positions in pixels
    :param p1: tuple, coordinate of point 1
    :param p2: tuple, coordinate of point 2
    :return: mean_dis, in mm
    """
    x1, y1 = p1
    x2, y2 = p2
    distance = np.abs((x2 - x1) * (y1 - trajectory[:, 1]) -
                      (x1 - trajectory[:, 0]) * (y2 - y1)) / np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    mean_dis = (distance.mean() / pixel_per_m) * 1000
    return mean_dis


def group_ana(df):
    # calculate various measures for each trajectory
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

            left_tra_dis = [get_tra_dis(tra, center_port, left_port) for tra in left_tra_array]
            right_tra_dis = [get_tra_dis(tra, center_port, right_port) for tra in right_tra_array]
            all_dis = left_tra_dis + right_tra_dis
            mean_dis = np.array(all_dis).mean()
            df.loc[i_video, 'avg_tra_dis'] = mean_dis  # log

            # calculate average velocity
            tra_vel = [get_tra_avg_speed(tra) for tra in all_tra_array]
            mean_velocity = np.array(tra_vel).mean()
            df.loc[i_video, 'avg_tra_vel'] = mean_velocity  # log

            # number of trajectories
            num_tra = len(all_tra_array)
            df.loc[i_video, 'num_tra'] = num_tra  # log

    # different plots
    control_vel = df[df['genotype'] == 'control'].loc[:, 'avg_tra_vel']
    rimKO_vel = df[df['genotype'] == 'RIMcKO'].loc[:, 'avg_tra_vel']
    two_set_scatter_plot(control_vel, rimKO_vel,
                         labels=["RIM Control", 'RIM cKO$^{DA}$'],
                         title_str="Averaged head speed, first 2 sessions",
                         ylabel='Averaged Velocity (m/s)',
                         save_str='headspeed_session12')

    control_vel_s1 = df[(df['genotype'] == 'control') & (df['session'] == 'TwoOdor-1')].loc[:, 'avg_tra_vel']
    rimKO_vel_s1 = df[(df['genotype'] == 'RIMcKO') & (df['session'] == 'TwoOdor-1')].loc[:, 'avg_tra_vel']
    two_set_scatter_plot(control_vel_s1, rimKO_vel_s1,
                         labels=["RIM Control", 'RIM cKO$^{DA}$'],
                         title_str="Averaged head speed, session 1",
                         ylabel='Averaged Velocity (m/s)',
                         save_str='headspeedsession1')

    control_vel_s2 = df[(df['genotype'] == 'control') & (df['session'] == 'TwoOdor-2')].loc[:, 'avg_tra_vel']
    rimKO_vel_s2 = df[(df['genotype'] == 'RIMcKO') & (df['session'] == 'TwoOdor-2')].loc[:, 'avg_tra_vel']
    two_set_scatter_plot(control_vel_s2, rimKO_vel_s2,
                         labels=["RIM Control", 'RIM cKO$^{DA}$'],
                         title_str="Averaged head speed, session 2",
                         ylabel='Averaged Velocity (m/s)',
                         save_str='headspeedsession2')

    control_vel = df[df['genotype'] == 'control'].loc[:, 'num_tra']
    rimKO_vel = df[df['genotype'] == 'RIMcKO'].loc[:, 'num_tra']
    two_set_scatter_plot(control_vel, rimKO_vel,
                         labels=["RIM Control", 'RIM cKO$^{DA}$'],
                         title_str="Number of trajectories, first 2 sessions",
                         ylabel='Number of trajectories',
                         save_str='num_tra_session12')

    control_vel_s1 = df[(df['genotype'] == 'control') & (df['session'] == 'TwoOdor-1')].loc[:, 'num_tra']
    rimKO_vel_s1 = df[(df['genotype'] == 'RIMcKO') & (df['session'] == 'TwoOdor-1')].loc[:, 'num_tra']
    two_set_scatter_plot(control_vel_s1, rimKO_vel_s1,
                         labels=["RIM Control", 'RIM cKO$^{DA}$'],
                         title_str="Number of trajectories, session 1",
                         ylabel='Number of trajectories',
                         save_str='num_tra_session1')

    control_vel_s1 = df[(df['genotype'] == 'control') & (df['session'] == 'TwoOdor-2')].loc[:, 'num_tra']
    rimKO_vel_s1 = df[(df['genotype'] == 'RIMcKO') & (df['session'] == 'TwoOdor-2')].loc[:, 'num_tra']
    two_set_scatter_plot(control_vel_s1, rimKO_vel_s1,
                         labels=["RIM Control", 'RIM cKO$^{DA}$'],
                         title_str="Number of trajectories, session 2",
                         ylabel='Number of trajectories',
                         save_str='num_tra_session2')

    control_dis = df[df['genotype'] == 'control'].loc[:, 'avg_tra_dis']
    rimKO_dis = df[df['genotype'] == 'RIMcKO'].loc[:, 'avg_tra_dis']
    two_set_scatter_plot(control_dis, rimKO_dis,
                         labels=["RIM Control", 'RIM cKO$^{DA}$'],
                         title_str="Averaged distance from \n"
                                   "optimal trajectory, first 2 sessions",
                         ylabel='Distance from optimal tra. (mm)',
                         save_str='distance_session12')

    control_dis_s1 = df[(df['genotype'] == 'control') & (df['session'] == 'TwoOdor-1')].loc[:, 'avg_tra_dis']
    rimKO_dis_s1 = df[(df['genotype'] == 'RIMcKO') & (df['session'] == 'TwoOdor-1')].loc[:, 'avg_tra_dis']
    two_set_scatter_plot(control_dis_s1, rimKO_dis_s1,
                         labels=["RIM Control", 'RIM cKO$^{DA}$'],
                         title_str="Averaged distance from \n"
                                   "optimal trajectory, session 1",
                         ylabel='Distance from optimal tra. (mm)',
                         save_str='distance_session1')

    control_dis_s1 = df[(df['genotype'] == 'control') & (df['session'] == 'TwoOdor-2')].loc[:, 'avg_tra_dis']
    rimKO_dis_s1 = df[(df['genotype'] == 'RIMcKO') & (df['session'] == 'TwoOdor-2')].loc[:, 'avg_tra_dis']
    two_set_scatter_plot(control_dis_s1, rimKO_dis_s1,
                         labels=["RIM Control", 'RIM cKO$^{DA}$'],
                         title_str="Averaged distance from \n"
                                   "optimal trajectory, session 2",
                         ylabel='Distance from optimal tra. (mm)',
                         save_str='distance_session2')
