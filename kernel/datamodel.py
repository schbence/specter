import pandas as pd

class PSDDataSetModel:

    def __init__(self, input_manager):
        if input_manager.check_shapes()[1]:
            self.chs = []
            self.freqs = []
            self.input = input_manager

    def set_freqs(self, freqs):
        if len(freqs) == self.input.n_freqs:
            self.freqs = freqs
        else:
            print("Warning: freq bin number difference!")

    def set_channels(self, chs):
        if len(chs) == self.input.n_chs:
            self.chs = chs
        else:
            print("Warning: channel number difference!")

    def get_data(self, n):
        subj, df = self.input.read(n)
        df.columns = self.chs
        df['freq'] = self.freqs
        df = df[['freq']+self.chs]
        return subj, df

    def process(self, processor):
        print('Processing using %s' % processor.name)
        if len(self.chs) > 0 and len(self.freqs) > 0:
            results = []
            for i in range(self.input.count()):
                subj, df = self.get_data(i)
                for ch in self.chs:
                    # Get the data
                    psd = df[ch]
                    ret = processor.doProcess(df['freq'], psd)

                    # Store the results
                    row = {}
                    row['subj'] = subj
                    row['CH'] = ch
                    for j, out in enumerate(processor.outputs):
                        row[out] = ret[j]
                    results.append(row)
            self.results = pd.DataFrame(results)
        else:
            print("Warning: set the frequency bins and channel names before processing!")

    def get_results(self):
        return self.results

    def __len__(self):
        return len(self.input.files)
