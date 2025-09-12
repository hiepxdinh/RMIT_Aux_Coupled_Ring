import sys

# Need to update the folder that contains asp_sin_lnoi_photonics/ipkiss


sys.path.append("C:/pdk/asp_sin_lnoi_photonics/ipkiss")
sys.path.append("H:/GitHub/asp_sin_lnoi_photonics/ipkiss")
sys.path.append("D:/RMITRaceHubDataHiepDX/PDKs/asp_sin_lnoi_photonics/ipkiss")


import asp_sin_lnoi_photonics.technology
import asp_sin_lnoi_photonics.all as asp
import ipkiss3.all as i3
import numpy as np


# from ring_gc_h_iden.cell import RingModulatorGCHiepIden
from ring_gc_h_iden_heater_changed.cell import RingModulatorGCHiepIden_heater_changed_v2_op1, RingModulatorGCHiepIden_heater_changed_v2_op2
# from ring_modulator_h_iden.cell import AddDropRingWithElectrodeHiepIden_v2
from ring_modulator_h_iden_heater_changed.cell import AddDropRingWithElectrodeHiepIden_heater_changed_v2_op1, AddDropRingWithElectrodeHiepIden_heater_changed_v2_op2
from waveguide_loop.cell import WaveguideLoop

from ring_modulator_h_iden_19Ghz_heater_changed.cell import AddDropRingWithElectrodeHiepIden_19GHz_heater_changed_v2_option_1, AddDropRingWithElectrodeHiepIden_19GHz_heater_changed_v2_option_2
from ring_gc_h_iden_19Ghz_heater_changed.cell import RingModulatorGCHiepIden_19GHz_heater_changed_v2_option_1, RingModulatorGCHiepIden_19GHz_heater_changed_v2_option_2

from ring_modulator import AddDropRingWithElectrode, AddDropRingWithOutElectrode
from ring_gc import RingModulatorGC, RingModulatorGC_NoElectrode, RingModulatorGC_NoElectrode_2
#######################################
# Global parameters
######################################
waveguide_spacing = 50 # spacing between adjacent waveguides
bend_radius = 200  # Bending radius used in waveguide routing
coupler_bend_radius = 200
hot_electrode_width = 40
hot_electrode_width_hiep = 50
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

ring_radius_test = 200


fsr = 19  # in GHz

fsr_2 = 9.5 # in GHz

fsr_test = 38 # in GHz

straight_length = ring_straight_length(ring_radius, ng, fsr)
ring_width = straight_length + ring_radius * 2

straight_length_2 = ring_straight_length(ring_radius, ng, fsr_2)
ring_width_2 = straight_length_2 + ring_radius *2

straight_length_test = ring_straight_length(ring_radius_test, ng, fsr_test)
ring_width_test = straight_length_test + ring_radius_test * 2

print("Ring straight length: {}".format(straight_length))

print("Ring straight length FSR-9.5GHz: {}".format(straight_length_2))

print("Ring straight length FSR-38GHz: {}".format(straight_length_test))

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


######################################
#I. FIRST BLOCK
######################################
electrode_gap = 7
######################################
coupling_gaps = 1.1
topo_gap = 0.7 # Topology coupler gap
change = 150
moving = 250 + change
gc_position = (3130 + moving - 1325-150 + 420 + 55-350-1000, 9250+390-60-25-185-185-45)  # Position of the first grating coupler

#Waveguide loop
wg_loop_1 = WaveguideLoop(name="wg_loop_1", spacing=fibre_array_pich *11, bend_radius=150)
wg_loop_lo_1 = wg_loop_1.Layout()

chip_elements.append(i3.SRef(name="wg_loop_1", reference=wg_loop_lo_1, position=gc_position))


#
ring_9_5_GHz = AddDropRingWithElectrodeHiepIden_heater_changed_v2_op1()


ring_9_5_GHz_lo = ring_9_5_GHz.Layout(ring_straight_length=straight_length_2,
                      topo_gap = topo_gap, # Topology coupler gap
                      coupler_spacing=coupling_gaps, # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length_2 - 250,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_9_5_GHz_in_pos = ring_9_5_GHz_lo.ports['in'].position

first_ring_9_5_GHz_position = (-ring_9_5_GHz_in_pos[0] + bend_radius - 3390, -1500 + 50+63)

# Ring
i = 1
gap = coupling_gaps
ring_position = (first_ring_9_5_GHz_position[0] + ring_width_2 * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_9_5_GHz_position[1])
name = "Ring_9_5GHz_EG_{}G_{}_TOPO_G_{}_V2_OP1".format(electrode_gap, gap, topo_gap)
ring_gc_h = RingModulatorGCHiepIden_heater_changed_v2_op1(name=name,
                                ring_position=ring_position,
                                gc_wg_distance=-ring_position[1] - ring_radius - 100 - bend_radius * 2 - waveguide_spacing * 4 * i,
                                ring_wg_distance=bend_radius + 5,
                                bend_radius=bend_radius,
                                coupler_bend_radius=coupler_bend_radius,
                                gc_spacing=fibre_array_pich,
                                waveguide_spacing=waveguide_spacing)
print("ring_position: {}".format(ring_position))
ring_gc_lo_h = ring_gc_h.Layout(ring_radius=ring_radius,
                                ring_straight_length=straight_length_2,
                                topo_gap=topo_gap, # Topology coupler gap
                                coupler_spacing=gap,  # Coupler gap
                                coupler_straight_length=coupl_length,
                                coupler_positions=[-straight_length_2 * 0.125 - 510-650 + coupl_length,
                                                   straight_length_2 * 0.2 - 600-600 - coupl_length],
                                electrode_length=straight_length_2 - 950,
                                # hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                # taper_gap = electrode_gap,
                                with_label=True,
                                label_position=ring_position,
                                label_angle=0,
                                coupler_gap_Hiep=gap,
                                electrode_gap_Hiep=electrode_gap
                                )

chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich + fibre_array_pich * 4 * i-4, gc_position[1])))  # Modified

first_block = i3.LayoutCell(name="first_block")
first_block_layout = first_block.Layout(elements=chip_elements)

########################
# II. SECOND BLOCK
########################
electrode_gap = 7
chip_elements = []
########################
########################
coupling_gaps = 1.1

topo_gap = 0.7 # Topology coupler gap

change = 150
moving = 250 + change
gc_position = (3130 + moving - 1325-150 + 420 + 55-350-1000, 9250+400-3000-295-65+100-250)  # Position of the first grating coupler

#Waveguide loop
wg_loop_1 = WaveguideLoop(name="wg_loop_1", spacing=fibre_array_pich *11, bend_radius=150)
wg_loop_lo_1 = wg_loop_1.Layout()

chip_elements.append(i3.SRef(name="wg_loop_1", reference=wg_loop_lo_1, position=gc_position))
################

ring_9_5_GHz = AddDropRingWithElectrodeHiepIden_heater_changed_v2_op2()

ring_9_5_GHz_lo = ring_9_5_GHz.Layout(ring_straight_length=straight_length_2,
                      topo_gap = topo_gap, # Topology coupler gap
                      coupler_spacing=coupling_gaps, # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length_2 - 250,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_9_5_GHz_in_pos = ring_9_5_GHz_lo.ports['in'].position

first_ring_9_5_GHz_position = (-ring_9_5_GHz_in_pos[0] + bend_radius - 3390, -1500 + 50-187+250)

# Ring
i = 1
gap = coupling_gaps
ring_position = (first_ring_9_5_GHz_position[0] + ring_width_2 * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_9_5_GHz_position[1])
name = "Ring_9_5GHz_EG_{}G_{}_TOPO_G_{}_V2_OP2".format(electrode_gap, gap, topo_gap)
ring_gc_h = RingModulatorGCHiepIden_heater_changed_v2_op2(name=name,
                                ring_position=ring_position,
                                gc_wg_distance=-ring_position[1] - ring_radius - 100 - bend_radius * 2 - waveguide_spacing * 4 * i,
                                ring_wg_distance=bend_radius + 5,
                                coupler_bend_radius=coupler_bend_radius,
                                bend_radius=bend_radius,
                                gc_spacing=fibre_array_pich,
                                waveguide_spacing=waveguide_spacing)
print("ring_position: {}".format(ring_position))
ring_gc_lo_h = ring_gc_h.Layout(ring_radius=ring_radius,
                                ring_straight_length=straight_length_2,
                                topo_gap = topo_gap, # Topology coupler gap
                                coupler_spacing=gap,  # Coupler gap
                                coupler_straight_length=coupl_length,
                                coupler_positions=[-straight_length_2 * 0.125 - 510 -650+ coupl_length,
                                                   straight_length_2 * 0.2 - 600 -600 - coupl_length],
                                electrode_length=straight_length_2 - 950-120,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                taper_gap = electrode_gap,
                                with_label=True,
                                label_position=ring_position,
                                label_angle=0,
                                coupler_gap_Hiep=gap,
                                electrode_gap_Hiep=electrode_gap
                                )

chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich + fibre_array_pich * 4 * i-4, gc_position[1])))  # Modified


second_block = i3.LayoutCell(name="second block")
second_block_layout = second_block.Layout(elements=chip_elements)


######################################
# III. THIRD BLOCK
#####################################
electrode_gap = 7
chip_elements = []


#######################################
# 1. Sweep the coupling gap - 3rd row
######################################
coupling_gaps = 1.1
topo_gap = 0.7 # Topology coupler gap
change = 150
moving = 250 + change
gc_position = (3130 + moving - 1325-150 + 420 + 55-350-1000+1000, 9250+400-6550)  # Position of the first grating coupler

wg_loop_2 = WaveguideLoop(name="wg_loop_2", spacing=fibre_array_pich * 11, bend_radius=150) #Modified
wg_loop_lo_2 = wg_loop_2.Layout()

chip_elements.append(i3.SRef(name="wg_loop_2", reference=wg_loop_lo_2, position=(gc_position[0]+75+140, gc_position[1])))


ring_19_GHz = AddDropRingWithElectrodeHiepIden_19GHz_heater_changed_v2_option_1()

ring_19_GHz_lo = ring_19_GHz.Layout(ring_straight_length=straight_length_2,
                      topo_gap = topo_gap,
                      coupler_spacing=coupling_gaps, # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length - 250,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_19_GHz_in_pos = ring_19_GHz_lo.ports['in'].position

first_ring_19_GHz_position = (-ring_19_GHz_in_pos[0] + bend_radius - 4500-360-150, -1500 + 153)

# Ring
i = 1
gap = coupling_gaps
topo_gap = topo_gap
ring_position = (first_ring_19_GHz_position[0] + ring_width_2 * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_19_GHz_position[1])
name = "Ring_19GHz_EG_{}G_{}_TOPO_G{}_V2_OP1".format(electrode_gap, gap,topo_gap)
ring_gc_h = RingModulatorGCHiepIden_19GHz_heater_changed_v2_option_1(name=name,
                                ring_position=ring_position,
                                gc_wg_distance=-ring_position[1] - ring_radius - 100 - bend_radius * 2 - waveguide_spacing * 4 * i,
                                ring_wg_distance=bend_radius + 5,
                                bend_radius=bend_radius,
                                coupler_bend_radius=coupler_bend_radius,
                                gc_spacing=fibre_array_pich,
                                waveguide_spacing=waveguide_spacing)
print("ring_position: {}".format(ring_position))
ring_gc_lo_h = ring_gc_h.Layout(ring_radius=ring_radius-30,
                                ring_straight_length=straight_length,
                                topo_gap=topo_gap, # Topology coupler gap
                                coupler_spacing=gap,  # Coupler gap
                                coupler_straight_length=coupl_length,
                                coupler_positions=[-straight_length * 0.125 - 750 + coupl_length,
                                                   straight_length * 0.2 - 700 - coupl_length],
                                electrode_length=straight_length - 750-45,
                                # hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                # taper_gap = electrode_gap,
                                with_label=True,
                                label_position=ring_position,
                                label_angle=0,
                                coupler_gap_Hiep=gap,
                                electrode_gap_Hiep=electrode_gap
                                )



chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich + fibre_array_pich * 4 * i-4+75+140, gc_position[1])))  # Modified


third_block = i3.LayoutCell(name="third block")
third_block_layout = third_block.Layout(elements=chip_elements)


######################################
# III. THIRD BLOCK
#####################################
electrode_gap = 7
chip_elements = []


#######################################
# 1. Sweep the coupling gap - 3rd row
######################################
coupling_gaps = 1.1
topo_gap = 0.7 # Topology coupler gap
change = 150
moving = 250 + change
gc_position = (3130 + moving - 1325-150 + 420 + 55-350-1000+1000, 9250+400-6550)  # Position of the first grating coupler

wg_loop_2 = WaveguideLoop(name="wg_loop_2", spacing=fibre_array_pich * 11, bend_radius=150) #Modified
wg_loop_lo_2 = wg_loop_2.Layout()

chip_elements.append(i3.SRef(name="wg_loop_2", reference=wg_loop_lo_2, position=(gc_position[0] + 75+140, gc_position[1])))


ring_19_GHz = AddDropRingWithElectrodeHiepIden_19GHz_heater_changed_v2_option_2()

ring_19_GHz_lo = ring_19_GHz.Layout(ring_straight_length=straight_length_2,
                      topo_gap = topo_gap,
                      coupler_spacing=coupling_gaps, # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length - 250,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_19_GHz_in_pos = ring_19_GHz_lo.ports['in'].position

first_ring_19_GHz_position = (-ring_19_GHz_in_pos[0] + bend_radius - 4500-360-150, -1500 + 153)


# Ring
i = 1
gap = coupling_gaps
topo_gap = topo_gap
ring_position = (first_ring_19_GHz_position[0] + ring_width_2 * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_19_GHz_position[1])
name = "Ring_19GHz_EG_{}G_{}_TOPO_G{}_V2_OP2".format(electrode_gap, gap,topo_gap)
ring_gc_h = RingModulatorGCHiepIden_19GHz_heater_changed_v2_option_2(name=name,
                                ring_position=ring_position,
                                gc_wg_distance=-ring_position[1] - ring_radius - 100 - bend_radius * 2 - waveguide_spacing * 4 * i,
                                ring_wg_distance=bend_radius + 5,
                                bend_radius=bend_radius,
                                coupler_bend_radius=coupler_bend_radius,
                                gc_spacing=fibre_array_pich,
                                waveguide_spacing=waveguide_spacing)
print("ring_position: {}".format(ring_position))
ring_gc_lo_h = ring_gc_h.Layout(ring_radius=ring_radius-30,
                                ring_straight_length=straight_length,
                                topo_gap=topo_gap, # Topology coupler gap
                                coupler_spacing=gap,  # Coupler gap
                                coupler_straight_length=coupl_length,
                                coupler_positions=[-straight_length * 0.125 - 750 + coupl_length,
                                                   straight_length * 0.2 - 700 - coupl_length],
                                electrode_length=straight_length - 750-280,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                taper_gap = electrode_gap,
                                with_label=True,
                                label_position=ring_position,
                                label_angle=0,
                                coupler_gap_Hiep=gap,
                                electrode_gap_Hiep=electrode_gap
                                )



chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich + fibre_array_pich * 4 * i-4+ 75+140, gc_position[1])))  # Modified


fourth_block = i3.LayoutCell(name="fourth block")
fourth_block_layout = fourth_block.Layout(elements=chip_elements)

######################################################################
# FIFTH BLOCK
######################################################################
electrode_gap = 7
chip_elements = []
####################
# RING TEST
####################
coupling_gaps = 1.1
topo_gap =0.7

change = 150
moving = 250 + change
gc_position = (3130 + moving - 1325-150 + 420 + 55-1000-127*2-450+4900-350+127*6,  9250+400-3000-295-65-300+50+450+250)  # Position of the first grating coupler

#Waveguide loop
wg_loop_2 = WaveguideLoop(name="wg_loop_2_test", spacing=fibre_array_pich *11, bend_radius=150)
wg_loop_lo_2 = wg_loop_2.Layout()

# chip_elements.append(i3.SRef(name="wg_loop_2", reference=wg_loop_lo_2, position=gc_position))

##############

ring_19_GHz = AddDropRingWithElectrode()

ring_19_GHz_lo = ring_19_GHz.Layout(ring_straight_length=straight_length,
                      coupler_spacing=coupling_gaps, # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length - 250,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_19_GHz_in_pos = ring_19_GHz_lo.ports['in'].position

first_ring_19_GHz_position = (-ring_19_GHz_in_pos[0] + bend_radius - 4500-800-800, -1500 + 50-895+25-50-450+1600)

# Ring
i = 1
gap = coupling_gaps
ring_position = (first_ring_19_GHz_position[0] + ring_width_2 * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_19_GHz_position[1])
name = "Ring_TEST_G_{}".format(electrode_gap, gap,topo_gap)
ring_gc_h = RingModulatorGC(name=name,
                                ring_position=ring_position,
                                gc_wg_distance=-ring_position[1] - ring_radius - 100 - bend_radius * 2 - waveguide_spacing * 4 * i,
                                ring_wg_distance=bend_radius + 5,
                                bend_radius=bend_radius,
                                gc_spacing=fibre_array_pich,
                                waveguide_spacing=waveguide_spacing)
print("ring_position: {}".format(ring_position))
ring_gc_lo_h = ring_gc_h.Layout(ring_radius=ring_radius,
                                ring_straight_length=straight_length,
                                coupler_spacing=gap,  # Coupler gap
                                coupler_straight_length=coupl_length,
                                coupler_positions=[-straight_length * 0.125 - 150 + coupl_length,
                                                   straight_length * 0.2 - coupl_length],
                                electrode_length=straight_length - 150,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                # with_label=True,
                                # label_position=ring_position,
                                # label_angle=0,
                                # coupler_gap_Hiep=gap,
                                # electrode_gap_Hiep=electrode_gap
                                )

# chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich * 4 * i, gc_position[1])))  # Modified

############

gc_position = (3130 + moving - 1325-150 + 420 + 55-1000-127*2-450+4900-350+127*6,  9250+400-3000-295-65-300+50+450-3000+250)  # Position of the first grating coupler

#Waveguide loop
wg_loop_2 = WaveguideLoop(name="wg_loop_2_test_2", spacing=fibre_array_pich *5, bend_radius=150)
wg_loop_lo_2 = wg_loop_2.Layout()

chip_elements.append(i3.SRef(name="wg_loop_2_test_2", reference=wg_loop_lo_2, position=gc_position))

##############

ring_19_GHz = AddDropRingWithOutElectrode()

ring_19_GHz_lo = ring_19_GHz.Layout(ring_straight_length=straight_length,
                      coupler_spacing=coupling_gaps, # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length - 250,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_19_GHz_in_pos = ring_19_GHz_lo.ports['in'].position

first_ring_19_GHz_position = (-ring_19_GHz_in_pos[0] + bend_radius - 4500-800-800-2000, -1500 + 50-895+25-50-450+1600)

# Ring
i = 1
gap = coupling_gaps
ring_position = (first_ring_19_GHz_position[0] + ring_width_2 * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_19_GHz_position[1])
name = "Ring_TEST_G_{}_No_Electrode".format(electrode_gap, gap,topo_gap)
ring_gc_h = RingModulatorGC_NoElectrode_2(name=name,
                                ring_position=ring_position,
                                gc_wg_distance=-ring_position[1] - ring_radius - 100 - bend_radius * 2 - waveguide_spacing * 4 * i,
                                ring_wg_distance=bend_radius + 5,
                                bend_radius=bend_radius,
                                gc_spacing=fibre_array_pich,
                                waveguide_spacing=waveguide_spacing)
print("ring_position: {}".format(ring_position))
ring_gc_lo_h = ring_gc_h.Layout(ring_radius=ring_radius,
                                ring_straight_length=straight_length,
                                coupler_spacing=gap,  # Coupler gap
                                coupler_straight_length=coupl_length,
                                coupler_positions=[-straight_length * 0.125 - 150 + coupl_length,
                                                   straight_length * 0.2 - coupl_length],
                                electrode_length=straight_length - 150,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                # with_label=True,
                                # label_position=ring_position,
                                # label_angle=0,
                                # coupler_gap_Hiep=gap,
                                # electrode_gap_Hiep=electrode_gap
                                )

chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich * 4 * i +19, gc_position[1])))  # Modified


############

gc_position = (3130 + moving - 1325-150 + 420 + 55-1000-127*2-450+4900-350+127*6,  9250+400-3000-295-65-300+50+450-3000+250)  # Position of the first grating coupler

#Waveguide loop
wg_loop_2 = WaveguideLoop(name="wg_loop_2_test_3", spacing=fibre_array_pich *5, bend_radius=150)
wg_loop_lo_2 = wg_loop_2.Layout()

chip_elements.append(i3.SRef(name="wg_loop_2_test_3", reference=wg_loop_lo_2, position=(gc_position[0], gc_position[1]+600), transformation=i3.VMirror()))

##############

ring_19_GHz = AddDropRingWithOutElectrode()

ring_19_GHz_lo = ring_19_GHz.Layout(ring_straight_length=straight_length,
                      coupler_spacing=coupling_gaps, # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length - 250,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_19_GHz_in_pos = ring_19_GHz_lo.ports['in'].position

first_ring_19_GHz_position = (-ring_19_GHz_in_pos[0] + bend_radius - 4500-800-800-2000, -1500 + 50-895+25-50-450+1600)

# Ring
i = 1
gap = coupling_gaps
ring_position = (first_ring_19_GHz_position[0] + ring_width_2 * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_19_GHz_position[1])
name = "Ring_TEST_G_{}_No_Electrode_2".format(electrode_gap, gap,topo_gap)
ring_gc_h = RingModulatorGC_NoElectrode_2(name=name,
                                ring_position=ring_position,
                                gc_wg_distance=-ring_position[1] - ring_radius - 100 - bend_radius * 2 - waveguide_spacing * 4 * i,
                                ring_wg_distance=bend_radius + 5,
                                bend_radius=bend_radius,
                                gc_spacing=fibre_array_pich,
                                waveguide_spacing=waveguide_spacing)
print("ring_position: {}".format(ring_position))
ring_gc_lo_h = ring_gc_h.Layout(ring_radius=ring_radius,
                                ring_straight_length=straight_length,
                                coupler_spacing=gap,  # Coupler gap
                                coupler_straight_length=coupl_length,
                                coupler_positions=[-straight_length * 0.125 - 150 + coupl_length,
                                                   straight_length * 0.2 - coupl_length],
                                electrode_length=straight_length - 150,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                # with_label=True,
                                # label_position=ring_position,
                                # label_angle=0,
                                # coupler_gap_Hiep=gap,
                                # electrode_gap_Hiep=electrode_gap
                                )

chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich * 4 * i +19, gc_position[1] + 600), transformation=i3.VMirror()))  # Modified


##############
fifth_block = i3.LayoutCell(name="Fifth block")
fifth_block_layout = fifth_block.Layout(elements=chip_elements)
###############################################################
######################################################################


####################################
# Generate the main layout
####################################
chip_design = i3.LayoutCell()
chip_layout = chip_design.Layout(elements=[
                                        i3.SRef(name="E_GAP_6um", reference=first_block_layout, position=(0, 0)),
                                          i3.SRef(name="E_GAP_6um", reference=second_block_layout, position=(0, 0)),
                                         i3.SRef(name="E_GAP_6um", reference=third_block_layout, transformation= i3.HMirror() + i3.Translation(translation=(14000-250,0))),
                                        i3.SRef(name="E_GAP_6um", reference=fourth_block_layout, position=(-1000+250, 0)),
                                        i3.SRef(name="E_GAP_6um", reference=fifth_block_layout, position=(-1000+250 + 6360-560, +3250-150)),
])


chip_layout.write_gdsii("gds_output/two_chips_iden_with_heaters_1.03_v3_update_heater_distance_new_heater_design.gds")