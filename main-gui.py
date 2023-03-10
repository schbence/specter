import tkinter as tk
from tkinter import filedialog
import gui.tableview as tv
from numpy.random import randint
import kernel.iomanager as io
import res.const as const


def generate_dummy_data():
    dat = []
    for n in range(0, randint(50)):
        name = str("Subj_%d") % randint(500)
        dat.append((name, randint(3), randint(1000)))
    return dat


class MainGUI:

    def __init__(self):
        self.init_vars()
        self.setup_gui()
        self.input_manager = None

    def init_vars(self):
        self.root = tk.Tk()
        self.root.minsize(1000,600)
        self.root.config(bg='skyblue')
        self.openDataCallback = None
        self.table_data = []
        self.dir_text = tk.StringVar()
        self.dir_text.set(const.INPUT_DIR_PLACEHOLDER)

    def setup_gui(self):
        self.setup_left_panel()
        self.setup_right_panel()

    def setup_left_panel(self):
        left = tk.Frame(self.root, width=600, height=600, bg='grey')
        left.pack(side='left', expand=True, fill='both')

        ltop = tk.Frame(left, width=600, height=100, bg='black')
        ltop.pack(side='top', fill='x')

        self.open_button = tk.Button(ltop, text='Open directory', command=self.select_input_dir, bg='black')
        self.open_button.grid(row=0, column=0)

        dir_label = tk.Label(ltop, textvariable=self.dir_text, bg='black', fg='white')
        dir_label.grid(row=0, column=1)

        lbot = tk.Frame(left, width=600, height=500)
        lbot.pack(side='bottom', fill='both', expand=True)

        self.table = tv.TableView(lbot, select_callback=lambda: self.select_callback())

        self.tree = self.table.get_tree()
        self.table.treeFrame.pack(fill='both', expand=True)

    def setup_right_panel(self):
        right = tk.Frame(self.root, width=400, height=600, bg='darkgrey')
        right.pack(side='right', expand=True, fill='both')

        rtop = tk.Frame(right, width=400, height=100, bg='darkred')
        rmid = tk.Frame(right, width=400, height=400, bg='yellow')
        rbot = tk.Frame(right, width=400, height=100, bg='darkgreen')

        rtop.pack(side='top', fill='both')
        rmid.pack(side='top', fill='both', expand=True, padx=4, pady=4)
        rbot.pack(side='bottom', fill='x')



    def select_callback(self):
        print("My selection: " + str(self.table.get_selected_idx()))



    def select_input_dir(self):
        dir = filedialog.askdirectory()
        if dir != '':
            self.set_current_dir(dir)
        else:
            print('Opening cancelled')

    def set_current_dir(self, dir):
        self.dir_text.set('Current dir: %s' % dir)
        self.input_manager = io.InputManager(dir, ext='.txt', delim_white=True, transpose=True)
        if self.input_manager.count() == 0:
            self.prompt_not_found()
        else:
            self.load_subjects_data()
            self.prompt_found()




    def load_subjects_data(self):
        self.tree.delete(*self.tree.get_children())
        self.table_data = self.input_manager.check_shapes()[0]
        for d in self.table_data:
            self.tree.insert('', tk.END, values=d)



    def prompt_not_found(self):
        self.dir_text.set(const.NO_FILES_FOUND % (self.input_manager.ext, self.input_manager.input_dir))

    def prompt_found(self):
        self.dir_text.set(const.FILES_FOUND % (self.input_manager.count(), self.input_manager.ext, self.input_manager.input_dir))


    def set_table_data(self, data):
        self.table_data = data



    def show(self):
        self.root.mainloop()



if __name__ == '__main__':
    g = MainGUI()
    g.show()
