from kernel.mytypes import *

class ProcessorFOOOF:

    name = 'FOOOF'
    outputs = ('slope','inter')

    param_defs = {}
    param_defs['fit_low']  = {'val' : 0.25,  'type' : float}
    param_defs['fit_high'] = {'val' : 48.0,  'type' : float}
    param_defs['use_knee'] = {'val' : False, 'type' : my_bool}

    def __init__(self):
        self.params = {}
        self.setup_params()
        print("%s processor initialized" % self.name)

    def setup_params(self):
        for param in ProcessorFOOOF.param_defs:
            self.params[param] = ProcessorFOOOF.param_defs[param]['val']


    def get_param_names(self):
        return list(self.params.keys())

    def get_param_types(self):
        return list([p['type'] for p in ProcessorFOOOF.param_defs.values()])

    def set_param(self, key, value):
        if key in list(ProcessorFOOOF.param_defs.keys()):
            self.params[key] = value
        else:
            print('No such parameter!')

    def doProcess(self, freq, psd):
        pmean = psd.mean()
        fmean = freq.mean()
        return fmean + self.params['fit_low'], pmean + self.params['fit_high']

    def report(self, report_dir, id, info=None):
        pass


ENABLED_PROCESSORS = [ProcessorFOOOF(), ProcessorFOOOF(), ProcessorFOOOF()]

def get_enabled_ps_dict():
    return dict(zip([p.name for p in ENABLED_PROCESSORS], ENABLED_PROCESSORS))

def get_enabled_ps_keys():
    return list(get_enabled_ps_dict().keys())
