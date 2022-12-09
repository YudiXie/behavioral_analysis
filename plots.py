import os
import matplotlib.pyplot as plt
import scipy.stats

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


def two_set_scatter_plot(data1, data2, labels, title_str, ylabel, save_str):
    """
    scatter plot for two groups
        :param data1: pandas series for data group 1
        :param data2: pandas series for data group 1
        :param labels: labels for two groups
        :param title_str: string for title
        :param ylabel: y label string
        :param save_str: string to save
    """
    mean_data1 = data1.mean()
    sem_data1 = data1.sem()
    data1_x = [1, ] * len(data1)

    mean_data2 = data2.mean()
    sem_data2 = data2.sem()
    data2_x = [2, ] * len(data2)

    # Mann-Whitney U rank test
    p_value = scipy.stats.mannwhitneyu(data1.dropna(), data2.dropna()).pvalue

    plt.figure(figsize=(2.5, 5))
    plt.scatter(data1_x, data1, 100, color='w', edgecolors='k', alpha=0.5)
    plt.errorbar([1], mean_data1, yerr=sem_data1,
                 fmt="o",
                 mfc='white',
                 ecolor='k',
                 color='k',
                 elinewidth=1,
                 capsize=10,
                 markersize=10
                 )

    plt.scatter(data2_x, data2, 100, color='mediumorchid', edgecolors='k', alpha=0.5)
    plt.errorbar([2], mean_data2, yerr=sem_data2,
                 fmt="o",
                 mfc='mediumorchid',
                 ecolor='k',
                 color='k',
                 elinewidth=1,
                 capsize=10,
                 markersize=10
                 )

    plt.xticks([1, 2], labels, rotation=45)
    plt.locator_params(nbins=5, axis='y')
    plt.xlim([0.5, 2.5])
    plt.title(title_str + "\nMann-Whitney U rank test P = {:.3f}".format(p_value))
    plt.ylabel(ylabel)
    adjust_figure()
    plt.savefig(save_str + '.pdf', transparent=True, bbox_inches="tight")
    plt.close()
