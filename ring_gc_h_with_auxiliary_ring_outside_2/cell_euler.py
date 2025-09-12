import ipkiss3.all as i3

import asp_sin_lnoi_photonics.all as asp

from ring_modulator_with_auxiliary_ring_outside_2.cell import AddDropRingWithAuxOutside_Top_Euler, AddDropRingWithAuxOutside_Top_Euler_2


import ipkiss

ipkiss_version = ipkiss.__version__.split('.')

# if int(ipkiss_version[0]) <= 3 and int(ipkiss_version[1]) < 7:
#     from picazzo3.routing.place_route import PlaceAndAutoRoute
#
#     class RingModulatorGCHiepAuxOutside(PlaceAndAutoRoute):
#         ring = i3.ChildCellProperty(doc="the ring modulator")
#         gc = i3.ChildCellProperty(doc="the grating coupler")
#         trace_template = i3.TraceTemplateProperty(doc="the trace template for the circuit")
#
#         def _default_ring(self):
#             return AddDropRingWithAuxOutside(ring_trace_template=self.trace_template,
#                                             bus_trace_template=self.trace_template)
#
#         def _default_gc(self):
#             return asp.GRATING_COUPLER_TE1550_RIBZ()
#
#         def _default_trace_template(self):
#             return asp.SiNRibWaveguideTemplate()
#
#         #def _default_child_cells(self):
#         #    return {"ring": self.ring,
#         #            "in_grating": self.gc,
#         #            "through_grating": self.gc,
#         #            "add_grating": self.gc,
#         #            "drop_grating": self.gc,
#         #            }
#
#         #def _default_links(self):
#         #    return [("in_grating:out", "ring:in"),
#         #            ("through_grating:out", "ring:through"),
#         #            ("add_grating:out", "ring:add"),
#         #            ("drop_grating:out", "ring:drop")
#         #            ]
#
#
#
#         #def _default_external_port_names(self):
#         #    return {"in_grating:vertical_in": "in",
#         #            "through_grating:vertical_in": "through",
#         #            "add_grating:vertical_in": "add",
#         #            "drop_grating:vertical_in": "drop",
#         #            }
#
#         class Layout(PlaceAndAutoRoute.Layout):
#             gc_spacing = i3.PositiveNumberProperty(default=127, doc="fibre array pich")
#             ring_position = i3.Coord2Property(default=(-1000, -2000), doc="the position of the ring with respect to the gc.")
#             waveguide_spacing = i3.PositiveNumberProperty(default=20, doc="minimum spacing between parallel waveguides")
#             bend_radius = i3.PositiveNumberProperty(default=200, doc="radius of in waveguide routing")
#             gc_wg_distance = i3.PositiveNumberProperty(default=300, doc="distance between the grating coupler and waveguide bending corner")
#             ring_wg_distance = i3.PositiveNumberProperty(default=300,
#                                                     doc="distance between the ring in port and waveguide bending corner")
#             ring_radius = i3.PositiveNumberProperty(default=100, doc="ring radius")
#             ring_straight_length = i3.PositiveNumberProperty(default=3000.0, doc="the circumference of the ring")
#             coupler_straight_length = i3.NumberProperty(default=0.0,
#                                                         doc="the length of the directional coupler straight section")
#             coupler_positions = i3.ListProperty(doc="location of the two couplers")
#
#             coupler_spacing = i3.PositiveNumberProperty(default=1.0,
#                                                         doc="spacing between edges of two waveguides")
#             coupler_bend_radius = i3.PositiveNumberProperty(default=300.0,
#                                                             doc="bending radius of the coupler bus waveguide")
#             #ring_wg_width = i3.PositiveNumberProperty(default=1.03, doc="the width of the waveguide1")
#             #bus_wg_width = i3.PositiveNumberProperty(default=1.03, doc="the width of the waveguide2")
#             #cladding_width = i3.PositiveNumberProperty(default=20.0, doc="the width of cladding")
#
#             electrode_length = i3.PositiveNumberProperty(default=2000.0, doc="the length of the electrode")
#             taper_length = i3.PositiveNumberProperty(default=100.0, doc="the length of the taper")
#             hot_width = i3.PositiveNumberProperty(default=23.0, doc="width of the hot electrode")
#             ground_width = i3.PositiveNumberProperty(default=100.0, doc="width of the ground planes")
#             electrode_gap = i3.PositiveNumberProperty(default=7.0, doc="gap between hot electrode and ground plane")
#             hot_taper_width = i3.PositiveNumberProperty(default=50.0,
#                                                         doc="width of the hot electrode at the end of the taper")
#             taper_gap = i3.PositiveNumberProperty(default=20.0,
#                                                   doc="gap between hot electrode and ground plane at the end of the taper")
#             taper_straight_length = i3.PositiveNumberProperty(default=10.0,
#                                                               doc="length of the straight section at the end of the taper")
#
#             def _default_ring(self):
#                 ring_lo = self.cell.ring.get_default_view(i3.LayoutView)
#                 ring_lo.set(ring_radius=self.ring_radius,
#                             ring_straight_length=self.ring_straight_length,
#                             coupler_straight_length=self.coupler_straight_length,
#                             coupler_positions = self.coupler_positions,
#                             coupler_spacing = self.coupler_spacing,
#                             coupler_bend_radius=self.coupler_bend_radius,
#                             #ring_wg_width=self.ring_wg_width,
#                             #bus_wg_width=self.bus_wg_width,
#                             #cladding_width=self.cladding_width,
#                             electrode_length=self.electrode_length,
#                             taper_length=self.taper_length,
#                             hot_width=self.hot_width,
#                             ground_width=self.ground_width,
#                             electrode_gap=self.electrode_gap,
#                             hot_taper_width=self.hot_taper_width,
#                             taper_gap=self.taper_gap,
#                             taper_straight_length=self.taper_straight_length
#                             )
#
#                 return ring_lo
#
#             def _default_coupler_positions(self):
#                 return [-self.ring_straight_length * 0.125 + self.coupler_straight_length,
#                         self.ring_straight_length * 0.125 - self.coupler_straight_length]
#
#
#             def _default_child_transformations(self):
#                 child_transformations = {"in_grating": i3.Rotation(rotation=-90) + i3.Translation((self.gc_spacing * 1, 0)),
#                                          "through_grating": i3.Rotation(rotation=-90) + i3.Translation((self.gc_spacing * 2, 0)),
#                                          "add_grating": i3.Rotation(rotation=-90) + i3.Translation((self.gc_spacing * 3, 0)),
#                                          "drop_grating": i3.Rotation(rotation=-90) + i3.Translation(
#                                              (self.gc_spacing * 4, 0)),
#                                          "ring": i3.VMirror() + i3.Translation(self.ring_position)
#                                          }
#
#                 return child_transformations
#
#
#
#             def _default_waveguide_shapes(self):
#                 gc_in_pos = self.ports['in'].position
#                 ring_in_pos = self.child_cells['ring'].get_default_view(i3.LayoutView).ports['in'].position.modified_copy()
#                 ring_in_pos.transform(self.child_transformations['ring'])
#
#                 straight_extension = (self.end_straight + self.start_straight)
#                 #in_wg_shape = self.waveguides[0].shape.points
#                 #gc_in_pos = in_wg_shape[0]
#                 #ring_in_pos = in_wg_shape[-1]
#                 in_wg_shape = [gc_in_pos,
#                                (gc_in_pos[0], gc_in_pos[1] - self.gc_wg_distance),
#                                (ring_in_pos[0] - self.ring_wg_distance, gc_in_pos[1] - self.gc_wg_distance),
#                                (ring_in_pos[0] - self.ring_wg_distance, ring_in_pos[1]),
#                                ring_in_pos
#                              ]
#                 print(in_wg_shape)
#                 gc_through_pos = self.ports['through'].position
#                 ring_through_pos = self.child_cells['ring'].get_default_view(i3.LayoutView).ports['through'].position.modified_copy()
#                 ring_through_pos.transform(self.child_transformations['ring'])
#
#                 #through_wg_shape = self.waveguides[1].shape.points
#                 #gc_through_pos = through_wg_shape[0]
#                 #ring_through_pos = through_wg_shape[-1]
#                 through_wg_shape = [gc_through_pos,
#                                     (gc_through_pos[0], gc_in_pos[1] - self.gc_wg_distance + self.waveguide_spacing),
#                                     (ring_through_pos[0] + self.bend_radius + straight_extension,
#                                      gc_in_pos[1] - self.gc_wg_distance + self.waveguide_spacing),
#                                     (ring_through_pos[0] + self.bend_radius + straight_extension, ring_through_pos[1]),
#                                     ring_through_pos
#                                     ]
#                 print(through_wg_shape)
#                 gc_add_pos = self.ports['add'].position
#                 ring_add_pos = self.child_cells['ring'].get_default_view(i3.LayoutView).ports[
#                     'add'].position.modified_copy()
#                 ring_add_pos.transform(self.child_transformations['ring'])
#
#                 #add_wg_shape = self.waveguides[2].shape.points
#                 #gc_add_pos = add_wg_shape[0]
#                 #ring_add_pos = add_wg_shape[-1]
#                 add_wg_shape = [gc_add_pos,
#                                 (gc_add_pos[0], gc_in_pos[1] - self.gc_wg_distance + self.waveguide_spacing * 2),
#                                 (ring_add_pos[0] - self.bend_radius - straight_extension,
#                                  gc_in_pos[1] - self.gc_wg_distance + self.waveguide_spacing * 2),
#                                 (ring_add_pos[0] - self.bend_radius - straight_extension, ring_add_pos[1]),
#                                 ring_add_pos
#                                 ]
#                 print(add_wg_shape)
#                 gc_drop_pos = self.ports['drop'].position
#                 ring_drop_pos = self.child_cells['ring'].get_default_view(i3.LayoutView).ports[
#                     'drop'].position.modified_copy()
#                 ring_drop_pos.transform(self.child_transformations['ring'])
#
#                 #drop_wg_shape = self.waveguides[2].shape.points
#                 #gc_drop_pos = drop_wg_shape[0]
#                 #ring_drop_pos = drop_wg_shape[-1]
#                 drop_wg_shape = [gc_drop_pos,
#                                 (gc_drop_pos[0], gc_in_pos[1] - self.gc_wg_distance + self.waveguide_spacing * 3),
#                                 (ring_drop_pos[0] + self.bend_radius + straight_extension,
#                                  gc_in_pos[1] - self.gc_wg_distance + self.waveguide_spacing * 3),
#                                 (ring_drop_pos[0] + self.bend_radius + straight_extension, ring_drop_pos[1]),
#                                 ring_drop_pos
#                                ]
#                 print(drop_wg_shape)
#                 #return [in_wg_shape, through_wg_shape, add_wg_shape, add_wg_shape]
#                 return [in_wg_shape, through_wg_shape, add_wg_shape, drop_wg_shape]
# else:
class RingModulatorGCHiepAuxOutside_Top(i3.Circuit):
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
        return AddDropRingWithAuxOutside_Top_Euler(ring_trace_template=self.trace_template,
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
            i3.Place('in_grating', position=(self.gc_spacing * 3 + 150, 0), angle=-90),
            i3.Place('through_grating', position=(self.gc_spacing * 4 + 150, 0), angle=-90),
            i3.Place('add_grating', position=(self.gc_spacing * 5 + 150, 0), angle=-90),
            i3.Place('drop_grating', position=(self.gc_spacing * 6 + 150, 0), angle=-90),
            i3.Place('ring', position=self.ring_position, angle=0),
            i3.FlipV('ring'),

            i3.ConnectManhattan(
                "in_grating:out", "ring:in",
                control_points=[i3.H(i3.START - self.gc_wg_distance - self.waveguide_spacing*2)
                                ],
                bend_radius=self.bend_radius,
            ),

            i3.ConnectManhattan(
                "through_grating:out", "ring:through",
                control_points=[i3.H(i3.START - self.gc_wg_distance - self.waveguide_spacing)
                                ],
                bend_radius=self.bend_radius,
            ),

            i3.ConnectManhattan(
                "add_grating:out", "ring:add",
                control_points=[i3.H(i3.START - self.gc_wg_distance)
                                ],
                bend_radius=self.bend_radius,
            ),

            i3.ConnectManhattan(
                "drop_grating:out", "ring:drop",
                control_points=[i3.H(i3.START - self.gc_wg_distance + self.waveguide_spacing)
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
        aux_coupling_gap = i3.NumberProperty(default=0.0,
                                                    doc="the length of the directional coupler straight section")
        ring_radius = i3.PositiveNumberProperty(default=100, doc="ring radius")
        ring_radius_aux = i3.PositiveNumberProperty(default=100, doc="ring radius")
        ring_straight_length = i3.PositiveNumberProperty(default=3000.0, doc="the circumference of the ring")
        ring_straight_length_aux = i3.PositiveNumberProperty(default=3000.0, doc="the circumference of the ring")
        coupler_straight_length = i3.NumberProperty(default=0.0,
                                                    doc="the length of the directional coupler straight section")
        coupler_positions = i3.ListProperty(doc="location of the two couplers")
        coupler_spacing = i3.PositiveNumberProperty(default=1.0,
                                                    doc="spacing between edges of two waveguides")
        coupler_bend_radius = i3.PositiveNumberProperty(default=300.0,
                                                        doc="bending radius of the coupler bus waveguide")
        ring_wg_width = i3.PositiveNumberProperty(default=1.4, doc="the width of the waveguide1")
        bus_wg_width = i3.PositiveNumberProperty(default=1.4, doc="the width of the waveguide2")
        cladding_width = i3.PositiveNumberProperty(default=28.0, doc="the width of cladding")

        electrode_length = i3.PositiveNumberProperty(default=2000.0, doc="the length of the electrode")
        taper_length = i3.PositiveNumberProperty(default=100.0, doc="the length of the taper")
        hot_width = i3.PositiveNumberProperty(default=23.0, doc="width of the hot electrode")
        ground_width = i3.PositiveNumberProperty(default=100.0, doc="width of the ground planes")
        ground_width_mod = i3.PositiveNumberProperty(default=100.0, doc="width of the ground planes")
        electrode_gap = i3.PositiveNumberProperty(default=7.0, doc="gap between hot electrode and ground plane")
        hot_taper_width = i3.PositiveNumberProperty(default=50.0,
                                                    doc="width of the hot electrode at the end of the taper")
        taper_gap = i3.PositiveNumberProperty(default=20.0,
                                              doc="gap between hot electrode and ground plane at the end of the taper")
        taper_straight_length = i3.PositiveNumberProperty(default=10.0,
                                                          doc="length of the straight section at the end of the taper")
        with_label = i3.BoolProperty(default=True, doc="whether to include a label")
        label_position = i3.Coord2Property(doc="position of the label")
        label_angle = i3.NumberProperty(default=0, doc="angle of the label")
        coupler_gap_Hiep = i3.PositiveNumberProperty(default=10.0,
                                                          doc="length of the straight section at the end of the taper")
        electrode_gap_Hiep = i3.PositiveNumberProperty(default=7.0, doc="gap between hot electrode and ground plane")


        def _default_trace_template(self):
            lo = self.cell.trace_template.get_default_view(i3.LayoutView)
            lo.set(core_width=self.ring_wg_width)

        def _default_ring(self):
            ring_lo = self.cell.ring.get_default_view(i3.LayoutView)
            ring_lo.set(aux_coupling_gap = self.aux_coupling_gap,
                        ring_radius=self.ring_radius,
                        ring_radius_aux = self.ring_radius_aux,
                        ring_straight_length=self.ring_straight_length,
                        ring_straight_length_aux=self.ring_straight_length_aux,
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

        def _default_label_position(self):
            return (0, 0)

        def _generate_elements(self, elems):
            """
            add labels at in/out put grating couplers regions
            """

            if self.with_label:
                elems += i3.PolygonText(layer=i3.TECH.PPLAYER.RWG.TEXT,
                                        coordinate=self.label_position,
                                        text="AUX_RING_V4_CORE_1.40_CG-" + str(self.coupler_gap_Hiep * 1000) + "nm" + "_" + "EG-" + str(self.electrode_gap_Hiep * 1000)+ "nm" + "_" +"AUX-CG-"+str(self.aux_coupling_gap*1000)+ "nm",
                                        height= 50,
                                        alignment=(i3.TEXT.ALIGN.CENTER, i3.TEXT.ALIGN.BOTTOM),
                                        transformation=i3.Rotation(rotation=self.label_angle))

            return elems

        def _default_coupler_positions(self):
            return [-self.ring_straight_length * 0.125 + self.coupler_straight_length,
                    self.ring_straight_length * 0.125 - self.coupler_straight_length]

class RingModulatorGCHiepAuxOutside_Top_2(i3.Circuit):
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
        return AddDropRingWithAuxOutside_Top_Euler_2(ring_trace_template=self.trace_template,
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
            i3.Place('in_grating', position=(self.gc_spacing * 3 + 150, 0), angle=-90),
            i3.Place('through_grating', position=(self.gc_spacing * 4 + 150, 0), angle=-90),
            i3.Place('add_grating', position=(self.gc_spacing * 5 + 150, 0), angle=-90),
            i3.Place('drop_grating', position=(self.gc_spacing * 6 + 150, 0), angle=-90),
            i3.Place('ring', position=self.ring_position, angle=0),
            i3.FlipV('ring'),

            i3.ConnectManhattan(
                "in_grating:out", "ring:in",
                control_points=[i3.H(i3.START - self.gc_wg_distance - self.waveguide_spacing*2)
                                ],
                bend_radius=self.bend_radius,
            ),

            i3.ConnectManhattan(
                "through_grating:out", "ring:through",
                control_points=[i3.H(i3.START - self.gc_wg_distance - self.waveguide_spacing)
                                ],
                bend_radius=self.bend_radius,
            ),

            i3.ConnectManhattan(
                "add_grating:out", "ring:add",
                control_points=[i3.H(i3.START - self.gc_wg_distance)
                                ],
                bend_radius=self.bend_radius,
            ),

            i3.ConnectManhattan(
                "drop_grating:out", "ring:drop",
                control_points=[i3.H(i3.START - self.gc_wg_distance + self.waveguide_spacing)
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
        aux_coupling_gap = i3.NumberProperty(default=0.0,
                                                    doc="the length of the directional coupler straight section")
        ring_radius = i3.PositiveNumberProperty(default=100, doc="ring radius")
        ring_radius_aux = i3.PositiveNumberProperty(default=100, doc="ring radius")
        ring_straight_length = i3.PositiveNumberProperty(default=3000.0, doc="the circumference of the ring")
        ring_straight_length_aux = i3.PositiveNumberProperty(default=3000.0, doc="the circumference of the ring")
        coupler_straight_length = i3.NumberProperty(default=0.0,
                                                    doc="the length of the directional coupler straight section")
        coupler_positions = i3.ListProperty(doc="location of the two couplers")
        coupler_spacing = i3.PositiveNumberProperty(default=1.0,
                                                    doc="spacing between edges of two waveguides")
        coupler_bend_radius = i3.PositiveNumberProperty(default=300.0,
                                                        doc="bending radius of the coupler bus waveguide")
        ring_wg_width = i3.PositiveNumberProperty(default=1.4, doc="the width of the waveguide1")
        bus_wg_width = i3.PositiveNumberProperty(default=1.4, doc="the width of the waveguide2")
        cladding_width = i3.PositiveNumberProperty(default=28.0, doc="the width of cladding")

        electrode_length = i3.PositiveNumberProperty(default=2000.0, doc="the length of the electrode")
        taper_length = i3.PositiveNumberProperty(default=100.0, doc="the length of the taper")
        hot_width = i3.PositiveNumberProperty(default=23.0, doc="width of the hot electrode")
        ground_width = i3.PositiveNumberProperty(default=100.0, doc="width of the ground planes")
        ground_width_mod = i3.PositiveNumberProperty(default=100.0, doc="width of the ground planes")
        electrode_gap = i3.PositiveNumberProperty(default=7.0, doc="gap between hot electrode and ground plane")
        hot_taper_width = i3.PositiveNumberProperty(default=50.0,
                                                    doc="width of the hot electrode at the end of the taper")
        taper_gap = i3.PositiveNumberProperty(default=20.0,
                                              doc="gap between hot electrode and ground plane at the end of the taper")
        taper_straight_length = i3.PositiveNumberProperty(default=10.0,
                                                          doc="length of the straight section at the end of the taper")
        with_label = i3.BoolProperty(default=True, doc="whether to include a label")
        label_position = i3.Coord2Property(doc="position of the label")
        label_angle = i3.NumberProperty(default=0, doc="angle of the label")
        coupler_gap_Hiep = i3.PositiveNumberProperty(default=10.0,
                                                          doc="length of the straight section at the end of the taper")
        electrode_gap_Hiep = i3.PositiveNumberProperty(default=7.0, doc="gap between hot electrode and ground plane")


        def _default_trace_template(self):
            lo = self.cell.trace_template.get_default_view(i3.LayoutView)
            lo.set(core_width=self.ring_wg_width)

        def _default_ring(self):
            ring_lo = self.cell.ring.get_default_view(i3.LayoutView)
            ring_lo.set(aux_coupling_gap = self.aux_coupling_gap,
                        ring_radius=self.ring_radius,
                        ring_radius_aux = self.ring_radius_aux,
                        ring_straight_length=self.ring_straight_length,
                        ring_straight_length_aux=self.ring_straight_length_aux,
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

        def _default_label_position(self):
            return (0, 0)

        def _generate_elements(self, elems):
            """
            add labels at in/out put grating couplers regions
            """

            if self.with_label:
                elems += i3.PolygonText(layer=i3.TECH.PPLAYER.RWG.TEXT,
                                        coordinate=self.label_position,
                                        text="AUX_RING_V4_CORE_1.40_CG-" + str(self.coupler_gap_Hiep * 1000) + "nm" + "_" + "EG-" + str(self.electrode_gap_Hiep * 1000)+ "nm" + "_" +"AUX-CG-"+str(self.aux_coupling_gap*1000)+ "nm",
                                        height= 50,
                                        alignment=(i3.TEXT.ALIGN.CENTER, i3.TEXT.ALIGN.BOTTOM),
                                        transformation=i3.Rotation(rotation=self.label_angle))

            return elems

        def _default_coupler_positions(self):
            return [-self.ring_straight_length * 0.125 + self.coupler_straight_length,
                    self.ring_straight_length * 0.125 - self.coupler_straight_length]
