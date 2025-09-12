import ipkiss3.all as i3

import asp_sin_lnoi_photonics.all as asp


class Coupler_Test04(i3.Circuit):
    gc = i3.ChildCellProperty(doc="the grating coupler")
    trace_template = i3.TraceTemplateProperty(doc="the trace template for the circuit")
    spacing = i3.PositiveNumberProperty(default=127 * 16, doc="spacing between two grating couplers")
    bend_radius = i3.PositiveNumberProperty(default=200, doc="bending radius in routing")

    def _default_gc(self):
        return asp.GratingCouplerTE1550RibZ()

    def _default_trace_template(self):
        return asp.SiNRibWaveguideTemplate()

    def _default_insts(self):
        return {"in_grating": self.gc.Layout(fill_factor=0.4),
                "out_grating": self.gc.Layout(fill_factor=0.4),
                }

    def _default_specs(self):
        # distance between the gc output port and the centre of the gc
        # gc_out_port_pos = self.gc.get_default_view(i3.LayoutView).ports['out'].postion

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

class Coupler_Test04_2(i3.Circuit):
    gc = i3.ChildCellProperty(doc="the grating coupler")
    trace_template = i3.TraceTemplateProperty(doc="the trace template for the circuit")
    spacing = i3.PositiveNumberProperty(default=127 * 16, doc="spacing between two grating couplers")
    bend_radius = i3.PositiveNumberProperty(default=200, doc="bending radius in routing")

    def _default_gc(self):
        return asp.GratingCouplerTE1550RibZ()

    def _default_trace_template(self):
        return asp.SiNRibWaveguideTemplate()

    def _default_insts(self):
        return {"in_grating": self.gc.Layout(fill_factor=0.4),
                "out_grating": self.gc.Layout(fill_factor=0.4),
                }

    def _default_specs(self):
        # distance between the gc output port and the centre of the gc
        # gc_out_port_pos = self.gc.get_default_view(i3.LayoutView).ports['out'].postion

        start_straight = 10.0
        end_straight = 10.0

        return [i3.Place('in_grating', position=(0, 0), angle=-90),
                i3.Place('out_grating', position=(self.spacing, 0), angle=-90),
                i3.ConnectManhattan(
                    'in_grating:out', 'out_grating:out',
                    control_points=[i3.H(i3.START - self.bend_radius - start_straight),
                                    i3.V(i3.START + self.bend_radius* 2),
                                    i3.H(i3.START - self.bend_radius - start_straight),
                                    i3.V(i3.END - self.bend_radius* 2),
                                    i3.H(i3.END - self.bend_radius - start_straight)
                                    ],
                    bend_radius=self.bend_radius,
                    start_straight=start_straight,
                    end_straight=end_straight,
                    min_straight=0
                )
                ]

class Coupler_Test04_3(i3.Circuit):
    gc = i3.ChildCellProperty(doc="the grating coupler")
    trace_template = i3.TraceTemplateProperty(doc="the trace template for the circuit")
    spacing = i3.PositiveNumberProperty(default=127 * 16, doc="spacing between two grating couplers")
    bend_radius = i3.PositiveNumberProperty(default=200, doc="bending radius in routing")

    def _default_gc(self):
        return asp.GratingCouplerTE1550RibZ()

    def _default_trace_template(self):
        return asp.SiNRibWaveguideTemplate()

    def _default_insts(self):
        return {"in_grating": self.gc.Layout(fill_factor=0.4),
                    "out_grating": self.gc.Layout(fill_factor=0.4),
                    }

    def _default_specs(self):
            # distance between the gc output port and the centre of the gc
            # gc_out_port_pos = self.gc.get_default_view(i3.LayoutView).ports['out'].postion

        start_straight = 10.0
        end_straight = 10.0

        return [i3.Place('in_grating', position=(0, 0), angle=-90),
                i3.Place('out_grating', position=(self.spacing, 0), angle=-90),
                i3.ConnectManhattan(
                    'in_grating:out', 'out_grating:out',
                    control_points=[i3.H(i3.START - self.bend_radius - start_straight-150),
                                        i3.V(i3.START + self.bend_radius * 2),
                                        i3.H(i3.START - self.bend_radius - start_straight-150),
                                        i3.V(i3.END - self.bend_radius * 2),
                                        i3.H(i3.END - self.bend_radius - start_straight-150)
                                        ],
                    bend_radius=self.bend_radius,
                    start_straight=start_straight,
                    end_straight=end_straight,
                    min_straight=0
                )
                ]

class Coupler_Test05(i3.Circuit):
    gc = i3.ChildCellProperty(doc="the grating coupler")
    trace_template = i3.TraceTemplateProperty(doc="the trace template for the circuit")
    spacing = i3.PositiveNumberProperty(default=127 * 16, doc="spacing between two grating couplers")
    bend_radius = i3.PositiveNumberProperty(default=200, doc="bending radius in routing")

    def _default_gc(self):
        return asp.GratingCouplerTE1550RibZ()

    def _default_trace_template(self):
        return asp.SiNRibWaveguideTemplate()

    def _default_insts(self):
        return {"in_grating": self.gc.Layout(fill_factor=0.5),
                "out_grating": self.gc.Layout(fill_factor=0.5),
                }

    def _default_specs(self):
        # distance between the gc output port and the centre of the gc
        # gc_out_port_pos = self.gc.get_default_view(i3.LayoutView).ports['out'].postion

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


class Coupler_Test05_2(i3.Circuit):
    gc = i3.ChildCellProperty(doc="the grating coupler")
    trace_template = i3.TraceTemplateProperty(doc="the trace template for the circuit")
    spacing = i3.PositiveNumberProperty(default=127 * 16, doc="spacing between two grating couplers")
    bend_radius = i3.PositiveNumberProperty(default=200, doc="bending radius in routing")

    def _default_gc(self):
        return asp.GratingCouplerTE1550RibZ()

    def _default_trace_template(self):
        return asp.SiNRibWaveguideTemplate()

    def _default_insts(self):
        return {"in_grating": self.gc.Layout(fill_factor=0.5),
                "out_grating": self.gc.Layout(fill_factor=0.5),
                }

    def _default_specs(self):
        # distance between the gc output port and the centre of the gc
        # gc_out_port_pos = self.gc.get_default_view(i3.LayoutView).ports['out'].postion

        start_straight = 10.0
        end_straight = 10.0

        return [i3.Place('in_grating', position=(0, 0), angle=-90),
                i3.Place('out_grating', position=(self.spacing, 0), angle=-90),
                i3.ConnectManhattan(
                    'in_grating:out', 'out_grating:out',
                    control_points=[i3.H(i3.START - self.bend_radius - start_straight),
                                    i3.V(i3.START + self.bend_radius* 2),
                                    i3.H(i3.START - self.bend_radius - start_straight),
                                    i3.V(i3.END - self.bend_radius* 2),
                                    i3.H(i3.END - self.bend_radius - start_straight)
                                    ],
                    bend_radius=self.bend_radius,
                    start_straight=start_straight,
                    end_straight=end_straight,
                    min_straight=0
                )
                ]


class Coupler_Test05_3(i3.Circuit):
    gc = i3.ChildCellProperty(doc="the grating coupler")
    trace_template = i3.TraceTemplateProperty(doc="the trace template for the circuit")
    spacing = i3.PositiveNumberProperty(default=127 * 16, doc="spacing between two grating couplers")
    bend_radius = i3.PositiveNumberProperty(default=200, doc="bending radius in routing")

    def _default_gc(self):
        return asp.GratingCouplerTE1550RibZ()

    def _default_trace_template(self):
        return asp.SiNRibWaveguideTemplate()

    def _default_insts(self):
        return {"in_grating": self.gc.Layout(fill_factor=0.5),
                    "out_grating": self.gc.Layout(fill_factor=0.5),
                    }

    def _default_specs(self):
            # distance between the gc output port and the centre of the gc
            # gc_out_port_pos = self.gc.get_default_view(i3.LayoutView).ports['out'].postion

        start_straight = 10.0
        end_straight = 10.0

        return [i3.Place('in_grating', position=(0, 0), angle=-90),
                i3.Place('out_grating', position=(self.spacing, 0), angle=-90),
                i3.ConnectManhattan(
                    'in_grating:out', 'out_grating:out',
                    control_points=[i3.H(i3.START - self.bend_radius - start_straight-150),
                                        i3.V(i3.START + self.bend_radius * 2),
                                        i3.H(i3.START - self.bend_radius - start_straight-150),
                                        i3.V(i3.END - self.bend_radius * 2),
                                        i3.H(i3.END - self.bend_radius - start_straight-150)
                                        ],
                    bend_radius=self.bend_radius,
                    start_straight=start_straight,
                    end_straight=end_straight,
                    min_straight=0
                )
                ]


class Coupler_Test06(i3.Circuit):
    gc = i3.ChildCellProperty(doc="the grating coupler")
    trace_template = i3.TraceTemplateProperty(doc="the trace template for the circuit")
    spacing = i3.PositiveNumberProperty(default=127 * 16, doc="spacing between two grating couplers")
    bend_radius = i3.PositiveNumberProperty(default=200, doc="bending radius in routing")

    def _default_gc(self):
        return asp.GratingCouplerTE1550RibZ()

    def _default_trace_template(self):
        return asp.SiNRibWaveguideTemplate()

    def _default_insts(self):
        return {"in_grating": self.gc.Layout(fill_factor=0.6),
                "out_grating": self.gc.Layout(fill_factor=0.6),
                }

    def _default_specs(self):
        # distance between the gc output port and the centre of the gc
        # gc_out_port_pos = self.gc.get_default_view(i3.LayoutView).ports['out'].postion

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

class Coupler_Test06_2(i3.Circuit):
    gc = i3.ChildCellProperty(doc="the grating coupler")
    trace_template = i3.TraceTemplateProperty(doc="the trace template for the circuit")
    spacing = i3.PositiveNumberProperty(default=127 * 16, doc="spacing between two grating couplers")
    bend_radius = i3.PositiveNumberProperty(default=200, doc="bending radius in routing")

    def _default_gc(self):
        return asp.GratingCouplerTE1550RibZ()

    def _default_trace_template(self):
        return asp.SiNRibWaveguideTemplate()

    def _default_insts(self):
        return {"in_grating": self.gc.Layout(fill_factor=0.6),
                "out_grating": self.gc.Layout(fill_factor=0.6),
                }

    def _default_specs(self):
        # distance between the gc output port and the centre of the gc
        # gc_out_port_pos = self.gc.get_default_view(i3.LayoutView).ports['out'].postion

        start_straight = 10.0
        end_straight = 10.0

        return [i3.Place('in_grating', position=(0, 0), angle=-90),
                i3.Place('out_grating', position=(self.spacing, 0), angle=-90),
                i3.ConnectManhattan(
                    'in_grating:out', 'out_grating:out',
                    control_points=[i3.H(i3.START - self.bend_radius - start_straight),
                                    i3.V(i3.START + self.bend_radius* 2),
                                    i3.H(i3.START - self.bend_radius - start_straight),
                                    i3.V(i3.END - self.bend_radius* 2),
                                    i3.H(i3.END - self.bend_radius - start_straight)
                                    ],
                    bend_radius=self.bend_radius,
                    start_straight=start_straight,
                    end_straight=end_straight,
                    min_straight=0
                )
                ]

class Coupler_Test06_3(i3.Circuit):
    gc = i3.ChildCellProperty(doc="the grating coupler")
    trace_template = i3.TraceTemplateProperty(doc="the trace template for the circuit")
    spacing = i3.PositiveNumberProperty(default=127 * 16, doc="spacing between two grating couplers")
    bend_radius = i3.PositiveNumberProperty(default=200, doc="bending radius in routing")

    def _default_gc(self):
        return asp.GratingCouplerTE1550RibZ()

    def _default_trace_template(self):
        return asp.SiNRibWaveguideTemplate()

    def _default_insts(self):
        return {"in_grating": self.gc.Layout(fill_factor=0.6),
                    "out_grating": self.gc.Layout(fill_factor=0.6),
                    }

    def _default_specs(self):
            # distance between the gc output port and the centre of the gc
            # gc_out_port_pos = self.gc.get_default_view(i3.LayoutView).ports['out'].postion

        start_straight = 10.0
        end_straight = 10.0

        return [i3.Place('in_grating', position=(0, 0), angle=-90),
                i3.Place('out_grating', position=(self.spacing, 0), angle=-90),
                i3.ConnectManhattan(
                    'in_grating:out', 'out_grating:out',
                    control_points=[i3.H(i3.START - self.bend_radius - start_straight-150),
                                        i3.V(i3.START + self.bend_radius * 2),
                                        i3.H(i3.START - self.bend_radius - start_straight-150),
                                        i3.V(i3.END - self.bend_radius * 2),
                                        i3.H(i3.END - self.bend_radius - start_straight-150)
                                        ],
                    bend_radius=self.bend_radius,
                    start_straight=start_straight,
                    end_straight=end_straight,
                    min_straight=0
                )
                ]

class Coupler_Test07(i3.Circuit):
    gc = i3.ChildCellProperty(doc="the grating coupler")
    trace_template = i3.TraceTemplateProperty(doc="the trace template for the circuit")
    spacing = i3.PositiveNumberProperty(default=127 * 16, doc="spacing between two grating couplers")
    bend_radius = i3.PositiveNumberProperty(default=200, doc="bending radius in routing")

    def _default_gc(self):
        return asp.GratingCouplerTE1550RibZ()

    def _default_trace_template(self):
        return asp.SiNRibWaveguideTemplate()

    def _default_insts(self):
        return {"in_grating": self.gc.Layout(fill_factor=0.7),
                "out_grating": self.gc.Layout(fill_factor=0.7),
                }

    def _default_specs(self):
        # distance between the gc output port and the centre of the gc
        # gc_out_port_pos = self.gc.get_default_view(i3.LayoutView).ports['out'].postion

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

class Coupler_Test07_3(i3.Circuit):
    gc = i3.ChildCellProperty(doc="the grating coupler")
    trace_template = i3.TraceTemplateProperty(doc="the trace template for the circuit")
    spacing = i3.PositiveNumberProperty(default=127 * 16, doc="spacing between two grating couplers")
    bend_radius = i3.PositiveNumberProperty(default=200, doc="bending radius in routing")

    def _default_gc(self):
        return asp.GratingCouplerTE1550RibZ()

    def _default_trace_template(self):
        return asp.SiNRibWaveguideTemplate()

    def _default_insts(self):
        return {"in_grating": self.gc.Layout(fill_factor=0.7),
                    "out_grating": self.gc.Layout(fill_factor=0.7),
                    }

    def _default_specs(self):
            # distance between the gc output port and the centre of the gc
            # gc_out_port_pos = self.gc.get_default_view(i3.LayoutView).ports['out'].postion

        start_straight = 10.0
        end_straight = 10.0

        return [i3.Place('in_grating', position=(0, 0), angle=-90),
                i3.Place('out_grating', position=(self.spacing, 0), angle=-90),
                i3.ConnectManhattan(
                    'in_grating:out', 'out_grating:out',
                    control_points=[i3.H(i3.START - self.bend_radius - start_straight-150),
                                        i3.V(i3.START + self.bend_radius * 2),
                                        i3.H(i3.START - self.bend_radius - start_straight-150),
                                        i3.V(i3.END - self.bend_radius * 2),
                                        i3.H(i3.END - self.bend_radius - start_straight-150)
                                        ],
                    bend_radius=self.bend_radius,
                    start_straight=start_straight,
                    end_straight=end_straight,
                    min_straight=0
                )
                ]

class Coupler_Test07_2(i3.Circuit):
    gc = i3.ChildCellProperty(doc="the grating coupler")
    trace_template = i3.TraceTemplateProperty(doc="the trace template for the circuit")
    spacing = i3.PositiveNumberProperty(default=127 * 16, doc="spacing between two grating couplers")
    bend_radius = i3.PositiveNumberProperty(default=200, doc="bending radius in routing")

    def _default_gc(self):
        return asp.GratingCouplerTE1550RibZ()

    def _default_trace_template(self):
        return asp.SiNRibWaveguideTemplate()

    def _default_insts(self):
        return {"in_grating": self.gc.Layout(fill_factor=0.7),
                "out_grating": self.gc.Layout(fill_factor=0.7),
                }

    def _default_specs(self):
        # distance between the gc output port and the centre of the gc
        # gc_out_port_pos = self.gc.get_default_view(i3.LayoutView).ports['out'].postion

        start_straight = 10.0
        end_straight = 10.0

        return [i3.Place('in_grating', position=(0, 0), angle=-90),
                i3.Place('out_grating', position=(self.spacing, 0), angle=-90),
                i3.ConnectManhattan(
                    'in_grating:out', 'out_grating:out',
                    control_points=[i3.H(i3.START - self.bend_radius - start_straight),
                                    i3.V(i3.START + self.bend_radius* 2),
                                    i3.H(i3.START - self.bend_radius - start_straight),
                                    i3.V(i3.END - self.bend_radius* 2),
                                    i3.H(i3.END - self.bend_radius - start_straight)
                                    ],
                    bend_radius=self.bend_radius,
                    start_straight=start_straight,
                    end_straight=end_straight,
                    min_straight=0
                )
                ]

class Coupler_Test08(i3.Circuit):
    gc = i3.ChildCellProperty(doc="the grating coupler")
    trace_template = i3.TraceTemplateProperty(doc="the trace template for the circuit")
    spacing = i3.PositiveNumberProperty(default=127 * 16, doc="spacing between two grating couplers")
    bend_radius = i3.PositiveNumberProperty(default=200, doc="bending radius in routing")

    def _default_gc(self):
        return asp.GratingCouplerTE1550RibZ()

    def _default_trace_template(self):
        return asp.SiNRibWaveguideTemplate()

    def _default_insts(self):
        return {"in_grating": self.gc.Layout(fill_factor=0.8),
                "out_grating": self.gc.Layout(fill_factor=0.8),
                }

    def _default_specs(self):
        # distance between the gc output port and the centre of the gc
        # gc_out_port_pos = self.gc.get_default_view(i3.LayoutView).ports['out'].postion

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


class Coupler_Test08_2(i3.Circuit):
    gc = i3.ChildCellProperty(doc="the grating coupler")
    trace_template = i3.TraceTemplateProperty(doc="the trace template for the circuit")
    spacing = i3.PositiveNumberProperty(default=127 * 16, doc="spacing between two grating couplers")
    bend_radius = i3.PositiveNumberProperty(default=200, doc="bending radius in routing")

    def _default_gc(self):
        return asp.GratingCouplerTE1550RibZ()

    def _default_trace_template(self):
        return asp.SiNRibWaveguideTemplate()

    def _default_insts(self):
        return {"in_grating": self.gc.Layout(fill_factor=0.8),
                "out_grating": self.gc.Layout(fill_factor=0.8),
                }

    def _default_specs(self):
        # distance between the gc output port and the centre of the gc
        # gc_out_port_pos = self.gc.get_default_view(i3.LayoutView).ports['out'].postion

        start_straight = 10.0
        end_straight = 10.0

        return [i3.Place('in_grating', position=(0, 0), angle=-90),
                i3.Place('out_grating', position=(self.spacing, 0), angle=-90),
                i3.ConnectManhattan(
                    'in_grating:out', 'out_grating:out',
                    control_points=[i3.H(i3.START - self.bend_radius - start_straight),
                                    i3.V(i3.START + self.bend_radius* 2),
                                    i3.H(i3.START - self.bend_radius - start_straight),
                                    i3.V(i3.END - self.bend_radius* 2),
                                    i3.H(i3.END - self.bend_radius - start_straight)
                                    ],
                    bend_radius=self.bend_radius,
                    start_straight=start_straight,
                    end_straight=end_straight,
                    min_straight=0
                )
                ]

class Coupler_Test08_3(i3.Circuit):
    gc = i3.ChildCellProperty(doc="the grating coupler")
    trace_template = i3.TraceTemplateProperty(doc="the trace template for the circuit")
    spacing = i3.PositiveNumberProperty(default=127 * 16, doc="spacing between two grating couplers")
    bend_radius = i3.PositiveNumberProperty(default=200, doc="bending radius in routing")

    def _default_gc(self):
        return asp.GratingCouplerTE1550RibZ()

    def _default_trace_template(self):
        return asp.SiNRibWaveguideTemplate()

    def _default_insts(self):
        return {"in_grating": self.gc.Layout(fill_factor=0.8),
                    "out_grating": self.gc.Layout(fill_factor=0.8),
                    }

    def _default_specs(self):
            # distance between the gc output port and the centre of the gc
            # gc_out_port_pos = self.gc.get_default_view(i3.LayoutView).ports['out'].postion

        start_straight = 10.0
        end_straight = 10.0

        return [i3.Place('in_grating', position=(0, 0), angle=-90),
                i3.Place('out_grating', position=(self.spacing, 0), angle=-90),
                i3.ConnectManhattan(
                    'in_grating:out', 'out_grating:out',
                    control_points=[i3.H(i3.START - self.bend_radius - start_straight-150),
                                        i3.V(i3.START + self.bend_radius * 2),
                                        i3.H(i3.START - self.bend_radius - start_straight-150),
                                        i3.V(i3.END - self.bend_radius * 2),
                                        i3.H(i3.END - self.bend_radius - start_straight-150)
                                        ],
                    bend_radius=self.bend_radius,
                    start_straight=start_straight,
                    end_straight=end_straight,
                    min_straight=0
                )
                ]

class Coupler_Test09(i3.Circuit):
    gc = i3.ChildCellProperty(doc="the grating coupler")
    trace_template = i3.TraceTemplateProperty(doc="the trace template for the circuit")
    spacing = i3.PositiveNumberProperty(default=127 * 16, doc="spacing between two grating couplers")
    bend_radius = i3.PositiveNumberProperty(default=200, doc="bending radius in routing")

    def _default_gc(self):
        return asp.GratingCouplerTE1550RibZ()

    def _default_trace_template(self):
        return asp.SiNRibWaveguideTemplate()

    def _default_insts(self):
        return {"in_grating": self.gc.Layout(fill_factor=0.9),
                "out_grating": self.gc.Layout(fill_factor=0.9),
                }

    def _default_specs(self):
        # distance between the gc output port and the centre of the gc
        # gc_out_port_pos = self.gc.get_default_view(i3.LayoutView).ports['out'].postion

        start_straight = 10.0
        end_straight = 10.0

        return [i3.Place('in_grating', position=(0, 0), angle=0),
                i3.Place('out_grating', position=(self.spacing, 0), angle=180),
                i3.ConnectManhattan(
                    'in_grating:out', 'out_grating:out',
                    start_straight=start_straight,
                    end_straight=end_straight,
                    min_straight=0
                )
                ]


class Coupler_Test10(i3.Circuit):
    gc = i3.ChildCellProperty(doc="the grating coupler")
    trace_template = i3.TraceTemplateProperty(doc="the trace template for the circuit")
    spacing = i3.PositiveNumberProperty(default=127 * 16, doc="spacing between two grating couplers")
    bend_radius = i3.PositiveNumberProperty(default=200, doc="bending radius in routing")

    def _default_gc(self):
        return asp.GratingCouplerTE1550RibZ()

    def _default_trace_template(self):
        return asp.SiNRibWaveguideTemplate()

    def _default_insts(self):
        return {"in_grating": self.gc.Layout(fill_factor=1.0),
                "out_grating": self.gc.Layout(fill_factor=1.0),
                }

    def _default_specs(self):
        # distance between the gc output port and the centre of the gc
        # gc_out_port_pos = self.gc.get_default_view(i3.LayoutView).ports['out'].postion

        start_straight = 10.0
        end_straight = 10.0

        return [i3.Place('in_grating', position=(0, 0), angle=0),
                i3.Place('out_grating', position=(self.spacing, 0), angle=180),
                i3.ConnectManhattan(
                    'in_grating:out', 'out_grating:out',
                    start_straight=start_straight,
                    end_straight=end_straight,
                    min_straight=0
                )
                ]

    class WaveguideLoop(i3.Circuit):
        gc = i3.ChildCellProperty(doc="the grating coupler")
        trace_template = i3.TraceTemplateProperty(doc="the trace template for the circuit")
        spacing = i3.PositiveNumberProperty(default=127 * 16, doc="spacing between two grating couplers")
        bend_radius = i3.PositiveNumberProperty(default=200, doc="bending radius in routing")

        def _default_gc(self):
            return asp.GRATING_COUPLER_TE1550_RIBZ()

        def _default_trace_template(self):
            return asp.SiNRibWaveguideTemplate()

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