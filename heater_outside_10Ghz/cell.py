
import sys
sys.path.append("H:/GitHub/asp_sin_lnoi_photonics/ipkiss")

import numpy as np
import ipkiss3.all as i3
import asp_sin_lnoi_photonics.all as asp
from ipkiss3.geometry.shapes.euler import _partial_euler

from ipkiss3.pcell.wiring import ElectricalWire
wire_tmpl = asp.MetalWireTemplate()
wire_tmpl_layout = wire_tmpl.Layout(width=40.0)

#electric_wire_length = 550
#hiep_wire = ElectricalWire(trace_template=wire_tmpl)
#hiep_wire_layout = hiep_wire.Layout(shape=[(0, 0), (0, electric_wire_length)])
#hiep_wire_layout.visualize()

class ElectricalPad_20x20(i3.PCell):

    """
    A rectangular electrical pad
    """

    class Layout(i3.LayoutView):
        size = i3.Size2Property(default=(97.5, 95.0))
        layer = i3.LayerProperty(default=i3.TECH.PPLAYER.PAD, locked=True)


        def _generate_elements(self, elems):
            elems += i3.Rectangle(layer=self.layer, box_size=self.size)
            return elems

        def _generate_ports(self, ports):
            ports += i3.ElectricalPort(name="m1", position=(0.0, 0.0), shape=self.size, process=self.layer.process)
            return ports

    class Netlist(i3.NetlistFromLayout):
        pass

class ElectricalPad_20x20_top(i3.PCell):

    """
    A rectangular electrical pad
    """

    class Layout(i3.LayoutView):
        size = i3.Size2Property(default=(60.0, 100.0))
        layer = i3.LayerProperty(default=i3.TECH.PPLAYER.PAD, locked=True)
        electrode_length = i3.PositiveNumberProperty(default=3000.0, doc="the length of the electrode")
        taper_length = i3.PositiveNumberProperty(default=100.0, doc="the length of the taper")
        hot_width = i3.PositiveNumberProperty(default=23.0, doc="width of the hot electrode")
        ground_width = i3.PositiveNumberProperty(default=100.0, doc="width of the ground planes")
        ground_width_mod = i3.PositiveNumberProperty(default=100.0, doc="width of the ground planes")
        electrode_gap = i3.PositiveNumberProperty(default=7.0, doc="gap between hot electrode and ground plane")
        hot_taper_width = i3.PositiveNumberProperty(default=50.0, doc="width of the hot electrode at the end of the taper")
        ground_taper_width = i3.PositiveNumberProperty(default=5.0,
                                                    doc="width of the hot electrode at the end of the taper")
        taper_gap = i3.PositiveNumberProperty(default=20.0,
                                                    doc="gap between hot electrode and ground plane at the end of the taper")
        taper_straight_length = i3.PositiveNumberProperty(default=10.0, doc="length of the straight section at the end of the taper")


        def _generate_elements(self, elems):
            grnd_taper_shape3 = i3.ShapeRound(
                original_shape=[(-self.electrode_length * 0.5, -self.hot_width * 0.5 - self.electrode_gap-2.5),
                                (-self.electrode_length * 0.5 - self.taper_straight_length,
                                -self.hot_width * 0.5 - self.electrode_gap-2.5),
                                (-self.electrode_length * 0.5 - self.taper_length + self.taper_straight_length,
                                    -self.hot_width * 0.5 - self.taper_gap-25-3.5),
                                (-self.electrode_length * 0.5 - self.taper_length+2.5,
                                 -self.hot_width * 0.5 - self.taper_gap-25-3.5)
                                ],
                radius = 25.0,
                )

            grnd_taper_shape4 = i3.Shape(points=[(-self.electrode_length * 0.5 - self.taper_length+2.5,
                                                  -self.hot_width * 0.5 - self.electrode_gap - self.ground_width+2.5),
                                                 (-self.electrode_length * 0.5,
                                                  -self.hot_width * 0.5 - self.electrode_gap - self.ground_width+2.5)])

            bottom_grnd_taper_shape = grnd_taper_shape3 + grnd_taper_shape4 #+ grnd_taper_shape4.h_mirror_copy().reverse() + grnd_taper_shape3.h_mirror_copy().reverse()
            bottom_grnd_taper_shape.close()
            elems += i3.Boundary(layer=self.layer, shape=bottom_grnd_taper_shape)
            return elems

        def _generate_ports(self, ports):
            ports += i3.ElectricalPort(name="m1", position=(0.0, 0.0), shape=self.size, process=self.layer.process)
            return ports
    class Netlist(i3.NetlistFromLayout):
        pass

class ElectricalPad_20x20_top_reverse(i3.PCell):

    """
    A rectangular electrical pad
    """

    class Layout(i3.LayoutView):
        size = i3.Size2Property(default=(60.0, 100.0))
        layer = i3.LayerProperty(default=i3.TECH.PPLAYER.PAD, locked=True)
        electrode_length = i3.PositiveNumberProperty(default=3000.0, doc="the length of the electrode")
        taper_length = i3.PositiveNumberProperty(default=100.0, doc="the length of the taper")
        hot_width = i3.PositiveNumberProperty(default=23.0, doc="width of the hot electrode")
        ground_width = i3.PositiveNumberProperty(default=100.0, doc="width of the ground planes")
        ground_width_mod = i3.PositiveNumberProperty(default=100.0, doc="width of the ground planes")
        electrode_gap = i3.PositiveNumberProperty(default=7.0, doc="gap between hot electrode and ground plane")
        hot_taper_width = i3.PositiveNumberProperty(default=50.0, doc="width of the hot electrode at the end of the taper")
        ground_taper_width = i3.PositiveNumberProperty(default=5.0,
                                                    doc="width of the hot electrode at the end of the taper")
        taper_gap = i3.PositiveNumberProperty(default=20.0,
                                                    doc="gap between hot electrode and ground plane at the end of the taper")
        taper_straight_length = i3.PositiveNumberProperty(default=10.0, doc="length of the straight section at the end of the taper")


        def _generate_elements(self, elems):
            grnd_taper_shape3 = i3.ShapeRound(
                original_shape=[(-self.electrode_length * 0.5, -self.hot_width * 0.5 - self.electrode_gap-2.5),
                                (-self.electrode_length * 0.5 - self.taper_straight_length,
                                -self.hot_width * 0.5 - self.electrode_gap-2.5),
                                (-self.electrode_length * 0.5 - self.taper_length + self.taper_straight_length,
                                    -self.hot_width * 0.5 - self.taper_gap-25-3.5),
                                (-self.electrode_length * 0.5 - self.taper_length+2.5,
                                 -self.hot_width * 0.5 - self.taper_gap-25-3.5)
                                ],
                radius = 25.0,
                )

            grnd_taper_shape4 = i3.Shape(points=[(-self.electrode_length * 0.5 - self.taper_length+2.5,
                                                  -self.hot_width * 0.5 - self.electrode_gap - self.ground_width+2.5),
                                                 (-self.electrode_length * 0.5,
                                                  -self.hot_width * 0.5 - self.electrode_gap - self.ground_width+2.5)])

            bottom_grnd_taper_shape = grnd_taper_shape4.h_mirror_copy().reverse() + grnd_taper_shape3.h_mirror_copy().reverse()
            bottom_grnd_taper_shape.close()
            elems += i3.Boundary(layer=self.layer, shape=bottom_grnd_taper_shape)
            return elems

        def _generate_ports(self, ports):
            ports += i3.ElectricalPort(name="m1", position=(0.0, 0.0), shape=self.size, process=self.layer.process)
            return ports
    class Netlist(i3.NetlistFromLayout):
        pass

class ElectricalPad_20x20_Mod(i3.PCell):

    """
    A rectangular electrical pad
    """

    class Layout(i3.LayoutView):
        size = i3.Size2Property(default=(60.0, 40.0))
        layer = i3.LayerProperty(default=i3.TECH.PPLAYER.PAD, locked=True)
        electrode_length = i3.PositiveNumberProperty(default=3000.0, doc="the length of the electrode")
        taper_length = i3.PositiveNumberProperty(default=100.0, doc="the length of the taper")
        hot_width = i3.PositiveNumberProperty(default=23.0, doc="width of the hot electrode")
        ground_width = i3.PositiveNumberProperty(default=100.0, doc="width of the ground planes")
        ground_width_mod = i3.PositiveNumberProperty(default=100.0, doc="width of the ground planes")
        electrode_gap = i3.PositiveNumberProperty(default=7.0, doc="gap between hot electrode and ground plane")
        hot_taper_width = i3.PositiveNumberProperty(default=50.0, doc="width of the hot electrode at the end of the taper")
        ground_taper_width = i3.PositiveNumberProperty(default=5.0,
                                                    doc="width of the hot electrode at the end of the taper")
        taper_gap = i3.PositiveNumberProperty(default=20.0,
                                                    doc="gap between hot electrode and ground plane at the end of the taper")
        taper_straight_length = i3.PositiveNumberProperty(default=10.0, doc="length of the straight section at the end of the taper")



        def _generate_elements(self, elems):
            he_taper_shape1 = i3.Shape(points=[(-self.electrode_length * 0.5, self.hot_width * 0.5 - 2.5),
                                                           (-self.electrode_length * 0.5 - self.taper_straight_length,#- self.taper_length,
                                                            self.hot_width * 0.5- 2.5)
                                                           ],
                                           )

            he_taper_shape2 = i3.Shape(points=[(-self.electrode_length * 0.5 - self.taper_length+self.taper_straight_length,
                                                            +self.hot_width * 0.5 - self.hot_taper_width*0.2- 2.5),
                                                            (-self.electrode_length * 0.5 - self.taper_length + 2.5,
                                                            +self.hot_width * 0.5 - self.hot_taper_width*0.2- 2.5),
                                                            (-self.electrode_length * 0.5 - self.taper_length +2.5,
                                                             +self.hot_width * 0.5 - self.hot_taper_width+ 2.5),
                                                            (-self.electrode_length * 0.5 - self.taper_length+self.taper_straight_length,
                                                            +self.hot_width * 0.5 - self.hot_taper_width+ 2.5),
                                                            # (-self.electrode_length * 0.5, -self.hot_width * 0.5),
                                                            # (-self.electrode_length * 0.5, -self.hot_width * 0.5),
                                                            (-self.electrode_length * 0.5 - self.taper_straight_length,
                                                             -self.hot_width * 0.5+ 2.5),
                                                            (-self.electrode_length * 0.5, -self.hot_width * 0.5+ 2.5),
                                                           ],
                                           )
            he_taper_shape = he_taper_shape1 + he_taper_shape2# + he_taper_shape2.h_mirror_copy().reverse() + he_taper_shape1.h_mirror_copy().reverse()
            he_taper_shape.close()
            elems += i3.Boundary(layer=self.layer, shape=he_taper_shape)
            return elems

        def _generate_ports(self, ports):
            ports += i3.ElectricalPort(name="m1", position=(0.0, 0.0), shape=self.size, process=self.layer.process)
            return ports

    class Netlist(i3.NetlistFromLayout):
        pass


class ElectricalPad_20x20_Mod_Reverse(i3.PCell):

    """
    A rectangular electrical pad
    """

    class Layout(i3.LayoutView):
        size = i3.Size2Property(default=(60.0, 40.0))
        layer = i3.LayerProperty(default=i3.TECH.PPLAYER.PAD, locked=True)
        electrode_length = i3.PositiveNumberProperty(default=3000.0, doc="the length of the electrode")
        taper_length = i3.PositiveNumberProperty(default=100.0, doc="the length of the taper")
        hot_width = i3.PositiveNumberProperty(default=23.0, doc="width of the hot electrode")
        ground_width = i3.PositiveNumberProperty(default=100.0, doc="width of the ground planes")
        ground_width_mod = i3.PositiveNumberProperty(default=100.0, doc="width of the ground planes")
        electrode_gap = i3.PositiveNumberProperty(default=7.0, doc="gap between hot electrode and ground plane")
        hot_taper_width = i3.PositiveNumberProperty(default=50.0, doc="width of the hot electrode at the end of the taper")
        ground_taper_width = i3.PositiveNumberProperty(default=5.0,
                                                    doc="width of the hot electrode at the end of the taper")
        taper_gap = i3.PositiveNumberProperty(default=20.0,
                                                    doc="gap between hot electrode and ground plane at the end of the taper")
        taper_straight_length = i3.PositiveNumberProperty(default=10.0, doc="length of the straight section at the end of the taper")



        def _generate_elements(self, elems):
            he_taper_shape1 = i3.Shape(points=[(-self.electrode_length * 0.5, self.hot_width * 0.5 - 2.5),
                                                           (-self.electrode_length * 0.5 - self.taper_straight_length,#- self.taper_length,
                                                            self.hot_width * 0.5- 2.5)
                                                           ],
                                           )

            he_taper_shape2 = i3.Shape(points=[(-self.electrode_length * 0.5 - self.taper_length+self.taper_straight_length,
                                                            +self.hot_width * 0.5 - self.hot_taper_width*0.2- 2.5),
                                                            (-self.electrode_length * 0.5 - self.taper_length + 2.5,
                                                            +self.hot_width * 0.5 - self.hot_taper_width*0.2- 2.5),
                                                            (-self.electrode_length * 0.5 - self.taper_length +2.5,
                                                             +self.hot_width * 0.5 - self.hot_taper_width+ 2.5),
                                                            (-self.electrode_length * 0.5 - self.taper_length+self.taper_straight_length,
                                                            +self.hot_width * 0.5 - self.hot_taper_width+ 2.5),
                                                            # (-self.electrode_length * 0.5, -self.hot_width * 0.5),
                                                            # (-self.electrode_length * 0.5, -self.hot_width * 0.5),
                                                            (-self.electrode_length * 0.5 - self.taper_straight_length,
                                                             -self.hot_width * 0.5+ 2.5),
                                                            (-self.electrode_length * 0.5, -self.hot_width * 0.5+ 2.5),
                                                           ],
                                           )
            he_taper_shape = he_taper_shape2.h_mirror_copy().reverse() + he_taper_shape1.h_mirror_copy().reverse()
            he_taper_shape.close()
            elems += i3.Boundary(layer=self.layer, shape=he_taper_shape)
            return elems

        def _generate_ports(self, ports):
            ports += i3.ElectricalPort(name="m1", position=(0.0, 0.0), shape=self.size, process=self.layer.process)
            return ports

    class Netlist(i3.NetlistFromLayout):
        pass

class HiepElectricalWire(i3.ElectricalWire):
    class Layout(i3.ElectricalWire.Layout):
        def _generate_ports(self, ports):
            ports = super(ElectricalWire.Layout, self)._generate_ports(ports)
            angles = self.shape.angles_deg()
            in_angle, out_angle = angles[0]+120, angles[-1]
            ports['in'].angle = in_angle
            ports['out'].angle = out_angle
            return ports

heater_tmpl = asp.HeaterWireTemplate()
#heater_length = 390
#ring_radius_aux = 180
#heater_tmpl = asp.HeaterWireTemplate()
#heater_tmpl_layout = heater_tmpl.Layout(width=3.0)
#hiep_heater = HiepElectricalWire(trace_template=heater_tmpl)
#hiep_heater_layout = hiep_heater.Layout(shape=[(0.0, 0.0), (heater_length*0.05, ring_radius_aux*0.4), (heater_length*0.1, ring_radius_aux*0.6), (heater_length*0.2, ring_radius_aux*0.8), (heater_length*0.3, ring_radius_aux*0.95),(heater_length*0.4, ring_radius_aux), (heater_length*0.6, ring_radius_aux),(heater_length*0.7, ring_radius_aux*0.95),(heater_length*0.8, ring_radius_aux*0.8), (heater_length*0.9, ring_radius_aux*0.6),(heater_length*0.95, ring_radius_aux*0.4),(heater_length, 0.0)])
#hiep_heater_layout.visualize()

#hiep_pad = asp.ELECTRICAL_PAD_150150()
#hiep_pad_layout = hiep_pad.Layout()
#hiep_pad_layout.visualize()

#lc = i3.LayoutCell()
#lay = lc.Layout(elements=[i3.SRef(hiep_pad, position=(0, 0)),
#                          i3.SRef(hiep_pad, position=(800, 0)),
#                          i3.SRef(hiep_wire, position=(0, 0)),
#                          i3.SRef(hiep_wire, transformation=i3.HMirror(), position=(800, 0)),
#                          i3.SRef(hiep_heater, position=(200, 400))] )
#lay.visualize()

class Hiephiep(i3.PCell):
    hiep_pad_heater = i3.ChildCellProperty(doc="the heater pad")
    hiep_pad_heater_2020 = i3.ChildCellProperty(doc="the heater pad 20x20")
    hiep_pad_heater_2020_top = i3.ChildCellProperty(doc="the heater pad 20x20")
    hiep_pad_heater_2020_top_reverse = i3.ChildCellProperty(doc="the heater pad 20x20")
    hiep_pad_heater_2020_mod = i3.ChildCellProperty(doc="the heater pad 20x20")
    hiep_pad_heater_2020_mod_reverse = i3.ChildCellProperty(doc="the heater pad 20x20")
    hiep_wire_heater = i3.ChildCellProperty(doc="the heater wire")
    hiep_electric_wire = i3.ChildCellProperty(doc="the electric wire")

    hiep_electric_wire2 = i3.ChildCellProperty(doc="the electric wire")


    def _default_hiep_wire_heater(self):
        return HiepElectricalWire(trace_template=heater_tmpl)

    def _default_hiep_electric_wire(self):
        return ElectricalWire(trace_template=wire_tmpl)

    def _default_hiep_electric_wire2(self):
        return ElectricalWire(trace_template=wire_tmpl)

    def _default_hiep_pad_heater(self):
        return asp.ELECTRICAL_PAD_150150()

    def _default_hiep_pad_heater_2020(self):
        return ElectricalPad_20x20()

    def _default_hiep_pad_heater_2020_top(self):
        return ElectricalPad_20x20_top()

    def _default_hiep_pad_heater_2020_top_reverse(self):
        return ElectricalPad_20x20_top_reverse()

    def _default_hiep_pad_heater_2020_mod(self):
        return ElectricalPad_20x20_Mod()

    def _default_hiep_pad_heater_2020_mod_reverse(self):
        return ElectricalPad_20x20_Mod_Reverse()

    class Layout(i3.LayoutView):
        heater_position = i3.Coord2Property(default=(-1000, -2000),
                                            doc="the position of the heater with respect to the gc.")
        electric_wire_length = i3.PositiveNumberProperty(default=1000, doc="spacing between two pad heaters")
        heater_length = i3.PositiveNumberProperty(default=230, doc="spacing between two pad heaters")
        curvature = i3.PositiveNumberProperty(default=180, doc="spacing between two pad heaters")
        spacing = i3.PositiveNumberProperty(default=127 * 11, doc="spacing between two grating couplers")
        pad_spacing = i3.PositiveNumberProperty(default=400, doc="spacing between two pad heaters")
        #heater_gap = i3.PositiveNumberProperty(default=10, doc="spacing between heater and ring waveguide")
        def _default_hiep_pad_heater(self):
            hiep_pad_heater_layout = self.cell.hiep_pad_heater.get_default_view(i3.LayoutView)
            return hiep_pad_heater_layout

        def _default_hiep_pad_heater_2020(self):
            hiep_pad_heater_2020_layout = self.cell.hiep_pad_heater_2020.get_default_view(i3.LayoutView)
            return hiep_pad_heater_2020_layout

        def _default_hiep_pad_heater_2020_top(self):
            hiep_pad_heater_2020_layout = self.cell.hiep_pad_heater_2020_top.get_default_view(i3.LayoutView)
            return hiep_pad_heater_2020_layout

        def _default_hiep_pad_heater_2020_top_reverse(self):
            hiep_pad_heater_2020_layout = self.cell.hiep_pad_heater_2020_top_reverse.get_default_view(i3.LayoutView)
            return hiep_pad_heater_2020_layout

        def _default_hiep_pad_heater_2020_mod(self):
            hiep_pad_heater_2020_mod_layout = self.cell.hiep_pad_heater_2020_mod.get_default_view(i3.LayoutView)
            return hiep_pad_heater_2020_mod_layout

        def _default_hiep_pad_heater_2020_mod_reverse(self):
            hiep_pad_heater_2020_mod_reverse_layout = self.cell.hiep_pad_heater_2020_mod_reverse.get_default_view(i3.LayoutView)
            return hiep_pad_heater_2020_mod_reverse_layout

        def _default_hiep_wire_heater(self):
            ring_radius_aux = 232
            straight_length_aux = 922
            hiep_wire_heater_layout = self.cell.hiep_wire_heater.get_default_view(i3.LayoutView)

            # points = []
            #
            # x_right = self.heater_length * 0.5 - self.heater_length * 0.5 * np.cos(0 * np.pi / 100) + 2 * ring_radius_aux + straight_length_aux + 8
            # y_right = (self.curvature + 2) * np.sin(0 * np.pi / 100)
            # points.append((x_right + 42.5, y_right))
            #
            # for i in range(51):
            #     x_axis = self.heater_length*0.5 - self.heater_length*0.5 * np.cos(i * np.pi / 100) - 2*ring_radius_aux - straight_length_aux- 8
            #     y_axis = (self.curvature+2) * np.sin(i * np.pi / 100)
            #     points.append((-x_axis, -y_axis))
            #
            # x_one = -straight_length_aux + self.heater_length*0.5 * np.cos(50 * np.pi / 100) - self.heater_length*0.5 + straight_length_aux
            # y_one = (self.curvature+2) * np.sin(50 * np.pi / 100)
            # x_two = -straight_length_aux + self.heater_length*0.5 * np.cos(50 * np.pi / 100) - self.heater_length*0.5
            # y_two = (self.curvature+2) * np.sin(50 * np.pi / 100)
            # point_one = (-x_one, -y_one)
            # point_two = (-x_two, -y_two)
            # points.append(point_one)
            # points.append(point_two)
            #
            # for i in range(50,-1,-1):
            #     x_axis = self.heater_length*0.5 * np.cos(i * np.pi / 100) - self.heater_length*0.5
            #     y_axis = (self.curvature+2) * np.sin(i * np.pi / 100)
            #     points.append((-x_axis, -y_axis))
            #
            # x_left = self.heater_length * 0.5 * np.cos(0 * np.pi / 100) - self.heater_length * 0.5
            # y_left = (self.curvature + 2) * np.sin(0 * np.pi / 100)
            # points.append((x_left - 42.5, y_left))
            #
            # heater_shape = i3.Shape(points=points)
            # hiep_wire_heater_layout.set(shape=heater_shape)

            use_effective_radius = i3.BoolProperty(default=False)
            euler_shape = _partial_euler(angle=180, radius=440.229 / 2+4, p=0.5,
                                         use_effective_radius=use_effective_radius)

            short_shape = i3.ShapeShorten(original_shape=euler_shape,
                                          trim_lengths=(0, 476))

            shape_2 = i3.Shape(
                [(-238.5 + 2.5 + 507 + 47.5+50, 440.229 / 2 + 22-10-0.65), (-238.5 + 2.5 + 48 + 507 + 47.5+50, 440.229 / 2 + 22-10-0.65)])

            shape_original = short_shape + shape_2

            shape_original_mirror = shape_original.h_mirror_copy()

            shape_mod = shape_original_mirror.modified_copy()
            #
            shape_mod_mirror = shape_mod.h_mirror_copy()
            # #
            shape_mod_mirror_2 = shape_mod_mirror.move((straight_length_aux, 0))
            #
            shape = shape_original_mirror.reverse() + shape_mod_mirror_2

            hiep_wire_heater_layout.set(shape=shape)

            return hiep_wire_heater_layout

        def _default_hiep_electric_wire(self):
            hiep_electric_wire_layout = self.cell.hiep_electric_wire.get_default_view(i3.LayoutView)
            electric_wire_shape = i3.Shape([(-1390+100+34, 650+280+95), (-1390+100+34, 850), (-27+2.5-45, 850), (-27+2.5-45, self.electric_wire_length+2.5+40+8+11)])
            hiep_electric_wire_layout.set(shape=electric_wire_shape)
            return hiep_electric_wire_layout

        def _default_hiep_electric_wire2(self):
            hiep_electric_wire_layout = self.cell.hiep_electric_wire2.get_default_view(i3.LayoutView)
            electric_wire_shape = i3.Shape([(-2210-200-640, 150+280+95), (-2210-200-640, 200), (31-2.5, 200), (31-2.5, self.electric_wire_length-500+2.5+40+8+11)])
            hiep_electric_wire_layout.set(shape=electric_wire_shape)
            return hiep_electric_wire_layout


        def _generate_instances(self, insts):

            # insts += i3.SRef(name='in_pad20_left', reference=self.hiep_pad_heater_2020_top,position=(159.45 - 5345 + 410 -0.45+1+1600-29+13+ 4-4178+5.45,-self.electric_wire_length+650+700+250-25+5+98.5+ 46.264-100-26.372+2.5 - 95))
            # insts += i3.SRef(name='mid_pad20_left', reference=self.hiep_pad_heater_2020_mod,position=(159.45 - 5345+ 410 -0.45+1.5+2000-416.5+ 4-4178+5.45,-self.electric_wire_length+650+700+350-39+1.5+14.95+ 46.264-100-26.372+2.5 - 95))
            # insts += i3.SRef(name='out_pad20_left', reference=self.hiep_pad_heater_2020,position=(159.45 - 5345+ 410 -0.45+35+1.25+ 4-4178+5.45,-self.electric_wire_length+650+700+450-32+2.5-25.55+ 46.264-100-26.372+2.5 - 95))
            #
            # insts += i3.SRef(name='in_pad20_right', reference=self.hiep_pad_heater_2020_top_reverse,position=(159.45 - 5345+ 410 -0.45+ 6345 +20-15-1600+30+ 4-652.3-97.5-1.5,-self.electric_wire_length+650+700+250-25+5+98.5+ 46.264-100-26.372+2.5 - 95))
            # insts += i3.SRef(name='mid_pad20_right', reference=self.hiep_pad_heater_2020_mod_reverse,position=(159.45 - 5345+ 410 -0.45+ 6345 +20+1.5-2003+416.5+ 4-652.3-97.5-1.5,-self.electric_wire_length+650+700+350-39+1.5+14.95+ 46.264-100-26.372+2.5 - 95))
            # insts += i3.SRef(name='out_pad20_right', reference=self.hiep_pad_heater_2020,position=(159.45 - 5345+ 410 -0.45 + 6345 +20-35-1.25+ 4-652.3-97.5-1.5,-self.electric_wire_length+650+700+450-32+2.5-25.55+ 46.264-100-26.372+2.5 - 95))

            insts += i3.SRef(name ='in_pad_2', reference=self.hiep_pad_heater, position=(-1805,-self.electric_wire_length+650+700-400))
            insts += i3.SRef(name ='in_pad', reference=self.hiep_pad_heater, position=(-1605,-self.electric_wire_length+650+700-400))
            insts += i3.SRef(name='out_pad', reference=self.hiep_pad_heater,position=(-1405, -self.electric_wire_length+650+700-400))
            insts += i3.SRef(name='wire_in',reference=self.hiep_electric_wire, position=(0-138, -self.electric_wire_length))
            insts += i3.SRef(name='wire_out',reference=self.hiep_electric_wire2,position=(self.pad_spacing+141, -self.electric_wire_length+500))
            insts += i3.SRef(name='heater',reference=self.hiep_wire_heater,position=(-2+238.5-2.5-50, 0-228.015-1.9845-5+55))

            return insts

    class Netlist(i3.NetlistFromLayout):
        pass