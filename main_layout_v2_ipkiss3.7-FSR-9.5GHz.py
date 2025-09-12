import sys

# Need to update the folder that contains asp_sin_lnoi_photonics/ipkiss


sys.path.append("C:/luceda/PDKs/asp_sin_lnoi_photonics-master/ipkiss")
sys.path.append("H:/GitHub/asp_sin_lnoi_photonics/ipkiss")

import asp_sin_lnoi_photonics.technology
import asp_sin_lnoi_photonics.all as asp
import ipkiss3.all as i3
import numpy as np

from ring_gc.cell import RingModulatorGC
from ring_gc_h.cell import RingModulatorGCHiep
from ring_gc_h_5.cell import RingModulatorGCHiep5
from ring_gc_h_6.cell import RingModulatorGCHiep6
from ring_gc_h_7.cell import RingModulatorGCHiep7
from ring_modulator.cell import AddDropRingWithElectrode
from waveguide_loop.cell import WaveguideLoop
from waveguide_h_5.cell import WaveguideHiep5
from waveguide_h_6.cell import WaveguideHiep6

#######################################
# Global parameters
######################################
waveguide_spacing = 75 # spacing between adjacent waveguides
bend_radius = 200  # Bending radius used in waveguide routing
hot_electrode_width = 23
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

fsr_2 = 9.5 # in GHz

straight_length = ring_straight_length(ring_radius, ng, fsr)
ring_width = straight_length + ring_radius * 2

straight_length_2 = ring_straight_length(ring_radius, ng, fsr_2)
ring_width_2 = straight_length_2 + ring_radius *2

print("Ring straight length: {}".format(straight_length))

print("Ring straight length FSR-9.5GHz: {}".format(straight_length_2))

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
wg_loop = WaveguideLoop(name="wg_loop", spacing=fibre_array_pich *16, bend_radius=150)
wg_loop_lo = wg_loop.Layout()

# Waveguide Hiep          # Added
wg_hiep = WaveguideHiep5(name="wg_hiep", spacing=fibre_array_pich *16, bend_radius=150) # Added
wg_hiep_lo = wg_hiep.Layout() # Added

######################################
# I. First half electrode gap: 6um
#####################################
electrode_gap = 6

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
coupling_gaps = [0.85, 0.75]

change = 150
moving = 250 + change
gc_position = (3130 + moving, 9250)  # Position of the first grating coupler

#gc_position = (3130 + 127 * 2, 9250)  # Position of the first grating coupler #Modified

# Waveguide loop
wg_loop_1 = WaveguideLoop(name="wg_loop_1", spacing=fibre_array_pich *11, bend_radius=150)
wg_loop_lo_1 = wg_loop_1.Layout()

chip_elements.append(i3.SRef(name="wg_loop_1", reference=wg_loop_lo_1, position=gc_position))

# Waveguide Hiep # Added
wg_hiep = WaveguideHiep5(name="wg_hiep", spacing=fibre_array_pich *10, bend_radius=200) # Added
wg_hiep_lo = wg_hiep.Layout() # Added

chip_elements.append(i3.SRef(name="wg_hiep", reference=wg_hiep_lo, position=gc_position)) # Added

ring = AddDropRingWithElectrode()

ring_lo = ring.Layout(ring_straight_length=straight_length,
                      coupler_spacing=coupling_gaps[0], # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length - 150,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_in_pos = ring_lo.ports['in'].position

first_ring_position = (-ring_in_pos[0] + bend_radius + 50 - 200, -1850 + 50)


ring_9_5_GHz = AddDropRingWithElectrode()

ring_9_5_GHz_lo = ring_9_5_GHz.Layout(ring_straight_length=straight_length_2,
                      coupler_spacing=coupling_gaps[0], # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length_2 - 150,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_9_5_GHz_in_pos = ring_9_5_GHz_lo.ports['in'].position

first_ring_9_5_GHz_position = (-ring_9_5_GHz_in_pos[0] + bend_radius - 2390, -1850 + 50)



# First ring
i = 0
gap = coupling_gaps[0]
ring_position = (first_ring_position[0] + ring_width * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_position[1])
name = "Ring_EG_{}G_{}".format(electrode_gap, gap)
ring_gc_h = RingModulatorGCHiep7(name=name,
                              ring_position=ring_position,
                                gc_wg_distance=-ring_position[1] - ring_radius - 50 - bend_radius * 2 - waveguide_spacing * 4 * i,
                                ring_wg_distance=bend_radius + 50,
                                bend_radius=bend_radius,
                                gc_spacing=fibre_array_pich,
                                waveguide_spacing=waveguide_spacing)
print("ring_position: {}".format(ring_position))
ring_gc_lo_h = ring_gc_h.Layout(ring_radius=ring_radius,
                                ring_straight_length=straight_length,
                                coupler_spacing=gap,  # Coupler gap
                                coupler_straight_length=coupl_length,
                                coupler_positions=[-straight_length * 0.125 + coupl_length,
                                                   straight_length * 0.2 + 100 - coupl_length],
                                electrode_length=straight_length - 150,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                with_label=True,
                                label_position=ring_position,
                                label_angle=0,
                                coupler_gap_Hiep=gap,
                                electrode_gap_Hiep=electrode_gap
                                )

chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich + fibre_array_pich * 4 * i, gc_position[1])))  # Modified

# Second ring
i = 1
gap = coupling_gaps[1]
ring_position = (first_ring_9_5_GHz_position[0] + ring_width_2 * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_position[1])
name = "Ring_9_5GHz_EG_{}G_{}".format(electrode_gap, gap)
ring_gc_h = RingModulatorGCHiep(name=name,
                              ring_position=ring_position,
                                gc_wg_distance=-ring_position[1] - ring_radius - 50 - bend_radius * 2 - waveguide_spacing * 4 * i,
                                ring_wg_distance=bend_radius + 50,
                                bend_radius=bend_radius,
                                gc_spacing=fibre_array_pich,
                                waveguide_spacing=waveguide_spacing)
print("ring_position: {}".format(ring_position))
ring_gc_lo_h = ring_gc_h.Layout(ring_radius=ring_radius,
                                ring_straight_length=straight_length_2,
                                coupler_spacing=gap,  # Coupler gap
                                coupler_straight_length=coupl_length,
                                coupler_positions=[-straight_length_2 * 0.125 - 510 + coupl_length,
                                                   straight_length_2 * 0.2 - 600 - coupl_length],
                                electrode_length=straight_length_2 - 150,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                with_label=True,
                                label_position=ring_position,
                                label_angle=0,
                                coupler_gap_Hiep=gap,
                                electrode_gap_Hiep=electrode_gap
                                )



chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich + fibre_array_pich * 4 * i, gc_position[1])))  # Modified

#ring_gc_lo.visualize()





#######################################
# 1. Sweep the coupling gap - 3rd row
######################################
coupling_gaps = [0.9, 0.8]

moving = 635
gc_position = (700 + moving, 9250)  # Position of the first grating coupler

wg_loop_2 = WaveguideLoop(name="wg_loop_2", spacing=fibre_array_pich * 11, bend_radius=150) #Modified
wg_loop_lo_2 = wg_loop_2.Layout()

chip_elements.append(i3.SRef(name="wg_loop_2", reference=wg_loop_lo_2, position=gc_position))

# Waveguide Hiep # Added
wg_hiep_2 = WaveguideHiep6(name="wg_hiep_2", spacing=fibre_array_pich *10, bend_radius=200) # Added
wg_hiep_lo_2 = wg_hiep_2.Layout() # Added

chip_elements.append(i3.SRef(name="wg_hiep_2", reference=wg_hiep_lo_2, position=gc_position)) # Added

ring = AddDropRingWithElectrode()
ring_lo = ring.Layout(ring_straight_length=straight_length,
                      coupler_spacing=coupling_gaps[0], # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length - 150,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_in_pos = ring_lo.ports['in'].position

first_ring_position = (-ring_in_pos[0] + bend_radius * 3 + 900, -3750)

ring_9_5_GHz = AddDropRingWithElectrode()

ring_9_5_GHz_lo = ring_9_5_GHz.Layout(ring_straight_length=straight_length_2,
                      coupler_spacing=coupling_gaps[0], # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length_2 - 150,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_9_5_GHz_in_pos = ring_9_5_GHz_lo.ports['in'].position

first_ring_9_5_GHz_position = (-ring_9_5_GHz_in_pos[0] + bend_radius - 400, -3750)

# First ring

i = 0
gap = coupling_gaps[0]
ring_position = (first_ring_position[0] + ring_width * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_position[1])
name = "Ring_EG_{}G_{}".format(electrode_gap, gap)
ring_gc = RingModulatorGCHiep5(name=name,
                              ring_position=ring_position,
                              gc_wg_distance=-ring_position[
                                  1] - ring_radius - 100 - bend_radius * 2 - waveguide_spacing * 4 * i,
                              ring_wg_distance=bend_radius + 50,
                              bend_radius=bend_radius,
                              gc_spacing=fibre_array_pich,
                              waveguide_spacing=waveguide_spacing
                              )
print("ring_position: {}".format(ring_position))
ring_gc_lo = ring_gc.Layout(ring_radius=ring_radius,
                                ring_straight_length=straight_length,
                                coupler_spacing=gap,  # Coupler gap
                                coupler_straight_length=coupl_length,
                                coupler_positions=[-straight_length * 0.125 + 100 + coupl_length,
                                                   straight_length * 0.2 + 175 - coupl_length],
                                electrode_length=straight_length - 150,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                with_label=True,
                                label_position=ring_position,
                                label_angle=0,
                                coupler_gap_Hiep=gap,
                                electrode_gap_Hiep=electrode_gap

                                )

#ring_gc_lo.visualize()

chip_elements.append(i3.SRef(name=name, reference=ring_gc, position=(gc_position[0] - moving + fibre_array_pich + fibre_array_pich * 4 * i, gc_position[1])))

# Second ring

i = 1
gap = coupling_gaps[1]
ring_position = (first_ring_9_5_GHz_position[0] + ring_width_2 * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_position[1])
name = "Ring_9_5GHz_EG_{}G_{}".format(electrode_gap, gap)
ring_gc_h = RingModulatorGCHiep6(name=name,
                              ring_position=ring_position,
                                gc_wg_distance=-ring_position[1] - ring_radius - 50 - bend_radius * 2 - waveguide_spacing * 4 * i,
                                ring_wg_distance=bend_radius + 50,
                                bend_radius=bend_radius,
                                gc_spacing=fibre_array_pich,
                                waveguide_spacing=waveguide_spacing)
print("ring_position: {}".format(ring_position))
ring_gc_lo_h = ring_gc_h.Layout(ring_radius=ring_radius,
                                ring_straight_length=straight_length_2,
                                coupler_spacing=gap,  # Coupler gap
                                coupler_straight_length=coupl_length,
                                coupler_positions=[-straight_length_2 * 0.125 - 100 + coupl_length,
                                                   straight_length_2 * 0.2 - 150 - coupl_length],
                                electrode_length=straight_length_2 - 150,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                with_label=True,
                                label_position=ring_position,
                                label_angle=0,
                                coupler_gap_Hiep=gap,
                                electrode_gap_Hiep=electrode_gap
                                )

#ring_gc_lo.visualize()

chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich + fibre_array_pich * 4 * i, gc_position[1])))


# First
#i = 0
#gap = coupling_gaps[0]
#ring_position = (first_ring_position[0] + ring_width * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_position[1])
#name = "Ring_EG_{}G_{}".format(electrode_gap, gap)
#ring_gc_h2_1 = RingModulatorGCHiep2(name=name,
#                              ring_position=ring_position,
#                                gc_wg_distance=-ring_position[1] - ring_radius - 50 - bend_radius * 2 - waveguide_spacing * 4 * i,
#                                ring_wg_distance=bend_radius + 50,
#                                bend_radius=bend_radius,
#                                gc_spacing=fibre_array_pich,
#                                waveguide_spacing=waveguide_spacing)
#print("ring_position: {}".format(ring_position))
#ring_gc_lo_h2_1 = ring_gc_h2_1.Layout(ring_radius=ring_radius,
#                                ring_straight_length=straight_length,
#                                coupler_spacing=gap,  # Coupler gap
#                                coupler_straight_length=coupl_length,
#                                coupler_positions=[-straight_length * 0.125 - 50 + coupl_length,
#                                                   straight_length * 0.2 - coupl_length],
#                                electrode_length=straight_length - 150,
#                                hot_width=hot_electrode_width,
#                                electrode_gap=electrode_gap,

#                                )

#chip_elements.append(i3.SRef(name=name, reference=ring_gc_h2_1, position=(gc_position[0] + moving + fibre_array_pich + fibre_array_pich * 4 * i, gc_position[1])))


    #ring_gc_lo.visualize()


first_half = i3.LayoutCell()
first_half_layout = first_half.Layout(elements=chip_elements)



######################################
# II. Second half electrode gap: 9um
#####################################
electrode_gap = 6
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
coupling_gaps = [0.95, 0.85]

change = 150
moving = 250 + change
gc_position = (3130 + moving, 9250)  # Position of the first grating coupler

# Waveguide loop
wg_loop_1 = WaveguideLoop(name="wg_loop_1", spacing=fibre_array_pich *11, bend_radius=150)
wg_loop_lo_1 = wg_loop_1.Layout()

chip_elements.append(i3.SRef(name="wg_loop_1", reference=wg_loop_lo_1, position=gc_position))

# Waveguide Hiep # Added
wg_hiep = WaveguideHiep5(name="wg_hiep", spacing=fibre_array_pich *10, bend_radius=200) # Added
wg_hiep_lo = wg_hiep.Layout() # Added

chip_elements.append(i3.SRef(name="wg_hiep", reference=wg_hiep_lo, position=gc_position)) # Added


ring = AddDropRingWithElectrode()

ring_lo = ring.Layout(ring_straight_length=straight_length,
                      coupler_spacing=coupling_gaps[0], # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length - 150,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_in_pos = ring_lo.ports['in'].position

first_ring_position = (-ring_in_pos[0] + bend_radius + 50 - 200, -1850 + 50)


ring_9_5_GHz = AddDropRingWithElectrode()

ring_9_5_GHz_lo = ring_9_5_GHz.Layout(ring_straight_length=straight_length_2,
                      coupler_spacing=coupling_gaps[0], # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length_2 - 150,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_9_5_GHz_in_pos = ring_9_5_GHz_lo.ports['in'].position

first_ring_9_5_GHz_position = (-ring_9_5_GHz_in_pos[0] + bend_radius - 2390, -1850 + 50)
# First ring
i = 0
gap = coupling_gaps[0]
ring_position = (first_ring_position[0] + ring_width * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_position[1])
name = "Ring_EG_{}G_{}".format(electrode_gap, gap)
ring_gc_h = RingModulatorGCHiep7(name=name,
                              ring_position=ring_position,
                                gc_wg_distance=-ring_position[1] - ring_radius - 50 - bend_radius * 2 - waveguide_spacing * 4 * i,
                                ring_wg_distance=bend_radius + 50,
                                bend_radius=bend_radius,
                                gc_spacing=fibre_array_pich,
                                waveguide_spacing=waveguide_spacing)
print("ring_position: {}".format(ring_position))
ring_gc_lo_h = ring_gc_h.Layout(ring_radius=ring_radius,
                                ring_straight_length=straight_length,
                                coupler_spacing=gap,  # Coupler gap
                                coupler_straight_length=coupl_length,
                                coupler_positions=[-straight_length * 0.125 + coupl_length,
                                                   straight_length * 0.2 + 100 - coupl_length],
                                electrode_length=straight_length - 150,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                with_label=True,
                                label_position=ring_position,
                                label_angle=0,
                                coupler_gap_Hiep=gap,
                                electrode_gap_Hiep=electrode_gap
                                )

chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich + fibre_array_pich * 4 * i, gc_position[1])))  # Modified

# Second ring
i = 1
gap = coupling_gaps[1]
ring_position = (first_ring_9_5_GHz_position[0] + ring_width_2 * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_position[1])
name = "Ring_9_5GHz_EG_{}G_{}".format(electrode_gap, gap)
ring_gc_h = RingModulatorGCHiep(name=name,
                              ring_position=ring_position,
                                gc_wg_distance=-ring_position[1] - ring_radius - 50 - bend_radius * 2 - waveguide_spacing * 4 * i,
                                ring_wg_distance=bend_radius + 50,
                                bend_radius=bend_radius,
                                gc_spacing=fibre_array_pich,
                                waveguide_spacing=waveguide_spacing)
print("ring_position: {}".format(ring_position))
ring_gc_lo_h = ring_gc_h.Layout(ring_radius=ring_radius,
                                ring_straight_length=straight_length_2,
                                coupler_spacing=gap,  # Coupler gap
                                coupler_straight_length=coupl_length,
                                coupler_positions=[-straight_length_2 * 0.125 - 510 + coupl_length,
                                                   straight_length_2 * 0.2 - 600 - coupl_length],
                                electrode_length=straight_length_2 - 150,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                with_label=True,
                                label_position=ring_position,
                                label_angle=0,
                                coupler_gap_Hiep=gap,
                                electrode_gap_Hiep=electrode_gap
                                )



chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich + fibre_array_pich * 4 * i, gc_position[1])))  # Modified

    #ring_gc_lo.visualize()




#######################################
# 1. Sweep the coupling gap - 3rd row
######################################
coupling_gaps = [1.0, 0.90]

moving = 635
gc_position = (700 + moving, 9250)  # Position of the first grating coupler

wg_loop_2 = WaveguideLoop(name="wg_loop_2", spacing=fibre_array_pich * 11, bend_radius=150) #Modified
wg_loop_lo_2 = wg_loop_2.Layout()

chip_elements.append(i3.SRef(name="wg_loop_2", reference=wg_loop_lo_2, position=gc_position))

# Waveguide Hiep # Added
wg_hiep_2 = WaveguideHiep6(name="wg_hiep_2", spacing=fibre_array_pich *10, bend_radius=200) # Added
wg_hiep_lo_2 = wg_hiep_2.Layout() # Added

chip_elements.append(i3.SRef(name="wg_hiep_2", reference=wg_hiep_lo_2, position=gc_position)) # Added

ring = AddDropRingWithElectrode()
ring_lo = ring.Layout(ring_straight_length=straight_length,
                      coupler_spacing=coupling_gaps[0], # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length - 150,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_in_pos = ring_lo.ports['in'].position

first_ring_position = (-ring_in_pos[0] + bend_radius * 3 + 900, -3750)

ring_9_5_GHz = AddDropRingWithElectrode()

ring_9_5_GHz_lo = ring_9_5_GHz.Layout(ring_straight_length=straight_length_2,
                      coupler_spacing=coupling_gaps[0], # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length_2 - 150,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_9_5_GHz_in_pos = ring_9_5_GHz_lo.ports['in'].position

first_ring_9_5_GHz_position = (-ring_9_5_GHz_in_pos[0] + bend_radius - 400, -3750)

# First ring

i = 0
gap = coupling_gaps[0]
ring_position = (first_ring_position[0] + ring_width * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_position[1])
name = "Ring_EG_{}G_{}".format(electrode_gap, gap)
ring_gc = RingModulatorGCHiep5(name=name,
                              ring_position=ring_position,
                              gc_wg_distance=-ring_position[
                                  1] - ring_radius - 100 - bend_radius * 2 - waveguide_spacing * 4 * i,
                              ring_wg_distance=bend_radius + 50,
                              bend_radius=bend_radius,
                              gc_spacing=fibre_array_pich,
                              waveguide_spacing=waveguide_spacing
                              )
print("ring_position: {}".format(ring_position))
ring_gc_lo = ring_gc.Layout(ring_radius=ring_radius,
                                ring_straight_length=straight_length,
                                coupler_spacing=gap,  # Coupler gap
                                coupler_straight_length=coupl_length,
                                coupler_positions=[-straight_length * 0.125 + 100 + coupl_length,
                                                   straight_length * 0.2 + 175 - coupl_length],
                                electrode_length=straight_length - 150,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                with_label=True,
                                label_position=ring_position,
                                label_angle=0,
                                coupler_gap_Hiep=gap,
                                electrode_gap_Hiep=electrode_gap

                                )

#ring_gc_lo.visualize()

chip_elements.append(i3.SRef(name=name, reference=ring_gc, position=(gc_position[0] - moving + fibre_array_pich + fibre_array_pich * 4 * i, gc_position[1])))

# Second ring

i = 1
gap = coupling_gaps[1]
ring_position = (first_ring_9_5_GHz_position[0] + ring_width_2 * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_position[1])
name = "Ring_9_5GHz_EG_{}G_{}".format(electrode_gap, gap)
ring_gc_h = RingModulatorGCHiep6(name=name,
                              ring_position=ring_position,
                                gc_wg_distance=-ring_position[1] - ring_radius - 50 - bend_radius * 2 - waveguide_spacing * 4 * i,
                                ring_wg_distance=bend_radius + 50,
                                bend_radius=bend_radius,
                                gc_spacing=fibre_array_pich,
                                waveguide_spacing=waveguide_spacing)
print("ring_position: {}".format(ring_position))
ring_gc_lo_h = ring_gc_h.Layout(ring_radius=ring_radius,
                                ring_straight_length=straight_length_2,
                                coupler_spacing=gap,  # Coupler gap
                                coupler_straight_length=coupl_length,
                                coupler_positions=[-straight_length_2 * 0.125 - 100 + coupl_length,
                                                   straight_length_2 * 0.2 - 150 - coupl_length],
                                electrode_length=straight_length_2 - 150,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                with_label=True,
                                label_position=ring_position,
                                label_angle=0,
                                coupler_gap_Hiep=gap,
                                electrode_gap_Hiep=electrode_gap
                                )

#ring_gc_lo.visualize()

chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich + fibre_array_pich * 4 * i, gc_position[1])))


#ring_gc_lo.visualize()

#chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich + fibre_array_pich * 4 * i, gc_position[1])))

second_half = i3.LayoutCell(name="Second_Half")
second_half_layout = second_half.Layout(elements=chip_elements)


####################################
# Generate the main layout
####################################
chip_design = i3.LayoutCell()
chip_layout = chip_design.Layout(elements=[i3.SRef(name="E_GAP_6um", reference=first_half_layout, position=(0, 0)),
                                           i3.SRef(name="E_GAP_9um", reference=second_half_layout, transformation=i3.VMirror() + i3.Translation(translation=(0, 10000)))
                                           ])
#chip_layout.write_gdsii("gds_output/ring_modulators_v2.0.gds")

chip_layout.write_gdsii("gds_output/ring_modulators_v2.0_FSR-9.5GHz_electrode_width-23.gds")