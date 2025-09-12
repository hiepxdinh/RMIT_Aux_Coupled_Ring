import ipkiss3.all as i3

import asp_sin_lnoi_photonics.all as asp

import numpy as np

from ring_modulator.cell_euler import AddDropRingWithElectrode
from ring_modulator.cell_euler import AddDropRingWithOutElectrode


import ipkiss


class RingModulatorGC(i3.Circuit):
    ring = i3.ChildCellProperty(doc="the ring modulator")
    gc = i3.ChildCellProperty(doc="the grating coupler")
    trace_template = i3.TraceTemplateProperty(doc="the trace template for the circuit")

    gc_spacing = i3.PositiveNumberProperty(default=127, doc="fibre array pich")
    ring_position = i3.Coord2Property(default=(-1000, -2000),
                                      doc="the position of the ring with respect to the gc.")
    waveguide_spacing = i3.PositiveNumberProperty(default=20, doc="minimum spacing between parallel waveguides")
    bend_radius = i3.PositiveNumberProperty(default=200, doc="radius of in waveguide routing")
    gc_wg_distance = i3.PositiveNumberProperty(default=300,
                                               doc="distance between the grating coupler and waveguide bending corner")
    ring_wg_distance = i3.PositiveNumberProperty(default=300,
                                                 doc="distance between the ring in port and waveguide bending corner")

    bend_radius = i3.PositiveNumberProperty(default=200, doc="radius of in waveguide routing")

    def _default_ring(self):
        return AddDropRingWithElectrode(ring_trace_template=self.trace_template,
                                        bus_trace_template=self.trace_template)

    def _default_gc(self):
        return asp.GRATING_COUPLER_TE1550_RIBZ(start_trace_template=self.trace_template)

    def _default_trace_template(self):
        return asp.SiNRibWaveguideTemplate()

    def _default_insts(self):
        return {"ring": self.ring,
                "in_grating": self.gc,
                "through_grating": self.gc,
                "add_grating": self.gc,
                "drop_grating": self.gc,
                }

    def _default_specs(self):
        return [
            i3.Place('in_grating', position=(0, 0), angle=-90),
            i3.Place('through_grating', position=(self.gc_spacing, 0), angle=-90),
            i3.Place('add_grating', position=(self.gc_spacing * 2, 0), angle=-90),
            i3.Place('drop_grating', position=(self.gc_spacing * 3, 0), angle=-90),
            i3.Place('ring', position=self.ring_position, angle=0),
            i3.FlipV('ring'),

            i3.ConnectManhattan(
                "in_grating:out", "ring:in",
                # control_points=[i3.H(i3.START - self.gc_wg_distance),
                #                 i3.V(i3.END - self.ring_wg_distance)
                #                 ],
                bend_radius=self.bend_radius,
            ),

            i3.ConnectManhattan(
                "through_grating:out", "ring:through",
                control_points=[i3.H(i3.START - self.gc_wg_distance + self.waveguide_spacing - self.waveguide_spacing * 2-200)
                                ],
                bend_radius=self.bend_radius,
            ),

            i3.ConnectManhattan(
                "add_grating:out", "ring:add",
                control_points=[i3.H(i3.START - self.gc_wg_distance + self.waveguide_spacing * 2 - self.waveguide_spacing * 2-200)
                                ],
                bend_radius=self.bend_radius,
            ),

            i3.ConnectManhattan(
                "drop_grating:out", "ring:drop",
                control_points=[i3.H(i3.START - self.gc_wg_distance + self.waveguide_spacing * 3 - self.waveguide_spacing * 2-200)
                                ],
                bend_radius=self.bend_radius,
            )

        ]


    def _default_exposed_ports(self):
        return {"in_grating:vertical_in": "in",
                "through_grating:vertical_in": "through",
                "add_grating:vertical_in": "add",
                "drop_grating:vertical_in": "drop",
                }

    class Layout(i3.Circuit.Layout):
        ring_radius = i3.PositiveNumberProperty(default=100, doc="ring radius")
        ring_straight_length = i3.PositiveNumberProperty(default=3000.0, doc="the circumference of the ring")
        coupler_straight_length = i3.NumberProperty(default=0.0,
                                                    doc="the length of the directional coupler straight section")
        coupler_positions = i3.ListProperty(doc="location of the two couplers")

        coupler_spacing = i3.PositiveNumberProperty(default=1.0,
                                                    doc="spacing between edges of two waveguides")
        coupler_bend_radius = i3.PositiveNumberProperty(default=300.0,
                                                        doc="bending radius of the coupler bus waveguide")
        ring_wg_width = i3.PositiveNumberProperty(default=1.4, doc="the width of the waveguide1")
        bus_wg_width = i3.PositiveNumberProperty(default=1.4, doc="the width of the waveguide2")
        cladding_width = i3.PositiveNumberProperty(default=20.0, doc="the width of cladding")

        electrode_length = i3.PositiveNumberProperty(default=2000.0, doc="the length of the electrode")
        taper_length = i3.PositiveNumberProperty(default=100.0, doc="the length of the taper")
        hot_width = i3.PositiveNumberProperty(default=23.0, doc="width of the hot electrode")
        ground_width = i3.PositiveNumberProperty(default=100.0, doc="width of the ground planes")
        electrode_gap = i3.PositiveNumberProperty(default=7.0, doc="gap between hot electrode and ground plane")
        hot_taper_width = i3.PositiveNumberProperty(default=50.0,
                                                    doc="width of the hot electrode at the end of the taper")
        taper_gap = i3.PositiveNumberProperty(default=20.0,
                                              doc="gap between hot electrode and ground plane at the end of the taper")
        taper_straight_length = i3.PositiveNumberProperty(default=10.0,
                                                          doc="length of the straight section at the end of the taper")

        def _default_trace_template(self):
            lo = self.cell.trace_template.get_default_view(i3.LayoutView)
            lo.set(core_width=self.ring_wg_width)

        def _default_ring(self):
            ring_lo = self.cell.ring.get_default_view(i3.LayoutView)
            ring_lo.set(ring_radius=self.ring_radius,
                        ring_straight_length=self.ring_straight_length,
                        coupler_straight_length=self.coupler_straight_length,
                        coupler_positions=self.coupler_positions,
                        coupler_spacing=self.coupler_spacing,
                        coupler_bend_radius=self.coupler_bend_radius,
                        # ring_wg_width=self.ring_wg_width,
                        # bus_wg_width=self.bus_wg_width,
                        # cladding_width=self.cladding_width,
                        electrode_length=self.electrode_length,
                        taper_length=self.taper_length,
                        hot_width=self.hot_width,
                        ground_width=self.ground_width,
                        electrode_gap=self.electrode_gap,
                        hot_taper_width=self.hot_taper_width,
                        taper_gap=self.taper_gap,
                        taper_straight_length=self.taper_straight_length
                        )

            return ring_lo

        def _default_coupler_positions(self):
            return [-self.ring_straight_length * 0.125 + self.coupler_straight_length,
                    self.ring_straight_length * 0.125 - self.coupler_straight_length]


class RingModulatorGC_NoElectrode_2(i3.Circuit):
    ring = i3.ChildCellProperty(doc="the ring modulator")
    gc = i3.ChildCellProperty(doc="the grating coupler")
    trace_template = i3.TraceTemplateProperty(doc="the trace template for the circuit")

    gc_spacing = i3.PositiveNumberProperty(default=127, doc="fibre array pich")
    ring_position = i3.Coord2Property(default=(-1000, -2000),
                                      doc="the position of the ring with respect to the gc.")
    waveguide_spacing = i3.PositiveNumberProperty(default=20, doc="minimum spacing between parallel waveguides")
    bend_radius = i3.PositiveNumberProperty(default=200, doc="radius of in waveguide routing")
    gc_wg_distance = i3.PositiveNumberProperty(default=300,
                                               doc="distance between the grating coupler and waveguide bending corner")
    ring_wg_distance = i3.PositiveNumberProperty(default=300,
                                                 doc="distance between the ring in port and waveguide bending corner")

    bend_radius = i3.PositiveNumberProperty(default=200, doc="radius of in waveguide routing")

    def _default_ring(self):
        return AddDropRingWithOutElectrode(ring_trace_template=self.trace_template,
                                        bus_trace_template=self.trace_template)

    def _default_gc(self):
        return asp.GRATING_COUPLER_TE1550_RIBZ(start_trace_template=self.trace_template)

    def _default_trace_template(self):
        return asp.SiNRibWaveguideTemplate()

    def _default_insts(self):
        return {"ring": self.ring,
                "in_grating": self.gc,
                "through_grating": self.gc,
                "add_grating": self.gc,
                "drop_grating": self.gc,
                }

    def _default_specs(self):
        return [
            i3.Place('in_grating', position=(0, 0), angle=-90),
            i3.Place('through_grating', position=(self.gc_spacing, 0), angle=-90),
            i3.Place('add_grating', position=(self.gc_spacing * 2, 0), angle=-90),
            i3.Place('drop_grating', position=(self.gc_spacing * 3, 0), angle=-90),
            i3.Place('ring', position=self.ring_position, angle=0),
            i3.FlipV('ring'),

            i3.ConnectManhattan(
                "drop_grating:out", "ring:drop",
                # control_points=[i3.H(i3.START - self.gc_wg_distance),
                                # i3.V(i3.END - self.ring_wg_distance)
                                # ],
                bend_radius=self.bend_radius,
            ),

            i3.ConnectManhattan(
                "add_grating:out", "ring:add",
                control_points=[i3.H(i3.START - self.gc_wg_distance + self.waveguide_spacing - self.waveguide_spacing * 2 )
                                ],
                bend_radius=self.bend_radius,
            ),

            i3.ConnectManhattan(
                "through_grating:out", "ring:through",
                control_points=[i3.H(i3.START - self.gc_wg_distance + self.waveguide_spacing * 2 - self.waveguide_spacing * 2)
                                ],
                bend_radius=self.bend_radius,
            ),

            i3.ConnectManhattan(
                "in_grating:out", "ring:in",
                control_points=[i3.H(i3.START - self.gc_wg_distance + self.waveguide_spacing * 3 - self.waveguide_spacing * 2)
                                ],
                bend_radius=self.bend_radius,
            )

        ]


    def _default_exposed_ports(self):
        return {"in_grating:vertical_in": "in",
                "through_grating:vertical_in": "through",
                "add_grating:vertical_in": "add",
                "drop_grating:vertical_in": "drop",
                }

    class Layout(i3.Circuit.Layout):
        ring_radius = i3.PositiveNumberProperty(default=100, doc="ring radius")
        ring_straight_length = i3.PositiveNumberProperty(default=3000.0, doc="the circumference of the ring")
        coupler_straight_length = i3.NumberProperty(default=0.0,
                                                    doc="the length of the directional coupler straight section")
        coupler_positions = i3.ListProperty(doc="location of the two couplers")

        coupler_spacing = i3.PositiveNumberProperty(default=1.0,
                                                    doc="spacing between edges of two waveguides")
        coupler_bend_radius = i3.PositiveNumberProperty(default=300.0,
                                                        doc="bending radius of the coupler bus waveguide")
        ring_wg_width = i3.PositiveNumberProperty(default=1.03, doc="the width of the waveguide1")
        bus_wg_width = i3.PositiveNumberProperty(default=1.03, doc="the width of the waveguide2")
        cladding_width = i3.PositiveNumberProperty(default=20.0, doc="the width of cladding")

        electrode_length = i3.PositiveNumberProperty(default=2000.0, doc="the length of the electrode")
        taper_length = i3.PositiveNumberProperty(default=100.0, doc="the length of the taper")
        hot_width = i3.PositiveNumberProperty(default=23.0, doc="width of the hot electrode")
        ground_width = i3.PositiveNumberProperty(default=100.0, doc="width of the ground planes")
        electrode_gap = i3.PositiveNumberProperty(default=7.0, doc="gap between hot electrode and ground plane")
        hot_taper_width = i3.PositiveNumberProperty(default=50.0,
                                                    doc="width of the hot electrode at the end of the taper")
        taper_gap = i3.PositiveNumberProperty(default=20.0,
                                              doc="gap between hot electrode and ground plane at the end of the taper")
        taper_straight_length = i3.PositiveNumberProperty(default=10.0,
                                                          doc="length of the straight section at the end of the taper")

        def _default_trace_template(self):
            lo = self.cell.trace_template.get_default_view(i3.LayoutView)
            lo.set(core_width=self.ring_wg_width)

        def _default_ring(self):
            ring_lo = self.cell.ring.get_default_view(i3.LayoutView)
            ring_lo.set(ring_radius=self.ring_radius,
                        ring_straight_length=self.ring_straight_length,
                        coupler_straight_length=self.coupler_straight_length,
                        coupler_positions=self.coupler_positions,
                        coupler_spacing=self.coupler_spacing,
                        coupler_bend_radius=self.coupler_bend_radius,
                        ring_wg_width=self.ring_wg_width,
                        bus_wg_width=self.bus_wg_width,
                        cladding_width=self.cladding_width,
                        electrode_length=self.electrode_length,
                        taper_length=self.taper_length,
                        hot_width=self.hot_width,
                        ground_width=self.ground_width,
                        electrode_gap=self.electrode_gap,
                        hot_taper_width=self.hot_taper_width,
                        taper_gap=self.taper_gap,
                        taper_straight_length=self.taper_straight_length
                        )

            return ring_lo

        def _default_coupler_positions(self):
            return [-self.ring_straight_length * 0.125 + self.coupler_straight_length,
                    self.ring_straight_length * 0.125 - self.coupler_straight_length]


class RingModulatorGC_NoElectrode(i3.Circuit):
    ring = i3.ChildCellProperty(doc="the ring modulator")
    gc = i3.ChildCellProperty(doc="the grating coupler")
    trace_template = i3.TraceTemplateProperty(doc="the trace template for the circuit")

    gc_spacing = i3.PositiveNumberProperty(default=127, doc="fibre array pich")
    ring_position = i3.Coord2Property(default=(-1000, -2000),
                                      doc="the position of the ring with respect to the gc.")
    waveguide_spacing = i3.PositiveNumberProperty(default=20, doc="minimum spacing between parallel waveguides")
    bend_radius = i3.PositiveNumberProperty(default=200, doc="radius of in waveguide routing")
    gc_wg_distance = i3.PositiveNumberProperty(default=300,
                                               doc="distance between the grating coupler and waveguide bending corner")
    ring_wg_distance = i3.PositiveNumberProperty(default=300,
                                                 doc="distance between the ring in port and waveguide bending corner")

    bend_radius = i3.PositiveNumberProperty(default=200, doc="radius of in waveguide routing")

    def _default_ring(self):
        return AddDropRingWithOutElectrode(ring_trace_template=self.trace_template,
                                        bus_trace_template=self.trace_template)

    def _default_gc(self):
        return asp.GRATING_COUPLER_TE1550_RIBZ(start_trace_template=self.trace_template)

    def _default_trace_template(self):
        return asp.SiNRibWaveguideTemplate()

    def _default_insts(self):
        return {"ring": self.ring,
                "in_grating": self.gc,
                "through_grating": self.gc,
                "add_grating": self.gc,
                "drop_grating": self.gc,
                }

    def _default_specs(self):
        return [
            i3.Place('in_grating', position=(0, 0), angle=-90),
            i3.Place('through_grating', position=(self.gc_spacing, 0), angle=-90),
            i3.Place('add_grating', position=(self.gc_spacing * 2, 0), angle=-90),
            i3.Place('drop_grating', position=(self.gc_spacing * 3, 0), angle=-90),
            i3.Place('ring', position=self.ring_position, angle=0),
            i3.FlipV('ring'),

            i3.ConnectManhattan(
                "in_grating:out", "ring:in",
                # control_points=[i3.H(i3.START - self.gc_wg_distance),
                                # i3.V(i3.END - self.ring_wg_distance)
                                # ],
                bend_radius=self.bend_radius,
            ),

            i3.ConnectManhattan(
                "through_grating:out", "ring:through",
                control_points=[i3.H(i3.START - self.gc_wg_distance + self.waveguide_spacing - self.waveguide_spacing * 2 )
                                ],
                bend_radius=self.bend_radius,
            ),

            i3.ConnectManhattan(
                "add_grating:out", "ring:add",
                control_points=[i3.H(i3.START - self.gc_wg_distance + self.waveguide_spacing * 2 - self.waveguide_spacing * 2)
                                ],
                bend_radius=self.bend_radius,
            ),

            i3.ConnectManhattan(
                "drop_grating:out", "ring:drop",
                control_points=[i3.H(i3.START - self.gc_wg_distance + self.waveguide_spacing * 3 - self.waveguide_spacing * 2)
                                ],
                bend_radius=self.bend_radius,
            )

        ]


    def _default_exposed_ports(self):
        return {"in_grating:vertical_in": "in",
                "through_grating:vertical_in": "through",
                "add_grating:vertical_in": "add",
                "drop_grating:vertical_in": "drop",
                }

    class Layout(i3.Circuit.Layout):
        ring_radius = i3.PositiveNumberProperty(default=100, doc="ring radius")
        ring_straight_length = i3.PositiveNumberProperty(default=3000.0, doc="the circumference of the ring")
        coupler_straight_length = i3.NumberProperty(default=0.0,
                                                    doc="the length of the directional coupler straight section")
        coupler_positions = i3.ListProperty(doc="location of the two couplers")

        coupler_spacing = i3.PositiveNumberProperty(default=1.0,
                                                    doc="spacing between edges of two waveguides")
        coupler_bend_radius = i3.PositiveNumberProperty(default=300.0,
                                                        doc="bending radius of the coupler bus waveguide")
        ring_wg_width = i3.PositiveNumberProperty(default=1.4, doc="the width of the waveguide1")
        bus_wg_width = i3.PositiveNumberProperty(default=1.4, doc="the width of the waveguide2")
        cladding_width = i3.PositiveNumberProperty(default=20.0, doc="the width of cladding")

        electrode_length = i3.PositiveNumberProperty(default=2000.0, doc="the length of the electrode")
        taper_length = i3.PositiveNumberProperty(default=100.0, doc="the length of the taper")
        hot_width = i3.PositiveNumberProperty(default=23.0, doc="width of the hot electrode")
        ground_width = i3.PositiveNumberProperty(default=100.0, doc="width of the ground planes")
        electrode_gap = i3.PositiveNumberProperty(default=7.0, doc="gap between hot electrode and ground plane")
        hot_taper_width = i3.PositiveNumberProperty(default=50.0,
                                                    doc="width of the hot electrode at the end of the taper")
        taper_gap = i3.PositiveNumberProperty(default=20.0,
                                              doc="gap between hot electrode and ground plane at the end of the taper")
        taper_straight_length = i3.PositiveNumberProperty(default=10.0,
                                                          doc="length of the straight section at the end of the taper")

        def _default_trace_template(self):
            lo = self.cell.trace_template.get_default_view(i3.LayoutView)
            lo.set(core_width=self.ring_wg_width)

        def _default_ring(self):
            ring_lo = self.cell.ring.get_default_view(i3.LayoutView)
            ring_lo.set(ring_radius=self.ring_radius,
                        ring_straight_length=self.ring_straight_length,
                        coupler_straight_length=self.coupler_straight_length,
                        coupler_positions=self.coupler_positions,
                        coupler_spacing=self.coupler_spacing,
                        coupler_bend_radius=self.coupler_bend_radius,
                        # ring_wg_width=self.ring_wg_width,
                        # bus_wg_width=self.bus_wg_width,
                        # cladding_width=self.cladding_width,
                        electrode_length=self.electrode_length,
                        taper_length=self.taper_length,
                        hot_width=self.hot_width,
                        ground_width=self.ground_width,
                        electrode_gap=self.electrode_gap,
                        hot_taper_width=self.hot_taper_width,
                        taper_gap=self.taper_gap,
                        taper_straight_length=self.taper_straight_length
                        )

            return ring_lo

        def _default_coupler_positions(self):
            return [-self.ring_straight_length * 0.125 + self.coupler_straight_length,
                    self.ring_straight_length * 0.125 - self.coupler_straight_length]



class NotchRingGC(i3.Circuit):
    grating_coupler = i3.ChildCellProperty(doc="grating coupler")
    ring = i3.ChildCellProperty(doc="ring resonator")
    trace_template = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")
    gc_spacing = i3.PositiveNumberProperty(default=900, doc="spacing between input and output grating couplers")

    def _default_grating_coupler(self):
        return asp.GratingCouplerTE1550RibY(start_trace_template=self.trace_template)

    def _default_ring(self):
        return asp.RectSBend90NotchRing()

    def _default_trace_template(self):
        return asp.SiNRibWaveguideTemplate()

    def _default_insts(self):
        return {"ring": self.ring,
                "in_grating": self.grating_coupler,
                "out_grating": self.grating_coupler
                }

    def _default_specs(self):
        ring_in_pos = self.ring.get_default_view(i3.LayoutView).ports['in'].position
        ring_out_pos = self.ring.get_default_view(i3.LayoutView).ports['through'].position
        return [
            i3.Place('in_grating', position=(-self.gc_spacing / 2, ring_in_pos[1]), angle=0),
            i3.Place('out_grating', position=(self.gc_spacing / 2, ring_out_pos[1]), angle=180),
            i3.Place('ring', position=(0, 0), angle=0),

            i3.ConnectManhattan(
                "in_grating:out", "ring:in",
                trace_template=self.trace_template
            ),

            i3.ConnectManhattan(
                "out_grating:out", "ring:through",
                trace_template=self.trace_template
            ),
        ]

    def _default_exposed_ports(self):
        return {"in_grating:vertical_in": "in",
                "out_grating:vertical_in": "out"
                }



    class Layout(i3.Circuit.Layout):
        ring_radius = i3.PositiveNumberProperty(default=100.0, doc="radius of the ring")
        straight_length = i3.PositiveNumberProperty(default=2000.0, doc="the length of the straight section")
        coupler_gap = i3.PositiveNumberProperty(default=1.9, doc="the gap between the edge of bus and ring waveguides")
        aux_ring_gap = i3.NumberProperty(default=1.0, doc="gap between two aux rings")
        coupler_length = i3.NumberProperty(default=30.0, doc="the coupling length of straight section")
        waveguide_width = i3.PositiveNumberProperty(default=1.03, doc="the width of all waveguides in the circuit")
        with_label = i3.BoolProperty(default=True, doc="whether to include a label")
        label_position = i3.Coord2Property(doc="position of the label")
        def _default_ring(self):
            lo = self.cell.ring.get_default_view(i3.LayoutView)
            lo.set(ring_circumference=2.0 * np.pi * self.ring_radius + self.straight_length * 2)
            lo.set(bend_radius=self.ring_radius)
            lo.set(coupler_length=self.coupler_length)
            lo.set(ring_wg_width=self.waveguide_width)
            lo.set(bus_wg_width=self.waveguide_width)
            lo.set(gap=self.coupler_gap)
            return lo

        def _default_trace_template(self):
            lo = self.cell.trace_template.get_default_view(i3.LayoutView)
            lo.set(core_width=self.waveguide_width)
            return lo

        def _default_label_position(self):
            return (0, 20.0)

        def _generate_elements(self, elems):
            """
            add labels at in/out put grating couplers regions
            """

            if self.with_label:
                elems += i3.PolygonText(layer=i3.TECH.PPLAYER.RWG.TEXT,
                                        coordinate=self.label_position,
                                        text="gap" + str(self.coupler_gap) + "UM_" + "straight_length" + str(int(self.straight_length)) + "um_" +"aux_gap"+str(self.aux_ring_gap)+"um",
                                        height=20,
                                        alignment=(i3.TEXT.ALIGN.CENTER, i3.TEXT.ALIGN.BOTTOM))

            return elems


from picazzo3.filters.ring import RingRectNotchFilter

class RingGCZProp(i3.Circuit):
    grating_coupler = i3.ChildCellProperty(doc="grating coupler")
    ring = i3.ChildCellProperty(doc="ring resonator")
    trace_template = i3.TraceTemplateProperty(doc="waveguide template used in the circuit")
    gc_spacing = i3.PositiveNumberProperty(default=900, doc="spacing between input and output grating couplers")

    def _default_grating_coupler(self):
        return asp.GratingCouplerTE1550RibZ(start_trace_template=self.trace_template)

    def _default_ring(self):
        return RingRectNotchFilter(ring_trace_template=self.trace_template,
                                   coupler_trace_templates=[self.trace_template])

    def _default_trace_template(self):
        return asp.SiNRibWaveguideTemplate()

    def _default_insts(self):
        return {"ring": self.ring,
                "in_grating": self.grating_coupler,
                "out_grating": self.grating_coupler
                }

    def _default_specs(self):
        ring_in_pos = self.ring.get_default_view(i3.LayoutView).ports['in'].position.modified_copy()
        ring_out_pos = self.ring.get_default_view(i3.LayoutView).ports['out'].position.modified_copy()
        ring_in_pos.transform(transformation=i3.Rotation(rotation=-90))
        ring_out_pos.transform(transformation=i3.Rotation(rotation=-90))

        return [
            i3.Place('in_grating', position=(ring_in_pos[0], self.gc_spacing / 2), angle=-90),
            i3.Place('out_grating', position=(ring_out_pos[0], -self.gc_spacing / 2), angle=90),
            i3.Place('ring', position=(0, 0), angle=-90),

            i3.ConnectManhattan(
                "in_grating:out", "ring:in",
                trace_template=self.trace_template
            ),

            i3.ConnectManhattan(
                "out_grating:out", "ring:out",
                trace_template=self.trace_template
            ),
        ]

    def _default_exposed_ports(self):
        return {"in_grating:vertical_in": "in",
                "out_grating:vertical_in": "out"
                }



    class Layout(i3.Circuit.Layout):
        ring_radius = i3.PositiveNumberProperty(default=100.0, doc="radius of the ring")
        straight_length = i3.PositiveNumberProperty(default=2000.0, doc="the length of the straight section")
        coupler_gap = i3.PositiveNumberProperty(default=1.9, doc="the gap between the edge of bus and ring waveguides")
        waveguide_width = i3.PositiveNumberProperty(default=1.03, doc="the width of all waveguides in the circuit")
        with_label = i3.BoolProperty(default=True, doc="whether to include a label")
        label_position = i3.Coord2Property(doc="position of the label")
        label_angle = i3.NumberProperty(default=0, doc="angle of the label")

        def _default_ring(self):
            lo = self.cell.ring.get_default_view(i3.LayoutView)
            lo.set(bend_radius=self.ring_radius)
            lo.set(straights=[0, self.straight_length])
            lo.set(coupler_spacings=[self.coupler_gap + self.waveguide_width])
            lo.set(angle_step=0.1)
            return lo

        def _default_trace_template(self):
            lo = self.cell.trace_template.get_default_view(i3.LayoutView)
            lo.set(core_width=self.waveguide_width)
            return lo

        def _default_label_position(self):
            return (0, 0)

        def _generate_elements(self, elems):
            """
            add labels at in/out put grating couplers regions
            """

            if self.with_label:
                elems += i3.PolygonText(layer=i3.TECH.PPLAYER.RWG.TEXT,
                                        coordinate=self.label_position,
                                        text="gap" + str(self.coupler_gap) + "UM_" + "straight_length" + str(int(self.straight_length)) + "um",
                                        height=20,
                                        alignment=(i3.TEXT.ALIGN.CENTER, i3.TEXT.ALIGN.BOTTOM),
                                        transformation=i3.Rotation(rotation=self.label_angle))

            return elems




