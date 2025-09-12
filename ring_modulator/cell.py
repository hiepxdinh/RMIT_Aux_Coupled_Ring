import ipkiss3.all as i3

import asp_sin_lnoi_photonics.all as asp

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
        electrode_gap = i3.PositiveNumberProperty(default=7.0, doc="gap between hot electrode and ground plane")
        hot_taper_width = i3.PositiveNumberProperty(default=50.0, doc="width of the hot electrode at the end of the taper")
        taper_gap = i3.PositiveNumberProperty(default=20.0,
                                                    doc="gap between hot electrode and ground plane at the end of the taper")
        taper_straight_length = i3.PositiveNumberProperty(default=10.0, doc="length of the straight section at the end of the taper")

        def _generate_elements(self, elems):
            # Hot electrode
            #elems += i3.Rectangle(self.layer, center=(0.0, 0.0), box_size=(self.electrode_length, self.hot_width))

            he_taper_shape1 = i3.Shape(points=[(-self.electrode_length * 0.5, -self.hot_width * 0.5),
                                                           (-self.electrode_length * 0.5 - self.taper_length,
                                                            -self.hot_width * 0.5)
                                                           ],
                                           )

            he_taper_shape2 = i3.ShapeRound(original_shape=[(-self.electrode_length * 0.5 - self.taper_length,
                                                            -self.hot_width * 0.5 + self.hot_taper_width),
                                                            (-self.electrode_length * 0.5 - self.taper_length + self.taper_straight_length,
                                                             -self.hot_width * 0.5 + self.hot_taper_width),
                                                            (-self.electrode_length * 0.5 - self.taper_straight_length,
                                                             self.hot_width * 0.5),
                                                            (-self.electrode_length * 0.5, self.hot_width * 0.5),
                                                           ],
                                           radius=50.0)

            he_taper_shape = he_taper_shape1 + he_taper_shape2 + he_taper_shape2.h_mirror_copy().reverse() + he_taper_shape1.h_mirror_copy().reverse()
            he_taper_shape.close()
            elems += i3.Boundary(layer=self.layer, shape=he_taper_shape)

            # Top ground plane
            grnd_taper_shape1 = i3.ShapeRound(original_shape=[(-self.electrode_length * 0.5, self.hot_width * 0.5 + self.electrode_gap),
                                                            (-self.electrode_length * 0.5 - self.taper_straight_length,
                                                             self.hot_width * 0.5 + self.electrode_gap),
                                                            (
                                                            -self.electrode_length * 0.5 - self.taper_length + self.taper_straight_length,
                                                            -self.hot_width * 0.5 + self.taper_gap + self.hot_taper_width),
                                                            (-self.electrode_length * 0.5 - self.taper_length,
                                                             -self.hot_width * 0.5 + self.taper_gap + self.hot_taper_width)
                                                            ],
                                            radius=50.0)

            grnd_taper_shape2 = i3.Shape(points=[(-self.electrode_length * 0.5 - self.taper_length,
                                                             self.hot_width * 0.5 + self.electrode_gap + self.ground_width),
                                                            (-self.electrode_length * 0.5,
                                                             self.hot_width * 0.5 + self.electrode_gap + self.ground_width)])

            top_grnd_taper_shape = grnd_taper_shape1 + grnd_taper_shape2 +  grnd_taper_shape2.h_mirror_copy().reverse() + grnd_taper_shape1.h_mirror_copy().reverse()
            top_grnd_taper_shape.close()
            elems += i3.Boundary(layer=self.layer, shape=top_grnd_taper_shape)

            # Bottom ground plane
            grnd_taper_shape3 = i3.ShapeRound(
                original_shape=[(-self.electrode_length * 0.5, -self.hot_width * 0.5 - self.electrode_gap),
                                (-self.electrode_length * 0.5 - self.taper_straight_length,
                                 -self.hot_width * 0.5 - self.electrode_gap),
                                (
                                    -self.electrode_length * 0.5 - self.taper_length + self.taper_straight_length,
                                    -self.hot_width * 0.5 - self.taper_gap),
                                (-self.electrode_length * 0.5 - self.taper_length,
                                 -self.hot_width * 0.5 - self.taper_gap)
                                ],
                radius=50.0)

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
                                            self.hot_width + self.electrode_gap * 2 + self.ground_width * 2))

            return elems

    class Netlist(i3.NetlistFromLayout):
        pass

class AddDropRingWithElectrode(i3.PCell):
    """
    Add-drop racetrack ring with a travelling electrode
    """
    ring_trace_template = i3.TraceTemplateProperty(doc="the trace template for ring")
    bus_trace_template = i3.TraceTemplateProperty(doc="the trace template for bus wg")
    ring_1 = i3.ChildCellProperty(locked=True, doc="the ring")
    ring_2 = i3.ChildCellProperty(locked=True, doc="the ring")
    bus_waveguide = i3.ChildCellProperty(locked=True, doc="the bus waveguide of the coupler")
    rf_electrode = i3.ChildCellProperty(locked=True, doc="the RF electrode")

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

    def _default_rf_electrode(self):
        return RFElectrode()

    def _default_bus_waveguide(self):
        return asp.RoundedRibWaveguide(trace_template=self.bus_trace_template)

    class Layout(i3.LayoutView):
        ring_radius = i3.PositiveNumberProperty(default=100, doc="ring radius")
        ring_straight_length = i3.PositiveNumberProperty(default=3000.0, doc="the circumference of the ring")
        coupler_straight_length = i3.NumberProperty(default=0.0, doc="the length of the directional coupler straight section")
        coupler_positions = i3.ListProperty(doc="location of the two couplers")

        coupler_spacing = i3.PositiveNumberProperty(default=1.0,
                                                    doc="spacing between edges of two waveguides")
        coupler_bend_angle = i3.PositiveNumberProperty(default=30.0,
                                               doc="angular span (in degrees) of the bend waveguide")
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


        def _default_coupler_positions(self):
            return [-self.ring_straight_length * 0.125 + self.coupler_straight_length,
                    self.ring_straight_length * 0.125 - self.coupler_straight_length]

        def _default_ring_trace_template(self):
           lo=self.cell.ring_trace_template.get_default_view(i3.LayoutView)
           lo.set(core_width=self.ring_wg_width, cladding_width=self.cladding_width)

        def _default_bus_trace_template(self):
           lo=self.cell.bus_trace_template.get_default_view(i3.LayoutView)
           lo.set(core_width=self.bus_wg_width, cladding_width=self.cladding_width)

        def _default_ring_1(self):

            # circle_shape = i3.ShapeArc(radius=self.ring_radius,
            #                          center=(self.ring_straight_length * 0.5, 0),
            #                          start_angle=-90,
            #                          end_angle=90,
            #                          angle_step=0.2)
            #
            # circle_shape_mirror = circle_shape.h_mirror_copy().reverse()

            # ring_shape = circle_shape + circle_shape_mirror
            #
            # ring_shape.close()

            # ring = asp.EulerBend(trace_template=self.ring_trace_template)

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
        
        def _generate_instances(self, insts):
            ring_wg_width = self.ring_trace_template.core_width
            bus_wg_width = self.bus_trace_template.core_width
            insts += i3.SRef(name='ring_1', reference=self.ring_1, position=(-self.ring_straight_length*0.5, -172.575), transformation=i3.HMirror())
            insts += i3.SRef(name='ring_2', reference=self.ring_2, position=(self.ring_straight_length*0.5, -172.575))

            # Connect input inverse_taper couplers to ring
            # ring_1_in = self.ring_1.ports["in"].position.modified_copy()
            # ring_2_in = self.ring_1.ports["in"].position.modified_copy()

            ring_1_in = [-self.ring_straight_length*0.5, -172.575]
            ring_2_in = [self.ring_straight_length*0.5, -172.575]

            link1_shape1 = i3.Shape([ring_1_in, ring_2_in])

            link1 = i3.RoundedWaveguide(trace_template=self.ring_trace_template)
            link1_lo1 = link1.Layout(shape=link1_shape1)
            insts += i3.SRef(reference=link1_lo1)

            ring_1_in = [-self.ring_straight_length*0.5, 2*self.ring_radius+30.172-172.575]
            ring_2_in = [self.ring_straight_length*0.5, 2*self.ring_radius+30.172-172.575]

            link1_shape1 = i3.Shape([ring_1_in, ring_2_in])

            link1 = i3.RoundedWaveguide(trace_template=self.ring_trace_template)
            link1_lo1 = link1.Layout(shape=link1_shape1)
            insts += i3.SRef(reference=link1_lo1)


            insts += i3.SRef(name='bus_in_through', reference=self.bus_waveguide,
                             position=(self.coupler_positions[0], -172.575 - ring_wg_width*0.5 - bus_wg_width*0.5 - self.coupler_spacing))
            insts += i3.SRef(name='bus_add_drop', reference=self.bus_waveguide,
                             position=(self.coupler_positions[1], -172.575 - ring_wg_width*0.5 - bus_wg_width*0.5 - self.coupler_spacing)
                             )

            # RF electrode

            insts += i3.SRef(name='electrode', reference=self.rf_electrode,
                             position=(0, 2*self.ring_radius+30.172-172.575 + self.electrode_gap * 0.5 + self.hot_width * 0.5))

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

class AddDropRingWithOutElectrode(i3.PCell):
    """
    Add-drop racetrack ring with a travelling electrode
    """
    ring_trace_template = i3.TraceTemplateProperty(doc="the trace template for ring")
    bus_trace_template = i3.TraceTemplateProperty(doc="the trace template for bus wg")
    ring_1 = i3.ChildCellProperty(locked=True, doc="the ring")
    ring_2 = i3.ChildCellProperty(locked=True, doc="the ring")
    bus_waveguide = i3.ChildCellProperty(locked=True, doc="the bus waveguide of the coupler")
    rf_electrode = i3.ChildCellProperty(locked=True, doc="the RF electrode")

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

    def _default_rf_electrode(self):
        return RFElectrode()

    def _default_bus_waveguide(self):
        return asp.RoundedRibWaveguide(trace_template=self.bus_trace_template)

    class Layout(i3.LayoutView):
        ring_radius = i3.PositiveNumberProperty(default=100, doc="ring radius")
        ring_straight_length = i3.PositiveNumberProperty(default=3000.0, doc="the circumference of the ring")
        coupler_straight_length = i3.NumberProperty(default=0.0,
                                                    doc="the length of the directional coupler straight section")
        coupler_positions = i3.ListProperty(doc="location of the two couplers")

        coupler_spacing = i3.PositiveNumberProperty(default=1.0,
                                                    doc="spacing between edges of two waveguides")
        coupler_bend_angle = i3.PositiveNumberProperty(default=30.0,
                                                       doc="angular span (in degrees) of the bend waveguide")
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

        def _default_coupler_positions(self):
            return [-self.ring_straight_length * 0.125 + self.coupler_straight_length,
                    self.ring_straight_length * 0.125 - self.coupler_straight_length]

        def _default_ring_trace_template(self):
           lo=self.cell.ring_trace_template.get_default_view(i3.LayoutView)
           lo.set(core_width=self.ring_wg_width, cladding_width=self.cladding_width)

        def _default_bus_trace_template(self):
           lo=self.cell.bus_trace_template.get_default_view(i3.LayoutView)
           lo.set(core_width=self.bus_wg_width, cladding_width=self.cladding_width)

        def _default_ring_1(self):
            # circle_shape = i3.ShapeArc(radius=self.ring_radius,
            #                          center=(self.ring_straight_length * 0.5, 0),
            #                          start_angle=-90,
            #                          end_angle=90,
            #                          angle_step=0.2)
            #
            # circle_shape_mirror = circle_shape.h_mirror_copy().reverse()

            # ring_shape = circle_shape + circle_shape_mirror
            #
            # ring_shape.close()

            # ring = asp.EulerBend(trace_template=self.ring_trace_template)

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

        def _generate_instances(self, insts):
            ring_wg_width = self.ring_trace_template.core_width
            bus_wg_width = self.bus_trace_template.core_width
            insts += i3.SRef(name='ring_1', reference=self.ring_1,
                             position=(-self.ring_straight_length * 0.5, -172.575), transformation=i3.HMirror())
            insts += i3.SRef(name='ring_2', reference=self.ring_2, position=(self.ring_straight_length * 0.5, -172.575))

            # Connect input inverse_taper couplers to ring
            # ring_1_in = self.ring_1.ports["in"].position.modified_copy()
            # ring_2_in = self.ring_1.ports["in"].position.modified_copy()

            ring_1_in = [-self.ring_straight_length * 0.5, -172.575]
            ring_2_in = [self.ring_straight_length * 0.5, -172.575]

            link1_shape1 = i3.Shape([ring_1_in, ring_2_in])

            link1 = i3.RoundedWaveguide(trace_template=self.ring_trace_template)
            link1_lo1 = link1.Layout(shape=link1_shape1)
            insts += i3.SRef(reference=link1_lo1)

            ring_1_in = [-self.ring_straight_length * 0.5, 2 * self.ring_radius + 30.172 - 172.575]
            ring_2_in = [self.ring_straight_length * 0.5, 2 * self.ring_radius + 30.172 - 172.575]

            link1_shape1 = i3.Shape([ring_1_in, ring_2_in])

            link1 = i3.RoundedWaveguide(trace_template=self.ring_trace_template)
            link1_lo1 = link1.Layout(shape=link1_shape1)
            insts += i3.SRef(reference=link1_lo1)

            insts += i3.SRef(name='bus_in_through', reference=self.bus_waveguide,
                             position=(self.coupler_positions[0],
                                       -172.575 - ring_wg_width * 0.5 - bus_wg_width * 0.5 - self.coupler_spacing))
            insts += i3.SRef(name='bus_add_drop', reference=self.bus_waveguide,
                             position=(self.coupler_positions[1],
                                       -172.575 - ring_wg_width * 0.5 - bus_wg_width * 0.5 - self.coupler_spacing)
                             )
            
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

# class AddDropRingWithOutElectrode(i3.PCell):
#     """
#     Add-drop racetrack ring with a travelling electrode
#     """
#     ring_trace_template = i3.TraceTemplateProperty(doc="the trace template for ring")
#     bus_trace_template = i3.TraceTemplateProperty(doc="the trace template for bus wg")
#     ring = i3.ChildCellProperty(locked=True, doc="the ring")
#     bus_waveguide = i3.ChildCellProperty(locked=True, doc="the bus waveguide of the coupler")
#     rf_electrode = i3.ChildCellProperty(locked=True, doc="the RF electrode")
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
#     def _default_rf_electrode(self):
#         return RFElectrode()
#
#     def _default_bus_waveguide(self):
#         return asp.RoundedRibWaveguide(trace_template=self.bus_trace_template)
#
#     class Layout(i3.LayoutView):
#         ring_radius = i3.PositiveNumberProperty(default=100, doc="ring radius")
#         ring_straight_length = i3.PositiveNumberProperty(default=3000.0, doc="the circumference of the ring")
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
#         ring_wg_width = i3.PositiveNumberProperty(default=1.06, doc="the width of the waveguide1")
#         bus_wg_width = i3.PositiveNumberProperty(default=1.06, doc="the width of the waveguide2")
#         cladding_width = i3.PositiveNumberProperty(default=20.0, doc="the width of cladding")
#
#         electrode_length = i3.PositiveNumberProperty(default=2000.0, doc="the length of the electrode")
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
#         # def _default_ring_trace_template(self):
#         #    lo=self.cell.ring_trace_template.get_default_view(i3.LayoutView)
#         #    lo.set(core_width=self.ring_wg_width, cladding_width=self.cladding_width)
#
#         # def _default_bus_trace_template(self):
#         #    lo=self.cell.bus_trace_template.get_default_view(i3.LayoutView)
#         #    lo.set(core_width=self.bus_wg_width, cladding_width=self.cladding_width)
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
#         def _generate_instances(self, insts):
#             ring_wg_width = self.ring_trace_template.core_width
#             bus_wg_width = self.bus_trace_template.core_width
#             insts += i3.SRef(name='ring', reference=self.ring, position=(0, 0))
#             insts += i3.SRef(name='bus_in_through', reference=self.bus_waveguide,
#                              position=(self.coupler_positions[0],
#                                        -self.ring_radius - ring_wg_width * 0.5 - self.coupler_spacing - bus_wg_width * 0.5))
#             insts += i3.SRef(name='bus_add_drop', reference=self.bus_waveguide,
#                              position=(self.coupler_positions[1],
#                                        -self.ring_radius - ring_wg_width * 0.5 - self.coupler_spacing - bus_wg_width * 0.5)
#                              )
#
#             # # RF electrode
#             #
#             # insts += i3.SRef(name='electrode', reference=self.rf_electrode,
#             #                  position=(0, self.ring_radius + self.electrode_gap * 0.5 + self.hot_width * 0.5))
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