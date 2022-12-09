import os
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 14})


def adjust_figure():
    ax = plt.gca()
    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    # Only show ticks on the left and bottom spines
    # ax.yaxis.set_ticks_position('left')
    # ax.xaxis.set_ticks_position('bottom')
    plt.tight_layout(pad=0.5)


def plot_trajectories(exp_name,
                      left_tra_list, right_tra_list,
                      centerport_pos,
                      leftport_pos,
                      rightport_pos):
    """
    Plot trajectories in a single video
    """
    centerport_x, centerport_y = centerport_pos
    leftport_x, leftport_y = leftport_pos
    rightport_x, rightport_y = rightport_pos

    plt.figure()
    # plot multiple tra
    for tra in left_tra_list:
        tra_zip = list(zip(*tra))
        plt.plot(tra_zip[0], tra_zip[1], color='royalblue', alpha=0.1)

    # plot multiple tra
    for tra in right_tra_list:
        tra_zip = list(zip(*tra))
        plt.plot(tra_zip[0], tra_zip[1], color='deeppink', alpha=0.1)


    # show ports
    port_color = 'k'
    port_size = 200
    plt.scatter(centerport_x, centerport_y, port_size, port_color)
    plt.text(centerport_x + 3, centerport_y, 'center port')
    plt.scatter(leftport_x, leftport_y, port_size, port_color)
    plt.text(leftport_x, leftport_y + 2.5, 'left port')
    plt.scatter(rightport_x, rightport_y, port_size, port_color)
    plt.text(rightport_x, rightport_y + 2.5, 'right port')

    # line connecting ports
    plt.plot([centerport_x, leftport_x], [centerport_y, leftport_y], 'k', linestyle='dashed')
    plt.plot([centerport_x, rightport_x], [centerport_y, rightport_y], 'k', linestyle='dashed')

    plt.ylim([centerport_y - 5, centerport_y + 30])
    plt.xlim([centerport_x - 60, centerport_x + 60])

    plt.gca().invert_yaxis()
    # plt.gca().set_aspect('equal')

    plt.xlabel('X axis (pixels)')
    plt.ylabel('Y axis (pixels)')
    plt.title(f'mice/session: {exp_name}'
              f'\n number of left trajectories: {len(left_tra_list)} '
              f'\n  number of right trajectories: {len(right_tra_list)}')
    adjust_figure()
    plt.savefig(os.path.join('./figures', exp_name+'.pdf'), transparent=True)
    plt.close()

