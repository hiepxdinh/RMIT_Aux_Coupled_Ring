import sys

sys.path.append("C:/Luceda/PDKs/asp_sin_lnoi_photonics-master/ipkiss")
sys.path.append("C:/pdk/asp_sin_lnoi_photonics/ipkiss")
import asp_sin_lnoi_photonics.technology
import asp_sin_lnoi_photonics.all as asp
import ipkiss3.all as i3
import numpy as np

from ring_gc.cell import RingModulatorGC
from ring_modulator.cell import AddDropRingWithElectrode
from waveguide_loop.cell import WaveguideLoop

#######################################
# Global parameters
######################################
waveguide_spacing = 50 # spacing between adjacent waveguides
bend_radius = 200  # Bending radius used in waveguide routing
hot_electrode_width = 20
fibre_array_pich = 127
ebl_writing_size = (1000, 1000)
chip_elements = list()


#### Calculate ring parameters ##########
def ring_straight_length(radius, ng, fsr):
    ring_length = 3e8 / (fsr * 1e9) / ng
    return int((ring_length - 2.0 * np.pi * radius * 1e-6) / 2 * 1e6)


ring_radius = 100
coupl_length = 0
ng = 2.234

fsr = 20  # in GHz

straight_length = ring_straight_length(ring_radius, ng, fsr)
ring_width = straight_length + ring_radius * 2

print("Ring straight length: {}".format(straight_length))
########################################


#######################################
# Main layout
######################################

######################################
# 1. Grid
######################################

grid = asp.FRAME_13000_10000_WITH_EBL_GRID()
grid_lo = grid.Layout(ebl_writing_size=ebl_writing_size)
chip_elements.append(i3.SRef(reference=grid, position=(0.0, 0.0)))

# Waveguide loop
wg_loop = WaveguideLoop(name="wg_loop")
wg_loop_lo = wg_loop.Layout(spacing=fibre_array_pich *13, bend_radius=150)


######################################
# I. First half electrode gap: 7um
#####################################
electrode_gap = 7


##################
# rings - 200GHz - Pulley
##################

h_separation = 665.0
v_separation = 35.0
separation = (0, 175, 175, 175, 175, 175, 175, 175, 175, 175)
gap_list = [1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]
for i, gap in enumerate(gap_list):
    ring = asp.EulerRectNotchRing()
    # ring.Layout(ring_radius=radius_200ghz, ring_gap=gap, v_separation = separation[i], ring_position_x=2650- i*h_separation, ring_position_y=(1-i)*v_separation)
    chip_elements.append(i3.SRef(reference=ring, position=(2500, 4500), transformation=i3.Rotation(rotation=90)))




first_half = i3.LayoutCell()
first_half_layout = first_half.Layout(elements=chip_elements)



######################################
# II. Second half electrode gap: 10um
#####################################
electrode_gap = 10
chip_elements = []

#######################################
# 1. Sweep the coupling gap - 1st row
######################################


second_half = i3.LayoutCell(name="Second_Half")
second_half_layout = second_half.Layout(elements=chip_elements)


####################################
# Generate the main layout
####################################
chip_design = i3.LayoutCell()
chip_layout = chip_design.Layout(elements=[i3.SRef(name="E_GAP_7um", reference=first_half_layout, position=(0, 0)),
                                           i3.SRef(name="E_GAP_10um", reference=second_half_layout, transformation=i3.VMirror() + i3.Translation(translation=(0, 10000)))
                                           ])
chip_layout.write_gdsii("gds_output/test_layout.gds")