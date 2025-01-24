import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm
import matplotlib.ticker as ticker
import calendar
from datetime import datetime
from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D
import numpy as np
import json

# sns.set_theme(
#     context="paper", font="Times New Roman", font_scale=1.5, style="whitegrid"
# )
sns.set_theme(
    context="paper", font="Times New Roman", style="whitegrid", font_scale=1.2
)
# plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]
plt.rcParams["font.size"] = 12
# plt.rcParams['mathtext.fontset'] = 'stix'  # 'stix' resembles Times

# Set the palette
sns.color_palette()
sns.set_palette(sns.color_palette())

palette = sns.color_palette()

# GPT-4o release date (May 13, 2024)
gpt4o_release = datetime(2024, 5, 13)
gpt4o_release_epoch = gpt4o_release.timestamp()
