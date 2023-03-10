class ProcessorFOOOF:

    outputs = ('slope','inter')
    name = 'FOOOF'

    def __init__(self):
        self.setup_params()
        print("%s processor initialized" % self.name)

    def setup_params(self):
        self.params = {}
        self.params['fit_range'] = [0.25, 48.]
        self.params['knee'] = False

    def get_param_names(self):
        return list(self.params.keys())

    def set_param(self, key, value):
        self.params[key] = value

    def doProcess(self, freq, psd):
        pmean = psd.mean()
        fmean = freq.mean()
        return fmean + self.params['fit_range'][0], pmean + self.params['fit_range'][1]

    def report(self, report_dir, id, info=None):
        pass
