import sys

# Need to update the folder that contains asp_sin_lnoi_photonics/ipkiss


# sys.path.append("C:/pdk/asp_sin_lnoi_photonics/ipkiss")
# sys.path.append("H:/GitHub/asp_sin_lnoi_photonics/ipkiss")
sys.path.append("C:/Users/Administrator/Documents/GitHub/pdk/asp_sin_lnoi_photonics/ipkiss")
import asp_sin_lnoi_photonics.technology
import asp_sin_lnoi_photonics.all as asp
import ipkiss3.all as i3
import numpy as np



points = []
radius = 180
for i in range(101):
    x_axis = (radius+23*0.5) * np.cos(i*np.pi/100) - radius - 23*0.5
    y_axis = radius * np.sin(i*np.pi/100)
    points.append((-x_axis,y_axis))

print(points)

ring = asp.RacetrackNotchCircularResonator()
ring_layout = ring.Layout()

ring_layout.visualize()
ring_layout.write_gdsii("ring_exp.gds")
