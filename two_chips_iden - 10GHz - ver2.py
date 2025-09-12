import sys

# Need to update the folder that contains asp_sin_lnoi_photonics/ipkiss


# sys.path.append("C:/pdk/asp_sin_lnoi_photonics/ipkiss")
# sys.path.append("H:/GitHub/asp_sin_lnoi_photonics/ipkiss")
# sys.path.append("D:/RMITRaceHubDataHiepDX/PDKs/asp_sin_lnoi_photonics/ipkiss")
sys.path.append("C:/Users/Administrator/Documents/GitHub/pdk/asp_sin_lnoi_photonics/ipkiss")

import asp_sin_lnoi_photonics.technology
import asp_sin_lnoi_photonics.all as asp
import ipkiss3.all as i3
import numpy as np



from ring_gc_h_iden.cell import RingModulatorGCHiepIden_heater_changed_Euler
from ring_gc_h_iden_heater_changed.cell import RingModulatorGCHiepIden_heater_changed_v2_op2_Euler
from ring_modulator_h_iden_heater_changed.cell import AddDropRingWithElectrodeHiepIden_heater_changed_v2_op2_Euler, AddDropRingWithElectrodeHiepIden_heater_changed_Euler
from waveguide_loop.cell import WaveguideLoop

from ring_modulator import AddDropRingWithElectrode, AddDropRingWithOutElectrode
from ring_gc import RingModulatorGC, RingModulatorGC_NoElectrode, RingModulatorGC_NoElectrode_2
#######################################
# Global parameters
######################################
waveguide_spacing = 50 # spacing between adjacent waveguides
bend_radius = 180  # Bending radius used in waveguide routing
coupler_bend_radius = 200
hot_electrode_width = 40
hot_electrode_width_hiep = 50
fibre_array_pich = 127
ebl_writing_size = (1000, 1000)
chip_elements = list()


#### Calculate ring parameters ########## for Circular bend
def ring_straight_length(radius, ng, fsr):
    ring_length = 3e8 / (fsr * 1e9) / ng
    return int((ring_length - 2.0 * np.pi * radius * 1e-6) / 2 * 1e6)

#### Calculate ring parameters ########## for Euler bend
def ring_straight_length_euler(euler_bend_length, delta_topology, ng, fsr):
    ring_length = 3e8 / (fsr * 1e9) / ng
    return int((ring_length - 2.0 * euler_bend_length * 1e-6 - delta_topology* 1e-6) / 2 * 1e6)

delta_topology_calculated = 3.65

delta_topology_calculated_v2_op2 = 35.6

ring_radius = 200
coupl_length = 100

topo_coupl_length = 37
ng = 2.234

euler_bend_length_calculated = 942.4772415892692

ring_radius_test = 150


fsr = 20  # in GHz

fsr_2 = 10 # in GHz

fsr_test = 10 # in GHz

fsr_ring_test = 20

straight_length = ring_straight_length_euler(euler_bend_length_calculated, delta_topology_calculated, ng, fsr)
ring_width = straight_length + ring_radius * 2

straight_length_2 = ring_straight_length_euler(euler_bend_length_calculated, delta_topology_calculated, ng, fsr_2)
ring_width_2 = straight_length + ring_radius * 2

straight_length_test = ring_straight_length_euler(euler_bend_length_calculated, delta_topology_calculated_v2_op2, ng, fsr_test)
ring_width_test = straight_length + ring_radius * 2

straight_length_ring_test = ring_straight_length_euler(euler_bend_length_calculated, delta_topology_calculated, ng, fsr_ring_test)
ring_width_ring_test = straight_length_ring_test + ring_radius * 2


print("Ring straight length: {}".format(straight_length))

print("Ring straight length FSR-9.5GHz: {}".format(straight_length_2))

print("Ring straight length FSR-10GHz: {}".format(straight_length_test))

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
coupling_gaps = 1.25
topo_gap = 1.0 # Topology coupler gap
change = 150
moving = 250 + change
gc_position = (3130 + moving - 1325-150 + 420 + 55-350-1000, 9250+390-60-25-185-185-45)  # Position of the first grating coupler

#Waveguide loop
wg_loop_1 = WaveguideLoop(name="wg_loop_1", spacing=fibre_array_pich *11, bend_radius=150)
wg_loop_lo_1 = wg_loop_1.Layout()

chip_elements.append(i3.SRef(name="wg_loop_1", reference=wg_loop_lo_1, position=gc_position, transformation=i3.Translation((10184-46-20-127*7, -619.5+480+20+20))))

ring_9_5_GHz = AddDropRingWithElectrodeHiepIden_heater_changed_v2_op2_Euler()

ring_9_5_GHz_lo = ring_9_5_GHz.Layout(ring_straight_length=straight_length_2,
                      topo_gap = topo_gap, # Topology coupler gap
                      coupler_spacing=coupling_gaps, # Coupler gap
                      coupler_straight_length=coupl_length,
                      topo_coupler_straight_length=topo_coupl_length,
                      electrode_length=straight_length_2 - 250,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_9_5_GHz_in_pos = ring_9_5_GHz_lo.ports['in'].position

first_ring_9_5_GHz_position = (-ring_9_5_GHz_in_pos[0] + bend_radius - 3390+3000-110+1000, -1500 + 50+63+25+20+50+25)

# Ring
i = 1
gap = coupling_gaps
ring_position = (first_ring_9_5_GHz_position[0] + ring_width_2 * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_9_5_GHz_position[1]-40)
name = "Ring_9_5GHz_EG_{}G_{}_TOPO_G_{}_V2_OP1".format(electrode_gap, gap, topo_gap)
ring_gc_h = RingModulatorGCHiepIden_heater_changed_v2_op2_Euler(name=name,
                                ring_position=ring_position,
                                gc_wg_distance=-ring_position[1] - ring_radius - 100 - bend_radius * 2 - waveguide_spacing * 4 * i,
                                ring_wg_distance=bend_radius + 5,
                                coupler_bend_radius=coupler_bend_radius,
                                bend_radius=bend_radius,
                                gc_spacing=fibre_array_pich,
                                waveguide_spacing=waveguide_spacing)
print("ring_position: {}".format(ring_position))
ring_gc_lo_h = ring_gc_h.Layout(ring_radius=ring_radius,
                                ring_straight_length=straight_length_test,
                                topo_gap = topo_gap, # Topology coupler gap
                                coupler_spacing=gap,  # Coupler gap
                                coupler_straight_length=coupl_length,
                                topo_coupler_straight_length=topo_coupl_length,
                                coupler_positions=[-straight_length_test * 0.125 - 510 -650+ coupl_length-500+150+450-40,
                                                   straight_length_test * 0.2 - 600 -600 - coupl_length-500-60],
                                electrode_length=straight_length_test - 950-120,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                taper_gap = electrode_gap,
                                with_label=True,
                                label_position=(ring_position[0], ring_position[1] + 105),
                                label_angle=0,
                                coupler_gap_Hiep=gap,
                                electrode_gap_Hiep=electrode_gap
                                )

chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich + fibre_array_pich * 4 * i-4, gc_position[1]), transformation=i3.HMirror()+ i3.Translation((10184-20, -619.5+480+20+20))))  # Modified

first_block = i3.LayoutCell(name="first_block")
first_block_layout = first_block.Layout(elements=chip_elements)

########################
# II. SECOND BLOCK
########################
electrode_gap = 7
chip_elements = []
########################
########################
coupling_gaps = 1.25

topo_gap = 1.0 # Topology coupler gap

change = 150
moving = 250 + change
gc_position = (3130 + moving - 1325-150 + 420 + 55-350-1000, 9250+400-3000-295-65+100-250)  # Position of the first grating coupler

#Waveguide loop
wg_loop_1 = WaveguideLoop(name="wg_loop_1", spacing=fibre_array_pich *11, bend_radius=150)
wg_loop_lo_1 = wg_loop_1.Layout()

chip_elements.append(i3.SRef(name="wg_loop_1", reference=wg_loop_lo_1, position=(gc_position[0], gc_position[1]-30-10)))
################

ring_9_5_GHz = AddDropRingWithElectrodeHiepIden_heater_changed_Euler()

ring_9_5_GHz_lo = ring_9_5_GHz.Layout(ring_straight_length=straight_length_2,
                      topo_gap = topo_gap, # Topology coupler gap
                      coupler_spacing=coupling_gaps, # Coupler gap
                      coupler_straight_length=coupl_length,
                      topo_coupler_straight_length=topo_coupl_length,
                      electrode_length=straight_length_2 - 250,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_9_5_GHz_in_pos = ring_9_5_GHz_lo.ports['in'].position

first_ring_9_5_GHz_position = (-ring_9_5_GHz_in_pos[0] + bend_radius - 3390+3000-110+1000, -1500 + 50-187+250+25+20+50+25+10)

# Ring
i = 1
gap = coupling_gaps
ring_position = (first_ring_9_5_GHz_position[0] + ring_width_2 * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_9_5_GHz_position[1])
name = "Ring_9_5GHz_EG_{}G_{}_TOPO_G_{}".format(electrode_gap, gap, topo_gap)
ring_gc_h = RingModulatorGCHiepIden_heater_changed_Euler(name=name,
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
                                topo_coupler_straight_length=topo_coupl_length,
                                coupler_positions=[-straight_length_2 * 0.125 - 510 -650+ coupl_length-500+400+30+155-90,
                                                   straight_length_2 * 0.2 - 600 -600 - coupl_length-500-47],
                                electrode_length=straight_length_2 - 950-120,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                taper_gap = electrode_gap,
                                with_label=True,
                                label_position=(ring_position[0], ring_position[1] + 105),
                                label_angle=0,
                                coupler_gap_Hiep=gap,
                                electrode_gap_Hiep=electrode_gap
                                )

chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich + fibre_array_pich * 4 * i-4, gc_position[1]-30-10)))  # Modified


second_block = i3.LayoutCell(name="second block")
second_block_layout = second_block.Layout(elements=chip_elements)



######################################
#I. FOURTH BLOCK
######################################
electrode_gap = 7
chip_elements = []
######################################

coupling_gaps = 1.25
topo_gap = 1.05 # Topology coupler gap
change = 150
moving = 250 + change
gc_position = (3130 + moving - 1325-150 + 420 + 55-350-1000, 9250+390-60-25-185-185-45+500)  # Position of the first grating coupler

#Waveguide loop
wg_loop_1 = WaveguideLoop(name="wg_loop_1", spacing=fibre_array_pich *11, bend_radius=150)
wg_loop_lo_1 = wg_loop_1.Layout()

chip_elements.append(i3.SRef(name="wg_loop_1", reference=wg_loop_lo_1, position=gc_position, transformation=i3.Translation((10184-46-20-127*7, -619.5+500-30-10))))

#
ring_9_5_GHz = AddDropRingWithElectrodeHiepIden_heater_changed_Euler()

ring_9_5_GHz_lo = ring_9_5_GHz.Layout(ring_straight_length=straight_length_2,
                      topo_gap = topo_gap, # Topology coupler gap
                      coupler_spacing=coupling_gaps, # Coupler gap
                      coupler_straight_length=coupl_length,
                      topo_coupler_straight_length=topo_coupl_length,
                      electrode_length=straight_length_2 - 250,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_9_5_GHz_in_pos = ring_9_5_GHz_lo.ports['in'].position

first_ring_9_5_GHz_position = (-ring_9_5_GHz_in_pos[0] + bend_radius - 3390+3000-110+1000, -1500 + 50+63+25+20+50+25+10)

# Ring
i = 1
gap = coupling_gaps
ring_position = (first_ring_9_5_GHz_position[0] + ring_width_2 * i - fibre_array_pich * 4 * i + waveguide_spacing * i, first_ring_9_5_GHz_position[1])
name = "Ring_9_5GHz_EG_{}G_{}_TOPO_G_{}".format(electrode_gap, gap, topo_gap)
ring_gc_h = RingModulatorGCHiepIden_heater_changed_Euler(name=name,
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
                                topo_coupler_straight_length=topo_coupl_length,
                                coupler_positions=[-straight_length_2 * 0.125 - 510 -650+ coupl_length-500+400+30+155-90,
                                                   straight_length_2 * 0.2 - 600 -600 - coupl_length-500-47],
                                electrode_length=straight_length_2 - 950-120,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                taper_gap = electrode_gap,
                                with_label=True,
                                label_position=(ring_position[0], ring_position[1] + 105),
                                label_angle=0,
                                coupler_gap_Hiep=gap,
                                electrode_gap_Hiep=electrode_gap
                                )

chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich + fibre_array_pich * 4 * i-4, gc_position[1]), transformation=i3.HMirror()+ i3.Translation((10184-20, -619.5+500-30-10))))  # Modified



fourth_block = i3.LayoutCell(name="fourth_block")
fourth_block_layout = fourth_block.Layout(elements=chip_elements)

######################################################################
# FIFTH BLOCK
######################################################################
electrode_gap = 7
chip_elements = []
####################
# RING TEST
####################
coupling_gaps = 1.25
topo_gap =0.7

change = 150
moving = 250 + change


############

gc_position = (3130 + moving - 1325-150 + 420 + 55-1000-127*2-450+4900-350+127*6-450,  9250+400-3000-295-65-300+50+450-3000+250)  # Position of the first grating coupler

#Waveguide loop
wg_loop_2 = WaveguideLoop(name="wg_loop_2_test_3", spacing=fibre_array_pich *5, bend_radius=150)
wg_loop_lo_2 = wg_loop_2.Layout()

chip_elements.append(i3.SRef(name="wg_loop_2_test_3", reference=wg_loop_lo_2, position=(gc_position[0], gc_position[1]+850), transformation=i3.VMirror()))

##############

ring_19_GHz = AddDropRingWithElectrode()

ring_19_GHz_lo = ring_19_GHz.Layout(ring_straight_length=straight_length_test,
                      coupler_spacing=coupling_gaps, # Coupler gap
                      coupler_straight_length=0,
                      electrode_length=straight_length_ring_test - 250,
                      hot_width=hot_electrode_width,
                      electrode_gap=electrode_gap
                      )

ring_19_GHz_in_pos = ring_19_GHz_lo.ports['in'].position

first_ring_19_GHz_position = (-ring_19_GHz_in_pos[0] + bend_radius - 4500-800-800+1100-60 + 3000-2000+2500-350-3000-1450+115, -1500 + 50-895+25-50-450+1600)

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
                                ring_straight_length=straight_length_ring_test,
                                coupler_spacing=gap,  # Coupler gap
                                coupler_straight_length=coupl_length,
                                coupler_positions=[-straight_length_ring_test * 0.125 - 150 + coupl_length+250-25-450,
                                                   straight_length_ring_test * 0.2 - coupl_length+250-25],
                                electrode_length=straight_length_ring_test - 150,
                                hot_width=hot_electrode_width,
                                electrode_gap=electrode_gap,
                                # with_label=True,
                                # label_position=ring_position,
                                # label_angle=0,
                                # coupler_gap_Hiep=gap,
                                # electrode_gap_Hiep=electrode_gap
                                )

chip_elements.append(i3.SRef(name=name, reference=ring_gc_h, position=(gc_position[0] - moving + fibre_array_pich * 4 * i +19, gc_position[1] + 850), transformation=i3.VMirror()))  # Modified


##############
fifth_block = i3.LayoutCell(name="Fifth block")
fifth_block_layout = fifth_block.Layout(elements=chip_elements)
###############################################################
######################################################################

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
                             ,transformation=(i3.Rotation(rotation_center=(0.0, 0.0), rotation=-90.0, magnification=5)
                                              )))  # Modified
####
#
##############
sixth_block = i3.LayoutCell(name="Sixth block")
sixth_block_layout = sixth_block.Layout(elements=chip_elements)
###############################################################

####################################
# Generate the main layout
####################################
chip_design = i3.LayoutCell()
chip_layout = chip_design.Layout(elements=[
                                        i3.SRef(name="E_GAP_6um", reference=first_block_layout, position=(0, 0)),
                                        i3.SRef(name="E_GAP_6um", reference=second_block_layout, position=(0, 384-3.5)),
                                        i3.SRef(name="E_GAP_6um", reference=fourth_block_layout, position=(0, 0), transformation=i3.HMirror(mirror_plane_x=5000+1425+127/2)+i3.Translation((0, -6000))),
                                        i3.SRef(name="E_GAP_6um", reference=fifth_block_layout, position=(-2000+250 + 6360-560-400-8300+150, +3250-150-5350+40+384-72+4500)),
                                        i3.SRef(name="E_GAP_6um", reference=fifth_block_layout, position=(0, -2400), transformation=i3.HMirror()+i3.Translation((17500,0))),
                                        i3.SRef(name="E_GAP_6um", reference=sixth_block_layout, position=(9500, 2000)),

])

chip_layout.write_gdsii("gds_output/two_euler_chips_iden_10GHz_with_heaters_1.40_v1.gds")