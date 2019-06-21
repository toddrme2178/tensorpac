"""
=====================================
Compute the ERPAC (Voytek et al 2013)
=====================================

Event-Related Phase-Amplitude Coupling (ERPAC) do not measure PAC across time
cycle but instead, across trials (just as proposed JP. Lachaux with the
PLV/PLS). Measuring across trials enable to have a real-time estimation of PAC.
Warning, depending on your data, even with tensor calculation the ERPAC is
significantly slower. Don't worry, take a coffee.

In this example, we generate a signal that have a 10<->100hz coupling the first
1000 points, then, the 700 following points are noise.
"""
import numpy as np
from tensorpac import Pac, pac_signals_wavelet

# Generate a 10<->100hz coupling :
n_epochs = 300
n_times = 1000
sf = 1024.
x1, tvec = pac_signals_wavelet(f_pha=10, f_amp=100, n_epochs=n_epochs, noise=2,
                               n_times=n_times, sf=sf)

# Generate noise and concatenate the coupling and the noise :
x2 = np.random.rand(n_epochs, 700)
x = np.concatenate((x1.squeeze(), x2), axis=1)  # Shape : (n_epochs, n_times)
time = np.arange(x.shape[1]) / sf

# Define a PAC object :
p = Pac(f_pha=[9, 11], f_amp=(60, 140, 5, 1))

# Extract the phase and the amplitude :
pha = p.filter(sf, x, ftype='phase')      # Shape (npha, n_epochs, n_times)
amp = p.filter(sf, x, ftype='amplitude')  # Shape (namp, n_epochs, n_times)

# Compute the ERPAC and use the traxis to specify that the trial axis is the
# first one :
erpac = p.erpac(pha, amp).squeeze()
pval = p.pvalues_.squeeze()

# Plot without p-values :
p.pacplot(erpac, time, p.yvec, xlabel='Time (second)', cmap='Spectral_r',
          ylabel='Amplitude frequency', title=str(p), cblabel='ERPAC',
          vmin=0., rmaxis=True)

# Plot with every non-significant values masked in gray :
# p.pacplot(erpac, time, p.yvec, xlabel='Time (second)', cmap='Spectral_r',
#           ylabel='Amplitude frequency', title='ERPAC example', vmin=0.,
#           vmax=1., pvalues=pval, bad='lightgray', plotas='contour',
#           cblabel='ERPAC')

# Plot with significiendy levels :
# p.pacplot(erpac, time, p.yvec, xlabel='Time (second)', cmap='Spectral_r',
#           ylabel='Amplitude frequency', title='ERPAC example', vmin=0.,
#           vmax=1., pvalues=pval, levels=[1e-20, 1e-10, 1e-2, 0.05],
#           levelcmap='inferno', plotas='contour', cblabel='ERPAC')
# p.savefig('erpac.png', dpi=300)
p.show()