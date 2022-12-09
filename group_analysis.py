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


def get_tra_dis2line(trajectory, p1, p2):
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
            all_tra = [np.array(tra) for tra in tra_dict['all_tra']]
            left_tra = [np.array(tra) for tra in tra_dict['left_tra']]
            right_tra = [np.array(tra) for tra in tra_dict['right_tra']]

            # interpolate trajectories and calculate distance to averaged trajectory
            num_p = 10
            left_tra_interpld = np.array([interpolate_tra(tra, num_p) for tra in left_tra])
            left_diff2avg_square = (left_tra_interpld - left_tra_interpld.mean(axis=0)) ** 2
            left_dist2avg = np.sqrt(left_diff2avg_square[:, :, 0] + left_diff2avg_square[:, :, 1])

            right_tra_interpld = np.array([interpolate_tra(tra, num_p) for tra in right_tra])
            right_diff2avg_square = (right_tra_interpld - right_tra_interpld.mean(axis=0)) ** 2
            right_dist2avg = np.sqrt(right_diff2avg_square[:, :, 0] + right_diff2avg_square[:, :, 1])

            dist2avg = np.concatenate((left_dist2avg, right_dist2avg), axis=0)
            dist2avg = (dist2avg / pixel_per_m) * 1000  # convert to mm
            # calculate the distances to average trajectory of each trajectory, and take mean
            df.loc[i_video, 'avg_tra_dis2avgtra'] = dist2avg.mean(axis=1).mean()  # log
            # calculate the distances to average trajectory of each trajectory, and take std
            df.loc[i_video, 'std_tra_dis2avgtra'] = dist2avg.mean(axis=1).std()  # log

            # calculate distance between trajectories and a straight line
            center_port = df.loc[i_video, 'center_port']
            left_port = df.loc[i_video, 'left_port']
            right_port = df.loc[i_video, 'right_port']
            left_tra_dis = [get_tra_dis2line(tra, center_port, left_port) for tra in left_tra]
            right_tra_dis = [get_tra_dis2line(tra, center_port, right_port) for tra in right_tra]
            all_dis = left_tra_dis + right_tra_dis
            mean_dis = np.array(all_dis).mean()
            df.loc[i_video, 'avg_tra_dis2line'] = mean_dis  # log

            # calculate average velocity
            tra_vel = [get_tra_avg_speed(tra) for tra in all_tra]
            mean_velocity = np.array(tra_vel).mean()
            df.loc[i_video, 'avg_tra_vel'] = mean_velocity  # log

            # number of trajectories
            num_tra = len(all_tra)
            df.loc[i_video, 'num_tra'] = num_tra  # log

    # plot the results
    read_label_list = ['avg_tra_vel',
                       'num_tra',
                       'avg_tra_dis2line',
                       'avg_tra_dis2avgtra',
                       'std_tra_dis2avgtra']
    title_list = ['Averaged head speed',
                  'Number of trajectories',
                  'Averaged distance from \nline',
                  'Averaged distance from \naveraged trajectory',
                  'Std of distance from \naveraged trajectory']
    ylabel_list = ['Averaged Velocity (m/s)',
                   'Number of trajectories',
                   'Distance from line (mm)',
                   'Distance from avg. tra. (mm)',
                   'Std of distance from avg. tra (mm)']
    save_str_list = ['headspeed',
                     'num_tra',
                     'dis2line',
                     'dis2avgtra',
                     'std_dis2avgtra']

    for read_label, title, ylabel, save_str in zip(read_label_list, title_list, ylabel_list, save_str_list):
        control_data = df[df['genotype'] == 'control'].loc[:, read_label]
        rimKO_data = df[df['genotype'] == 'RIMcKO'].loc[:, read_label]
        two_set_scatter_plot(control_data, rimKO_data,
                             labels=["RIM Control", 'RIM cKO$^{DA}$'],
                             title_str=title+", first 2 sessions",
                             ylabel=ylabel,
                             save_str=save_str+'_session12')

        control_s1_data = df[(df['genotype'] == 'control') & (df['session'] == 'TwoOdor-1')].loc[:, read_label]
        rimKO_s1_data = df[(df['genotype'] == 'RIMcKO') & (df['session'] == 'TwoOdor-1')].loc[:, read_label]
        two_set_scatter_plot(control_s1_data, rimKO_s1_data,
                             labels=["RIM Control", 'RIM cKO$^{DA}$'],
                             title_str=title+", session 1",
                             ylabel=ylabel,
                             save_str=save_str+'_session1')

        control_s2_data = df[(df['genotype'] == 'control') & (df['session'] == 'TwoOdor-2')].loc[:, read_label]
        rimKO_s2_data = df[(df['genotype'] == 'RIMcKO') & (df['session'] == 'TwoOdor-2')].loc[:, read_label]
        two_set_scatter_plot(control_s2_data, rimKO_s2_data,
                             labels=["RIM Control", 'RIM cKO$^{DA}$'],
                             title_str=title+", session 2",
                             ylabel=ylabel,
                             save_str=save_str+'_session2')
