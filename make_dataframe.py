import os
import numpy as np
import pandas as pd

from extract import distance


def get_port_loc(df, name):
    x_array = df.loc[:, (name, 'x')]
    y_array = df.loc[:, (name, 'y')]

    # filter low likelihood points
    ll_array = df.loc[:, (name, 'likelihood')]
    filter_idx = ll_array < 0.98
    x_array.loc[filter_idx] = np.nan
    y_array.loc[filter_idx] = np.nan

    # filter outliers for port positions

    return x_array.mean(), y_array.mean()


def make_df():
    data_frame = pd.DataFrame(
        {
            "mouse_name": ['rim10', 'rim10', 'rim106', 'rim106',
                           'rim123', 'rim123', 'rim138', 'rim138',
                           'rim139', 'rim139', 'rim145', 'rim145',
                           'rim12', 'rim12', 'rim108', 'rim108',
                           'rim124', 'rim124', 'rim136', 'rim136',
                           'rim137', 'rim137', 'rim141', 'rim141'],
            "genotype": ['control', 'control', 'control', 'control',
                         'control', 'control', 'control', 'control',
                         'control', 'control', 'control', 'control',
                         'RIMcKO', 'RIMcKO', 'RIMcKO', 'RIMcKO',
                         'RIMcKO', 'RIMcKO', 'RIMcKO', 'RIMcKO',
                         'RIMcKO', 'RIMcKO', 'RIMcKO', 'RIMcKO'],
            "session": ['TwoOdor-1', 'TwoOdor-2', 'TwoOdor-1', 'TwoOdor-2',
                        'TwoOdor-1', 'TwoOdor-2', 'TwoOdor-1', 'TwoOdor-2',
                        'TwoOdor-1', 'TwoOdor-2', 'TwoOdor-1', 'TwoOdor-2',
                        'TwoOdor-1', 'TwoOdor-2', 'TwoOdor-1', 'TwoOdor-2',
                        'TwoOdor-1', 'TwoOdor-2', 'TwoOdor-1', 'TwoOdor-2',
                        'TwoOdor-1', 'TwoOdor-2', 'TwoOdor-1', 'TwoOdor-2'],
            "csv_path": ['rim10_2019-12-02-085240-0000DLC_resnet50_RIMdataSep11shuffle1_500000.csv',
                         'rim10_2019-12-03-083501-0000DLC_resnet50_RIMdataSep11shuffle1_500000.csv',
                         'rim106_2019-12-09-085330-0000DLC_resnet50_RIMdataSep11shuffle1_500000.csv',
                         'rim106_2019-12-10-082017-0000DLC_resnet50_RIMdataSep11shuffle1_500000.csv',
                         'rim123_2019-11-30-082443-0000DLC_resnet50_RIMdataSep11shuffle1_500000.csv',
                         'rim123_2019-12-01-082615-0000DLC_resnet50_RIMdataSep11shuffle1_500000.csv',
                         'rim138_2019-11-29-094734-0000DLC_resnet50_RIMdataSep11shuffle1_500000.csv',
                         'rim138_2019-11-30-092231-0000DLC_resnet50_RIMdataSep11shuffle1_500000.csv',
                         'rim139_2019-11-28-115422-0000DLC_resnet50_RIMdataSep11shuffle1_500000.csv',
                         'rim139_2019-11-29-113907-0000DLC_resnet50_RIMdataSep11shuffle1_500000.csv',
                         'rim145_2019-11-28-115441-0000DLC_resnet50_RIMdataSep11shuffle1_500000.csv',
                         'rim145_2019-11-29-113923-0000DLC_resnet50_RIMdataSep11shuffle1_500000.csv',
                         'rim12_2019-12-09-100215-0000DLC_resnet50_RIMdataSep11shuffle1_500000.csv',
                         None,
                         'rim108_2019-12-11-094329-0000DLC_resnet50_RIMdataSep11shuffle1_500000.csv',
                         'rim108_2019-12-12-094016-0000DLC_resnet50_RIMdataSep11shuffle1_500000.csv',
                         'rim124_2019-12-10-095942-0000DLC_resnet50_RIMdataSep11shuffle1_500000.csv',
                         None,
                         'rim136_2019-11-28-103604-0000DLC_resnet50_RIMdataSep11shuffle1_500000.csv',
                         'rim136_2019-11-29-103936-0000DLC_resnet50_RIMdataSep11shuffle1_500000.csv',
                         'rim137_2019-12-10-113052-0000DLC_resnet50_RIMdataSep11shuffle1_500000.csv',
                         None,
                         'rim141_2019-12-23-104658-0000DLC_resnet50_RIMdataSep11shuffle1_500000.csv',
                         'rim141_2019-12-24-102330-0000DLC_resnet50_RIMdataSep11shuffle1_500000.csv'],
            "exp_name": None,
            "center_port": None,
            "left_port": None,
            "right_port": None,
            "tra_dict_path": None,
        }
    )

    for i_video in range(len(data_frame)):
        # load data
        exp = data_frame.loc[i_video, 'mouse_name'] \
              + data_frame.loc[i_video, 'genotype'] \
              + data_frame.loc[i_video, 'session']
        data_frame.loc[i_video, 'exp_name'] = exp

        csv_name = data_frame.loc[i_video, 'csv_path']
        if csv_name is not None:

            # set tra_dict_path
            tra_dict_path = exp + "tra_dict.json"
            full_tra_dict_path = os.path.join('./', 'data', 'extracted_trajectories', tra_dict_path)
            data_frame.loc[i_video, 'tra_dict_path'] = full_tra_dict_path

            # set location of ports
            filename = os.path.join('./data/TwoOdor', csv_name)
            data = pd.read_csv(filename, header=[1, 2], index_col=0)

            centerport_x, centerport_y = get_port_loc(data, 'centerport')
            leftport_x, leftport_y = get_port_loc(data, 'leftport')
            rightport_x, rightport_y = get_port_loc(data, 'rightport')

            print(f'center to left distance (pixels): ',
                  distance(centerport_x, centerport_y, leftport_x, leftport_y))
            print(f'center to right distance (pixels): ',
                  distance(centerport_x, centerport_y, rightport_x, rightport_y))

            data_frame.loc[i_video, 'center_port'] = (centerport_x, centerport_y)
            data_frame.loc[i_video, 'left_port'] = (leftport_x, leftport_y)
            data_frame.loc[i_video, 'right_port'] = (rightport_x, rightport_y)

    return data_frame


