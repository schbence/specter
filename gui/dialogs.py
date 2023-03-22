import tkinter as tk
import numpy as np

class ChannelNamesDialog:

    root = None

    def __init__(self, n_ch):
        self.top = tk.Toplevel(ChannelNamesDialog.root)
        self.N = n_ch
        fm = tk.Frame(self.top, borderwidth=4, relief='ridge')
        fm.pack(fill='both', expand=True)

        self.txts = []
        self.vars = [tk.StringVar() for i in range(self.N)]
        for i in range(self.N):
            label = tk.Label(fm, text="Channel %d" % i)
            label.pack(padx=4, pady=4)

            txt = tk.Entry(fm, width=6, textvariable=self.vars[i])
            txt.pack()

        closeButton = tk.Button(fm, text='Set')
        closeButton.pack(padx=4, pady=4)
        closeButton['command'] = self.top.destroy

    def getValues(self):
        self.top.grab_set()
        self.top.wait_window()
        vals = []
        for i in range(self.N):
            vals.append(self.vars[i].get())
        return vals

class ParameterInputDialog:

    root = None

    def __init__(self, param_names, param_types):
        self.top = tk.Toplevel(ParameterInputDialog.root)
        self.param_names = param_names
        self.param_types = param_types
        fm = tk.Frame(self.top, borderwidth=4, relief='ridge')
        fm.pack(fill='both', expand=True)

        self.str_vals = []
        self.str_vals = [tk.StringVar() for i in param_names]
        for i, param in enumerate(self.param_names):
            param_label = tk.Label(fm, text=param+':')
            param_label.pack(padx=4, pady=4)

            param_input = tk.Entry(fm, width=6, textvariable=self.str_vals[i])
            param_input.pack()

        closeButton = tk.Button(fm, text='Set')
        closeButton.pack(padx=4, pady=4)
        closeButton['command'] = self.top.destroy


    def getParamValues(self):
        new_params = {}
        for i, p in enumerate(self.param_names):
            new_params[p] = self.param_types[i](self.str_vals[i].get())
        print(new_params)
        return new_params






class FreqBinsDialog:

    root = None

    def __init__(self, n_freqs):
        self.N = n_freqs
        self.min = tk.StringVar()
        self.max = tk.StringVar()
        self.step = tk.StringVar()

        self.top = tk.Toplevel(FreqBinsDialog.root)
        fm = tk.Frame(self.top, borderwidth=4, relief='ridge')
        fm.pack(fill='both', expand=True)

        label_min = tk.Label(fm, text="f_min: ")
        label_min.pack(side='left')
        in_min = tk.Entry(fm, textvariable=self.min)
        in_min.pack(side='left')

        label_max = tk.Label(fm, text="f_max: ")
        label_max.pack(side='left')
        in_max = tk.Entry(fm, textvariable=self.max)
        in_max.pack(side='left')

        label_step = tk.Label(fm, text="f_step: ")
        label_step.pack(side='left')
        in_step = tk.Entry(fm, textvariable=self.step)
        in_step.pack(side='left')

        closeButton = tk.Button(fm, text='Set')
        closeButton.pack(padx=4, pady=4, side='bottom')
        closeButton['command'] = self.top.destroy

    def getValues(self):
        self.top.grab_set()
        self.top.wait_window()
        min = self.min
        if self.step.get() != '':
            print('Step not null')
            freqs = float(self.min.get()) + np.arange(self.N) * 1.0 / float(self.step.get())
        elif self.max.get() != '':
            print('Max not null')
            freqs = np.linspace(float(self.min.get()), float(self.max.get()), self.N)

        return freqs
