import matplotlib.pyplot as plt
import pandas as pd
import matplotlib

def get_color(x, max_x, cmap):
    if pd.isna(x):
        return 'darkgrey'
    return matplotlib.colors.rgb2hex(plt.get_cmap(cmap)(x/max_x))