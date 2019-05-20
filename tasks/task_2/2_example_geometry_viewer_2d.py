#!/usr/bin/env python3

"""example_isotope_plot.py: plots few 2D views of a simple geometry ."""

__author__      = "Jonathan Shimwell"

import openmc
import matplotlib.pyplot as plt

mats = openmc.Materials()

natural_lead = openmc.Material(1, "natural_lead")
natural_lead.add_element('Pb', 1,'ao')
natural_lead.set_density('g/cm3', 11.34)
mats.append(natural_lead)


natural_copper = openmc.Material(2, "natural_copper") #hint this is an example material you will need another one called natural_tungsten ,density is 19.3
natural_copper.add_element('Cu', 1,'ao')
natural_copper.set_density('g/cm3', 8.96)
mats.append(natural_copper)


shield_material = openmc.Material(3, "mixed_tungsten_water")
shield_material.add_element('W', 0.9, 'ao')
shield_material.add_element('Cu', 0.1, 'ao')
mats.append(shield_material)


mats.export_to_xml()



#example surfaces
surface_sph1 = openmc.Sphere(R=500) #hint, change the radius of this shpere to 500
surface_sph2 = openmc.Sphere(R=600) #hint, change the radius of this shpere to 500+100
surface_sph3=openmc.Sphere(R=480)
surface_cy=openmc.ZCylinder(r=100)
surface_up_zp=openmc.ZPlane(z0=600)
surface_low_zp=openmc.ZPlane(z0=-600)
surface_cy_2=openmc.ZCylinder(r=140)

#add more surfaces here using https://openmc.readthedocs.io/en/stable/usersguide/geometry.html#surfaces-and-regions

volume_sph1 = +surface_sph1 & -surface_sph2 # above (+) surface_sph and below (-) surface_sph2
capped_cy= -surface_cy & -surface_up_zp & +surface_low_zp
first_wall= -surface_sph1 & +surface_sph3
shield= -surface_cy_2 & +surface_cy & -surface_up_zp & +surface_low_zp


#example cell
cell_1 = openmc.Cell(region=capped_cy)
cell_1.fill = natural_copper #assigning a material to a cell
cell_2 = openmc.Cell(region=first_wall)
cell_2.fill = shield_material
cell_3 = openmc.Cell(region=shield)
cell_3.fill = shield_material
cell_4 = openmc.Cell(region=volume_sph1)
cell_4.fill = natural_lead



#add more cells here

universe = openmc.Universe(cells=[cell_1, cell_2, cell_3, cell_4]) #hint, this list will need to include the new cell

plt.show(universe.plot(width=(2000,2000),basis='xz',colors={cell_1: 'blue', cell_2: 'yellow', cell_3: 'green', cell_4: 'red'})) #hint the width might need to be increased so you can see the new model
plt.show(universe.plot(width=(2000,2000),basis='xy',colors={cell_1: 'blue', cell_2: 'yellow', cell_3: 'green', cell_4: 'red'}))
plt.show(universe.plot(width=(2000,2000),basis='yz',colors={cell_1: 'blue', cell_2: 'yellow', cell_3: 'green', cell_4: 'red'}))

geom = openmc.Geometry(universe)





