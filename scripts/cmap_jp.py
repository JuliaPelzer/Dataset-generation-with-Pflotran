import numpy as np
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap

# shifted hot colormap to better capture details
def new_cmap(colors, nodes, name:str=None):
    nodes[...] -= nodes[0]
    nodes /= nodes[-1]
    # print(nodes)

    if name:
        try:
            my_cmap = LinearSegmentedColormap.from_list(name, list(zip(nodes, colors)))
            mpl.colormaps.register(cmap=my_cmap)
        except:
            my_cmap = LinearSegmentedColormap.from_list("dummy", list(zip(nodes, colors)))
            print("Already defined")

name = "jp"
colors = ["white", "darkblue", "red", "orange", "white"]
nodes = np.array([10.6, 11.5, 12.8, 14, 15.6])
new_cmap(colors, nodes, name)

# name = "jp_wBroy"
# colors = ["white", "darkblue", "red", "orange", "yellow"]
# nodes = np.array([10.6, 11.5, 12.8, 14, 15.6])
# new_cmap(colors, nodes, name)

# call by 
# import DIR.cmap_jp
# in code: plt.imshow(data, cmap="jp")