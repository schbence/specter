from kernel import *
import numpy as np

dir = '/Users/schbnc/Research/EEG/Resting_state_elemzesek/Zmax_PSD_output/'
inp = iomanager.InputManager(dir, ext='.txt', delim_white=True, transpose=True)
inp.check_shapes()
dat = datamodel.PSDDataSetModel(inp)
dat.set_freqs(np.linspace(0, 128, 1025))
dat.set_channels(['C3','C4'])

p1 = processors.ProcessorFOOOF()
dat.process(p1)
res1 = dat.get_results()

p2 = processors.ProcessorFOOOF()
p2.set_param('fit_range',[-500, 500])
dat.process(p2)
res2 = dat.get_results()
