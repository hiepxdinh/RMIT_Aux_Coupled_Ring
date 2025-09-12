import sys

# Need to update the folder that contains asp_sin_lnoi_photonics/ipkiss


sys.path.append("C:/pdk/asp_sin_lnoi_photonics/ipkiss")
sys.path.append("H:/GitHub/asp_sin_lnoi_photonics/ipkiss")
sys.path.append("D:/RMITRaceHubDataHiepDX/PDKs/asp_sin_lnoi_photonics/ipkiss")


import asp_sin_lnoi_photonics.technology
import asp_sin_lnoi_photonics.all as asp
import ipkiss3.all as i3
import numpy as np

from ring_modulator.cell import AddDropRingWithElectrode
from ring_gc_h_iden.cell import RingModulatorGCHiepIden
from ring_gc_h_iden_heater_changed.cell import RingModulatorGCHiepIden_heater_changed
from ring_modulator_h_iden.cell import AddDropRingWithElectrodeHiepIden
from ring_modulator_h_iden_heater_changed.cell import AddDropRingWithElectrodeHiepIden_heater_changed
from ring_gc_h_iden_test.cell import RingModulatorGCHiepIden_Test
from ring_modulator_h_iden_coupling_test.cell import AddDropRingWithElectrodeHiepIden_Test
from waveguide_loop.cell import WaveguideLoop
from grating_coupler_test import Coupler_Test04, Coupler_Test04_2, Coupler_Test04_3, Coupler_Test05, Coupler_Test05_2,Coupler_Test05_3, Coupler_Test06, Coupler_Test06_2,Coupler_Test06_3, Coupler_Test07,Coupler_Test07_3,Coupler_Test07_2, Coupler_Test08, Coupler_Test08_2,Coupler_Test08_3

from waveguide_h_6.cell import WaveguideHiep6

from tasneem_bragg_grating import BraggGrating, BragGratingnew, BraggGrating_circuit,Tasneem_Grating


from circuit1_period import BraggGrating_circuit_1_layout_period
from circuit2_period import BraggGrating_circuit_2_layout_period
from circuit3_period import BraggGrating_circuit_3_layout_period
from circuit4_period import BraggGrating_circuit_4_layout_period
from circuit5_period import BraggGrating_circuit_5_layout_period
from circuit6_period import BraggGrating_circuit_6_layout_period
from circuit7_period import BraggGrating_circuit_7_layout_period
from circuit8_period import BraggGrating_circuit_8_layout_period
from ground_wire_period import ground_wire_up_lo_period, ground_wire_down_lo_period
from electric_pad_period import Out_pad_lo_period
from plus_wire_period import plus_wire2_lo_period, plus_wire1_lo_period, plus_wire3_lo_period, plus_wire4_lo_period,plus_wire5_lo_period, plus_wire6_lo_period, plus_wire7_lo_period, plus_wire8_lo_period


from circuit1a_strength import BraggGrating_circuit_1_layout
from circuit2a_strength import BraggGrating_circuit_2_layout
from circuit3a_strength import BraggGrating_circuit_3_layout
from circuit4a_strength import BraggGrating_circuit_4_layout
from circuit5a_strength import BraggGrating_circuit_5_layout
from circuit6a_strength import BraggGrating_circuit_6_layout
from circuit7a_strength import BraggGrating_circuit_7_layout
from circuit8a_strength import BraggGrating_circuit_8_layout
from ground_wire_strength import ground_wire_up_lo_strength, ground_wire_down_lo_strength
from electric_pad_strength import Out_pad_lo_strength
from plus_wire_strength import plus_wire2_lo_strength, plus_wire1_lo_strength, plus_wire3_lo_strength, plus_wire4_lo_strength,plus_wire5_lo_strength, plus_wire6_lo_strength, plus_wire7_lo_strength, plus_wire8_lo_strength





#######################################
# Global parameters
######################################
waveguide_spacing = 50 # spacing between adjacent waveguides
bend_radius = 200  # Bending radius used in waveguide routing
coupler_bend_radius = 300
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

# Waveguide loop
#wg_loop = WaveguideLoop(name="wg_loop", spacing=fibre_array_pich *16, bend_radius=150)
#wg_loop_lo = wg_loop.Layout()

######################################
#I. FIRST BLOCK
#####################################
electrode_gap = 7

#######################################
###############################
coupling_gaps = 1.1
topo_gap = 0.65 # Topology coupler gap
change = 150
moving = 250 + change
gc_position = (3130 + moving - 1325-150 + 420 + 55-350-1000, 9250+390-60-25-185-185-45)  # Position of the first grating coupler

#Waveguide loop
wg_loop_1 = WaveguideLoop(name="wg_loop_1", spacing=fibre_array_pich *11, bend_radius=150)
wg_loop_lo_1 = wg_loop_1.Layout()

chip_elements.append(i3.SRef(name="wg_loop_1", reference=wg_loop_lo_1, position=gc_position))

# Coupler_Test
coupler_position04_1 = (3500, 9250+390-60-25-185-185-45)
coupler_position05_1 = (5700, 9250+390-60-25-185-185-45)

coupler_position04_2 = (3500+127*2, 9250+390-60-25-185-185-45)
coupler_position05_2 = (5700+127*2, 9250+390-60-25-185-185-45)

coupler_position04_3 = (3500+127, 9250+390-60-25-185-185-45)
coupler_position05_3 = (5700+127, 9250+390-60-25-185-185-45)


coupler_test04_1 = Coupler_Test04(name="coupler_test04_1", spacing=fibre_array_pich*11, bend_radius=150) # Added
coupler_test_lo04_1 = coupler_test04_1.Layout() # Added
chip_elements.append(i3.SRef(name="coupler_test04_1", reference=coupler_test_lo04_1, position=coupler_position04_1)) # Added
coupler_test05_1 = Coupler_Test05(name="coupler_test05_1", spacing=fibre_array_pich*11, bend_radius=150) # Added
coupler_test_lo05_1 = coupler_test05_1.Layout() # Added
chip_elements.append(i3.SRef(name="coupler_test05_1", reference=coupler_test_lo05_1, position=coupler_position05_1)) # Added


coupler_test04_2 = Coupler_Test04_2(name="coupler_test04_2", spacing=fibre_array_pich*7, bend_radius=150) # Added
coupler_test_lo04_2 = coupler_test04_2.Layout() # Added
chip_elements.append(i3.SRef(name="coupler_test04_2", reference=coupler_test_lo04_2, position=coupler_position04_2)) # Added
coupler_test05_2 = Coupler_Test05_2(name="coupler_test05_2", spacing=fibre_array_pich*7, bend_radius=150) # Added
coupler_test_lo05_2 = coupler_test05_2.Layout() # Added
chip_elements.append(i3.SRef(name="coupler_test05_2", reference=coupler_test_lo05_2, position=coupler_position05_2)) # Added


coupler_test04_3 = Coupler_Test04_3(name="coupler_test04_3", spacing=fibre_array_pich*9, bend_radius=150) # Added
coupler_test_lo04_3 = coupler_test04_3.Layout() # Added
chip_elements.append(i3.SRef(name="coupler_test04_3", reference=coupler_test_lo04_3, position=coupler_position04_3)) # Added
coupler_test05_3 = Coupler_Test05_3(name="coupler_test05_3", spacing=fibre_array_pich*9, bend_radius=150) # Added
coupler_test_lo05_3 = coupler_test05_3.Layout() # Added
chip_elements.append(i3.SRef(name="coupler_test05_3", reference=coupler_test_lo05_3, position=coupler_position05_3)) # Added
#

#
ring_9_5_GHz = AddDropRingWithElectrodeHiepIden_heater_changed()

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
name = "Ring_9_5GHz_EG_{}G_{}_TOPO_G_{}".format(electrode_gap, gap, topo_gap)
ring_gc_h = RingModulatorGCHiepIden_heater_changed(name=name,
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
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                taper_gap = electrode_gap,
                                with_label=True,
                                label_position=ring_position,
                                label_angle=0,
                                coupler_gap_Hiep=gap,
                                electrode_gap_Hiep=electrode_gap
                                )

chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich + fibre_array_pich * 4 * i, gc_position[1])))  # Modified




# ##########################################
# # RING TEST
# ##########################################
# gc_position = (3130 + moving - 1325-150 + 420 + 55-350-1000 + 7000, 9250+390-60-25-185-185-45+230)
#
# wg_loop_1 = WaveguideLoop(name="wg_loop_1", spacing=fibre_array_pich *11, bend_radius=150)
# wg_loop_lo_1 = wg_loop_1.Layout()
#
# chip_elements.append(i3.SRef(name="wg_loop_1", reference=wg_loop_lo_1, position=gc_position))
#
# ring_test = AddDropRingWithElectrode()
#
# ring_test_lo = ring_test.Layout(ring_straight_length=straight_length, # Topology coupler gap
#                       coupler_spacing=coupling_gaps, # Coupler gap
#                       coupler_straight_length=0,
#                       electrode_length=straight_length - 250,
#                       hot_width=hot_electrode_width,
#                       electrode_gap=electrode_gap
#                       )
#
# ring_test_in_pos = ring_test_lo.ports['in'].position
#
# first_ring_test_position = (-ring_test_in_pos[0] + bend_radius - 4390, -1500 + 50+33-230)
#
# # Ring
# i = 1
# gap = coupling_gaps
# ring_position = (first_ring_test_position[0] + ring_width_2 * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_test_position[1])
# name = "Ring_TEST_G_{}_TOPO_G_{}".format(electrode_gap, gap, topo_gap)
# ring_gc_h = RingModulatorGCHiepIden_Test(name=name,
#                                 ring_position=ring_position,
#                                 gc_wg_distance=-ring_position[1] - ring_radius - 100 - bend_radius * 2 - waveguide_spacing * 4 * i,
#                                 ring_wg_distance=bend_radius + 5,
#                                 bend_radius=bend_radius,
#                                 coupler_bend_radius=coupler_bend_radius,
#                                 gc_spacing=fibre_array_pich,
#                                 waveguide_spacing=waveguide_spacing)
# print("ring_position: {}".format(ring_position))
# ring_gc_lo_h = ring_gc_h.Layout(ring_radius=ring_radius_test,
#                                 ring_straight_length=straight_length_test,
#                                 topo_gap=topo_gap, # Topology coupler gap
#                                 coupler_spacing=gap,  # Coupler gap
#                                 coupler_straight_length=coupl_length,
#                                 coupler_positions=[-straight_length_test * 0.125 -255+ coupl_length,
#                                                    straight_length_test * 0.2 + 195 - coupl_length],
#                                 electrode_length=straight_length_test - 580,
#                                 hot_width=hot_electrode_width,
#                                 electrode_gap=electrode_gap,
#                                 taper_gap = electrode_gap,
#                                 with_label=True,
#                                 label_position=ring_position,
#                                 label_angle=0,
#                                 coupler_gap_Hiep=gap,
#                                 electrode_gap_Hiep=electrode_gap
#                                 )
#
# chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich + fibre_array_pich * 4 * i, gc_position[1])))  # Modified
#
# ########################################



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

#
coupler_position06 = (3500, 9250+400-3000-295-65+100-250)
coupler_position07 = (5700, 9250+400-3000-295-65+100-250)

coupler_position06_2 = (3500+127*2, 9250+400-3000-295-65+100-250)
coupler_position07_2 = (5700+127*2, 9250+400-3000-295-65+100-250)

coupler_position06_3 = (3500+127, 9250+400-3000-295-65+100-250)
coupler_position07_3 = (5700+127, 9250+400-3000-295-65+100-250)


coupler_test06 = Coupler_Test06(name="coupler_test06", spacing=fibre_array_pich*11, bend_radius=150) # Added
coupler_test_lo06 = coupler_test06.Layout() # Added
chip_elements.append(i3.SRef(name="coupler_test06", reference=coupler_test_lo06, position=coupler_position06)) # Added

coupler_test07 = Coupler_Test07(name="coupler_test07", spacing=fibre_array_pich*11, bend_radius=150) # Added
coupler_test_lo07 = coupler_test07.Layout() # Added
chip_elements.append(i3.SRef(name="coupler_test07", reference=coupler_test_lo07, position=coupler_position07)) # Added

coupler_test06_2 = Coupler_Test06_2(name="coupler_test06_2", spacing=fibre_array_pich*7, bend_radius=150) # Added
coupler_test_lo06_2 = coupler_test06_2.Layout() # Added
chip_elements.append(i3.SRef(name="coupler_test06_2", reference=coupler_test_lo06_2, position=coupler_position06_2)) # Added

coupler_test07_2 = Coupler_Test07_2(name="coupler_test07_2", spacing=fibre_array_pich*7, bend_radius=150) # Added
coupler_test_lo07_2 = coupler_test07_2.Layout() # Added
chip_elements.append(i3.SRef(name="coupler_test07_2", reference=coupler_test_lo07_2, position=coupler_position07_2)) # Added

coupler_test06_3 = Coupler_Test06_3(name="coupler_test06_3", spacing=fibre_array_pich*9, bend_radius=150) # Added
coupler_test_lo06_3 = coupler_test06_3.Layout() # Added
chip_elements.append(i3.SRef(name="coupler_test06_3", reference=coupler_test_lo06_3, position=coupler_position06_3)) # Added
coupler_test07_3 = Coupler_Test07_3(name="coupler_test07_3", spacing=fibre_array_pich*9, bend_radius=150) # Added
coupler_test_lo07_3 = coupler_test05_3.Layout() # Added
chip_elements.append(i3.SRef(name="coupler_test07_3", reference=coupler_test_lo07_3, position=coupler_position07_3)) # Added

#

ring_9_5_GHz = AddDropRingWithElectrodeHiepIden()

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
name = "Ring_9_5GHz_EG_{}G_{}_TOPO_G_{}".format(electrode_gap, gap, topo_gap)
ring_gc_h = RingModulatorGCHiepIden(name=name,
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
                                electrode_length=straight_length_2 - 950,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                taper_gap = electrode_gap,
                                with_label=True,
                                label_position=ring_position,
                                label_angle=0,
                                coupler_gap_Hiep=gap,
                                electrode_gap_Hiep=electrode_gap
                                )

chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich + fibre_array_pich * 4 * i, gc_position[1])))  # Modified

##########################################
# RING TEST
##########################################
gc_position = (3130 + moving - 1325-150 + 420 + 55-350-1000 + 7000, 9250+400-3000-295-65+100-250+230)

wg_loop_1 = WaveguideLoop(name="wg_loop_1", spacing=fibre_array_pich *11, bend_radius=150)
wg_loop_lo_1 = wg_loop_1.Layout()

#chip_elements.append(i3.SRef(name="wg_loop_1", reference=wg_loop_lo_1, position=gc_position))

ring_test = AddDropRingWithElectrode()

ring_test_lo = ring_test.Layout(ring_straight_length=straight_length, # Topology coupler gap
                      coupler_spacing=coupling_gaps, # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length - 250,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_test_in_pos = ring_test_lo.ports['in'].position

first_ring_test_position = (-ring_test_in_pos[0] + bend_radius - 4390, -1500 + 50+33-230)

# Ring
i = 1
gap = coupling_gaps
ring_position = (first_ring_test_position[0] + ring_width_2 * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_test_position[1])
name = "Ring_TEST_G_{}_TOPO_G_{}".format(electrode_gap, gap, topo_gap)
ring_gc_h = RingModulatorGCHiepIden_Test(name=name,
                                ring_position=ring_position,
                                gc_wg_distance=-ring_position[1] - ring_radius - 100 - bend_radius * 2 - waveguide_spacing * 4 * i,
                                ring_wg_distance=bend_radius + 5,
                                bend_radius=bend_radius,
                                coupler_bend_radius=coupler_bend_radius,
                                gc_spacing=fibre_array_pich,
                                waveguide_spacing=waveguide_spacing)
print("ring_position: {}".format(ring_position))
ring_gc_lo_h = ring_gc_h.Layout(ring_radius=ring_radius_test,
                                ring_straight_length=straight_length_test,
                                topo_gap=topo_gap, # Topology coupler gap
                                coupler_spacing=gap,  # Coupler gap
                                coupler_straight_length=coupl_length,
                                coupler_positions=[-straight_length_test * 0.125 -255+ coupl_length,
                                                   straight_length_test * 0.2 + 195 - coupl_length],
                                electrode_length=straight_length_test - 580,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                taper_gap = electrode_gap,
                                with_label=True,
                                label_position=ring_position,
                                label_angle=0,
                                coupler_gap_Hiep=gap,
                                electrode_gap_Hiep=electrode_gap
                                )

#chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich + fibre_array_pich * 4 * i, gc_position[1])))  # Modified

########################################


second_block = i3.LayoutCell(name="second block")
second_block_layout = second_block.Layout(elements=chip_elements)
########################

#



######################################
# III. THIRD BLOCK
#####################################
electrode_gap = 7
chip_elements = []


#######################################
# 1. Sweep the coupling gap - 3rd row
######################################
coupling_gaps = 1.1
topo_gap = 0.75 # Topology coupler gap
change = 150
moving = 250 + change
gc_position = (3130 + moving - 1325-150 + 420 + 55-350-1000+1000, 9250+400-6550)  # Position of the first grating coupler

wg_loop_2 = WaveguideLoop(name="wg_loop_2", spacing=fibre_array_pich * 11, bend_radius=150) #Modified
wg_loop_lo_2 = wg_loop_2.Layout()

chip_elements.append(i3.SRef(name="wg_loop_2", reference=wg_loop_lo_2, position=gc_position))

# Waveguide Hiep # Added
wg_hiep_2 = WaveguideHiep6(name="wg_hiep_2", spacing=fibre_array_pich *10, bend_radius=150) # Added
wg_hiep_lo_2 = wg_hiep_2.Layout() # Added
#chip_elements.append(i3.SRef(name="wg_hiep_2", reference=wg_hiep_lo_2, position=gc_position)) # Added


#
coupler_position08 = (4700, 9250+400-6550)
coupler_position08_2 = (4700+127*2, 9250+400-6550)
coupler_position08_3 = (4700+127, 9250+400-6550)

coupler_test08 = Coupler_Test08(name="coupler_test08", spacing=fibre_array_pich * 11, bend_radius=150) # Added
coupler_test_lo08 = coupler_test08.Layout() # Added
chip_elements.append(i3.SRef(name="coupler_test08", reference=coupler_test_lo08, position=coupler_position08)) # Added

coupler_test08_2 = Coupler_Test08_2(name="coupler_test08_2", spacing=fibre_array_pich * 7, bend_radius=150) # Added
coupler_test_lo08_2 = coupler_test08_2.Layout() # Added
chip_elements.append(i3.SRef(name="coupler_test08_2", reference=coupler_test_lo08_2, position=coupler_position08_2)) # Added

coupler_test08_3 = Coupler_Test08_3(name="coupler_test08_3", spacing=fibre_array_pich*9, bend_radius=150) # Added
coupler_test_lo08_3 = coupler_test08_3.Layout() # Added
chip_elements.append(i3.SRef(name="coupler_test08_3", reference=coupler_test_lo08_3, position=coupler_position08_3)) # Added

#

ring_9_5_GHz = AddDropRingWithElectrodeHiepIden()

ring_9_5_GHz_lo = ring_9_5_GHz.Layout(ring_straight_length=straight_length_2,
                      topo_gap = topo_gap, # Topology coupler gap
                      coupler_spacing=coupling_gaps, # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length_2 - 450,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_9_5_GHz_in_pos = ring_9_5_GHz_lo.ports['in'].position

first_ring_9_5_GHz_position = (-ring_9_5_GHz_in_pos[0] + bend_radius - 3390, -1500 + 153)



# Ring
i = 1
gap = coupling_gaps
ring_position = (first_ring_9_5_GHz_position[0] + ring_width_2 * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_9_5_GHz_position[1])
name = "Ring_9_5GHz_EG_{}G_{}_TOPO_G_{}".format(electrode_gap, gap, topo_gap)
ring_gc_h = RingModulatorGCHiepIden(name=name,
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
                                                   straight_length_2 * 0.2 - 600 -600- coupl_length],
                                electrode_length=straight_length_2 - 950,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                taper_gap = electrode_gap,
                                with_label=True,
                                label_position=ring_position,
                                label_angle=0,
                                coupler_gap_Hiep=gap,
                                electrode_gap_Hiep=electrode_gap
                                )



chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich + fibre_array_pich * 4 * i, gc_position[1])))  # Modified


third_block = i3.LayoutCell(name="third block")
third_block_layout = third_block.Layout(elements=chip_elements)

##########################################
# III. FORTH BLOCK
chip_elements = []
# RING TEST
##########################################
change = 150
moving = 250 + change
gc_position = (3130 + moving - 1325-150 + 420 + 55-350-1000, 9250+400-6550+40+230)

wg_loop_1 = WaveguideLoop(name="wg_loop_1", spacing=fibre_array_pich *11, bend_radius=150)
wg_loop_lo_1 = wg_loop_1.Layout()

chip_elements.append(i3.SRef(name="wg_loop_1", reference=wg_loop_lo_1, position=gc_position))

ring_test = AddDropRingWithElectrode()

ring_test_lo = ring_test.Layout(ring_straight_length=straight_length, # Topology coupler gap
                      coupler_spacing=coupling_gaps, # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length - 250,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_test_in_pos = ring_test_lo.ports['in'].position

first_ring_test_position = (-ring_test_in_pos[0] + bend_radius - 4390, -1500 + 50+33-230)

# Ring
i = 1
gap = coupling_gaps
ring_position = (first_ring_test_position[0] + ring_width_2 * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_test_position[1])
name = "Ring_TEST_EG_{}G_{}_TOPO_G_{}".format(electrode_gap, gap, topo_gap)
ring_gc_h = RingModulatorGCHiepIden_Test(name=name,
                                ring_position=ring_position,
                                gc_wg_distance=-ring_position[1] - ring_radius - 100 - bend_radius * 2 - waveguide_spacing * 4 * i,
                                ring_wg_distance=bend_radius + 5,
                                bend_radius=bend_radius,
                                coupler_bend_radius=coupler_bend_radius,
                                gc_spacing=fibre_array_pich,
                                waveguide_spacing=waveguide_spacing)
print("ring_position: {}".format(ring_position))
ring_gc_lo_h = ring_gc_h.Layout(ring_radius=ring_radius_test,
                                ring_straight_length=straight_length_test,
                                topo_gap=topo_gap, # Topology coupler gap
                                coupler_spacing=gap,  # Coupler gap
                                coupler_straight_length=coupl_length,
                                coupler_positions=[-straight_length_test * 0.125 -255+ coupl_length,
                                                   straight_length_test * 0.2 + 195 - coupl_length],
                                electrode_length=straight_length_test - 580,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                taper_gap = electrode_gap,
                                with_label=True,
                                label_position=ring_position,
                                label_angle=0,
                                coupler_gap_Hiep=gap,
                                electrode_gap_Hiep=electrode_gap
                                )

chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich + fibre_array_pich * 4 * i, gc_position[1])))  # Modified

########################################
fourth_block = i3.LayoutCell(name="fourth block")
fourth_block_layout = fourth_block.Layout(elements=chip_elements)


##########################################
# III. FIFTH BLOCK # TASNEEM DEVICE
chip_elements = []


gc_position = (10200, 5900)

name = "TASNEEM"
tasneem_grating = Tasneem_Grating()
tasneem_grating_lo = tasneem_grating.Layout()
#
chip_elements.append(i3.SRef(reference=BraggGrating_circuit_1_layout, position=(9200.0, 4900+250)))
chip_elements.append(i3.SRef(reference=BraggGrating_circuit_2_layout, position=(9200.0, 4900+330)))
chip_elements.append(i3.SRef(reference=BraggGrating_circuit_3_layout, position=(9200.0, 4900+410)))
chip_elements.append(i3.SRef(reference=BraggGrating_circuit_4_layout, position=(9200.0, 4900+490)))
chip_elements.append(i3.SRef(reference=BraggGrating_circuit_5_layout, position=(9200.0, 4900+570)))
chip_elements.append(i3.SRef(reference=BraggGrating_circuit_6_layout, position=(9200.0, 4900+650)))
chip_elements.append(i3.SRef(reference=BraggGrating_circuit_7_layout, position=(9200.0, 4900+730)))
chip_elements.append(i3.SRef(reference=BraggGrating_circuit_8_layout, position=(9200.0, 4900+810)))
chip_elements.append(i3.SRef(reference=ground_wire_down_lo_strength, position=(9100+186, 4900+810)))
chip_elements.append(i3.SRef(reference=ground_wire_up_lo_strength, position=(9100+186, 4900+250+970)))
# chip_elements.append(i3.SRef(reference=Out_pad_lo_strength, position=(9100+400, 4900-700)))
# chip_elements.append(i3.SRef(reference=Out_pad_lo_strength, position=(9100+600, 4900-700)))
# chip_elements.append(i3.SRef(reference=Out_pad_lo_strength, position=(9100+800, 4900-700)))
# chip_elements.append(i3.SRef(reference=Out_pad_lo_strength, position=(9100+200, 4900-700)))
chip_elements.append(i3.SRef(reference=Out_pad_lo_strength, position=(9100+400, 4900-700)))
chip_elements.append(i3.SRef(reference=Out_pad_lo_strength, position=(9100+600, 4900-700)))
chip_elements.append(i3.SRef(reference=Out_pad_lo_strength, position=(9100+800, 4900-700)))
chip_elements.append(i3.SRef(reference=Out_pad_lo_strength, position=(9100+1010, 4900-700)))
chip_elements.append(i3.SRef(reference=Out_pad_lo_strength, position=(9100+400, 4900+250+980)))
chip_elements.append(i3.SRef(reference=Out_pad_lo_strength, position=(9100+600, 4900+250+980)))
chip_elements.append(i3.SRef(reference=Out_pad_lo_strength, position=(9100+800, 4900+250+980)))
chip_elements.append(i3.SRef(reference=Out_pad_lo_strength, position=(9100+1010, 4900+250+980)))

# chip_elements.append(i3.SRef(reference=plus_wire1_lo_strength, position=(9100+400, 4900-700)))
# chip_elements.append(i3.SRef(reference=plus_wire2_lo_strength, position=(9100+600, 4900-700)))
# chip_elements.append(i3.SRef(reference=plus_wire3_lo_strength, position=(9100+800, 4900-700)))

chip_elements.append(i3.SRef(reference=plus_wire1_lo_strength, position=(9100+400, 4900-700)))
chip_elements.append(i3.SRef(reference=plus_wire2_lo_strength, position=(9100+600, 4900-700)))
chip_elements.append(i3.SRef(reference=plus_wire3_lo_strength, position=(9100+800, 4900-700)))
chip_elements.append(i3.SRef(reference=plus_wire4_lo_strength, position=(9100+1010, 4900-700)))
chip_elements.append(i3.SRef(reference=plus_wire8_lo_strength, position=(9100+400, 4900+250+980)))
chip_elements.append(i3.SRef(reference=plus_wire7_lo_strength, position=(9100+600, 4900+250+980)))
chip_elements.append(i3.SRef(reference=plus_wire6_lo_strength, position=(9100+800, 4900+250+980)))
chip_elements.append(i3.SRef(reference=plus_wire5_lo_strength, position=(9100+1010, 4900+250+980)))
#
chip_elements.append(i3.SRef(reference=BraggGrating_circuit_1_layout_period, position=(10200.0, 4900+250)))
chip_elements.append(i3.SRef(reference=BraggGrating_circuit_2_layout_period, position=(10200.0, 4900+330)))
chip_elements.append(i3.SRef(reference=BraggGrating_circuit_3_layout_period, position=(10200.0, 4900+410)))
chip_elements.append(i3.SRef(reference=BraggGrating_circuit_4_layout_period, position=(10200.0, 4900+490)))
chip_elements.append(i3.SRef(reference=BraggGrating_circuit_5_layout_period, position=(10200.0, 4900+570)))
chip_elements.append(i3.SRef(reference=BraggGrating_circuit_6_layout_period, position=(10200.0, 4900+650)))
chip_elements.append(i3.SRef(reference=BraggGrating_circuit_7_layout_period, position=(10200.0, 4900+730)))
chip_elements.append(i3.SRef(reference=BraggGrating_circuit_8_layout_period, position=(10200.0, 4900+810)))
chip_elements.append(i3.SRef(reference=ground_wire_down_lo_period, position=(10100+186, 4900+810)))
chip_elements.append(i3.SRef(reference=ground_wire_up_lo_period, position=(10100+186, 4900+250+970)))

# chip_elements.append(i3.SRef(reference=Out_pad_lo_period, position=(10100+400, 4900-700)))
# chip_elements.append(i3.SRef(reference=Out_pad_lo_period, position=(10100+600, 4900-700)))
# chip_elements.append(i3.SRef(reference=Out_pad_lo_period, position=(10100+800, 4900-700)))

# chip_elements.append(i3.SRef(reference=Out_pad_lo_period, position=(10100+200, 4900-700)))
chip_elements.append(i3.SRef(reference=Out_pad_lo_period, position=(10100+400, 4900-700)))
chip_elements.append(i3.SRef(reference=Out_pad_lo_period, position=(10100+600, 4900-700)))
chip_elements.append(i3.SRef(reference=Out_pad_lo_period, position=(10100+800, 4900-700)))
chip_elements.append(i3.SRef(reference=Out_pad_lo_period, position=(10100+1010, 4900-700)))
chip_elements.append(i3.SRef(reference=Out_pad_lo_period, position=(10100+400, 4900+250+980)))
chip_elements.append(i3.SRef(reference=Out_pad_lo_period, position=(10100+600, 4900+250+980)))
chip_elements.append(i3.SRef(reference=Out_pad_lo_period, position=(10100+800, 4900+250+980)))
chip_elements.append(i3.SRef(reference=Out_pad_lo_period, position=(10100+1010, 4900+250+980)))

# chip_elements.append(i3.SRef(reference=plus_wire1_lo_period, position=(10100+400, 4900-700)))
# chip_elements.append(i3.SRef(reference=plus_wire2_lo_period, position=(10100+600, 4900-700)))
# chip_elements.append(i3.SRef(reference=plus_wire3_lo_period, position=(10100+800, 4900-700)))
chip_elements.append(i3.SRef(reference=plus_wire1_lo_period, position=(10100+400, 4900-700)))
chip_elements.append(i3.SRef(reference=plus_wire2_lo_period, position=(10100+600, 4900-700)))
chip_elements.append(i3.SRef(reference=plus_wire3_lo_period, position=(10100+800, 4900-700)))
chip_elements.append(i3.SRef(reference=plus_wire4_lo_period, position=(10100+1010, 4900-700)))
chip_elements.append(i3.SRef(reference=plus_wire8_lo_period, position=(10100+400, 4900+250+980)))
chip_elements.append(i3.SRef(reference=plus_wire7_lo_period, position=(10100+600, 4900+250+980)))
chip_elements.append(i3.SRef(reference=plus_wire6_lo_period, position=(10100+800, 4900+250+980)))
chip_elements.append(i3.SRef(reference=plus_wire5_lo_period, position=(10100+1010, 4900+250+980)))




########################################
fifth_block = i3.LayoutCell(name="fifth block")
fifth_block_layout = fifth_block.Layout(elements=chip_elements)


####################################
# Generate the main layout
####################################
chip_design = i3.LayoutCell()
chip_layout = chip_design.Layout(elements=[
                                        i3.SRef(name="E_GAP_6um", reference=first_block_layout, position=(0, 0)),
                                          i3.SRef(name="E_GAP_6um", reference=second_block_layout, position=(0, 0)),
                                         i3.SRef(name="E_GAP_6um", reference=third_block_layout, transformation= i3.HMirror() + i3.Translation(translation=(13000,0)) + i3.VMirror() + i3.Translation(translation=(0,4000))),
                                        # i3.SRef(name="E_GAP_6um", reference=fifth_block_layout,position=(0, 0)),

])


chip_layout.write_gdsii("gds_output/two_chips_iden_with_heaters_1.06.gds")