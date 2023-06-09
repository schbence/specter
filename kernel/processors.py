from kernel.mytypes import *
from fooof import FOOOF
import numpy as np

class ProcessorFOOOF:

    name = 'FOOOF'
    outputs = ('slope','inter')

    param_defs = {}
    param_defs['fit_low']  = {'val' : 0.25,  'type' : float}
    param_defs['fit_high'] = {'val' : 48.0,  'type' : float}
    param_defs['max_n_peaks'] = {'val' : 6, 'type' : int}
    param_defs['peak_threshold'] = {'val' : 2.0,  'type' : float}
    #param_defs['use_knee'] = {'val' : False, 'type' : my_bool}

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

    def get_default_values(self):
        return list([p['val'] for p in ProcessorFOOOF.param_defs.values()])

    def set_param(self, key, value):
        if key in list(ProcessorFOOOF.param_defs.keys()):
            self.params[key] = value
        else:
            print('No such parameter!')

    def doProcess(self, freq, psd, report=False):
        # calculate outputs
        print(self.params['max_n_peaks'])
        model = FOOOF(
            aperiodic_mode = 'fixed',
            max_n_peaks    = self.params['max_n_peaks'],
            peak_threshold = self.params['peak_threshold'])
        model.fit(freq, psd, freq_range = [self.params['fit_low'], self.params['fit_high']])
        slope = model.get_params('aperiodic_params', 'exponent')
        inter = model.get_params('aperiodic_params', 'offset')
        if report:
            model.report()
        return {'slope' : slope, 'inter' : inter}

    def report(self, report_dir, id, info=None):
        pass


ENABLED_PROCESSORS = [ProcessorFOOOF()]

def get_enabled_ps_dict():
    return dict(zip([p.name for p in ENABLED_PROCESSORS], ENABLED_PROCESSORS))

def get_enabled_ps_keys():
    return list(get_enabled_ps_dict().keys())
