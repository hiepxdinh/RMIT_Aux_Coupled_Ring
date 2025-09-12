import sys
sys.path.append("C:/Work/OneDrive - RMIT University-/Software/asp_sin_lnoi_photonics/ipkiss")
sys.path.append("../")

import asp_sin_lnoi_photonics.technology
import asp_sin_lnoi_photonics.all as asp
import ipkiss3.all as i3
import numpy as np

from ring_modulator.cell import AddDropRingWithElectrode
from ring_gc.cell import RingModulatorGC


def ring_straight_length(radius, ng, fsr):
    ring_length = 3e8 / (fsr * 1e9)  / ng
    return int((ring_length - 2.0 * np.pi * radius * 1e-6) / 2 * 1e6)

# Calculate the ring parameters

ring_radius = 100
ng = 2.234

fsr = 20 # in GHz

straight_length = ring_straight_length(ring_radius, ng, fsr)

print("Ring straight length: {}".format(straight_length))

ring_gc = RingModulatorGC(                      ring_position=(4000, -5000),
                      gc_wg_distance=500,
                      ring_wg_distance=500
)
ring_gc_lo = ring_gc.Layout(ring_straight_length=straight_length,
                      coupler_spacing=1.0, # Coupler gap
                      coupler_straight_length=0,
                      electrode_length = straight_length - 150,
                      hot_width=20,
                      electrode_gap=7,
                      ring_position=(4000, -5000),
                      gc_wg_distance=500,
                      ring_wg_distance=500
                      )

ring_gc_lo.visualize(annotate=True)
ring_gc_lo.write_gdsii('test.gds')


