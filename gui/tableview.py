import tkinter as tk
from tkinter import ttk
from numpy.random import randint


class TableView:
    def __init__(self, parent, select_callback=None):
        columns = ('subj', 'n_chs', 'n_freqs')

        self.select_callback = select_callback

        self.treeFrame = tk.Frame(parent)
        self.tree = ttk.Treeview(self.treeFrame, columns = columns, show = 'headings')

        self.init_columns()

        self.tree.bind('<<TreeviewSelect>>', self.item_selected)
        self.tree.pack(fill='both', side=tk.LEFT, expand=True)

        self.setup_scrollbar()

    def get_tree(self):
        return self.tree

    def init_columns(self):
        self.tree.heading('subj', text='Subject')
        self.tree.heading('n_freqs', text='N_FREQS')
        self.tree.heading('n_chs', text='N_CHS')

    def setup_scrollbar(self):
        scrollbar = ttk.Scrollbar(self.treeFrame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(fill='y', side=tk.RIGHT)

    def item_selected(self, event):
        idx = self.get_selected_idx()
        # print(idx)
        # print('---')
        if self.select_callback:
            self.select_callback()

    def get_selected_idx(self):
        return list(map(self.tree.index, self.tree.selection()))


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Table demo')
    root.geometry('800x600')
    tf, tree = create_table_view(root)
    tf.pack(fill='both', expand=True)
    root.mainloop()
