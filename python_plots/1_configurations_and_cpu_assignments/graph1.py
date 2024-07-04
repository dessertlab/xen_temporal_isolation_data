from cProfile import label
from turtle import title
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import seaborn.objects as so

from matplotlib.patches import PathPatch

def adjust_box_widths(g, fac):
    """
    Adjust the withs of a seaborn-generated boxplot.
    """
    # iterating through Axes instances
    for ax in g.axes:

        # iterating through axes artists:
        for c in ax.get_children():

            # searching for PathPatches
            if isinstance(c, PathPatch):
                # getting current width of box:
                p = c.get_path()
                verts = p.vertices
                verts_sub = verts[:-1]
                xmin = np.min(verts_sub[:, 0])
                xmax = np.max(verts_sub[:, 0])
                xmid = 0.5*(xmin+xmax)
                xhalf = 0.5*(xmax - xmin)

                # setting new width of box
                xmin_new = xmid-fac*xhalf
                xmax_new = xmid+fac*xhalf
                verts_sub[verts_sub[:, 0] == xmin, 0] = xmin_new
                verts_sub[verts_sub[:, 0] == xmax, 0] = xmax_new

                # setting new width of median line
                for l in ax.lines:
                    if np.all(l.get_xdata() == [xmin, xmax]):
                        l.set_xdata([xmin_new, xmax_new])

sns.set_theme(style="whitegrid", palette="pastel",font_scale=3)

# Load the example tips dataset
df_credit = pd.read_csv('credit2_data.txt', sep=',')
df_rtds = pd.read_csv('rtds_data.txt', sep=',')

# Draw boxplots 
fig= plt.figure("credit")
plt.ylim(0, 600)
ax = sns.boxplot(
        x="ratelimit(us)", 
        y="max_latency(us)", 
        hue="cpu_assignment", 
        hue_order=["one_to_one","many_to_many"],
        palette=["g","m"],
        data=df_credit, 
        medianprops={"color": "coral"},
        linewidth=4
        )
ax.set(
    #title='Scheduler: Credit2', 
    xlabel='Rate limit [\u03BCs]', 
    ylabel='Maximum execution time [\u03BCs]'
)
handles, _ = ax.get_legend_handles_labels()
ax.legend(handles,["One-to-One", "Many-to-Many"]).set_title("CPU pinning")
adjust_box_widths(fig, 0.8)

fig = plt.figure("rtds")
plt.ylim(0, 600)
ax = sns.boxplot(
        x="budget_on_period(us)", 
        y="max_latency(us)", 
        order=["1k/5k","3k/9k","5k/10k","10k/10k"],
        hue="cpu_assignment", 
        hue_order=["one_to_one","many_to_many"],
        palette=["g","m"],
        data=df_rtds, 
        medianprops={"color": "coral"},
        linewidth=4
        )
ax.set(
    #title='Scheduler: RTDS', 
    xlabel='Budget on Period [\u03BCs]', 
    ylabel='Maximum execution time [\u03BCs]'
)
handles, _ = ax.get_legend_handles_labels()
ax.legend(handles,["One-to-One", "Many-to-Many"]).set_title("CPU pinning")
adjust_box_widths(fig, 0.8)

plt.show()

