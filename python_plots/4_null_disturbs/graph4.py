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
df = pd.read_csv('null_disturbs.txt', sep=',')
df_voter = pd.read_csv('voter_null_disturbs.txt', sep=',')

# Draw a  boxplot 
#sns.set_style("darkgrid")
fig = plt.figure("null_sched")
plt.ylim(0, 200)
ax = sns.boxplot(
        x="disturb", 
        y="max_latency(us)", 
        order=["nodisturb", "cpu_disturb", "cache_disturb", "device_disturb", "io_disturb", "interrupt_disturb", "filesystem_disturb", "net_disturb"],
        palette=["lightblue", "lightblue", "lightblue", "lightblue", "lightblue", "lightblue", "lightblue", "lightblue"],
        data=df, 
        medianprops={"color": "red"},
        linewidth=2,
        width = 0.6
        )
ax.set(
    #title='Null Scheduler', 
    xlabel='Stress Levels', 
    ylabel='Maximum execution time [\u03BCs]'
)
ax.set_xticklabels(
    ["No", "CPU", "Cache", "Device", "I/O", "Intr", "FS", "Net"],
    rotation=30
)
plt.subplots_adjust(bottom=0.17, top=0.98)
#sns.despine(offset=10, trim=True)
#adjust_box_widths(fig, 0.8)

fig = plt.figure("voter_null_sched")
plt.ylim(0, 200)
ax = sns.boxplot(
        x="disturb", 
        y="max_latency(us)", 
        order=["nodisturb", "cpu_disturb", "cache_disturb", "device_disturb", "io_disturb", "interrupt_disturb", "filesystem_disturb", "net_disturb"],
        palette=["lightblue", "lightblue", "lightblue", "lightblue", "lightblue", "lightblue", "lightblue", "lightblue"],
        data=df_voter, 
        medianprops={"color": "red"},
        linewidth=2,
        width = 0.6
        )
ax.set(
    #title='Null Scheduler', 
    xlabel='Stress Levels', 
    ylabel='Maximum execution time [\u03BCs]'
)
ax.set_xticklabels(
    ["No", "CPU", "Cache", "Device", "I/O", "Intr", "FS", "Net"],
    rotation=30
)
plt.subplots_adjust(bottom=0.17, top=0.98)

plt.show()

