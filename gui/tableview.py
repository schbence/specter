import tkinter as tk
from tkinter import ttk
from numpy.random import randint


def create_table_view(parent):
    columns = ('subj', 'n_chs', 'n_freqs')

    treeFrame = tk.Frame(parent)

    tree = ttk.Treeview(treeFrame, columns = columns, show = 'headings')

    tree.heading('subj', text='Subject')
    tree.heading('n_freqs', text='N_FREQS')
    tree.heading('n_chs', text='N_CHS')

    def item_selected(event):
        for selected_item in tree.selection():
            print(selected_item)
            '''
            item = tree.item(selected_item)
            record = item['values']
            print(",".join(record))
            '''
        print('----------------------')

    tree.bind('<<TreeviewSelect>>', item_selected)
    tree.pack(fill='both', side=tk.LEFT, expand=True)
    #tree.grid(row=0, column=0, sticky='nsew')

    scrollbar = ttk.Scrollbar(treeFrame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(fill='y', side=tk.RIGHT)
    #scrollbar.grid(row=0, column=1, sticky='ns')
    return treeFrame, tree

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Table demo')
    root.geometry('800x600')
    tf, tree = create_table_view(root)
    tf.pack(fill='both', expand=True)
    root.mainloop()
