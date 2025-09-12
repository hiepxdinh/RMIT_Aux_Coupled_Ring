import sys

sys.path.append("C:/Luceda/PDKs/asp_sin_lnoi_photonics-master/ipkiss")

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


ring_radius = 230
coupl_length = 0
ng = 2.234

fsr = 19  # in GHz

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

#######################################
# 1. Sweep the coupling gap - 1st row
######################################
# coupling_gaps = [0.8, 0.85]
#
# gc_position = (5800, 9500)  # Position of the first grating coupler
#
#
# chip_elements.append(i3.SRef(name="wg_loop_1", reference=wg_loop_lo, position=gc_position))
#
# ring = AddDropRingWithElectrode()
# ring_lo = ring.Layout(ring_straight_length=straight_length,
#                       coupler_spacing=coupling_gaps[0], # Coupler gap
#                       #coupler_positions=[-2500,2500],
#                       coupler_straight_length=0,
#                       electrode_length=straight_length - 150,
#                       hot_width=hot_electrode_width,
#                       electrode_gap=electrode_gap
#                       )
#
# ring_in_pos = ring_lo.ports['in'].position
#
# first_ring_position = (-ring_in_pos[0] + bend_radius + 50, -1260)
#
#
# for i, gap in enumerate(coupling_gaps):
#     name = "Ring_EG_{}G_{}".format(electrode_gap, gap)
#     ring_gc = RingModulatorGC(name=name)
#     ring_position = (first_ring_position[0] + ring_width * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_position[1])
#     print("ring_position: {}".format(ring_position))
#     ring_gc_lo = ring_gc.Layout(ring_radius=ring_radius,
#                                 ring_straight_length=straight_length,
#                                 coupler_spacing=gap,  # Coupler gap
#                                 coupler_straight_length=coupl_length,
#                                 coupler_positions=[-straight_length * 0.125 + coupl_length,
#                                                    straight_length * 0.2 - coupl_length],
#                                 electrode_length=straight_length - 150,
#                                 hot_width=hot_electrode_width,
#                                 electrode_gap=electrode_gap,
#                                 ring_position=ring_position,
#                                 gc_wg_distance=-ring_position[1] - ring_radius - 50 - bend_radius * 2 - waveguide_spacing * 4 * i,
#                                 ring_wg_distance=bend_radius + 50,
#                                 bend_radius=bend_radius,
#                                 gc_spacing=fibre_array_pich,
#                                 waveguide_spacing=waveguide_spacing
#                                 )
#
#     #ring_gc_lo.visualize()
#
#     chip_elements.append(i3.SRef(name=name, reference=ring_gc, position=(gc_position[0] + fibre_array_pich + fibre_array_pich * 4 * i, gc_position[1])))



#######################################
# 1. Sweep the coupling gap - 2nd row
######################################
coupling_gaps = [0.9, 0.95, 1.0]

gc_position = (3130, 9250)  # Position of the first grating coupler

# Waveguide loop
wg_loop = WaveguideLoop(name="wg_loop")
wg_loop_lo = wg_loop.Layout(spacing=fibre_array_pich *13, bend_radius=150)

chip_elements.append(i3.SRef(name="wg_loop_2", reference=wg_loop_lo, position=gc_position))

ring = AddDropRingWithElectrode()
ring_lo = ring.Layout(ring_straight_length=straight_length,
                      coupler_spacing=coupling_gaps[0], # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length - 150,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_in_pos = ring_lo.ports['in'].position

first_ring_position = (-ring_in_pos[0] + bend_radius + 50, -1850)


for i, gap in enumerate(coupling_gaps):
    name = "Ring_EG_{}G_{}".format(electrode_gap, gap)
    ring_gc = RingModulatorGC(name=name)
    ring_position = (first_ring_position[0] + ring_width * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_position[1])
    print("ring_position: {}".format(ring_position))
    ring_gc_lo = ring_gc.Layout(ring_radius=ring_radius,
                                ring_straight_length=straight_length,
                                coupler_spacing=gap,  # Coupler gap
                                coupler_straight_length=coupl_length,
                                coupler_positions=[-straight_length * 0.125 + coupl_length,
                                                   straight_length * 0.2 - coupl_length],
                                electrode_length=straight_length - 150,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                ring_position=ring_position,
                                gc_wg_distance=-ring_position[1] - ring_radius - 50 - bend_radius * 2 - waveguide_spacing * 4 * i,
                                ring_wg_distance=bend_radius + 50,
                                bend_radius=bend_radius,
                                gc_spacing=fibre_array_pich,
                                waveguide_spacing=waveguide_spacing
                                )

    #ring_gc_lo.visualize()

    chip_elements.append(i3.SRef(name=name, reference=ring_gc, position=(gc_position[0] + fibre_array_pich + fibre_array_pich * 4 * i, gc_position[1])))



#######################################
# 1. Sweep the coupling gap - 3rd row
######################################
coupling_gaps = [1.05, 1.1, 1.15]

gc_position = (700, 9250)  # Position of the first grating coupler

chip_elements.append(i3.SRef(name="wg_loop_3", reference=wg_loop_lo, position=gc_position))

ring = AddDropRingWithElectrode()
ring_lo = ring.Layout(ring_straight_length=straight_length,
                      coupler_spacing=coupling_gaps[0], # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length - 150,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_in_pos = ring_lo.ports['in'].position

first_ring_position = (-ring_in_pos[0] + bend_radius * 3 + 1065, -3750)


for i, gap in enumerate(coupling_gaps):
    name = "Ring_EG_{}G_{}".format(electrode_gap, gap)
    ring_gc = RingModulatorGC(name=name)
    ring_position = (first_ring_position[0] + ring_width * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_position[1])
    print("ring_position: {}".format(ring_position))
    ring_gc_lo = ring_gc.Layout(ring_radius=ring_radius,
                                ring_straight_length=straight_length,
                                coupler_spacing=gap,  # Coupler gap
                                coupler_straight_length=coupl_length,
                                coupler_positions=[-straight_length * 0.125 + coupl_length,
                                                   straight_length * 0.2 - coupl_length],
                                electrode_length=straight_length - 150,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                ring_position=ring_position,
                                gc_wg_distance=-ring_position[1] - ring_radius - 50 - bend_radius * 2 - waveguide_spacing * 4 * i,
                                ring_wg_distance=bend_radius + 50,
                                bend_radius=bend_radius,
                                gc_spacing=fibre_array_pich,
                                waveguide_spacing=waveguide_spacing
                                )

    #ring_gc_lo.visualize()

    chip_elements.append(i3.SRef(name=name, reference=ring_gc, position=(gc_position[0] + fibre_array_pich + fibre_array_pich * 4 * i, gc_position[1])))


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
# coupling_gaps = [0.8, 0.85]
#
# gc_position = (5800, 9500)  # Position of the first grating coupler
#
#
# chip_elements.append(i3.SRef(name="wg_loop_1", reference=wg_loop_lo, position=gc_position))
#
# ring = AddDropRingWithElectrode()
# ring_lo = ring.Layout(ring_straight_length=straight_length,
#                       coupler_spacing=coupling_gaps[0], # Coupler gap
#                       coupler_straight_length=0,
#                       electrode_length=straight_length - 150,
#                       hot_width=hot_electrode_width,
#                       electrode_gap=electrode_gap
#                       )
#
# ring_in_pos = ring_lo.ports['in'].position
#
# first_ring_position = (-ring_in_pos[0] + bend_radius + 50, -1260)
#
#
# for i, gap in enumerate(coupling_gaps):
#     name = "Ring_EG_{}G_{}".format(electrode_gap, gap)
#     ring_gc = RingModulatorGC(name=name)
#     ring_position = (first_ring_position[0] + ring_width * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_position[1])
#     print("ring_position: {}".format(ring_position))
#     ring_gc_lo = ring_gc.Layout(ring_radius=ring_radius,
#                                 ring_straight_length=straight_length,
#                                 coupler_spacing=gap,  # Coupler gap
#                                 coupler_straight_length=coupl_length,
#                                 coupler_positions=[-straight_length * 0.125 + coupl_length,
#                                                    straight_length * 0.2 - coupl_length],
#                                 electrode_length=straight_length - 150,
#                                 hot_width=hot_electrode_width,
#                                 electrode_gap=electrode_gap,
#                                 ring_position=ring_position,
#                                 gc_wg_distance=-ring_position[1] - ring_radius - 50 - bend_radius * 2 - waveguide_spacing * 4 * i,
#                                 ring_wg_distance=bend_radius + 50,
#                                 bend_radius=bend_radius,
#                                 gc_spacing=fibre_array_pich,
#                                 waveguide_spacing=waveguide_spacing
#                                 )
#
#     #ring_gc_lo.visualize()
#
#     chip_elements.append(i3.SRef(name=name, reference=ring_gc, position=(gc_position[0] + fibre_array_pich + fibre_array_pich * 4 * i, gc_position[1])))



#######################################
# 1. Sweep the coupling gap - 2nd row
######################################
coupling_gaps = [0.9, 0.95, 1.0]

gc_position = (3130, 9250)  # Position of the first grating coupler

# Waveguide loop
wg_loop = WaveguideLoop(name="wg_loop")
wg_loop_lo = wg_loop.Layout(spacing=fibre_array_pich *13, bend_radius=150)

chip_elements.append(i3.SRef(name="wg_loop_2", reference=wg_loop_lo, position=gc_position))

ring = AddDropRingWithElectrode()
ring_lo = ring.Layout(ring_straight_length=straight_length,
                      coupler_spacing=coupling_gaps[0], # Coupler gap
                      coupler_straight_length=coupl_length,
                      electrode_length=straight_length - 150,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_in_pos = ring_lo.ports['in'].position

first_ring_position = (-ring_in_pos[0] + bend_radius + 50, -1850)


for i, gap in enumerate(coupling_gaps):
    name = "Ring_EG_{}G_{}".format(electrode_gap, gap)
    ring_gc = RingModulatorGC(name=name)
    ring_position = (first_ring_position[0] + ring_width * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_position[1])
    print("ring_position: {}".format(ring_position))
    ring_gc_lo = ring_gc.Layout(ring_radius=ring_radius,
                                ring_straight_length=straight_length,
                                coupler_spacing=gap,  # Coupler gap
                                coupler_straight_length=coupl_length,
                                coupler_positions=[-straight_length * 0.125 + coupl_length,straight_length * 0.2 - coupl_length],
                                electrode_length=straight_length - 150,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                ring_position=ring_position,
                                gc_wg_distance=-ring_position[1] - ring_radius - 50 - bend_radius * 2 - waveguide_spacing * 4 * i,
                                ring_wg_distance=bend_radius + 50,
                                bend_radius=bend_radius,
                                gc_spacing=fibre_array_pich,
                                waveguide_spacing=waveguide_spacing
                                )

    #ring_gc_lo.visualize()

    chip_elements.append(i3.SRef(name=name, reference=ring_gc, position=(gc_position[0] + fibre_array_pich + fibre_array_pich * 4 * i, gc_position[1])))



#######################################
# 1. Sweep the coupling gap - 3rd row
######################################
coupling_gaps = [1.05, 1.1, 1.15]

gc_position = (700, 9250)  # Position of the first grating coupler

chip_elements.append(i3.SRef(name="wg_loop_3", reference=wg_loop_lo, position=gc_position))

ring = AddDropRingWithElectrode()
ring_lo = ring.Layout(ring_straight_length=straight_length,
                      coupler_spacing=coupling_gaps[0], # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length - 150,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_in_pos = ring_lo.ports['in'].position

first_ring_position = (-ring_in_pos[0] + bend_radius * 3 + 1065, -3750)


for i, gap in enumerate(coupling_gaps):
    name = "Ring_EG_{}G_{}".format(electrode_gap, gap)
    ring_gc = RingModulatorGC(name=name)
    ring_position = (first_ring_position[0] + ring_width * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_position[1])
    print("ring_position: {}".format(ring_position))
    ring_gc_lo = ring_gc.Layout(ring_radius=ring_radius,
                                ring_straight_length=straight_length,
                                coupler_spacing=gap,  # Coupler gap
                                coupler_straight_length=coupl_length,
                                coupler_positions=[-straight_length * 0.125 + coupl_length,
                                                   straight_length * 0.2 - coupl_length],
                                electrode_length=straight_length - 150,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                ring_position=ring_position,
                                gc_wg_distance=-ring_position[1] - ring_radius - 50 - bend_radius * 2 - waveguide_spacing * 4 * i,
                                ring_wg_distance=bend_radius + 50,
                                bend_radius=bend_radius,
                                gc_spacing=fibre_array_pich,
                                waveguide_spacing=waveguide_spacing
                                )

    #ring_gc_lo.visualize()

    chip_elements.append(i3.SRef(name=name, reference=ring_gc, position=(gc_position[0] + fibre_array_pich + fibre_array_pich * 4 * i, gc_position[1])))


second_half = i3.LayoutCell(name="Second_Half")
second_half_layout = second_half.Layout(elements=chip_elements)


####################################
# Generate the main layout
####################################
chip_design = i3.LayoutCell()
chip_layout = chip_design.Layout(elements=[i3.SRef(name="E_GAP_7um", reference=first_half_layout, position=(0, 0)),
                                           i3.SRef(name="E_GAP_10um", reference=second_half_layout, transformation=i3.VMirror() + i3.Translation(translation=(0, 10000)))
                                           ])
chip_layout.write_gdsii("gds_output/ring_modulators_v2.0.gds")