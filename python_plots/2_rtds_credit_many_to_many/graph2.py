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
df = pd.read_csv('credit_rtds_high.txt', sep=',')

# Draw a  boxplot 
#sns.set_style("darkgrid")
fig = plt.figure("credit2_rtds")
plt.ylim(0, 600)
ax = sns.boxplot(
        x="scheduler", 
        y="max_latency(us)", 
        hue="disturb", 
        hue_order=["nodisturb","cpu_disturb"], 
        palette=["lightblue", "r"], 
        data=df, 
        medianprops={"color": "coral"},
        linewidth=4,
        width=0.5
        )
ax.set(
    #title='Scheduler (many to many) comparison', 
    xlabel='Scheduler', 
    ylabel='Maximum execution time [\u03BCs]'
)
ax.set_xticklabels(
    ["Credit2","RTDS"]
)
#sns.despine(offset=10, trim=True)
handles, _ = ax.get_legend_handles_labels()
ax.legend(handles,["No", "Yes"]).set_title("CPU Stress")
adjust_box_widths(fig, 0.8)
plt.show()

