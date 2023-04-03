import pandas as pd
from datetime import datetime

class PSDDataSetModel:

    def __init__(self, input_manager):
        if input_manager.checked:
            self.chs = []
            self.freqs = []
            self.input = input_manager
            self.outdir = '.'
            self.outfile = 'specter-output'
        else:
            print('Input manager has unchecked shapes')

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

    def freqs_chs_set(self):
        print("Freqs chs set test: %d %d" % (len(self.chs), len(self.freqs)))
        return len(self.chs) > 0 and len(self.freqs) > 0

    def get_data(self, n):
        if self.freqs_chs_set():
            subj, df = self.input.read(n)
            df.columns = self.chs
            df['freq'] = self.freqs
            df = df[['freq']+self.chs]
            return subj, df
        else:
            print("Warning: set the frequency bins and channel names before using the data!")

    def process_single(self, processor, i):
        subj, df = self.get_data(i)
        rows = []
        for ch in self.chs:
            psd = df[ch]
            ret = processor.doProcess(df['freq'].values, psd.values, report=False)

            row = {}
            row['CH'] = ch

            rows.append({**row, **ret})
        self.results = pd.DataFrame(rows)



    def process_batch(self, processor):
        print('Processing using %s' % processor.name)
        if self.freqs_chs_set():
            results = []
            for i in range(self.input.count()):
                subj, df = self.get_data(i)
                for ch in self.chs:
                    # Get the data
                    freqs = df['freq'].values
                    psd = df[ch].values
                    ret = processor.doProcess(freqs, psd)

                    # Store the results
                    row = {}
                    row['subj'] = subj
                    row['CH'] = ch
                    results.append({**row, **ret})
            df = pd.DataFrame(results)
            df = pd.pivot_table(df, index=['subj'], columns=['CH'])
            print(df)
            df.columns = ['_'.join(c).strip() for c in df.columns.values]
            self.results = df

        else:
            print("Warning: set the frequency bins and channel names before processing!")

    def get_results(self):
        return self.results

    def get_time(self):
        return datetime.now().strftime("%Y-%m-%d_%H-%M")

    def save_results(self, pname):
        self.outfile = '_'.join([pname, self.get_time()])
        path = self.outdir + '/' + self.outfile
        self.results.to_csv(path + '.csv')
        self.results.to_excel(path + '.xlsx')
        return path + '.csv'

    def __len__(self):
        return len(self.input.files)
