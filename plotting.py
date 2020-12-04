import matplotlib.pyplot as plt
import matplotlib.colors
import matplotlib.animation as animation
from rhboard import RHBoard
import numpy as np


def plot_solution(path_solution, speed=1000, file_export=None):
    def rect(board):
        rhb = RHBoard(board)
        sit = rhb.board_status
        [p.remove() for p in reversed(ax.patches)]
        for k, v in sit.items():
            pos = np.array([v[0][1], v[0][0]])
            height = 1 if v[1] == 'V' else v[2]
            width = 1 if v[1] == 'H' else v[2]
            r = plt.Rectangle(pos - 0.5, height, width, facecolor="none", edgecolor="k", linewidth=2)
            plt.gca().add_patch(r)

    def generate_data():
        return path_solution[0][2].board

    def update(data):
        ax.set_title(u"Iter = {}, Car: {}".format(data[0], data[1][0]))
        mat.set_data(data[1][2].board)
        rect(data[1][2].board)
        return mat

    def data_gen():
        for i, subpath in enumerate(path_solution):
            yield i, subpath

    fig, ax = plt.subplots()

    vbig = plt.cm.get_cmap('cividis', 12)
    l_colors = [x for x in vbig(np.linspace(0.25, 0.75, 12))]
    colors = ["red", "white"] + l_colors
    colormap = matplotlib.colors.ListedColormap(colors)

    mat = ax.matshow(generate_data(), cmap=colormap)
    ani = animation.FuncAnimation(fig, update, data_gen, interval=speed,
                                  save_count=len(path_solution))

    writergif = animation.PillowWriter(fps=5)

    if file_export:
        ani.save(file_export, writer=writergif)

    plt.show()