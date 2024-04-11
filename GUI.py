import tkinter as tk
from tkinter import filedialog 
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from main import generate
import os
cmaps = [('Perceptually Uniform Sequential', [
            'viridis', 'plasma', 'inferno', 'magma', 'cividis']),
         ('Sequential', [
            'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']),
         ('Sequential (2)', [
            'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
            'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
            'hot', 'afmhot', 'gist_heat', 'copper']),
         ('Diverging', [
            'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
            'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']),
         ('Cyclic', ['twilight', 'twilight_shifted', 'hsv']),
         ('Qualitative', [
            'Pastel1', 'Pastel2', 'Paired', 'Accent',
            'Dark2', 'Set1', 'Set2', 'Set3',
            'tab10', 'tab20', 'tab20b', 'tab20c']),
         ('Miscellaneous', [
            'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
            'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
            'gist_rainbow', 'rainbow', 'jet', 'turbo', 'nipy_spectral',
            'gist_ncar'])]

def plot_color_map(cmap_name):
    cmap = matplotlib.colormaps.get_cmap(cmap_name)
    fig, ax = plt.subplots(figsize=(5, 2))
    ax.imshow([[i] for i in range(10)], cmap=cmap)
    ax.axis('off')
    ax.set_title(cmap_name)
    plt.tight_layout()

class ColorMapSelectorApp:
    def __init__(self, master):
        self.master = master
        master.resizable(False, False)

        self.category_var = tk.StringVar(master)
        self.category_var.set(cmaps[0][0])  # Default to first category
        self.category_menu = tk.OptionMenu(master, self.category_var, *[(category[0]) for category in cmaps], command=self.update_cmap_menu)
        self.category_menu.grid(row=0, column=0)

        self.cmap_var = tk.StringVar(master)
        self.cmap_var.set(cmaps[0][1][0])  # Default to first colormap
        self.cmap_menu = tk.OptionMenu(master, self.cmap_var, *cmaps[0][1], command=self.update_plot)
        self.cmap_menu.grid(row=0, column=1)

        self.plot_frame = tk.Frame(master)
        self.plot_frame.grid(row=1, column=0, columnspan=2)

        self.generate_button = tk.Button(master, text="Generate", command=self.generate)
        self.generate_button.grid(row=2, column=0, columnspan=2)

        self.plot()

    def update_cmap_menu(self, category):
        self.cmap_menu['menu'].delete(0, tk.END)  # Clear existing options
        cmaps_in_category = [entry[1] for entry in cmaps if entry[0] == category][0]
        for cmap in cmaps_in_category:
            self.cmap_menu['menu'].add_command(label=cmap, command=tk._setit(self.cmap_var, cmap, self.update_plot))

    def update_plot(self, *args):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        plot_color_map(self.cmap_var.get())
        canvas = FigureCanvasTkAgg(plt.gcf(), master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def generate(self):
        target_folder = filedialog.askdirectory()
        print('Path: ', os.path.join(target_folder, 'map.html'))
        generate(self.cmap_var.get(), target_folder)

    def plot(self):
        plot_color_map(self.cmap_var.get())
        canvas = FigureCanvasTkAgg(plt.gcf(), master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
    
    def close_window(self):
        self.master.destroy()

root = tk.Tk()
root.title("Color Map Generator")
root.geometry("500x300")
app = ColorMapSelectorApp(root)
root.mainloop()