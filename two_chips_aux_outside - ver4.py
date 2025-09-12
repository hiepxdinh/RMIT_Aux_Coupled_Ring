import sys


# Need to update the folder that contains asp_sin_lnoi_photonics/ipkiss


# sys.path.append("C:/pdk/asp_sin_lnoi_photonics/ipkiss")
# sys.path.append("H:/GitHub/asp_sin_lnoi_photonics/ipkiss")
# sys.path.append("D:/RMITRaceHubDataHiepDX/PDKs/asp_sin_lnoi_photonics/ipkiss")
sys.path.append("C:/Users/Administrator/Documents/GitHub/asp_sin_lnoi_photonics/ipkiss")
import asp_sin_lnoi_photonics.technology
import asp_sin_lnoi_photonics.all as asp
import ipkiss3.all as i3
import numpy as np

from ring_gc.cell import NotchRingGC
from ring_gc_h_with_auxiliary_ring_outside.cell import RingModulatorGCHiepAuxOutside
from ring_gc_h_with_auxiliary_ring_outside_19GHz.cell import RingModulatorGCHiepAuxOutside2, RingModulatorGCHiepAuxOutside3
from ring_gc_h_with_auxiliary_ring_outside_2.cell import RingModulatorGCHiepAuxOutside_Top, RingModulatorGCHiepAuxOutside_Top_2
from ring_gc_h_with_auxiliary_ring_outside_19GHz_2.cell import RingModulatorGCHiepAuxOutside2_Top
from ring_modulator.cell import AddDropRingWithElectrode

from ring_modulator_with_auxiliary_ring_outside.cell import AddDropRingWithAuxOutside_Euler
from waveguide_loop.cell import WaveguideLoop


from ring_modulator import AddDropRingWithElectrode
from ring_gc import RingModulatorGC


#######################################
# Global parameters
######################################
waveguide_spacing = 75 # spacing between adjacent waveguides
bend_radius = 180  # Bending radius used in waveguide routing
hot_electrode_width = 23
fibre_array_pich = 127
ebl_writing_size = (1000, 1000)
chip_elements = list()


#### Calculate ring parameters ########## for Circular bend
def ring_straight_length_circular(radius, ng, fsr):
    ring_length = 3e8 / (fsr * 1e9) / ng
    return int((ring_length - 2.0 * np.pi * radius * 1e-6) / 2 * 1e6)


#### Calculate ring parameters ########## for Euler bend
def ring_straight_length_euler(euler_bend_length, ng, fsr):
    ring_length = 3e8 / (fsr * 1e9) / ng
    return int((ring_length - 2.0 * euler_bend_length * 1e-6) / 2 * 1e6)



ring_radius = 200
coupl_length = 100
ng = 2.234

ring_radius_aux = 200

ring_radius_test = 150

#Euler bend length is calculated based on the defined ring radius:

euler_bend_length_calculated = 942.4772415892692

fsr = 19  # in GHz

fsr_2 = 6 # in GHz

fsr_aux= fsr_2*6 # in GHz

fsr_test = 20 # in GHz

straight_length = ring_straight_length_euler(euler_bend_length_calculated, ng, fsr)
ring_width = straight_length + ring_radius * 2

straight_length_2 = ring_straight_length_euler(euler_bend_length_calculated, ng, fsr_2)
ring_width_2 = straight_length_2 + ring_radius *2

straight_length_aux = ring_straight_length_euler(euler_bend_length_calculated, ng, fsr_aux)
ring_width_aux = straight_length_aux + ring_radius_aux * 2

print("Ring straight length FSR-19GHz: {}".format(straight_length))

print("Ring straight length FSR-6GHz: {}".format(straight_length_2))

print("Ring straight length-auxiliary: {}".format(straight_length_aux))

straight_length_test = ring_straight_length_euler(euler_bend_length_calculated, ng, fsr_test)
ring_widtth_test = straight_length + ring_radius * 2

print("Ring straight length test: {}".format(straight_length_test))

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


######################################
# I. First half electrode gap: 6um
#####################################
electrode_gap = 8
coupling_gaps = [1.25, 1.25]
#######################################
# 1. Sweep the coupling gap - 2nd row
######################################
aux_coupling_gap = 2.05
change = 150
moving = 250 + change
gc_position = (3130 + moving-2000+1000+525-1000, 9180-300-150)  # Position of the first grating coupler

# Waveguide loop
wg_loop_1 = WaveguideLoop(name="wg_loop_1", spacing=fibre_array_pich *7, bend_radius=150)
wg_loop_lo_1 = wg_loop_1.Layout()

chip_elements.append(i3.SRef(name="wg_loop_1", reference=wg_loop_lo_1, position=gc_position))


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


ring_9_5_GHz = AddDropRingWithAuxOutside_Euler()

ring_9_5_GHz_lo = ring_9_5_GHz.Layout(ring_straight_length=straight_length_2,
                      coupler_spacing=coupling_gaps[1], # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length_2 - 150,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_9_5_GHz_in_pos = ring_9_5_GHz_lo.ports['in'].position

first_ring_9_5_GHz_position = (-ring_9_5_GHz_in_pos[0] + bend_radius - 2800-3700-125+127*4-1000-525+525, -1500-50 - 29.5+200-180+40+150-55)

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
                                coupler_positions=[-straight_length * 0.125 + 500 + coupl_length-50,
                                                   straight_length * 0.2 + 450 - coupl_length-50-20],
                                electrode_length=straight_length - 150,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                with_label=True,
                                label_position=ring_position,
                                label_angle=0,
                                coupler_gap_Hiep=gap,
                                electrode_gap_Hiep=electrode_gap
                                )
# chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich + fibre_array_pich * 4 * i-4, gc_position[1])))  # Modified

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
                                coupler_positions=[-straight_length_2 * 0.125 - 510-730+110+500 + coupl_length-109,
                                                   straight_length_2 * 0.2 - 600 -730+150+330 - coupl_length-20],
                                electrode_length=straight_length_2 - 150,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                with_label=True,
                                label_position=ring_position,
                                label_angle=0,
                                coupler_gap_Hiep=gap,
                                electrode_gap_Hiep=electrode_gap
                                )



chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich + fibre_array_pich * 0 * i-4, gc_position[1])))  # Modified

##########################################
# Second row
##########################################
#######################################
# 1. Sweep the coupling gap - 2nd row
######################################
coupling_gaps = [1.25, 1.25]
aux_coupling_gap = 2.10
change = 150
moving = 250 + change
gc_position = (3130 + moving-2000+1000+525-1000, 9180-2300-17.5-50)  # Position of the first grating coupler

# Waveguide loop
wg_loop_1 = WaveguideLoop(name="wg_loop_1", spacing=fibre_array_pich *7, bend_radius=150)
wg_loop_lo_1 = wg_loop_1.Layout()

chip_elements.append(i3.SRef(name="wg_loop_1", reference=wg_loop_lo_1, position=gc_position))

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


ring_9_5_GHz = AddDropRingWithAuxOutside_Euler()

ring_9_5_GHz_lo = ring_9_5_GHz.Layout(ring_straight_length=straight_length_2,
                      coupler_spacing=coupling_gaps[1], # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length_2 - 150,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_9_5_GHz_in_pos = ring_9_5_GHz_lo.ports['in'].position

first_ring_9_5_GHz_position = (-ring_9_5_GHz_in_pos[0] + bend_radius - 2800-3700-125+127*4-1000-525+525, -1500-50 - 29.5+50)

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
                                coupler_positions=[-straight_length * 0.125 + 500 + coupl_length-50,
                                                   straight_length * 0.2 + 450 - coupl_length-50-20],
                                electrode_length=straight_length - 150,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                with_label=True,
                                label_position=ring_position,
                                label_angle=0,
                                coupler_gap_Hiep=gap,
                                electrode_gap_Hiep=electrode_gap
                                )
# chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich + fibre_array_pich * 4 * i-4, gc_position[1])))  # Modified

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
                                coupler_positions=[-straight_length_2 * 0.125 - 510-730+110+500 + coupl_length-109,
                                                   straight_length_2 * 0.2 - 600 -730+150+330 - coupl_length-20],
                                electrode_length=straight_length_2 - 150,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                with_label=True,
                                label_position=ring_position,
                                label_angle=0,
                                coupler_gap_Hiep=gap,
                                electrode_gap_Hiep=electrode_gap
                                )



chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich + fibre_array_pich * 0 * i-4, gc_position[1]+1)))  # Modified


###########################################

first_half = i3.LayoutCell()
first_half_layout = first_half.Layout(elements=chip_elements)



######################################
# II. Second half electrode gap: 9um
#####################################
electrode_gap = 8
chip_elements = []
#######################################
# 1. Sweep the coupling gap - 2nd row
coupling_gaps = [1.25, 1.25]
aux_coupling_gap = 2.05
change = 150
moving = 250 + change
gc_position = (3130 + moving-2000+1000+525-1000, 9180-300-150)  # Position of the first grating coupler

# Waveguide loop
wg_loop_1 = WaveguideLoop(name="wg_loop_1", spacing=fibre_array_pich *7, bend_radius=150)
wg_loop_lo_1 = wg_loop_1.Layout()

chip_elements.append(i3.SRef(name="wg_loop_1", reference=wg_loop_lo_1, position=gc_position))



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


ring_9_5_GHz = AddDropRingWithAuxOutside_Euler()

ring_9_5_GHz_lo = ring_9_5_GHz.Layout(ring_straight_length=straight_length_2,
                      coupler_spacing=coupling_gaps[1], # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length_2 - 150,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_9_5_GHz_in_pos = ring_9_5_GHz_lo.ports['in'].position

first_ring_9_5_GHz_position = (-ring_9_5_GHz_in_pos[0] + bend_radius - 2800-3700-125+127*4-1000-525+525, -1500-50 - 29.5+200-180+40+150-55)

#First ring
i = 0
gap = coupling_gaps[0]
ring_position = (first_ring_position[0] + ring_width_2 * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_position[1])
name = "Ring_19GHz_EG_{}G_{}_AUX_G_{}_3".format(electrode_gap, gap,aux_coupling_gap)
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
                                coupler_positions=[-straight_length * 0.125 + 500 + coupl_length-50,
                                                   straight_length * 0.2 + 450 - coupl_length-50-20],
                                electrode_length=straight_length - 150,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                with_label=True,
                                label_position=ring_position,
                                label_angle=0,
                                coupler_gap_Hiep=gap,
                                electrode_gap_Hiep=electrode_gap
                                )
# chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich + fibre_array_pich * 4 * i-4, gc_position[1])))  # Modified

# Second ring
i = 1
gap = coupling_gaps[1]
ring_position = (first_ring_9_5_GHz_position[0] + ring_width_2 * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_9_5_GHz_position[1])
name = "Ring_9_5GHz_EG_{}G_{}_AUX_G_{}_4".format(electrode_gap, gap,aux_coupling_gap)
ring_gc_h = RingModulatorGCHiepAuxOutside_Top_2(name=name,
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
                                coupler_positions=[-straight_length_2 * 0.125 - 510-730+110+500 + coupl_length-109,
                                                   straight_length_2 * 0.2 - 600 -730+150+330 - coupl_length-20],
                                electrode_length=straight_length_2 - 150,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                with_label=True,
                                label_position=ring_position,
                                label_angle=0,
                                coupler_gap_Hiep=gap,
                                electrode_gap_Hiep=electrode_gap
                                )



chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich + fibre_array_pich * 0 * i-4, gc_position[1])))  # Modified

##########################################
# Second row
##########################################
#######################################
# 1. Sweep the coupling gap - 2nd row
######################################
coupling_gaps = [1.25, 1.25]
aux_coupling_gap = 2.05
change = 150
moving = 250 + change
gc_position = (3130 + moving-2000+1000+525-1000, 9180-2300-17.5-50)   # Position of the first grating coupler

# Waveguide loop
wg_loop_1 = WaveguideLoop(name="wg_loop_1", spacing=fibre_array_pich *7, bend_radius=150)
wg_loop_lo_1 = wg_loop_1.Layout()

chip_elements.append(i3.SRef(name="wg_loop_1", reference=wg_loop_lo_1, position=gc_position))


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


ring_9_5_GHz = AddDropRingWithAuxOutside_Euler()

ring_9_5_GHz_lo = ring_9_5_GHz.Layout(ring_straight_length=straight_length_2,
                      coupler_spacing=coupling_gaps[1], # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length_2 - 150,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_9_5_GHz_in_pos = ring_9_5_GHz_lo.ports['in'].position

first_ring_9_5_GHz_position = (-ring_9_5_GHz_in_pos[0] + bend_radius - 2800-3700-125+127*4-1000-525+525, -1500-50 - 29.5 +50)

#First ring
i = 0
gap = coupling_gaps[0]
ring_position = (first_ring_position[0] + ring_width_2 * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_position[1])
name = "Ring_19GHz_EG_{}G_{}_AUX_G_{}_2".format(electrode_gap, gap,aux_coupling_gap)
ring_gc_h = RingModulatorGCHiepAuxOutside3(name=name,
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
                                coupler_positions=[-straight_length * 0.125 + 500 + coupl_length-50,
                                                   straight_length * 0.2 + 450 - coupl_length-50-20],
                                electrode_length=straight_length - 150,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                with_label=True,
                                label_position=ring_position,
                                label_angle=0,
                                coupler_gap_Hiep=gap,
                                electrode_gap_Hiep=electrode_gap
                                )
# chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich + fibre_array_pich * 4 * i-4, gc_position[1])))  # Modified

# Second ring
i = 1
gap = coupling_gaps[1]
ring_position = (first_ring_9_5_GHz_position[0] + ring_width_2 * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_9_5_GHz_position[1])
name = "Ring_9_5GHz_EG_{}G_{}_AUX_G_{}_3".format(electrode_gap, gap,aux_coupling_gap)
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
                                coupler_positions=[-straight_length_2 * 0.125 - 510-730+110+500 + coupl_length-109,
                                                   straight_length_2 * 0.2 - 600 -730+150+330 - coupl_length-20],
                                electrode_length=straight_length_2 - 150,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                with_label=True,
                                label_position=ring_position,
                                label_angle=0,
                                coupler_gap_Hiep=gap,
                                electrode_gap_Hiep=electrode_gap
                                )



chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich + fibre_array_pich * 0 * i-4, gc_position[1])))  # Modified





######################################
second_half = i3.LayoutCell(name="Second_Half")
second_half_layout = second_half.Layout(elements=chip_elements)


#######################################
# THIRD BLOCK
chip_elements = []
####################

electrode_gap = 7

####################
# RING TEST
####################
coupling_gaps = 1.25
topo_gap = 1.0

change = 150
moving = 250 + change
gc_position = (3130 + moving - 1325-150 + 420 + 55-1000-127*2-450+4900-350+127*6+2450+250-250+125,  9250+400-3000-295-65-300+50+450+250+850+250)  # Position of the first grating coupler

#Waveguide loop
wg_loop_2 = WaveguideLoop(name="wg_loop_2_test", spacing=fibre_array_pich *5, bend_radius=150)
wg_loop_lo_2 = wg_loop_2.Layout()

chip_elements.append(i3.SRef(name="wg_loop_2_test", reference=wg_loop_lo_2, position=gc_position, transformation=i3.VMirror()))

chip_elements.append(i3.SRef(name="wg_loop_2_test", reference=wg_loop_lo_2, position=gc_position, transformation=i3.VMirror()+ i3.VMirror(mirror_plane_y=-2850)))

##############

ring_19_GHz = AddDropRingWithElectrode()

ring_19_GHz_lo = ring_19_GHz.Layout(ring_straight_length=straight_length_test,
                      coupler_spacing=coupling_gaps, # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length_test - 250,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_19_GHz_in_pos = ring_19_GHz_lo.ports['in'].position

first_ring_19_GHz_position = (-ring_19_GHz_in_pos[0] + bend_radius - 4500-800-800-50-410+150-8000+200+125, -1500 + 50-895+25-50-450+1600-100)

# Ring
i = 1
gap = coupling_gaps
ring_position = (first_ring_19_GHz_position[0] + ring_width_2 * i - fibre_array_pich * 4 * i + waveguide_spacing * i+4000, first_ring_19_GHz_position[1])
name = "Ring_TEST_G_{}".format(electrode_gap, gap,topo_gap)
ring_gc_h = RingModulatorGC(name=name,
                                ring_position=ring_position,
                                gc_wg_distance=-ring_position[1] - ring_radius_test - 100 - bend_radius * 2 - waveguide_spacing * 4 * i,
                                ring_wg_distance=bend_radius + 5,
                                bend_radius=bend_radius,
                                gc_spacing=fibre_array_pich,
                                waveguide_spacing=waveguide_spacing)
print("ring_position: {}".format(ring_position))
ring_gc_lo_h = ring_gc_h.Layout(ring_radius=ring_radius_test,
                                ring_straight_length=straight_length_test,
                                coupler_spacing=gap,  # Coupler gap
                                coupler_straight_length=coupl_length,
                                coupler_positions=[-straight_length_test * 0.125 - 150 + coupl_length+250-25-150,
                                                   straight_length_test * 0.2 - coupl_length+250-20],
                                electrode_length=straight_length_test - 150,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                # with_label=True,
                                # label_position=ring_position,
                                # label_angle=0,
                                # coupler_gap_Hiep=gap,
                                # electrode_gap_Hiep=electrode_gap
                                )

chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich * 4 * i +19, gc_position[1]), transformation=i3.VMirror()))  # Modified

chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich * 4 * i +19, gc_position[1]), transformation=i3.VMirror() + i3.VMirror(mirror_plane_y=-2850)))  # Modified


######################
third_block = i3.LayoutCell(name="Third_Block")
third_block_layout = third_block.Layout(elements=chip_elements)

###############################
chip_elements = []
# For logos
from ipkiss.process.layer_map import GenericGdsiiPPLayerInputMap

layer_map = GenericGdsiiPPLayerInputMap(
    ignore_undefined_mappings=True,
    pplayer_map={
        # only define a mapping for the Core layer.
        # the cladding layer will be ignored, because ignore_undefined_mappings is set to True
        (i3.TECH.PROCESS.RWG, i3.TECH.PURPOSE.LF.LINE): (100, 0)
    },
)

logo_imported = i3.GDSCell(filename="rmit_logo.gds")
logo_imported_lv = logo_imported.Layout(layer_map=layer_map)
# logo_imported_lv.visualize()

from ipkiss.process.layer_map import GenericGdsiiPPLayerOutputMap

# # # we make a copy, so that we can freely modify it.
# pplayer_map = dict(i3.TECH.GDSII.LAYERTABLE)
# pplayer_map[i3.TECH.PROCESS.NONE, i3.TECH.PURPOSE.LOGOTXT] = (100, 0)
# output_layer_map = GenericGdsiiPPLayerOutputMap(pplayer_map=pplayer_map)
# # # now we use it to write our GDS:
# # logo_imported_lv.write_gdsii("logo_drawing_B.gds", layer_map=output_layer_map)

logo_name = "rmit_logo"
chip_elements.append(i3.SRef(name=logo_name,reference=logo_imported_lv, position=(0,0)
                             ,transformation=(i3.NoDistortTransform(rotation_center=(0.0, 0.0), rotation=0.0, magnification=5.0)
                                              )))  # Modified

##############
fourth_block = i3.LayoutCell(name="Fourth block")
fourth_block_layout = fourth_block.Layout(elements=chip_elements)
####################################
# Generate the main layout
####################################
chip_design = i3.LayoutCell()
chip_layout = chip_design.Layout(elements=[i3.SRef(name="E_GAP_6um", reference=first_half_layout, position=(0, 0)),
                                           i3.SRef(name="E_GAP_6um", reference=second_half_layout, transformation=i3.VMirror() + i3.Translation(translation=(0, 10000))),
                                           i3.SRef(name="E_GAP_6um", reference=third_block_layout, position=(0, 0)),
                                           i3.SRef(name="E_GAP_6um", reference=fourth_block_layout, position=(4550, 8500))
                                           ])


chip_layout.write_gdsii("gds_output/two_euler_chips_aux_outside_with_heaters_1.40_v2.gds")