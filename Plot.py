###
#   routing printing plot class
#   requires matplotlib package (https://matplotlib.org)

import matplotlib.pyplot as plt
import seaborn as sns
from Construction import create_unserved_cus
from Objectives import Instance


# draw nodes and routes
# requires list of routes: routes = [[0,..,0],..]
def draw_routes(routes: list[list[int]], nodes: dict, instance:Instance):
    # set colormap
    colors = plt.cm.get_cmap('viridis', len(routes))

    # set theme
    # sns.set_theme()

    fig, ax = plt.subplots()

    for r_idx, r in enumerate(filter(lambda r: len(r) > 2, routes)):
        path = list()
        for i in range(1, len(r)):
            if r[i]==0:
                path.append((nodes['x'][r[i]],
                             nodes['y'][r[i]]))
            else:
                path.append((nodes['x'][create_unserved_cus(instance).index(r[i])+1], nodes['y'][create_unserved_cus(instance).index(r[i])+1]))
        # print(path)

        # plot control points and connecting lines
        x, y = zip(*path)
        line, = ax.plot(x, y, 'o-', color=colors(r_idx))

    # plot depot
    ax.plot(nodes['x'][0], nodes['y'][0], 'ks')

    # # add labels to nodes
    # for k in nodes:
    #     plt.annotate('{:.2f}'.format(nodes[k]['id']),  # text
    #                 (nodes[k]['x'], nodes[k]['y']),  # coordinates to position the label
    #                 textcoords='offset points',  # position of text
    #                 xytext=(0, 10),  # distance between text and points (x,y)
    #                 ha='center')  # horizontal alignment

    # ax.grid()
    ax.axis('equal')

    # hide axis labels
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)

    # hide bounding box
    for pos in ['right', 'top', 'bottom', 'left']:
        plt.gca().spines[pos].set_visible(False)

    plt.show()

