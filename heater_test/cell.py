
import sys
sys.path.append("H:/GitHub/asp_sin_lnoi_photonics/ipkiss")

import numpy as np
import ipkiss3.all as i3
import asp_sin_lnoi_photonics.all as asp

from ipkiss3.pcell.wiring import ElectricalWire
wire_tmpl = asp.MetalWireTemplate()
wire_tmpl_layout = wire_tmpl.Layout(width=20.0)

#electric_wire_length = 550
#hiep_wire = ElectricalWire(trace_template=wire_tmpl)
#hiep_wire_layout = hiep_wire.Layout(shape=[(0, 0), (0, electric_wire_length)])
#hiep_wire_layout.visualize()

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


class Hiephiep_test(i3.PCell):
    hiep_pad_heater = i3.ChildCellProperty(doc="the heater pad")
    hiep_wire_heater = i3.ChildCellProperty(doc="the heater wire")
    hiep_wire_heater2 = i3.ChildCellProperty(doc="the heater wire")
    hiep_electric_wire = i3.ChildCellProperty(doc="the electric wire")
    hiep_electric_wire2 = i3.ChildCellProperty(doc="the electric wire")
    hiep_electric_wire3 = i3.ChildCellProperty(doc="the electric wire")


    def _default_hiep_wire_heater(self):
        return HiepElectricalWire(trace_template=heater_tmpl)
    def _default_hiep_wire_heater2(self):
        return HiepElectricalWire(trace_template=heater_tmpl)

    def _default_hiep_electric_wire(self):
        return ElectricalWire(trace_template=wire_tmpl)

    def _default_hiep_pad_heater(self):
        return asp.ELECTRICAL_PAD_100100()

    def _default_hiep_electric_wire2(self):
        return ElectricalWire(trace_template=wire_tmpl)

    def _default_hiep_electric_wire3(self):
        return ElectricalWire(trace_template=wire_tmpl)

    class Layout(i3.LayoutView):
        heater_position = i3.Coord2Property(default=(-1000, -2000),
                                            doc="the position of the heater with respect to the gc.")
        electric_wire_length = i3.PositiveNumberProperty(default=175, doc="spacing between two pad heaters")
        heater_length = i3.PositiveNumberProperty(default=200, doc="spacing between two pad heaters")
        spacing = i3.PositiveNumberProperty(default=127 * 11, doc="spacing between two grating couplers")
        pad_spacing = i3.PositiveNumberProperty(default=200, doc="spacing between two pad heaters")
        heater_gap = i3.PositiveNumberProperty(default=10, doc="spacing between heater and ring waveguide")
        def _default_hiep_pad_heater(self):
            hiep_pad_heater_layout = self.cell.hiep_pad_heater.get_default_view(i3.LayoutView)
            return hiep_pad_heater_layout
        def _default_hiep_wire_heater(self):
            hiep_wire_heater_layout = self.cell.hiep_wire_heater.get_default_view(i3.LayoutView)
            heater_shape = i3.Shape(points=[(0,0), (self.heater_length,0)])
            hiep_wire_heater_layout.set(shape=heater_shape)
            return hiep_wire_heater_layout

        def _default_hiep_wire_heater2(self):
            hiep_wire_heater_layout2 = self.cell.hiep_wire_heater2.get_default_view(i3.LayoutView)
            heater_shape = i3.Shape(points=[(0,0), (self.heater_length,0)])
            hiep_wire_heater_layout2.set(shape=heater_shape)
            return hiep_wire_heater_layout2

        def _default_hiep_electric_wire(self):
            hiep_electric_wire_layout = self.cell.hiep_electric_wire.get_default_view(i3.LayoutView)
            electric_wire_shape = i3.Shape([(0, 0), (0, self.electric_wire_length)])
            hiep_electric_wire_layout.set(shape=electric_wire_shape)
            return hiep_electric_wire_layout

        def _default_hiep_electric_wire2(self):
            hiep_electric_wire_layout2 = self.cell.hiep_electric_wire2.get_default_view(i3.LayoutView)
            electric_wire_shape = i3.Shape([(0, 0), (0, self.electric_wire_length+1050), (-self.pad_spacing*2,self.electric_wire_length+1050),
                                            (-self.pad_spacing*2, self.electric_wire_length+1050-280+202)])
            hiep_electric_wire_layout2.set(shape=electric_wire_shape)
            return hiep_electric_wire_layout2

        def _default_hiep_electric_wire3(self):
            hiep_electric_wire_layout3 = self.cell.hiep_electric_wire3.get_default_view(i3.LayoutView)
            electric_wire_shape = i3.Shape([(0, 0), (0, self.electric_wire_length+1150), (-self.pad_spacing*4, self.electric_wire_length+1150),
                                            (-self.pad_spacing*4, self.electric_wire_length+1150-280+102)])
            hiep_electric_wire_layout3.set(shape=electric_wire_shape)
            return hiep_electric_wire_layout3


        def _generate_instances(self, insts):
            insts += i3.SRef(name ='in_pad', reference=self.hiep_pad_heater, position=(55, 2*self.electric_wire_length))
            insts += i3.SRef(name='out_pad', reference=self.hiep_pad_heater,position=(self.pad_spacing+55, 2*self.electric_wire_length))
            insts += i3.SRef(name='wire_in',reference=self.hiep_electric_wire, position=(55+5, +self.electric_wire_length))
            insts += i3.SRef(name='wire_out',reference=self.hiep_electric_wire,position=(self.pad_spacing+55-5, +self.electric_wire_length))
            insts += i3.SRef(name='heater',reference=self.hiep_wire_heater,position=(55,2.5+self.electric_wire_length))

            return insts

    class Netlist(i3.NetlistFromLayout):
        pass