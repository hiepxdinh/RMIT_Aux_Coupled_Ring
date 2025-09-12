import sys

# Need to update the folder that contains asp_sin_lnoi_photonics/ipkiss


sys.path.append("C:/pdk/asp_sin_lnoi_photonics/ipkiss")
sys.path.append("H:/GitHub/asp_sin_lnoi_photonics/ipkiss")
sys.path.append("D:/RMITRaceHubDataHiepDX/PDKs/asp_sin_lnoi_photonics/ipkiss")
import asp_sin_lnoi_photonics.technology
import asp_sin_lnoi_photonics.all as asp
import ipkiss3.all as i3
import numpy as np

from ring_gc.cell import NotchRingGC
from ring_gc_h_with_auxiliary_ring_outside.cell import RingModulatorGCHiepAuxOutside
from ring_gc_h_with_auxiliary_ring_outside_19GHz.cell import RingModulatorGCHiepAuxOutside2
from ring_gc_h_with_auxiliary_ring_outside_2.cell import RingModulatorGCHiepAuxOutside_Top
from ring_gc_h_with_auxiliary_ring_outside_19GHz_2.cell import RingModulatorGCHiepAuxOutside2_Top
from ring_modulator.cell import AddDropRingWithElectrode

from ring_modulator_with_auxiliary_ring_outside.cell import AddDropRingWithAuxOutside
from waveguide_loop.cell import WaveguideLoop
from waveguide_h_5.cell import WaveguideHiep5



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

ring_radius_aux = 230

fsr = 19  # in GHz

fsr_2 = 9.5 # in GHz

fsr_aux= fsr*4 # in GHz

straight_length = ring_straight_length(ring_radius, ng, fsr)
ring_width = straight_length + ring_radius * 2

straight_length_2 = ring_straight_length(ring_radius, ng, fsr_2)
ring_width_2 = straight_length_2 + ring_radius *2

straight_length_aux = ring_straight_length(ring_radius_aux, ng, fsr_aux)
ring_width_aux = straight_length_aux + ring_radius_aux * 2

print("Ring straight length FSR-19GHz: {}".format(straight_length))

print("Ring straight length FSR-9.5GHz: {}".format(straight_length_2))

print("Ring straight length-auxiliary: {}".format(straight_length_aux))

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
coupling_gaps = [1.1, 1.1]
#######################################
# 1. Sweep the coupling gap - 2nd row
######################################
aux_coupling_gap = 0.95
change = 150
moving = 250 + change
gc_position = (3130 + moving, 9180-300)  # Position of the first grating coupler

# Waveguide loop
wg_loop_1 = WaveguideLoop(name="wg_loop_1", spacing=fibre_array_pich *11, bend_radius=150)
wg_loop_lo_1 = wg_loop_1.Layout()

chip_elements.append(i3.SRef(name="wg_loop_1", reference=wg_loop_lo_1, position=gc_position))

# Waveguide Hiep # Added
wg_hiep = WaveguideHiep5(name="wg_hiep", spacing=fibre_array_pich *10, bend_radius=200) # Added
wg_hiep_lo = wg_hiep.Layout() # Added

#chip_elements.append(i3.SRef(name="wg_hiep2", reference=wg_hiep_lo, position=gc_position)) # Added

ring = AddDropRingWithElectrode()

ring_lo = ring.Layout(ring_straight_length=straight_length,
                      coupler_spacing=coupling_gaps[0], # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length - 150,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_in_pos = ring_lo.ports['in'].position

first_ring_position = (-ring_in_pos[0] + bend_radius + 50 - 800-530, -1500-50 - 29.5)


ring_9_5_GHz = AddDropRingWithAuxOutside()

ring_9_5_GHz_lo = ring_9_5_GHz.Layout(ring_straight_length=straight_length_2,
                      coupler_spacing=coupling_gaps[1], # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length_2 - 150,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_9_5_GHz_in_pos = ring_9_5_GHz_lo.ports['in'].position

first_ring_9_5_GHz_position = (-ring_9_5_GHz_in_pos[0] + bend_radius - 2800, -1500-50 - 29.5)

#First ring
i = 0
gap = coupling_gaps[0]
ring_position = (first_ring_position[0] + ring_width_2 * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_position[1])
name = "Ring_19GHz_EG_{}G_{}_AUX_G_{}".format(electrode_gap, gap,aux_coupling_gap)
ring_gc_h = RingModulatorGCHiepAuxOutside2_Top(name=name,
                                ring_position=ring_position,
                                gc_wg_distance=-ring_position[1] - ring_radius - 50 - bend_radius * 2 - waveguide_spacing * 4 * i,
                                ring_wg_distance=bend_radius + 50,
                                bend_radius=bend_radius,
                                gc_spacing=fibre_array_pich,
                                waveguide_spacing=waveguide_spacing)
print("ring_position: {}".format(ring_position))
ring_gc_lo_h = ring_gc_h.Layout(aux_coupling_gap = aux_coupling_gap,
                                ring_radius=ring_radius,
                                ring_radius_aux=ring_radius_aux,
                                ring_straight_length=straight_length,
                                ring_straight_length_aux=straight_length_aux,
                                coupler_spacing=gap,  # Coupler gap
                                coupler_straight_length=coupl_length,
                                coupler_positions=[-straight_length * 0.125 + 500 + coupl_length,
                                                   straight_length * 0.2 + 450 - coupl_length],
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
ring_position = (first_ring_9_5_GHz_position[0] + ring_width_2 * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_9_5_GHz_position[1])
name = "Ring_9_5GHz_EG_{}G_{}_AUX_G_{}".format(electrode_gap, gap,aux_coupling_gap)
ring_gc_h = RingModulatorGCHiepAuxOutside_Top(name=name,
                              ring_position=ring_position,
                                gc_wg_distance=-ring_position[1] - ring_radius - 50 - bend_radius * 2 - waveguide_spacing * 4 * i,
                                ring_wg_distance=bend_radius + 50,
                                bend_radius=bend_radius,
                                gc_spacing=fibre_array_pich,
                                waveguide_spacing=waveguide_spacing)
print("ring_position: {}".format(ring_position))
ring_gc_lo_h = ring_gc_h.Layout(aux_coupling_gap = aux_coupling_gap,
                                ring_radius=ring_radius,
                                ring_radius_aux=ring_radius_aux,
                                ring_straight_length=straight_length_2,
                                ring_straight_length_aux=straight_length_aux,
                                coupler_spacing=gap,  # Coupler gap
                                coupler_straight_length=coupl_length,
                                coupler_positions=[-straight_length_2 * 0.125 - 510-730+110 + coupl_length,
                                                   straight_length_2 * 0.2 - 600 -730+150 - coupl_length],
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

##########################################
# Second row
##########################################
#######################################
# 1. Sweep the coupling gap - 2nd row
######################################
coupling_gaps = [1.1, 1.1]
aux_coupling_gap = 1.0
change = 150
moving = 250 + change
gc_position = (3130 + moving, 9180-2300-17.5-50)  # Position of the first grating coupler

# Waveguide loop
wg_loop_1 = WaveguideLoop(name="wg_loop_1", spacing=fibre_array_pich *11, bend_radius=150)
wg_loop_lo_1 = wg_loop_1.Layout()

chip_elements.append(i3.SRef(name="wg_loop_1", reference=wg_loop_lo_1, position=gc_position))

# Waveguide Hiep # Added
wg_hiep = WaveguideHiep5(name="wg_hiep", spacing=fibre_array_pich *10, bend_radius=200) # Added
wg_hiep_lo = wg_hiep.Layout() # Added

#chip_elements.append(i3.SRef(name="wg_hiep2", reference=wg_hiep_lo, position=gc_position)) # Added

ring = AddDropRingWithElectrode()

ring_lo = ring.Layout(ring_straight_length=straight_length,
                      coupler_spacing=coupling_gaps[0], # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length - 150,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_in_pos = ring_lo.ports['in'].position

first_ring_position = (-ring_in_pos[0] + bend_radius + 50 - 800-530, -1500-50 - 29.5+50)


ring_9_5_GHz = AddDropRingWithAuxOutside()

ring_9_5_GHz_lo = ring_9_5_GHz.Layout(ring_straight_length=straight_length_2,
                      coupler_spacing=coupling_gaps[1], # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length_2 - 150,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_9_5_GHz_in_pos = ring_9_5_GHz_lo.ports['in'].position

first_ring_9_5_GHz_position = (-ring_9_5_GHz_in_pos[0] + bend_radius - 2800, -1500-50 - 29.5+50)

#First ring
i = 0
gap = coupling_gaps[0]
ring_position = (first_ring_position[0] + ring_width_2 * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_position[1])
name = "Ring_19GHz_EG_{}G_{}_AUX_G_{}".format(electrode_gap, gap,aux_coupling_gap)
ring_gc_h = RingModulatorGCHiepAuxOutside2(name=name,
                                ring_position=ring_position,
                                gc_wg_distance=-ring_position[1] - ring_radius - 50 - bend_radius * 2 - waveguide_spacing * 4 * i,
                                ring_wg_distance=bend_radius + 50,
                                bend_radius=bend_radius,
                                gc_spacing=fibre_array_pich,
                                waveguide_spacing=waveguide_spacing)
print("ring_position: {}".format(ring_position))
ring_gc_lo_h = ring_gc_h.Layout(aux_coupling_gap = aux_coupling_gap,
                                ring_radius=ring_radius,
                                ring_radius_aux=ring_radius_aux,
                                ring_straight_length=straight_length,
                                ring_straight_length_aux=straight_length_aux,
                                coupler_spacing=gap,  # Coupler gap
                                coupler_straight_length=coupl_length,
                                coupler_positions=[-straight_length * 0.125 + 500 + coupl_length,
                                                   straight_length * 0.2 + 450 - coupl_length],
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
ring_position = (first_ring_9_5_GHz_position[0] + ring_width_2 * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_9_5_GHz_position[1])
name = "Ring_9_5GHz_EG_{}G_{}_AUX_G_{}".format(electrode_gap, gap,aux_coupling_gap)
ring_gc_h = RingModulatorGCHiepAuxOutside(name=name,
                              ring_position=ring_position,
                                gc_wg_distance=-ring_position[1] - ring_radius - 50 - bend_radius * 2 - waveguide_spacing * 4 * i,
                                ring_wg_distance=bend_radius + 50,
                                bend_radius=bend_radius,
                                gc_spacing=fibre_array_pich,
                                waveguide_spacing=waveguide_spacing)
print("ring_position: {}".format(ring_position))
ring_gc_lo_h = ring_gc_h.Layout(aux_coupling_gap = aux_coupling_gap,
                                ring_radius=ring_radius,
                                ring_radius_aux=ring_radius_aux,
                                ring_straight_length=straight_length_2,
                                ring_straight_length_aux=straight_length_aux,
                                coupler_spacing=gap,  # Coupler gap
                                coupler_straight_length=coupl_length,
                                coupler_positions=[-straight_length_2 * 0.125 - 510-730+110 + coupl_length,
                                                   straight_length_2 * 0.2 - 600 -730+150 - coupl_length],
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


###########################################

first_half = i3.LayoutCell()
first_half_layout = first_half.Layout(elements=chip_elements)



######################################
# II. Second half electrode gap: 9um
#####################################
electrode_gap = 6
chip_elements = []
#######################################
# 1. Sweep the coupling gap - 2nd row
coupling_gaps = [1.1, 1.1]
aux_coupling_gap = 1.05
change = 150
moving = 250 + change
gc_position = (3130 + moving, 9180-300)  # Position of the first grating coupler

# Waveguide loop
wg_loop_1 = WaveguideLoop(name="wg_loop_1", spacing=fibre_array_pich *11, bend_radius=150)
wg_loop_lo_1 = wg_loop_1.Layout()

chip_elements.append(i3.SRef(name="wg_loop_1", reference=wg_loop_lo_1, position=gc_position))

# Waveguide Hiep # Added
wg_hiep = WaveguideHiep5(name="wg_hiep", spacing=fibre_array_pich *10, bend_radius=200) # Added
wg_hiep_lo = wg_hiep.Layout() # Added

#chip_elements.append(i3.SRef(name="wg_hiep2", reference=wg_hiep_lo, position=gc_position)) # Added

ring = AddDropRingWithElectrode()

ring_lo = ring.Layout(ring_straight_length=straight_length,
                      coupler_spacing=coupling_gaps[0], # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length - 150,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_in_pos = ring_lo.ports['in'].position

first_ring_position = (-ring_in_pos[0] + bend_radius + 50 - 800-530, -1500-50 - 29.5)


ring_9_5_GHz = AddDropRingWithAuxOutside()

ring_9_5_GHz_lo = ring_9_5_GHz.Layout(ring_straight_length=straight_length_2,
                      coupler_spacing=coupling_gaps[1], # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length_2 - 150,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_9_5_GHz_in_pos = ring_9_5_GHz_lo.ports['in'].position

first_ring_9_5_GHz_position = (-ring_9_5_GHz_in_pos[0] + bend_radius - 2800, -1500-50 - 29.5)

#First ring
i = 0
gap = coupling_gaps[0]
ring_position = (first_ring_position[0] + ring_width_2 * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_position[1])
name = "Ring_19GHz_EG_{}G_{}_AUX_G_{}".format(electrode_gap, gap,aux_coupling_gap)
ring_gc_h = RingModulatorGCHiepAuxOutside2_Top(name=name,
                                ring_position=ring_position,
                                gc_wg_distance=-ring_position[1] - ring_radius - 50 - bend_radius * 2 - waveguide_spacing * 4 * i,
                                ring_wg_distance=bend_radius + 50,
                                bend_radius=bend_radius,
                                gc_spacing=fibre_array_pich,
                                waveguide_spacing=waveguide_spacing)
print("ring_position: {}".format(ring_position))
ring_gc_lo_h = ring_gc_h.Layout(aux_coupling_gap = aux_coupling_gap,
                                ring_radius=ring_radius,
                                ring_radius_aux=ring_radius_aux,
                                ring_straight_length=straight_length,
                                ring_straight_length_aux=straight_length_aux,
                                coupler_spacing=gap,  # Coupler gap
                                coupler_straight_length=coupl_length,
                                coupler_positions=[-straight_length * 0.125 + 500 + coupl_length,
                                                   straight_length * 0.2 + 450 - coupl_length],
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
ring_position = (first_ring_9_5_GHz_position[0] + ring_width_2 * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_9_5_GHz_position[1])
name = "Ring_9_5GHz_EG_{}G_{}_AUX_G_{}".format(electrode_gap, gap,aux_coupling_gap)
ring_gc_h = RingModulatorGCHiepAuxOutside_Top(name=name,
                              ring_position=ring_position,
                                gc_wg_distance=-ring_position[1] - ring_radius - 50 - bend_radius * 2 - waveguide_spacing * 4 * i,
                                ring_wg_distance=bend_radius + 50,
                                bend_radius=bend_radius,
                                gc_spacing=fibre_array_pich,
                                waveguide_spacing=waveguide_spacing)
print("ring_position: {}".format(ring_position))
ring_gc_lo_h = ring_gc_h.Layout(aux_coupling_gap = aux_coupling_gap,
                                ring_radius=ring_radius,
                                ring_radius_aux=ring_radius_aux,
                                ring_straight_length=straight_length_2,
                                ring_straight_length_aux=straight_length_aux,
                                coupler_spacing=gap,  # Coupler gap
                                coupler_straight_length=coupl_length,
                                coupler_positions=[-straight_length_2 * 0.125 - 510-730+110 + coupl_length,
                                                   straight_length_2 * 0.2 - 600 -730+150 - coupl_length],
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

##########################################
# Second row
##########################################
#######################################
# 1. Sweep the coupling gap - 2nd row
######################################
coupling_gaps = [1.1, 1.1]
aux_coupling_gap = 1.1
change = 150
moving = 250 + change
gc_position = (3130 + moving, 9180-2300-17.5-50)   # Position of the first grating coupler

# Waveguide loop
wg_loop_1 = WaveguideLoop(name="wg_loop_1", spacing=fibre_array_pich *11, bend_radius=150)
wg_loop_lo_1 = wg_loop_1.Layout()

chip_elements.append(i3.SRef(name="wg_loop_1", reference=wg_loop_lo_1, position=gc_position))

# Waveguide Hiep # Added
wg_hiep = WaveguideHiep5(name="wg_hiep", spacing=fibre_array_pich *10, bend_radius=200) # Added
wg_hiep_lo = wg_hiep.Layout() # Added

#chip_elements.append(i3.SRef(name="wg_hiep2", reference=wg_hiep_lo, position=gc_position)) # Added

ring = AddDropRingWithElectrode()

ring_lo = ring.Layout(ring_straight_length=straight_length,
                      coupler_spacing=coupling_gaps[0], # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length - 150,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_in_pos = ring_lo.ports['in'].position

first_ring_position = (-ring_in_pos[0] + bend_radius + 50 - 800-530, -1500-50 - 29.5 +50)


ring_9_5_GHz = AddDropRingWithAuxOutside()

ring_9_5_GHz_lo = ring_9_5_GHz.Layout(ring_straight_length=straight_length_2,
                      coupler_spacing=coupling_gaps[1], # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length_2 - 150,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_9_5_GHz_in_pos = ring_9_5_GHz_lo.ports['in'].position

first_ring_9_5_GHz_position = (-ring_9_5_GHz_in_pos[0] + bend_radius - 2800, -1500-50 - 29.5 +50)

#First ring
i = 0
gap = coupling_gaps[0]
ring_position = (first_ring_position[0] + ring_width_2 * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_position[1])
name = "Ring_19GHz_EG_{}G_{}_AUX_G_{}".format(electrode_gap, gap,aux_coupling_gap)
ring_gc_h = RingModulatorGCHiepAuxOutside2(name=name,
                                ring_position=ring_position,
                                gc_wg_distance=-ring_position[1] - ring_radius - 50 - bend_radius * 2 - waveguide_spacing * 4 * i,
                                ring_wg_distance=bend_radius + 50,
                                bend_radius=bend_radius,
                                gc_spacing=fibre_array_pich,
                                waveguide_spacing=waveguide_spacing)
print("ring_position: {}".format(ring_position))
ring_gc_lo_h = ring_gc_h.Layout(aux_coupling_gap = aux_coupling_gap,
                                ring_radius=ring_radius,
                                ring_radius_aux=ring_radius_aux,
                                ring_straight_length=straight_length,
                                ring_straight_length_aux=straight_length_aux,
                                coupler_spacing=gap,  # Coupler gap
                                coupler_straight_length=coupl_length,
                                coupler_positions=[-straight_length * 0.125 + 500 + coupl_length,
                                                   straight_length * 0.2 + 450 - coupl_length],
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
ring_position = (first_ring_9_5_GHz_position[0] + ring_width_2 * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_9_5_GHz_position[1])
name = "Ring_9_5GHz_EG_{}G_{}_AUX_G_{}".format(electrode_gap, gap,aux_coupling_gap)
ring_gc_h = RingModulatorGCHiepAuxOutside(name=name,
                              ring_position=ring_position,
                                gc_wg_distance=-ring_position[1] - ring_radius - 50 - bend_radius * 2 - waveguide_spacing * 4 * i,
                                ring_wg_distance=bend_radius + 50,
                                bend_radius=bend_radius,
                                gc_spacing=fibre_array_pich,
                                waveguide_spacing=waveguide_spacing)
print("ring_position: {}".format(ring_position))
ring_gc_lo_h = ring_gc_h.Layout(aux_coupling_gap = aux_coupling_gap,
                                ring_radius=ring_radius,
                                ring_radius_aux=ring_radius_aux,
                                ring_straight_length=straight_length_2,
                                ring_straight_length_aux=straight_length_aux,
                                coupler_spacing=gap,  # Coupler gap
                                coupler_straight_length=coupl_length,
                                coupler_positions=[-straight_length_2 * 0.125 - 510-730+110 + coupl_length,
                                                   straight_length_2 * 0.2 - 600 -730+150 - coupl_length],
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





######################################
second_half = i3.LayoutCell(name="Second_Half")
second_half_layout = second_half.Layout(elements=chip_elements)


#######################################
# THIRD BLOCK
chip_elements = []
####################
aux_ring_gaps = [0.6, 0.65, 0.7, 0.75]
straight_lengths = straight_length_aux
ring_x_positions = 11500
y_positions = 8040
ring_radii = ring_radius_aux
waveguide_width = 1.0
gaps = 0.8
for i, aux_ring_gap in enumerate(aux_ring_gaps):
    name = "Ring_R{}_W{}_G{}_L{}_aux_g_{}".format(ring_radii, waveguide_width, gaps, straight_lengths, aux_ring_gap)
    ring_gc = NotchRingGC(name=name)
    ring_gc_lo = ring_gc.Layout(ring_radius=ring_radii,
                            straight_length=straight_lengths,
                            coupler_gap=gaps,
                            coupler_length=0.0,
                            waveguide_width=waveguide_width,
                            with_label=True,
                            aux_ring_gap=aux_ring_gap
                            )
    chip_elements.append(i3.SRef(name=name, reference=ring_gc_lo, position=(ring_x_positions, y_positions-i*2000 - int(i*0.5)*1000)))
    chip_elements.append(i3.SRef(name=name +"Flip", reference=ring_gc_lo, position=(ring_x_positions, y_positions-i*2000-int(i*0.5)*1000), transformation=i3.VMirror()+i3.Translation(translation=(0, 4*ring_radii+aux_ring_gap+waveguide_width))))


######################
third_block = i3.LayoutCell(name="Third_Block")
third_block_layout = third_block.Layout(elements=chip_elements)
####################################
# Generate the main layout
####################################
chip_design = i3.LayoutCell()
chip_layout = chip_design.Layout(elements=[i3.SRef(name="E_GAP_6um", reference=first_half_layout, position=(0, 0)),
                                           i3.SRef(name="E_GAP_6um", reference=second_half_layout, transformation=i3.VMirror() + i3.Translation(translation=(0, 10000))),
                                           #i3.SRef(name="E_GAP_6um", reference=third_block_layout, position=(0, 0)),
                                           ])


chip_layout.write_gdsii("gds_output/two_chips_aux_outside_with_heaters_1.06-2.gds")