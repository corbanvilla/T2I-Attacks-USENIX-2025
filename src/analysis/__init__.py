import json
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm
import matplotlib.ticker as ticker
import calendar
import scipy.stats as stats

from datetime import datetime
from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D

sns.set_theme(context="paper", font_scale=1.4, style="white")

# Set the palette
sns.color_palette()
sns.set_palette(sns.color_palette())

palette = sns.color_palette()

# GPT-4o release date (May 13, 2024)
gpt4o_release = datetime(2024, 5, 13)
gpt4o_release_epoch = gpt4o_release.timestamp()
