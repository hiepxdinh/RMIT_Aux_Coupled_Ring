import ipkiss3.all as i3

import asp_sin_lnoi_photonics.all as asp
from heater_outside import Hiephiep

class SBendAlgorithm(i3.ShapeRoundAdiabaticSpline):

    def _default_radius(self):
        return 300.0

    def _default_adiabatic_angles(self):
        return (0.0, 0.0)


class RFElectrode(i3.PCell):
    class Layout(i3.LayoutView):
        layer = i3.LayerProperty(default=i3.PPLayer(process=i3.TECH.PROCESS.RF, purpose=i3.TECH.PURPOSE.DRAWING),
                                 doc="electrode layer")
        waveguide_cladding_layer = i3.LayerProperty(default=i3.TECH.PPLAYER.RWG.CLADDING,
                                 doc="the optical waveguide cladding layer")
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
            # Hot electrode
            #elems += i3.Rectangle(self.layer, center=(0.0, 0.0), box_size=(self.electrode_length, self.hot_width))

            he_taper_shape1 = i3.Shape(points=[(-self.electrode_length * 0.5, self.hot_width * 0.5),
                                                           (-self.electrode_length * 0.5 - self.taper_straight_length,#- self.taper_length,
                                                            self.hot_width * 0.5)
                                                           ],
                                           )

            he_taper_shape2 = i3.Shape(points=[(-self.electrode_length * 0.5 - self.taper_length+self.taper_straight_length,
                                                            +self.hot_width * 0.5 - self.hot_taper_width*0.2),
                                                            (-self.electrode_length * 0.5 - self.taper_length,
                                                            +self.hot_width * 0.5 - self.hot_taper_width*0.2),
                                                            (-self.electrode_length * 0.5 - self.taper_length,
                                                             +self.hot_width * 0.5 - self.hot_taper_width),
                                                            (-self.electrode_length * 0.5 - self.taper_length+self.taper_straight_length,
                                                            +self.hot_width * 0.5 - self.hot_taper_width),
                                                            (-self.electrode_length * 0.5 - self.taper_straight_length,
                                                             -self.hot_width * 0.5),
                                                            (-self.electrode_length * 0.5, -self.hot_width * 0.5),
                                                           ],
                                           )

            he_taper_shape = he_taper_shape1 + he_taper_shape2 + he_taper_shape2.h_mirror_copy().reverse() + he_taper_shape1.h_mirror_copy().reverse()
            he_taper_shape.close()
            elems += i3.Boundary(layer=self.layer, shape=he_taper_shape)

            # Top ground plane
            # grnd_taper_shape1 = i3.ShapeRound(original_shape=[(-self.electrode_length * 0.5, self.hot_width * 0.5 + self.electrode_gap),
            #                                                 (-self.electrode_length * 0.5 - self.taper_straight_length,
            #                                                  self.hot_width * 0.5 + self.electrode_gap),
            #                                                 #(-self.electrode_length * 0.5 - self.taper_length + self.taper_straight_length,
            #                                                 #-self.hot_width * 0.5 + self.taper_gap + self.hot_taper_width*0.3),
            #                                                 (-self.electrode_length * 0.5 - self.taper_length,
            #                                                  -self.hot_width * 0.5 + self.taper_gap + self.hot_taper_width*0.3),
            #                                                 (-self.electrode_length * 0.5 - self.taper_length,
            #                                                    -self.hot_width * 0.5 + self.taper_gap + self.ground_width_mod),
            #                                                 (
            #                                                   -self.electrode_length * 0.5 - self.taper_length + self.taper_straight_length*2,
            #                                                   self.hot_width * 0.5 + self.electrode_gap + self.ground_width_mod),
            #                                                 ],
            #                                 radius=50.0)
            # grnd_taper_shape1 = i3.ShapeRound(original_shape=[(-self.electrode_length * 0.5, self.hot_width * 0.5 + self.electrode_gap),
            #                                                 (-self.electrode_length * 0.5 - self.taper_straight_length,
            #                                                  self.hot_width * 0.5 + self.electrode_gap),
            #                                                 (
            #                                                 -self.electrode_length * 0.5 - self.taper_length + self.taper_straight_length,
            #                                                 -self.hot_width * 0.5 + self.taper_gap + self.hot_taper_width),
            #                                                 (-self.electrode_length * 0.5 - self.taper_length,
            #                                                  -self.hot_width * 0.5 + self.taper_gap + self.hot_taper_width)
            #                                                 ],
            #                                 radius=50.0)
            grnd_taper_shape1 = i3.Shape(points=[(-self.electrode_length * 0.5 - self.taper_length,
                                                             self.hot_width * 0.5 + self.electrode_gap),
                                                 (-self.electrode_length * 0.5 - self.taper_length,
                                                            self.hot_width * 0.5 + self.electrode_gap + self.ground_width_mod),
                                                 (-self.electrode_length * 0.5,
                                                            self.hot_width * 0.5 + self.electrode_gap + self.ground_width_mod),
                                                (-self.electrode_length * 0.5,
                                                             self.hot_width * 0.5 + self.electrode_gap)])

            grnd_taper_shape2 = i3.Shape(points=[(-self.electrode_length * 0.5 - self.taper_length,
                                                             self.hot_width * 0.5 + self.electrode_gap + self.ground_width_mod),
                                                            (-self.electrode_length * 0.5,
                                                             self.hot_width * 0.5 + self.electrode_gap + self.ground_width_mod)])

            top_grnd_taper_shape = grnd_taper_shape1 + grnd_taper_shape2 + grnd_taper_shape2.h_mirror_copy().reverse() + grnd_taper_shape1.h_mirror_copy().reverse()
            top_grnd_taper_shape.close()
            elems += i3.Boundary(layer=self.layer, shape=top_grnd_taper_shape)


            # Bottom ground plane
            grnd_taper_shape3 = i3.ShapeRound(
                original_shape=[(-self.electrode_length * 0.5, -self.hot_width * 0.5 - self.electrode_gap),
                                (-self.electrode_length * 0.5 - self.taper_straight_length,
                                 -self.hot_width * 0.5 - self.electrode_gap),
                                (-self.electrode_length * 0.5 - self.taper_length + self.taper_straight_length,
                                    -self.hot_width * 0.5 - self.taper_gap-25),
                                (-self.electrode_length * 0.5 - self.taper_length,
                                 -self.hot_width * 0.5 - self.taper_gap-25)
                                ],
                radius=25.0)


            grnd_taper_shape4 = i3.Shape(points=[(-self.electrode_length * 0.5 - self.taper_length,
                                                  -self.hot_width * 0.5 - self.electrode_gap - self.ground_width),
                                                 (-self.electrode_length * 0.5,
                                                  -self.hot_width * 0.5 - self.electrode_gap - self.ground_width)])

            bottom_grnd_taper_shape = grnd_taper_shape3 + grnd_taper_shape4 + grnd_taper_shape4.h_mirror_copy().reverse() + grnd_taper_shape3.h_mirror_copy().reverse()
            bottom_grnd_taper_shape.close()
            elems += i3.Boundary(layer=self.layer, shape=bottom_grnd_taper_shape)


            # Expand the waveguide cladding region under the electrode
            elems += i3.Rectangle(self.waveguide_cladding_layer, center=(0.0, 0.0),
                                  box_size=(self.electrode_length + self.taper_length * 2,
                                            self.hot_width + self.electrode_gap * 2 + self.ground_width + self.ground_width_mod))

            return elems

    class Netlist(i3.NetlistFromLayout):
        pass

class AddDropRingWithAuxOutside2(i3.PCell):
    """
    Add-drop racetrack ring with a travelling electrode
    """
    ring_trace_template = i3.TraceTemplateProperty(doc="the trace template for ring")
    ring_aux_trace_template = i3.TraceTemplateProperty(doc="the trace template for aux ring")
    bus_trace_template = i3.TraceTemplateProperty(doc="the trace template for bus wg")
    ring_1 = i3.ChildCellProperty(locked=True, doc="the ring")
    ring_2 = i3.ChildCellProperty(locked=True, doc="the ring")
    ring_aux_1 = i3.ChildCellProperty(locked=True, doc="the ring")
    ring_aux_2 = i3.ChildCellProperty(locked=True, doc="the ring")
    heater = i3.ChildCellProperty(locked=True, doc="the heater")
    bus_waveguide = i3.ChildCellProperty(locked=True, doc="the bus waveguide of the coupler")
    rf_electrode = i3.ChildCellProperty(locked=True, doc="the RF electrode")

    def _default_ring_aux_trace_template(self):
        return asp.SiNRibWaveguideTemplate()

    def _default_ring_trace_template(self):
        return asp.SiNRibWaveguideTemplate()

    def _default_bus_trace_template(self):
        return asp.SiNRibWaveguideTemplate()

    def _default_ring_1(self):
        # return asp.RoundedRibWaveguide(trace_template=self.ring_trace_template)
        return asp.EulerBend(trace_template=self.ring_trace_template)

    def _default_ring_2(self):
        # return asp.RoundedRibWaveguide(trace_template=self.ring_trace_template)
        return asp.EulerBend(trace_template=self.ring_trace_template)

    def _default_ring_aux_1(self):
        return asp.RoundedRibWaveguide(trace_template=self.ring_aux_trace_template)

    def _default_ring_aux_2(self):
        return asp.RoundedRibWaveguide(trace_template=self.ring_trace_template)

    def _default_rf_electrode(self):
        return RFElectrode()

    def _default_heater(self):
        return Hiephiep()

    def _default_bus_waveguide(self):
        return asp.RoundedRibWaveguide(trace_template=self.bus_trace_template)

    class Layout(i3.LayoutView):
        aux_coupling_gap = i3.NumberProperty(default=0.0, doc="gap between main ring and auxiliary ring")
        ring_radius = i3.PositiveNumberProperty(default=100, doc="ring radius")
        ring_radius_aux = i3.PositiveNumberProperty(default=100, doc="ring radius")
        ring_straight_length = i3.PositiveNumberProperty(default=3000.0, doc="the circumference of the ring")
        ring_straight_length_aux = i3.PositiveNumberProperty(default=3000.0, doc="the circumference of the ring")
        coupler_straight_length = i3.NumberProperty(default=0.0, doc="the length of the directional coupler straight section")
        coupler_positions = i3.ListProperty(doc="location of the two couplers")

        coupler_spacing = i3.PositiveNumberProperty(default=1.0,
                                                    doc="spacing between edges of two waveguides")
        coupler_bend_angle = i3.PositiveNumberProperty(default=30.0,
                                               doc="angular span (in degrees) of the bend waveguide")
        coupler_bend_radius = i3.PositiveNumberProperty(default=300.0,
                                               doc="bending radius of the coupler bus waveguide")
        ring_wg_width = i3.PositiveNumberProperty(default=1.43, doc="the width of the waveguide1")
        bus_wg_width = i3.PositiveNumberProperty(default=1.43, doc="the width of the waveguide2")
        cladding_width = i3.PositiveNumberProperty(default=28.0, doc="the width of cladding")
        heater_gap = i3.PositiveNumberProperty(default=10, doc="the length of the electrode")
        electrode_length = i3.PositiveNumberProperty(default=0, doc="the length of the electrode")
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




        def _default_coupler_positions(self):
            return [-self.ring_straight_length * 0.125 + self.coupler_straight_length,
                    self.ring_straight_length * 0.125 - self.coupler_straight_length]

        def _default_ring_aux_trace_template(self):
            lo=self.cell.ring_aux_trace_template.get_default_view(i3.LayoutView)
            lo.set(core_width=self.ring_wg_width, cladding_width = self.cladding_width)

        def _default_ring_trace_template(self):
            lo=self.cell.ring_trace_template.get_default_view(i3.LayoutView)
            lo.set(core_width=self.ring_wg_width)

        def _default_bus_trace_template(self):
            lo=self.cell.bus_trace_template.get_default_view(i3.LayoutView)
            lo.set(core_width=self.bus_wg_width)

        def _default_ring_1(self):
            ring_cell_layout = self.cell.ring_1.get_default_view(i3.LayoutView)
            ring_cell_layout.set(angle=180,
                                 bend_radius=self.ring_radius,
                                 straight_length=0)
            return ring_cell_layout

        def _default_ring_2(self):
            ring_cell_layout = self.cell.ring_2.get_default_view(i3.LayoutView)
            ring_cell_layout.set(angle=180,
                                 bend_radius=self.ring_radius,
                                 straight_length=0)
            return ring_cell_layout

        def _default_ring_aux_1(self):

            circle_shape = i3.ShapeArc(radius=self.ring_radius_aux,
                                     center=(self.ring_straight_length_aux * 0.5, 0),
                                     start_angle=-90,
                                     end_angle=0,
                                     angle_step=0.2)

            circle_shape_mirror = circle_shape.h_mirror_copy().reverse()



            # ring_shape = i3.Shape([(-self.ring_straight_length * 0.5, -self.ring_radius),
            #                        (self.ring_straight_length * 0.5, -self.ring_radius)]) +\
            #              circle_shape + \
            #              i3.Shape([(self.ring_straight_length * 0.5, self.ring_radius),
            #                        (-self.ring_straight_length * 0.5, self.ring_radius)]) + \
            #              circle_shape.h_mirror_copy().reverse()

            straight_shape = i3.Shape([(-self.ring_straight_length_aux * 0.5, -self.ring_radius_aux),
                                   (self.ring_straight_length_aux * 0.5, -self.ring_radius_aux)])

            ring_shape = circle_shape_mirror + straight_shape + circle_shape

            # ring_shape.close()

            ring_aux_cell_layout = self.cell.ring_aux_1.get_default_view(i3.LayoutView)
            ring_aux_cell_layout.set(shape=ring_shape, bend_radius=self.ring_radius_aux, angle_step=0.2)
            return ring_aux_cell_layout

        def _default_ring_aux_2(self):

            circle_shape = i3.ShapeArc(radius=self.ring_radius_aux,
                                     center=(self.ring_straight_length_aux * 0.5, 0),
                                     start_angle=-0.25,
                                     end_angle=90,
                                     angle_step=0.2)

            circle_shape_mirror = circle_shape.h_mirror_copy().reverse()



            # ring_shape = i3.Shape([(-self.ring_straight_length * 0.5, -self.ring_radius),
            #                        (self.ring_straight_length * 0.5, -self.ring_radius)]) +\
            #              circle_shape + \
            #              i3.Shape([(self.ring_straight_length * 0.5, self.ring_radius),
            #                        (-self.ring_straight_length * 0.5, self.ring_radius)]) + \
            #              circle_shape.h_mirror_copy().reverse()

            straight_shape = i3.Shape([(-self.ring_straight_length_aux * 0.5, self.ring_radius_aux),
                                   (self.ring_straight_length_aux * 0.5, self.ring_radius_aux)])

            ring_shape = circle_shape + straight_shape + circle_shape_mirror

            # ring_shape.close()

            ring_aux_cell_layout = self.cell.ring_aux_2.get_default_view(i3.LayoutView)
            ring_aux_cell_layout.set(shape=ring_shape, bend_radius=self.ring_radius_aux, angle_step=0.2)
            return ring_aux_cell_layout

        def _default_bus_waveguide(self):
            # set the layout parameters of the waveguide
            r = 0
            a = 0.5 * self.coupler_bend_angle
            s = i3.TECH.RWG.SHORT_STRAIGHT
            l = self.coupler_straight_length / 2.0

            # Bus waveguide layout
            bend_layout = self.cell.bus_waveguide.get_default_view(i3.LayoutView)  # default bus layout view
            bend_layout.set(bend_radius=self.coupler_bend_radius,
                            trace_template=self.bus_trace_template,
                            rounding_algorithm=SBendAlgorithm,
                            angle_step=0.2)

            b1, b2 = bend_layout.get_bend_size(a)  # calculates the size of the waveguide bend
            # control shape for the bus waveguide (one half)
            # the RoundedWaveguide will automatically generate smooth bends
            s1 = i3.Shape([(0.0, -r), (-l - b1, -r)])
            s1.add_polar(2 * b2, 180.0 - a)
            s1.add_polar(b1 + s, 180.0)
            # stitching 2 halves together
            bend_shape = s1.reversed().v_mirror_copy(mirror_plane_y=-r) + s1.h_mirror_copy().v_mirror_copy(
                mirror_plane_y=-r)

            # assigning the shape to the bus
            bend_layout.set(shape=bend_shape,
                            draw_control_shape=False)
            return bend_layout

        def _default_rf_electrode(self):
            electrode_layout = self.cell.rf_electrode.get_default_view(i3.LayoutView)
            electrode_layout.set(electrode_length=self.electrode_length,
                                 taper_length=self.taper_length,
                                 hot_width=self.hot_width,
                                 ground_width=self.ground_width,
                                 electrode_gap=self.electrode_gap,
                                 hot_taper_width=self.hot_taper_width,
                                 taper_gap=self.taper_gap,
                                 taper_straight_length=self.taper_straight_length
                                 )
            return electrode_layout

        def _default_heater(self):
            heater_layout = self.cell.heater.get_default_view(i3.LayoutView)
            heater_layout.set(heater_length =self.ring_radius_aux*2+8, pad_spacing=self.ring_radius_aux*2 + self.ring_straight_length_aux+4, curvature = self.ring_radius_aux+4)
            return heater_layout
        
        def _generate_instances(self, insts):
            ring_width = self.ring_trace_template.core_width
            bus_width = self.bus_trace_template.core_width

            print("ring with = {}".format(ring_width))
            print("bus with = {}".format(bus_width))

            insts += i3.SRef(name='ring_1', reference=self.ring_1,
                             position=(-self.ring_straight_length * 0.5, self.ring_radius+self.ground_width+self.electrode_gap), transformation=i3.HMirror())
            insts += i3.SRef(name='ring_2', reference=self.ring_2, position=(self.ring_straight_length * 0.5, self.ring_radius+self.ground_width+self.electrode_gap))

            ring_1_in = [-self.ring_straight_length * 0.5, self.ring_radius+self.ground_width+self.electrode_gap]
            ring_2_in = [self.ring_straight_length * 0.5, self.ring_radius+self.ground_width+self.electrode_gap]

            link1_shape1 = i3.Shape([ring_1_in, ring_2_in])

            link1 = i3.RoundedWaveguide(trace_template=self.ring_trace_template)
            link1_lo1 = link1.Layout(shape=link1_shape1)
            insts += i3.SRef(reference=link1_lo1)

            ring_1_in = [-self.ring_straight_length * 0.5, -self.ring_radius- 46.264]
            ring_2_in = [self.ring_straight_length * 0.5, -self.ring_radius- 46.264]

            link1_shape1 = i3.Shape([ring_1_in, ring_2_in])

            link1 = i3.RoundedWaveguide(trace_template=self.ring_trace_template)
            link1_lo1 = link1.Layout(shape=link1_shape1)
            insts += i3.SRef(reference=link1_lo1)

            insts += i3.SRef(name='ring_aux_1', reference=self.ring_aux_1, position=(-self.ring_straight_length * 0.45,
                                                                                     -self.ring_radius - self.ring_radius_aux - self.ring_wg_width - self.aux_coupling_gap- 46.264))
            insts += i3.SRef(name='ring_aux_2', reference=self.ring_aux_2, position=(-self.ring_straight_length * 0.45,
                                                                                     -self.ring_radius - self.ring_radius_aux - self.ring_wg_width - self.aux_coupling_gap- 46.264))
            insts += i3.SRef(name='bus_in_through', reference=self.bus_waveguide,
                             position=(self.coupler_positions[0], -self.ring_radius - self.ring_wg_width * 0.5 - self.coupler_spacing - self.bus_wg_width * 0.5- 46.264))
            insts += i3.SRef(name='bus_add_drop', reference=self.bus_waveguide,
                             position=(self.coupler_positions[1], -self.ring_radius - self.ring_wg_width * 0.5 - self.coupler_spacing - self.bus_wg_width * 0.5- 46.264)
                             )

            # Heater
            insts += i3.SRef(name='heater', reference=self.heater,position=(-self.ring_straight_length*0.45-self.ring_straight_length_aux*0.5-self.ring_radius_aux-4, -self.ring_radius-self.ring_radius_aux- self.ring_wg_width-self.aux_coupling_gap- 46.264))

            # RF electrode
            insts += i3.SRef(name='electrode', reference=self.rf_electrode,
                             position=(0, self.ring_radius + self.electrode_gap * 0.5 + self.hot_width * 0.5- self.hot_width - self.electrode_gap))

            return insts

        def _generate_ports(self, ports):
            ports += i3.expose_ports(self.instances, {
                'bus_in_through:in': 'in',
                'bus_in_through:out': 'through',
                'bus_add_drop:in': 'add',
                'bus_add_drop:out': 'drop',
            })

            return ports

    class Netlist(i3.NetlistFromLayout):
        pass


class AddDropRingWithAuxOutside3(i3.PCell):
    """
    Add-drop racetrack ring with a travelling electrode
    """
    ring_trace_template = i3.TraceTemplateProperty(doc="the trace template for ring")
    ring_aux_trace_template = i3.TraceTemplateProperty(doc="the trace template for aux ring")
    bus_trace_template = i3.TraceTemplateProperty(doc="the trace template for bus wg")
    ring_1 = i3.ChildCellProperty(locked=True, doc="the ring")
    ring_2 = i3.ChildCellProperty(locked=True, doc="the ring")
    ring_aux_1 = i3.ChildCellProperty(locked=True, doc="the ring")
    ring_aux_2 = i3.ChildCellProperty(locked=True, doc="the ring")
    heater = i3.ChildCellProperty(locked=True, doc="the heater")
    bus_waveguide = i3.ChildCellProperty(locked=True, doc="the bus waveguide of the coupler")
    rf_electrode = i3.ChildCellProperty(locked=True, doc="the RF electrode")

    def _default_ring_aux_trace_template(self):
        return asp.SiNRibWaveguideTemplate()

    def _default_ring_trace_template(self):
        return asp.SiNRibWaveguideTemplate()

    def _default_bus_trace_template(self):
        return asp.SiNRibWaveguideTemplate()

    def _default_ring_1(self):
        # return asp.RoundedRibWaveguide(trace_template=self.ring_trace_template)
        return asp.EulerBend(trace_template=self.ring_trace_template)

    def _default_ring_2(self):
        # return asp.RoundedRibWaveguide(trace_template=self.ring_trace_template)
        return asp.EulerBend(trace_template=self.ring_trace_template)

    def _default_ring_aux_1(self):
        return asp.RoundedRibWaveguide(trace_template=self.ring_aux_trace_template)

    def _default_ring_aux_2(self):
        return asp.RoundedRibWaveguide(trace_template=self.ring_trace_template)

    def _default_rf_electrode(self):
        return RFElectrode()

    def _default_heater(self):
        return Hiephiep()

    def _default_bus_waveguide(self):
        return asp.RoundedRibWaveguide(trace_template=self.bus_trace_template)

    class Layout(i3.LayoutView):
        aux_coupling_gap = i3.NumberProperty(default=0.0, doc="gap between main ring and auxiliary ring")
        ring_radius = i3.PositiveNumberProperty(default=100, doc="ring radius")
        ring_radius_aux = i3.PositiveNumberProperty(default=100, doc="ring radius")
        ring_straight_length = i3.PositiveNumberProperty(default=3000.0, doc="the circumference of the ring")
        ring_straight_length_aux = i3.PositiveNumberProperty(default=3000.0, doc="the circumference of the ring")
        coupler_straight_length = i3.NumberProperty(default=0.0,
                                                    doc="the length of the directional coupler straight section")
        coupler_positions = i3.ListProperty(doc="location of the two couplers")

        coupler_spacing = i3.PositiveNumberProperty(default=1.0,
                                                    doc="spacing between edges of two waveguides")
        coupler_bend_angle = i3.PositiveNumberProperty(default=30.0,
                                                       doc="angular span (in degrees) of the bend waveguide")
        coupler_bend_radius = i3.PositiveNumberProperty(default=300.0,
                                                        doc="bending radius of the coupler bus waveguide")
        ring_wg_width = i3.PositiveNumberProperty(default=1.03, doc="the width of the waveguide1")
        bus_wg_width = i3.PositiveNumberProperty(default=1.03, doc="the width of the waveguide2")
        cladding_width = i3.PositiveNumberProperty(default=30.0, doc="the width of cladding")
        heater_gap = i3.PositiveNumberProperty(default=10, doc="the length of the electrode")
        electrode_length = i3.PositiveNumberProperty(default=0, doc="the length of the electrode")
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

        def _default_coupler_positions(self):
            return [-self.ring_straight_length * 0.125 + self.coupler_straight_length,
                    self.ring_straight_length * 0.125 - self.coupler_straight_length]

        def _default_ring_aux_trace_template(self):
            lo = self.cell.ring_aux_trace_template.get_default_view(i3.LayoutView)
            lo.set(core_width=self.ring_wg_width, cladding_width=self.cladding_width)

        def _default_ring_trace_template(self):
            lo = self.cell.ring_trace_template.get_default_view(i3.LayoutView)
            lo.set(core_width=self.ring_wg_width)

        def _default_bus_trace_template(self):
            lo = self.cell.bus_trace_template.get_default_view(i3.LayoutView)
            lo.set(core_width=self.bus_wg_width)

        def _default_ring_1(self):
            ring_cell_layout = self.cell.ring_1.get_default_view(i3.LayoutView)
            ring_cell_layout.set(angle=180,
                                 bend_radius=self.ring_radius,
                                 straight_length=0)
            return ring_cell_layout

        def _default_ring_2(self):
            ring_cell_layout = self.cell.ring_2.get_default_view(i3.LayoutView)
            ring_cell_layout.set(angle=180,
                                 bend_radius=self.ring_radius,
                                 straight_length=0)
            return ring_cell_layout

        def _default_ring_aux_1(self):
            circle_shape = i3.ShapeArc(radius=self.ring_radius_aux,
                                       center=(self.ring_straight_length_aux * 0.5, 0),
                                       start_angle=-90,
                                       end_angle=0,
                                       angle_step=0.2)

            circle_shape_mirror = circle_shape.h_mirror_copy().reverse()

            # ring_shape = i3.Shape([(-self.ring_straight_length * 0.5, -self.ring_radius),
            #                        (self.ring_straight_length * 0.5, -self.ring_radius)]) +\
            #              circle_shape + \
            #              i3.Shape([(self.ring_straight_length * 0.5, self.ring_radius),
            #                        (-self.ring_straight_length * 0.5, self.ring_radius)]) + \
            #              circle_shape.h_mirror_copy().reverse()

            straight_shape = i3.Shape([(-self.ring_straight_length_aux * 0.5, -self.ring_radius_aux),
                                       (self.ring_straight_length_aux * 0.5, -self.ring_radius_aux)])

            ring_shape = circle_shape_mirror + straight_shape + circle_shape

            # ring_shape.close()

            ring_aux_cell_layout = self.cell.ring_aux_1.get_default_view(i3.LayoutView)
            ring_aux_cell_layout.set(shape=ring_shape, bend_radius=self.ring_radius_aux, angle_step=0.2)
            return ring_aux_cell_layout

        def _default_ring_aux_2(self):
            circle_shape = i3.ShapeArc(radius=self.ring_radius_aux,
                                       center=(self.ring_straight_length_aux * 0.5, 0),
                                       start_angle=-0.25,
                                       end_angle=90,
                                       angle_step=0.2)

            circle_shape_mirror = circle_shape.h_mirror_copy().reverse()

            # ring_shape = i3.Shape([(-self.ring_straight_length * 0.5, -self.ring_radius),
            #                        (self.ring_straight_length * 0.5, -self.ring_radius)]) +\
            #              circle_shape + \
            #              i3.Shape([(self.ring_straight_length * 0.5, self.ring_radius),
            #                        (-self.ring_straight_length * 0.5, self.ring_radius)]) + \
            #              circle_shape.h_mirror_copy().reverse()

            straight_shape = i3.Shape([(-self.ring_straight_length_aux * 0.5, self.ring_radius_aux),
                                       (self.ring_straight_length_aux * 0.5, self.ring_radius_aux)])

            ring_shape = circle_shape + straight_shape + circle_shape_mirror

            # ring_shape.close()

            ring_aux_cell_layout = self.cell.ring_aux_2.get_default_view(i3.LayoutView)
            ring_aux_cell_layout.set(shape=ring_shape, bend_radius=self.ring_radius_aux, angle_step=0.2)
            return ring_aux_cell_layout

        def _default_bus_waveguide(self):
            # set the layout parameters of the waveguide
            r = 0
            a = 0.5 * self.coupler_bend_angle
            s = i3.TECH.RWG.SHORT_STRAIGHT
            l = self.coupler_straight_length / 2.0

            # Bus waveguide layout
            bend_layout = self.cell.bus_waveguide.get_default_view(i3.LayoutView)  # default bus layout view
            bend_layout.set(bend_radius=self.coupler_bend_radius,
                            trace_template=self.bus_trace_template,
                            rounding_algorithm=SBendAlgorithm,
                            angle_step=0.2)

            b1, b2 = bend_layout.get_bend_size(a)  # calculates the size of the waveguide bend
            # control shape for the bus waveguide (one half)
            # the RoundedWaveguide will automatically generate smooth bends
            s1 = i3.Shape([(0.0, -r), (-l - b1, -r)])
            s1.add_polar(2 * b2, 180.0 - a)
            s1.add_polar(b1 + s, 180.0)
            # stitching 2 halves together
            bend_shape = s1.reversed().v_mirror_copy(mirror_plane_y=-r) + s1.h_mirror_copy().v_mirror_copy(
                mirror_plane_y=-r)

            # assigning the shape to the bus
            bend_layout.set(shape=bend_shape,
                            draw_control_shape=False)
            return bend_layout

        def _default_rf_electrode(self):
            electrode_layout = self.cell.rf_electrode.get_default_view(i3.LayoutView)
            electrode_layout.set(electrode_length=self.electrode_length,
                                 taper_length=self.taper_length,
                                 hot_width=self.hot_width,
                                 ground_width=self.ground_width,
                                 electrode_gap=self.electrode_gap,
                                 hot_taper_width=self.hot_taper_width,
                                 taper_gap=self.taper_gap,
                                 taper_straight_length=self.taper_straight_length
                                 )
            return electrode_layout

        def _default_heater(self):
            heater_layout = self.cell.heater.get_default_view(i3.LayoutView)
            heater_layout.set(heater_length=self.ring_radius_aux * 2 + 8,
                              pad_spacing=self.ring_radius_aux * 2 + self.ring_straight_length_aux + 4,
                              curvature=self.ring_radius_aux + 4)
            return heater_layout

        def _generate_instances(self, insts):
            ring_wg_width = self.ring_trace_template.core_width
            bus_wg_width = self.bus_trace_template.core_width

            insts += i3.SRef(name='ring_1', reference=self.ring_1,
                             position=(-self.ring_straight_length * 0.5, self.ring_radius+self.ground_width+self.electrode_gap), transformation=i3.HMirror())
            insts += i3.SRef(name='ring_2', reference=self.ring_2, position=(self.ring_straight_length * 0.5, self.ring_radius+self.ground_width+self.electrode_gap))

            ring_1_in = [-self.ring_straight_length * 0.5, self.ring_radius+self.ground_width+self.electrode_gap]
            ring_2_in = [self.ring_straight_length * 0.5, self.ring_radius+self.ground_width+self.electrode_gap]

            link1_shape1 = i3.Shape([ring_1_in, ring_2_in])

            link1 = i3.RoundedWaveguide(trace_template=self.ring_trace_template)
            link1_lo1 = link1.Layout(shape=link1_shape1)
            insts += i3.SRef(reference=link1_lo1)

            ring_1_in = [-self.ring_straight_length * 0.5, -self.ring_radius- 46.264]
            ring_2_in = [self.ring_straight_length * 0.5, -self.ring_radius- 46.264]

            link1_shape1 = i3.Shape([ring_1_in, ring_2_in])

            link1 = i3.RoundedWaveguide(trace_template=self.ring_trace_template)
            link1_lo1 = link1.Layout(shape=link1_shape1)
            insts += i3.SRef(reference=link1_lo1)

            insts += i3.SRef(name='ring_aux_1', reference=self.ring_aux_1, position=(-self.ring_straight_length * 0.45,
                                                                                     -self.ring_radius - self.ring_radius_aux - ring_wg_width - self.aux_coupling_gap- 46.264))
            insts += i3.SRef(name='ring_aux_2', reference=self.ring_aux_2, position=(-self.ring_straight_length * 0.45,
                                                                                     -self.ring_radius - self.ring_radius_aux - ring_wg_width - self.aux_coupling_gap- 46.264))
            insts += i3.SRef(name='bus_in_through', reference=self.bus_waveguide,
                             position=(self.coupler_positions[0],
                                       -self.ring_radius - ring_wg_width * 0.5 - self.coupler_spacing - bus_wg_width * 0.5- 46.264))
            insts += i3.SRef(name='bus_add_drop', reference=self.bus_waveguide,
                             position=(self.coupler_positions[1],
                                       -self.ring_radius - ring_wg_width * 0.5 - self.coupler_spacing - bus_wg_width * 0.5- 46.264)
                             )

            # Heater
            # insts += i3.SRef(name='heater', reference=self.heater, position=(
            # -self.ring_straight_length * 0.45 - self.ring_straight_length_aux * 0.5 - self.ring_radius_aux - 4,
            # -self.ring_radius - self.ring_radius_aux - ring_wg_width - self.aux_coupling_gap))

            # RF electrode
            insts += i3.SRef(name='electrode', reference=self.rf_electrode,
                             position=(0,
                                       self.ring_radius + self.electrode_gap * 0.5 + self.hot_width * 0.5 - self.hot_width - self.electrode_gap))

            return insts

        def _generate_ports(self, ports):
            ports += i3.expose_ports(self.instances, {
                'bus_in_through:in': 'in',
                'bus_in_through:out': 'through',
                'bus_add_drop:in': 'add',
                'bus_add_drop:out': 'drop',
            })

            return ports

    class Netlist(i3.NetlistFromLayout):
        pass

# class AddDropRingWithAuxOutside3(i3.PCell):
#     """
#     Add-drop racetrack ring with a travelling electrode
#     """
#     ring_trace_template = i3.TraceTemplateProperty(doc="the trace template for ring")
#     ring_aux_trace_template = i3.TraceTemplateProperty(doc="the trace template for aux ring")
#     bus_trace_template = i3.TraceTemplateProperty(doc="the trace template for bus wg")
#     ring = i3.ChildCellProperty(locked=True, doc="the ring")
#     ring_aux_1 = i3.ChildCellProperty(locked=True, doc="the ring")
#     ring_aux_2 = i3.ChildCellProperty(locked=True, doc="the ring")
#     heater = i3.ChildCellProperty(locked=True, doc="the heater")
#     bus_waveguide = i3.ChildCellProperty(locked=True, doc="the bus waveguide of the coupler")
#     rf_electrode = i3.ChildCellProperty(locked=True, doc="the RF electrode")
#
#     def _default_ring_aux_trace_template(self):
#         return asp.SiNRibWaveguideTemplate()
#
#     def _default_ring_trace_template(self):
#         return asp.SiNRibWaveguideTemplate()
#
#     def _default_bus_trace_template(self):
#         return asp.SiNRibWaveguideTemplate()
#
#     def _default_ring(self):
#         return asp.RoundedRibWaveguide(trace_template=self.ring_trace_template)
#
#     def _default_ring_aux_1(self):
#         return asp.RoundedRibWaveguide(trace_template=self.ring_aux_trace_template)
#
#     def _default_ring_aux_2(self):
#         return asp.RoundedRibWaveguide(trace_template=self.ring_trace_template)
#
#     def _default_rf_electrode(self):
#         return RFElectrode()
#
#     def _default_heater(self):
#         return Hiephiep()
#
#     def _default_bus_waveguide(self):
#         return asp.RoundedRibWaveguide(trace_template=self.bus_trace_template)
#
#     class Layout(i3.LayoutView):
#         aux_coupling_gap = i3.NumberProperty(default=0.0, doc="gap between main ring and auxiliary ring")
#         ring_radius = i3.PositiveNumberProperty(default=100, doc="ring radius")
#         ring_radius_aux = i3.PositiveNumberProperty(default=100, doc="ring radius")
#         ring_straight_length = i3.PositiveNumberProperty(default=3000.0, doc="the circumference of the ring")
#         ring_straight_length_aux = i3.PositiveNumberProperty(default=3000.0, doc="the circumference of the ring")
#         coupler_straight_length = i3.NumberProperty(default=0.0,
#                                                     doc="the length of the directional coupler straight section")
#         coupler_positions = i3.ListProperty(doc="location of the two couplers")
#
#         coupler_spacing = i3.PositiveNumberProperty(default=1.0,
#                                                     doc="spacing between edges of two waveguides")
#         coupler_bend_angle = i3.PositiveNumberProperty(default=30.0,
#                                                        doc="angular span (in degrees) of the bend waveguide")
#         coupler_bend_radius = i3.PositiveNumberProperty(default=300.0,
#                                                         doc="bending radius of the coupler bus waveguide")
#         ring_wg_width = i3.PositiveNumberProperty(default=1.03, doc="the width of the waveguide1")
#         bus_wg_width = i3.PositiveNumberProperty(default=1.03, doc="the width of the waveguide2")
#         cladding_width = i3.PositiveNumberProperty(default=30.0, doc="the width of cladding")
#         heater_gap = i3.PositiveNumberProperty(default=10, doc="the length of the electrode")
#         electrode_length = i3.PositiveNumberProperty(default=0, doc="the length of the electrode")
#         taper_length = i3.PositiveNumberProperty(default=100.0, doc="the length of the taper")
#         hot_width = i3.PositiveNumberProperty(default=23.0, doc="width of the hot electrode")
#         ground_width = i3.PositiveNumberProperty(default=100.0, doc="width of the ground planes")
#         electrode_gap = i3.PositiveNumberProperty(default=7.0, doc="gap between hot electrode and ground plane")
#         hot_taper_width = i3.PositiveNumberProperty(default=50.0,
#                                                     doc="width of the hot electrode at the end of the taper")
#         taper_gap = i3.PositiveNumberProperty(default=20.0,
#                                               doc="gap between hot electrode and ground plane at the end of the taper")
#         taper_straight_length = i3.PositiveNumberProperty(default=10.0,
#                                                           doc="length of the straight section at the end of the taper")
#
#         def _default_coupler_positions(self):
#             return [-self.ring_straight_length * 0.125 + self.coupler_straight_length,
#                     self.ring_straight_length * 0.125 - self.coupler_straight_length]
#
#         def _default_ring_aux_trace_template(self):
#             lo = self.cell.ring_aux_trace_template.get_default_view(i3.LayoutView)
#             lo.set(core_width=self.ring_wg_width, cladding_width=self.cladding_width)
#
#         def _default_ring_trace_template(self):
#             lo = self.cell.ring_trace_template.get_default_view(i3.LayoutView)
#             lo.set(core_width=self.ring_wg_width)
#
#         def _default_bus_trace_template(self):
#             lo = self.cell.bus_trace_template.get_default_view(i3.LayoutView)
#             lo.set(core_width=self.bus_wg_width)
#
#         def _default_ring(self):
#             circle_shape = i3.ShapeArc(radius=self.ring_radius,
#                                        center=(self.ring_straight_length * 0.5, 0),
#                                        start_angle=-90,
#                                        end_angle=90,
#                                        angle_step=0.2)
#
#             circle_shape_mirror = circle_shape.h_mirror_copy().reverse()
#
#             # ring_shape = i3.Shape([(-self.ring_straight_length * 0.5, -self.ring_radius),
#             #                        (self.ring_straight_length * 0.5, -self.ring_radius)]) +\
#             #              circle_shape + \
#             #              i3.Shape([(self.ring_straight_length * 0.5, self.ring_radius),
#             #                        (-self.ring_straight_length * 0.5, self.ring_radius)]) + \
#             #              circle_shape.h_mirror_copy().reverse()
#
#             ring_shape = circle_shape + circle_shape_mirror
#
#             ring_shape.close()
#
#             ring_cell_layout = self.cell.ring.get_default_view(i3.LayoutView)
#             ring_cell_layout.set(shape=ring_shape, bend_radius=self.ring_radius, angle_step=0.2)
#             return ring_cell_layout
#
#         def _default_ring_aux_1(self):
#             circle_shape = i3.ShapeArc(radius=self.ring_radius_aux,
#                                        center=(self.ring_straight_length_aux * 0.5, 0),
#                                        start_angle=-90,
#                                        end_angle=0,
#                                        angle_step=0.2)
#
#             circle_shape_mirror = circle_shape.h_mirror_copy().reverse()
#
#             # ring_shape = i3.Shape([(-self.ring_straight_length * 0.5, -self.ring_radius),
#             #                        (self.ring_straight_length * 0.5, -self.ring_radius)]) +\
#             #              circle_shape + \
#             #              i3.Shape([(self.ring_straight_length * 0.5, self.ring_radius),
#             #                        (-self.ring_straight_length * 0.5, self.ring_radius)]) + \
#             #              circle_shape.h_mirror_copy().reverse()
#
#             straight_shape = i3.Shape([(-self.ring_straight_length_aux * 0.5, -self.ring_radius_aux),
#                                        (self.ring_straight_length_aux * 0.5, -self.ring_radius_aux)])
#
#             ring_shape = circle_shape_mirror + straight_shape + circle_shape
#
#             # ring_shape.close()
#
#             ring_aux_cell_layout = self.cell.ring_aux_1.get_default_view(i3.LayoutView)
#             ring_aux_cell_layout.set(shape=ring_shape, bend_radius=self.ring_radius_aux, angle_step=0.2)
#             return ring_aux_cell_layout
#
#         def _default_ring_aux_2(self):
#             circle_shape = i3.ShapeArc(radius=self.ring_radius_aux,
#                                        center=(self.ring_straight_length_aux * 0.5, 0),
#                                        start_angle=-0.25,
#                                        end_angle=90,
#                                        angle_step=0.2)
#
#             circle_shape_mirror = circle_shape.h_mirror_copy().reverse()
#
#             # ring_shape = i3.Shape([(-self.ring_straight_length * 0.5, -self.ring_radius),
#             #                        (self.ring_straight_length * 0.5, -self.ring_radius)]) +\
#             #              circle_shape + \
#             #              i3.Shape([(self.ring_straight_length * 0.5, self.ring_radius),
#             #                        (-self.ring_straight_length * 0.5, self.ring_radius)]) + \
#             #              circle_shape.h_mirror_copy().reverse()
#
#             straight_shape = i3.Shape([(-self.ring_straight_length_aux * 0.5, self.ring_radius_aux),
#                                        (self.ring_straight_length_aux * 0.5, self.ring_radius_aux)])
#
#             ring_shape = circle_shape + straight_shape + circle_shape_mirror
#
#             # ring_shape.close()
#
#             ring_aux_cell_layout = self.cell.ring_aux_2.get_default_view(i3.LayoutView)
#             ring_aux_cell_layout.set(shape=ring_shape, bend_radius=self.ring_radius_aux, angle_step=0.2)
#             return ring_aux_cell_layout
#
#         def _default_bus_waveguide(self):
#             # set the layout parameters of the waveguide
#             r = 0
#             a = 0.5 * self.coupler_bend_angle
#             s = i3.TECH.RWG.SHORT_STRAIGHT
#             l = self.coupler_straight_length / 2.0
#
#             # Bus waveguide layout
#             bend_layout = self.cell.bus_waveguide.get_default_view(i3.LayoutView)  # default bus layout view
#             bend_layout.set(bend_radius=self.coupler_bend_radius,
#                             trace_template=self.bus_trace_template,
#                             rounding_algorithm=SBendAlgorithm,
#                             angle_step=0.2)
#
#             b1, b2 = bend_layout.get_bend_size(a)  # calculates the size of the waveguide bend
#             # control shape for the bus waveguide (one half)
#             # the RoundedWaveguide will automatically generate smooth bends
#             s1 = i3.Shape([(0.0, -r), (-l - b1, -r)])
#             s1.add_polar(2 * b2, 180.0 - a)
#             s1.add_polar(b1 + s, 180.0)
#             # stitching 2 halves together
#             bend_shape = s1.reversed().v_mirror_copy(mirror_plane_y=-r) + s1.h_mirror_copy().v_mirror_copy(
#                 mirror_plane_y=-r)
#
#             # assigning the shape to the bus
#             bend_layout.set(shape=bend_shape,
#                             draw_control_shape=False)
#             return bend_layout
#
#         def _default_rf_electrode(self):
#             electrode_layout = self.cell.rf_electrode.get_default_view(i3.LayoutView)
#             electrode_layout.set(electrode_length=self.electrode_length,
#                                  taper_length=self.taper_length,
#                                  hot_width=self.hot_width,
#                                  ground_width=self.ground_width,
#                                  electrode_gap=self.electrode_gap,
#                                  hot_taper_width=self.hot_taper_width,
#                                  taper_gap=self.taper_gap,
#                                  taper_straight_length=self.taper_straight_length
#                                  )
#             return electrode_layout
#
#         def _default_heater(self):
#             heater_layout = self.cell.heater.get_default_view(i3.LayoutView)
#             heater_layout.set(heater_length=self.ring_radius_aux * 2 + 8,
#                               pad_spacing=self.ring_radius_aux * 2 + self.ring_straight_length_aux + 4,
#                               curvature=self.ring_radius_aux + 4)
#             return heater_layout
#
#         def _generate_instances(self, insts):
#             ring_wg_width = self.ring_trace_template.core_width
#             bus_wg_width = self.bus_trace_template.core_width
#             insts += i3.SRef(name='ring', reference=self.ring, position=(0, 0))
#             insts += i3.SRef(name='ring_aux_1', reference=self.ring_aux_1, position=(-self.ring_straight_length * 0.45,
#                                                                                      -self.ring_radius - self.ring_radius_aux - ring_wg_width - self.aux_coupling_gap))
#             insts += i3.SRef(name='ring_aux_2', reference=self.ring_aux_2, position=(-self.ring_straight_length * 0.45,
#                                                                                      -self.ring_radius - self.ring_radius_aux - ring_wg_width - self.aux_coupling_gap))
#             insts += i3.SRef(name='bus_in_through', reference=self.bus_waveguide,
#                              position=(self.coupler_positions[0],
#                                        -self.ring_radius - ring_wg_width * 0.5 - self.coupler_spacing - bus_wg_width * 0.5))
#             insts += i3.SRef(name='bus_add_drop', reference=self.bus_waveguide,
#                              position=(self.coupler_positions[1],
#                                        -self.ring_radius - ring_wg_width * 0.5 - self.coupler_spacing - bus_wg_width * 0.5)
#                              )
#
#             # Heater
#             # insts += i3.SRef(name='heater', reference=self.heater, position=(
#             # -self.ring_straight_length * 0.45 - self.ring_straight_length_aux * 0.5 - self.ring_radius_aux - 4,
#             # -self.ring_radius - self.ring_radius_aux - ring_wg_width - self.aux_coupling_gap))
#
#             # RF electrode
#             insts += i3.SRef(name='electrode', reference=self.rf_electrode,
#                              position=(0,
#                                        self.ring_radius + self.electrode_gap * 0.5 + self.hot_width * 0.5 - self.hot_width - self.electrode_gap))
#
#             return insts
#
#         def _generate_ports(self, ports):
#             ports += i3.expose_ports(self.instances, {
#                 'bus_in_through:in': 'in',
#                 'bus_in_through:out': 'through',
#                 'bus_add_drop:in': 'add',
#                 'bus_add_drop:out': 'drop',
#             })
#
#             return ports
#
#     class Netlist(i3.NetlistFromLayout):
#         pass