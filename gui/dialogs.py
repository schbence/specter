import tkinter as tk

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
            label = tk.Label(fm, text="Label %d" % i)
            label.pack(padx=4, pady=4)

            txt = tk.Entry(fm, width=6, textvariable=self.vars[i])
            txt.pack()

        closeButton = tk.Button(fm, text='Close')
        closeButton.pack(padx=4, pady=4)
        closeButton['command'] = self.top.destroy

    def getValues(self):
        self.top.grab_set()
        self.top.wait_window()
        vals = []
        for i in range(self.N):
            vals.append(self.vars[i].get())
        return vals
