import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, scrolledtext

from numpy.random import randint

import res.const as const

import kernel.iomanager as io
import kernel.datamodel as dm
import kernel.processors as ps

import gui.dialogs as dia
import gui.plotview as pv
import gui.tableview as tv


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
        self.datamodel = None
        self.processor = None

    def init_vars(self):
        self.root = tk.Tk()
        self.root.minsize(1000,600)
        self.root.config(bg='skyblue')
        self.openDataCallback = None
        self.table_view_data = []
        self.prompt_text = tk.StringVar()
        self.prompt_text.set(const.INPUT_DIR_PLACEHOLDER)
        self.active_processor_key = tk.StringVar()
        self.active_processor_key.set('<Select>')

    def setup_gui(self):
        self.setup_left_panel()
        self.setup_right_panel()

    def setup_left_panel(self):
        left = tk.Frame(self.root, width=600, height=600, bg='grey')
        left.pack(side='left', expand=True, fill='both')

        ltop = tk.Frame(left, width=600, height=100, bg='black')
        ltop.pack(side='top', fill='x')

        self.open_button = tk.Button(ltop, text='Open directory', command=self.select_input_dir)
        self.open_button.grid(row=0, column=0)

        dir_label = tk.Label(ltop, textvariable=self.prompt_text, bg='black', fg='white')
        dir_label.grid(row=0, column=1)

        lbot = tk.Frame(left, width=600, height=500)
        lbot.pack(side='bottom', fill='both', expand=True)

        self.table = tv.TableView(lbot, select_callback=lambda: self.subj_select_callback())

        self.tree = self.table.get_tree()
        self.table.treeFrame.pack(fill='both', expand=True)

    def setup_right_panel(self):
        right = tk.Frame(self.root, width=400, height=600, bg='darkgrey')
        right.pack(side='right', expand=True, fill='both')
        self.setup_right_top(right)
        self.setup_right_middle(right)
        self.setup_right_bottom(right)

    def setup_right_top(self, right):
        rtop = tk.Frame(right, width=400, height=100) #, bg='darkred')
        rtop.pack(side='top', fill='both')

        freqs_button = tk.Button(rtop, text='Set frequency bins', command=self.set_freq_bins)
        freqs_button.pack(side='left')

        chs_button = tk.Button(rtop, text='Set channel names', command=self.set_channel_names)
        chs_button.pack(side='left')

    def setup_right_middle(self, right):
        rmid = tk.Frame(right, width=400, height=300, bg='#525449')
        rmid.pack(side='top', fill='both', expand=True)

        self.plot = pv.PlotView(rmid)
        self.plot.test()

        log_frame = tk.Frame(right, width=400, height=50)
        log_frame.pack(side='top', fill='both', expand=True)

        self.log_panel = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=8)
        self.log_panel.configure(state='disabled')
        self.log_panel.pack(fill='both', expand=True)



    def add_log_message(self, message):
        self.log_panel.configure(state='normal')
        self.log_panel.insert('end', str(message) + '\n')
        self.log_panel.configure(state='disabled')
        self.log_panel.see('end')

    def setup_right_bottom(self, right):
        rbot1 = tk.Frame(right, width=400, height=100)
        rbot1.pack(side='top', fill='x')
        self.setup_processor_panel(rbot1)

        sep = ttk.Separator(right, orient='horizontal')
        sep.pack(fill='x')

        rbot2 = tk.Frame(right, width=400, height=100)
        rbot2.pack(side='top', fill='x')
        self.setup_batch_panel(rbot2)

    def setup_processor_panel(self, rbot1):
        processor_chooser_label = tk.Label(rbot1, text='Processor:')
        processor_chooser_label.pack(side='left', padx=5, pady=5)

        processor_chooser = ttk.Combobox(rbot1, textvariable=self.active_processor_key, state='readonly')
        processor_chooser['values'] = ps.get_enabled_ps_keys()
        processor_chooser.bind('<<ComboboxSelected>>', self.processor_choice_callback)
        processor_chooser.pack(side='left', padx=5, pady=5)

        set_param_button = tk.Button(rbot1, text='Set parameters...', command=self.set_params_callback)
        set_param_button.pack(side='left', padx=5, pady=5)

        process_one_button = tk.Button(rbot1, text='Run process', command=self.process_one_callback)
        process_one_button.pack(side='left', padx=5, pady=5)

    def setup_batch_panel(self, rbot2):
        batch_label = tk.Label(rbot2, text="Batch processing: ")
        batch_label.pack(side='left', padx=5, pady=5)

        out_options_button = tk.Button(rbot2, text='Output options')
        out_options_button.pack(side='left', padx=5, pady=5)

        batch_process_button = tk.Button(rbot2, text='Batch process', command=self.process_batch_callback)
        batch_process_button.pack(side='left', padx=5, pady=5)


    def set_channel_names(self):
        if self.input_manager != None and self.input_manager.checked:
            cnd = dia.ChannelNamesDialog(self.input_manager.n_chs)
            ch_names = cnd.getValues()
            self.datamodel.chs = ch_names
            print('Channels named as: %s' % str(ch_names))
        else:
            print('Error: input is not loaded so cannot set channel names')
            self.prompt_text.set(const.NO_VALID_DATA)

    def set_freq_bins(self):
        self.plot.update()
        if self.input_manager != None and self.input_manager.checked:
            print("Nfreqs %d" % self.input_manager.n_freqs)
            fbd = dia.FreqBinsDialog(self.input_manager.n_freqs)
            #print('Frequencies: %s' % str(fbd.getValues()))
            self.datamodel.freqs = fbd.getValues()
        else:
            print('Error: input is not loaded so cannot set frequencies')
            self.prompt_text.set(const.NO_VALID_DATA)

    def subj_select_callback(self):
        idx = self.table.get_selected_idx()
        print("My selection: " + str(idx))
        if self.datamodel.freqs_chs_set():
            self.plot.set_data(self.datamodel.get_data(idx[0]))
            self.plot.update()
            print(self.datamodel.get_data(idx[0]))

    def set_params_callback(self):
        print('Set the parameters for the processor')
        if (self.active_processor_key.get() == '<Select>'):
            self.prompt_text.set(const.NO_PROCESSOR_SELECTED)
        else:
            self.param_dialog = dia.ParameterInputDialog(self.processor)

    def update_processor_params(self):
        try:
            self.processor.params = self.param_dialog.get_param_values()
        except AttributeError:
            print('default params')

    def processor_choice_callback(self, event):
        print('Processor selected: %s' % self.active_processor_key.get())
        self.processor = ps.get_enabled_ps_dict()[self.active_processor_key.get()]

    def process_one_callback(self):
        if self.processor != None:
            if len(self.table.get_selected_idx()) > 0:
                self.update_processor_params()
                idx = self.table.get_selected_idx()[0]
                self.add_log_message('======================================================================')
                self.add_log_message("Processing Subj: %s" % self.datamodel.input.get_subj_name(idx))
                self.add_log_message('----------------------------------------------------------------------')
                self.add_log_message(' + Parameters: ')
                self.add_log_message(', '.join([p + ':' + str(self.processor.params[p]) for p in self.processor.params]))
                self.add_log_message('----------------------------------------------------------------------')

                self.datamodel.process_single(self.processor, idx)

                self.add_log_message(' + Results:')
                self.add_log_message(self.datamodel.get_results())
                self.add_log_message('======================================================================\n')
            else:
                self.prompt_text.set("Select a subject to process!")
        else:
            self.prompt_text.set("Choose a Processor!")

    def process_batch_callback(self):
        if self.processor != None:
            self.datamodel.process_batch(self.processor)
            self.add_log_message(self.datamodel.get_results())
        else:
            self.prompt_text.set("Choose a processor!")



    def select_input_dir(self):
        dir = filedialog.askdirectory()
        if dir != '':
            self.set_current_dir(dir)
        else:
            print('Opening cancelled')

    def set_current_dir(self, dir):
        self.prompt_text.set('Current dir: %s' % dir)
        self.input_manager = io.InputManager(dir, ext='.txt', delim_white=True, transpose=True)
        if self.input_manager.count() == 0:
            self.prompt_not_found()
        else:
            self.load_subjects_data()
            self.prompt_found()



    def load_subjects_data(self):
        self.tree.delete(*self.tree.get_children())
        self.table_view_data = self.input_manager.check_shapes()[0]
        for d in self.table_view_data:
            self.tree.insert('', tk.END, values=d)
        self.datamodel = dm.PSDDataSetModel(self.input_manager)



    def prompt_not_found(self):
        self.prompt_text.set(const.NO_FILES_FOUND % (self.input_manager.ext, self.input_manager.input_dir))

    def prompt_found(self):
        self.prompt_text.set(const.FILES_FOUND % (self.input_manager.count(), self.input_manager.ext, self.input_manager.input_dir))



    def show(self):
        self.root.mainloop()



if __name__ == '__main__':
    g = MainGUI()
    g.show()
