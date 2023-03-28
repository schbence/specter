import pandas as pd
import os

class InputManager:

    def __init__(self, input_dir, ext='', delim_white=False, transpose=False):
        self.input_dir = os.path.abspath(input_dir)
        self.ext = ext
        self.locate_files()
        self.delim_white = delim_white
        self.t = transpose
        self.n_freqs = 0
        self.n_chs = 0
        self.checked = False

    def locate_files(self):
        all_files = os.listdir(self.input_dir)
        self.files = sorted(list(filter(lambda f:f.endswith(self.ext), all_files)))

    def get_filenames(self):
        return self.files

    def get_subj_name(self, i):
        return self.files[i]

    def get_full_paths(self):
        return list(map(lambda f:self.input_dir + '/' + f, self.files))

    def count(self):
        self.locate_files()
        return len(self.get_filenames())

    def read(self, n):
        print("Reading: '%s'" % self.files[n])
        if self.t:
            df = pd.read_csv(self.input_dir + '/' + self.files[n], delim_whitespace=self.delim_white, header=None).T
        else:
            df = pd.read_csv(self.input_dir + '/' + self.files[n], delim_whitespace=self.delim_white)
        return self.files[n], df

    def check_shapes(self):
        common_shape = self.read(0)[1].shape
        all_shapes = []
        self.checked = True
        for i in range(0, len(self.files)):
            si = self.read(i)[1].shape
            if not (si == common_shape):
                print("Shape inconsistency detected!")
                self.checked = False
            all_shapes.append((self.files[i],) + si)
        print("Shapes consistent! Freq bins: %d Channels: %d" % common_shape)
        self.n_freqs, self.n_chs = common_shape
        return all_shapes, self.checked, common_shape
