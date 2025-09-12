"""

Author: Thach Nguyen

"""

import sys
sys.path.append("C:/Users/e54491/OneDrive - RMIT University/Research/Software/asp_sin_lnoi_photonics/ipkiss")
sys.path.append("../components")

import asp_sin_lnoi_photonics.all as asp
import ipkiss3.all as i3

class SBendAlgorithm(i3.ShapeRoundAdiabaticSpline):

    def _default_radius(self):
        return 300.0

    def _default_adiabatic_angles(self):
        return (0.0, 0.0)

class _RaceTrack(i3.Circuit):
    bend_radius=i3.PositiveNumberProperty(default=150, doc="FSR in nm")
    straight_length = i3.PositiveNumberProperty(default=300.0, doc="the straight section of the ring")
    trace_template=i3.TraceTemplateProperty(default=asp.RWG1000(), doc="the trace template for the waveguide")
    bend = i3.ChildCellProperty(locked=True, doc="U-turn bend")
    bus = i3.ChildCellProperty(locked=True, doc="bus waveguide")
    coupler_straight_length = i3.NumberProperty(default=0.0, doc="the length of the directional coupler straight section")
    coupler_spacing = i3.PositiveNumberProperty(default=2.0,
                                                    doc="centre to centre waveguide spacing")
    coupler_bend_angle = i3.PositiveNumberProperty(default=40.0,
                                               doc="angular span (in degrees) of the bend waveguide")
    coupler_bend_radius = i3.PositiveNumberProperty(default=300.0,
                                               doc="bending radius of the coupler bus waveguide")

    def _default_bus(self):
        bus = asp.RoundedRibWaveguide(trace_template=self.trace_template)

        # set the layout parameters of the waveguide
        r = 0
        a = 0.5 * self.coupler_bend_angle
        s = i3.TECH.RWG.SHORT_STRAIGHT
        l = self.coupler_straight_length / 2.0

            # Bus waveguide layout
        bend_lv = bus.Layout(bend_radius=self.coupler_bend_radius,
                             rounding_algorithm=SBendAlgorithm,
                             angle_step=0.2)

        b1, b2 = bend_lv.get_bend_size(a)  # calculates the size of the waveguide bend
        # control shape for the bus waveguide (one half)
            # the RoundedWaveguide will automatically generate smooth bends
        s1 = i3.Shape([(0.0, -r), (-l - b1, -r)])
        s1.add_polar(2 * b2, 180.0 - a)
        s1.add_polar(b1 + s, 180.0)
        # stitching 2 halves together
        bend_shape = s1.reversed().v_mirror_copy(mirror_plane_y=-r) + s1.h_mirror_copy().v_mirror_copy(
                mirror_plane_y=-r)

        # assigning the shape to the bus
        bend_lv.set(shape=bend_shape,
                            draw_control_shape=False)
        return bus

    def _default_bend(self):
        bend = asp.CircularBend(trace_template=self.trace_template)
        bend_lv = bend.Layout(angle=180,
                              bend_radius=self.bend_radius,
                              straight_length=0
                   )
        return bend

    def _default_insts(self):
        bus = asp.RoundedRibWaveguide(trace_template=self.trace_template)
        return {
            "bend1": self.bend,
            "bend2": self.bend,
            "bus": self.bus,
        }
    
    def _default_specs(self):
        specs = [
            i3.Place("bend1", (-self.straight_length * 0.5, 0)),
            i3.FlipH("bend1"),
            i3.Place("bend2", (self.straight_length * 0.5, 0)),
            i3.Place("bus", (0, -self.coupler_spacing)),
            i3.ConnectManhattan("bend1:in", "bend2:in",
                                   trace_template=self.trace_template),
            i3.ConnectManhattan("bend1:out", "bend2:out",
                                   trace_template=self.trace_template)                    
        ]
        return specs
        
    def _default_exposed_ports(self):
        return {"bus:in":"in", "bus:out":"out"}

class RaceTrack(_RaceTrack):
    pass

class RaceTrackEuler(_RaceTrack):
    def _default_bend(self):
        bend = asp.EulerBend(trace_template=self.trace_template)
        bend_lv = bend.Layout(angle=180,
                              bend_radius=self.bend_radius,
                              straight_length=0
                   )
        return bend
    
class RingGC(i3.Circuit):
    ring=i3.ChildCellProperty(doc="ring")
    gc=i3.ChildCellProperty(default=asp.GRATING_COUPLER_TE1550_RIBY(), doc="grating coupler")
    trace_template=i3.TraceTemplateProperty(default=asp.RWG1000(), doc="the trace template for the waveguide")

    def _default_insts(self):
        
        return {
            "ring": self.ring,
            "gc1": self.gc,
            "gc2": self.gc,
        }
    
    def _default_specs(self):

        return [
            i3.Place("ring", (0, 0)),
            i3.Place("gc1", (-100, 0), relative_to="ring:in"),
            i3.Place("gc2", (100, 0), relative_to="ring:out", angle=180),
            
            i3.ConnectManhattan([("ring:in", "gc1:out"),
                            ("ring:out", "gc2:out")
                            ], 
                            trace_template=self.trace_template
                        ),  
        ]
    
    def _default_exposed_ports(self):
        return {"gc1:vertical_in": "in", "gc2:vertical_in": "out"}



#ring = RaceTrackEuler()
#ring_gc = RingGC(ring=ring)
#ring_gc_lv = ring_gc.Layout()
#ring_gc_lv.visualize(annotate=True)

