import pandas as pd
import pingouin as pg
import researchpy as rp
import numpy as np
import seaborn as sns
from scipy.stats import f_oneway
from scipy.stats import ttest_ind
import scipy.stats as stats
#import qgrid
import matplotlib as mpl
from mpltools import style
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

import warnings
warnings.filterwarnings('ignore')
#from mpltools import layout



plt.style.use('default')
cmap = ["#000000", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7"]

BLUE = cmap[5]
TURK = cmap[3]
ORANGE = cmap[1]
GREEN = cmap[2]



def raise_window(figname=None):
    """
    Raise the plot window for Figure figname to the foreground.  If no argument
    is given, raise the current figure.

    This function will only work with a Qt graphics backend.  It assumes you
    have already executed the command 'import matplotlib.pyplot as plt'.
    """

    if figname: plt.figure(figname)
    cfm = plt.get_current_fig_manager()
    cfm.window.activateWindow()
    cfm.window.raise_()


def barplot_annotate_brackets(
    num1, 
    num2, 
    data, 
    center, 
    height, 
    ax=None, 
    yerr=None, 
    dh=.05, 
    barh=.05, 
    fs=None, 
    maxasterix=None
    ):
    
    """ 
    Annotate barplot with p-values.

    :param num1: number of left bar to put bracket over
    :param num2: number of right bar to put bracket over
    :param data: string to write or number for generating asterixes
    :param center: centers of all bars (like plt.bar() input)
    :param height: heights of all bars (like plt.bar() input)
    :param yerr: yerrs of all bars (like plt.bar() input)
    :param dh: height offset over bar / bar + yerr in axes coordinates (0 to 1)
    :param barh: bar height in axes coordinates (0 to 1)
    :param fs: font size
    :param maxasterix: maximum number of asterixes to write (for very small p-values)
    """

    if type(data) is str:
        text = data

    lx, ly = center[num1], height[num1]
    rx, ry = center[num2], height[num2]

    if yerr:
        ly += yerr[num1]
        ry += yerr[num2]

    ax_y0, ax_y1 = ax.get_ylim() if ax!=None else plt.gca().get_ylim()
    dh *= (ax_y1 - ax_y0)
    barh *= (ax_y1 - ax_y0)

    y = max(ly, ry) + dh

    barx = [lx, lx, rx, rx]
    bary = [y, y+barh, y+barh, y]
    mid = ((lx+rx)/2, (y+barh)*1.0)
    
    if(ax!=None):
        ax.plot(barx, bary, c='black')
    else:
        plt.plot(barx, bary, c='black')

    kwargs = dict(ha='center', va='bottom')
    if fs is not None:
        kwargs['fontsize'] = fs
        
        
    if(ax!=None):
        ax.text(*mid, text, **kwargs)
    else:
        plt.text(*mid, text, **kwargs)

    

class ttest_results:
    
    def __init__(self, results):
        self.results = results
        
        self.d = results[1].loc[6].results
        self.pvalue = results[1].loc[3].results
        self.diff = results[1].loc[0].results

def plot():
    plt.show()
    cfm = plt.get_current_fig_manager()

    cfm.window.activateWindow()
    cfm.window.raise_()
    
    
def word_count(df_frequencies, title, color, saveas="", share_axis=True, figsize=(10,10)):

    num_plots = len(title)-1
    
    fig, axes = plt.subplots(1,num_plots)

    for ax in axes:
        sns.despine(bottom=False, left=False, ax=ax)
        
    top = []
    for i in range(num_plots):
        top.append(df_frequencies.iloc[i*20:(i+1)*20].sort_values())

        if type(color) == type([]):
            axes[i].barh(top[i].index, top[i].values, color=color[i])
        else:
            axes[i].barh(top[i].index, top[i].values, color=color)

    if share_axis:
        for ax in axes:
            ax.set_xlim(0,df_frequencies.head(20*num_plots).max())
            ax.set_xlabel("Count")

    if type(title) == type([]):
        for ax, t in zip(axes, title):
            ax.set_title(t)
        if(len(title) == num_plots+1):
             plt.suptitle(title[num_plots])
    else:
        plt.suptitle(title)

    for ax in axes:
        add_annotations(ax)

    plt.tight_layout()
    
    if(saveas != ""):
        plt.savefig(saveas)
        
    plt.show()


def add_annotations(ax):
    rects = ax.patches

    # Place a label for each bar
    for rect in rects:
        # Get X and Y placement of label from rect
        x_value = rect.get_width()
        y_value = rect.get_y() + rect.get_height() / 2

        # Number of points between bar and label; change to your liking
        space = 5
        # Vertical alignment for positive values
        ha = 'left'

        # If value of bar is negative: place label to the left of the bar
        if x_value < 0:
            # Invert space to place label to the left
            space *= -1
            # Horizontally align label to the right
            ha = 'right'

        # Use X value as label and format number
        label = '{:,.0f}'.format(x_value)

        # Create annotation
        #ax.annotate(
        #    label,                      # Use `label` as label
        #    (x_value, y_value),         # Place label at bar end
        #    xytext=(space, 0),          # Horizontally shift label by `space`
        #    textcoords='offset points', # Interpret `xytext` as offset in points
        #    va='center',                # Vertically center label
        #    ha=ha,                      # Horizontally align label differently for positive and negative values
        #    color = 'black')            # Change label color to white


def avg_words(df):
    return round(df.set_index("participant_id")[word_cols].T.sum().mean() ,2)

def remove_cols_prefix_dict(cols_list):
    return dict(zip(cols_list, [word.split("_")[1] for word in cols_list]))

def get_word_frequencies(df):
    return df[word_cols].sum().rename(remove_cols_prefix_dict(word_cols)).sort_values(ascending=False)
    
