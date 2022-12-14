import os
import numpy as np
import pandas as pd
import json


def distance(x1, y1, x2, y2):
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)


def extract_trajectories(data_frame):
    """
    extract trajectories from the set of data specified in data_frame
    and save them in a json file
    """
    if not os.path.exists('./data/extracted_trajectories'):
        os.makedirs('./data/extracted_trajectories')

    for i_video in range(len(data_frame)):
        # load data
        print("Analyzing: ", data_frame.loc[i_video, 'exp_name'])
        csv_name = data_frame.loc[i_video, 'csv_path']

        if csv_name is not None:
            filename = os.path.join('./data/TwoOdor', csv_name)
            data = pd.read_csv(filename, header=[1, 2], index_col=0)

            centerport_x, centerport_y = data_frame.loc[i_video, 'center_port']
            leftport_x, leftport_y = data_frame.loc[i_video, 'left_port']
            rightport_x, rightport_y = data_frame.loc[i_video, 'right_port']

            # extract trajectories
            nose_x = data.loc[:, ('nose', 'x')]
            nose_y = data.loc[:, ('nose', 'y')]

            threshold = 5  # pixels, cutoff distance for port entry

            in_center_count = 0
            left_center = False
            record = False
            max_tra_len = 4 # in seconds
            fps = 84
            tra = []

            tra_list = []
            left_tra_list = []
            right_tra_list = []
            for i in range(len(nose_x)):
                in_center = distance(nose_x[i], nose_y[i], centerport_x, centerport_y) < threshold
                if in_center:
                    # count to 5
                    in_center_count += 1
                else:
                    in_center_count = 0

                # need to in center consecutively 5 frames to trigger recording
                if in_center_count >= 5:
                    record = True

                if record:
                    if not in_center:
                        left_center = True

                    if left_center:
                        # record nose positions, and frame index
                        tra.append((nose_x[i], nose_y[i], i))

                        in_left = distance(nose_x[i], nose_y[i], leftport_x, leftport_y) < threshold
                        in_right = distance(nose_x[i], nose_y[i], rightport_x, rightport_y) < threshold

                        assert (in_center and (in_left or in_right)) == False, 'not possible position'
                        # if first left center and then in center again
                        if in_center:
                            record = False
                            tra = []
                            left_center = False
                        elif in_left or in_right:
                            record = False
                            if len(tra) <= max_tra_len * fps:
                                if in_left:
                                    left_tra_list.append(tra)
                                    tra_list.append(tra)
                                elif in_right:
                                    right_tra_list.append(tra)
                                    tra_list.append(tra)
                                else:
                                    raise RuntimeError
                            tra = []
                            left_center = False
                        else:
                            pass

            print(f'number of trajectories: {len(tra_list)}')

            # save a list of trajectories
            tra_dict = {
                'left_tra': left_tra_list,
                'right_tra': right_tra_list,
                'all_tra': tra_list,
            }

            json_file = json.dumps(tra_dict)
            f = open(data_frame.loc[i_video, 'tra_dict_path'], "w")  # open file for writing, "w"
            f.write(json_file)  # write json object to file
            f.close()  # close file
