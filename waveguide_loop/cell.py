import ipkiss3.all as i3

import asp_sin_lnoi_photonics.all as asp

import ipkiss

ipkiss_version = ipkiss.__version__.split('.')

if int(ipkiss_version[0]) <= 3 and int(ipkiss_version[1]) < 7:
    from picazzo3.routing.place_route import PlaceAndAutoRoute

    class WaveguideLoop(PlaceAndAutoRoute):
        gc = i3.ChildCellProperty(doc="the grating coupler")
        trace_template = i3.TraceTemplateProperty(doc="the trace template for the circuit")

        def _default_gc(self):
            return asp.GRATING_COUPLER_TE1550_RIBZ()

        def _default_trace_template(self):
            return asp.SiNRibWaveguideTemplate()

        def _default_child_cells(self):
            return {"in_grating": self.gc,
                    "out_grating": self.gc
                    }

        def _default_links(self):
            return [("in_grating:out", "out_grating:out")
                    ]

        def _default_external_port_names(self):
            return {"in_grating:vertical_in": "in",
                    "out_grating:vertical_in": "out"
                    }

        class Layout(PlaceAndAutoRoute.Layout):
            spacing = i3.PositiveNumberProperty(default=127*16, doc="spacing between two grating couplers")
            def _default_bend_radius(self):
                return 200

            def _default_child_transformations(self):
                child_transformations = {"in_grating": i3.Rotation(rotation=-90) + i3.Translation((0, 0)),
                                         "out_grating": i3.Rotation(rotation=-90) + i3.Translation((self.spacing, 0))
                                         }

                return child_transformations

            def _default_waveguide_shapes(self):
                gc_in_pos = self.child_cells['in_grating'].get_default_view(i3.LayoutView).ports['out'].position.modified_copy()
                gc_in_pos.transform(self.child_transformations['in_grating'])
                gc_out_pos = self.child_cells['out_grating'].get_default_view(i3.LayoutView).ports['out'].position.modified_copy()
                gc_out_pos.transform(self.child_transformations['out_grating'])
                straight_extension = (self.end_straight + self.start_straight)

                return [[gc_in_pos,
                         (gc_in_pos[0], gc_in_pos[1] - self.bend_radius - straight_extension),
                         (gc_in_pos[0] - self.bend_radius * 2 - straight_extension * 2, gc_in_pos[1] - self.bend_radius - straight_extension),
                         (gc_in_pos[0] - self.bend_radius * 2 - straight_extension * 2, gc_in_pos[1] + self.bend_radius + straight_extension * 2),
                         (gc_out_pos[0] + self.bend_radius * 2 + straight_extension * 2, gc_in_pos[1] + self.bend_radius + straight_extension * 2),
                         (gc_out_pos[0] + self.bend_radius * 2 + straight_extension * 2,
                          gc_out_pos[1] - self.bend_radius - straight_extension),
                         (gc_out_pos[0],
                          gc_out_pos[1] - self.bend_radius - straight_extension),
                         gc_out_pos
                         ]]

else:

    # For IPKISS version >= 3.7.0
    print("Using IPKISS 3.7 version")
    class WaveguideLoop(i3.Circuit):
        gc = i3.ChildCellProperty(doc="the grating coupler")
        trace_template = i3.TraceTemplateProperty(doc="the trace template for the circuit")
        spacing = i3.PositiveNumberProperty(default=127 * 16, doc="spacing between two grating couplers")
        bend_radius = i3.PositiveNumberProperty(default=200, doc="bending radius in routing")

        def _default_trace_template(self):
            return asp.SiNRibWaveguideTemplate()

        def _default_gc(self):
            return asp.GratingCouplerTE1550RibZ(start_trace_template=self.trace_template)

        def _default_insts(self):
            return {"in_grating": self.gc,
                    "out_grating": self.gc
                    }

        def _default_specs(self):
            # distance between the gc output port and the centre of the gc
            #gc_out_port_pos = self.gc.get_default_view(i3.LayoutView).ports['out'].postion

            start_straight = 10.0
            end_straight = 10.0

            return [i3.Place('in_grating', position=(0, 0), angle=-90),
                    i3.Place('out_grating', position=(self.spacing, 0), angle=-90),
                    i3.ConnectManhattan(
                        'in_grating:out', 'out_grating:out',
                        control_points=[i3.H(i3.START - self.bend_radius - start_straight),
                                        i3.V(i3.START - self.bend_radius * 2),
                                        i3.H(i3.START - start_straight + self.bend_radius),
                                        i3.V(i3.END + self.bend_radius * 2),
                                        i3.H(i3.END - self.bend_radius - start_straight)
                                        ],
                        bend_radius=self.bend_radius,
                        start_straight=start_straight,
                        end_straight=end_straight,
                        min_straight=0
                    )
            ]

        def _default_exposed_ports(self):
            return {"in_grating:vertical_in": "in",
                    "out_grating:vertical_in": "out"
                    }

        class Layout(i3.Circuit.Layout):
            core_wg_width = i3.PositiveNumberProperty(default=1.4, doc="the width of the waveguide2")

            def _default_trace_template(self):
                trace_lo = self.cell.trace_template.get_default_view(i3.LayoutView)
                trace_lo.set(core_width=self.core_wg_width)
                return trace_lo

            def _default_gc(self):
                gc_lo = self.cell.gc.get_default_view(i3.LayoutView)
                return gc_lo
