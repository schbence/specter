import tkinter as tk
import numpy as np

class PlotView:

    x_pad_l = 40
    x_pad_r = 20
    y_pad = 40
    WIDTH = 400
    HEIGHT = 300

    def __init__(self, parent):
        self.xs = None
        self.ys = None
        self.size = (400, 300)
        self.canvas = tk.Canvas(parent, bg="#23241f", highlightthickness=0, width=self.size[0], height=self.size[1])
        self.canvas.pack(side='top', fill='both', expand=True)
        self.canvas.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        self.update()

    def set_data(self, data):
        subj_name, data_table = data
        self.xs = data_table['freq']
        psd_data = data_table.drop('freq', axis=1)
        self.ys = np.log(psd_data.values.T)
        self.labels = psd_data.columns
        del(psd_data)

    def set_data_simple(self, xs, ys):
        self.xs = xs
        self.ys = ys

    def test(self):
        xs = np.linspace(0.5, 50, 1025)
        ys = np.random.randn(2, 1025)
        self.set_data_simple(xs, ys)
        self.init_plot()

    def update(self):
        self.canvas.update()
        self.update_size()
        self.canvas.delete('all')
        self.draw_axes()
        self.draw_lines()

    def update_size(self):
        self.size = (self.canvas.winfo_width(), self.canvas.winfo_height())

    def init_plot(self):
        self.draw_axes()
        self.draw_lines()

    def get_draw_xs(self):
        return np.interp(self.xs, [min(self.xs), max(self.xs)], [PlotView.x_pad_l, self.size[0] - PlotView.x_pad_r])

    def get_draw_ys(self):
        return np.interp(self.ys,
            [np.min(self.ys), np.max(self.ys)],
            [self.size[1] - PlotView.y_pad, PlotView.y_pad])

    def draw_axes(self):
        self.canvas.create_line(
            PlotView.x_pad_l,
            self.size[1] - PlotView.y_pad,
            self.size[0] - PlotView.x_pad_r,
            self.size[1] - PlotView.y_pad,
            fill="#f0f0f0", width=3)

        self.canvas.create_line(
            PlotView.x_pad_l,
            self.size[1] - PlotView.y_pad,
            PlotView.x_pad_l,
            PlotView.y_pad,
            fill="#f0f0f0", width=3)

        # TODO draw ticks

    def draw_lines(self):
        drx = self.get_draw_xs()
        drys = self.get_draw_ys()
        for dry in drys:
            ps = np.vstack([drx, dry]).T.flatten()
            print("LEN PS: %d" % len(ps))
            self.canvas.create_line(list(ps), fill='#f0f0f0')
